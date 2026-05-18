"""
Cross-spec Memory Bus (C6) — the typed tensor namespace connecting all modules.

Implements three surfaces:
  1. Published signals (read-only contract)
  2. Handoff signals (binding commands)
  3. CR-1..CR-6 gate modules
"""

import torch
import torch.nn as nn
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple
from enum import IntEnum
import math


class EvidenceLabel(IntEnum):
    UNKNOWN = 0
    SPECULATIVE = 1
    INFERRED = 2
    PAPER_DERIVED = 3
    PAPER_PROVEN = 4


@dataclass
class BusSignal:
    tensor: torch.Tensor
    label: EvidenceLabel
    producer: str
    timestep: int


class MemoryBus(nn.Module):
    """
    C6: Cross-spec memory bus. Zero learned parameters.
    Implements publish/read/handoff + CR-1..CR-6 gates.
    """

    def __init__(self, epsilon_spread: float = 0.05, epsilon_tie: float = 0.05,
                 cr3_mid_threshold: float = 0.4,
                 cr3_high_threshold: float = 0.7,
                 cr3_max_k: int = 32,
                 cr3_high_scale: float = 2.0):
        super().__init__()
        self.epsilon_spread = epsilon_spread
        self.epsilon_tie = epsilon_tie
        self.cr3_mid_threshold = cr3_mid_threshold
        self.cr3_high_threshold = cr3_high_threshold
        self.cr3_max_k = cr3_max_k
        self.cr3_high_scale = cr3_high_scale
        self._signals: Dict[str, BusSignal] = {}
        self._previous_signals: Dict[str, BusSignal] = {}
        self._handoffs: Dict[str, BusSignal] = {}
        self._contract_log: list = []
        self._owner_table = {
            "conflict_score": "critic",
            "recommended_action": "critic",
            "route_history": "critic",
            "route_regret_estimate": "critic",
            "latent_drift_proxy": "memory",
            "anchor_set": "memory",
            "policy_log": "memory",
            "selected_anchors": "memory",
            "memory_retrieval_log": "memory",
            "bank_occupancy": "memory",
            "quarantine_count": "memory",
            "nsa_branch_weights": "memory",
            "dynamic_ratio": "permanence",
            "object_track_stability": "permanence",
            "suppress_static_write": "permanence",
            "admit_static_write": "permanence",
            "capability_match": "composer",
            "route_recommendation": "composer",
            "route_regret": "composer",
            "regime_card": "composer",
            "routed_expert_id": "composer",
            "expert_latency": "composer",
            "routing_logits": "composer",
            "cost_adjusted_scores": "composer",
        }

    def reset(self):
        self._previous_signals = {
            name: BusSignal(
                signal.tensor.detach() if isinstance(signal.tensor, torch.Tensor) else signal.tensor,
                signal.label,
                signal.producer,
                signal.timestep,
            )
            for name, signal in self._signals.items()
        }
        self._signals.clear()
        self._handoffs.clear()

    def publish(self, signal_name: str, tensor: torch.Tensor,
                label: EvidenceLabel, producer: str, timestep: int):
        expected_owner = self._owner_table.get(signal_name)
        if expected_owner and expected_owner != producer:
            raise RuntimeError(
                f"Contract violation: {producer} tried to publish {signal_name}, "
                f"owned by {expected_owner}"
            )
        self._signals[signal_name] = BusSignal(tensor, label, producer, timestep)

    def read(self, signal_name: str, consumer: str) -> Optional[BusSignal]:
        signal = self._signals.get(signal_name)
        if signal is not None:
            self._contract_log.append({
                "signal": signal_name,
                "producer": signal.producer,
                "label": signal.label,
                "consumer": consumer,
                "t": signal.timestep,
                "source": "current",
            })
        return signal

    def read_previous(self, signal_name: str, consumer: str) -> Optional[BusSignal]:
        signal = self._previous_signals.get(signal_name)
        if signal is not None:
            self._contract_log.append({
                "signal": signal_name,
                "producer": signal.producer,
                "label": signal.label,
                "consumer": consumer,
                "t": signal.timestep,
                "source": "previous",
            })
        return signal

    def publish_handoff(self, signal_name: str, tensor: torch.Tensor,
                        producer: str, timestep: int):
        self._handoffs[signal_name] = BusSignal(
            tensor, EvidenceLabel.INFERRED, producer, timestep
        )

    def read_handoff(self, signal_name: str) -> Optional[BusSignal]:
        return self._handoffs.get(signal_name)

    def gate_cr1(self) -> Optional[torch.Tensor]:
        """CR-1: Critic A5 reroute requires Composer capability_match spread > epsilon."""
        cap = self._signals.get("capability_match")
        if cap is None:
            return None
        spread = cap.tensor.max() - cap.tensor.min()
        return (spread > self.epsilon_spread).float()

    def gate_cr2(self) -> Optional[torch.Tensor]:
        """CR-2: Permanence suppress_static_write is binding on Memory."""
        handoff = self._handoffs.get("suppress_static_write")
        if handoff is None:
            return None
        suppress = handoff.tensor
        if suppress.dim() == 2:
            return (suppress.float().mean(dim=-1) > 0.5).float()
        return suppress

    def cr2_per_slot_suppress(self) -> Optional[torch.Tensor]:
        handoff = self._handoffs.get("suppress_static_write")
        if handoff is None:
            return None
        return handoff.tensor

    def gate_cr3(self, base_k: int = 8) -> int:
        """CR-3: Low Critic confidence increases retrieval depth.

        When conflict_score is high (meaning the Critic is uncertain about
        reconstruction quality), the Memory should retrieve more bank entries
        to gather additional evidence. Returns an adjusted top-k value.
        """
        conflict = self._previous_signals.get("conflict_score")
        if conflict is None:
            return base_k
        conf_mean = torch.sigmoid(conflict.tensor).mean().item()
        if conf_mean <= self.cr3_mid_threshold:
            return base_k

        span = max(self.cr3_high_threshold - self.cr3_mid_threshold, 1e-6)
        ratio = min(max((conf_mean - self.cr3_mid_threshold) / span, 0.0), 1.0)
        scale = 1.0 + ratio * (self.cr3_high_scale - 1.0)
        return min(math.ceil(base_k * scale), self.cr3_max_k)

    def cr3_retrieval_bias(self) -> Optional[torch.Tensor]:
        """CR-3 auxiliary: return Critic confidence as a retrieval bias weight.

        Modules can use this to bias retrieval scoring toward entries that
        were written under high confidence.
        """
        conflict = self._previous_signals.get("conflict_score")
        if conflict is None:
            return None
        return 1.0 - torch.sigmoid(conflict.tensor)

    def cr3_permanence_bias(self) -> Optional[torch.Tensor]:
        """CR-3 auxiliary: permanence link bias for spatial retrieval.

        Entries associated with tracked objects (high permanence) should
        be preferred during retrieval under uncertainty.
        """
        perm = self._signals.get("dynamic_ratio")
        if perm is None:
            return None
        dynamic_ratio = perm.tensor
        if dynamic_ratio.dim() == 3:
            dynamic_ratio = dynamic_ratio.mean(dim=1)
        return 1.0 - dynamic_ratio

    def gate_cr4(self, route_history: Optional[torch.Tensor] = None
                 ) -> Optional[torch.Tensor]:
        """CR-4: Tiebreak on capability ties using Critic-internal preference."""
        cap = self._signals.get("capability_match")
        if cap is None:
            return None
        scores = cap.tensor
        top2 = torch.topk(scores.flatten(), min(2, scores.numel()))
        if top2.values.numel() < 2:
            return top2.indices[0:1]
        if (top2.values[0] - top2.values[1]).abs() < self.epsilon_tie:
            if route_history is not None:
                mask = torch.ones_like(scores.flatten(), dtype=torch.bool)
                for idx in route_history.long().flatten():
                    if idx < mask.numel():
                        mask[idx] = False
                masked = scores.flatten().clone()
                masked[~mask] = -float("inf")
                return masked.argmax(dim=-1, keepdim=True)
        return top2.indices[0:1]

    def propagate_labels_cr5(self, read_labels: list) -> EvidenceLabel:
        """CR-5: Output label = MIN of all input labels."""
        if not read_labels:
            return EvidenceLabel.UNKNOWN
        return EvidenceLabel(min(read_labels))

    def get_contract_log(self) -> list:
        """CR-6: Return the audit log."""
        return self._contract_log
