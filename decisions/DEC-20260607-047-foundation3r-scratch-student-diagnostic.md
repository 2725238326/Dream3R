# DEC-20260607-047: Foundation3R Scratch Student Diagnostic

Status: accepted

## Decision

Stop scaling the current scratch `Foundation3RDecoder` as the proposal-free quality route. Keep the code path as a contract-locked training scaffold, but the next Foundation3R implementation must use a stronger pretrained visual representation while preserving the inference contract:

```text
RGB/images + optional Dream state -> pointmap/confidence
forbidden at inference: proposal pointmaps, expert confidences, teacher model calls
```

VGGT-Omega remains an offline dense teacher/cache source for this line, not an inference-time geometry module.

## Evidence

BUAA-Server GPU1 used the real 50+50 KITTI/ETH3D dense teacher caches from `runs/stage6_fusion/foundation3r_dense_teacher_50x2_20260607/`.

Baseline 20-epoch scratch student:

```text
state:         KITTI 0.4778, ETH3D 0.3422
no-state:      KITTI 0.4818, ETH3D 0.3388
shuffle-state: KITTI 0.4872, ETH3D 0.3333
teacher:       KITTI 0.3554, ETH3D 0.0913
```

After adding patch coordinates, ray-style positive depth, target scale normalization, train-split diagnostics, and log-depth shape loss:

```text
20e state/no-state/shuffle all converge to KITTI 0.4734, ETH3D 0.3271
50e state train split: KITTI 0.4620, ETH3D 0.3798
50e state test split:  KITTI 0.4734, ETH3D 0.3271
GT-only 50e: same train/test metric pattern
LR 1e-2 / 1e-4 20e: same final metric pattern
```

This is a fit failure on real data, not merely a state-causality or holdout-generalization failure.

## Implemented

- `code/dream3r/foundation3r_decoder.py`
  - Added patch coordinate injection.
  - Constrained output to normalized ray-like `(x, y, positive depth)` pointmaps.
- `code/dream3r/scripts/train_foundation3r.py`
  - Added target scale normalization.
  - Added train-split evaluation output.
  - Added normalized log-depth shape loss.
  - Keeps proposal/teacher inference flags false.
- `code/dream3r/tests/test_foundation3r_contract.py`
  - Locks positive depth and patch-coordinate behavior.
- `code/dream3r/tests/test_foundation3r_training.py`
  - Locks scale normalization, log-depth loss, train diagnostics, and no-proposal contract.

## Verification

```text
local targeted pytest: 8 passed
local py_compile: pass
BUAA-Server targeted training tests: 4 passed
BUAA-Server GPU1 diagnostics: completed
frozen core files: unchanged
```

## Consequence

Do not spend more time on unchanged scratch CNN/Transformer sweeps. The next useful implementation is a proposal-free student with pretrained visual features and the same leak controls, evaluated against the same state/no-state/shuffle gates.
