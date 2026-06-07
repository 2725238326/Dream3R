# Cycle 20260607: Foundation3R Training Smoke

Date: 2026-06-07
Status: closed training-entry-smoke-positive
Decision: `decisions/DEC-20260607-046-foundation3r-train-smoke.md`

## Goal

Prove that Foundation3R can train from the verified 50+50 dense teacher cache
without proposal or inference-teacher leakage.

## Action

Added:

```text
code/dream3r/scripts/train_foundation3r.py
code/dream3r/tests/test_foundation3r_training.py
```

Synced to BUAA-Server and ran a 1-epoch GPU1 smoke on:

```text
runs/stage6_fusion/foundation3r_dense_teacher_50x2_20260607/kitti_dense_teacher_cache.pt
runs/stage6_fusion/foundation3r_dense_teacher_50x2_20260607/eth3d_dense_teacher_cache.pt
```

## Result

```text
local targeted tests: 13 passed
server Foundation3R tests: 5 passed
server 1-epoch smoke: pass
proposal_inputs_used=false
teacher_used_at_inference=false
```

Smoke eval:

```text
KITTI Ours_Foundation3R: 0.4718
KITTI Teacher_Dense:     0.3554
ETH3D Ours_Foundation3R: 0.3269
ETH3D Teacher_Dense:     0.0913
```

## Verdict

Training-entry smoke is positive. Model quality is not yet claimable. The next
gate is 20-epoch state/no-state/shuffle-state control on the same 50+50 cache.
