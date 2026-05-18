"""MoGe-2 adapter — monocular geometry estimation."""

import torch
from typing import Dict, Optional

from .base_adapter import ExpertAdapter, ExpertOutput
from .fallback import image_fallback_output


class MoGe2Adapter(ExpertAdapter):

    name = "moge2"
    capability_card = {
        "indoor_static": 0.5,
        "outdoor_static": 0.6,
        "dynamic_scene": 0.7,
        "sparse_view": 0.9,
        "dense_sequential": 0.3,
    }
    latency_estimate_ms = 18.0
    attention_regime = "full"

    def __init__(self, d_out: int = 768, n_evidence: int = 17,
                 d_evidence: int = 32, **kwargs):
        self.d_out = d_out
        self.n_evidence = n_evidence
        self.d_evidence = d_evidence
        self._loaded = False

    def forward(self, images: torch.Tensor,
                context: Optional[Dict[str, torch.Tensor]] = None,
                ) -> ExpertOutput:
        return image_fallback_output(
            images, self.name, "monocular_geometry",
            self.n_evidence, self.d_evidence,
            metadata={"attention_regime": self.attention_regime},
        )

    def load_checkpoint(self, path: str) -> None:
        self._loaded = True

    @property
    def is_loaded(self) -> bool:
        return self._loaded
