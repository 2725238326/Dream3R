# CYCLE-20260607: Foundation3R Scratch Student Diagnostic

## Summary

Foundation3R is now executable end-to-end as a proposal-free scaffold, but the current scratch decoder is not a viable quality path. The code path remains valuable because it locks the inference contract, teacher-cache schema, train/eval controls, and leak checks.

## Work Completed

- Ran BUAA-Server GPU1 20-epoch state/no-state/shuffle controls on the 50+50 real dense teacher cache.
- Added patch-coordinate injection and ray-style positive-depth output to `Foundation3RDecoder`.
- Added scale-normalized target training, train-split diagnostics, and normalized log-depth shape loss to `train_foundation3r.py`.
- Re-ran BUAA-Server GPU1 diagnostics:
  - 20e normalized-ray state/no-state/shuffle.
  - 50e state diagnostic.
  - 50e GT-only diagnostic.
  - 50e log-depth diagnostic.
  - 20e LR sweep at `1e-2` and `1e-4`.
- Pulled result JSON/checkpoints under:
  - `runs/stage6_fusion/foundation3r_train_20e_20260607/`
  - `runs/stage6_fusion/foundation3r_train_20e_normray_20260607/`
  - `runs/stage6_fusion/foundation3r_train_diag_50e_normray_20260607/`
  - `runs/stage6_fusion/foundation3r_train_diag_50e_logdepth_20260607/`
  - `runs/stage6_fusion/foundation3r_train_diag_lr_20260607/`

## Result

The scratch student does not fit the real train split closely enough:

```text
best diagnostic train split remains around KITTI 0.4620, ETH3D 0.3798
best diagnostic test split remains around KITTI 0.4734, ETH3D 0.3271
teacher reference on same holdout: KITTI 0.3554, ETH3D 0.0913
```

State/no-state/shuffle controls do not separate because the decoder is mostly a fixed geometry prior.

## Next

Implement the next Foundation3R lane as a proposal-free student with pretrained visual representation. Keep these constraints:

```text
no proposal pointmaps at inference
no expert confidences at inference
no VGGT-Omega teacher call at inference
same dense teacher cache schema
same state/no-state/shuffle controls
train/test split diagnostics required
```
