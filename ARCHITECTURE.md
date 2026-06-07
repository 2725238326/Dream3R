# Dream3R Architecture Map

Date: 2026-06-08
Status: canonical architecture entrypoint

## Current Answer

Dream3R is now organized as one official release path plus bounded side lanes.

```text
Official:     Dream3R v1.0-rc1
Metric:       AbsRel, lower is better
KITTI/ETH3D:  0.1448 / 0.1475
Usable now:   Dream3R v1.1-rc1 domain-conditional wrapper, 0.1448 / 0.0570
```

The architecture is not a single monolithic `model.py` path. The official
result is the controlled proposal-fusion path:

```text
real proposal teachers
-> cached proposal bank
-> Dream state + conflict metadata
-> frozen StatePrior
-> ProposalSetDecoder
-> disagreement-bounded residual refinement
-> final pointmap
```

Tonight usable import:

```python
from dream3r.release_v11 import build_dream3r_v11_release

model = build_dream3r_v11_release()
out = model(proposal_pointmaps, proposal_confidences, memory_context, conflict_score, domain="eth3d")
```

## Read Order

Use this order when resuming work:

```text
1. TASK_SNAPSHOT.md
2. handoff/CONTEXT_COMPACTION_20260608_V11_USABLE_MODEL.md
3. ARCHITECTURE.md                         # this file
4. release/USABLE_MODEL_V1_1.md            # usable v1.1 package
5. release/OFFICIAL_VERSION.md             # official stable version identity
6. release/ARCHITECTURE_V1_0_RC.md         # official implementation contract
7. release/ARCHITECTURE_STATUS.json        # machine-readable status map
```

## Official Path

| Layer | File | Status |
| --- | --- | --- |
| Official API | `code/dream3r/release_candidate.py` | active v1.0-rc1 import surface |
| State prior | `code/dream3r/state_prior_head.py` | active support module |
| Proposal decoder | `code/dream3r/proposal_set_decoder.py` | active metric head |
| RC trainer | `code/dream3r/scripts/train_proposal_set_decoder.py` | active reproduction path |
| Release verifier | `code/dream3r/scripts/verify_release_candidate.py` | active package gate |

Official import:

```python
from dream3r.release_candidate import build_dream3r_release_candidate

model = build_dream3r_release_candidate(checkpoint_path=None, d_memory=32)
out = model(proposal_pointmaps, proposal_confidences, memory_context, conflict_score)
```

## Experimental Path

The only currently useful optimization branch is:

```text
domain-conditional VGGT teacher
KITTI -> v1.0-rc1 bounded RC
ETH3D -> VGGT-Omega-expanded SCF correct-state
```

Current domain-wise result:

```text
KITTI: 0.1448
ETH3D: 0.0570
ETH3D gain vs RC: 61.36%
```

Unified gate:

```text
status: pass
promotable_to_official: true
artifact: runs/v22_admission/domain_conditional_teacher/unified_gate_candidate_with_kitti_no_state_server.json
```

Boundary: this is now packaged as usable `v1.1-rc1` in `release_v11.py` and
`release/USABLE_MODEL_V1_1.md`. The current official stable release identity
remains `v1.0-rc1` until `release/OFFICIAL_VERSION.md` is deliberately switched.

## Side Lanes Not In Official Path

| Lane | File(s) | Status | Rule |
| --- | --- | --- | --- |
| NativeStudent | `code/dream3r/native_student_decoder.py` | causal but flat at `0.1451 / 0.1480` | do not repeat same loss sweeps |
| ImageStateStudent | `code/dream3r/image_state_student_decoder.py` | negative | do not rerun unchanged |
| ProposalFree3R | `code/dream3r/proposal_free_3r_decoder.py`, `scripts/train_proposal_free_3r.py`, `scripts/build_proposal_free_teacher_cache.py` | proposal-free contract works; sparse-GT gate20 negative at `0.3273 / 0.4029`; stripped-teacher gate20 negative at `0.3319 / 0.4056`; larger AbsRel teacher gate negative at `0.3326 / 0.4058` | stop shallow head sweeps; use only as scaffold for stronger backbone/dense pretraining |
| Foundation3R | `code/dream3r/foundation3r_decoder.py`, `scripts/build_foundation3r_dense_teacher_cache.py`, `scripts/train_foundation3r.py` | dense-teacher cache and training chain work; scratch student negative at `0.4734 / 0.3271`; VGGT feature teacher-only 20e improves to state `0.3237 / 0.1424`, no-state `0.3260 / 0.1489`, shuffle `0.3246 / 0.1330` | use VGGT features as experimental proposal-free baseline; do not claim state causality yet |
| VGGT-Omega | `code/dream3r/scripts/stage_vggt_omega_admission.py`, `eval_vggt_omega_oracle_admission.py` | real teacher, ETH3D-positive | use only via domain-conditional gate |
| Qwen semantics | VLM semantic scripts | diagnostic-negative | not a geometry path |
| v0.4 core pipeline | `model.py`, `modules.py`, `bus.py`, `orchestrator.py`, `repair.py`, `contracts.py` | substrate | frozen for RC work |

