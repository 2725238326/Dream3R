"""Dream3R-U1 image/state native reconstruction decoder.

This non-core decoder is the first usable-model step after DEC-024. Unlike
``NativeStudentDecoder``, it has an image-token reconstruction path and treats
proposal teachers as optional anchors instead of mandatory mixture outputs.
That gives Dream3R a real partial-teacher inference contract:

``image tokens + Dream state + optional proposal anchors -> pointmap``.
"""

from __future__ import annotations

from typing import Dict, Optional

import torch
import torch.nn as nn

from dream3r.state_prior_head import StatePriorHead


class ImageStateStudentDecoder(nn.Module):
    """Image-conditioned native student with optional proposal anchors."""

    def __init__(
        self,
        n_experts: int,
        d_image: int,
        d_memory: int,
        model_dim: int = 128,
        state_dim: int = 64,
        hidden: int = 128,
        prior_hidden: int = 128,
        use_state: bool = True,
        anchor_residual_scale: float = 0.05,
        native_residual_scale: float = 0.05,
    ):
        super().__init__()
        self.n_experts = int(n_experts)
        self.d_image = int(d_image)
        self.d_memory = int(d_memory)
        self.model_dim = int(model_dim)
        self.state_dim = int(state_dim)
        self.use_state = bool(use_state)
        self.anchor_residual_scale = float(anchor_residual_scale)
        self.native_residual_scale = float(native_residual_scale)

        self.image_proj = nn.Linear(self.d_image, self.model_dim)
        self.context_proj = nn.Linear(self.d_memory, self.state_dim)
        self.state_to_model = nn.Linear(self.state_dim + 1, self.model_dim)

        self.state_prior = StatePriorHead(
            n_experts=n_experts,
            d_memory=d_memory,
            state_dim=state_dim,
            hidden=prior_hidden,
            use_state=use_state,
        )

        self.native_point_head = nn.Sequential(
            nn.LayerNorm(self.model_dim),
            nn.Linear(self.model_dim, hidden),
            nn.GELU(),
            nn.Linear(hidden, 3),
        )
        self.anchor_refine_head = nn.Sequential(
            nn.LayerNorm(self.model_dim + 6),
            nn.Linear(self.model_dim + 6, hidden),
            nn.GELU(),
            nn.Linear(hidden, 3),
        )
        self.confidence_head = nn.Sequential(
            nn.LayerNorm(self.model_dim + 4),
            nn.Linear(self.model_dim + 4, hidden),
            nn.GELU(),
            nn.Linear(hidden, 1),
        )

        # Start as an image/native point head plus zero anchor residual. This
        # avoids silently promoting teacher-copy behavior at initialization.
        nn.init.zeros_(self.anchor_refine_head[-1].weight)
        nn.init.zeros_(self.anchor_refine_head[-1].bias)

    def freeze_state_prior(self) -> None:
        for param in self.state_prior.parameters():
            param.requires_grad = False

    def _state_tokens(
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
            state = self.context_proj(memory_context.to(dtype))
        if conflict_score is None:
            conflict = torch.zeros(batch, 1, device=device, dtype=dtype)
        else:
            conflict = conflict_score if conflict_score.dim() == 2 else conflict_score.view(batch, 1)
            conflict = torch.sigmoid(conflict.to(dtype))
        return self.state_to_model(torch.cat([state, conflict], dim=-1))

    @staticmethod
    def _scale_normalize(proposal_pointmaps: torch.Tensor) -> torch.Tensor:
        b, e = proposal_pointmaps.shape[:2]
        z = proposal_pointmaps[..., 2]
        with torch.no_grad():
            med = z.abs().reshape(b, e, -1).median(dim=-1).values.clamp_min(1e-6)
        return proposal_pointmaps / med.view(b, e, 1, 1, 1)

    def _dropout_mask(
        self,
        batch: int,
        proposal_dropout: float,
        device: torch.device,
        dtype: torch.dtype,
    ) -> torch.Tensor:
        if (not self.training) or proposal_dropout <= 0:
            return torch.ones(batch, self.n_experts, 1, 1, device=device, dtype=dtype)
        keep = torch.rand(batch, self.n_experts, device=device) >= float(proposal_dropout)
        empty = ~keep.any(dim=1)
        if bool(empty.any()):
            keep[empty, 0] = True
        return keep.to(dtype).view(batch, self.n_experts, 1, 1)

    def _anchor_from_proposals(
        self,
        proposal_pointmaps: torch.Tensor,
        proposal_confidences: torch.Tensor,
        memory_context: Optional[torch.Tensor],
        conflict_score: Optional[torch.Tensor],
        proposal_dropout: float,
    ) -> Dict[str, torch.Tensor]:
        b = proposal_pointmaps.shape[0]
        pm_norm = self._scale_normalize(proposal_pointmaps)
        prior = self.state_prior(proposal_pointmaps, proposal_confidences, memory_context, conflict_score)
        prior_weights = prior["expert_weights"]
        keep = self._dropout_mask(b, proposal_dropout, proposal_pointmaps.device, proposal_pointmaps.dtype)
        kept = prior_weights * keep
        kept = kept / kept.sum(dim=1, keepdim=True).clamp_min(1e-8)
        anchor = (kept.unsqueeze(-1) * pm_norm).sum(dim=1)
        conf = (kept.unsqueeze(-1) * proposal_confidences.to(pm_norm.dtype)).sum(dim=1)
        disp = (kept.unsqueeze(-1) * (pm_norm - anchor.unsqueeze(1)).pow(2)).sum(dim=1).sqrt()
        entropy = -(kept.clamp_min(1e-8) * kept.clamp_min(1e-8).log()).sum(dim=1, keepdim=True)
        return {
            "anchor_pointmap": anchor,
            "anchor_confidence": conf,
            "anchor_dispersion": disp,
            "prior_weights": prior_weights,
            "kept_prior_weights": kept,
            "kept_mask": keep,
            "prior_entropy": entropy.permute(0, 2, 3, 1),
        }

    def forward(
        self,
        image_tokens: torch.Tensor,
        memory_context: Optional[torch.Tensor] = None,
        conflict_score: Optional[torch.Tensor] = None,
        proposal_pointmaps: Optional[torch.Tensor] = None,
        proposal_confidences: Optional[torch.Tensor] = None,
        proposal_dropout: float = 0.0,
    ) -> Dict[str, torch.Tensor]:
        if image_tokens.dim() != 4:
            raise ValueError(f"image_tokens must be [B,N,P,D], got {tuple(image_tokens.shape)}")
        b, n, p, _ = image_tokens.shape
        dtype = image_tokens.dtype
        device = image_tokens.device

        img = self.image_proj(image_tokens.to(dtype))
        state = self._state_tokens(b, memory_context, conflict_score, device, dtype)
        fused = img + state.view(b, 1, 1, self.model_dim)
        native = self.native_point_head(fused)

        has_anchor = proposal_pointmaps is not None and proposal_confidences is not None
        if has_anchor:
            if proposal_pointmaps.shape[0] != b or proposal_pointmaps.shape[2:4] != (n, p):
                raise ValueError("proposal_pointmaps must align with image_tokens [B,E,N,P,3]")
            anchor = self._anchor_from_proposals(
                proposal_pointmaps,
                proposal_confidences,
                memory_context,
                conflict_score,
                proposal_dropout,
            )
            anchor_pointmap = anchor["anchor_pointmap"]
            anchor_confidence = anchor["anchor_confidence"]
            anchor_disp = anchor["anchor_dispersion"]
            anchor_entropy = anchor["prior_entropy"]
        else:
            anchor_pointmap = native.detach()
            anchor_confidence = torch.zeros(b, n, p, 1, device=device, dtype=dtype)
            anchor_disp = torch.zeros(b, n, p, 3, device=device, dtype=dtype)
            anchor_entropy = torch.zeros(b, n, p, 1, device=device, dtype=dtype)
            anchor = {
                "prior_weights": None,
                "kept_prior_weights": None,
                "kept_mask": None,
            }

        residual_to_anchor = native - anchor_pointmap
        refine_feat = torch.cat(
            [fused, anchor_pointmap, anchor_confidence, anchor_disp.mean(dim=-1, keepdim=True), anchor_entropy],
            dim=-1,
        )
        anchor_delta = torch.tanh(self.anchor_refine_head(refine_feat))
        anchor_delta = anchor_delta * anchor_disp.mean(dim=-1, keepdim=True) * self.anchor_residual_scale
        native_delta = torch.tanh(residual_to_anchor) * self.native_residual_scale
        final = anchor_pointmap + anchor_delta + native_delta
        conf_feat = torch.cat([fused, final, anchor_confidence], dim=-1)
        final_conf = torch.sigmoid(self.confidence_head(conf_feat))

        return {
            "final_pointmap": final,
            "native_pointmap": native,
            "anchor_pointmap": anchor_pointmap,
            "anchor_delta": anchor_delta,
            "native_delta": native_delta,
            "final_confidence": final_conf,
            "prior_weights": anchor["prior_weights"],
            "kept_prior_weights": anchor["kept_prior_weights"],
            "kept_mask": anchor["kept_mask"],
            "has_proposal_anchor": torch.tensor(has_anchor, device=device),
        }
