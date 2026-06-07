# Dream3R v1.1.0 Effective Architecture

Date: 2026-06-08
Status: current effective architecture version

## Identity

```text
name: Dream3R
effective version: v1.1.0
candidate: domain_conditional_vggt_teacher
metric: AbsRel, lower is better
KITTI / ETH3D: 0.1448 / 0.0570
stable fallback: v1.0-rc1 frozen_state_prior_bounded_residual
```

This is the most reasonable effective Dream3R architecture today. It keeps the
state-conditioned proposal-fusion line that passed controls and adds the only
currently useful VGGT-Omega branch through a domain-conditional policy.

It is not a proposal-free foundation model.

## Architecture

```text
input images
-> real 3R proposal teachers
-> cached proposal bank + confidences
-> Dream state / memory context + conflict metadata
-> domain policy
   -> KITTI: v1.0 bounded StatePrior + ProposalSetDecoder + residual refinement
   -> ETH3D: VGGT-Omega-expanded SCF correct-state branch
-> final pointmap + confidence
```

The current import surface is:

```python
from dream3r.release_v11 import build_dream3r_v11_release

model = build_dream3r_v11_release()
out = model(
    proposal_pointmaps,
    proposal_confidences,
    memory_context,
    conflict_score,
    domain="eth3d",
)
```

## Why This Is The Effective Version

v1.1 is selected because it is the strongest branch with both metric value and
state-causality controls:

```text
KITTI state/no-state/shuffle: 0.1448 / 0.1553 / 0.1521
ETH3D state/no-state/shuffle: 0.0570 / 0.0583 / 0.0598
```

The correct-state branch beats no-state and shuffle-state on both domains.

v1.0 remains important because it is the conservative stable fallback:

```text
v1.0-rc1 KITTI / ETH3D: 0.1448 / 0.1475
```

## Module Roles

| Lane | Modules | Status |
| --- | --- | --- |
| Effective release | `release_v11.py`, `release_candidate.py`, `state_prior_head.py`, `proposal_set_decoder.py`, `scf_head.py` | active |
| Teacher/proposal infrastructure | `composer_experts/*`, VGGT-Omega admission/eval scripts, SCF cache scripts | active support |
| Proposal-free research | `proposal_free_3r_decoder.py`, `foundation3r_decoder.py`, Foundation3R cache/train scripts | research only |
| Semantic diagnostics | Qwen/VLM semantic label and controller scripts | diagnostic only |
| Frozen substrate | `model.py`, `bus.py`, `orchestrator.py`, `modules.py`, `contracts.py`, related core files | frozen |

## Boundaries

Safe claims:

```text
Dream3R v1.1.0 is a state-conditioned proposal-fusion 3R architecture with a
domain-conditional VGGT-Omega ETH3D branch and verified state/no-state/shuffle
controls.
```

Do not claim:

```text
Dream3R is already a proposal-free independent 3R foundation model.
Qwen improves geometry.
Foundation3R is promotable.
VGGT-Omega alone is Dream3R.
```

## Verification

```powershell
cd E:\Dream3R
python -B code\dream3r\scripts\verify_v11_release.py --root .
python -B -m pytest --assert=plain code\dream3r\tests\test_release_v11_architecture.py code\dream3r\tests\test_release_v11_verifier.py -q
```

Expected verifier identity:

```text
status: pass
version: v1.1.0
candidate: domain_conditional_vggt_teacher
```

## Next Architecture Work

Only two next directions are valid:

1. Package and present v1.1 as the current effective proposal-fusion model.
2. Redesign proposal-free Foundation3R by changing target, data scale, or
   architecture, then re-run state/no-state/shuffle controls.

Do not add another named module unless it retires or supersedes an existing
negative lane with a clear gate.
