# CYCLE-20260602: image-state native student U1

Date: 2026-06-02
Status: closed negative; U1 scaffold preserved but not promoted
Decision: `decisions/DEC-20260602-025-image-state-native-student-u1.md`

## Trigger

The user said the current model is still not usable and asked to move quickly.
The prior native student gate was controlled but still proposal-cache-bound, so
this pass added an image-conditioned native reconstruction path.

## Work completed

Added:

```text
code/dream3r/image_state_student_decoder.py
code/dream3r/scripts/build_image_state_student_cache.py
code/dream3r/scripts/train_image_state_student.py
code/dream3r/scripts/run_image_state_student_sweep.sh
code/dream3r/tests/test_image_state_student_decoder.py
```

## Architecture change

Old native gate:

```text
proposal pointmaps + Dream state -> frozen-StatePrior teacher residual
```

New U1 scaffold:

```text
image tokens + Dream state + optional proposal anchors -> native pointmap
```

The decoder supports:

- full proposal-anchor mode;
- proposal-dropout / partial-anchor mode;
- no-proposal mode.

## Important finding

Existing SCF caches cannot train U1 because they do not store image tokens.
The new trainer rejects those caches instead of silently pretending to be
image-conditioned. The new builder writes image tokens from frozen Perceiver
plus the existing real proposal bank.

## Verification

Local:

```text
python -B -m py_compile \
  code/dream3r/image_state_student_decoder.py \
  code/dream3r/scripts/build_image_state_student_cache.py \
  code/dream3r/scripts/train_image_state_student.py \
  code/dream3r/tests/test_image_state_student_decoder.py

python -B -m pytest \
  code/dream3r/tests/test_image_state_student_decoder.py \
  code/dream3r/tests/test_native_student_decoder.py -q
# 6 passed
```

Server:

```text
ssh BUAA-Server
cd /hdd3/kykt26/code/dream3r
conda run --no-capture-output -n dream3r \
  python -B -m pytest dream3r/tests/test_image_state_student_decoder.py -q
# 3 passed
```

## GPU gate run

```text
Kitti labels: runs/stage3_regime_labels/regime_labels.json
ETH3D labels: runs/eth3d_cross_dataset_regime_labels/regime_labels.json
```

Built image-token caches on BUAA-Server GPU1:

```text
runs/stage6_fusion/image_state_student_kitti_cache.pt
  n_windows: 246, d_memory: 128, d_image: 768

runs/stage6_fusion/image_state_student_eth3d_cache.pt
  n_windows: 50, d_memory: 128, d_image: 768
```

Then ran the bounded U1 controls:

```text
runs/stage6_fusion/image_state_student_smoke_seed7
EPOCHS=1
correct-state: KITTI 0.1642, ETH3D 0.2840

runs/stage6_fusion/image_state_student_gate20_seed7
EPOCHS=20
correct-state: KITTI 0.1649, ETH3D 0.2842
no-state:      KITTI 0.1526, ETH3D 0.1702
shuffle-state: KITTI 0.1577, ETH3D 0.2754
fallback contamination: 0
```

Locked comparison target:

```text
bounded frozen-StatePrior refinement: KITTI/ETH3D 0.1448/0.1475
```

## Verdict

U1 is not usable as-is. It has the desired non-core image-native surface, but
the gate failed on quality and controls:

```text
correct-state is worse than no-state on both KITTI and ETH3D,
and both are worse than the locked bounded baseline.
```

Do not promote U1. Do not spend the next pass on another epoch-only rerun. The
next native attempt needs an objective/architecture change, or the fallback
path should be VGGT-Omega one-window teacher admission.
