"""Dream3R v1.0-rc1 inference branch used for KITTI sequences.

The branch applies state-conditioned proposal fusion with bounded residual
refinement and exposes a stable checkpoint-loading interface.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import torch
import torch.nn as nn

from dream3r.proposal_set_decoder import ProposalSetDecoder


RELEASE_VERSION = "v1.0-rc1"
RELEASE_CANDIDATE = "frozen_state_prior_bounded_residual"
OFFICIAL_EXPERT_ORDER = ("fast3r", "mast3r", "spann3r")


@dataclass(frozen=True)
class Dream3RReleaseConfig:
    """Configuration for the official v1.0-rc1 architecture surface."""

    n_experts: int = 3
    d_memory: int = 32
    token_dim: int = 64
    state_dim: int = 64
    hidden: int = 128
    num_layers: int = 2
    num_heads: int = 4
    use_state: bool = True
    use_state_prior: bool = True
    prior_hidden: int = 128
    prior_logit_scale: float = 1.0
    residual_refine_scale: float = 0.05
    freeze_state_prior: bool = True
    prior_kl_weight: float = 0.1
    expert_order: tuple[str, ...] = OFFICIAL_EXPERT_ORDER

    @classmethod
    def from_checkpoint_config(cls, config: Dict[str, Any]) -> "Dream3RReleaseConfig":
        """Build release config from a ProposalSetDecoder checkpoint config."""

        fields = {
            "n_experts": int(config.get("n_experts", cls.n_experts)),
            "d_memory": int(config.get("d_memory", cls.d_memory)),
            "token_dim": int(config.get("token_dim", cls.token_dim)),
            "state_dim": int(config.get("state_dim", cls.state_dim)),
            "hidden": int(config.get("hidden", cls.hidden)),
            "num_layers": int(config.get("num_layers", cls.num_layers)),
            "num_heads": int(config.get("num_heads", cls.num_heads)),
            "use_state": bool(config.get("use_state", cls.use_state)),
            "use_state_prior": bool(config.get("use_state_prior", cls.use_state_prior)),
            "prior_hidden": int(config.get("prior_hidden", cls.prior_hidden)),
            "prior_logit_scale": float(config.get("prior_logit_scale", cls.prior_logit_scale)),
            "residual_refine_scale": float(
                config.get("residual_refine_scale", cls.residual_refine_scale)
            ),
            "freeze_state_prior": bool(
                config.get("freeze_state_prior", cls.freeze_state_prior)
            ),
            "prior_kl_weight": float(config.get("prior_kl_weight", cls.prior_kl_weight)),
        }
        return cls(**fields)


class Dream3RReleaseCandidate(nn.Module):
    """Stable inference wrapper for the selected Dream3R v1.0-rc1 model.

    Inputs follow the cached proposal-bank contract:

    - ``proposal_pointmaps``: ``[B, E, N, P, 3]``
    - ``proposal_confidences``: ``[B, E, N, P, 1]``
    - ``memory_context``: optional ``[B, D_mem]``
    - ``conflict_score``: optional ``[B, 1]``
    """

    def __init__(self, config: Optional[Dream3RReleaseConfig] = None):
        super().__init__()
        self.config = config or Dream3RReleaseConfig()
        self._validate_release_config(self.config)
        self.decoder = ProposalSetDecoder(
            n_experts=self.config.n_experts,
            d_memory=self.config.d_memory,
            token_dim=self.config.token_dim,
            state_dim=self.config.state_dim,
            hidden=self.config.hidden,
            num_layers=self.config.num_layers,
            num_heads=self.config.num_heads,
            use_state=self.config.use_state,
            use_state_prior=self.config.use_state_prior,
            prior_hidden=self.config.prior_hidden,
            prior_logit_scale=self.config.prior_logit_scale,
            residual_refine_scale=self.config.residual_refine_scale,
        )

    @staticmethod
    def _validate_release_config(config: Dream3RReleaseConfig) -> None:
        if config.n_experts != len(config.expert_order):
            raise ValueError("n_experts must match expert_order length")
        if tuple(config.expert_order) != OFFICIAL_EXPERT_ORDER:
            raise ValueError(f"v1.0-rc1 expert_order must be {OFFICIAL_EXPERT_ORDER}")
        if not config.use_state:
            raise ValueError("v1.0-rc1 requires use_state=True")
        if not config.use_state_prior:
            raise ValueError("v1.0-rc1 requires use_state_prior=True")
        if not config.freeze_state_prior:
            raise ValueError("v1.0-rc1 requires a frozen StatePrior branch")
        if config.residual_refine_scale <= 0:
            raise ValueError("v1.0-rc1 requires bounded residual refinement")

    @classmethod
    def from_checkpoint(
        cls,
        checkpoint_path: str | Path,
        map_location: str | torch.device = "cpu",
        strict: bool = True,
    ) -> "Dream3RReleaseCandidate":
        """Load the official wrapper from a ProposalSetDecoder checkpoint."""

        ckpt = torch.load(checkpoint_path, map_location=map_location)
        config = Dream3RReleaseConfig.from_checkpoint_config(ckpt.get("config", {}))
        model = cls(config)
        model.decoder.load_state_dict(ckpt["decoder_state_dict"], strict=strict)
        model.eval()
        return model

    def forward(
        self,
        proposal_pointmaps: torch.Tensor,
        proposal_confidences: torch.Tensor,
        memory_context: Optional[torch.Tensor] = None,
        conflict_score: Optional[torch.Tensor] = None,
    ) -> Dict[str, torch.Tensor]:
        out = self.decoder(
            proposal_pointmaps=proposal_pointmaps,
            proposal_confidences=proposal_confidences,
            memory_context=memory_context,
            conflict_score=conflict_score,
        )
        out["release_version"] = torch.tensor(1, device=proposal_pointmaps.device)
        return out

    def release_metadata(self) -> Dict[str, Any]:
        return {
            "version": RELEASE_VERSION,
            "release_candidate": RELEASE_CANDIDATE,
            "expert_order": list(self.config.expert_order),
            "metric": "AbsRel",
            "metric_direction": "lower_is_better",
            "selected_kitti_abs_rel": 0.1448,
            "selected_eth3d_abs_rel": 0.1475,
            "config": asdict(self.config),
        }


def build_dream3r_release_candidate(
    checkpoint_path: str | Path | None = None,
    d_memory: int = 32,
) -> Dream3RReleaseCandidate:
    """Build v1.0-rc1 from a checkpoint or default synthetic-safe config."""

    if checkpoint_path is not None:
        return Dream3RReleaseCandidate.from_checkpoint(checkpoint_path)
    return Dream3RReleaseCandidate(Dream3RReleaseConfig(d_memory=d_memory))
