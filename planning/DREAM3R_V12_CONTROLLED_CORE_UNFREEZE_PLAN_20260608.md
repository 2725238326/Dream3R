# Dream3R v1.2 Controlled Core Unfreeze Plan - 2026-06-08

## Purpose

The v1.1 official release is usable, but the architecture is too wrapper-heavy:
the official proposal-fusion model lives mostly outside the historical
`Dream3R` core. This plan opens a controlled v1.2 experimental lane that
touches core files for a real architecture repair while preserving v1.1 as the
official fallback.

## Current Change

Implemented first core bridge:

```text
Perceiver -> Permanence -> SpatialMemory -> Composer -> Critic
                                    |
                                    v
                   pooled Dream latent state + Critic conflict
                                    |
                                    v
            ProposalSetDecoder over cached proposal bank
                                    |
                                    v
                         final pointmap/confidence
```

New experimental API:

```python
from dream3r.release_v12_experimental import build_dream3r_v12_experimental

model = build_dream3r_v12_experimental()
out = model(x, proposal_pointmaps, proposal_confidences)
```

## Files Opened

These files are no longer treated as byte-frozen for the v1.2 experimental
lane:

```text
code/dream3r/model.py
code/dream3r/modules.py
code/dream3r/config.py
```

The official v1.1 API remains:

```python
from dream3r.release_v11 import build_dream3r_v11_release
```

## What Changed

```text
code/dream3r/model.py
  Adds optional enable_proposal_fusion_bridge.
  Dream3R.forward can now accept proposal_pointmaps/proposal_confidences.
  Core Memory/Critic state is pooled and fed into ProposalSetDecoder.
  Outputs final_pointmap/final_confidence/expert_weights when bridge is active.

code/dream3r/modules.py
  Makes SpatialMemory frame_input_dim configurable instead of hard-coded 768.
  This removes a real core rigidity and allows small-core experiments.

code/dream3r/config.py
  Threads v1.2 bridge knobs through config_to_model_args.

code/dream3r/release_v12_experimental.py
  Adds v1.2-exp0 builder and metadata.

code/dream3r/tests/test_release_v12_experimental_architecture.py
  Locks bridge shape contract, fallback boundary, and half-input rejection.
```

## Promotion Gate

`v1.2-exp0` is not official. Promotion requires all of:

```text
1. KITTI AbsRel beats v1.1.0 / v1.0 fallback 0.1448.
2. ETH3D AbsRel beats v1.1.0 0.0570 or provides a justified broader-domain gain.
3. correct-state beats no-state and shuffle-state controls.
4. v1.1 official API remains callable and regression tests pass.
5. no proposal-free claim unless proposal inputs are absent at inference.
```

## Immediate Next Work

```text
1. Sync v1.2-exp0 to BUAA-Server.
2. Run architecture tests on GPU1.
3. Add a cache-mode training/eval script that feeds real SCF/VGGT proposal
   caches into the core bridge.
4. Run state/no-state/shuffle gate against v1.1 metrics.
5. Promote only if the metrics and controls pass.
```

## Validation Evidence

```text
local:
  v1.2 architecture tests: 4 passed
  v1.1/v1.0 release architecture tests: 9 passed
  spatial/core tests: 20 passed
  manifest JSON parse: pass
  import smoke: v1.2-exp0 and v1.1.0

BUAA-Server GPU1:
  v1.2 architecture tests: 4 passed
  v1.1/v1.0 release architecture tests: 9 passed
  manifest JSON parse: pass
  import smoke: v1.2-exp0 and v1.1.0
```
