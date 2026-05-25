# Review Prompt - Stage 5 S1 Regime-Stats Closure

You are reviewing Dream3R Stage 5 S1 strengthened closure evidence.

Working directory: `E:\Dream3R`
Server execution root: `/hdd3/kykt26/code/dream3r`
Server env: `conda run -n dream3r`

Read in order:

1. `CLAUDE.md`
2. `mainwork.md`
3. `cycles/CYCLE-20260525-stage5-s1-three-expert.md`
4. `decisions/DEC-20260525-002-stage5-s1-three-expert-closure.md`
5. `code/dream3r/RECENT_PROGRESS.md`
6. `code/dream3r/scripts/train_router_only.py`
7. `code/dream3r/scripts/eval_router_ablation.py`
8. `code/dream3r/tests/test_router_ablation_eval.py`

Review task:

Audit whether Stage 5 S1 is legitimately closed under the documented claim:

- Three real experts are in the candidate set: `fast3r`, `mast3r`, `spann3r`.
- Spann3R is a real oracle winner on two KITTI windows.
- The strengthened `feature_mode=regime_stats` learned router uses online regime-label `features`, not oracle metrics, as input.
- The strengthened learned router selects all three experts and matches oracle routes on the 12-window closure set.
- The reported ablation improves over the best single expert by at least 5%.
- The docs do not overclaim SOTA, cross-dataset generalization, or held-out performance.

Run these server checks:

```bash
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -m pytest \
  dream3r/tests/test_router_ablation_eval.py \
  dream3r/tests/test_router_only_training.py -q

cat /hdd3/kykt26/checkpoints/router_stage5_s1_regime_stats_v1/summary.json
cat /hdd3/kykt26/code/dream3r/runs/stage5_s1_router_ablation/results_regime_stats.json
```

Expected evidence to verify:

```text
summary.json:
feature_mode: regime_stats
feature_meta.stat_source: features
final_accuracy: 1.0
prediction_counts: fast3r=2, mast3r=8, spann3r=2

results_regime_stats.json:
learned_router: 0.1636828103
oracle_router: 0.1636828103
always_mast3r: 0.1906146836
relative_improvement_vs_best_single: 0.1412896043
learned_uses_ge_3_experts: true
stage5_s1: true
```

Return findings first, ordered by severity, with file/line references. Focus on:

- Any leakage from oracle metrics into router input.
- Any mismatch between checkpoint/eval feature dimensions or feature source.
- Any documentation overclaim.
- Any regression risk to Stage 4 router/repair behavior.
- Any missing test that would make this closure hard to reproduce.

If no blocking issue is found, say so clearly and list remaining non-blocking risks.
