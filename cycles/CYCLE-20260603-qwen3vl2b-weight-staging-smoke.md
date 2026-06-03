# Cycle 20260603: Qwen3-VL-2B Weight Staging Smoke

Date: 2026-06-03
Status: closed; weights staged and real KITTI schema smoke passed
Decision: `decisions/DEC-20260603-030-qwen3vl2b-weight-staging-smoke.md`

## Goal

Stage Qwen3-VL-2B-Instruct weights and verify that Dream3R V11 can run real
offline semantic labels on BUAA-Server GPU1.

## Actions

1. Created checkpoint staging directory:

```text
/hdd3/kykt26/checkpoints/qwen/Qwen3-VL-2B-Instruct
```

2. Used an SSH reverse proxy tunnel from the local machine to make server-side
Hugging Face download possible. The tunnel was stopped after download.

3. Downloaded 12 Qwen3-VL-2B-Instruct files, including:

```text
model.safetensors 4255140312 bytes
config.json
tokenizer.json
preprocessor_config.json
video_preprocessor_config.json
```

4. Created isolated runtime:

```text
/hdd3/kykt26/envs/qwen3vl2b_smoke
```

The existing `dream3r` conda env was not upgraded. The isolated venv uses
`--system-site-packages` and installed the Qwen-facing runtime packages only.

5. Synchronized V11 non-core scripts to the server package path:

```text
/hdd3/kykt26/code/dream3r/dream3r/scripts/
```

6. Tightened `build_vlm_semantic_labels.py` prompt/parser:

- explicit raw JSON only;
- JSON booleans only for suggestion fields;
- allowlisted `visible_failure_causes`;
- strict parser accepts pure JSON or a single JSON fenced block, then runs the
  same schema validation.

## Verification

Local:

```text
python -B -m pytest --assert=plain \
  code/dream3r/tests/test_vlm_semantic_labels.py \
  code/dream3r/tests/test_vlm_controller_integration.py -q
# 6 passed
```

Server:

```text
/hdd3/kykt26/envs/qwen3vl2b_smoke/bin/python -B -m py_compile \
  dream3r/scripts/build_vlm_semantic_labels.py \
  dream3r/scripts/build_vlm_window_manifest.py \
  dream3r/scripts/eval_vlm_controller_dryrun.py
```

GPU1 smoke:

```text
n_windows: 5
valid_records: 5
failure_records: 0
schema_pass_rate: 1.0
```

Artifacts:

```text
runs/vlm_semantic_controller/qwen3vl2b_real_smoke/kitti_5win_manifest.json
runs/vlm_semantic_controller/qwen3vl2b_real_smoke/qwen_labels_5win_t320.json
runs/vlm_semantic_controller/qwen3vl2b_real_smoke/schema_report_5win_t320.json
```

## Boundaries

- No frozen-core edit.
- No training.
- No Qwen geometry claim.
- No Router/Critic promotion yet.

## Next

Run a larger 50-window real Qwen cache and then evaluate real/shuffle/disabled
semantic controls with the dry-run evaluator before any training.
