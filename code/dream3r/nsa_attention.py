"""
Native Sparse Attention (NSA) — 3-branch selective attention for Dream3R.

Three branches operate in parallel on the same query:
  1. Compressed: attends to n_compress latent state tokens (long-term context)
  2. Selected:   top-k lookup from an external bank (spatial recall)
  3. Sliding:    local window of recent tokens (short-term continuity)

Outputs are fused via a learned per-query gate that weights the three branches.

Reference: DeepSeek NSA (2025), adapted for 3D reconstruction streaming.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Optional, Tuple


class NSABranch(nn.Module):
    """Single multi-head attention branch used by all three NSA paths."""

    def __init__(self, d_model: int, n_heads: int, dropout: float = 0.0):
        super().__init__()
        assert d_model % n_heads == 0
        self.n_heads = n_heads
        self.d_head = d_model // n_heads
        self.scale = self.d_head ** -0.5

        self.q_proj = nn.Linear(d_model, d_model, bias=False)
        self.k_proj = nn.Linear(d_model, d_model, bias=False)
        self.v_proj = nn.Linear(d_model, d_model, bias=False)
        self.out_proj = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, query: torch.Tensor, key: torch.Tensor,
                value: torch.Tensor,
                mask: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Args:
            query: [B, Q, D]
            key:   [B, K, D]
            value: [B, K, D]
            mask:  [B, Q, K] or None — True = attend, False = mask out
        Returns:
            output: [B, Q, D]
        """
        B, Q, _ = query.shape
        K = key.shape[1]

        q = self.q_proj(query).view(B, Q, self.n_heads, self.d_head).transpose(1, 2)
        k = self.k_proj(key).view(B, K, self.n_heads, self.d_head).transpose(1, 2)
        v = self.v_proj(value).view(B, K, self.n_heads, self.d_head).transpose(1, 2)

        attn = (q @ k.transpose(-2, -1)) * self.scale
        if mask is not None:
            if mask.dim() == 3:
                mask = mask.unsqueeze(1)
            attn = attn.masked_fill(~mask, torch.finfo(attn.dtype).min)

        attn = self.dropout(F.softmax(attn, dim=-1))
        out = (attn @ v).transpose(1, 2).contiguous().view(B, Q, -1)
        return self.out_proj(out)


class CompressedBranch(nn.Module):
    """Branch 1: attends to a fixed set of compressed latent tokens."""

    def __init__(self, d_model: int, n_compress: int, n_heads: int,
                 dropout: float = 0.0):
        super().__init__()
        self.n_compress = n_compress
        self.compress_proj = nn.Linear(d_model, d_model)
        self.attn = NSABranch(d_model, n_heads, dropout)

    def forward(self, query: torch.Tensor,
                compressed_ctx: torch.Tensor) -> torch.Tensor:
        """
        Args:
            query:          [B, Q, D]
            compressed_ctx: [B, C, D] where C = n_compress
        Returns:
            output: [B, Q, D]
        """
        ctx = self.compress_proj(compressed_ctx)
        return self.attn(query, ctx, ctx)


