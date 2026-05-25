# DEC-20260525-002 - Stage 5 S1 Three-Expert Closure

## Decision

Close Stage 5 S1 as complete, with the `regime_stats/features` router ablation
as the strengthened closure result.

## Rationale

Stage 5 S1 asked whether the Composer can be extended beyond the two-expert Stage 3/4 setup into a >=3 real-expert candidate set on KITTI.

The final server ablation uses real Fast3R, MASt3R, and Spann3R pointmap metrics:

```text
expert_order: [fast3r, mast3r, spann3r]
n_sequences: 12
oracle_counts: mast3r=8, fast3r=2, spann3r=2
```

The first learned router beats every single-expert baseline:

```text
learned_router: 0.1722621613
always_mast3r: 0.1906146836
always_fast3r: 0.2252575532
always_spann3r: 0.2086918801
oracle_router: 0.1636828103
relative_improvement_vs_best_single: 0.0962807369
stage5_s1: true
```

This is a real three-candidate Composer ablation, and the oracle proves Spann3R is not a dead adapter: it is the best real expert on two KITTI windows.

The strengthened router-only ablation adds online regime-label `features`
(`frame_count`, `depth_mean`, `valid_ratio`, `depth_temporal_change`,
`oxts_available`, `mean_speed`, `speed_std`) to the router input without using
oracle metrics as features. It matches the oracle routes on the closure set:

```text
feature_mode: regime_stats
stat_source: features
learned_router: 0.1636828103
oracle_router: 0.1636828103
always_mast3r: 0.1906146836
always_fast3r: 0.2252575532
always_spann3r: 0.2086918801
relative_improvement_vs_best_single: 0.1412896043
learned_expert_counts: fast3r=2, mast3r=8, spann3r=2
learned_uses_ge_3_experts: true
stage5_s1: true
```

## Important Limitation

The original 6D regime-probability-only router did not select Spann3R:

```text
learned_expert_counts: fast3r=3, mast3r=9, spann3r=0
oracle_expert_counts: fast3r=2, mast3r=8, spann3r=2
learned_uses_ge_3_experts: false
```

This does not invalidate S1's three-candidate ablation gate. It records why the
feature-augmented router is the strengthened result and why the 6D-only router
should remain a diagnostic baseline.

A class-balanced diagnostic made the router select Spann3R, but reduced the best-single improvement to 3.18019488%, below the 5% threshold. The closure therefore keeps the metric-winning checkpoint and records the limitation explicitly.

The strengthened result is still a 12-window KITTI closure ablation, not a SOTA
claim, a held-out generalization result, or a cross-dataset result.

## Implementation Boundary

Changed:

- `build_oracle_expert_labels.py`: supports `--experts`, including `spann3r`.
- `train_router_only.py`: builds registry from oracle `expert_order`, adds optional class-balance alpha, adds `--disable-critic-augmentation` for pure router ablations, and supports `feature_mode=regime_stats` from regime-label `stats`/`features`.
- `eval_router_ablation.py`: loads arbitrary expert order, records learned/oracle expert usage counts, and evaluates the same feature mode.
- `test_oracle_expert_labels.py`, `test_router_ablation_eval.py`: cover Stage 5 three-expert schema behavior.

Not changed:

- `model.py`
- `anchor_bank.py`
- `nsa_attention.py`
- `bus.py`

## Verification

Server:

```text
Spann3R integration: 2 passed, 8 warnings
Focused router/oracle tests: 10 passed, 1 warning
Focused feature-mode tests: 5 passed
Stage 4 regression ablation: t4_3 = true
```

Artifacts:

```text
/hdd3/kykt26/code/dream3r/runs/stage5_s1_oracle_labels/oracle_expert_labels.json
/hdd3/kykt26/checkpoints/router_stage5_s1_v1/latest.pt
/hdd3/kykt26/code/dream3r/runs/stage5_s1_router_ablation/results.json
/hdd3/kykt26/checkpoints/router_stage5_s1_regime_stats_v1/latest.pt
/hdd3/kykt26/code/dream3r/runs/stage5_s1_router_ablation/results_regime_stats.json
```

## Follow-Up

The next high-value task is independent review of the strengthened closure,
then either a real-data ablation table or the next Stage 5 stretch item with
fresh server evidence.
