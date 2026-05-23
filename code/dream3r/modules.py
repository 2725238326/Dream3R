"""
Dream3R computational cores C1-C5.

v0.2 modules (MemorySSM_v01, Composer_v01) are preserved for ablation.
v0.3 modules (SpatialMemory, ComposerRouter) are the current defaults.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import time
from typing import Optional, Dict, List

from dream3r.nsa_attention import NSAAttention
from dream3r.anchor_bank import AnchorBank
from dream3r.composer_experts import ExpertRegistry
from dream3r.composer_experts.base_adapter import ExpertOutput


# ---------------------------------------------------------------------------
# C1: Perceiver
# ---------------------------------------------------------------------------

class Perceiver(nn.Module):
    """Per-frame backbone plus trainable geometry/evidence heads."""

    EVIDENCE_SIGNALS = [
        "pose_novelty", "view_overlap", "reprojection_residual",
        "pointmap_conflict", "confidence_drop", "latent_drift_proxy",
        "dynamic_ratio", "optical_flow_conflict", "object_track_stability",
        "loop_candidate_score", "anchor_importance", "cache_pressure",
        "external_memory_overlap", "prior_rgb_conflict",
        "blur_or_low_light_score", "uncertainty_area",
        "model_capability_match",
    ]

    DINO_HUB_NAMES = {
        "dinov2_vitb14": "dinov2_vitb14",
        "dinov2_vitl14": "dinov2_vitl14",
        "dinov3": "dinov2_vitb14",
    }

    def __init__(self, d_model: int = 768, n_evidence: int = 17,
                 d_evidence: int = 32, img_size: int = 224,
                 patch_size: int = 16, use_backbone: bool = True,
                 backbone_type: str = "none",
                 backbone_freeze: bool = True,
                 backbone_checkpoint_path: str = ""):
        super().__init__()
        self.d_model = d_model
        self.n_evidence = n_evidence
        self.d_evidence = d_evidence
        self.use_backbone = use_backbone
        self.backbone_type = backbone_type or "none"
        self.backbone_freeze = backbone_freeze
        self.backbone_checkpoint_path = backbone_checkpoint_path or ""
        self.backbone_load_error = None
        self.backbone = None
        self.backbone_dim = d_model
        self.backbone_proj = nn.Identity()

        if use_backbone and self.backbone_type not in {"none", "identity"}:
            self._try_load_backbone()
        elif use_backbone and self.backbone_type in {"none", "identity"}:
            self._try_load_timm_backbone(pretrained=False)

        self.pointmap_head = nn.Sequential(
            nn.Linear(d_model, d_model // 2), nn.GELU(),
            nn.Linear(d_model // 2, 3),
        )
        self.confidence_head = nn.Sequential(
            nn.Linear(d_model, d_model // 4), nn.GELU(),
            nn.Linear(d_model // 4, 1),
        )
        self.evidence_projectors = nn.ModuleDict({
            name: nn.Sequential(
                nn.Linear(d_model, d_model // 4), nn.GELU(),
                nn.Linear(d_model // 4, d_evidence),
            )
            for name in self.EVIDENCE_SIGNALS
        })

    def _finalize_backbone(self, backbone: nn.Module, backbone_dim: int):
        self.backbone = backbone
        self.backbone_dim = backbone_dim
        if self.backbone_freeze:
            self.backbone.requires_grad_(False)
            self.backbone.eval()
        self.backbone_proj = (
            nn.Linear(backbone_dim, self.d_model)
            if backbone_dim != self.d_model else nn.Identity()
        )
        self.backbone_load_error = None

    def _try_load_backbone(self):
        try:
            if self.backbone_type.startswith("dinov2") or self.backbone_type == "dinov3":
                self._load_dino_backbone()
            else:
                self._try_load_timm_backbone(pretrained=False)
        except Exception as exc:
            original_error = f"{self.backbone_type}: {exc}"
            self.backbone_load_error = original_error
            self._try_load_timm_backbone(pretrained=False, preserve_error=True)
            if self.backbone_load_error is None:
                self.backbone_load_error = original_error

    def _load_dino_backbone(self):
        hub_name = self.DINO_HUB_NAMES.get(self.backbone_type)
        if hub_name is None:
            raise ValueError(f"unsupported backbone_type: {self.backbone_type}")
        backbone = torch.hub.load("facebookresearch/dinov2", hub_name)
        if self.backbone_checkpoint_path:
            payload = torch.load(self.backbone_checkpoint_path, map_location="cpu")
            state_dict = payload.get("model", payload) if isinstance(payload, dict) else payload
            backbone.load_state_dict(state_dict, strict=False)
        backbone_dim = 1024 if "vitl14" in hub_name else 768
        self._finalize_backbone(backbone, backbone_dim)

    def _try_load_timm_backbone(self, pretrained: bool = False,
                                preserve_error: bool = False):
        previous_error = self.backbone_load_error
        try:
            import timm
            backbone = timm.create_model(
                "vit_base_patch16_224", pretrained=pretrained,
                num_classes=0, global_pool="",
            )
            self._finalize_backbone(backbone, 768)
            if preserve_error:
                self.backbone_load_error = previous_error
        except Exception as exc:
            self.backbone_load_error = previous_error or f"timm fallback failed: {exc}"
            self.backbone = None
            self.backbone_dim = self.d_model
            self.backbone_proj = nn.Identity()

    def train(self, mode: bool = True):
        super().train(mode)
        if self.backbone is not None and self.backbone_freeze:
            self.backbone.eval()
        return self

    def _extract_backbone_tokens(self, flat: torch.Tensor) -> torch.Tensor:
        if self.backbone is None:
            return flat

        def run_backbone():
            if (self.backbone_type.startswith("dinov2") or self.backbone_type == "dinov3")                     and hasattr(self.backbone, "forward_features"):
                return self.backbone.forward_features(flat)
            return self.backbone(flat)

        if self.backbone_freeze:
            with torch.no_grad():
                features = run_backbone()
        else:
            features = run_backbone()
        if isinstance(features, dict):
            features = features.get(
                "x_norm_patchtokens",
                features.get("tokens", features.get("last_hidden_state")),
            )
        if features.dim() == 2:
            features = features.unsqueeze(1)
        if features.shape[1] > 1 and self.backbone_type.startswith("dinov2"):
            return features
        if features.shape[1] > 1 and features.shape[1] != (flat.shape[-1] // 16) ** 2:
            return features[:, 1:]
        return features

    def encode_images(self, images: torch.Tensor) -> torch.Tensor:
        B, N = images.shape[:2]
        flat = images.reshape(B * N, *images.shape[2:])
        features = self._extract_backbone_tokens(flat)
        features = self.backbone_proj(features)
        return features.view(B, N, features.shape[1], features.shape[2])

    def forward(self, x: torch.Tensor) -> Dict[str, torch.Tensor]:
        """
        Args:
            x: [B, N, 3, H, W] raw images OR [B, N, P, D] pre-extracted
        Returns:
            t1, t2_pointmap, t2_confidence, t3_evidence, t3_named, perception_summary
        """
        if self.use_backbone and x.dim() == 5:
            t1 = self.encode_images(x)
        else:
            t1 = x

        t2_pointmap = self.pointmap_head(t1)
        t2_confidence = torch.sigmoid(self.confidence_head(t1))
        pooled = t1.mean(dim=2)

        t3_named = {}
        t3_list = []
        for name in self.EVIDENCE_SIGNALS:
            sig = self.evidence_projectors[name](pooled)
            t3_named[name] = sig
            t3_list.append(sig)

        t3 = torch.stack(t3_list, dim=2)
        perception_summary = t1.mean(dim=(1, 2))

        return {
            "t1": t1,
            "t2_pointmap": t2_pointmap,
            "t2_confidence": t2_confidence,
            "t3_evidence": t3,
            "t3_named": t3_named,
            "perception_summary": perception_summary,
            "backbone_type": self.backbone_type,
            "backbone_load_error": self.backbone_load_error,
        }


# ---------------------------------------------------------------------------
# C2: Executive Memory — A1 branching + bus-informed decisions
# ---------------------------------------------------------------------------

class MemorySSM_v01(nn.Module):
    """
    [v0.1 — preserved for ablation ABL-v02-1]
    Recurrent state controller with 5 distinct update modes.

    A1 update modes:
      0 = full_update:     standard GRU forward, full gain
      1 = pose_adaptive:   gain scaled by pose_novelty evidence
      2 = kalman:          residual-weighted update (new - old, scaled by confidence)
      3 = skip:            copy prev_state unchanged
      4 = reset:           zero state

    A2: write_decision conditioned on suppress_mask (CR-2).
    Bus reads: dynamic_ratio (Permanence), conflict_score (Critic t-1).
    """

    # Named indices for update_kind
    FULL, POSE_ADAPTIVE, KALMAN, SKIP, RESET = 0, 1, 2, 3, 4

    def __init__(self, d_percept: int = 768, d_evidence_flat: int = 544,
                 d_state: int = 256, n_layers: int = 6,
                 d_bus_context: int = 3):
        super().__init__()
        self.d_state = d_state
        # d_bus_context: dynamic_ratio(1) + conflict_score(1) + drift(1)
        d_input = d_percept + d_evidence_flat + d_bus_context
        self.input_proj = nn.Linear(d_input, d_state)
        self.layers = nn.ModuleList([
            nn.GRUCell(d_state, d_state) for _ in range(n_layers)
        ])
        self.norm = nn.LayerNorm(d_state)

        # A1 heads
        self.update_classifier = nn.Linear(d_state, 5)
        self.full_gate = nn.Linear(d_state, 1)
        self.pose_gate = nn.Linear(d_state, 1)
        self.kalman_gain = nn.Linear(d_state, d_state)

        # A2 write head
        self.write_head = nn.Linear(d_state, 4)
        # A3 anchor scorer
        self.anchor_scorer = nn.Linear(d_state, 1)
        # Drift proxy
        self.drift_proj = nn.Linear(d_state, 1)

    def init_state(self, B: int, device: torch.device) -> torch.Tensor:
        return torch.zeros(B, self.d_state, device=device)

    def forward(self, perception_summary: torch.Tensor,
                evidence_flat: torch.Tensor,
                prev_state: torch.Tensor,
                suppress_mask: Optional[torch.Tensor] = None,
                bus_dynamic_ratio: Optional[torch.Tensor] = None,
                bus_conflict_score: Optional[torch.Tensor] = None,
                ) -> Dict[str, torch.Tensor]:
        """
        Args:
            perception_summary: [B, d_percept]
            evidence_flat:      [B, d_evidence_flat]
            prev_state:         [B, d_state]
            suppress_mask:      [B] CR-2 from Permanence
            bus_dynamic_ratio:  [B, 1] from bus (Permanence)
            bus_conflict_score: [B, 1] from bus (Critic t-1)
        """
        B = perception_summary.shape[0]
        device = perception_summary.device

        # Pack bus context (null protocol: zeros if not available)
        dyn = bus_dynamic_ratio if bus_dynamic_ratio is not None else torch.zeros(B, 1, device=device)
        conf = bus_conflict_score if bus_conflict_score is not None else torch.zeros(B, 1, device=device)
        prev_drift = self.drift_proj(prev_state).detach()  # [B, 1] don't backprop through prev drift read
        bus_ctx = torch.cat([dyn, conf, prev_drift], dim=-1)  # [B, 3]

        x = self.input_proj(torch.cat([perception_summary, evidence_flat, bus_ctx], dim=-1))

        # GRU stack → candidate new state
        h = prev_state
        for gru in self.layers:
            h = gru(x, h)
        h = self.norm(h)

        # --- A1: classify then branch ---
        update_logits = self.update_classifier(h)  # [B, 5]
        update_probs = F.softmax(update_logits, dim=-1)  # [B, 5]

        # Compute each update mode's output
        g_full = torch.sigmoid(self.full_gate(h))           # [B, 1]
        g_pose = torch.sigmoid(self.pose_gate(h))           # [B, 1]
        k_gain = torch.sigmoid(self.kalman_gain(h))         # [B, d_state]
        residual = h - prev_state                           # [B, d_state]

        s_full = prev_state + g_full * residual
        s_pose = prev_state + (g_full * g_pose) * residual
        s_kalman = prev_state + k_gain * residual
        s_skip = prev_state
        s_reset = torch.zeros_like(prev_state)

        # Soft mixture (differentiable; hard argmax at inference)
        modes = torch.stack([s_full, s_pose, s_kalman, s_skip, s_reset], dim=1)  # [B, 5, d]
        new_state = (update_probs.unsqueeze(-1) * modes).sum(dim=1)  # [B, d]

        # --- A2: write decision (CR-2 gated) ---
        write_logits = self.write_head(new_state)  # [B, 4]
        if suppress_mask is not None:
            write_logits = write_logits.clone()
            write_logits[:, 0] = write_logits[:, 0] - 1e9 * suppress_mask

        # --- A3: anchor scoring ---
        anchor_scores = self.anchor_scorer(new_state)  # [B, 1]

        # Drift proxy for bus
        drift = self.drift_proj(new_state)  # [B, 1]

        return {
            "latent_state": new_state,
            "update_kind": update_logits,
            "update_probs": update_probs,
            "write_decision": write_logits,
            "anchor_scores": anchor_scores,
            "latent_drift_proxy": drift,
        }


# ---------------------------------------------------------------------------
# C3: Permanence — Slot Attention + bus-informed mint control
# ---------------------------------------------------------------------------

class Permanence(nn.Module):
    """
    Object identity tracking via Slot Attention.
    A6: region_decision (suppress/admit/defer), dynamic_ratio, suppress handoff.
    Bus reads: conflict_score → modulates object mint conservatism.
    """

    def __init__(self, d_input: int = 768, d_slot: int = 128,
                 n_slots: int = 16, n_iters: int = 3,
                 isa_pose_match_weight: float = 1.0):
        super().__init__()
        self.d_slot = d_slot
        self.n_slots = n_slots
        self.n_iters = n_iters
        self.isa_pose_match_weight = isa_pose_match_weight

        self.slot_mu = nn.Parameter(torch.randn(1, 1, d_slot) * (d_slot ** -0.5))
        self.slot_log_sigma = nn.Parameter(torch.zeros(1, 1, d_slot))

        self.input_norm = nn.LayerNorm(d_input)
        self.input_proj = nn.Linear(d_input, d_slot)
        self.position_proj = nn.Linear(3, d_slot)
        self.isa_pose_bias_strength = nn.Parameter(torch.tensor(1.0))

        self.slot_norm = nn.LayerNorm(d_slot)
        self.k_proj = nn.Linear(d_slot, d_slot, bias=False)
        self.q_proj = nn.Linear(d_slot, d_slot, bias=False)
        self.v_proj = nn.Linear(d_slot, d_slot, bias=False)

        self.gru = nn.GRUCell(d_slot, d_slot)
        self.mlp = nn.Sequential(
            nn.LayerNorm(d_slot),
            nn.Linear(d_slot, d_slot * 2),
            nn.ReLU(),
            nn.Linear(d_slot * 2, d_slot),
        )

        # A6 heads
        self.region_head = nn.Linear(d_slot, 3)
        self.dynamic_head = nn.Linear(d_slot, 1)
        # Conflict-aware mint gate: when conflict is high, be more conservative
        self.mint_gate = nn.Linear(d_slot + 1, 1)  # slot feature + conflict_score

    def _init_slots(self, B: int, device: torch.device) -> torch.Tensor:
        mu = self.slot_mu.expand(B, self.n_slots, -1)
        sigma = self.slot_log_sigma.exp().expand(B, self.n_slots, -1)
        return mu + sigma * torch.randn_like(mu)

    @staticmethod
    def match_slots(current_slots: torch.Tensor,
                    prev_slots: torch.Tensor,
                    current_slot_poses: Optional[torch.Tensor] = None,
                    prev_slot_poses: Optional[torch.Tensor] = None,
                    pose_weight: float = 1.0) -> tuple[torch.Tensor, torch.Tensor]:
        current_norm = F.normalize(current_slots, dim=-1)
        prev_norm = F.normalize(prev_slots, dim=-1)
        sim = torch.bmm(current_norm, prev_norm.transpose(1, 2))
        if current_slot_poses is not None and prev_slot_poses is not None:
            pose_dist = torch.cdist(current_slot_poses[..., :3].float(), prev_slot_poses[..., :3].float())
            denom = pose_dist.detach().mean(dim=(1, 2), keepdim=True).clamp_min(1e-6)
            sim = sim - pose_weight * (pose_dist.to(sim.dtype) / denom.to(sim.dtype))
        B, S, _ = sim.shape
        device = sim.device
        all_indices = torch.zeros(B, S, dtype=torch.long, device=device)
        all_scores = torch.zeros(B, S, dtype=sim.dtype, device=device)

        for b in range(B):
            sim_cpu = sim[b].detach().cpu()
            dp = {0: 0.0}
            parents = []
            for row in range(S):
                next_dp = {}
                parent = {}
                for mask, score in dp.items():
                    for col in range(S):
                        bit = 1 << col
                        if mask & bit:
                            continue
                        next_mask = mask | bit
                        value = score + float(sim_cpu[row, col])
                        if value > next_dp.get(next_mask, -float("inf")):
                            next_dp[next_mask] = value
                            parent[next_mask] = (mask, col)
                dp = next_dp
                parents.append(parent)

            mask = (1 << S) - 1
            assignment = [0] * S
            for row in range(S - 1, -1, -1):
                prev_mask, col = parents[row][mask]
                assignment[row] = col
                mask = prev_mask

            idx = torch.tensor(assignment, dtype=torch.long, device=device)
            all_indices[b] = idx
            all_scores[b] = sim[b, torch.arange(S, device=device), idx]
        return all_indices, all_scores

    def forward(self, features: torch.Tensor,
                prev_slots: Optional[torch.Tensor] = None,
                bus_conflict_score: Optional[torch.Tensor] = None,
                input_positions: Optional[torch.Tensor] = None,
                prev_slot_poses: Optional[torch.Tensor] = None,
                ) -> Dict[str, torch.Tensor]:
        """
        Args:
            features:           [B, N, d_input]
            prev_slots:         [B, n_slots, d_slot] or None
            bus_conflict_score: [B, 1] from bus (Critic t-1)
            input_positions:    [B, N, 3] pointmap-derived token positions
            prev_slot_poses:    [B, n_slots, 7] previous slot reference frames
        """
        B, N, _ = features.shape
        device = features.device
        if input_positions is None:
            input_positions = torch.zeros(B, N, 3, device=device, dtype=features.dtype)
        inputs = self.input_proj(self.input_norm(features)) + self.position_proj(input_positions)
        k = self.k_proj(inputs)
        v = self.v_proj(inputs)

        slots = prev_slots if prev_slots is not None else self._init_slots(B, device)
        pose_attention_bias = None
        if prev_slot_poses is not None:
            pose_dist = torch.cdist(prev_slot_poses[..., :3].float(), input_positions.float())
            denom = pose_dist.detach().mean(dim=(1, 2), keepdim=True).clamp_min(1e-6)
            pose_attention_bias = -F.softplus(self.isa_pose_bias_strength) * (pose_dist / denom).to(features.dtype)

        attn = None
        for _ in range(self.n_iters):
            slots_prev = slots
            q = self.q_proj(self.slot_norm(slots))
            attn_logits = torch.einsum("bsd,bnd->bsn", q, k) * (self.d_slot ** -0.5)
            if pose_attention_bias is not None:
                attn_logits = attn_logits + pose_attention_bias
            attn = F.softmax(attn_logits, dim=1)
            attn = attn / (attn.sum(dim=-1, keepdim=True) + 1e-8)
            updates = torch.einsum("bsn,bnd->bsd", attn, v)
            slots = self.gru(
                updates.reshape(B * self.n_slots, self.d_slot),
                slots_prev.reshape(B * self.n_slots, self.d_slot),
            ).view(B, self.n_slots, self.d_slot)
            slots = slots + self.mlp(slots)

        region_logits = self.region_head(slots)  # [B, S, 3]
        dynamic_ratio = torch.sigmoid(self.dynamic_head(slots))  # [B, S, 1]

        # Mint gate: modulated by conflict_score from bus
        conflict = bus_conflict_score if bus_conflict_score is not None else torch.zeros(B, 1, device=device)
        conflict_expanded = conflict.unsqueeze(1).expand(B, self.n_slots, 1)
        mint_input = torch.cat([slots, conflict_expanded], dim=-1)  # [B, S, d_slot+1]
        mint_confidence = torch.sigmoid(self.mint_gate(mint_input)).squeeze(-1)  # [B, S]

        suppress = (region_logits.argmax(dim=-1) == 0).float()
        slot_translation = torch.einsum("bsn,bnd->bsd", attn, input_positions)
        identity_quat = input_positions.new_zeros(B, self.n_slots, 4)
        identity_quat[..., 0] = 1.0
        slot_poses = torch.cat([slot_translation, identity_quat], dim=-1)

        if prev_slots is None:
            slot_match_indices = torch.arange(self.n_slots, device=device).unsqueeze(0).expand(B, -1)
            slot_match_scores = torch.zeros(B, self.n_slots, device=device)
        else:
            slot_match_indices, slot_match_scores = self.match_slots(
                slots, prev_slots, slot_poses, prev_slot_poses,
                pose_weight=self.isa_pose_match_weight,
            )

        return {
            "object_track_set": slots,
            "object_slot_poses": slot_poses,
            "region_logits": region_logits,
            "dynamic_ratio": dynamic_ratio,
            "suppress_static_write": suppress,
            "mint_confidence": mint_confidence,
            "slot_match_indices": slot_match_indices,
            "slot_match_scores": slot_match_scores,
        }


# ---------------------------------------------------------------------------
# C4: Critic — transformer over evidence sequence
# ---------------------------------------------------------------------------

class Critic(nn.Module):
    """
    Small transformer reading the 17 evidence tokens.
    A4: conflict_score (scalar).
    A5: repair_action (6-way, CR-1 gated on reroute).
    """
    REROUTE_IDX = 2

    def __init__(self, n_evidence: int = 17, d_evidence: int = 32,
                 d_critic: int = 256, n_heads: int = 4, n_layers: int = 2,
                 geometric_conflict_scale: float = 8.0,
                 geometric_clean_bias: float = -2.0):
        super().__init__()
        self.token_proj = nn.Linear(d_evidence, d_critic)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_critic, nhead=n_heads, dim_feedforward=d_critic * 2,
            activation="gelu", batch_first=True, norm_first=True,
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        self.geom_proj = nn.Linear(4, d_critic)
        self.conflict_head = nn.Linear(d_critic, 1)
        self.repair_head = nn.Linear(d_critic, 6)
        self.geometric_conflict_scale = geometric_conflict_scale
        self.geometric_clean_bias = geometric_clean_bias

    @staticmethod
    def compute_geometric_consistency(pointmap_pair: torch.Tensor,
                                      confidence_pair: Optional[torch.Tensor] = None
                                      ) -> Dict[str, torch.Tensor]:
        p0, p1 = pointmap_pair[:, 0], pointmap_pair[:, 1]
        if confidence_pair is None:
            covisible = torch.ones_like(p0[..., 0])
            confidence_disagreement = torch.zeros_like(covisible)
        else:
            c0 = confidence_pair[:, 0].squeeze(-1).clamp(0, 1)
            c1 = confidence_pair[:, 1].squeeze(-1).clamp(0, 1)
            covisible = torch.sqrt((c0 * c1).clamp_min(0.0))
            confidence_disagreement = (c0 - c1).abs()

        residual = p0 - p1
        depth_scale = (p0[..., 2].abs() + p1[..., 2].abs()).clamp_min(1e-3)
        sampson = residual[..., :2].pow(2).sum(dim=-1) / depth_scale.pow(2)
        depth_inconsistency = (p0[..., 2] - p1[..., 2]).abs() / depth_scale

        weight = covisible / covisible.sum(dim=-1, keepdim=True).clamp_min(1e-6)
        sampson_mean = (sampson * weight).sum(dim=-1)
        depth_mean = (depth_inconsistency * weight).sum(dim=-1)
        covisible_inconsistency = 1.0 - covisible.mean(dim=-1)
        conf_disagreement_mean = (confidence_disagreement * weight).sum(dim=-1)
        features = torch.stack(
            [sampson_mean, covisible_inconsistency, conf_disagreement_mean, depth_mean],
            dim=-1,
        )
        return {
            "features": features,
            "sampson_distance": sampson_mean,
            "covisible_inconsistency": covisible_inconsistency,
            "confidence_disagreement": conf_disagreement_mean,
            "depth_inconsistency": depth_mean,
        }

    def forward(self, evidence: torch.Tensor,
                cr1_mask: Optional[torch.Tensor] = None,
                pointmap_pair: Optional[torch.Tensor] = None,
                confidence_pair: Optional[torch.Tensor] = None,
                ) -> Dict[str, torch.Tensor]:
        """
        Args:
            evidence: [B, n_evidence, d_evidence]
            cr1_mask: scalar or [B], 1=allow reroute, 0=block
            pointmap_pair: [B, 2, P, 3] overlapping pointmaps for geometric verification
            confidence_pair: [B, 2, P, 1] point confidence for the pair
        """
        x = self.token_proj(evidence)
        geometric_log = None
        geometry_adjustment = None
        if pointmap_pair is not None and pointmap_pair.shape[1] >= 2:
            geometric_log = self.compute_geometric_consistency(
                pointmap_pair[:, :2],
                confidence_pair[:, :2] if confidence_pair is not None else None,
            )
            x = torch.cat([x, self.geom_proj(geometric_log["features"]).unsqueeze(1)], dim=1)
            geometry_adjustment = self.geometric_clean_bias + self.geometric_conflict_scale * (
                geometric_log["sampson_distance"]
                + 0.5 * geometric_log["depth_inconsistency"]
                + 0.25 * geometric_log["confidence_disagreement"]
                + 0.25 * geometric_log["covisible_inconsistency"]
            )

        x = self.encoder(x)
        pooled = x.mean(dim=1)

        conflict = self.conflict_head(pooled)
        if geometry_adjustment is not None:
            conflict = conflict + geometry_adjustment.unsqueeze(-1).to(conflict.dtype)
        repair = self.repair_head(pooled)
        repair = repair.clone()
        conflict_pressure = (torch.sigmoid(conflict).squeeze(-1) - 0.5).clamp_min(0.0) * 2.0
        repair[:, 1] = repair[:, 1] + conflict_pressure

        if cr1_mask is not None:
            cr1 = cr1_mask.float()
            if cr1.dim() == 0:
                cr1 = cr1.unsqueeze(0)
            cr1 = cr1.expand(repair.shape[0])
            repair = repair.clone()
            repair[:, self.REROUTE_IDX] = torch.where(
                cr1 > 0.5, repair[:, self.REROUTE_IDX],
                torch.full_like(repair[:, self.REROUTE_IDX], -65000),
            )

        out = {
            "conflict_score": conflict,
            "repair_logits": repair,
            "recommended_action": repair.argmax(dim=-1),
        }
        if geometric_log is not None:
            out["geometric_consistency_log"] = {
                k: v for k, v in geometric_log.items() if k != "features"
            }
        return out


# ---------------------------------------------------------------------------
# C5: Composer — parameter-free table join
# ---------------------------------------------------------------------------

class Composer_v01(nn.Module):
    """[v0.1 — preserved for ablation] Zero parameters. regime @ capability_cards.T -> match -> rank."""

    def __init__(self, n_regimes: int = 5, n_models: int = 8):
        super().__init__()
        self.n_regimes = n_regimes
        self.n_models = n_models
        self.register_buffer("capability_cards",
                             torch.ones(n_models, n_regimes) / n_regimes)

    def set_capability_cards(self, cards: torch.Tensor):
        self.capability_cards.copy_(cards)

    def forward(self, regime_probs: torch.Tensor) -> Dict[str, torch.Tensor]:
        match = regime_probs @ self.capability_cards.t()
        scores, indices = match.sort(dim=-1, descending=True)
        regret = scores[:, 0] - scores[:, 1] if self.n_models > 1 else match.new_zeros(match.shape[0])
        return {
            "capability_match": match,
            "route_recommendation": indices,
            "route_regret": regret,
        }


# Aliases for backward compatibility
MemorySSM = MemorySSM_v01
Composer = Composer_v01


# ---------------------------------------------------------------------------
# C2 v0.3: Spatial Memory — NSA + AnchorBank + latent state recurrence
# ---------------------------------------------------------------------------

class StateTokenRecurrence(nn.Module):
    """CUT3R-style latent state token update via cross-attention with frame tokens."""

    def __init__(self, d_model: int, n_state_tokens: int, n_heads: int = 4,
                 grassmannian_strength: float = 0.1):
        super().__init__()
        self.n_state_tokens = n_state_tokens
        self.grassmannian_strength = grassmannian_strength
        self.init_tokens = nn.Parameter(
            torch.randn(1, n_state_tokens, d_model) * (d_model ** -0.5)
        )
        self.cross_attn = nn.MultiheadAttention(
            d_model, n_heads, batch_first=True,
        )
        self.self_attn = nn.MultiheadAttention(
            d_model, n_heads, batch_first=True,
        )
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_model * 2),
            nn.GELU(),
            nn.Linear(d_model * 2, d_model),
        )
        self.norm3 = nn.LayerNorm(d_model)

    def init_state(self, batch_size: int, device: torch.device) -> torch.Tensor:
        return self.init_tokens.expand(batch_size, -1, -1).clone()

    @staticmethod
    def grassmannian_regularize(prev_state: torch.Tensor,
                                new_state: torch.Tensor,
                                strength: float = 0.1) -> torch.Tensor:
        if strength <= 0:
            return new_state
        delta = new_state - prev_state
        denom = prev_state.pow(2).sum(dim=-1, keepdim=True).clamp_min(1e-8)
        parallel = prev_state * (delta * prev_state).sum(dim=-1, keepdim=True) / denom
        return new_state - strength * parallel

    def forward(self, prev_state: torch.Tensor,
                frame_tokens: torch.Tensor) -> torch.Tensor:
        """
        Args:
            prev_state:   [B, S, D] — previous latent state tokens
            frame_tokens: [B, P, D] — current frame tokens
        Returns:
            new_state: [B, S, D]
        """
        h = self.norm1(prev_state)
        h = prev_state + self.cross_attn(h, frame_tokens, frame_tokens)[0]

        h2 = self.norm2(h)
        h = h + self.self_attn(h2, h2, h2)[0]

        h = self.grassmannian_regularize(
            prev_state, h, strength=self.grassmannian_strength
        )
        h = h + self.ffn(self.norm3(h))
        return h


class MambaHybridRecurrence(nn.Module):
    """Mamba-inspired selective-scan state update plus frame cross-attention."""

    def __init__(self, d_model: int, n_state_tokens: int, n_heads: int = 4,
                 grassmannian_strength: float = 0.1):
        super().__init__()
        self.n_state_tokens = n_state_tokens
        self.grassmannian_strength = grassmannian_strength
        self.backend = "pytorch_selective_scan"
        self.init_tokens = nn.Parameter(
            torch.randn(1, n_state_tokens, d_model) * (d_model ** -0.5)
        )
        self.mamba = None
        self.backend_error = ""
        try:
            from mamba_ssm import Mamba
            self.mamba = Mamba(d_model=d_model, use_fast_path=False)
            self.backend = "mamba_ssm"
        except Exception as exc:
            self.mamba = None
            self.backend_error = f"{type(exc).__name__}: {exc}"

        self.state_norm = nn.LayerNorm(d_model)
        self.frame_context = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(d_model, d_model),
            nn.SiLU(),
        )
        self.scan_proj = nn.Linear(d_model, d_model * 3)
        self.scan_out = nn.Linear(d_model, d_model)

        self.cross_norm = nn.LayerNorm(d_model)
        self.frame_norm = nn.LayerNorm(d_model)
        self.cross_attn = nn.MultiheadAttention(
            d_model, n_heads, batch_first=True,
        )
        self.ffn = nn.Sequential(
            nn.LayerNorm(d_model),
            nn.Linear(d_model, d_model * 2),
            nn.GELU(),
            nn.Linear(d_model * 2, d_model),
        )

    def init_state(self, batch_size: int, device: torch.device) -> torch.Tensor:
        return self.init_tokens.expand(batch_size, -1, -1).clone()

    def _selective_scan(self, x: torch.Tensor) -> torch.Tensor:
        candidate, gate, decay = self.scan_proj(x).chunk(3, dim=-1)
        candidate = torch.tanh(candidate)
        gate = torch.sigmoid(gate)
        decay = torch.sigmoid(decay)

        hidden = torch.zeros_like(candidate[:, 0])
        outputs = []
        for idx in range(candidate.shape[1]):
            hidden = decay[:, idx] * hidden + (1.0 - decay[:, idx]) * candidate[:, idx]
            outputs.append(gate[:, idx] * hidden)
        return self.scan_out(torch.stack(outputs, dim=1))

    def forward(self, prev_state: torch.Tensor,
                frame_tokens: torch.Tensor) -> torch.Tensor:
        frame_summary = frame_tokens.mean(dim=1)
        context = self.frame_context(frame_summary).unsqueeze(1)
        scan_input = self.state_norm(prev_state + context)
        if self.mamba is not None:
            try:
                scan_update = self.mamba(scan_input)
            except Exception as exc:
                self.mamba = None
                self.backend = "pytorch_selective_scan"
                self.backend_error = f"{type(exc).__name__}: {exc}"
                scan_update = self._selective_scan(scan_input)
        else:
            scan_update = self._selective_scan(scan_input)
        h = prev_state + scan_update

        frame_ctx = self.frame_norm(frame_tokens)
        h = h + self.cross_attn(self.cross_norm(h), frame_ctx, frame_ctx)[0]
        h = StateTokenRecurrence.grassmannian_regularize(
            prev_state, h, strength=self.grassmannian_strength
        )
        return h + self.ffn(h)


def build_state_recurrence(recurrence_type: str,
                           d_model: int,
                           n_state_tokens: int,
                           n_heads: int = 4,
                           grassmannian_strength: float = 0.1) -> nn.Module:
    recurrence_type = (recurrence_type or "cross_attention").lower()
    if recurrence_type == "cross_attention":
        return StateTokenRecurrence(
            d_model, n_state_tokens, n_heads=n_heads,
            grassmannian_strength=grassmannian_strength,
        )
    if recurrence_type == "mamba_hybrid":
        return MambaHybridRecurrence(
            d_model, n_state_tokens, n_heads=n_heads,
            grassmannian_strength=grassmannian_strength,
        )
    raise ValueError(
        f"Unsupported state_recurrence_type={recurrence_type!r}. "
        "Expected 'cross_attention' or 'mamba_hybrid'."
    )


class SpatialMemory(nn.Module):
    """
    C2 v0.3: NSA-backed spatial memory with AnchorBank and latent recurrence.

    Architecture:
      1. Latent state tokens recur via cross-attention with frame tokens (compressed branch source)
      2. AnchorBank stores/retrieves spatial K/V anchors (selected branch source)
      3. Sliding window buffer holds recent frames (sliding branch source)
      4. NSA fuses all three branches
      5. Bus-gated writes to AnchorBank

    Args:
        d_model:          token dimension for all internal representations
        n_state_tokens:   number of latent state tokens (CUT3R-style)
        bank_capacity:    max AnchorBank entries
        nsa_n_select_k:   top-k for NSA selected branch
        nsa_n_heads:      attention heads in NSA
        sliding_window:   number of recent windows to keep in sliding buffer
        n_evidence:       number of evidence signals (for write decision)
        d_evidence:       evidence signal dimension
    """

    def __init__(self, d_model: int = 128, n_state_tokens: int = 32,
                 bank_capacity: int = 256, nsa_n_select_k: int = 8,
                 nsa_n_heads: int = 4, sliding_window: int = 4,
                 n_evidence: int = 17, d_evidence: int = 32,
                 nsa_confidence_bias_strength: float = 2.0,
                 nsa_geometry_bias_strength: float = 1.0,
                 nsa_top_k_branches: int = 2,
                 grassmannian_strength: float = 0.1,
                 anchor_spatial_bias_alpha: float = 1.0,
                 anchor_spatial_retrieval_mode: str = "latent_plus_3d",
                 active_to_stable_threshold: float = 0.6,
                 stable_recall_threshold: float = -1.0,
                 stable_recall_strength: float = 0.25,
                 stability_prune_bonus: float = 1.0,
                 state_recurrence_type: str = "cross_attention",
                 memory_use_nsa: bool = True,
                 enable_stable_memory: bool = True):
        super().__init__()
        self.d_model = d_model
        self.n_state_tokens = n_state_tokens
        self.sliding_window = sliding_window
        self.memory_use_nsa = memory_use_nsa
        self.enable_stable_memory = enable_stable_memory

        self.state_recurrence_type = state_recurrence_type
        self.state_recurrence = build_state_recurrence(
            state_recurrence_type,
            d_model, n_state_tokens, n_heads=nsa_n_heads,
            grassmannian_strength=grassmannian_strength,
        )

        self.anchor_bank = AnchorBank(
            capacity=bank_capacity, d_key=d_model, d_value=d_model,
            spatial_bias_alpha=anchor_spatial_bias_alpha,
            spatial_retrieval_mode=anchor_spatial_retrieval_mode,
            stability_prune_bonus=stability_prune_bonus,
        )
        self.active_to_stable_threshold = active_to_stable_threshold
        self.stable_recall_threshold = stable_recall_threshold
        self.stable_recall_strength = stable_recall_strength

        self.nsa = NSAAttention(
            d_model=d_model, n_compress=n_state_tokens,
            n_select_k=nsa_n_select_k, n_heads=nsa_n_heads,
            confidence_bias_strength=nsa_confidence_bias_strength,
            geometry_bias_strength=nsa_geometry_bias_strength,
            top_k_branches=nsa_top_k_branches,
        )

        self.frame_proj = nn.Linear(768, d_model)
        self.evidence_proj = nn.Linear(n_evidence * d_evidence, d_model)

        self.write_gate = nn.Sequential(
            nn.Linear(d_model * 2, d_model),
            nn.GELU(),
            nn.Linear(d_model, 1),
        )

        self.key_gen = nn.Linear(d_model, d_model)
        self.value_gen = nn.Linear(d_model, d_model)

        self.drift_proj = nn.Linear(d_model, 1)

        self.update_classifier = nn.Linear(d_model, 5)
        self.write_head = nn.Linear(d_model, 4)
        self.anchor_scorer = nn.Linear(d_model, 1)

        self._sliding_buffer: List[torch.Tensor] = []

    def init_state(self, batch_size: int,
                   device: torch.device) -> torch.Tensor:
        self.anchor_bank.reset(batch_size, device)
        self._sliding_buffer = []
        return self.state_recurrence.init_state(batch_size, device)

    def promote_to_stable(self, state_tokens: torch.Tensor,
                          confidence: torch.Tensor,
                          points3d_mean: Optional[torch.Tensor] = None):
        promote_confidence = torch.where(
            confidence >= self.active_to_stable_threshold,
            confidence,
            torch.zeros_like(confidence),
        )
        return self.anchor_bank.promote(
            state_tokens.detach(),
            confidence=promote_confidence.detach(),
            points3d_mean=points3d_mean.detach() if points3d_mean is not None else None,
        )

    def recall_from_stable(self, memory_output: torch.Tensor,
                           selected_indices: torch.Tensor,
                           selected_scores: torch.Tensor):
        B, Q, K = selected_indices.shape
        D = memory_output.shape[-1]
        flat_idx = selected_indices.reshape(B, -1)
        stable_values = self.anchor_bank.values[:B].detach().gather(
            1, flat_idx.unsqueeze(-1).expand(-1, -1, D)
        ).view(B, Q, K, D)
        finite_scores = torch.isfinite(selected_scores)
        safe_scores = torch.where(finite_scores, selected_scores, torch.zeros_like(selected_scores))
        weights = torch.softmax(safe_scores, dim=-1) * finite_scores.float()
        weights = weights / weights.sum(dim=-1, keepdim=True).clamp_min(1e-6)
        recalled = (weights.unsqueeze(-1) * stable_values).sum(dim=2)
        activated = finite_scores.any(dim=-1) & (selected_scores.max(dim=-1).values > self.stable_recall_threshold)
        mixed = memory_output + self.stable_recall_strength * recalled * activated.unsqueeze(-1).float()
        return mixed, {
            "stable_recall_activated": activated.detach(),
            "stable_recall_strength": torch.tensor(
                self.stable_recall_strength, device=memory_output.device, dtype=memory_output.dtype
            ),
            "stable_recall_weight_mean": weights.detach().mean(),
        }

    def forward(self, frame_tokens: torch.Tensor,
                evidence_flat: torch.Tensor,
                prev_state_tokens: torch.Tensor,
                t2_pointmap: Optional[torch.Tensor] = None,
                bus_dynamic_ratio: Optional[torch.Tensor] = None,
                bus_conflict_score: Optional[torch.Tensor] = None,
                suppress_mask: Optional[torch.Tensor] = None,
                cr3_critic_confidence: Optional[torch.Tensor] = None,
                cr3_permanence_bias: Optional[torch.Tensor] = None,
                cr3_dynamic_k: Optional[int] = None,
                ) -> Dict[str, torch.Tensor]:
        """
        Args:
            frame_tokens:      [B, P, D_frame] (D_frame=768)
            evidence_flat:     [B, n_ev * d_ev]
            prev_state_tokens: [B, S, D] latent state from previous window
            t2_pointmap:       [B, P, 3] or None
            bus_dynamic_ratio: [B, 1] from Permanence
            bus_conflict_score:[B, 1] from Critic t-1
            suppress_mask:     [B] CR-2 from Permanence
        Returns:
            latent_state_tokens, update_kind, write_decision, retrieval_log, etc.
        """
        B = frame_tokens.shape[0]
        device = frame_tokens.device

        frame_proj = self.frame_proj(frame_tokens)
        evidence_proj = self.evidence_proj(evidence_flat).unsqueeze(1)

        new_state = self.state_recurrence(prev_state_tokens, frame_proj)

        self._sliding_buffer.append(frame_proj.detach())
        if len(self._sliding_buffer) > self.sliding_window:
            self._sliding_buffer = self._sliding_buffer[-self.sliding_window:]
        sliding = torch.cat(self._sliding_buffer, dim=1)

        bank_keys = self.anchor_bank.keys[:B].detach().clone()
        bank_values = self.anchor_bank.values[:B].detach().clone()
        bank_mask = self.anchor_bank.readable_mask[:B].detach().clone()
        if not self.enable_stable_memory:
            bank_mask = torch.zeros_like(bank_mask)
        bank_points3d = self.anchor_bank.points3d_mean[:B].detach().clone()

        if self.memory_use_nsa:
            nsa_out = self.nsa(
                query=frame_proj,
                compressed_ctx=new_state,
                bank_keys=bank_keys,
                bank_values=bank_values,
                sliding_buffer=sliding,
                bank_mask=bank_mask,
                critic_confidence=cr3_critic_confidence,
                permanence_bias=cr3_permanence_bias,
                query_points3d=t2_pointmap,
                bank_points3d=bank_points3d,
                dynamic_top_k=cr3_dynamic_k,
            )
        else:
            K = min(self.nsa.selected.n_select_k, bank_keys.shape[1])
            memory_output = self.nsa.norm(frame_proj + new_state.mean(dim=1, keepdim=True))
            branch_weights = torch.zeros(B, frame_proj.shape[1], 3, device=device, dtype=frame_proj.dtype)
            branch_weights[..., 0] = 1.0
            selected_indices = torch.zeros(B, frame_proj.shape[1], K, device=device, dtype=torch.long)
            selected_scores = torch.zeros(B, frame_proj.shape[1], K, device=device, dtype=frame_proj.dtype)
            nsa_out = {
                "output": memory_output,
                "branch_weights": branch_weights,
                "selected_indices": selected_indices,
                "retrieval_log": {
                    "effective_top_k": 0,
                    "confidence_bias_applied": torch.zeros((), device=device, dtype=frame_proj.dtype),
                    "permanence_bias_applied": torch.zeros((), device=device, dtype=frame_proj.dtype),
                    "geometry_bias_applied": torch.zeros((), device=device, dtype=frame_proj.dtype),
                    "selected_3d_distances": None,
                    "branch_active_mask": branch_weights.bool().detach(),
                    "selected_scores_before_bias": selected_scores.detach(),
                    "selected_scores_after_bias": selected_scores.detach(),
                },
            }

        retrieval_log = dict(nsa_out["retrieval_log"])
        retrieval_log["state_recurrence_type"] = self.state_recurrence_type
        retrieval_log["memory_use_nsa"] = self.memory_use_nsa
        retrieval_log["enable_stable_memory"] = self.enable_stable_memory
        selected_indices = nsa_out["selected_indices"]
        if self.enable_stable_memory:
            memory_output, stable_recall_log = self.recall_from_stable(
                nsa_out["output"], selected_indices, retrieval_log["selected_scores_after_bias"]
            )
        else:
            memory_output = nsa_out["output"]
            stable_recall_log = {
                "stable_recall_activated": torch.zeros(
                    B, memory_output.shape[1], device=device, dtype=torch.bool
                ),
                "stable_recall_strength": torch.zeros((), device=device, dtype=memory_output.dtype),
                "stable_recall_weight_mean": torch.zeros((), device=device, dtype=memory_output.dtype),
            }
        retrieval_log.update(stable_recall_log)
        pooled = memory_output.mean(dim=1)

        flat_selected = selected_indices.reshape(B, -1)
        source_frame_pose = self.anchor_bank.source_frame_pose[:B].detach().clone()
        source_patch_ids = self.anchor_bank.source_patch_ids[:B].detach().clone()
        points3d_mean = self.anchor_bank.points3d_mean[:B].detach().clone()
        retrieval_log["retrieved_source_frame_pose"] = source_frame_pose.gather(
            1, flat_selected.unsqueeze(-1).unsqueeze(-1).expand(-1, -1, 4, 4)
        ).view(B, selected_indices.shape[1], selected_indices.shape[2], 4, 4).detach()
        retrieval_log["retrieved_source_patch_ids"] = source_patch_ids.gather(
            1, flat_selected
        ).view(B, selected_indices.shape[1], selected_indices.shape[2]).detach()
        retrieval_log["retrieved_points3d_mean"] = points3d_mean.gather(
            1, flat_selected.unsqueeze(-1).expand(-1, -1, 3)
        ).view(B, selected_indices.shape[1], selected_indices.shape[2], 3).detach()

        update_logits = self.update_classifier(pooled)
        update_probs = F.softmax(update_logits, dim=-1)

        write_logits = self.write_head(pooled)
        if suppress_mask is not None:
            write_logits = write_logits.clone()
            write_logits[:, 0] = write_logits[:, 0] - 1e9 * suppress_mask

        write_conf = torch.sigmoid(self.write_gate(
            torch.cat([pooled, evidence_proj.squeeze(1)], dim=-1)
        ))

        n_write_candidates = min(8, frame_proj.shape[1])
        anchor_scores_per_token = torch.bmm(
            self.key_gen(frame_proj),
            pooled.unsqueeze(-1)
        ).squeeze(-1)
        _, top_indices = anchor_scores_per_token.topk(n_write_candidates, dim=1)
        write_keys = self.key_gen(frame_proj).gather(
            1, top_indices.unsqueeze(-1).expand(-1, -1, self.d_model)
        )
        write_values = self.value_gen(memory_output).gather(
            1, top_indices.unsqueeze(-1).expand(-1, -1, self.d_model)
        )

        if t2_pointmap is None:
            points3d_mean = torch.zeros(B, n_write_candidates, 3, device=device)
        else:
            points3d_mean = t2_pointmap.gather(
                1, top_indices.unsqueeze(-1).expand(-1, -1, 3)
            )
        source_patch_ids = top_indices.long()
        source_frame_pose = torch.eye(4, device=device).view(1, 1, 4, 4).expand(
            B, n_write_candidates, 4, 4
        )
        retrieval_log["written_source_patch_ids"] = source_patch_ids.detach()
        retrieval_log["written_points3d_mean"] = points3d_mean.detach()

        if self.enable_stable_memory:
            write_result = self.anchor_bank.write(
                keys=write_keys,
                values=write_values,
                confidence=write_conf.expand(B, n_write_candidates),
                bus_dynamic_ratio=bus_dynamic_ratio,
                bus_conflict_score=bus_conflict_score,
                source_frame_pose=source_frame_pose,
                source_patch_ids=source_patch_ids,
                points3d_mean=points3d_mean,
            )
        else:
            write_result = type("WriteResultStub", (), {
                "n_written": 0,
                "n_suppressed": n_write_candidates * B,
                "n_quarantined": 0,
            })()

        active_state_confidence = torch.sigmoid((new_state * pooled.unsqueeze(1)).mean(dim=-1))
        if t2_pointmap is None:
            stable_points = torch.zeros(B, self.n_state_tokens, 3, device=device)
        else:
            stable_points = t2_pointmap.mean(dim=1, keepdim=True).expand(B, self.n_state_tokens, 3)
        if self.enable_stable_memory:
            promote_result = self.promote_to_stable(
                new_state, active_state_confidence, points3d_mean=stable_points
            )
            promoted_to_stable = promote_result.written_mask.detach()
        else:
            promoted_to_stable = torch.zeros(
                B, self.n_state_tokens, device=device, dtype=torch.bool
            )
        retrieval_log["active_state_confidence"] = active_state_confidence.detach()
        retrieval_log["promoted_to_stable"] = promoted_to_stable
        retrieval_log["stable_state_score"] = self.anchor_bank.stability_score[:B].detach().clone()
        self.anchor_bank.tick()

        anchor_scores = self.anchor_scorer(pooled)
        drift = self.drift_proj(pooled)

        return {
            "latent_state_tokens": new_state,
            "latent_state": pooled,
            "update_kind": update_logits,
            "update_probs": update_probs,
            "write_decision": write_logits,
            "anchor_scores": anchor_scores,
            "latent_drift_proxy": drift,
            "nsa_branch_weights": nsa_out["branch_weights"],
            "nsa_selected_indices": selected_indices,
            "memory_retrieval_log": retrieval_log,
            "bank_occupancy": self.anchor_bank.occupancy,
            "write_result": {
                "n_written": write_result.n_written,
                "n_suppressed": write_result.n_suppressed,
                "n_quarantined": write_result.n_quarantined,
            },
        }


# ---------------------------------------------------------------------------
# C5 v0.3: Composer Router — expert dispatch with cost-normalized matching
# ---------------------------------------------------------------------------

class ComposerRouter(nn.Module):
    """
    C5 v0.3: Expert routing with cost-normalized capability matching.

    Replaces the zero-param table join with learned routing that accounts
    for latency cost and Critic confidence feedback.

    Args:
        n_regimes:       number of reconstruction regimes
        d_routing:       routing embedding dimension
        cost_alpha:      latency cost weight (0 = ignore latency, 1 = latency-only)
        expert_registry: ExpertRegistry instance (optional, for dispatch)
    """

    def __init__(self, n_regimes: int = 5, d_routing: int = 64,
                 cost_alpha: float = 0.5,
                 expert_registry: Optional[ExpertRegistry] = None):
        super().__init__()
        self.n_regimes = n_regimes
        self.d_routing = d_routing
        self.cost_alpha = cost_alpha
        self.registry = expert_registry

        n_experts = len(expert_registry.names) if expert_registry is not None else 8
        self.register_buffer(
            "capability_cards",
            torch.ones(n_experts, n_regimes) / n_regimes,
        )
        self.register_buffer(
            "latency_costs",
            torch.ones(n_experts) * 30.0,
        )

        self.regime_encoder = nn.Sequential(
            nn.Linear(n_regimes, d_routing),
            nn.GELU(),
            nn.Linear(d_routing, d_routing),
        )
        self.confidence_gate = nn.Linear(1, d_routing)
        self.routing_head = nn.Linear(d_routing, n_experts)

    def set_capability_cards(self, cards: torch.Tensor):
        self.capability_cards.copy_(cards)

    def set_latency_costs(self, costs: torch.Tensor):
        self.latency_costs.copy_(costs)

    def load_from_registry(self):
        if self.registry is None:
            return
        cards = self.registry.capability_matrix()
        latencies = self.registry.latency_vector()
        n = min(cards.shape[0], self.capability_cards.shape[0])
        self.capability_cards[:n] = cards[:n]
        self.latency_costs[:n] = latencies[:n]

    def forward(self, regime_probs: torch.Tensor,
                critic_confidence: Optional[torch.Tensor] = None,
                latency_budget_ms: Optional[float] = None,
                ) -> Dict[str, torch.Tensor]:
        """
        Args:
            regime_probs:      [B, n_regimes]
            critic_confidence: [B, 1] or None
            latency_budget_ms: float or None
        Returns:
            capability_match, route_recommendation, route_regret,
            routing_logits, selected_expert
        """
        B = regime_probs.shape[0]
        device = regime_probs.device

        table_match = regime_probs @ self.capability_cards.t()

        latency_norm = self.latency_costs / (self.latency_costs.max() + 1e-8)
        cost_penalty = self.cost_alpha * latency_norm.unsqueeze(0).expand(B, -1)

        if latency_budget_ms is not None:
            over_budget = (self.latency_costs > latency_budget_ms).float()
            cost_penalty = cost_penalty + over_budget.unsqueeze(0) * 10.0

        regime_embed = self.regime_encoder(regime_probs)
        if critic_confidence is not None:
            conf_in = critic_confidence.to(self.confidence_gate.weight.dtype)
            conf_mod = self.confidence_gate(conf_in)
            regime_embed = regime_embed + conf_mod.to(regime_embed.dtype)

        learned_logits = self.routing_head(regime_embed)
        combined = table_match + 0.1 * learned_logits - cost_penalty

        scores, indices = combined.sort(dim=-1, descending=True)
        regret = scores[:, 0] - scores[:, 1] if combined.shape[1] > 1 else combined.new_zeros(B)
        selected = indices[:, 0]

        return {
            "capability_match": table_match,
            "route_recommendation": indices,
            "route_regret": regret,
            "routing_logits": learned_logits,
            "cost_adjusted_scores": combined,
            "selected_expert": selected,
        }

    def dispatch(self, expert_id: int, images: torch.Tensor,
                 context: Optional[Dict[str, torch.Tensor]] = None,
                 ) -> Optional[ExpertOutput]:
        if self.registry is None:
            return None
        names = sorted(self.registry.names)
        if expert_id >= len(names):
            return None
        adapter = self.registry.get(names[expert_id])
        t0 = time.perf_counter()
        out = adapter.forward(images, context)
        latency_ms = (time.perf_counter() - t0) * 1000
        out.metadata.setdefault("dispatch_latency_ms", latency_ms)
        out.metadata.setdefault("selected_expert_id", expert_id)
        out.metadata.setdefault("selected_expert_name", names[expert_id])
        out.metadata.setdefault("adapter_is_loaded", bool(adapter.is_loaded))
        out.metadata.setdefault(
            "adapter_is_available",
            bool(adapter.is_available()) if hasattr(adapter, "is_available") else False,
        )
        return out
