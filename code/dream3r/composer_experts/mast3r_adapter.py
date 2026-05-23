"""MASt3R adapter -- static multi-view matching and reconstruction."""

import os
import sys
import time
from pathlib import Path
from typing import Dict, Optional

import torch
import torch.nn.functional as F

from .base_adapter import ExpertAdapter, ExpertOutput


DEFAULT_MAST3R_REPO = "/hdd3/kykt26/code/mast3r"
DEFAULT_MAST3R_CHECKPOINT = "/hdd3/kykt26/checkpoints/mast3r-vitl"


class MASt3RAdapter(ExpertAdapter):

    name = "mast3r"
    capability_card = {
        "indoor_static": 0.9,
        "outdoor_static": 0.85,
        "dynamic_scene": 0.3,
        "sparse_view": 0.7,
        "dense_sequential": 0.5,
    }
    latency_estimate_ms = 35.0
    attention_regime = "full"

    def __init__(self, d_out: int = 768, n_evidence: int = 17,
                 d_evidence: int = 32,
                 repo_path: Optional[str] = None,
                 checkpoint_path: Optional[str] = None,
                 patch_grid: int = 14,
                 **kwargs):
        self.d_out = d_out
        self.n_evidence = n_evidence
        self.d_evidence = d_evidence
        self.patch_grid = patch_grid
        self.repo_path = repo_path or os.environ.get("MAST3R_REPO", DEFAULT_MAST3R_REPO)
        self.checkpoint_path = checkpoint_path or os.environ.get(
            "MAST3R_CHECKPOINT", DEFAULT_MAST3R_CHECKPOINT
        )
        self._model = None
        self._model_device = None
        self._loaded = False
        self._load_error: Optional[str] = None

    def _ensure_repo_path(self):
        repo = str(Path(self.repo_path))
        if repo not in sys.path:
            sys.path.insert(0, repo)

    def _load_real_model(self, path: str, device: torch.device):
        self._ensure_repo_path()
        import mast3r.utils.path_to_dust3r  # noqa: F401
        from mast3r.model import AsymmetricMASt3R

        model = AsymmetricMASt3R.from_pretrained(path).to(device)
        model.eval()
        for param in model.parameters():
            param.requires_grad = False
        self._model = model
        self._model_device = device
        self._loaded = True
        self._load_error = None

    def _fallback_forward(self, images: torch.Tensor) -> ExpertOutput:
        B, N = images.shape[:2]
        P = self.patch_grid * self.patch_grid
        pooled = F.adaptive_avg_pool2d(
            images.reshape(B * N, *images.shape[2:]), (self.patch_grid, self.patch_grid)
        ).reshape(B, N, 3, P).permute(0, 1, 3, 2)

        y = torch.linspace(-1.0, 1.0, self.patch_grid, device=images.device)
        x = torch.linspace(-1.0, 1.0, self.patch_grid, device=images.device)
        yy, xx = torch.meshgrid(y, x, indexing="ij")
        grid = torch.stack([xx, yy], dim=-1).reshape(1, 1, P, 2).expand(B, N, P, 2)

        depth = pooled.mean(dim=-1, keepdim=True)
        pointmap = torch.cat([grid, depth], dim=-1)
        confidence = pooled.var(dim=-1, keepdim=True).neg().exp().clamp(0.05, 1.0)

        stats = torch.cat([
            pooled.mean(dim=2),
            pooled.std(dim=2),
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
                "regime": "static_matching",
                "backend": "deterministic_fallback",
                "is_loaded": False,
                "checkpoint_path": self.checkpoint_path,
                "load_error": self._load_error,
            },
        )

    def _real_forward(self, images: torch.Tensor) -> ExpertOutput:
        if self._model is None:
            raise RuntimeError("MASt3R model is not loaded")
        device = images.device
        if self._model_device != device:
            self._model = self._model.to(device)
            self._model_device = device

        B, N = images.shape[:2]
        img1 = images[:, 0]
        img2 = images[:, 1] if N >= 2 else images[:, 0]
        H, W = img1.shape[-2:]
        shape = torch.tensor([[H, W]], device=device).expand(B, -1)
        view1 = {
            "img": img1,
            "true_shape": shape,
            "idx": torch.zeros(B, dtype=torch.long, device=device),
            "instance": ["0"] * B,
        }
        view2 = {
            "img": img2,
            "true_shape": shape,
            "idx": torch.ones(B, dtype=torch.long, device=device),
            "instance": ["1"] * B,
        }

        t0 = time.perf_counter()
        with torch.no_grad():
            pred1, pred2 = self._model(view1, view2)
        if device.type == "cuda":
            torch.cuda.synchronize(device)
        latency_ms = (time.perf_counter() - t0) * 1000

        pts1 = pred1["pts3d"].permute(0, 3, 1, 2)
        conf1 = pred1.get("conf")
        if conf1 is None:
            conf1 = torch.ones(pts1.shape[0], pts1.shape[2], pts1.shape[3], device=device)
        conf1 = conf1.unsqueeze(1)

        pointmap_1 = F.adaptive_avg_pool2d(
            pts1, (self.patch_grid, self.patch_grid)
        ).permute(0, 2, 3, 1).reshape(B, 1, -1, 3)
        conf_1 = F.adaptive_avg_pool2d(
            conf1, (self.patch_grid, self.patch_grid)
        ).permute(0, 2, 3, 1).reshape(B, 1, -1, 1).sigmoid()

        if N > 1:
            pointmap = pointmap_1.expand(B, N, pointmap_1.shape[2], 3).contiguous()
            confidence = conf_1.expand(B, N, conf_1.shape[2], 1).contiguous()
        else:
            pointmap = pointmap_1
            confidence = conf_1

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
                "regime": "static_matching",
                "backend": "mast3r",
                "is_loaded": True,
                "checkpoint_path": self.checkpoint_path,
                "latency_ms": latency_ms,
            },
        )

    def forward(self, images: torch.Tensor,
                context: Optional[Dict[str, torch.Tensor]] = None,
                ) -> ExpertOutput:
        if self._loaded:
            return self._real_forward(images)
        return self._fallback_forward(images)

    def load_checkpoint(self, path: Optional[str] = None) -> None:
        checkpoint = path or self.checkpoint_path
        if not checkpoint or not Path(checkpoint).exists():
            self._loaded = False
            self._load_error = f"checkpoint not found: {checkpoint}"
            raise FileNotFoundError(self._load_error)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.checkpoint_path = checkpoint
        self._load_real_model(checkpoint, device)

    def is_available(self) -> bool:
        return Path(self.checkpoint_path).exists() and Path(self.repo_path).exists()

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    @property
    def load_error(self) -> Optional[str]:
        return self._load_error
