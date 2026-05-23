"""
Dream3R v0.4 cross-module contracts.

Defines typed dataclasses for every module boundary so the v0.4 closed-loop
orchestrator can pass structured signals between Perception, Memory,
Permanence, Critic, Composer/Expert, and Repair without leaking raw dicts.

These are forward-compatible: existing Dream3R.forward keeps returning a
dict, and the orchestrator wraps that dict into these contracts. Adding a
real DINOv3 backend / real expert backend later does not require changing
these signatures, only the producer side.

Repair action codes (v0.4 / v0.5 convention):
    0 = no_repair
    1 = local_rerun           (re-run perception+memory with deeper retrieval)
    2 = window_rerun          (re-run the full window forward, capped by max_repair_attempts)
    3 = reroute_model         (force composer to pick a different expert)
    4 = test3r_offpath_verify (dispatch Test3R off-path; result does NOT replace main output)
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import torch


ARCHITECTURE_VERSION = "v0.4"

REPAIR_ACTION_NAMES = {
    0: "no_repair",
    1: "local_rerun",
    2: "window_rerun",
    3: "reroute_model",
    4: "test3r_offpath_verify",
}

BACKEND_REAL = "real"
BACKEND_FALLBACK = "fallback"
BACKEND_STUB = "stub"


# ---------------------------------------------------------------------------
# Perception
# ---------------------------------------------------------------------------

@dataclass
class PerceptionOutput:
    """C1 Perceiver contract.

    feature_tokens:     [B, N, P, D]  per-frame patch tokens
    pointmap_proposal:  [B, N, P, 3]  per-frame 3D position proposal
    confidence:         [B, N, P, 1]  per-token confidence in [0, 1]
    evidence_signals:   {name: [B, N, d_evidence]}  17 named evidence channels
    backbone_status:    metadata about the visual backbone actually used
    """
    feature_tokens: torch.Tensor
    pointmap_proposal: torch.Tensor
    confidence: torch.Tensor
    evidence_signals: Dict[str, torch.Tensor] = field(default_factory=dict)
    backbone_status: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Memory
# ---------------------------------------------------------------------------

@dataclass
class MemoryOutput:
    """C2 SpatialMemory contract.

    fused_context:           [B, D]            pooled cross-branch memory
    latent_drift_proxy:      [B, 1]            published to bus as drift signal
    bank_occupancy:          [B]               valid anchors currently in bank
    selected_anchor_stats:   per-tick summary of selected branch (top-k, scores)
    retrieval_log:           raw NSA + recall log (passthrough)
    memory_backend_status:   recurrence type, NSA enabled, stable memory enabled
    """
    fused_context: torch.Tensor
    latent_drift_proxy: torch.Tensor
    bank_occupancy: torch.Tensor
    selected_anchor_stats: Dict[str, Any] = field(default_factory=dict)
    retrieval_log: Dict[str, Any] = field(default_factory=dict)
    memory_backend_status: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Permanence
# ---------------------------------------------------------------------------

@dataclass
class PermanenceOutput:
    """C3 Permanence contract.

    dynamic_logits:        [B, S, 3]   region classifier logits (suppress/admit/defer)
    dynamic_mask_proxy:    [B, S]      bool proxy mask True where slot is dynamic-suppressed
    dynamic_mask_final:    [B, S]      optional final D2 mask; coexists with proxy during transition
    dynamic_ratio:         [B, S, 1]   per-slot dynamic ratio
    suppress_static_write: [B, S]      CR-2 handoff signal (binding on Memory)
    object_track_set:      [B, S, D]   slot embeddings
    stable_promotion_log:  mint confidence + slot match info
    """
    dynamic_logits: torch.Tensor
    dynamic_mask_proxy: torch.Tensor
    dynamic_mask_final: Optional[torch.Tensor]
    dynamic_ratio: torch.Tensor
    suppress_static_write: torch.Tensor
    object_track_set: torch.Tensor
    stable_promotion_log: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Critic
# ---------------------------------------------------------------------------

@dataclass
class CriticDecision:
    """C4 Critic contract.

    conflict_score:    [B, 1]    scalar conflict per batch element
    repair_action:     [B]       v0.4 action codes 0..3 (see module docstring)
    reroute_hint:      [B] bool  True iff repair_action == 3
    reason_codes:      per-batch list of short codes explaining the action
    local_window_ids:  window timesteps affected (single tick by default)
    critic_log:        raw critic outputs (geometric log + repair logits)
    """
    conflict_score: torch.Tensor
    repair_action: torch.Tensor
    reroute_hint: torch.Tensor
    reason_codes: List[List[str]] = field(default_factory=list)
    local_window_ids: List[int] = field(default_factory=list)
    critic_log: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Composer / Expert
# ---------------------------------------------------------------------------

@dataclass
class ComposerDecision:
    """C5 Composer router decision (pre-dispatch)."""
    selected_expert: torch.Tensor          # [B] expert index
    routing_logits: torch.Tensor           # [B, n_experts]
    cost_adjusted_scores: torch.Tensor     # [B, n_experts]
    route_recommendation: torch.Tensor     # [B, n_experts] sorted indices
    capability_match: torch.Tensor         # [B, n_experts]
    route_regret: torch.Tensor             # [B]
    reroute_applied: bool = False
    backend_status: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DispatchedExpertOutput:
    """Wrapper around ExpertOutput that also carries explicit backend status.

    Mirrors composer_experts.base_adapter.ExpertOutput but adds an explicit
    backend_status block so downstream consumers do not have to dig through
    the freeform metadata dict.
    """
    pointmap: torch.Tensor                 # [B, N, P, 3]
    confidence: torch.Tensor               # [B, N, P, 1]
    evidence_tokens: torch.Tensor          # [B, N, n_ev, d_ev]
    expert_name: str
    backend_status: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Repair
# ---------------------------------------------------------------------------

@dataclass
class RepairAttempt:
    """Single entry in the repair_action_log."""
    attempt_index: int
    action_code: int
    action_name: str
    reason: str
    triggered_by_critic: bool
    succeeded: bool
    note: str = ""


@dataclass
class OffpathVerification:
    """Result of a Test3R off-path verification dispatch.

    This is a side-channel result that does NOT replace the main output.
    It records the off-path expert's pointmap shape, confidence, and
    whether the off-path result was accepted (always False in v0.5 scaffold).
    """
    expert_id: str
    backend: str  # "real" | "fallback" | "stub"
    triggered_by: str  # reason code
    pointmap_shape: List[int] = field(default_factory=list)
    confidence_mean: float = 0.0
    accepted_as_main_output: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RepairReport:
    """Repair executor summary for one pipeline.forward call."""
    final_action: int
    final_action_name: str
    n_attempts: int
    max_attempts: int
    reroute_hint: bool
    attempts: List[RepairAttempt] = field(default_factory=list)
    capped: bool = False
    offpath_verification: Optional['OffpathVerification'] = None


# ---------------------------------------------------------------------------
# Final
# ---------------------------------------------------------------------------

@dataclass
class ReconstructionOutput:
    """v0.4 final pipeline output.

    All v0.4 closure tests assert against fields of this dataclass.
    """
    pointmap: torch.Tensor
    confidence: torch.Tensor
    dynamic_logits: torch.Tensor
    dynamic_mask_proxy: torch.Tensor
    dynamic_mask_final: Optional[torch.Tensor]
    evidence: torch.Tensor                  # evidence_tokens from selected expert
    selected_expert: torch.Tensor           # final expert id (post-reroute)
    backend_status: Dict[str, Any]
    conflict_score: torch.Tensor
    memory_log: Dict[str, Any]
    route_log: Dict[str, Any]
    repair_action_log: Dict[str, Any]
    contract_log: List[Dict[str, Any]]
    architecture_version: str = ARCHITECTURE_VERSION
    perception: Optional[PerceptionOutput] = None
    memory: Optional[MemoryOutput] = None
    permanence: Optional[PermanenceOutput] = None
    critic: Optional[CriticDecision] = None
    composer: Optional[ComposerDecision] = None
    expert: Optional[DispatchedExpertOutput] = None
    repair: Optional[RepairReport] = None
    next_memory_state: Optional[torch.Tensor] = None
    next_object_slots: Optional[torch.Tensor] = None
    next_object_slot_poses: Optional[torch.Tensor] = None
