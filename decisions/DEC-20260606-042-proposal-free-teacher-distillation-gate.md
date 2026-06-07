# DEC-20260606-042: Proposal-free teacher distillation gate

Date: 2026-06-06
Status: accepted as implemented gate; model result negative
Scope: Dream3R proposal-free foundation-model route

## Context

DEC-041 made the proposal-free inference contract real:

```text
image tokens + Dream state -> pointmap
```

Gate20 without teacher distillation was far below the release path and failed
KITTI state-causality. The next low-risk step was to let proposal teachers act
only as offline distillation targets, not inference inputs.

## Decision

Add a stripped proposal-free teacher cache builder and train the proposal-free
decoder with optional teacher loss.

The cache builder may read proposal tensors offline, but the saved training
cache strips proposal fields by default and keeps only:

```text
image_tokens
memory_context
conflict_score
gt_pointmap / gt_mask
teacher_pointmap
```

## Implementation

Added:

```text
code/dream3r/scripts/build_proposal_free_teacher_cache.py
```

Updated:

```text
code/dream3r/scripts/train_proposal_free_3r.py
code/dream3r/tests/test_proposal_free_3r_decoder.py
```

The tests verify that the built teacher cache strips `proposals` and that the
trainer still reports `proposal_inputs_used=false`.

## Server Gate

BUAA-Server teacher cache:

```text
runs/stage6_fusion/proposal_free_teacher_cache/best_single_teacher_cache.pt
teacher_policy: best_single
proposal_fields_stripped: true
```

BUAA-Server GPU1 gate20, `teacher_weight=1.0`:

```text
state:         KITTI 0.3319, ETH3D 0.4056
no-state:      KITTI 0.3292, ETH3D 0.4049
shuffle-state: KITTI 0.3288, ETH3D 0.4116
offline teacher target: KITTI 0.1360, ETH3D 0.1470
```

Artifacts:

```text
runs/stage6_fusion/proposal_free_3r_teacher_gate20_20260606/state_seed_7/results.json
runs/stage6_fusion/proposal_free_3r_teacher_gate20_20260606/no_state_seed_7/results.json
runs/stage6_fusion/proposal_free_3r_teacher_gate20_20260606/shuffle_state_seed_7/results.json
```

## Verdict

The teacher-distillation mechanism is implemented correctly, but the current
small proposal-free decoder does not learn the teacher target:

```text
release_promotable: false
state_causality: failed because state does not beat no-state on either domain
quality: far worse than v1.0-rc1 and far from the offline teacher target
```

Do not repeat this shallow teacher-weight sweep. The next proposal-free route
needs a stronger visual backbone / dense geometry pretraining / longer training
surface, not more scalar loss tuning on the same small head.
