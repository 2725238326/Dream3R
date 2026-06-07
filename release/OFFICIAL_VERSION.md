# Dream3R v1.0-rc1 Official Version

Date: 2026-06-06
Status: official release-candidate package

## Version Identity

```text
name: Dream3R
version: v1.0-rc1
release candidate: frozen_state_prior_bounded_residual
metric: AbsRel, lower is better
KITTI / ETH3D: 0.1448 / 0.1475
```

This is the formal versioned package for the current architecture. It is not
the ideal proposal-free Dream3R model; it is the strongest controlled,
state-causal implementation currently available.

## What Is Official In v1.0-rc1

The official path is:

```text
real proposal teachers
-> cached proposal bank
-> Dream state and conflict metadata
-> frozen StatePrior
-> bounded convex proposal fusion
-> disagreement-bounded residual refinement
```

The official import surface is:

```python
from dream3r.release_candidate import build_dream3r_release_candidate

model = build_dream3r_release_candidate(checkpoint_path=None, d_memory=32)
out = model(proposal_pointmaps, proposal_confidences, memory_context, conflict_score)
```

The supported claim is narrow:

```text
Dream3R v1.0-rc1 is a controlled state-conditioned proposal-fusion release
candidate that improves over the best single proposal expert and preserves
state-causality against shuffled-state controls on the selected KITTI/ETH3D
gate.
```

## What Is Not Official

The following are implemented or staged but not part of the official model
path:

| Lane | Status | Reason |
| --- | --- | --- |
| NativeStudentDecoder | implemented; causal but flat | `0.1451 / 0.1480`, does not beat RC |
| ImageStateStudentDecoder | implemented; negative | loses to controls and baseline |
| VGGT-Omega | real backend admitted | raw 4-expert KITTI release controls fail |
| domain-conditional VGGT policy | unified gate passed; v1.1 promotion candidate | not packaged as the official version yet |
| Qwen semantic controller | schema/runtime implemented | diagnostic-negative for routing/Critic gates |
| v0.4 typed pipeline | implemented substrate | not the selected metric path |

## v1.1 Promotion Candidate

The passed promotion-candidate policy is:

```text
KITTI -> Dream3R v1.0-rc1 bounded StatePrior + residual
ETH3D -> VGGT-Omega-expanded SCF correct-state
```

Unified gate result:

```text
artifact: runs/v22_admission/domain_conditional_teacher/unified_gate_candidate_with_kitti_no_state_server.json
KITTI state/no-state/shuffle: 0.1448 / 0.1553 / 0.1521
ETH3D state/no-state/shuffle: 0.0570 / 0.0583 / 0.0598
status: pass
promotable_to_official: true
```

This is not silently promoted in this file. A v1.1 package needs its own
version switch, artifact manifest update, verifier update, and reproducibility
notes.

## Required Verification

Local package verification:

```powershell
cd E:\Dream3R
python -B code\dream3r\scripts\verify_release_candidate.py
```

Expected:

```text
"status": "pass"
"version": "v1.0-rc1"
```

Targeted tests:

```powershell
python -B -m pytest --assert=plain code/dream3r/tests/test_release_candidate_verifier.py -q
python -B -m pytest --assert=plain code/dream3r/tests/test_release_candidate_architecture.py -q
python -B -m pytest --assert=plain code/dream3r/tests/test_native_student_decoder.py -q
```

## Entry Points

Read in this order:

```text
ARCHITECTURE.md
release/OFFICIAL_VERSION.md
release/ARCHITECTURE_V1_0_RC.md
release/ARCHITECTURE_STATUS.json
release/DREAM3R_RC_CARD.md
release/REPRODUCE.md
release/VERIFY_REPORT.md
release/LIMITATIONS.md
release/NON_CLAIMS.md
```

The version exists to stabilize the architecture surface. Future model
improvement should branch from this version and must pass the same
state/no-state/shuffle control discipline before replacing it.
