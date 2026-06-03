# CYCLE-20260603: VLM semantic label-cache gate

Date: 2026-06-03
Status: local implementation gate complete
Decision: `decisions/DEC-20260603-028-vlm-semantic-label-cache-gate.md`

## Trigger

The user asked to test Qwen3-VL-2B-Instruct as an offline semantic controller
signal for Dream3R, not as a geometry model. The requested first gate was a
small reversible label cache with strict JSON schema, mock backend tests,
optional Qwen backend only if weights are already available or approved, and
state-causality controls for later Router/Critic evaluation.

## Work completed

Added:

```text
code/dream3r/scripts/build_vlm_semantic_labels.py
code/dream3r/tests/test_vlm_semantic_labels.py
decisions/DEC-20260603-028-vlm-semantic-label-cache-gate.md
cycles/CYCLE-20260603-vlm-semantic-label-cache-gate.md
runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_window_manifest.json
runs/vlm_semantic_controller/qwen3vl2b_smoke/mock_labels.json
runs/vlm_semantic_controller/qwen3vl2b_smoke/schema_report.json
```

Updated the project guidance chain:

```text
TASK_SNAPSHOT.md
WORKFLOW_STATUS.md
INDEX.md
mainwork.md
registry/decision_registry.md
README.md
RESEARCH_STATE.md
AGENT_MASTER_PROMPT.md
planning/DREAM3R_V11_VLM_SEMANTIC_CONTROLLER_RESEARCH_PLAN.md
handoff/ARCHITECTURE_V11_VLM_SEMANTIC_CONTROLLER_AGENT_PROMPT.md
```

## Implementation summary

The label builder:

- reads a JSON window manifest;
- produces strict `dream3r_vlm_semantic_v1` semantic-risk records;
- keeps `model_id`, prompt hash, backend, window id, dataset, and frame list;
- rejects malformed or out-of-schema VLM output into explicit `failure_flags`;
- derives fixed-length controller features;
- writes real, shuffled, and disabled feature controls for later causality
  experiments;
- keeps Qwen model loading local-only unless an explicit remote-load flag is
  passed after approval.

The script does not write geometry, pointmaps, depth, camera, pose, or training
targets.

## Verification

Local compile:

```text
python -B -m py_compile \
  code/dream3r/scripts/build_vlm_semantic_labels.py \
  code/dream3r/tests/test_vlm_semantic_labels.py
```

Targeted tests:

```text
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

Schema result:

```text
backend: mock_valid
n_windows: 2
valid_records: 2
failure_records: 0
schema_pass_rate: 1.0
control_keys: features, shuffled_features, disabled_features
```

## Qwen availability check

Read-only server checks found no staged Qwen3-VL-2B-Instruct weights at the
checked paths:

```text
/hdd3/kykt26/checkpoints/qwen/Qwen3-VL-2B-Instruct
/hdd3/kykt26/checkpoints/Qwen3-VL-2B-Instruct
/hdd3/kykt26/models/Qwen3-VL-2B-Instruct
/hdd3/kykt26/checkpoints/huggingface/Qwen3-VL-2B-Instruct
```

The existing BUAA-Server `dream3r` conda environment reports:

```text
transformers 4.46.0
```

The official Qwen3-VL repository states Qwen3-VL requires
`transformers>=4.57.0`. Therefore no Qwen inference was attempted in this pass.

## Boundaries preserved

- no frozen-core edit;
- no model training;
- no checkpoint download;
- no server environment mutation;
- no claim that VLM labels are geometry;
- no claim that Dream3R is usable beyond the locked 0.1448/0.1475 bounded
  baseline.

## Next executable gate

Create a real KITTI/ETH3D window manifest from existing cache windows, then run
a 10-window Qwen smoke on BUAA-Server GPU1 only after Qwen3-VL weights and a
compatible Transformers/Qwen stack are staged or explicitly approved. The next
Router/Critic gate should consume the generated `features`,
`shuffled_features`, and `disabled_features` without changing geometry code.
