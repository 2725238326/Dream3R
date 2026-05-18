"""Fast3R adapter -- speed-optimized many-view reconstruction."""

import os
import sys
import time
import importlib.util
from pathlib import Path
from typing import Dict, Optional

import torch
import torch.nn.functional as F

from .base_adapter import ExpertAdapter, ExpertOutput
from .fallback import image_fallback_output


DEFAULT_FAST3R_REPO = "/hdd3/kykt26/code/fast3r"
DEFAULT_FAST3R_CHECKPOINT_DIR = "/hdd3/kykt26/models/fast3r/Fast3R_ViT_Large_512"


def _scaled_dot_product_attention(q, k, v, attn_mask=None, dropout_p=0.0,
                                  is_causal=False, scale=None):
    scale_factor = scale if scale is not None else q.size(-1) ** -0.5
    scores = torch.matmul(q, k.transpose(-2, -1)) * scale_factor
    if is_causal:
        target_length = q.size(-2)
        source_length = k.size(-2)
        causal_mask = torch.ones(
            (target_length, source_length), dtype=torch.bool, device=q.device,
        ).tril(diagonal=0)
        scores = scores.masked_fill(~causal_mask, torch.finfo(scores.dtype).min)
    if attn_mask is not None:
        if attn_mask.dtype == torch.bool:
            scores = scores.masked_fill(~attn_mask, torch.finfo(scores.dtype).min)
        else:
            scores = scores + attn_mask
    weights = torch.softmax(scores, dim=-1)
    if dropout_p and dropout_p > 0:
        weights = F.dropout(weights, dropout_p, training=True)
    return torch.matmul(weights, v)


