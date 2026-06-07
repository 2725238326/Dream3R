"""Proposal-free Dream3R native reconstruction decoder.

This module is the clean starting point for an independent Dream3R 3R model:

``image tokens + Dream state -> pointmap``

It deliberately has no proposal-pointmap or expert-confidence inputs. Existing
proposal teachers may still be used offline to build caches or as external
evaluation baselines, but this decoder's inference contract is proposal-free.
"""

from __future__ import annotations

from typing import Dict, Optional

import torch
import torch.nn as nn


class ProposalFree3RDecoder(nn.Module):
    """Predict pointmaps directly from image tokens and optional Dream state."""

    def __init__(
        self,
        d_image: int,
        d_memory: int,
        model_dim: int = 128,
        state_dim: int = 64,
        hidden: int = 128,
        num_layers: int = 2,
        num_heads: int = 4,
        use_state: bool = True,
    ):
        super().__init__()
        self.d_image = int(d_image)
        self.d_memory = int(d_memory)
        self.model_dim = int(model_dim)
        self.state_dim = int(state_dim)
        self.use_state = bool(use_state)

        self.image_proj = nn.Linear(self.d_image, self.model_dim)
        self.context_proj = nn.Linear(self.d_memory, self.state_dim)
        self.state_to_model = nn.Linear(self.state_dim + 1, self.model_dim)
        self.frame_gate = nn.Sequential(
            nn.LayerNorm(self.model_dim),
            nn.Linear(self.model_dim, self.model_dim),
            nn.Sigmoid(),
        )
        enc_layer = nn.TransformerEncoderLayer(
            d_model=self.model_dim,
            nhead=num_heads,
            dim_feedforward=hidden,
            dropout=0.0,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.temporal_mixer = nn.TransformerEncoder(enc_layer, num_layers=num_layers)
        self.point_head = nn.Sequential(
            nn.LayerNorm(self.model_dim),
            nn.Linear(self.model_dim, hidden),
            nn.GELU(),
            nn.Linear(hidden, 3),
        )
        self.confidence_head = nn.Sequential(
            nn.LayerNorm(self.model_dim),
            nn.Linear(self.model_dim, hidden),
            nn.GELU(),
            nn.Linear(hidden, 1),
        )

    def _state_embedding(
        self,
        batch: int,
        memory_context: Optional[torch.Tensor],
        conflict_score: Optional[torch.Tensor],
        device: torch.device,
        dtype: torch.dtype,
    ) -> torch.Tensor:
        if (memory_context is None) or (not self.use_state):
            state = torch.zeros(batch, self.state_dim, device=device, dtype=dtype)
        else:
            state = self.context_proj(memory_context.to(device=device, dtype=dtype))
        if conflict_score is None:
            conflict = torch.zeros(batch, 1, device=device, dtype=dtype)
        else:
            conflict = conflict_score.to(device=device, dtype=dtype)
            conflict = conflict if conflict.dim() == 2 else conflict.view(batch, 1)
            conflict = torch.sigmoid(conflict)
        return self.state_to_model(torch.cat([state, conflict], dim=-1))

    def forward(
        self,
        image_tokens: torch.Tensor,
        memory_context: Optional[torch.Tensor] = None,
        conflict_score: Optional[torch.Tensor] = None,
    ) -> Dict[str, torch.Tensor]:
        if image_tokens.dim() != 4:
            raise ValueError(f"image_tokens must be [B,N,P,D], got {tuple(image_tokens.shape)}")
        b, n, p, _ = image_tokens.shape
        dtype = image_tokens.dtype
        device = image_tokens.device

        img = self.image_proj(image_tokens)
        state = self._state_embedding(b, memory_context, conflict_score, device, dtype)
        gated_state = self.frame_gate(state).view(b, 1, 1, self.model_dim) * state.view(
            b, 1, 1, self.model_dim
        )
        fused = img + gated_state

        # Mix each patch track across frames. This is still proposal-free:
        # the only sequence tokens are image/state features.
        tokens = fused.permute(0, 2, 1, 3).reshape(b * p, n, self.model_dim)
        mixed = self.temporal_mixer(tokens).reshape(b, p, n, self.model_dim).permute(0, 2, 1, 3)
        pointmap = self.point_head(mixed)
        confidence = torch.sigmoid(self.confidence_head(mixed))

        return {
            "pointmap": pointmap,
            "final_pointmap": pointmap,
            "confidence": confidence,
            "final_confidence": confidence,
            "proposal_inputs_used": torch.tensor(False, device=device),
        }
