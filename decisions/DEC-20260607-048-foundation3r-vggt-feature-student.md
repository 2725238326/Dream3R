# DEC-20260607-048: Foundation3R VGGT Feature Student

Status: accepted as experimental-positive, not official

## Decision

Use VGGT-Omega aggregator patch tokens as the next Foundation3R pretrained visual representation lane. This keeps the proposal-free inference contract:

```text
VGGT backbone features + optional Dream state -> pointmap/confidence
forbidden at inference: proposal pointmaps, expert confidences, teacher model calls
```

Do not train this lane with the previous hybrid `teacher + GT AbsRel + log-depth` objective by default. In `input_mode=vggt_features`, the trainer now resolves `loss_profile=auto` to `teacher_only` (`teacher_weight=1.0`, `gt_weight=0.0`, `depth_weight=0.0`) unless weights are explicitly overridden.

## Evidence

Real VGGT-Omega features were extracted on BUAA-Server GPU1 from:

```text
/hdd3/kykt26/externals/vggt-omega
/hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt
```

50+50 feature cache:

```text
runs/stage6_fusion/foundation3r_vggt_feature_50x2_20260607/kitti_feature_cache.pt
runs/stage6_fusion/foundation3r_vggt_feature_50x2_20260607/eth3d_feature_cache.pt
```

Both caches contain 50 windows, failures 0, fallback contamination 0, `vggt_patch_features` shape `[4,196,128]`, GT/state present, and proposal fields stripped.

Bad hybrid objective diagnostic:

```text
state/no-state/shuffle 20e all collapse to about KITTI 0.4734 / ETH3D 0.3271
```

Teacher-only 20e VGGT feature student:

```text
state:         KITTI 0.3237, ETH3D 0.1424
no-state:      KITTI 0.3260, ETH3D 0.1489
shuffle-state: KITTI 0.3246, ETH3D 0.1330
dense teacher: KITTI 0.3554, ETH3D 0.0913
```

Interpretation:

```text
VGGT features are useful versus scratch student.
Dream state is not yet causally useful in this feature-student setup.
The lane is not promotable over official v1.0-rc1 or v1.1 domain-conditional VGGT.
```

## Implemented

- `code/dream3r/foundation3r_decoder.py`
  - Added `Foundation3RVGGTFeatureDecoder`.
  - Uses VGGT patch features, patch coordinates, optional Dream state, and proposal-free output flags.
  - Emits z-only pointmaps to match the current dense teacher cache target.
- `code/dream3r/scripts/build_foundation3r_dense_teacher_cache.py`
  - Added optional `--include-vggt-features`.
  - Extracts VGGT-Omega aggregator final patch tokens and stores compact `[N,P,128]` features.
- `code/dream3r/scripts/train_foundation3r.py`
  - Added `--input-mode vggt_features`.
  - Added `loss_profile=auto|hybrid|teacher_only`.
  - Defaults VGGT feature training to teacher-only while preserving explicit weight overrides.
- Tests now lock feature-cache fields, proposal-free VGGT feature forward behavior, and the auto loss-profile contract.

## Verification

```text
local targeted pytest: 11 passed
local py_compile: pass
BUAA-Server targeted pytest: 11 passed
BUAA-Server GPU1 real feature-cache smoke: pass
BUAA-Server GPU1 50+50 feature cache: pass
BUAA-Server GPU1 teacher-only 20e state/no-state/shuffle gate: complete
BUAA-Server auto-profile smoke: loss_profile=teacher_only, gt_weight=0.0, depth_weight=0.0
frozen core files: unchanged
```

## Consequence

The next Foundation3R step is not another scratch or hybrid-loss sweep. The shortest useful path is:

```text
1. Keep VGGT feature student as proposal-free experimental baseline.
2. Improve state causality with an explicit state adapter or domain/state-conditioned modulation.
3. Compare against v1.0-rc1 and v1.1 domain-conditional policy before any promotion claim.
```

