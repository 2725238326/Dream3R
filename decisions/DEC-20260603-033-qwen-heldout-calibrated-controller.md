# DEC-20260603-033: Qwen held-out calibrated controller gate

Date: 2026-06-03
Status: accepted; held-out diagnostic negative against shuffle
Scope: Dream3R V11 Qwen offline semantic-controller signal

## Context

DEC-20260603-032 repaired the deterministic Qwen semantic controller enough to
beat the disabled control and marginally beat shuffle on the same 50-window
dry-run. That result was not promotable because it still used a hand-written
policy tuned on the observed cache.

The next useful question is causal: do the Qwen semantic features support a
learned controller on held-out windows, or is the improvement mostly a same-set
policy artifact?

## Decision

Add a standalone held-out calibrated controller evaluator:

1. Split windows by KITTI drive/group using leave-one-group-out when possible.
2. Use oracle labels only inside each train fold to fit nearest-centroid
   semantic prototypes per expert.
3. Predict held-out routes from cached VLM features only.
4. Compare real Qwen features against shuffled and disabled feature controls.
5. Persist state-causality metadata for later Router/Critic evaluation.

This remains outside frozen core. It does not train Dream3R modules and does
not treat Qwen as geometry.

## Implementation

Changed:

```text
code/dream3r/scripts/eval_vlm_calibrated_controller.py
code/dream3r/tests/test_vlm_controller_integration.py
```

New artifact:

```text
runs/vlm_semantic_controller/qwen3vl2b_real_50win_v2/calibrated_controller_50win_t320_v2.json
```

The evaluator emits:

```text
schema_version: dream3r_vlm_calibrated_controller_v1
split_strategy: leave_one_group_out
state_causality_controls:
  oracle_used_for: train_fold_centroid_calibration_only
  heldout_oracle_leakage: false
  vlm_geometry_access: false
  dream3r_core_mutation: false
  control_variants: [vlm_real, vlm_shuffle, vlm_disabled]
```

## Verification

Local:

```text
python -B -m pytest --assert=plain \
  code/dream3r/tests/test_vlm_semantic_labels.py \
  code/dream3r/tests/test_vlm_controller_integration.py -q
# 10 passed
```

Server:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/hdd3/kykt26/code/dream3r \
/hdd3/kykt26/envs/qwen3vl2b_smoke/bin/python -B -m pytest --assert=plain \
  dream3r/tests/test_vlm_semantic_labels.py \
  dream3r/tests/test_vlm_controller_integration.py -q
# 10 passed
```

Held-out calibrated 50-window result:

```text
n_windows: 50
n_groups: 27
split_strategy: leave_one_group_out
oracle_mean: 0.14893413588404655
default_expert_mean: 0.2365107437968254
vlm_real:     0.18129218325018884
vlm_shuffle:  0.17762137934565544
vlm_disabled: 0.2365107437968254
real_beats_disabled: true
real_beats_shuffle: false
promotable: false
```

Route accuracy versus oracle:

```text
vlm_real:     0.44
vlm_shuffle:  0.44
vlm_disabled: 0.08
```

## Verdict

The held-out gate is negative for promotion. Qwen semantic features are better
than no semantic signal, but they do not beat shuffled features under this
calibrated leave-one-group-out controller. Therefore the current Qwen path
should remain an offline diagnostic/cache lane only.

Next work should not train Router/Critic from this 50-window cache. A future
Qwen pass needs broader data, a pre-registered promotion threshold, and
Router/Critic state-causality evaluation where real features beat both shuffle
and disabled controls.
