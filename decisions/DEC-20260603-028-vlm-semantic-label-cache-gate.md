# DEC-20260603-028: VLM semantic label-cache gate

Date: 2026-06-03
Status: accepted; local mock gate closed, Qwen inference blocked
Scope: Dream3R V11 offline semantic-controller cache

## Context

DEC-20260603-027 accepted Qwen3-VL-2B-Instruct as a semantic controller
candidate, not as a geometry model. The first executable gate was a strict
offline label cache with explicit failure handling, mock backend tests, optional
Qwen backend, and shuffled/disabled controls for later Router/Critic evaluation.

The current usable bounded Dream3R baseline remains:

```text
proposal teachers + Dream state -> frozen StatePrior -> bounded residual
KITTI/ETH3D: 0.1448/0.1475
```

## Decision

Add the smallest reversible V11 implementation surface:

```text
code/dream3r/scripts/build_vlm_semantic_labels.py
code/dream3r/tests/test_vlm_semantic_labels.py
runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_window_manifest.json
runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_labels.json
runs/vlm_semantic_controller/qwen3vl2b_smoke/schema_report.json
```

The script:

- consumes a window manifest with `window_id`, `dataset`, and frame paths;
- writes strict `dream3r_vlm_semantic_v1` records;
- records `model_id`, prompt hash, backend, window id, dataset, frames, risk
  labels, suggestions, confidence, and `failure_flags`;
- converts records to a fixed feature vector for Router/Critic experiments;
- emits `features`, `shuffled_features`, and `disabled_features` controls;
- turns malformed or invalid VLM output into explicit failure records;
- defaults Qwen loading to local files only, so selecting the Qwen backend does
  not download weights by accident.

## Boundaries

- No frozen-core edits.
- No geometry labels, depth, camera, or pointmaps are generated.
- No training was started.
- No checkpoint was downloaded.
- No server environment was mutated.
- Qwen inference was not run because the required weights/dependencies are not
  already staged.

## Verification

Local:

```text
python -B -m py_compile \
  code/dream3r/scripts/build_vlm_semantic_labels.py \
  code/dream3r/tests/test_vlm_semantic_labels.py

python -B -m pytest code/dream3r/tests/test_vlm_semantic_labels.py -q
# 4 passed
```

Mock smoke:

```text
python -B code/dream3r/scripts/build_vlm_semantic_labels.py \
  --window-manifest runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_window_manifest.json \
  --output runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_labels.json \
  --schema-report runs/vlm_semantic_controller/qwen3vl2b_smoke/schema_report.json \
  --backend mock \
  --mock-mode valid
```

Result:

```text
schema_version: dream3r_vlm_semantic_v1
backend: mock_valid
n_windows: 2
valid_records: 2
failure_records: 0
schema_pass_rate: 1.0
control_keys: features, shuffled_features, disabled_features
```

BUAA-Server read-only availability check:

```text
missing:/hdd3/kykt26/checkpoints/qwen/Qwen3-VL-2B-Instruct
missing:/hdd3/kykt26/checkpoints/Qwen3-VL-2B-Instruct
missing:/hdd3/kykt26/models/Qwen3-VL-2B-Instruct
missing:/hdd3/kykt26/checkpoints/huggingface/Qwen3-VL-2B-Instruct
dream3r env transformers: 4.46.0
```

The official Qwen3-VL repo currently states Qwen3-VL requires
`transformers>=4.57.0`, so the existing server environment is not ready for
Qwen3-VL inference without an approved environment update.

## Verdict

The V11 label-cache gate is implementation-ready for local schema/control work.
It is not a Qwen result yet. Real Qwen smoke remains blocked until:

1. Qwen3-VL-2B-Instruct weights are staged on BUAA-Server;
2. the server environment has a compatible Transformers/Qwen3-VL stack;
3. the run is launched on GPU1 with no fallback contamination.

## Next gate

Build a real window manifest for existing KITTI/ETH3D cache windows and run a
10-window Qwen smoke only after weights and dependencies are staged or approved.
Then compare `features` versus `shuffled_features` and `disabled_features` in a
Router/Critic dry-run before any training claim.
