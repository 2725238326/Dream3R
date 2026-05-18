"""Dependency-free 3D Gaussian parameter contract.

This module intentionally does not render. It only predicts bounded Gaussian
parameters so W18 can be tested without `gsplat` or rasterizer dependencies.
"""

from typing import Dict, Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


class GaussianHead(nn.Module):
    """Predict pure tensor Gaussian parameters from tokens and point means."""

    def __init__(self, d_input: int, min_scale: float = 1e-4):
        super().__init__()
        self.min_scale = min_scale
        self.scale_head = nn.Linear(d_input, 3)
        self.rotation_head = nn.Linear(d_input, 4)
        self.color_head = nn.Linear(d_input, 3)
        self.opacity_head = nn.Linear(d_input, 1)

    def forward(self,
                tokens: torch.Tensor,
                means: torch.Tensor,
                confidence: Optional[torch.Tensor] = None,
                source_anchor_ids: Optional[torch.Tensor] = None
                ) -> Dict[str, torch.Tensor]:
        """
        Args:
            tokens: [B, G, D]
            means: [B, G, 3]
            confidence: optional [B, G, 1]
            source_anchor_ids: optional [B, G], -1 for frame-token Gaussians
        """
        if tokens.dim() != 3:
            raise ValueError("tokens must have shape [B, G, D]")
        if means.shape[:2] != tokens.shape[:2] or means.shape[-1] != 3:
            raise ValueError("means must have shape [B, G, 3]")
        if confidence is not None and confidence.shape != (*tokens.shape[:2], 1):
            raise ValueError("confidence must have shape [B, G, 1]")

        B, G, _ = tokens.shape
        scales = F.softplus(self.scale_head(tokens)) + self.min_scale
        rotations = F.normalize(self.rotation_head(tokens), dim=-1, eps=1e-6)
        colors = torch.sigmoid(self.color_head(tokens))
        opacity = torch.sigmoid(self.opacity_head(tokens))
        if confidence is not None:
            opacity = 0.5 * (opacity + confidence.clamp(0.0, 1.0))

        if source_anchor_ids is None:
            source_anchor_ids = torch.full(
                (B, G), -1, dtype=torch.long, device=tokens.device
            )
        elif source_anchor_ids.shape != (B, G):
            raise ValueError("source_anchor_ids must have shape [B, G]")

        return {
            "means": means,
            "scales": scales,
            "rotations": rotations,
            "colors": colors,
            "opacity": opacity,
            "source_anchor_ids": source_anchor_ids,
        }
