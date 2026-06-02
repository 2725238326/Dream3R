# DEC-20260602-025: Image-state native student U1

Date: 2026-06-02
Status: closed negative on U1 gate20; scaffold preserved, not promoted
Scope: Dream3R usable-model U1 architecture

## Context

DEC-024 made native student decoding executable, but it still consumed only
proposal caches and stayed metric-flat versus the frozen StatePrior teacher.
That is not yet a usable Dream3R model. A usable first target needs an
image-conditioned native path so inference is not permanently equivalent to a
three-teacher fusion system.

## Decision

Add a non-core U1 decoder:

```text
images -> frozen Perceiver image tokens
image tokens + Dream state + optional proposal anchors -> native pointmap
```

The new model has three inference modes:

```text
full-anchor:      image + state + all proposal anchors
partial-anchor:   image + state + proposal dropout / one-teacher-only training
no-proposal:      image + state only
```

## Files

```text
code/dream3r/image_state_student_decoder.py
code/dream3r/scripts/build_image_state_student_cache.py
code/dream3r/scripts/train_image_state_student.py
code/dream3r/scripts/run_image_state_student_sweep.sh
code/dream3r/tests/test_image_state_student_decoder.py
```

## Boundaries

- No frozen-core edits.
- Existing SCF caches are rejected for U1 training because they do not contain
  image tokens.
- Cache build must use real-backend guardrail for Fast3R / MASt3R / Spann3R.
- No checkpoint download or environment mutation.
- Do not claim U1 quality until image-token cache build and state/no-state/
  shuffle training controls complete.

## Verification completed

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

## GPU gate executed

Image-token caches were built on BUAA-Server GPU1 with the existing
real-backend guardrail:

```text
runs/stage6_fusion/image_state_student_kitti_cache.pt
  n_windows: 246, d_memory: 128, d_image: 768

runs/stage6_fusion/image_state_student_eth3d_cache.pt
  n_windows: 50, d_memory: 128, d_image: 768

experts: fast3r, mast3r, spann3r
fallback contamination: 0
```

The bounded U1 sweep then ran:

```text
CUDA_VISIBLE_DEVICES=1 conda run --no-capture-output -n dream3r \
  python -m dream3r.scripts.build_image_state_student_cache \
    --dataset kitti_long \
    --regime-labels runs/stage3_regime_labels/regime_labels.json \
    --output runs/stage6_fusion/image_state_student_kitti_cache.pt

CUDA_VISIBLE_DEVICES=1 EPOCHS=20 \
OUT=runs/stage6_fusion/image_state_student_gate20_seed7 \
bash dream3r/scripts/run_image_state_student_sweep.sh
```

Final gate20 result:

```text
runs/stage6_fusion/image_state_student_gate20_seed7

correct-state: KITTI 0.1649, ETH3D 0.2842
no-state:      KITTI 0.1526, ETH3D 0.1702
shuffle-state: KITTI 0.1577, ETH3D 0.2754
fallback contamination: 0
```

The 1-epoch smoke also ran and was worse than the locked baseline:

```text
runs/stage6_fusion/image_state_student_smoke_seed7
correct-state: KITTI 0.1642, ETH3D 0.2840
```

## Verdict

```text
U1 fails the usable-model gate:

- it does not beat the locked bounded frozen-StatePrior baseline
  (KITTI/ETH3D 0.1448/0.1475);
- correct-state is worse than no-state on both domains;
- shuffle-state remains competitive with correct-state;
- the no-proposal/native point head is unstable.
```

Keep the U1 scaffold because it is the right non-core surface for future image
native work, but do not rerun it as-is. The next native attempt needs a changed
objective or architecture, not more epochs on this gate.
