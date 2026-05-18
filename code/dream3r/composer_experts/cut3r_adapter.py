"""CUT3R adapter — state-token recurrence for temporal continuity."""

import torch
import torch.nn.functional as F
from typing import Dict, Optional

from .base_adapter import ExpertAdapter, ExpertOutput
from .fallback import image_fallback_output


class CUT3RAdapter(ExpertAdapter):

    name = "cut3r"
    capability_card = {
        "indoor_static": 0.75,
        "outdoor_static": 0.7,
        "dynamic_scene": 0.65,
        "sparse_view": 0.8,
        "dense_sequential": 0.85,
    }
    latency_estimate_ms = 30.0
    attention_regime = "full"

    def __init__(self, d_out: int = 768, n_evidence: int = 17,
                 d_evidence: int = 32, n_state_tokens: int = 32, **kwargs):
        self.d_out = d_out
        self.n_evidence = n_evidence
        self.d_evidence = d_evidence
        self.n_state_tokens = n_state_tokens
        self._loaded = False

    def forward(self, images: torch.Tensor,
                context: Optional[Dict[str, torch.Tensor]] = None,
                ) -> ExpertOutput:
        B = images.shape[0]
        stats = F.adaptive_avg_pool2d(
            images.reshape(-1, *images.shape[2:]), (1, 1)
        ).reshape(B, -1)
        repeat = (self.n_state_tokens * self.d_out + stats.shape[-1] - 1) // stats.shape[-1]
        state_tokens = stats.repeat(1, repeat)[..., :self.n_state_tokens * self.d_out]
        state_tokens = state_tokens.view(B, self.n_state_tokens, self.d_out)
        return image_fallback_output(
            images, self.name, "state_token_recurrence",
            self.n_evidence, self.d_evidence,
            metadata={
                "attention_regime": self.attention_regime,
                "state_tokens": state_tokens,
            },
        )

    def load_checkpoint(self, path: str) -> None:
        self._loaded = True

    @property
    def is_loaded(self) -> bool:
        return self._loaded