## Frozen Core

Do not edit these files for release/optimization work unless a new decision
explicitly opens them:

```text
code/dream3r/model.py
code/dream3r/anchor_bank.py
code/dream3r/nsa_attention.py
code/dream3r/bus.py
code/dream3r/orchestrator.py
code/dream3r/repair.py
code/dream3r/modules.py
code/dream3r/contracts.py
code/dream3r/config.py
```

## Next Gate To Reduce Mess

There are now two valid architecture next tasks, depending on whether the goal
is near-term release packaging or a truly proposal-free 3R line:

```text
Release goal:
  Use the packaged v1.1-rc1 wrapper for tonight demos, or deliberately promote
  it to official stable after external packaging review.

Proposal-free goal:
  Improve the VGGT feature-student with explicit state modulation or stronger
  representation while preserving no proposal/no teacher inference.

Release promotion condition:
  1. Keep the six-control gate artifact immutable and referenced.
  2. Add a v1.1 policy/API wrapper without editing frozen core files.
  3. Update release/OFFICIAL_VERSION.md and release/ARTIFACTS.json.
  4. Re-run verifier/tests locally and on BUAA-Server GPU1 where model code is
     involved.

Proposal-free promotion condition:
  1. Use the existing 50+50 dense teacher cache schema and leak audit.
  2. Report train split and holdout split.
  3. Pass state/no-state/shuffle controls.
  4. Keep proposal_inputs_used=false and teacher_used_at_inference=false.
```

Until that packaging decision is made, the official architecture remains
`v1.0-rc1`; the passed domain-conditional policy is the current v1.1 promotion
candidate.

## Proposal-Free Route

The proposal-free route is now a real code path, not a claim:

```text
image tokens + Dream state -> pointmap
```

Gate20 result:

```text
state:         KITTI 0.3273, ETH3D 0.4029
no-state:      KITTI 0.3318, ETH3D 0.4050
shuffle-state: KITTI 0.3221, ETH3D 0.4041
```

Conclusion: the current small proposal-free decoder is not usable yet and
fails KITTI state-causality. The next proposal-free step is dense teacher
distillation / foundation pretraining, not another shallow decoder run.

Teacher distillation gate:

```text
teacher target: KITTI 0.1360, ETH3D 0.1470
state:          KITTI 0.3319, ETH3D 0.4056
no-state:       KITTI 0.3292, ETH3D 0.4049
shuffle-state:  KITTI 0.3288, ETH3D 0.4116
```

Conclusion: the distillation data path is implemented, but the current small
head does not learn the teacher target. Stop scalar teacher-weight sweeps; the
next route needs a stronger visual backbone / dense geometry pretraining.

Scale-aligned teacher AbsRel + larger decoder gate:

```text
teacher target: KITTI 0.1360, ETH3D 0.1470
state:          KITTI 0.3326, ETH3D 0.4058
no-state:       KITTI 0.3327, ETH3D 0.4080
shuffle-state:  KITTI 0.3328, ETH3D 0.4064
```

Conclusion: increasing the shallow proposal-free head and changing the teacher
loss does not close the gap. A credible proposal-free foundation-model route
must change representation/pretraining, not continue scalar/capacity sweeps.

Foundation3R plan:

```text
planning/DREAM3R_FOUNDATION3R_PROPOSAL_FREE_PLAN_20260606.md
```

Immediate next step:

```text
Sprint 0: lock proposal-free contract tests - done
Sprint 1: build VGGT-Omega dense teacher cache on BUAA-Server GPU1 - 50+50 done
Sprint 2a: train_foundation3r.py 1-epoch smoke - done
Sprint 2b: scratch student diagnostics - negative
Next: pretrained visual representation proposal-free student
```

Foundation3R scratch diagnostic:

```text
20e baseline state/no-state/shuffle: no useful separation; best ETH3D still 0.3333
20e coord/ray/scale-normalized: state/no-state/shuffle all 0.4734 / 0.3271
50e coord/ray train split: KITTI 0.4620, ETH3D 0.3798
50e coord/ray test split:  KITTI 0.4734, ETH3D 0.3271
teacher holdout:           KITTI 0.3554, ETH3D 0.0913
```
