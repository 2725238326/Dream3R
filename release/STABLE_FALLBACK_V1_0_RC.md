# Dream3R v1.0-rc1 Stable Fallback

Date: 2026-06-08
Status: stable fallback package; superseded by official v1.1.0

## Identity

```text
name: Dream3R
version: v1.0-rc1
release candidate: frozen_state_prior_bounded_residual
metric: AbsRel, lower is better
KITTI / ETH3D: 0.1448 / 0.1475
```

This package is retained for reproducibility and rollback. It is not the
current official Dream3R release.

## Fallback Architecture

```text
real proposal teachers
-> cached proposal bank
-> Dream state and conflict metadata
-> frozen StatePrior
-> bounded convex proposal fusion
-> disagreement-bounded residual refinement
```

Fallback import:

```python
from dream3r.release_candidate import build_dream3r_release_candidate

model = build_dream3r_release_candidate(checkpoint_path=None, d_memory=32)
out = model(proposal_pointmaps, proposal_confidences, memory_context, conflict_score)
```

## Verification

```powershell
python -B code\dream3r\scripts\verify_release_candidate.py --root .
```

Expected:

```text
status: pass
version: v1.0-rc1
```

## Current Official Release

The current official release is:

```text
Dream3R v1.1.0
doc: release/OFFICIAL_VERSION.md
api: dream3r.release_v11.build_dream3r_v11_release
KITTI / ETH3D: 0.1448 / 0.0570
```