class SelectedBranch(nn.Module):
    """Branch 2: top-k selection from an external key/value bank."""

    def __init__(self, d_model: int, n_select_k: int, n_heads: int,
                 dropout: float = 0.0):
        super().__init__()
        self.n_select_k = n_select_k
        self.score_proj = nn.Linear(d_model, d_model, bias=False)
        self.attn = NSABranch(d_model, n_heads, dropout)

    def forward(self, query: torch.Tensor,
                bank_keys: torch.Tensor,
                bank_values: torch.Tensor,
                bank_mask: Optional[torch.Tensor] = None,
                score_bias: Optional[torch.Tensor] = None,
                ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Args:
            query:       [B, Q, D]
            bank_keys:   [B, M, D] — full bank keys
            bank_values: [B, M, D] — full bank values
            bank_mask:   [B, M] — True = valid entry, False = empty/quarantined
            score_bias:  [B, Q, M], [B, M], or [B, 1] additive bank score bias
        Returns:
            output:        [B, Q, D]
            indices:       [B, Q, K] — selected bank indices per query
            scores_before: [B, Q, K] — selected raw similarity scores
            scores_after:  [B, Q, K] — selected scores after CR-3 bias
        """
        B, Q, D = query.shape
        M = bank_keys.shape[1]
        K = min(self.n_select_k, M)

        score_q = self.score_proj(query)
        scores_before_bias = torch.bmm(score_q, bank_keys.transpose(1, 2)) * (D ** -0.5)
        scores = scores_before_bias

        if score_bias is not None:
            if score_bias.dim() == 3 and score_bias.shape[-1] == 1:
                score_bias = score_bias.squeeze(-1)
            if score_bias.dim() == 2:
                if score_bias.shape[-1] == 1:
                    score_bias = score_bias.expand(-1, M)
                score_bias = score_bias.unsqueeze(1)
            scores = scores + score_bias.to(dtype=scores.dtype, device=scores.device)

        if bank_mask is not None:
            mask_expanded = bank_mask.unsqueeze(1).expand(B, Q, M)
            scores = scores.masked_fill(~mask_expanded, torch.finfo(scores.dtype).min)
            scores_before_bias = scores_before_bias.masked_fill(
                ~mask_expanded, torch.finfo(scores_before_bias.dtype).min
            )

        topk_scores, topk_idx = scores.topk(K, dim=-1)
        topk_scores_before = scores_before_bias.gather(-1, topk_idx)

        flat_idx = topk_idx.reshape(B, -1)
        sel_k = bank_keys.gather(1, flat_idx.unsqueeze(-1).expand(-1, -1, D)).view(B, Q, K, D)
        sel_v = bank_values.gather(1, flat_idx.unsqueeze(-1).expand(-1, -1, D)).view(B, Q, K, D)

        sel_k = sel_k.reshape(B * Q, K, D)
        sel_v = sel_v.reshape(B * Q, K, D)
        q_flat = query.reshape(B * Q, 1, D)

        out = self.attn(q_flat, sel_k, sel_v)
        out = out.view(B, Q, D)

        return out, topk_idx, topk_scores_before, topk_scores


class SlidingBranch(nn.Module):
    """Branch 3: local sliding window attention over recent tokens."""

    def __init__(self, d_model: int, n_heads: int, dropout: float = 0.0):
        super().__init__()
        self.attn = NSABranch(d_model, n_heads, dropout)

    def forward(self, query: torch.Tensor,
                sliding_buffer: torch.Tensor) -> torch.Tensor:
        """
        Args:
            query:          [B, Q, D]
            sliding_buffer: [B, W, D] — last W*P tokens concatenated
        Returns:
            output: [B, Q, D]
        """
        return self.attn(query, sliding_buffer, sliding_buffer)


class NSAAttention(nn.Module):
    """
    3-branch Native Sparse Attention.

    Fuses compressed (long-term), selected (spatial recall), and sliding
    (short-term) branches via a learned per-query gate.

    Args:
        d_model:        token dimension
        n_compress:     number of compressed latent tokens
        n_select_k:     top-k entries to select from bank per query
        n_heads:        attention heads per branch
        dropout:        attention dropout
    """

    def __init__(self, d_model: int = 128, n_compress: int = 32,
                 n_select_k: int = 8, n_heads: int = 4,
                 dropout: float = 0.0,
                 confidence_bias_strength: float = 2.0,
                 geometry_bias_strength: float = 1.0,
                 top_k_branches: int = 2):
        super().__init__()
        self.d_model = d_model
        self.n_compress = n_compress
        self.n_select_k = n_select_k
        self.confidence_bias_strength = nn.Parameter(
            torch.tensor(float(confidence_bias_strength))
        )
        self.geometry_bias_strength = nn.Parameter(
            torch.tensor(float(geometry_bias_strength))
        )
        self.top_k_branches = top_k_branches

        self.compressed = CompressedBranch(d_model, n_compress, n_heads, dropout)
        self.selected = SelectedBranch(d_model, n_select_k, n_heads, dropout)
        self.sliding = SlidingBranch(d_model, n_heads, dropout)

        self.gate = nn.Sequential(
            nn.Linear(d_model, d_model // 2),
            nn.GELU(),
            nn.Linear(d_model // 2, 3),
        )
        self.norm = nn.LayerNorm(d_model)

    def forward(self, query: torch.Tensor,
                compressed_ctx: torch.Tensor,
                bank_keys: torch.Tensor,
                bank_values: torch.Tensor,
                sliding_buffer: torch.Tensor,
                bank_mask: Optional[torch.Tensor] = None,
                critic_confidence: Optional[torch.Tensor] = None,
                permanence_bias: Optional[torch.Tensor] = None,
                query_points3d: Optional[torch.Tensor] = None,
                bank_points3d: Optional[torch.Tensor] = None,
                dynamic_top_k: Optional[int] = None,
                ) -> Dict[str, torch.Tensor]:
        """
        Args:
            query:              [B, Q, D]
            compressed_ctx:     [B, C, D]
            bank_keys:          [B, M, D]
            bank_values:        [B, M, D]
            sliding_buffer:     [B, W, D]
            bank_mask:          [B, M] — True = valid
            critic_confidence:  [B, 1] — CR-3: high values bias toward high-confidence entries
            permanence_bias:    [B, 1] — CR-3: high values prefer stable/permanent entries
            query_points3d:     [B, Q, 3] current query geometry
            bank_points3d:      [B, M, 3] stored anchor geometry
            dynamic_top_k:      int — CR-3: adjusted retrieval depth based on Critic confidence
        Returns:
            output:               [B, Q, D]
            branch_weights:       [B, Q, 3]
            selected_indices:     [B, Q, K]
        """
        out_c = self.compressed(query, compressed_ctx)

        effective_k = dynamic_top_k if dynamic_top_k is not None else self.n_select_k
        if effective_k != self.n_select_k:
            saved_k = self.selected.n_select_k
            self.selected.n_select_k = effective_k

        selected_score_bias = None
        permanence_bias_applied = torch.zeros((), device=query.device, dtype=query.dtype)
        if permanence_bias is not None:
            selected_score_bias = permanence_bias
            permanence_bias_applied = permanence_bias.to(
                device=query.device, dtype=query.dtype
            ).abs().mean()

        geometry_bias_applied = torch.zeros((), device=query.device, dtype=query.dtype)
        geometry_distances = None
        if query_points3d is not None and bank_points3d is not None:
            geometry_distances = torch.cdist(
                query_points3d.float(), bank_points3d.float()
            ).to(device=query.device, dtype=query.dtype)
            denom = geometry_distances.detach().mean().clamp_min(1e-6)
            geometry_bias = -F.softplus(self.geometry_bias_strength) * (geometry_distances / denom)
            selected_score_bias = (
                geometry_bias if selected_score_bias is None
                else selected_score_bias.unsqueeze(1) + geometry_bias
            )
            geometry_bias_applied = geometry_bias.abs().mean().detach()

        out_s, sel_idx, scores_before, scores_after = self.selected(
            query, bank_keys, bank_values, bank_mask, score_bias=selected_score_bias
        )
        selected_geometry_distances = None
        if geometry_distances is not None:
            selected_geometry_distances = geometry_distances.gather(-1, sel_idx).detach()

        if effective_k != self.n_select_k and dynamic_top_k is not None:
            self.selected.n_select_k = saved_k

        out_w = self.sliding(query, sliding_buffer)

        gate_logits = self.gate(query)

        if critic_confidence is not None:
            conf = critic_confidence.unsqueeze(1).expand(-1, query.shape[1], -1)
            gate_logits = gate_logits.clone()
            confidence_bias = (1.0 - conf.squeeze(-1)) * self.confidence_bias_strength
            gate_logits[:, :, 1] = gate_logits[:, :, 1] + confidence_bias
            confidence_bias_applied = confidence_bias.detach().mean()
        else:
            confidence_bias_applied = torch.zeros((), device=query.device, dtype=query.dtype)

        if self.top_k_branches < gate_logits.shape[-1]:
            top_values, top_indices = gate_logits.topk(self.top_k_branches, dim=-1)
            sparse_logits = torch.full_like(gate_logits, torch.finfo(gate_logits.dtype).min)
            sparse_logits.scatter_(-1, top_indices, top_values)
            branch_active_mask = torch.zeros_like(gate_logits, dtype=torch.bool)
            branch_active_mask.scatter_(-1, top_indices, True)
            gate_logits = sparse_logits
        else:
            branch_active_mask = torch.ones_like(gate_logits, dtype=torch.bool)

        gate_weights = F.softmax(gate_logits, dim=-1)

        branches = torch.stack([out_c, out_s, out_w], dim=-2)
        fused = (gate_weights.unsqueeze(-1) * branches).sum(dim=-2)
        output = self.norm(fused + query)

        return {
            "output": output,
            "branch_weights": gate_weights,
            "selected_indices": sel_idx,
            "retrieval_log": {
                "effective_top_k": effective_k,
                "confidence_bias_applied": confidence_bias_applied,
                "permanence_bias_applied": permanence_bias_applied,
                "geometry_bias_applied": geometry_bias_applied,
                "selected_3d_distances": selected_geometry_distances,
                "branch_active_mask": branch_active_mask.detach(),
                "selected_scores_before_bias": scores_before.detach(),
                "selected_scores_after_bias": scores_after.detach(),
            },
        }
