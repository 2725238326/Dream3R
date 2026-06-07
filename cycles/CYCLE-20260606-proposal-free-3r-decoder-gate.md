# Cycle 20260606: Proposal-Free 3R Decoder Gate

Date: 2026-06-06
Status: closed scaffold-positive, metric/control-negative
Decision: `decisions/DEC-20260606-041-proposal-free-3r-decoder-gate.md`

## Goal

Start the fully proposal-free Dream3R route requested by the user.

## Action

Added:

```text
code/dream3r/proposal_free_3r_decoder.py
code/dream3r/scripts/train_proposal_free_3r.py
code/dream3r/tests/test_proposal_free_3r_decoder.py
```

The decoder contract is:

```text
image tokens + Dream state -> pointmap
```

No proposal pointmaps or expert confidences are accepted by `forward()`.

## Verification

Local:

```text
test_proposal_free_3r_decoder.py: 3 passed
proposal-free + release-architecture targeted tests: 7 passed
```

BUAA-Server:

```text
test_proposal_free_3r_decoder.py: 3 passed
```

Server GPU1 training smoke:

```text
runs/stage6_fusion/proposal_free_3r_train_smoke_20260606/state_seed_7
1 epoch: KITTI 0.3219, ETH3D 0.4250
```

Server GPU1 gate20:

```text
state:         KITTI 0.3273, ETH3D 0.4029
no-state:      KITTI 0.3318, ETH3D 0.4050
shuffle-state: KITTI 0.3221, ETH3D 0.4041
```

## Verdict

The proposal-free path is now executable, but it is not usable as a model yet.
It is far worse than v1.0-rc1 and fails state-causality on KITTI because
shuffle-state is better than correct-state.

## Next

The next proposal-free step must be dense teacher distillation / foundation
pretraining, not another shallow decoder run on sparse GT.
