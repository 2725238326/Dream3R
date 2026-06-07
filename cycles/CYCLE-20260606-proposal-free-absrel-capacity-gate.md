# Cycle 20260606: Proposal-Free AbsRel Capacity Gate

Date: 2026-06-06
Status: closed implemented-negative
Decision: `decisions/DEC-20260606-043-proposal-free-absrel-capacity-gate.md`

## Goal

Test whether scale-aligned teacher AbsRel distillation plus a larger
proposal-free decoder can close the gap to the stripped offline teacher target.

## Action

Updated:

```text
code/dream3r/scripts/train_proposal_free_3r.py
code/dream3r/tests/test_proposal_free_3r_decoder.py
```

Added trainer support for:

```text
teacher_absrel_weight
model_dim / state_dim / hidden / num_layers / num_heads
```

Ran BUAA-Server GPU1 gate20 with `teacher_absrel_weight=1.0`,
`model_dim=256`, `state_dim=128`, `hidden=512`, `num_layers=4`,
and `num_heads=8`.

## Result

```text
state:         KITTI 0.3326, ETH3D 0.4058
no-state:      KITTI 0.3327, ETH3D 0.4080
shuffle-state: KITTI 0.3328, ETH3D 0.4064
teacher target: KITTI 0.1360, ETH3D 0.1470
```

## Verdict

Negative. The proposal-free decoder remains far from the teacher target, and
true state is effectively indistinguishable from no-state and shuffle-state
controls.

Do not continue scalar/capacity sweeps on this shallow head. The next
proposal-free route must change the representation and training surface:
stronger visual backbone, dense teacher targets, and foundation-style
pretraining before claiming an independent 3R model.
