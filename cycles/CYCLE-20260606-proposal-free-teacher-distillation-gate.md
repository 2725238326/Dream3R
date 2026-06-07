# Cycle 20260606: Proposal-Free Teacher Distillation Gate

Date: 2026-06-06
Status: closed implemented-negative
Decision: `decisions/DEC-20260606-042-proposal-free-teacher-distillation-gate.md`

## Goal

Continue the proposal-free route by using proposal teachers only as offline
training targets, not as inference inputs.

## Action

Added:

```text
code/dream3r/scripts/build_proposal_free_teacher_cache.py
```

Updated:

```text
code/dream3r/scripts/train_proposal_free_3r.py
code/dream3r/tests/test_proposal_free_3r_decoder.py
```

Built a stripped teacher cache on BUAA-Server:

```text
runs/stage6_fusion/proposal_free_teacher_cache/best_single_teacher_cache.pt
proposal_fields_stripped: true
```

## Result

GPU1 gate20 with `teacher_weight=1.0`:

```text
state:         KITTI 0.3319, ETH3D 0.4056
no-state:      KITTI 0.3292, ETH3D 0.4049
shuffle-state: KITTI 0.3288, ETH3D 0.4116
teacher target: KITTI 0.1360, ETH3D 0.1470
```

## Verdict

The distillation data path is correct, but the model result is negative. The
decoder does not approach the teacher target and state does not beat no-state.

Next proposal-free work should widen the actual model/pretraining surface
instead of repeating shallow teacher-weight sweeps.
