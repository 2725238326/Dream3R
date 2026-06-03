# DEC-20260603-029: Qwen semantic-controller architecture integration

Date: 2026-06-03
Status: accepted; local dry-run gate closed, real Qwen still blocked
Scope: Dream3R V11 Router/Critic semantic-controller integration

## Context

DEC-20260603-028 added the offline VLM semantic label-cache gate. The next
architecture step is to make that cache consumable by Dream3R control surfaces
without changing geometry code or promoting VLM labels to depth/camera/pointmap
evidence.

The current usable bounded Dream3R baseline remains:

```text
proposal teachers + Dream state -> frozen StatePrior -> bounded residual
KITTI/ETH3D: 0.1448/0.1475
```

## Decision

Add the smallest reversible controller-integration surface:

```text
code/dream3r/scripts/build_vlm_window_manifest.py
code/dream3r/scripts/eval_vlm_controller_dryrun.py
code/dream3r/tests/test_vlm_controller_integration.py
runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_oracle_labels.json
runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_controller_dryrun.json
```

The manifest builder converts existing KITTI/ETH3D window metadata into an
image-window manifest for VLM labeling. The dry-run evaluator consumes a VLM
cache plus oracle expert labels/metrics and compares:

- real VLM semantic features;
- deterministically shuffled VLM features;
- VLM-disabled zero features.

The evaluator also records Critic-like trigger rates for geometry verification
and expensive teacher scheduling. It emits `promotable=false` by construction:
this gate proves schema/control plumbing only, not Qwen quality and not geometry
quality.

## Boundaries

- No frozen-core edits.
- No training.
- No checkpoint download.
- No server environment mutation.
- No real Qwen inference in this pass.
- VLM output remains semantic controller metadata only.
- Promotion requires real Qwen labels and held-out Router/Critic evaluation
  where real labels beat shuffled and disabled controls.

## Verification

Local syntax and targeted tests:

```text
python -B -m py_compile \
  code/dream3r/scripts/build_vlm_window_manifest.py \
  code/dream3r/scripts/eval_vlm_controller_dryrun.py \
  code/dream3r/tests/test_vlm_controller_integration.py

python -B -m pytest \
  code/dream3r/tests/test_vlm_semantic_labels.py \
  code/dream3r/tests/test_vlm_controller_integration.py -q
# 6 passed
```

Mock controller dry-run:

```text
python -B code/dream3r/scripts/eval_vlm_controller_dryrun.py \
  --vlm-cache runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_labels.json \
  --oracle-labels runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_oracle_labels.json \
  --output runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_controller_dryrun.json
```

Result:

```text
schema_version: dream3r_vlm_controller_dryrun_v1
n_windows: 2
oracle_mean: 0.2100
vlm_real: 0.2100
vlm_shuffle: 0.5250
vlm_disabled: 0.3600
real_beats_disabled: true
real_beats_shuffle: true
promotable: false
```

## Verdict

V11 is now wired as a local architecture-control lane: real window manifests can
feed semantic labels, and those labels can be tested against shuffled/disabled
controls before any Router/Critic training. This remains a mock-positive
controller-integration result, not a real Qwen result.

## Next gate

After Qwen3-VL-2B-Instruct weights and a compatible Qwen/Transformers stack are
staged on BUAA-Server, build a small real KITTI/ETH3D manifest, run 10-50 Qwen
labels on GPU1, then run this dry-run against held-out oracle metrics. Only if
real labels beat shuffled and disabled controls should the signal enter router
training or Critic threshold calibration.
