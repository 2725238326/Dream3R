# CYCLE 20260525 Stage 5 S1 - Three-Expert Composer Ablation

## Scope

Advance Stage 5 S1 by adding a third real expert candidate to the KITTI Composer oracle and rerunning the learned-router ablation with real pointmap metrics.

The third expert is Spann3R. No new checkpoint was downloaded in this cycle; the server already had the Spann3R repo and checkpoint artifacts.

## Changes

- Parameterized `build_oracle_expert_labels.py` with `--experts`, while preserving the default Stage 3 two-expert behavior.
- Added Spann3R support to the oracle builder through the existing real `Spann3RAdapter`.
- Generalized router training and router ablation from two hard-coded experts to an `expert_order` read from oracle labels/checkpoints.
- Added `--disable-critic-augmentation` for router-only Stage 5 ablations, so Stage 4 critic-confidence training does not distort the no-critic router evaluation target.
- Added optional class-balance alpha for diagnostics on small imbalanced expert-label sets.
- Extended router-ablation output with learned/oracle expert usage counts.
- Added schema tests for three-expert router training/eval.

## Server Verification

Spann3R real integration:

```text
DREAM3R_RUN_SPANN3R_INTEGRATION=1 CUDA_VISIBLE_DEVICES=0 python -m pytest dream3r/tests/test_spann3r_integration.py -q

2 passed, 8 warnings
```

Focused tests after script generalization:

```text
python -m pytest \
  dream3r/tests/test_oracle_expert_labels.py \
  dream3r/tests/test_router_ablation_eval.py \
  dream3r/tests/test_router_only_training.py \
  dream3r/tests/test_repair_pipeline_ablation_eval.py -q

10 passed, 1 warning
```

Stage 4 regression check after the shared router-loader change:

```text
stage4_repair_pipeline_ablation/results.json
t4_3: true
critic_changed_route_count: 1
repair_changed_output_count: 2
```

## Oracle Build

Command:

```text
python -m dream3r.scripts.build_oracle_expert_labels \
  --root /hdd3/kykt26/data \
  --regime-labels /hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json \
  --output /hdd3/kykt26/code/dream3r/runs/stage5_s1_oracle_labels/oracle_expert_labels.json \
  --experts fast3r mast3r spann3r \
  --max-per-regime 3 \
  --window-frames 4 \
  --max-frames-per-sequence 32 \
  --image-size 224 \
  --align-scale
```

Output:

```text
/hdd3/kykt26/code/dream3r/runs/stage5_s1_oracle_labels/oracle_expert_labels.json
n_sequences: 12
expert_order: [fast3r, mast3r, spann3r]
oracle_counts: mast3r=8, fast3r=2, spann3r=2
metric: scale_aligned_abs_rel
```

Spann3R is a real oracle winner on two KITTI windows:

```text
2011_09_28_drive_0177_sync_02
2011_09_29_drive_0026_sync_03
```

## Router Train

Command:

```text
python -m dream3r.scripts.train_router_only \
  --preset router_only \
  --oracle-labels /hdd3/kykt26/code/dream3r/runs/stage5_s1_oracle_labels/oracle_expert_labels.json \
  --output-dir /hdd3/kykt26/checkpoints/router_stage5_s1_v1 \
  --epochs 2000 \
  --lr 0.05 \
  --batch-size 12 \
  --disable-critic-augmentation
```

Summary:

```text
/hdd3/kykt26/checkpoints/router_stage5_s1_v1/summary.json
n_examples: 12
final_accuracy: 0.75
target_counts: mast3r=8, fast3r=2, spann3r=2
prediction_counts: mast3r=9, fast3r=3, spann3r=0
augmented_with_critic_confidence: false
critic_augmentation_disabled: true
```

## Router Ablation

Output:

```text
/hdd3/kykt26/code/dream3r/runs/stage5_s1_router_ablation/results.json
```

Final metrics:

```text
learned_router: 0.1722621613
oracle_router: 0.1636828103
always_mast3r: 0.1906146836
always_fast3r: 0.2252575532
always_spann3r: 0.2086918801
random_routing: 0.2293711156
best_single_expert: mast3r
relative_improvement_vs_best_single: 0.0962807369
route_regime_cramers_v: 1.0
```

Success fields:

```text
candidate_count_ge_3: true
oracle_uses_ge_3_experts: true
learned_uses_ge_3_experts: false
beats_best_single: true
improves_best_single_ge_5pct: true
stage5_s1: true
```

## Diagnostics

A class-balanced diagnostic run (`class_balance_alpha=0.4`) forced the learned router to use Spann3R, but it reduced the ablation gain below the S1 threshold:

```text
/hdd3/kykt26/code/dream3r/runs/stage5_s1_router_ablation/results_alpha04.json
learned_router: 0.1845527651
relative_improvement_vs_best_single: 0.0318019488
stage5_s1: false
```

This supports the final choice: use the checkpoint that optimizes real abs-rel, not the one that cosmetically selects every expert.

## Limitations

- The third real expert is in the candidate set and wins oracle on two real KITTI windows, but the final learned router does not select Spann3R.
- This means Stage 5 S1 closes only as a three-candidate learned-router ablation, not as proof that the current 6D regime-probability router can exploit every useful third-expert case.
- Several oracle conflicts are not separable from current router inputs alone. Example: some dynamic windows share identical regime probabilities but have different oracle experts.
- The next credible step is to add richer router features from the existing regime-label `stats` block or from per-sequence evidence, then rerun this same ablation.

## Boundary

Touched:

- `code/dream3r/scripts/build_oracle_expert_labels.py`
- `code/dream3r/scripts/train_router_only.py`
- `code/dream3r/scripts/eval_router_ablation.py`
- `code/dream3r/tests/test_oracle_expert_labels.py`
- `code/dream3r/tests/test_router_ablation_eval.py`

Not touched:

- `code/dream3r/model.py`
- `code/dream3r/anchor_bank.py`
- `code/dream3r/nsa_attention.py`
- `code/dream3r/bus.py`

## Conclusion

Stage 5 S1 is closed under the explicit router-ablation gate: the learned router with a three-real-expert candidate set improves over the best single expert by 9.62807369% on the 12-window KITTI sample set, with all numbers coming from server artifacts.
