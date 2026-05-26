"""Stage 6 post-dispatch fusion head.

Connects `memory.fused_context` and `critic.conflict_score` to the final
pointmap output without modifying v0.3/v0.5 core. The head ingests the
selected expert's standalone pointmap together with anchor/memory state
and produces a refined pointmap.

Architecture (see MIDTERM-20260530.md §4.1):

    inputs:
        expert_pointmap    [B, N, P, 3]
        expert_confidence  [B, N, P, 1]
        memory_context     [B, D_mem]
        conflict_score     [B, 1]

    forward:
        ctx = Linear(D_mem -> head_dim)(memory_context)        [B, head_dim]
        ctx_bcast = ctx.unsqueeze(1).unsqueeze(2)              [B, 1, 1, head_dim]
        ctx_bcast = ctx_bcast.expand(B, N, P, head_dim)
        x = concat([expert_pointmap, expert_confidence,
                    ctx_bcast, sigmoid(conflict_score).expand(...)])
        delta = MLP(x)                                          [B, N, P, 3]
        gate = tanh(conflict_score).view(B, 1, 1, 1)            [B, 1, 1, 1]
        refined = expert_pointmap + gate * delta

The gate term ensures identity behaviour when the critic is confident
(conflict_score near 0 -> gate near 0 -> refined ~ expert_pointmap).
Refinement only kicks in when the critic flags conflict.
"""

from __future__ import annotations

from typing import Optional

import torch
import torch.nn as nn


class Stage6FusionHead(nn.Module):
    """Post-dispatch refinement head for Dream3R V04Pipeline.

    Args:
        d_memory:  dimension of memory.fused_context tensor (i.e. last dim).
        head_dim:  dimension memory context is projected to before concat.
        hidden:    hidden width for the 3-layer refinement MLP.
    """

    def __init__(self, d_memory: int, head_dim: int = 64, hidden: int = 128):
        super().__init__()
        self.d_memory = int(d_memory)
        self.head_dim = int(head_dim)
        self.hidden = int(hidden)

        self.context_proj = nn.Linear(self.d_memory, self.head_dim)

        # Per-patch input width: 3 (pointmap) + 1 (confidence) + head_dim + 1 (conflict)
        in_dim = 3 + 1 + self.head_dim + 1
        self.refine = nn.Sequential(
            nn.Linear(in_dim, self.hidden),
            nn.GELU(),
            nn.Linear(self.hidden, self.hidden),
            nn.GELU(),
            nn.Linear(self.hidden, 3),
        )

        # Initialise the final layer to near-zero so the head starts close
        # to identity (refined ~= expert_pointmap at init). Critical for
        # training stability: a randomly-initialised head would degrade
        # the strong expert baseline before any gradient signal lands.
        nn.init.zeros_(self.refine[-1].weight)
        nn.init.zeros_(self.refine[-1].bias)

    def forward(
        self,
        expert_pointmap: torch.Tensor,        # [B, N, P, 3]
        expert_confidence: torch.Tensor,      # [B, N, P, 1]
        memory_context: Optional[torch.Tensor],  # [B, D_mem] or None
        conflict_score: Optional[torch.Tensor],  # [B, 1] or None
    ) -> torch.Tensor:
        """Returns refined pointmap of shape `[B, N, P, 3]`."""
        if expert_pointmap.dim() != 4 or expert_pointmap.shape[-1] != 3:
            raise ValueError(
                f"expert_pointmap must be [B,N,P,3], got {tuple(expert_pointmap.shape)}"
            )
        b, n, p, _ = expert_pointmap.shape
        device = expert_pointmap.device
        dtype = expert_pointmap.dtype

        # ---- 1) Memory context: project + broadcast to per-patch
        if memory_context is None:
            ctx_b = torch.zeros(b, self.head_dim, device=device, dtype=dtype)
        else:
            if memory_context.dim() != 2 or memory_context.shape[1] != self.d_memory:
                raise ValueError(
                    f"memory_context must be [B,{self.d_memory}], "
                    f"got {tuple(memory_context.shape)}"
                )
            ctx_b = self.context_proj(memory_context.to(dtype))
        ctx_patch = ctx_b.unsqueeze(1).unsqueeze(2).expand(b, n, p, self.head_dim)

        # ---- 2) Conflict score: broadcast to per-patch (sigmoid for [0,1] scale)
        if conflict_score is None:
            conflict_b = torch.zeros(b, 1, device=device, dtype=dtype)
        else:
            if conflict_score.dim() == 1:
                conflict_b = conflict_score.unsqueeze(-1)
            else:
                conflict_b = conflict_score
            if conflict_b.shape[-1] != 1:
                raise ValueError(
                    f"conflict_score must end in dim 1, got {tuple(conflict_b.shape)}"
                )
        conflict_patch = (
            torch.sigmoid(conflict_b.to(dtype))
            .view(b, 1, 1, 1)
            .expand(b, n, p, 1)
        )

        # ---- 3) Concat per-patch inputs, apply refinement MLP
        x = torch.cat(
            [expert_pointmap, expert_confidence.to(dtype), ctx_patch, conflict_patch],
            dim=-1,
        )
        delta = self.refine(x)  # [B, N, P, 3]

        # ---- 4) Gate by conflict: identity when conflict ~ 0, refine when high
        gate = torch.tanh(conflict_b.to(dtype)).view(b, 1, 1, 1)
        refined = expert_pointmap + gate * delta
        return refined
