"""Dream3R native student decoder over cached proposal teachers.

This non-core module is the first native distillation gate after the bounded
frozen-StatePrior baseline. It keeps the DEC-019 StatePrior as an explicit
frozen teacher and trains a compact student residual over that teacher with
proposal dropout. The output is no longer only a convex expert mixture, but
epoch-0 behavior still equals the frozen-prior teacher.
"""

from __future__ import annotations

from typing import Dict, Optional

import torch
import torch.nn as nn

from dream3r.state_prior_head import StatePriorHead


class NativeStudentDecoder(nn.Module):
    """Native student decoder with a frozen StatePrior teacher.

    Args:
        n_experts: number of proposal teachers in the cache.
        d_memory: dimension of ``memory.fused_context``.
        token_dim: hidden width for proposal tokens.
        state_dim: projected Dream-state width.
        hidden: feed-forward width.
        num_layers: number of per-patch proposal mixer layers.
        num_heads: attention heads inside the proposal mixer.
        id_dim: learnable expert identity embedding width.
        use_state: ablation flag; False zeroes Dream state in both teacher and
            student paths.
        prior_hidden: hidden width of the StatePrior teacher MLP.
        residual_scale: residual bound as a multiple of local proposal
            disagreement. Zero-initialized residuals make initial output match
            the frozen-prior teacher exactly when no proposal dropout is used.
    """

    def __init__(
        self,
        n_experts: int,
        d_memory: int,
        token_dim: int = 64,
        state_dim: int = 64,
        hidden: int = 128,
        num_layers: int = 2,
        num_heads: int = 4,
        id_dim: int = 8,
        use_state: bool = True,
        prior_hidden: int = 128,
        residual_scale: float = 0.05,
    ):
        super().__init__()
        self.n_experts = int(n_experts)
        self.d_memory = int(d_memory)
        self.token_dim = int(token_dim)
        self.state_dim = int(state_dim)
        self.id_dim = int(id_dim)
        self.use_state = bool(use_state)
        self.residual_scale = float(residual_scale)

        self.state_prior = StatePriorHead(
            n_experts=n_experts,
            d_memory=d_memory,
            state_dim=state_dim,
            hidden=prior_hidden,
            use_state=use_state,
        )
        self.context_proj = nn.Linear(self.d_memory, self.state_dim)
        self.expert_embed = nn.Parameter(torch.randn(self.n_experts, self.id_dim) * 0.02)

        # xyz + confidence + residual-to-teacher xyz + residual norm +
        # prior weight + available mask + state + conflict + expert id.
        in_dim = 3 + 1 + 3 + 1 + 1 + 1 + self.state_dim + 1 + self.id_dim
        self.input_proj = nn.Linear(in_dim, self.token_dim)
        enc_layer = nn.TransformerEncoderLayer(
            d_model=self.token_dim,
            nhead=num_heads,
            dim_feedforward=hidden,
            dropout=0.0,
            activation="gelu",
            batch_first=True,
            norm_first=True,
        )
        self.mixer = nn.TransformerEncoder(enc_layer, num_layers=num_layers)
        self.residual_head = nn.Sequential(
            nn.Linear(self.token_dim + 2, hidden),
            nn.GELU(),
            nn.Linear(hidden, 3),
        )
        self.confidence_head = nn.Sequential(
            nn.Linear(self.token_dim + 2, hidden),
            nn.GELU(),
            nn.Linear(hidden, 1),
        )

        nn.init.zeros_(self.residual_head[-1].weight)
        nn.init.zeros_(self.residual_head[-1].bias)

    def freeze_state_prior(self) -> None:
        """Freeze the explicit StatePrior teacher path."""

        for param in self.state_prior.parameters():
            param.requires_grad = False

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
            # Deterministic fallback for fully dropped rows: keep expert 0.
            keep[empty, 0] = True
        return keep.to(dtype).view(batch, self.n_experts, 1, 1)

    def forward(
        self,
        proposal_pointmaps: torch.Tensor,
        proposal_confidences: torch.Tensor,
        memory_context: Optional[torch.Tensor] = None,
        conflict_score: Optional[torch.Tensor] = None,
        proposal_dropout: float = 0.0,
    ) -> Dict[str, torch.Tensor]:
        if proposal_pointmaps.dim() != 5 or proposal_pointmaps.shape[-1] != 3:
            raise ValueError(
                "proposal_pointmaps must be [B,E,N,P,3], "
                f"got {tuple(proposal_pointmaps.shape)}"
            )
        b, e, n, p, _ = proposal_pointmaps.shape
        if e != self.n_experts:
            raise ValueError(f"expected E={self.n_experts} proposals, got {e}")
        if proposal_confidences.shape[:4] != proposal_pointmaps.shape[:4]:
            raise ValueError("proposal_confidences must align with proposal_pointmaps")

        device = proposal_pointmaps.device
        dtype = proposal_pointmaps.dtype

        z = proposal_pointmaps[..., 2]
        with torch.no_grad():
            med = z.abs().reshape(b, e, -1).median(dim=-1).values.clamp_min(1e-6)
        pm_norm = proposal_pointmaps / med.view(b, e, 1, 1, 1)
        conf = proposal_confidences.to(dtype)

        prior_out = self.state_prior(
            proposal_pointmaps,
            proposal_confidences,
            memory_context,
            conflict_score,
        )
        teacher = prior_out["final_pointmap"]
        prior_weights = prior_out["expert_weights"]

        keep = self._dropout_mask(b, proposal_dropout, device, dtype)
        kept_weights = prior_weights * keep
        kept_weights = kept_weights / kept_weights.sum(dim=1, keepdim=True).clamp_min(1e-8)
        dropout_teacher = (kept_weights.unsqueeze(-1) * pm_norm).sum(dim=1)

        if (memory_context is None) or (not self.use_state):
            state = torch.zeros(b, self.state_dim, device=device, dtype=dtype)
        else:
            state = self.context_proj(memory_context.to(dtype))
        if conflict_score is None:
            conflict = torch.zeros(b, 1, device=device, dtype=dtype)
        else:
            conflict = conflict_score if conflict_score.dim() == 2 else conflict_score.view(b, 1)
            conflict = torch.sigmoid(conflict.to(dtype))

        state_b = state.view(b, 1, 1, 1, self.state_dim).expand(
            b, e, n, p, self.state_dim
        )
        conflict_b = conflict.view(b, 1, 1, 1, 1).expand(b, e, n, p, 1)
        expert_b = self.expert_embed.to(dtype).view(1, e, 1, 1, self.id_dim).expand(
            b, e, n, p, self.id_dim
        )
        available = keep.view(b, e, 1, 1, 1).expand(b, e, n, p, 1)
        prior_w = prior_weights.unsqueeze(-1)
        residual = pm_norm - dropout_teacher.unsqueeze(1)
        residual_norm = residual.norm(dim=-1, keepdim=True)

        feat = torch.cat(
            [
                pm_norm * available,
                conf * available,
                residual * available,
                residual_norm * available,
                prior_w,
                available,
                state_b,
                conflict_b,
                expert_b,
            ],
            dim=-1,
        )
        tokens = self.input_proj(feat).permute(0, 2, 3, 1, 4).reshape(
            b * n * p, e, self.token_dim
        )
        mixed = self.mixer(tokens)
        pool_w = kept_weights.permute(0, 2, 3, 1).reshape(b * n * p, e, 1)
        pooled = (pool_w * mixed).sum(dim=1)

        disp = (kept_weights.unsqueeze(-1) * residual.pow(2)).sum(dim=1).sqrt()
        disp_scalar = disp.mean(dim=-1, keepdim=True)
        entropy = -(
            kept_weights.clamp_min(1e-8) * kept_weights.clamp_min(1e-8).log()
        ).sum(dim=1, keepdim=True)
        entropy = entropy.permute(0, 2, 3, 1)
        head_feat = torch.cat(
            [pooled, disp_scalar.reshape(b * n * p, 1), entropy.reshape(b * n * p, 1)],
            dim=-1,
        )
        delta = torch.tanh(self.residual_head(head_feat)).view(b, n, p, 3)
        delta = delta * disp_scalar * self.residual_scale
        final = dropout_teacher + delta
        confidence_delta = torch.sigmoid(self.confidence_head(head_feat)).view(b, n, p, 1)
        final_confidence = (
            kept_weights.unsqueeze(-1) * conf
        ).sum(dim=1) * confidence_delta

        return {
            "final_pointmap": final,
            "teacher_pointmap": teacher,
            "dropout_teacher_pointmap": dropout_teacher,
            "residual_delta": delta,
            "final_confidence": final_confidence,
            "prior_weights": prior_weights,
            "kept_prior_weights": kept_weights,
            "kept_mask": keep,
        }