class Fast3RAdapter(ExpertAdapter):

    name = "fast3r"
    capability_card = {
        "indoor_static": 0.7,
        "outdoor_static": 0.7,
        "dynamic_scene": 0.5,
        "sparse_view": 0.6,
        "dense_sequential": 0.8,
    }
    latency_estimate_ms = 12.0
    attention_regime = "linear"

    def __init__(self, d_out: int = 768, n_evidence: int = 17,
                 d_evidence: int = 32,
                 repo_path: Optional[str] = None,
                 checkpoint_dir: Optional[str] = None,
                 patch_grid: int = 14,
                 **kwargs):
        self.d_out = d_out
        self.n_evidence = n_evidence
        self.d_evidence = d_evidence
        self.patch_grid = patch_grid
        self.repo_path = repo_path or os.environ.get("FAST3R_REPO", DEFAULT_FAST3R_REPO)
        self.checkpoint_dir = checkpoint_dir or os.environ.get(
            "FAST3R_CHECKPOINT_DIR", DEFAULT_FAST3R_CHECKPOINT_DIR
        )
        self._model = None
        self._model_device = None
        self._loaded = False
        self._load_error: Optional[str] = None

    def _missing_dependency(self) -> Optional[str]:
        if importlib.util.find_spec("omegaconf") is None:
            return "missing dependency: omegaconf"
        if importlib.util.find_spec("huggingface_hub") is None:
            return "missing dependency: huggingface_hub"
        return None

    def _ensure_repo_path(self):
        repo = str(Path(self.repo_path))
        if repo not in sys.path:
            sys.path.insert(0, repo)

    def _install_attention_fallback(self):
        try:
            if torch.cuda.is_available():
                torch.backends.cuda.enable_flash_sdp(False)
                torch.backends.cuda.enable_mem_efficient_sdp(False)
                torch.backends.cuda.enable_math_sdp(True)
            from fast3r.croco.models import blocks as fast3r_blocks
            fast3r_blocks.scaled_dot_product_attention = _scaled_dot_product_attention
        except Exception as exc:
            self._load_error = f"attention fallback setup failed: {exc}"

    def _load_real_model(self, checkpoint_dir: str, device: torch.device):
        self._ensure_repo_path()
        from fast3r.models.fast3r import Fast3R

        self._install_attention_fallback()
        try:
            model = Fast3R.from_pretrained(str(checkpoint_dir), attn_implementation="pytorch_naive")
        except TypeError as exc:
            if "attn_implementation" not in str(exc):
                raise
            model = Fast3R.from_pretrained(str(checkpoint_dir))
        model.eval().to(device)
        for param in model.parameters():
            param.requires_grad = False
        self._model = model
        self._model_device = device
        self._loaded = True
        self._load_error = None

    def _build_views(self, images: torch.Tensor):
        B, N, _, H, W = images.shape
        true_shape = torch.tensor([[H, W]], device=images.device).expand(B, -1)
        normalized = images.clamp(-1.0, 1.0)
        views = []
        for idx in range(N):
            views.append({
                "img": normalized[:, idx],
                "true_shape": true_shape,
                "idx": torch.full((B,), idx, dtype=torch.long, device=images.device),
                "instance": [str(idx)] * B,
            })
        return views

    def _real_forward(self, images: torch.Tensor) -> ExpertOutput:
        if self._model is None:
            raise RuntimeError("Fast3R model is not loaded")
        device = images.device
        if self._model_device != device:
            self._model = self._model.to(device)
            self._model_device = device

        B, N = images.shape[:2]
        views = self._build_views(images)
        t0 = time.perf_counter()
        with torch.no_grad():
            preds, profiling_info = self._model(views, profiling=True)
        if device.type == "cuda":
            torch.cuda.synchronize(device)
        latency_ms = (time.perf_counter() - t0) * 1000

        pointmaps = []
        confidences = []
        for pred in preds[:N]:
            pts = pred["pts3d_in_other_view"].permute(0, 3, 1, 2)
            conf = pred.get("conf")
            if conf is None:
                conf = torch.ones(pts.shape[0], pts.shape[2], pts.shape[3], device=device)
            conf = conf.unsqueeze(1)
            pointmaps.append(
                F.adaptive_avg_pool2d(pts, (self.patch_grid, self.patch_grid))
                .permute(0, 2, 3, 1)
                .reshape(B, -1, 3)
            )
            confidences.append(
                F.adaptive_avg_pool2d(conf, (self.patch_grid, self.patch_grid))
                .permute(0, 2, 3, 1)
                .reshape(B, -1, 1)
                .sigmoid()
            )

        pointmap = torch.stack(pointmaps, dim=1)
        confidence = torch.stack(confidences, dim=1)
        stats = torch.cat([
            pointmap.mean(dim=2),
            pointmap.std(dim=2),
            confidence.mean(dim=2),
        ], dim=-1)
        repeat = (self.n_evidence * self.d_evidence + stats.shape[-1] - 1) // stats.shape[-1]
        evidence = stats.repeat(1, 1, repeat)[..., :self.n_evidence * self.d_evidence]
        evidence = evidence.view(B, N, self.n_evidence, self.d_evidence)

        return ExpertOutput(
            pointmap=pointmap,
            confidence=confidence,
            evidence_tokens=evidence,
            metadata={
                "expert": self.name,
                "regime": "speed_optimized",
                "backend": "fast3r",
                "is_loaded": True,
                "checkpoint_dir": self.checkpoint_dir,
                "latency_ms": latency_ms,
                "profiling_info": profiling_info,
            },
        )

    def forward(self, images: torch.Tensor,
                context: Optional[Dict[str, torch.Tensor]] = None,
                ) -> ExpertOutput:
        if self._loaded:
            return self._real_forward(images)
        return image_fallback_output(
            images, self.name, "speed_optimized",
            self.n_evidence, self.d_evidence,
            metadata={
                "attention_regime": self.attention_regime,
                "checkpoint_dir": self.checkpoint_dir,
                "load_error": self._load_error,
            },
        )

    def load_checkpoint(self, path: Optional[str] = None) -> None:
        checkpoint_dir = path or self.checkpoint_dir
        model_file = Path(checkpoint_dir) / "model.safetensors"
        if not model_file.exists():
            self._loaded = False
            self._load_error = f"checkpoint not found: {model_file}"
            raise FileNotFoundError(self._load_error)
        missing = self._missing_dependency()
        if missing is not None:
            self._loaded = False
            self._load_error = missing
            raise ImportError(missing)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.checkpoint_dir = str(checkpoint_dir)
        self._load_real_model(str(checkpoint_dir), device)

    def is_available(self) -> bool:
        return (
            Path(self.repo_path).exists()
            and (Path(self.checkpoint_dir) / "model.safetensors").exists()
            and self._missing_dependency() is None
        )

    def has_checkpoint_artifacts(self) -> bool:
        return Path(self.repo_path).exists() and (Path(self.checkpoint_dir) / "model.safetensors").exists()

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    @property
    def load_error(self) -> Optional[str]:
        return self._load_error
