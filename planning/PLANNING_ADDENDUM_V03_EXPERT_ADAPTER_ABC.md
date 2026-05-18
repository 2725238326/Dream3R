# Planning addendum v0.3 — ExpertAdapter abstract base class specification

addendum_id:    PLANNING_ADDENDUM_V03_EXPERT_ADAPTER_ABC
date:           2026-05-07
cycle:          023 (S2 deliverable; per DEC-20260507-003)
addresses:      RA-02 [HIGH] from Path C Agent A review (cycle 022)
resolves:       Q-cs-2 from CODE_STRUCTURE §"Open questions"
parent_artifact: planning/DREAM3R_V02_CODE_STRUCTURE.md (cycle 020; NOT modified)
rule:           B-roadmap-F (no in-place modification; NEW addendum file)
source:         CODE_STRUCTURE §"composer_experts/", COMPOSER_CAPABILITY_DESCRIPTORS.md

---

## Problem statement

Path C Agent A (cycle 022) identified that Q-cs-2 (ExpertAdapter base class design) is
unresolved. The CODE_STRUCTURE file specifies "base class with shared `capability_match` +
`latency_estimate` + `attention_regime` slots" but does not define method signatures,
return-dict keys, or error protocol. All 7 adapter implementations are blocked without this.

## ExpertAdapter abstract base class

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import torch

class ExpertAdapter(ABC):
    """Base class for Dream3R v0.2 Composer expert adapters."""

    # --- Class-level slots (set by each subclass) ---

    expert_id: str                    # e.g., "mast3r", "fast3r", "test3r"
    attention_regime: str             # "full" | "linear" | "sparse"
    is_streaming_path: bool           # True = in 30-50 ms budget; False = lazy off-path
    checkpoint_source: str            # URL or path to official checkpoint
    license: str                      # e.g., "Apache-2.0", "non-commercial"

    # --- Required methods ---

    @abstractmethod
    def forward(
        self,
        frames: torch.Tensor,         # (B, N, C, H, W) or (B, C, H, W) for mono
        bus_signals: Dict[str, Any],   # read-only snapshot of current bus state
        **kwargs,
    ) -> Dict[str, torch.Tensor]:
        """Run expert inference and return standardized output dict.

        Required return keys:
          "pointmap":       (B, N, H, W, 3) or None if expert produces depth only
          "depth":          (B, N, H, W, 1) or None if expert produces pointmap only
          "confidence":     (B, N, H, W, 1) per-pixel confidence score
          "expert_id":      str (self.expert_id)
          "latency_ms":     float (wall-clock ms for this forward call)

        Optional return keys:
          "state_vector":   torch.Tensor if expert maintains persistent state (CUT3R)
          "match_features": torch.Tensor if expert produces matching features (MASt3R)
        """
        ...

    @abstractmethod
    def get_capability_match(self) -> Dict[str, float]:
        """Return capability_match vector for this expert.

        Required keys (per COMPOSER_CAPABILITY_DESCRIPTORS cross-axis table):
          "pair_quality", "multi_view_scale", "streaming", "mono",
          "dynamic", "long_context"

        Values: float in [0, 1]. Source: COMPOSER_CAPABILITY_DESCRIPTORS.md.
        These values are INFERRED until ABL-v02-5 (capability_match measurement)
        promotes them to MEASURED.
        """
        ...

    @abstractmethod
    def get_latency_estimate(self) -> Dict[str, float]:
        """Return latency profile for this expert.

        Required keys:
          "forward_ms":     expected per-call forward latency (inferred or measured)
          "vram_mb":        expected VRAM usage in fp16
          "params_m":       parameter count in millions

        Evidence label: inferred until bench_frame_budget.py measures actual values.
        """
        ...

    # --- Provided methods (shared) ---

    def is_available(self) -> bool:
        """Check if expert checkpoint is loadable. Returns True/False."""
        ...

    def load_checkpoint(self, path: str) -> None:
        """Load expert checkpoint. Raises CheckpointNotFoundError if missing."""
        ...
```

## Error protocol

```text
1. Missing checkpoint: raise CheckpointNotFoundError(expert_id, expected_path)
   at adapter initialization time. NOT at forward() time. NOT silent skip.
   The expert registry in __init__.py catches this and marks the expert as
   unavailable; Composer's routing policy skips unavailable experts with
   an explicit route_log entry.

2. Forward failure: raise ExpertForwardError(expert_id, original_exception)
   wrapping the underlying model's error. Composer catches this and falls
   back to next-best expert per routing policy; logs route_regret penalty.

3. Shape mismatch: raise ExpertOutputError(expert_id, key, expected_shape,
   actual_shape) if return dict values don't match expected shapes.
   Caught at integration test time (smoke_test.py); NOT silent.

4. Latency budget violation: NOT an error at runtime. bench_frame_budget.py
   measures and reports; the adapter itself does not self-enforce latency.
```

## Custom exceptions

```python
class CheckpointNotFoundError(FileNotFoundError):
    def __init__(self, expert_id: str, path: str):
        super().__init__(f"Expert {expert_id}: checkpoint not found at {path}")
        self.expert_id = expert_id

class ExpertForwardError(RuntimeError):
    def __init__(self, expert_id: str, cause: Exception):
        super().__init__(f"Expert {expert_id} forward failed: {cause}")
        self.expert_id = expert_id
        self.__cause__ = cause

class ExpertOutputError(ValueError):
    def __init__(self, expert_id: str, key: str, expected, actual):
        super().__init__(
            f"Expert {expert_id} output '{key}': expected {expected}, got {actual}"
        )
        self.expert_id = expert_id
```

## Expert registry (__init__.py)

```python
EXPERT_REGISTRY = {
    "mast3r":           MASt3RAdapter,
    "fast3r":           Fast3RAdapter,
    "spann3r":          Spann3RAdapter,
    "cut3r":            CUT3RAdapter,
    "moge2":            MoGe2Adapter,
    "depthanything_v2": DepthAnythingV2Adapter,
    "test3r":           Test3RAdapter,
}

def get_expert(expert_id: str) -> ExpertAdapter:
    """Get expert adapter instance. Raises KeyError if unknown expert_id."""
    cls = EXPERT_REGISTRY[expert_id]
    return cls()

def available_experts() -> list[str]:
    """Return list of expert_ids whose checkpoints are loadable."""
    available = []
    for eid, cls in EXPERT_REGISTRY.items():
        try:
            adapter = cls()
            if adapter.is_available():
                available.append(eid)
        except CheckpointNotFoundError:
            pass  # explicitly unavailable; logged at registry init
    return available
```

## Evidence labels

```text
- ExpertAdapter ABC design: engineering-judgment (follows standard
  Python ABC patterns; domain-specific return dict keys per
  COMPOSER_CAPABILITY_DESCRIPTORS).
- capability_match values: inferred (from COMPOSER_CAPABILITY_DESCRIPTORS;
  ABL-v02-5 promotes to measured).
- latency_estimate values: inferred (from paper-derived numbers in
  COMPOSER_CAPABILITY_DESCRIPTORS; bench_frame_budget.py promotes to
  measured).
- Error protocol: engineering-judgment (fail-loud pattern is standard
  practice; specific exception hierarchy is new to Dream3R).
```

## Version history

```text
v1  2026-05-07  cycle 023. Addresses RA-02 from Path C Agent A.
                Resolves Q-cs-2 from CODE_STRUCTURE. Specifies
                ExpertAdapter ABC, method signatures, return-dict
                keys, error protocol, custom exceptions, and expert
                registry pattern.
```
