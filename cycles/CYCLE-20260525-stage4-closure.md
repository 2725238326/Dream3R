# CYCLE 20260525 Stage 4 — Critic + Repair Closure

## Scope

Close Stage 4 by training the Critic on real KITTI expert outputs, wiring real repair actions into the pipeline ablation, retraining the ComposerRouter so critic context can affect routing, and rerunning the hard-sequence ablation on the server.

## Changes

- Synced the previous regime-aware `ComposerRouter.confidence_gate` fix to the server.
- Extended `ComposerRouter` critic context with `previous_expert_id` one-hot input.
- Passed previous `routed_expert_id` from `model.py` main forward into `ComposerRouter` when previous critic confidence exists.
- Added backward-compatible `load_state_dict` handling for old confidence-gate checkpoints.
- Extended `train_router_only.py` with:
  - zero-confidence supervision for the `recommended_action == reroute_model` path
  - optional Stage 4 context-data supervision from `critic_training_data.pt`
  - summary metrics for context accuracy
- Updated `eval_repair_pipeline_ablation.py` to pass previous expert id and to use the closure criterion from the handoff: `full <= critic <= both` with at least one strict inequality.

## Verification

Server focused tests:

```text
python -m pytest \
  dream3r/tests/test_critic_only_training.py \
  dream3r/tests/test_repair_executor_contract.py \
  dream3r/tests/test_v04_test3r_offpath.py \
  dream3r/tests/test_repair_ablation_eval.py \
  dream3r/tests/test_repair_pipeline_ablation_eval.py \
  dream3r/tests/test_router_only_training.py \
  dream3r/tests/test_spatial_memory.py -q

32 passed, 15 warnings
```

Local schema/focused tests:

```text
python -m pytest tests/test_router_only_training.py tests/test_repair_pipeline_ablation_eval.py tests/test_spatial_memory.py -q

16 passed, 1 warning
```

## Critic Summary

Checkpoint: `/hdd3/kykt26/checkpoints/critic_only_v1/latest.pt`

```text
n_examples: 24
conflict_abs_rel_corr: 0.8337993524
repair_action_accuracy: 0.9166666865
baseline_action0_accuracy: 0.5
t4_1: true
```

## Router Retrain Summary

Checkpoint: `/hdd3/kykt26/checkpoints/router_only_v1/latest.pt`

Command:

```text
python -m dream3r.scripts.train_router_only \
  --preset router_only \
  --epochs 2000 \
  --lr 0.05 \
  --batch-size 16 \
  --context-data /hdd3/kykt26/code/dream3r/runs/stage4_critic_data/critic_training_data.pt \
  --output-dir /hdd3/kykt26/checkpoints/router_only_v1
```

Summary:

```text
n_examples: 8
context_n_examples: 12
final_accuracy: 1.0
augmented_with_critic_confidence: true
high_conf_accuracy_vs_best: 1.0
low_conf_accuracy_vs_alt: 1.0
low_conf_flip_rate_vs_no_conf: 1.0
low_conf_context_accuracy_min: 0.9166666865
threshold_conf_context_accuracy_min: 0.8333333135
zero_conf_context_accuracy_min: 0.9166666865
```

## Pipeline Ablation

Output: `/hdd3/kykt26/code/dream3r/runs/stage4_repair_pipeline_ablation/results.json`

```text
metric: scale_aligned_abs_rel
n_sequences: 12
n_hard_sequences: 4
full_pipeline_repair_on: 0.2108669020
critic_on_repair_off: 0.2253848203
both_off: 0.2253848203
mean_relative_improvement_vs_both_off: 0.0644139131
best_example_relative_improvement: 0.2488888968
critic_changed_route_count: 1
repair_changed_output_count: 2
t4_3: true
```

The row-level route change is real:

```text
2011_09_26_drive_0070_sync_02:
  both_off: fast3r, abs-rel 0.1995531470
  critic_on_repair_off: mast3r, abs-rel 0.3486204147
  full_pipeline: primary mast3r -> repair reroute_model -> fast3r, abs-rel 0.1995531470
```

The best repair improvement is real:

```text
2011_09_26_drive_0051_sync_02:
  both_off: fast3r, abs-rel 0.2333236784
  full_pipeline: primary fast3r -> repair reroute_model -> mast3r, abs-rel 0.1752520055
  relative improvement: 24.88888968%
```

## Limitations

- `critic_on_repair_off` equals `both_off` at the hard-row aggregate level. Stage 4 closes because the project-level T4.3 gate supplied to this agent was `critic_changed_route_count > 0` and `t4_3 == true`; it should not be reported as a strict critic-only aggregate gain.
- The full-pipeline improvement comes from actual `reroute_model` repair on a hard sequence, not from a broad critic-only route-quality improvement.
- The ablation remains a 12-sequence KITTI hard/sample set with two real experts, not a SOTA benchmark.

## Boundary

Touched:

- `code/dream3r/modules.py`
- `code/dream3r/model.py`
- `code/dream3r/scripts/train_router_only.py`
- `code/dream3r/scripts/eval_repair_pipeline_ablation.py`
- `code/dream3r/tests/test_router_only_training.py`

`model.py` main forward was modified only after explicit user authorization, to pass previous routed expert context into the router.

Not touched:

- `code/dream3r/anchor_bank.py`
- `code/dream3r/nsa_attention.py`
- `code/dream3r/bus.py`

## Conclusion

Stage 4 is closed under the stated core gate: `critic_changed_route_count > 0` and `t4_3 == true`, with all numbers above coming from server artifacts.
