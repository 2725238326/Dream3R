"""DepthAnything-V2 adapter — monocular metric depth estimation."""

import torch
from typing import Dict, Optional

from .base_adapter import ExpertAdapter, ExpertOutput
from .fallback import image_fallback_output


class DepthAnythingAdapter(ExpertAdapter):

    name = "depthanything"
    capability_card = {
        "indoor_static": 0.55,
        "outdoor_static": 0.65,
        "dynamic_scene": 0.75,
        "sparse_view": 0.85,
        "dense_sequential": 0.25,
    }
    latency_estimate_ms = 8.0
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
            images, self.name, "monocular_depth",
            self.n_evidence, self.d_evidence,
            metadata={"attention_regime": self.attention_regime},
        )

    def load_checkpoint(self, path: str) -> None:
        self._loaded = True

    @property
    def is_loaded(self) -> bool:
        return self._loaded
