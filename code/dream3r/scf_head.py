"""Dream3R-v0.6 SCF -- multi-expert state-conditioned fusion head.

Generalises ``Stage6FusionHead`` from single-expert residual correction to a
bounded multi-expert soft fusion: a convex combination over E expert
proposals, conditioned on per-expert confidence, a learnable per-expert
prior, and persistent Memory/Critic state.

Why convex fusion instead of residual: the L1 real-backend rerun
(MIDTERM-20260530 §4.5) showed an unbounded residual head damages a real
expert (KITTI -47pp, ETH3D -92pp) because the current (untrained) state is
not depth-informative. A softmax-weighted convex combination of real
proposals stays inside their convex hull -- it cannot diverge below the
worst proposal and degrades gracefully toward a single expert -- so it is
the safe L2 architecture. Residual correction is available behind a flag
(default off) for the L4 retrained-state regime.

Each proposal is scale-normalised by its own median depth before fusion so
that proposals from experts with different absolute scales (fast3r / mast3r
/ spann3r) can be combined meaningfully; the downstream abs_rel metric uses
``align_scale=True`` so this normalisation does not bias the comparison.

Inputs:
    proposal_pointmaps    [B, E, N, P, 3]
    proposal_confidences  [B, E, N, P, 1]
    memory_context        [B, D_mem]   (optional; zeros if None / ablated)
    conflict_score        [B, 1]       (optional; zeros if None)

Outputs (dict):
    final_pointmap    [B, N, P, 3]   convex fusion (+ optional gated residual)
    final_confidence  [B, N, P, 1]
    expert_weights    [B, E, N, P]    softmax over experts
    correction_mask   [B, N, P, 1]    |residual| magnitude (0 if residual off)
"""

from __future__ import annotations

from typing import Dict, Optional

import torch
import torch.nn as nn


