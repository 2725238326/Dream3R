"""Deterministic image-derived fallback outputs for expert adapters."""

from typing import Dict, Optional

import torch
import torch.nn.functional as F

from .base_adapter import ExpertOutput


def image_fallback_output(images: torch.Tensor, expert: str, regime: str,
                          n_evidence: int = 17, d_evidence: int = 32,
                          patch_grid: int = 14,
                          metadata: Optional[Dict[str, object]] = None) -> ExpertOutput:
    B, N = images.shape[:2]
    P = patch_grid * patch_grid
    pooled = F.adaptive_avg_pool2d(
        images.reshape(B * N, *images.shape[2:]), (patch_grid, patch_grid)
    ).reshape(B, N, 3, P).permute(0, 1, 3, 2)

    y = torch.linspace(-1.0, 1.0, patch_grid, device=images.device)
    x = torch.linspace(-1.0, 1.0, patch_grid, device=images.device)
    yy, xx = torch.meshgrid(y, x, indexing="ij")
    grid = torch.stack([xx, yy], dim=-1).reshape(1, 1, P, 2).expand(B, N, P, 2)

    depth = pooled.mean(dim=-1, keepdim=True)
    pointmap = torch.cat([grid, depth], dim=-1)
    confidence = pooled.var(dim=-1, keepdim=True).neg().exp().clamp(0.05, 1.0)

    stats = torch.cat([pooled.mean(dim=2), pooled.std(dim=2)], dim=-1)
    repeat = (n_evidence * d_evidence + stats.shape[-1] - 1) // stats.shape[-1]
    evidence = stats.repeat(1, 1, repeat)[..., :n_evidence * d_evidence]
    evidence = evidence.view(B, N, n_evidence, d_evidence)

    out_meta = {
        "expert": expert,
        "regime": regime,
        "backend": "deterministic_fallback",
        "is_loaded": False,
    }
    if metadata:
        out_meta.update(metadata)

    return ExpertOutput(
        pointmap=pointmap,
        confidence=confidence,
        evidence_tokens=evidence,
        metadata=out_meta,
    )
