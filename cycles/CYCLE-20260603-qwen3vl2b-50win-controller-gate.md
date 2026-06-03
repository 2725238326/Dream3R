# Cycle 20260603: Qwen3-VL-2B 50-Window Controller Gate

Date: 2026-06-03
Status: closed negative; schema-positive, controller-negative
Decision: `decisions/DEC-20260603-031-qwen3vl2b-50win-controller-gate.md`

## Goal

Move from the five-window Qwen schema smoke to the first oracle-aligned
50-window controller diagnostic, without training and without touching frozen
core files.

## Actions

1. Inspected existing oracle labels:

```text
runs/stage5_s1_expand_oracle/oracle_expert_labels.json
labels: 59
metrics: 59
expert_order: fast3r, mast3r, spann3r
metric: scale_aligned_abs_rel
```

2. Added reversible manifest id mode:

```text
--window-id-mode prefixed   # default, prior behavior
--window-id-mode sequence   # oracle-compatible ids for dry-run overlap
```

3. Added regression coverage for oracle-compatible ids.

4. Built a KITTI 50-window manifest on BUAA-Server:

```text
output: runs/vlm_semantic_controller/qwen3vl2b_real_50win/kitti_50win_manifest.json
n_windows: 50
oracle overlap: 50/50
missing frame paths: 0
```

5. Ran Qwen3-VL-2B-Instruct label generation on GPU1:

```text
CUDA_VISIBLE_DEVICES=1
model: /hdd3/kykt26/checkpoints/qwen/Qwen3-VL-2B-Instruct
runtime: /hdd3/kykt26/envs/qwen3vl2b_smoke
max_new_tokens: 320
```

The log showed Qwen weights loading successfully. A short SSH reset happened
during polling, then SSH recovered and artifacts were retrieved.

6. Ran the controller dry-run:

```text
output: runs/vlm_semantic_controller/qwen3vl2b_real_50win/controller_dryrun_50win_t320.json
oracle: runs/stage5_s1_expand_oracle/oracle_expert_labels.json
controls: real, shuffled, disabled
```

## Verification

Local:

```text
PYTHONDONTWRITEBYTECODE=1 python -B -m pytest --assert=plain \
  code/dream3r/tests/test_vlm_semantic_labels.py \
  code/dream3r/tests/test_vlm_controller_integration.py -q
# 7 passed
```

Server manifest overlap:

```text
n_windows: 50
overlap: 50
missing_frames: []
```

Qwen schema:

```text
n_windows: 50
valid_records: 50
failure_records: 0
schema_pass_rate: 1.0
```

Controller dry-run:

```text
oracle_mean: 0.14893413588404655
vlm_real: 0.2365107437968254
vlm_shuffle: 0.2365107437968254
vlm_disabled: 0.2365107437968254
real_beats_disabled: false
real_beats_shuffle: false
promotable: false
```

Detailed finding:

```text
real/shuffle/disabled routes all selected Fast3R for 50/50 windows.
Qwen scene labels: building=33, road=17.
Risk scores: all zero across dynamic/low_texture/reflection/occlusion/
large_baseline/scale_drift/repeated_structure.
suggest_verify_geometry: true for 50/50.
```

Artifacts copied locally:

```text
runs/vlm_semantic_controller/qwen3vl2b_real_50win/kitti_50win_manifest.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win/qwen_labels_50win_t320.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win/schema_report_50win_t320.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win/controller_dryrun_50win_t320.json
```

## Boundary

This cycle does not promote Qwen into the model. It only proves that Qwen can
produce strict offline labels; the current controller policy has no routing
advantage over shuffled/disabled controls.

## Next

Do not train Router/Critic from this cache. The next Qwen pass should redesign
the semantic prompt/features/policy so it emits discriminative risk/regime
signals, then re-run the same real/shuffle/disabled gate.
