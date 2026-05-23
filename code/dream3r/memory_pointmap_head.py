"""External memory-conditioned residual head for pointmap correction."""

from typing import Dict, Tuple

import torch
import torch.nn as nn


class MemoryPointmapResidualHead(nn.Module):
    """Predicts a small global pointmap residual from SpatialMemory state."""

    def __init__(
        self,
        d_memory: int = 128,
        hidden_dim: int = 64,
        max_scale: float = 0.5,
        max_shift: float = 5.0,
    ):
        super().__init__()
        self.max_scale = float(max_scale)
        self.max_shift = float(max_shift)
        self.mlp = nn.Sequential(
            nn.LayerNorm(d_memory),
            nn.Linear(d_memory, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, 7),
        )

    def forward(
        self,
        pointmap: torch.Tensor,
        latent_state_tokens: torch.Tensor,
        prev_pointmap: torch.Tensor | None = None,
        overlap_frames: int = 4,
    ) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
        if pointmap.dim() != 4 or pointmap.shape[-1] != 3:
            raise ValueError("pointmap must have shape [B, N, P, 3]")
        if latent_state_tokens.dim() != 3:
            raise ValueError("latent_state_tokens must have shape [B, S, D]")

        context = latent_state_tokens.mean(dim=1)
        params = self.mlp(context)
        scale = torch.tanh(params[:, :3]) * self.max_scale
        shift = torch.tanh(params[:, 3:6]) * self.max_shift
        blend = torch.sigmoid(params[:, 6:7])
        residual = pointmap * scale[:, None, None, :] + shift[:, None, None, :]
        corrected = pointmap + residual
        if prev_pointmap is not None and overlap_frames > 0:
            overlap = min(overlap_frames, corrected.shape[1], prev_pointmap.shape[1])
            prev_overlap = prev_pointmap[:, -overlap:].detach()
            current_overlap = corrected[:, :overlap]
            corrected = corrected.clone()
            corrected[:, :overlap] = (
                blend[:, None, None] * prev_overlap
                + (1.0 - blend[:, None, None]) * current_overlap
            )
        return corrected, {
            "scale": scale,
            "shift": shift,
            "blend": blend,
            "residual": residual,
        }
