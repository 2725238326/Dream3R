"""Foundation3R proposal-free native reconstruction model.

This module is a contract-first scaffold for the real independent 3R line:

``RGB images + optional Dream state -> pointmap / confidence``

It deliberately does not accept proposal pointmaps, expert confidences, teacher
pointmaps, or teacher model calls in ``forward``.
"""

from __future__ import annotations

from typing import Dict, Optional

import torch
import torch.nn as nn


class Foundation3RDecoder(nn.Module):
    """Predict dense patch pointmaps directly from RGB windows."""

    def __init__(
        self,
        d_memory: int,
        image_channels: int = 3,
        patch_size: int = 16,
        model_dim: int = 128,
        state_dim: int = 64,
        hidden: int = 256,
        num_layers: int = 2,
        num_heads: int = 4,
        use_state: bool = True,
    ):
        super().__init__()
        self.d_memory = int(d_memory)
        self.image_channels = int(image_channels)
        self.patch_size = int(patch_size)
        self.model_dim = int(model_dim)
        self.state_dim = int(state_dim)
        self.use_state = bool(use_state)

        self.image_encoder = nn.Conv2d(
            self.image_channels,
            self.model_dim,
            kernel_size=self.patch_size,
            stride=self.patch_size,
        )
        self.coord_proj = nn.Linear(2, self.model_dim)
        self.context_proj = nn.Linear(self.d_memory, self.state_dim)
        self.state_to_model = nn.Linear(self.state_dim + 1, self.model_dim)
        self.state_gate = nn.Sequential(
            nn.LayerNorm(self.model_dim),
            nn.Linear(self.model_dim, self.model_dim),
            nn.Sigmoid(),
        )
        self.state_scale = nn.Sequential(
            nn.LayerNorm(self.model_dim),
            nn.Linear(self.model_dim, self.model_dim),
            nn.Tanh(),
        )
        self.state_shift = nn.Sequential(
            nn.LayerNorm(self.model_dim),
            nn.Linear(self.model_dim, self.model_dim),
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
        self.multi_view_mixer = nn.TransformerEncoder(enc_layer, num_layers=num_layers)
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

    @staticmethod
    def _patch_grid(
        grid_h: int,
        grid_w: int,
        device: torch.device,
        dtype: torch.dtype,
    ) -> torch.Tensor:
        ys = torch.linspace(-1.0, 1.0, grid_h, device=device, dtype=dtype)
        xs = torch.linspace(-1.0, 1.0, grid_w, device=device, dtype=dtype)
        yy, xx = torch.meshgrid(ys, xs, indexing="ij")
        return torch.stack([xx, yy], dim=-1).reshape(grid_h * grid_w, 2)

    def _encode_images(self, images: torch.Tensor) -> torch.Tensor:
        if images.dim() != 5:
            raise ValueError(f"images must be [B,N,C,H,W], got {tuple(images.shape)}")
        b, n, c, h, w = images.shape
        if c != self.image_channels:
            raise ValueError(f"expected {self.image_channels} image channels, got {c}")
        if h % self.patch_size != 0 or w % self.patch_size != 0:
            raise ValueError(
                f"image H/W must be divisible by patch_size={self.patch_size}, got {(h, w)}"
            )
        flat = images.reshape(b * n, c, h, w)
        conv = self.image_encoder(flat)
        grid_h, grid_w = conv.shape[-2:]
        encoded = conv.flatten(2).transpose(1, 2)
        coords = self._patch_grid(grid_h, grid_w, images.device, encoded.dtype)
        coord_tokens = self.coord_proj(coords).view(1, 1, grid_h * grid_w, self.model_dim)
        return encoded.reshape(b, n, encoded.shape[1], self.model_dim) + coord_tokens

    def forward(
        self,
        images: torch.Tensor,
        memory_context: Optional[torch.Tensor] = None,
        conflict_score: Optional[torch.Tensor] = None,
    ) -> Dict[str, torch.Tensor]:
        tokens = self._encode_images(images)
        b, n, p, _ = tokens.shape
        device = images.device
        dtype = tokens.dtype
        grid_h = images.shape[-2] // self.patch_size
        grid_w = images.shape[-1] // self.patch_size

        state = self._state_embedding(b, memory_context, conflict_score, device, dtype)
        gated_state = self.state_gate(state).view(b, 1, 1, self.model_dim) * state.view(
            b, 1, 1, self.model_dim
        )
        state_scale = 0.25 * self.state_scale(state).view(b, 1, 1, self.model_dim)
        state_shift = 0.25 * self.state_shift(state).view(b, 1, 1, self.model_dim)
        fused = tokens * (1.0 + state_scale) + state_shift + gated_state

        mixed = self.multi_view_mixer(
            fused.permute(0, 2, 1, 3).reshape(b * p, n, self.model_dim)
        )
        mixed = mixed.reshape(b, p, n, self.model_dim).permute(0, 2, 1, 3)
        raw = self.point_head(mixed)
        coords = self._patch_grid(
            grid_h,
            grid_w,
            device,
            raw.dtype,
        ).view(1, 1, p, 2)
        depth = torch.nn.functional.softplus(raw[..., 2:3]) + 1e-3
        xy = (coords + 0.25 * torch.tanh(raw[..., :2])) * depth
        pointmap = torch.cat([xy, depth], dim=-1)
        confidence = torch.sigmoid(self.confidence_head(mixed))
        return {
            "pointmap": pointmap,
            "final_pointmap": pointmap,
            "confidence": confidence,
            "final_confidence": confidence,
            "proposal_inputs_used": torch.tensor(False, device=device),
            "teacher_used_at_inference": torch.tensor(False, device=device),
            "state_modulation_used": torch.tensor(self.use_state, device=device),
        }


class Foundation3RVGGTFeatureDecoder(nn.Module):
    """Proposal-free decoder over cached or live VGGT-Omega patch features.

    This class treats VGGT-Omega as a pretrained visual representation source.
    It does not consume VGGT pointmaps, proposal pointmaps, expert confidences,
    or teacher targets at inference.
    """

    def __init__(
        self,
        d_vggt_feature: int,
        d_memory: int,
        model_dim: int = 128,
        state_dim: int = 64,
        hidden: int = 256,
        num_layers: int = 2,
        num_heads: int = 4,
        use_state: bool = True,
    ):
        super().__init__()
        self.d_vggt_feature = int(d_vggt_feature)
        self.d_memory = int(d_memory)
        self.model_dim = int(model_dim)
        self.state_dim = int(state_dim)
        self.use_state = bool(use_state)

        self.feature_proj = nn.Sequential(
            nn.LayerNorm(self.d_vggt_feature),
            nn.Linear(self.d_vggt_feature, self.model_dim),
        )
        self.coord_proj = nn.Linear(2, self.model_dim)
        self.context_proj = nn.Linear(self.d_memory, self.state_dim)
        self.state_to_model = nn.Linear(self.state_dim + 1, self.model_dim)
        self.state_gate = nn.Sequential(
            nn.LayerNorm(self.model_dim),
            nn.Linear(self.model_dim, self.model_dim),
            nn.Sigmoid(),
        )
        self.state_scale = nn.Sequential(
            nn.LayerNorm(self.model_dim),
            nn.Linear(self.model_dim, self.model_dim),
            nn.Tanh(),
        )
        self.state_shift = nn.Sequential(
            nn.LayerNorm(self.model_dim),
            nn.Linear(self.model_dim, self.model_dim),
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
        self.multi_view_mixer = nn.TransformerEncoder(enc_layer, num_layers=num_layers)
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
        vggt_patch_features: torch.Tensor,
        memory_context: Optional[torch.Tensor] = None,
        conflict_score: Optional[torch.Tensor] = None,
    ) -> Dict[str, torch.Tensor]:
        if vggt_patch_features.dim() != 4:
            raise ValueError(
                "vggt_patch_features must be [B,N,P,C], "
                f"got {tuple(vggt_patch_features.shape)}"
            )
        b, n, p, c = vggt_patch_features.shape
        if c != self.d_vggt_feature:
            raise ValueError(f"expected {self.d_vggt_feature} VGGT feature channels, got {c}")
        side = int(p ** 0.5)
        if side * side != p:
            raise ValueError(f"patch count must be square for ray output, got {p}")

        device = vggt_patch_features.device
        dtype = vggt_patch_features.dtype
        tokens = self.feature_proj(vggt_patch_features)
        coords = Foundation3RDecoder._patch_grid(side, side, device, dtype)
        tokens = tokens + self.coord_proj(coords).view(1, 1, p, self.model_dim)

        state = self._state_embedding(b, memory_context, conflict_score, device, dtype)
        gated_state = self.state_gate(state).view(b, 1, 1, self.model_dim) * state.view(
            b, 1, 1, self.model_dim
        )
        state_scale = 0.25 * self.state_scale(state).view(b, 1, 1, self.model_dim)
        state_shift = 0.25 * self.state_shift(state).view(b, 1, 1, self.model_dim)
        fused = tokens * (1.0 + state_scale) + state_shift + gated_state
        mixed = self.multi_view_mixer(
            fused.permute(0, 2, 1, 3).reshape(b * p, n, self.model_dim)
        )
        mixed = mixed.reshape(b, p, n, self.model_dim).permute(0, 2, 1, 3)
        raw = self.point_head(mixed)
        depth = torch.nn.functional.softplus(raw[..., 2:3]) + 1e-3
        # The current VGGT-Omega dense teacher cache is a depth-to-pointmap
        # proxy with x/y set to zero. Keep the student target-compatible and
        # let patch coordinates enter through tokens, not the supervised output.
        xy = torch.zeros_like(raw[..., :2])
        pointmap = torch.cat([xy, depth], dim=-1)
        confidence = torch.sigmoid(self.confidence_head(mixed))
        return {
            "pointmap": pointmap,
            "final_pointmap": pointmap,
            "confidence": confidence,
            "final_confidence": confidence,
            "proposal_inputs_used": torch.tensor(False, device=device),
            "teacher_used_at_inference": torch.tensor(False, device=device),
            "vggt_backbone_features_used": torch.tensor(True, device=device),
            "state_modulation_used": torch.tensor(self.use_state, device=device),
        }
