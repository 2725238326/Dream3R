"""Dream3R v1.2 experimental core-integrated architecture.

This module is deliberately not the official release. It opens a controlled
research lane where the historical Dream3R core produces Memory/Critic state
and feeds that state into the proposal-fusion decoder inside ``Dream3R.forward``.

The purpose is to stop treating the release proposal-fusion path as an external
wrapper only. v1.1.0 remains the stable fallback until this lane beats its
metrics and state/no-state/shuffle controls.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

import torch
import torch.nn as nn

from dream3r.model import Dream3R


RELEASE_V12_EXPERIMENTAL_VERSION = "v1.2-exp0"
RELEASE_V12_EXPERIMENTAL_CANDIDATE = "core_state_conditioned_proposal_fusion"
V12_BRANCH = "v12_core_state_conditioned_proposal_fusion"


@dataclass(frozen=True)
class Dream3RV12ExperimentalConfig:
    """Small, explicit config for the v1.2 experimental core bridge."""

    d_model: int = 128
    d_memory: int = 128
    n_state_tokens: int = 16
    bank_capacity: int = 128
    nsa_select_k: int = 4
    nsa_heads: int = 4
    n_evidence: int = 17
    d_evidence: int = 16
    d_slot: int = 64
    n_slots: int = 8
    d_critic: int = 128
    n_regimes: int = 6
    d_routing: int = 32
    n_experts: int = 3
    proposal_token_dim: int = 64
    proposal_state_dim: int = 64
    proposal_hidden: int = 128
    proposal_num_layers: int = 2
    proposal_num_heads: int = 4
    proposal_residual_refine_scale: float = 0.05
    use_state: bool = True
    use_state_prior: bool = True

    def to_core_config(self) -> Dict[str, Any]:
        return {
            "version": "v03",
            "d_model": self.d_model,
            "d_memory": self.d_memory,
            "memory_frame_input_dim": self.d_model,
            "n_state_tokens": self.n_state_tokens,
            "bank_capacity": self.bank_capacity,
            "nsa_select_k": self.nsa_select_k,
            "nsa_heads": self.nsa_heads,
            "n_evidence": self.n_evidence,
            "d_evidence": self.d_evidence,
            "d_slot": self.d_slot,
            "n_slots": self.n_slots,
            "d_critic": self.d_critic,
            "n_regimes": self.n_regimes,
            "d_routing": self.d_routing,
            "use_backbone": False,
            "img_size": 224,
            "memory_use_nsa": True,
            "enable_stable_memory": True,
            "enable_proposal_fusion_bridge": True,
            "proposal_fusion_n_experts": self.n_experts,
            "proposal_fusion_d_memory": self.d_memory,
            "proposal_fusion_token_dim": self.proposal_token_dim,
            "proposal_fusion_state_dim": self.proposal_state_dim,
            "proposal_fusion_hidden": self.proposal_hidden,
            "proposal_fusion_num_layers": self.proposal_num_layers,
            "proposal_fusion_num_heads": self.proposal_num_heads,
            "proposal_fusion_use_state": self.use_state,
            "proposal_fusion_use_state_prior": self.use_state_prior,
            "proposal_fusion_residual_refine_scale": self.proposal_residual_refine_scale,
        }


class Dream3RV12Experimental(nn.Module):
    """Core-integrated experimental Dream3R architecture."""

    def __init__(self, config: Optional[Dream3RV12ExperimentalConfig] = None):
        super().__init__()
        self.config = config or Dream3RV12ExperimentalConfig()
        self.core = Dream3R(self.config.to_core_config())

    def forward(
        self,
        x: torch.Tensor,
        proposal_pointmaps: torch.Tensor,
        proposal_confidences: torch.Tensor,
        regime_probs: Optional[torch.Tensor] = None,
        prev_memory_state: Optional[torch.Tensor] = None,
        prev_object_slots: Optional[torch.Tensor] = None,
        timestep: int = 0,
    ) -> Dict[str, Any]:
        out = self.core(
            x,
            regime_probs=regime_probs,
            prev_memory_state=prev_memory_state,
            prev_object_slots=prev_object_slots,
            timestep=timestep,
            proposal_pointmaps=proposal_pointmaps,
            proposal_confidences=proposal_confidences,
        )
        if "final_pointmap" not in out:
            raise RuntimeError("v1.2 experimental core did not produce proposal-fusion output")
        out["release_version"] = RELEASE_V12_EXPERIMENTAL_VERSION
        out["experimental_candidate"] = RELEASE_V12_EXPERIMENTAL_CANDIDATE
        out["architecture_branch"] = V12_BRANCH
        out["claim_boundary"] = (
            "experimental core-integrated state-conditioned proposal fusion; "
            "not official v1.1 replacement until metrics and controls pass"
        )
        return out

    def release_metadata(self) -> Dict[str, Any]:
        return {
            "version": RELEASE_V12_EXPERIMENTAL_VERSION,
            "release_candidate": RELEASE_V12_EXPERIMENTAL_CANDIDATE,
            "architecture_branch": V12_BRANCH,
            "official_fallback": "v1.1.0",
            "metric": "AbsRel",
            "metric_direction": "lower_is_better",
            "promotion_gate": [
                "beat v1.1.0 KITTI/ETH3D metrics",
                "correct-state beats no-state and shuffle controls",
                "fallback v1.1.0 remains callable",
            ],
            "config": asdict(self.config),
        }


def build_dream3r_v12_experimental(
    config: Optional[Dream3RV12ExperimentalConfig] = None,
) -> Dream3RV12Experimental:
    return Dream3RV12Experimental(config)
