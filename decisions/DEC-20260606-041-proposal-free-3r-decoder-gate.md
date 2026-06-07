# DEC-20260606-041: Proposal-free 3R decoder gate

Date: 2026-06-06
Status: accepted as proposal-free scaffold; gate negative for release/model claim
Scope: Dream3R proposal-free foundation-model route

## Context

The user asked to move toward a fully proposal-free independent 3R model. The
current official and v1.1-candidate paths still depend on proposal teachers at
inference time:

```text
v1.0-rc1: proposal bank -> StatePrior -> ProposalSetDecoder
v1.1 candidate: KITTI v1.0-rc1 + ETH3D VGGT-Omega proposal path
```

Those are useful controlled systems, but they are not a proposal-free 3R
foundation model.

## Decision

Add a clean non-core proposal-free decoder and trainer:

```text
image tokens + Dream state -> pointmap
```

The forward contract deliberately has no proposal pointmap or expert-confidence
inputs. Existing teacher/proposal artifacts may be used for offline cache
construction or future distillation targets, but not as inference inputs.

## Implementation

Added:

```text
code/dream3r/proposal_free_3r_decoder.py
code/dream3r/scripts/train_proposal_free_3r.py
code/dream3r/tests/test_proposal_free_3r_decoder.py
```

The test suite includes a poisoned-proposal smoke test: cache entries contain
invalid proposal objects, and training still succeeds, proving the trainer does
not read proposal tensors.

## Gate20 Result

BUAA-Server GPU1, image-state caches:

```text
runs/stage6_fusion/proposal_free_3r_gate20_20260606/state_seed_7/results.json
runs/stage6_fusion/proposal_free_3r_gate20_20260606/no_state_seed_7/results.json
runs/stage6_fusion/proposal_free_3r_gate20_20260606/shuffle_state_seed_7/results.json
```

Metrics:

```text
state:        KITTI 0.3273, ETH3D 0.4029
no-state:     KITTI 0.3318, ETH3D 0.4050
shuffle-state: KITTI 0.3221, ETH3D 0.4041
```

## Verdict

The proposal-free inference contract is now real, but the current small decoder
is not a usable model:

```text
release_promotable: false
state_causality: failed on KITTI because shuffle beats correct state
quality: far worse than v1.0-rc1 0.1448 / 0.1475
```

This proves the next proposal-free step cannot be another small head trained
only on sparse GT. It needs foundation-style pretraining/distillation: stronger
visual backbone/features, dense teacher targets, multi-view/self-supervised
geometry losses, and a longer training schedule.

## Next Route

Do not promote this v0 scaffold. Use it as the inference contract for the next
proposal-free foundation route:

```text
1. Build dense teacher-target caches, preferably VGGT-Omega/RC domain-policy targets.
2. Train ProposalFree3RDecoder with teacher distillation plus sparse GT.
3. Run state/no-state/shuffle and teacher/no-teacher ablations.
4. Only compare to v1.0/v1.1 after proposal-free inference beats controls.
```
