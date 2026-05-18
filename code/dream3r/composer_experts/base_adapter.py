"""
Expert adapter base class and output contract for Dream3R C5 Composer.
"""

import torch
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class ExpertOutput:
    """Uniform output contract for all expert adapters."""
    pointmap: torch.Tensor              # [B, N, P, 3]
    confidence: torch.Tensor            # [B, N, P, 1]
    evidence_tokens: torch.Tensor       # [B, N, n_ev, d_ev]
    metadata: Dict[str, object] = field(default_factory=dict)


class ExpertAdapter(ABC):
    """
    ABC for Dream3R expert adapters.

    Each adapter wraps a specific 3R backbone (MASt3R, Fast3R, etc.) behind
    a uniform interface. Adapters define their capability card (per-regime
    suitability scores), latency estimate, and attention regime.

    In fallback mode (no checkpoint loaded), adapters produce deterministic
    image-derived outputs with correct shapes for architecture validation.
    """

    name: str = "base"
    capability_card: Dict[str, float] = {}
    latency_estimate_ms: float = 0.0
    attention_regime: str = "full"  # "full" | "linear" | "sparse"

    REGIMES = ["indoor_static", "outdoor_static", "dynamic_scene",
               "sparse_view", "dense_sequential"]

    @abstractmethod
    def forward(self, images: torch.Tensor,
                context: Optional[Dict[str, torch.Tensor]] = None,
                ) -> ExpertOutput:
        """
        Run inference through the expert.

        Args:
            images:  [B, N, 3, H, W]
            context: optional bus context (regime_probs, critic_confidence, etc.)
        Returns:
            ExpertOutput
        """
        ...

    @abstractmethod
    def load_checkpoint(self, path: str) -> None:
        """Load model weights from a checkpoint file."""
        ...

    def capability_tensor(self, regime_order: Optional[list] = None) -> torch.Tensor:
        order = regime_order or self.REGIMES
        return torch.tensor([self.capability_card.get(r, 0.0) for r in order])

    @property
    def is_loaded(self) -> bool:
        return False

    def is_available(self) -> bool:
        return False

    def has_checkpoint_artifacts(self) -> bool:
        return self.is_available()