class SCFHead(nn.Module):
    """State-conditioned multi-expert fusion head.

    Args:
        n_experts:    number of expert proposals E.
        d_memory:     dimension of memory.fused_context.
        head_dim:     projection width for memory context.
        hidden:       hidden width of the weight / residual MLPs.
        id_dim:       width of the learnable per-expert embedding.
        use_state:    if False, memory context is ablated to zeros.
        use_residual: if True, add a gated residual correction on top of the
                      convex fusion (default False per the L1 verdict).
        conflict_dampening_strength:
                      if >0, high conflict shrinks expert logits toward 0
                      before softmax, making fusion weights more conservative.
    """

    def __init__(self, n_experts: int, d_memory: int, head_dim: int = 64,
                 hidden: int = 128, id_dim: int = 8,
                 use_state: bool = True, use_residual: bool = False,
                 conflict_dampening_strength: float = 0.0):
        super().__init__()
        self.n_experts = int(n_experts)
        self.d_memory = int(d_memory)
        self.head_dim = int(head_dim)
        self.id_dim = int(id_dim)
        self.use_state = bool(use_state)
        self.use_residual = bool(use_residual)
        self.conflict_dampening_strength = float(conflict_dampening_strength)
        if not 0.0 <= self.conflict_dampening_strength <= 1.0:
            raise ValueError("conflict_dampening_strength must be in [0, 1]")

        self.context_proj = nn.Linear(self.d_memory, self.head_dim)
        # Learnable per-expert prior so the head can express a global expert
        # preference (small random init keeps experts distinguishable while
        # the zero-init weight head below still starts uniform).
        self.expert_embed = nn.Parameter(torch.randn(self.n_experts, self.id_dim) * 0.02)

        # Per-(expert, patch) weight scorer:
        #   [confidence(1) + state(head_dim) + conflict(1) + expert_id(id_dim)] -> logit
        w_in = 1 + self.head_dim + 1 + self.id_dim
        self.weight_mlp = nn.Sequential(
            nn.Linear(w_in, hidden),
            nn.GELU(),
            nn.Linear(hidden, 1),
        )
        # Zero-init final layer -> uniform weights at init (fused = mean of
        # scale-normalised proposals); training learns to concentrate.
        nn.init.zeros_(self.weight_mlp[-1].weight)
        nn.init.zeros_(self.weight_mlp[-1].bias)

        if self.use_residual:
            r_in = 3 + 1 + self.head_dim + 1
            self.residual_mlp = nn.Sequential(
                nn.Linear(r_in, hidden),
                nn.GELU(),
                nn.Linear(hidden, hidden),
                nn.GELU(),
                nn.Linear(hidden, 3),
            )
            nn.init.zeros_(self.residual_mlp[-1].weight)
            nn.init.zeros_(self.residual_mlp[-1].bias)

    @staticmethod
    def _apply_conflict_dampening(
        logits: torch.Tensor,
        conflict_signal: torch.Tensor,
        strength: float,
    ) -> torch.Tensor:
        if strength <= 0.0:
            return logits
        scale = 1.0 - float(strength) * conflict_signal.clamp(0.0, 1.0)
        return logits * scale.view(logits.shape[0], 1, 1, 1)

    def forward(
        self,
        proposal_pointmaps: torch.Tensor,       # [B, E, N, P, 3]
        proposal_confidences: torch.Tensor,     # [B, E, N, P, 1]
        memory_context: Optional[torch.Tensor] = None,   # [B, D_mem]
        conflict_score: Optional[torch.Tensor] = None,   # [B, 1]
    ) -> Dict[str, torch.Tensor]:
        if proposal_pointmaps.dim() != 5 or proposal_pointmaps.shape[-1] != 3:
            raise ValueError(
                f"proposal_pointmaps must be [B,E,N,P,3], got {tuple(proposal_pointmaps.shape)}"
            )
        b, e, n, p, _ = proposal_pointmaps.shape
        if e != self.n_experts:
            raise ValueError(f"expected E={self.n_experts} proposals, got {e}")
        device, dtype = proposal_pointmaps.device, proposal_pointmaps.dtype

        # ---- 1) scale-normalise each proposal by its own median depth (detached)
        z = proposal_pointmaps[..., 2]                                   # [B,E,N,P]
        with torch.no_grad():
            med = z.abs().reshape(b, e, -1).median(dim=-1).values        # [B,E]
            med = med.clamp_min(1e-6)
        pm_norm = proposal_pointmaps / med.view(b, e, 1, 1, 1)

        # ---- 2) state context -> [B,E,N,P,head_dim]
        if (memory_context is None) or (not self.use_state):
            ctx = torch.zeros(b, self.head_dim, device=device, dtype=dtype)
        else:
            ctx = self.context_proj(memory_context.to(dtype))
        ctx_b = ctx.view(b, 1, 1, 1, self.head_dim).expand(b, e, n, p, self.head_dim)

        # ---- 3) conflict score -> sigmoid, broadcast
        if conflict_score is None:
            conf_sig = torch.zeros(b, 1, device=device, dtype=dtype)
        else:
            cs = conflict_score if conflict_score.dim() == 2 else conflict_score.view(b, 1)
            conf_sig = torch.sigmoid(cs.to(dtype))
        conflict_b = conf_sig.view(b, 1, 1, 1, 1).expand(b, e, n, p, 1)

        # ---- 4) per-expert id embedding, broadcast
        id_b = self.expert_embed.to(dtype).view(1, e, 1, 1, self.id_dim).expand(b, e, n, p, self.id_dim)

        # ---- 5) weight logits + softmax over experts
        conf = proposal_confidences.to(dtype)                            # [B,E,N,P,1]
        w_feat = torch.cat([conf, ctx_b, conflict_b, id_b], dim=-1)      # [B,E,N,P, w_in]
        logits = self.weight_mlp(w_feat).squeeze(-1)                     # [B,E,N,P]
        logits = self._apply_conflict_dampening(
            logits,
            conf_sig,
            self.conflict_dampening_strength,
        )
        weights = torch.softmax(logits, dim=1)                          # over experts

        # ---- 6) convex fusion
        fused = (weights.unsqueeze(-1) * pm_norm).sum(dim=1)             # [B,N,P,3]
        final_conf = (weights.unsqueeze(-1) * conf).sum(dim=1)          # [B,N,P,1]

        correction = torch.zeros(b, n, p, 1, device=device, dtype=dtype)
        final = fused
        if self.use_residual:
            ctx_np = ctx.view(b, 1, 1, self.head_dim).expand(b, n, p, self.head_dim)
            conflict_np = conf_sig.view(b, 1, 1, 1).expand(b, n, p, 1)
            r_feat = torch.cat([fused, final_conf, ctx_np, conflict_np], dim=-1)
            delta = self.residual_mlp(r_feat)                            # [B,N,P,3]
            gate = torch.tanh(conf_sig).view(b, 1, 1, 1)
            final = fused + gate * delta
            correction = (gate * delta).abs().mean(dim=-1, keepdim=True)

        return {
            "final_pointmap": final,
            "final_confidence": final_conf,
            "expert_weights": weights,
            "correction_mask": correction,
        }
