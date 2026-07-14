"""State-only expert prior head.

This diagnostic head excludes proposal geometry and confidence from the
weighting network, isolating the contribution of Dream state.

The output remains a convex fusion of cached real expert proposals, so it is
bounded and comparable to SCF / ProposalSetDecoder while isolating the state
signal.
"""

from __future__ import annotations

from typing import Dict, Optional

import torch
import torch.nn as nn


class StatePriorHead(nn.Module):
    """Window-level expert prior from Dream state only."""

    def __init__(
        self,
        n_experts: int,
        d_memory: int,
        state_dim: int = 64,
        hidden: int = 128,
        use_state: bool = True,
    ):
        super().__init__()
        self.n_experts = int(n_experts)
        self.d_memory = int(d_memory)
        self.state_dim = int(state_dim)
        self.use_state = bool(use_state)

        self.context_proj = nn.Linear(self.d_memory, self.state_dim)
        self.prior_mlp = nn.Sequential(
            nn.Linear(self.state_dim + 1, hidden),
            nn.GELU(),
            nn.Linear(hidden, self.n_experts),
        )

        nn.init.zeros_(self.prior_mlp[-1].weight)
        nn.init.zeros_(self.prior_mlp[-1].bias)

    def forward(
        self,
        proposal_pointmaps: torch.Tensor,
        proposal_confidences: torch.Tensor,
        memory_context: Optional[torch.Tensor] = None,
        conflict_score: Optional[torch.Tensor] = None,
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

        if (memory_context is None) or (not self.use_state):
            state = torch.zeros(b, self.state_dim, device=device, dtype=dtype)
        else:
            state = self.context_proj(memory_context.to(dtype))

        if conflict_score is None:
            conflict = torch.zeros(b, 1, device=device, dtype=dtype)
        else:
            conflict = conflict_score if conflict_score.dim() == 2 else conflict_score.view(b, 1)
            conflict = torch.sigmoid(conflict.to(dtype))

        logits = self.prior_mlp(torch.cat([state, conflict], dim=-1))
        weights = torch.softmax(logits, dim=1).view(b, e, 1, 1)
        weights_full = weights.expand(b, e, n, p)
        conf = proposal_confidences.to(dtype)

        final = (weights_full.unsqueeze(-1) * pm_norm).sum(dim=1)
        final_conf = (weights_full.unsqueeze(-1) * conf).sum(dim=1)

        return {
            "final_pointmap": final,
            "final_confidence": final_conf,
            "expert_weights": weights_full,
        }
