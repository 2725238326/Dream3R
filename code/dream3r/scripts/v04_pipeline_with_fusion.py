"""V04Pipeline subclass that injects Stage 6 fusion head after expert dispatch.

This is the minimal extension that connects ``memory.fused_context`` and
``critic.conflict_score`` to the final pointmap output, **without
modifying v0.3/v0.5 core**. ``code/dream3r/orchestrator.py`` is read-only
here — we subclass ``V04Pipeline`` and override only the forward call to
swap in a refined pointmap.

The subclass is the entry point for both training (``train_fusion_head.py``)
and downstream evaluation. At inference time, calling
``pipeline(images=...)`` returns a ``ReconstructionOutput`` whose
``pointmap`` field is the head's refined output (instead of the raw
``expert.pointmap``). All other fields are passed through unchanged.
"""

from __future__ import annotations

import dataclasses
from typing import Optional

import torch

from dream3r.contracts import ReconstructionOutput
from dream3r.fusion_head import Stage6FusionHead
from dream3r.orchestrator import V04Pipeline


class V04PipelineWithFusion(V04Pipeline):
    """V04Pipeline + post-dispatch Stage 6 fusion head.

    Args:
        model:           Dream3R instance (same as V04Pipeline).
        fusion_head:     Stage6FusionHead instance (constructed externally
                         so d_memory can match the model preset).
        max_repair_attempts:  forwarded to V04Pipeline.
    """

    def __init__(
        self,
        model: torch.nn.Module,
        fusion_head: Stage6FusionHead,
        max_repair_attempts: int = 1,
    ):
        super().__init__(model=model, max_repair_attempts=max_repair_attempts)
        self.fusion_head = fusion_head

    def forward(self, *args, **kwargs) -> ReconstructionOutput:
        out = super().forward(*args, **kwargs)
        refined = self._refine_pointmap(out)
        if refined is None:
            return out
        return dataclasses.replace(out, pointmap=refined)

    # ------------------------------------------------------------------
    # Internal: extract the four head inputs from ReconstructionOutput
    # ------------------------------------------------------------------

    def _refine_pointmap(self, out: ReconstructionOutput) -> Optional[torch.Tensor]:
        """Returns refined pointmap or None if any required input is missing."""
        expert = out.expert
        memory = out.memory
        critic = out.critic
        if expert is None or memory is None or critic is None:
            return None

        expert_pointmap = expert.pointmap
        expert_confidence = expert.confidence
        memory_context = memory.fused_context
        conflict_score = critic.conflict_score

        if expert_pointmap is None or expert_confidence is None:
            return None
        # memory_context / conflict_score are allowed to be None — the
        # head handles them as zeros internally.
        return self.fusion_head(
            expert_pointmap=expert_pointmap,
            expert_confidence=expert_confidence,
            memory_context=memory_context,
            conflict_score=conflict_score,
        )


def build_v04_pipeline_with_fusion(
    model: torch.nn.Module,
    d_memory: int,
    head_dim: int = 64,
    hidden: int = 128,
    max_repair_attempts: int = 1,
) -> V04PipelineWithFusion:
    """Convenience constructor mirroring ``build_v04_pipeline``."""
    head = Stage6FusionHead(d_memory=d_memory, head_dim=head_dim, hidden=hidden)
    return V04PipelineWithFusion(
        model=model,
        fusion_head=head,
        max_repair_attempts=max_repair_attempts,
    )
