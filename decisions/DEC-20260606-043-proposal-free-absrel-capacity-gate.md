# DEC-20260606-043: Proposal-free abs-rel capacity gate

Date: 2026-06-06
Status: accepted as implemented gate; model result negative
Scope: Dream3R proposal-free foundation-model route

## Context

DEC-042 showed that stripped teacher distillation was wired correctly, but the
small proposal-free decoder did not approach the offline teacher target. The
remaining low-risk hypothesis was that the loss shape and decoder capacity were
too weak.

## Decision

Extend the proposal-free trainer with:

```text
teacher_absrel_weight
model_dim / state_dim / hidden / num_layers / num_heads
```

Then run a larger decoder with scale-aligned teacher AbsRel loss on BUAA-Server
GPU1. This keeps the inference contract proposal-free:

```text
image tokens + Dream state -> pointmap
proposal_inputs_used=false
```

## Implementation

Updated:

```text
code/dream3r/scripts/train_proposal_free_3r.py
code/dream3r/tests/test_proposal_free_3r_decoder.py
```

The trainer now supports teacher AbsRel distillation and explicit decoder
capacity settings. Tests verify that these options are recorded while proposal
inputs remain unused.

## Server Gate

BUAA-Server GPU1 gate20:

```text
cache: runs/stage6_fusion/proposal_free_teacher_cache/best_single_teacher_cache.pt
teacher_absrel_weight: 1.0
model_dim: 256
state_dim: 128
hidden: 512
num_layers: 4
num_heads: 8
```

Results:

```text
state:         KITTI 0.3326, ETH3D 0.4058
no-state:      KITTI 0.3327, ETH3D 0.4080
shuffle-state: KITTI 0.3328, ETH3D 0.4064
offline teacher target: KITTI 0.1360, ETH3D 0.1470
```

Artifacts:

```text
runs/stage6_fusion/proposal_free_3r_absrel_gate20_20260606/state_seed_7/results.json
runs/stage6_fusion/proposal_free_3r_absrel_gate20_20260606/no_state_seed_7/results.json
runs/stage6_fusion/proposal_free_3r_absrel_gate20_20260606/shuffle_state_seed_7/results.json
```

## Verdict

The larger decoder and scale-aligned teacher loss do not improve the
proposal-free path:

```text
release_promotable: false
state_causality: failed because true state is indistinguishable from controls
quality: far worse than v1.0-rc1 and far from the offline teacher target
```

Stop this family of shallow proposal-free head experiments. A credible
proposal-free Dream3R now requires a stronger visual geometry backbone and
dense geometry pretraining/teacher targets, not more scalar loss or capacity
sweeps on the current head.
