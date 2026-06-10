"""Dream3R v1.1.0 domain-conditional official release wrapper.

This module exposes the current official Dream3R policy as a stable callable
surface:

* KITTI-style windows use the v1.0-rc1 bounded ProposalSetDecoder fallback.
* ETH3D-style windows use the VGGT-Omega-expanded SCF head.

The wrapper does not run image experts itself. It consumes the proposal bank
and Dream state tensors produced by the existing cache/runtime pipeline.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

import torch
import torch.nn as nn

from dream3r.release_candidate import (
    Dream3RReleaseCandidate,
    Dream3RReleaseConfig,
    build_dream3r_release_candidate,
)
from dream3r.scf_head import SCFHead


RELEASE_V11_VERSION = "v1.1.0"
RELEASE_V11_CANDIDATE = "domain_conditional_vggt_teacher"
KITTI_POLICY = "v1.0-rc1 bounded StatePrior + residual"
ETH3D_POLICY = "VGGT-Omega-expanded SCF correct-state"
KITTI_EXPERT_ORDER = ("fast3r", "mast3r", "spann3r")
ETH3D_EXPERT_ORDER = ("fast3r", "mast3r", "spann3r", "vggt_omega")


@dataclass(frozen=True)
class Dream3RDomainConditionalConfig:
    """Configuration for the v1.1.0 domain-conditional wrapper."""

    kitti: Dream3RReleaseConfig = field(default_factory=Dream3RReleaseConfig)
    eth3d_n_experts: int = len(ETH3D_EXPERT_ORDER)
    eth3d_d_memory: int = 32
    eth3d_head_dim: int = 64
    eth3d_hidden: int = 128
    eth3d_use_state: bool = True
    eth3d_use_residual: bool = False
    eth3d_conflict_dampening_strength: float = 0.0
    eth3d_expert_order: tuple[str, ...] = ETH3D_EXPERT_ORDER

    @classmethod
    def from_eth3d_checkpoint_config(
        cls,
        eth3d_config: Dict[str, Any],
        kitti_config: Optional[Dream3RReleaseConfig] = None,
    ) -> "Dream3RDomainConditionalConfig":
        return cls(
            kitti=kitti_config or Dream3RReleaseConfig(),
            eth3d_n_experts=int(eth3d_config.get("n_experts", len(ETH3D_EXPERT_ORDER))),
            eth3d_d_memory=int(eth3d_config.get("d_memory", 32)),
            eth3d_head_dim=int(eth3d_config.get("head_dim", 64)),
            eth3d_hidden=int(eth3d_config.get("hidden", 128)),
            eth3d_use_state=bool(eth3d_config.get("use_state", True)),
            eth3d_use_residual=bool(
                eth3d_config.get("use_residual", False)
            ),
            eth3d_conflict_dampening_strength=float(
                eth3d_config.get("conflict_dampening_strength", 0.0)
            ),
            eth3d_expert_order=tuple(
                eth3d_config.get("expert_order", ETH3D_EXPERT_ORDER)
            ),
        )


class Dream3RDomainConditionalRelease(nn.Module):
    """Callable v1.1.0 policy wrapper for proposal-bank inference.

    Inputs are the same tensor family as the existing SCF/ProposalSetDecoder
    path. Pass ``domain="kitti"`` or ``domain="eth3d"`` to choose the branch.
    """

    def __init__(
        self,
        config: Optional[Dream3RDomainConditionalConfig] = None,
        kitti_model: Optional[Dream3RReleaseCandidate] = None,
        eth3d_head: Optional[SCFHead] = None,
    ):
        super().__init__()
        self.config = config or Dream3RDomainConditionalConfig()
        self._validate_config(self.config)
        self.kitti_model = kitti_model or Dream3RReleaseCandidate(self.config.kitti)
        self.eth3d_head = eth3d_head or SCFHead(
            n_experts=self.config.eth3d_n_experts,
            d_memory=self.config.eth3d_d_memory,
            head_dim=self.config.eth3d_head_dim,
            hidden=self.config.eth3d_hidden,
            use_state=self.config.eth3d_use_state,
            use_residual=self.config.eth3d_use_residual,
            conflict_dampening_strength=self.config.eth3d_conflict_dampening_strength,
        )

    @staticmethod
    def _validate_config(config: Dream3RDomainConditionalConfig) -> None:
        if tuple(config.kitti.expert_order) != KITTI_EXPERT_ORDER:
            raise ValueError(f"KITTI policy requires expert_order={KITTI_EXPERT_ORDER}")
        if tuple(config.eth3d_expert_order) != ETH3D_EXPERT_ORDER:
            raise ValueError(f"ETH3D policy requires expert_order={ETH3D_EXPERT_ORDER}")
        if config.eth3d_n_experts != len(config.eth3d_expert_order):
            raise ValueError("eth3d_n_experts must match eth3d_expert_order length")
        if not config.eth3d_use_state:
            raise ValueError("v1.1.0 ETH3D policy requires use_state=True")
        if config.eth3d_use_residual:
            raise ValueError("v1.1.0 ETH3D policy uses convex SCF without residual")
        if not 0.0 <= config.eth3d_conflict_dampening_strength <= 1.0:
            raise ValueError("eth3d_conflict_dampening_strength must be in [0, 1]")

    @classmethod
    def from_checkpoints(
        cls,
        *,
        kitti_checkpoint: str | Path | None = None,
        eth3d_checkpoint: str | Path | None = None,
        map_location: str | torch.device = "cpu",
        strict: bool = True,
    ) -> "Dream3RDomainConditionalRelease":
        kitti_model = build_dream3r_release_candidate(kitti_checkpoint)
        eth_config: Dict[str, Any] = {}
        eth_head: Optional[SCFHead] = None
        if eth3d_checkpoint is not None:
            ckpt = torch.load(eth3d_checkpoint, map_location=map_location, weights_only=False)
            eth_config = dict(ckpt.get("config", {}))
            eth_config.setdefault("expert_order", ETH3D_EXPERT_ORDER)
            cfg = Dream3RDomainConditionalConfig.from_eth3d_checkpoint_config(
                eth_config,
                kitti_model.config,
            )
            eth_head = SCFHead(
                n_experts=cfg.eth3d_n_experts,
                d_memory=cfg.eth3d_d_memory,
                head_dim=cfg.eth3d_head_dim,
                hidden=cfg.eth3d_hidden,
                use_state=cfg.eth3d_use_state,
                use_residual=cfg.eth3d_use_residual,
                conflict_dampening_strength=cfg.eth3d_conflict_dampening_strength,
            )
            eth_head.load_state_dict(ckpt["head_state_dict"], strict=strict)
            eth_head.eval()
            return cls(cfg, kitti_model=kitti_model, eth3d_head=eth_head)
        return cls(kitti_model=kitti_model)

    def forward(
        self,
        proposal_pointmaps: torch.Tensor,
        proposal_confidences: torch.Tensor,
        memory_context: Optional[torch.Tensor] = None,
        conflict_score: Optional[torch.Tensor] = None,
        *,
        domain: str,
    ) -> Dict[str, Any]:
        domain_key = domain.lower()
        if domain_key in {"kitti", "kitti_long"}:
            out = self.kitti_model(
                proposal_pointmaps,
                proposal_confidences,
                memory_context,
                conflict_score,
            )
            out["release_version"] = RELEASE_V11_VERSION
            out["domain_branch"] = "kitti_v1_0_rc1"
            return out
        if domain_key in {"eth3d", "eth3d_long"}:
            out = self.eth3d_head(
                proposal_pointmaps,
                proposal_confidences,
                memory_context,
                conflict_score,
            )
            out["release_version"] = RELEASE_V11_VERSION
            out["domain_branch"] = "eth3d_vggt_omega_scf"
            return out
        raise ValueError(f"unsupported domain for v1.1 policy: {domain}")

    def release_metadata(self) -> Dict[str, Any]:
        return {
            "version": RELEASE_V11_VERSION,
            "release_candidate": RELEASE_V11_CANDIDATE,
            "metric": "AbsRel",
            "metric_direction": "lower_is_better",
            "policy": {
                "kitti": KITTI_POLICY,
                "eth3d": ETH3D_POLICY,
            },
            "expert_order": {
                "kitti": list(KITTI_EXPERT_ORDER),
                "eth3d": list(ETH3D_EXPERT_ORDER),
            },
            "selected_kitti_abs_rel": 0.1448,
            "selected_eth3d_abs_rel": 0.0570,
            "controls": {
                "kitti_state_abs_rel": 0.1448,
                "kitti_no_state_abs_rel": 0.1553,
                "kitti_shuffle_abs_rel": 0.1521,
                "eth3d_state_abs_rel": 0.0570,
                "eth3d_no_state_abs_rel": 0.0583,
                "eth3d_shuffle_abs_rel": 0.0598,
            },
            "config": asdict(self.config),
        }


def build_dream3r_v11_release(
    *,
    kitti_checkpoint: str | Path | None = None,
    eth3d_checkpoint: str | Path | None = None,
    d_memory: int | None = None,
    eth3d_conflict_dampening_strength: float = 0.0,
) -> Dream3RDomainConditionalRelease:
    """Build the v1.1.0 domain-conditional Dream3R wrapper."""

    if kitti_checkpoint is not None or eth3d_checkpoint is not None:
        if d_memory is not None or eth3d_conflict_dampening_strength != 0.0:
            raise ValueError(
                "d_memory/conflict-dampening overrides are only valid without checkpoints"
            )
        return Dream3RDomainConditionalRelease.from_checkpoints(
            kitti_checkpoint=kitti_checkpoint,
            eth3d_checkpoint=eth3d_checkpoint,
        )
    if d_memory is not None or eth3d_conflict_dampening_strength != 0.0:
        memory_dim = 32 if d_memory is None else int(d_memory)
        return Dream3RDomainConditionalRelease(
            Dream3RDomainConditionalConfig(
                kitti=Dream3RReleaseConfig(d_memory=memory_dim),
                eth3d_d_memory=memory_dim,
                eth3d_conflict_dampening_strength=float(
                    eth3d_conflict_dampening_strength
                ),
            )
        )
    return Dream3RDomainConditionalRelease()
