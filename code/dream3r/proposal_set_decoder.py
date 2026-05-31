"""Dream3R-PD non-core proposal-set reconstruction decoder.

This is the first implementation of the selected final-path decoder in
DEC-20260530-015 / SPEC-20260530-005. It consumes cached proposal pointmaps
from multiple real 3R teachers plus Dream state features and predicts a
bounded final pointmap. It intentionally lives outside the frozen core path.

Compared with SCFHead, this decoder adds per-patch proposal-set mixing: each
patch gets an E-token mini-transformer over expert proposals, conditioned on
Dream state and conflict metadata. The output remains a convex combination of
scale-normalized proposal pointmaps, so the first version is inspectable and
bounded while being more expressive than a per-expert MLP scorer.
"""

from __future__ import annotations

from typing import Dict, Optional

import torch
import torch.nn as nn


class ProposalSetDecoder(nn.Module):
    """State-conditioned decoder over an expert proposal set.

    Args:
        n_experts: number of proposal teachers.
        d_memory: dimension of ``memory.fused_context``.
        token_dim: hidden width for proposal tokens.
        state_dim: projected Dream-state width.
        hidden: transformer feed-forward width.
        num_layers: number of per-patch proposal mixer layers.
        num_heads: attention heads inside the proposal mixer.
        id_dim: learnable expert-identity embedding width.
        use_state: ablation flag; False zeroes the Dream state input.
        use_state_prior: whether to add an explicit StatePrior-style MLP
            branch into expert logits.
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
        use_state_prior: bool = True,
        prior_hidden: int = 128,
        prior_logit_scale: float = 1.0,
    ):
        super().__init__()
        self.n_experts = int(n_experts)
        self.d_memory = int(d_memory)
        self.token_dim = int(token_dim)
        self.state_dim = int(state_dim)
        self.id_dim = int(id_dim)
        self.use_state = bool(use_state)
        self.use_state_prior = bool(use_state_prior)
        self.prior_logit_scale = float(prior_logit_scale)

        self.context_proj = nn.Linear(self.d_memory, self.state_dim)
        self.expert_embed = nn.Parameter(torch.randn(self.n_experts, self.id_dim) * 0.02)

        # proposal xyz + confidence + residual-to-set-mean xyz + residual norm
        # + state + conflict + expert id
        in_dim = 3 + 1 + 3 + 1 + self.state_dim + 1 + self.id_dim
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
        self.weight_head = nn.Linear(self.token_dim, 1)
        self.uncertainty_head = nn.Sequential(
            nn.Linear(self.token_dim + 2, hidden),
            nn.GELU(),
            nn.Linear(hidden, 1),
        )

        # Direct state-to-expert prior. The first sweep showed that simply
        # concatenating the same state vector to every expert token can be
        # too easy for the mixer to ignore, so this gives state a dedicated
        # route into relative expert logits.
        self.state_bias_head = nn.Linear(self.state_dim + 1, self.n_experts)
        self.state_prior_mlp = nn.Sequential(
            nn.Linear(self.state_dim + 1, prior_hidden),
            nn.GELU(),
            nn.Linear(prior_hidden, self.n_experts),
        )

        # Uniform expert weighting at initialization.
        nn.init.zeros_(self.weight_head.weight)
        nn.init.zeros_(self.weight_head.bias)
        nn.init.zeros_(self.state_bias_head.weight)
        nn.init.zeros_(self.state_bias_head.bias)
        nn.init.zeros_(self.state_prior_mlp[-1].weight)
        nn.init.zeros_(self.state_prior_mlp[-1].bias)

    def forward(
        self,
        proposal_pointmaps: torch.Tensor,
        proposal_confidences: torch.Tensor,
        memory_context: Optional[torch.Tensor] = None,
        conflict_score: Optional[torch.Tensor] = None,
    ) -> Dict[str, torch.Tensor]:
        """Decode a bounded pointmap from cached proposal tensors.

        Args:
            proposal_pointmaps: ``[B, E, N, P, 3]`` tensor.
            proposal_confidences: ``[B, E, N, P, 1]`` tensor.
            memory_context: optional ``[B, D_mem]`` state tensor.
            conflict_score: optional ``[B, 1]`` critic conflict scalar.
        """

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

        # Scale-normalize each proposal by its own median depth.
        z = proposal_pointmaps[..., 2]
        with torch.no_grad():
            med = z.abs().reshape(b, e, -1).median(dim=-1).values.clamp_min(1e-6)
        pm_norm = proposal_pointmaps / med.view(b, e, 1, 1, 1)

        set_mean = pm_norm.mean(dim=1, keepdim=True)
        residual = pm_norm - set_mean
        residual_norm = residual.norm(dim=-1, keepdim=True)

        if (memory_context is None) or (not self.use_state):
            state = torch.zeros(b, self.state_dim, device=device, dtype=dtype)
        else:
            state = self.context_proj(memory_context.to(dtype))
        state_b = state.view(b, 1, 1, 1, self.state_dim).expand(
            b, e, n, p, self.state_dim
        )

        if conflict_score is None:
            conflict = torch.zeros(b, 1, device=device, dtype=dtype)
        else:
            conflict = conflict_score if conflict_score.dim() == 2 else conflict_score.view(b, 1)
            conflict = torch.sigmoid(conflict.to(dtype))
        conflict_b = conflict.view(b, 1, 1, 1, 1).expand(b, e, n, p, 1)

        expert_b = self.expert_embed.to(dtype).view(1, e, 1, 1, self.id_dim).expand(
            b, e, n, p, self.id_dim
        )
        conf = proposal_confidences.to(dtype)

        feat = torch.cat(
            [pm_norm, conf, residual, residual_norm, state_b, conflict_b, expert_b],
            dim=-1,
        )
        tokens = self.input_proj(feat).permute(0, 2, 3, 1, 4).reshape(b * n * p, e, self.token_dim)
        mixed = self.mixer(tokens)
        logits = self.weight_head(mixed).view(b, n, p, e).permute(0, 3, 1, 2)
        state_input = torch.cat([state, conflict], dim=-1)
        state_bias = self.state_bias_head(state_input)
        if self.use_state_prior:
            state_prior_logits = self.state_prior_mlp(state_input)
        else:
            state_prior_logits = torch.zeros_like(state_bias)
        logits = logits + state_bias.view(b, e, 1, 1)
        logits = logits + self.prior_logit_scale * state_prior_logits.view(b, e, 1, 1)
        weights = torch.softmax(logits, dim=1)

        final = (weights.unsqueeze(-1) * pm_norm).sum(dim=1)
        final_conf = (weights.unsqueeze(-1) * conf).sum(dim=1)

        mixed_weighted = (
            weights.permute(0, 2, 3, 1).reshape(b * n * p, e, 1) * mixed
        ).sum(dim=1)
        entropy = -(weights.clamp_min(1e-8) * weights.clamp_min(1e-8).log()).sum(dim=1, keepdim=True)
        entropy = entropy.permute(0, 2, 3, 1).reshape(b * n * p, 1)
        set_disp = residual_norm.mean(dim=1).reshape(b * n * p, 1)
        uncertainty = torch.sigmoid(
            self.uncertainty_head(torch.cat([mixed_weighted, entropy, set_disp], dim=-1))
        ).view(b, n, p, 1)

        return {
            "final_pointmap": final,
            "final_confidence": final_conf,
            "expert_weights": weights,
            "state_prior_weights": torch.softmax(state_prior_logits, dim=1),
            "uncertainty": uncertainty,
        }
