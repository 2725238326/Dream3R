# DEC-20260607-046: Foundation3R training smoke

Date: 2026-06-07
Status: accepted as training-entry smoke positive
Scope: Dream3R proposal-free Foundation3R line

## Context

DEC-045 produced a verified `50+50` real VGGT-Omega dense teacher cache for
Foundation3R. The next gate was to prove the training entrypoint can consume
that cache without proposal leakage before running longer state-causality
controls.

## Decision

Add `train_foundation3r.py` and run a 1-epoch BUAA-Server GPU1 smoke.

The trainer must keep the same Foundation3R inference contract:

```text
proposal_inputs_used=false
teacher_used_at_inference=false
```

It supports:

```text
teacher dense pointmap loss
GT AbsRel loss when GT exists
state / no-state / shuffle-state controls
image loading from cache frame paths
test-time image tensor entries for unit tests
```

## Implementation

Added:

```text
code/dream3r/scripts/train_foundation3r.py
code/dream3r/tests/test_foundation3r_training.py
```

The cache loader rejects forbidden proposal fields:

```text
proposals
proposal_pointmaps
proposal_confidences
expert_confidences
expert_order
teacher_model
```

## Verification

Local:

```text
test_foundation3r_contract.py
test_foundation3r_training.py
test_proposal_free_3r_decoder.py
test_release_candidate_architecture.py
result: 13 passed
```

Server:

```text
test_foundation3r_contract.py
test_foundation3r_training.py
result: 5 passed
```

BUAA-Server GPU1 1-epoch smoke:

```text
cache: foundation3r_dense_teacher_50x2_20260607 KITTI + ETH3D
output: runs/stage6_fusion/foundation3r_train_smoke_20260607/state_seed_7
train/test: 80 / 20
proposal_inputs_used: false
teacher_used_at_inference: false
```

Smoke metrics:

```text
KITTI Ours_Foundation3R: 0.4718
KITTI Teacher_Dense:     0.3554
ETH3D Ours_Foundation3R: 0.3269
ETH3D Teacher_Dense:     0.0913
```

## Verdict

Training entrypoint smoke is positive. This is not a quality result and is not
promotable. It proves that Foundation3R can train from the verified dense cache
without proposal or inference-teacher inputs.

## Next

Run the actual small gate:

```text
20-epoch state
20-epoch no-state
20-epoch shuffle-state
same 50+50 cache
same proposal leak controls
```

Promotion from this stage requires true state to beat no-state and
shuffle-state, plus a large improvement over the previous shallow
proposal-free `0.33 / 0.40` failure line.
