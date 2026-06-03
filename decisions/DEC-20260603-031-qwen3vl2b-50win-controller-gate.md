# DEC-20260603-031: Qwen3-VL-2B 50-window controller gate

Date: 2026-06-03
Status: accepted; schema-positive but controller-negative
Scope: Dream3R V11 Qwen semantic-controller held-out gate

## Context

DEC-20260603-030 staged Qwen3-VL-2B-Instruct and proved that the offline
semantic labeler can emit strict JSON for a five-window KITTI smoke. The next
gate is not training. It is a held-out controller diagnostic: real Qwen semantic
features must be compared against shuffled and disabled controls before any
Router/Critic promotion.

## Decision

Proceed with the first larger real gate on BUAA-Server GPU1 using existing
oracle labels and metrics.

Use Qwen only as an offline semantic controller signal:

- input: RGB image windows;
- output: strict semantic/risk JSON label cache;
- controls: real, shuffled, disabled feature maps;
- downstream check: deterministic Router/Critic dry-run against existing
  oracle expert labels/metrics;
- forbidden: Qwen geometry, depth, pose, pointmap, training, or frozen-core
  edits.

## Implementation Delta

Added a reversible manifest id option:

```text
build_vlm_window_manifest.py --window-id-mode {prefixed,sequence}
```

The default remains `prefixed`, preserving prior artifacts. The new
`sequence` mode is used only when the VLM manifest must overlap existing oracle
files whose keys are raw KITTI/ETH3D sequence ids.

## Verification

Local tests:

```text
PYTHONDONTWRITEBYTECODE=1 python -B -m pytest --assert=plain \
  code/dream3r/tests/test_vlm_semantic_labels.py \
  code/dream3r/tests/test_vlm_controller_integration.py -q
# 7 passed
```

Server 50-window manifest:

```text
manifest: runs/vlm_semantic_controller/qwen3vl2b_real_50win/kitti_50win_manifest.json
oracle:   runs/stage5_s1_expand_oracle/oracle_expert_labels.json
windows:  50
overlap:  50/50
missing_frames: []
```

Qwen command on GPU1:

```text
cd /hdd3/kykt26/code/dream3r
CUDA_VISIBLE_DEVICES=1 PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=/hdd3/kykt26/code/dream3r \
/hdd3/kykt26/envs/qwen3vl2b_smoke/bin/python -B \
  dream3r/scripts/build_vlm_semantic_labels.py \
  --window-manifest runs/vlm_semantic_controller/qwen3vl2b_real_50win/kitti_50win_manifest.json \
  --output runs/vlm_semantic_controller/qwen3vl2b_real_50win/qwen_labels_50win_t320.json \
  --schema-report runs/vlm_semantic_controller/qwen3vl2b_real_50win/schema_report_50win_t320.json \
  --backend qwen \
  --model-path /hdd3/kykt26/checkpoints/qwen/Qwen3-VL-2B-Instruct \
  --max-windows 50 \
  --max-new-tokens 320
```

Schema result:

```text
n_windows: 50
valid_records: 50
failure_records: 0
schema_pass_rate: 1.0
control_keys: features, shuffled_features, disabled_features
```

Controller dry-run:

```text
oracle_mean: 0.14893413588404655
vlm_real:    0.2365107437968254
vlm_shuffle: 0.2365107437968254
vlm_disabled:0.2365107437968254
promotable:  false
```

Detailed diagnostic:

```text
vlm_real expert_counts:    fast3r=50, mast3r=0, spann3r=0
vlm_shuffle expert_counts: fast3r=50, mast3r=0, spann3r=0
vlm_disabled expert_counts:fast3r=50, mast3r=0, spann3r=0
hard_windows: 38
verify trigger real/shuffle: 1.0
verify trigger disabled:     0.0
```

The 50 Qwen records were schema-valid but not controller-useful under the
current prompt/features/policy. The labels collapsed to `road`/`building`, risk
scores were all zero, and `suggest_verify_geometry=True` fired for every
window. The deterministic route policy therefore selected Fast3R for every
window, exactly matching shuffled and disabled route metrics.

Artifacts copied into the local workspace:

```text
runs/vlm_semantic_controller/qwen3vl2b_real_50win/kitti_50win_manifest.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win/qwen_labels_50win_t320.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win/schema_report_50win_t320.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win/controller_dryrun_50win_t320.json
```

## Boundaries

- No frozen-core files edited.
- No Router/Critic training.
- No Qwen geometry outputs.
- No claim that Qwen improves routing; real/shuffle/disabled controls did not
  separate.

## Verdict

Qwen3-VL-2B-Instruct is operational as an offline semantic labeler, but this
first 50-window controller policy is not promotable. Future work should change
the semantic question/features/policy before any Router/Critic training.
