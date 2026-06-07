# DEC-20260604-034: Qwen semantic Critic-prior gate

Date: 2026-06-04
Status: accepted; diagnostic negative versus geometry-only
Scope: Dream3R V11 Qwen offline semantic signal for Critic trigger support

## Context

DEC-20260603-033 showed that Qwen semantic features are not promotable for
direct expert routing: real beats disabled but loses to shuffle under a
held-out calibrated controller. The next narrower question is whether Qwen can
still help as a Critic prior, where semantics only modulate a geometry
disagreement signal instead of choosing an expert.

## Decision

Add a standalone semantic-Critic diagnostic gate:

1. Keep Qwen/VLM as an offline semantic risk signal only.
2. Use per-expert metric dispersion as an offline geometry-disagreement proxy.
3. Evaluate hard-window verification triggers under the same trigger budget.
4. Compare:
   - geometry-only;
   - Qwen-only real/shuffle/disabled;
   - Qwen+geometry real/shuffle/disabled.

This does not train a Critic, does not run Qwen inference, and does not treat
Qwen output as geometry.

## Implementation

Changed:

```text
code/dream3r/scripts/eval_vlm_semantic_critic_gate.py
code/dream3r/tests/test_vlm_controller_integration.py
```

Artifact:

```text
runs/vlm_semantic_controller/qwen3vl2b_real_50win_v2/semantic_critic_gate_50win_t320_v2.json
```

## Verification

Local:

```text
python -B -m pytest --assert=plain \
  code/dream3r/tests/test_vlm_semantic_labels.py \
  code/dream3r/tests/test_vlm_controller_integration.py -q
# 11 passed
```

Server:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/hdd3/kykt26/code/dream3r \
/hdd3/kykt26/envs/qwen3vl2b_smoke/bin/python -B -m pytest --assert=plain \
  dream3r/tests/test_vlm_semantic_labels.py \
  dream3r/tests/test_vlm_controller_integration.py -q
# 11 passed
```

Server 50-window semantic Critic-prior gate:

```text
n_windows: 50
hard_window_count: 38
trigger_budget: 38
geometry_only_f1: 0.9210526315789473
vlm_real_qwen_only_f1: 0.7631578947368421
vlm_real_plus_geometry_f1: 0.8947368421052632
vlm_shuffle_plus_geometry_f1: 0.8421052631578947
vlm_disabled_plus_geometry_f1: 0.9210526315789473
```

Diagnostic:

```text
real_plus_beats_geometry_only: false
real_plus_beats_shuffle_plus: true
real_plus_beats_disabled_plus: false
promotable: false
```

## Verdict

Qwen semantics do not pass the current Critic-prior gate. They help relative to
shuffle in this diagnostic, but adding them to the geometry proxy makes the
trigger worse than geometry-only and no better than disabled+geometry. Therefore
the current Qwen cache remains an offline annotation/diagnostic lane only.

Future semantic-Critic work needs a real Critic/proposal-disagreement cache,
not oracle metric dispersion alone, and must pre-register a real > shuffle >
disabled threshold before promotion.
