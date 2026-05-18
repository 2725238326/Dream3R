"""Spann3R adapter -- sequential/streaming spatial reconstruction."""

import importlib.util
import os
import sys
import time
from pathlib import Path
from typing import Dict, Optional

import torch
import torch.nn.functional as F

from .base_adapter import ExpertAdapter, ExpertOutput
from .fallback import image_fallback_output


DEFAULT_SPANN3R_REPO = "/hdd3/kykt26/code/spann3r"
DEFAULT_SPANN3R_CHECKPOINT = "/hdd3/kykt26/code/spann3r/checkpoints/spann3r.pth"
DEFAULT_DUST3R_CHECKPOINT = "/hdd3/kykt26/code/spann3r/checkpoints/DUSt3R_ViTLarge_BaseDecoder_512_dpt.pth"


class Spann3RAdapter(ExpertAdapter):

    name = "spann3r"
    capability_card = {
        "indoor_static": 0.6,
        "outdoor_static": 0.7,
        "dynamic_scene": 0.4,
        "sparse_view": 0.5,
        "dense_sequential": 0.95,
    }
    latency_estimate_ms = 28.0
    attention_regime = "sparse"

    def __init__(self, d_out: int = 768, n_evidence: int = 17,
                 d_evidence: int = 32,
                 repo_path: Optional[str] = None,
                 checkpoint_path: Optional[str] = None,
                 dust3r_checkpoint: Optional[str] = None,
                 patch_grid: int = 14,
                 **kwargs):
        self.d_out = d_out
        self.n_evidence = n_evidence
        self.d_evidence = d_evidence
        self.patch_grid = patch_grid
        self.repo_path = repo_path or os.environ.get("SPANN3R_REPO", DEFAULT_SPANN3R_REPO)
        self.checkpoint_path = checkpoint_path or os.environ.get(
            "SPANN3R_CHECKPOINT", DEFAULT_SPANN3R_CHECKPOINT
        )
        self.dust3r_checkpoint = dust3r_checkpoint or os.environ.get(
            "SPANN3R_DUST3R_CHECKPOINT", DEFAULT_DUST3R_CHECKPOINT
        )
        self._model = None
        self._model_device = None
        self._loaded = False
        self._load_error: Optional[str] = None

    def _missing_dependency(self) -> Optional[str]:
        repo = Path(self.repo_path)
        if not repo.exists():
            return f"repo not found: {repo}"
        for module in ("cv2", "einops"):
            if importlib.util.find_spec(module) is None:
                return f"missing dependency: {module}"
        return None

    def _ensure_repo_path(self):
        repo = Path(self.repo_path)
        for entry in (repo, repo / "dust3r", repo / "croco"):
            path = str(entry)
            if path not in sys.path:
                sys.path.insert(0, path)

    def _load_real_model(self, checkpoint_path: str, device: torch.device):
        self._ensure_repo_path()
        from spann3r.model import Spann3R

        model = Spann3R(dus3r_name=self.dust3r_checkpoint, use_feat=False).to(device)
        payload = torch.load(checkpoint_path, map_location=device)
        state_dict = payload["model"] if isinstance(payload, dict) and "model" in payload else payload
        model.load_state_dict(state_dict)
        model.eval()
        for param in model.parameters():
            param.requires_grad = False

        self._model = model
        self._model_device = device
        self._loaded = True
        self._load_error = None

    def _build_frames(self, images: torch.Tensor):
        B, N, _, H, W = images.shape
        true_shape = torch.tensor([[H, W]], device=images.device).expand(B, -1)
        normalized = images.clamp(-1.0, 1.0)
        frames = []
        for idx in range(N):
            frames.append({
                "img": normalized[:, idx],
                "true_shape": true_shape,
                "idx": torch.full((B,), idx, dtype=torch.long, device=images.device),
                "instance": [str(idx)] * B,
            })
        return frames

    def _real_forward(self, images: torch.Tensor) -> ExpertOutput:
        if self._model is None:
            raise RuntimeError("Spann3R model is not loaded")
        if images.shape[1] < 2:
            return image_fallback_output(
                images, self.name, "streaming_spatial",
                self.n_evidence, self.d_evidence,
                metadata={
                    "attention_regime": self.attention_regime,
                    "backend": "deterministic_fallback",
                    "load_error": "Spann3R real path requires at least two views",
                },
            )

        device = images.device
        if self._model_device != device:
            self._model = self._model.to(device)
            self._model_device = device

        B, N = images.shape[:2]
        frames = self._build_frames(images)
        t0 = time.perf_counter()
        with torch.no_grad():
            preds, _ = self._model.forward(frames)
        if device.type == "cuda":
            torch.cuda.synchronize(device)
        latency_ms = (time.perf_counter() - t0) * 1000

        pointmaps = []
        confidences = []
        for idx, pred in enumerate(preds[:N]):
            point_key = "pts3d" if idx == 0 else "pts3d_in_other_view"
            pts = pred[point_key].permute(0, 3, 1, 2)
            conf = pred["conf"].unsqueeze(1)
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
                "regime": "streaming_spatial",
                "backend": "spann3r",
                "is_loaded": True,
                "checkpoint_path": self.checkpoint_path,
                "dust3r_checkpoint": self.dust3r_checkpoint,
                "latency_ms": latency_ms,
            },
        )

    def forward(self, images: torch.Tensor,
                context: Optional[Dict[str, torch.Tensor]] = None,
                ) -> ExpertOutput:
        if self._loaded:
            return self._real_forward(images)
        return image_fallback_output(
            images, self.name, "streaming_spatial",
            self.n_evidence, self.d_evidence,
            metadata={
                "attention_regime": self.attention_regime,
                "checkpoint_path": self.checkpoint_path,
                "load_error": self._load_error,
            },
        )

    def load_checkpoint(self, path: Optional[str] = None) -> None:
        checkpoint_path = Path(path or self.checkpoint_path)
        if not checkpoint_path.exists():
            self._loaded = False
            self._load_error = f"checkpoint not found: {checkpoint_path}"
            raise FileNotFoundError(self._load_error)
        dust3r_path = Path(self.dust3r_checkpoint)
        if not dust3r_path.exists():
            self._loaded = False
            self._load_error = f"DUSt3R checkpoint not found: {dust3r_path}"
            raise FileNotFoundError(self._load_error)
        missing = self._missing_dependency()
        if missing is not None:
            self._loaded = False
            self._load_error = missing
            raise ImportError(missing)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.checkpoint_path = str(checkpoint_path)
        self._load_real_model(str(checkpoint_path), device)

    def is_available(self) -> bool:
        return (
            Path(self.repo_path).exists()
            and Path(self.checkpoint_path).exists()
            and Path(self.dust3r_checkpoint).exists()
            and self._missing_dependency() is None
        )

    def has_checkpoint_artifacts(self) -> bool:
        return (
            Path(self.repo_path).exists()
            and Path(self.checkpoint_path).exists()
            and Path(self.dust3r_checkpoint).exists()
        )

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    @property
    def load_error(self) -> Optional[str]:
        return self._load_error
