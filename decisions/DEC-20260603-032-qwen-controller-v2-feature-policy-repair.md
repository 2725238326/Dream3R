# DEC-20260603-032: Qwen controller v2 feature/policy repair

Date: 2026-06-03
Status: accepted; weak-positive dry-run, not promotable
Scope: Dream3R V11 Qwen offline semantic-controller signal

## Context

DEC-20260603-031 closed the first 50-window Qwen controller gate as negative.
Qwen produced strict JSON for all windows, but the controller ignored the useful
parts of the output: `visible_failure_causes` and object lists carried signal,
while most `risk_*` numeric fields collapsed to zero. The deterministic policy
also routed road scenes to Fast3R before considering low-texture, reflection,
repeated-structure, or occlusion risks.

## Decision

Patch only the reversible label-cache/controller surface:

1. Tighten the prompt so any `visible_failure_causes` token must correspond to
   a non-zero matching risk and `suggest_verify_geometry` should not be always
   true.
2. Derive a feature-level risk floor from `visible_failure_causes`.
3. Route dynamic risk to Spann3R first; then route low-texture, reflection,
   repeated-structure, or occlusion risk to MASt3R; then fall back to Fast3R for
   large-baseline or road-like windows.

This does not touch frozen core and does not train Router/Critic.

## Implementation

Changed:

```text
code/dream3r/scripts/build_vlm_semantic_labels.py
code/dream3r/scripts/eval_vlm_controller_dryrun.py
code/dream3r/tests/test_vlm_semantic_labels.py
code/dream3r/tests/test_vlm_controller_integration.py
```

New behavior:

```text
visible_failure_causes dynamic            -> risk_dynamic floor
visible_failure_causes low_texture        -> risk_low_texture floor
visible_failure_causes reflection         -> risk_reflection floor
visible_failure_causes occlusion          -> risk_occlusion floor
visible_failure_causes large_baseline     -> risk_large_baseline floor
visible_failure_causes scale_drift        -> risk_scale_drift floor
visible_failure_causes repeated_structure -> risk_repeated_structure floor
```

The floor is used as controller feature derivation, not as geometry evidence.

## Verification

Local:

```text
PYTHONDONTWRITEBYTECODE=1 python -B -m pytest --assert=plain \
  code/dream3r/tests/test_vlm_semantic_labels.py \
  code/dream3r/tests/test_vlm_controller_integration.py -q
# 9 passed
```

Server:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/hdd3/kykt26/code/dream3r \
/hdd3/kykt26/envs/qwen3vl2b_smoke/bin/python -B -m pytest --assert=plain \
  dream3r/tests/test_vlm_semantic_labels.py \
  dream3r/tests/test_vlm_controller_integration.py -q
# 9 passed
```

Offline re-evaluation of the DEC-031 cache with v2 feature/policy:

```text
oracle_mean: 0.14893413588404655
vlm_real:    0.16996440216898917
vlm_shuffle: 0.17206742718815804
vlm_disabled:0.2365107437968254
```

Fresh Qwen v2 50-window run on GPU1:

```text
schema_pass_rate: 1.0
valid_records: 50
failure_records: 0
oracle_mean: 0.14893413588404655
vlm_real:    0.175017766058445
vlm_shuffle: 0.17588756889104842
vlm_disabled:0.2365107437968254
promotable: false
```

V2 real labels beat disabled clearly and beat shuffled marginally, but the
real-vs-shuffle gap is too small for promotion.

Artifacts:

```text
runs/vlm_semantic_controller/qwen3vl2b_real_50win_v2/kitti_50win_manifest.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win_v2/qwen_labels_50win_t320_v2.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win_v2/schema_report_50win_t320_v2.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win_v2/controller_dryrun_50win_t320_v2.json
```

## Verdict

Qwen semantic control is no longer dead-on-arrival: the v2 feature/policy repair
creates a measurable signal and repairs the disabled-control gap. It is still
not strong enough to train or promote Router/Critic. The next useful gate is a
learned or calibrated controller over these semantic features with a held-out
split, not another deterministic rule tweak on the same 50 windows.
