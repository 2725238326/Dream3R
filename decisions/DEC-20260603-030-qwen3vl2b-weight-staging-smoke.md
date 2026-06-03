# DEC-20260603-030: Qwen3-VL-2B weight staging and real-label smoke

Date: 2026-06-03
Status: accepted; weights staged, real KITTI smoke schema-positive
Scope: Dream3R V11 Qwen semantic-controller runtime readiness

## Context

DEC-20260603-028 and DEC-20260603-029 built the offline VLM semantic label
cache and controller dry-run surfaces. Until this pass, Qwen3-VL-2B-Instruct
was blocked because weights were not staged and the existing `dream3r` env used
Transformers 4.46.0.

The user authorized starting weight work with: "我们权重开始搞吧".

## Decision

Stage `Qwen/Qwen3-VL-2B-Instruct` on BUAA-Server and run the smallest real
semantic-label smoke on GPU1.

Server staging:

```text
weights: /hdd3/kykt26/checkpoints/qwen/Qwen3-VL-2B-Instruct
runtime: /hdd3/kykt26/envs/qwen3vl2b_smoke
repo:    /hdd3/kykt26/code/dream3r
gpu:     CUDA_VISIBLE_DEVICES=1
```

The existing `dream3r` env was not mutated. A separate venv was created with
`--system-site-packages` to reuse the existing Torch install while isolating
new Qwen runtime packages.

## Verification

Weight inventory:

```text
model.safetensors sha256:
7de1838c87a5349b016c26a1c3f7d2bc400a3d485f95ef39a7059ffd734977a0

model.safetensors size: 4255140312 bytes
checkpoint dir size:   4.0G
```

Runtime probe:

```text
python: /hdd3/kykt26/envs/qwen3vl2b_smoke/bin/python
torch: 2.5.1+cu121
transformers: 5.9.0
huggingface_hub: 1.17.0
qwen_vl_utils: installed
accelerate: 1.13.0
processor: Qwen3VLProcessor
config: Qwen3VLConfig / qwen3_vl
```

Local test after prompt/parser tightening:

```text
python -B -m pytest --assert=plain \
  code/dream3r/tests/test_vlm_semantic_labels.py \
  code/dream3r/tests/test_vlm_controller_integration.py -q
# 6 passed
```

Server compile:

```text
cd /hdd3/kykt26/code/dream3r
/hdd3/kykt26/envs/qwen3vl2b_smoke/bin/python -B -m py_compile \
  dream3r/scripts/build_vlm_semantic_labels.py \
  dream3r/scripts/build_vlm_window_manifest.py \
  dream3r/scripts/eval_vlm_controller_dryrun.py
```

Real Qwen smoke:

```text
CUDA_VISIBLE_DEVICES=1 PYTHONPATH=/hdd3/kykt26/code/dream3r \
  /hdd3/kykt26/envs/qwen3vl2b_smoke/bin/python -B \
  dream3r/scripts/build_vlm_semantic_labels.py \
  --window-manifest runs/vlm_semantic_controller/qwen3vl2b_real_smoke/kitti_5win_manifest.json \
  --output runs/vlm_semantic_controller/qwen3vl2b_real_smoke/qwen_labels_5win_t320.json \
  --schema-report runs/vlm_semantic_controller/qwen3vl2b_real_smoke/schema_report_5win_t320.json \
  --backend qwen \
  --model-path /hdd3/kykt26/checkpoints/qwen/Qwen3-VL-2B-Instruct \
  --max-windows 5 \
  --max-new-tokens 320
```

Result:

```text
n_windows: 5
valid_records: 5
failure_records: 0
schema_pass_rate: 1.0
control_keys: features, shuffled_features, disabled_features
```

Artifacts copied into local workspace:

```text
runs/vlm_semantic_controller/qwen3vl2b_real_smoke/kitti_5win_manifest.json
runs/vlm_semantic_controller/qwen3vl2b_real_smoke/qwen_labels_5win_t320.json
runs/vlm_semantic_controller/qwen3vl2b_real_smoke/schema_report_5win_t320.json
```

## Boundaries

- No frozen-core edits.
- No Router/Critic training.
- No geometry outputs, depth, pose, or pointmaps from Qwen.
- Existing `dream3r` env was not upgraded or overwritten.
- A temporary SSH reverse proxy tunnel was used only for download, then stopped.

## Verdict

Qwen3-VL-2B-Instruct is now staged and runnable as an offline semantic labeler
for Dream3R V11. The real smoke proves runtime and strict-schema viability on
five KITTI windows. It does not prove that Qwen improves routing, Critic
calibration, or geometry quality.

## Next gate

Build a larger 50-window KITTI/ETH3D Qwen label cache, then run
`eval_vlm_controller_dryrun.py` against held-out oracle labels/metrics. Promote
to Router/Critic training only if real Qwen features beat shuffled and disabled
controls.
