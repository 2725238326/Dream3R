# Cycle 20260603: Qwen Semantic Controller Integration

Date: 2026-06-03
Status: closed local mock-positive; real Qwen blocked
Decision: `decisions/DEC-20260603-029-qwen-semantic-controller-integration.md`

## Goal

Integrate the V11 Qwen/VLM semantic label cache into Dream3R architecture
evaluation as a controller signal, not as a geometry model.

## Work Completed

1. Added `code/dream3r/scripts/build_vlm_window_manifest.py`.
   - Builds VLM image-window manifests from KITTI/ETH3D dataset metadata.
   - Keeps output at image paths and window ids only; no geometry labels are
     generated.

2. Added `code/dream3r/scripts/eval_vlm_controller_dryrun.py`.
   - Consumes `dream3r_vlm_semantic_v1` cache outputs.
   - Compares real, shuffled, and disabled VLM feature controls.
   - Reports Router-style route regret and Critic-like trigger rates.
   - Forces `promotable=false` until real Qwen labels and held-out evaluation
     exist.

3. Added `code/dream3r/tests/test_vlm_controller_integration.py`.
   - Covers KITTI manifest generation from local fixture metadata.
   - Covers controller dry-run causality controls.

4. Added mock dry-run artifacts under
   `runs/vlm_semantic_controller/qwen3vl2b_smoke/`.

## Verification

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

Mock dry-run:

```text
python -B code/dream3r/scripts/eval_vlm_controller_dryrun.py \
  --vlm-cache runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_labels.json \
  --oracle-labels runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_oracle_labels.json \
  --output runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_controller_dryrun.json
```

Observed:

```text
vlm_real: 0.2100
vlm_shuffle: 0.5250
vlm_disabled: 0.3600
promotable: false
```

## Boundaries Preserved

- No frozen-core files changed.
- No training run.
- No checkpoint download.
- No server environment mutation.
- No VLM geometry claim.
- Qwen inference remains blocked until weights and compatible dependencies are
  staged or approved.

## Next Step

Run real Qwen labels only after staging weights/dependencies on BUAA-Server
GPU1. Then use the dry-run evaluator on held-out windows before any Router or
Critic promotion.
