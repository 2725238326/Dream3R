# DEC-20260525-002 - Stage 5 S1 Three-Expert Closure

## Decision

Close Stage 5 S1 as complete.

## Rationale

Stage 5 S1 asked whether the Composer can be extended beyond the two-expert Stage 3/4 setup into a >=3 real-expert candidate set on KITTI.

The final server ablation uses real Fast3R, MASt3R, and Spann3R pointmap metrics:

```text
expert_order: [fast3r, mast3r, spann3r]
n_sequences: 12
oracle_counts: mast3r=8, fast3r=2, spann3r=2
```

The learned router beats every single-expert baseline:

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

## Important Limitation

The final learned router does not select Spann3R:

```text
learned_expert_counts: fast3r=3, mast3r=9, spann3r=0
oracle_expert_counts: fast3r=2, mast3r=8, spann3r=2
learned_uses_ge_3_experts: false
```

This does not invalidate S1's three-candidate ablation gate, but it blocks any stronger claim that the current 6D regime-probability router has learned to exploit all useful third-expert cases.

A class-balanced diagnostic made the router select Spann3R, but reduced the best-single improvement to 3.18019488%, below the 5% threshold. The closure therefore keeps the metric-winning checkpoint and records the limitation explicitly.

## Implementation Boundary

Changed:

- `build_oracle_expert_labels.py`: supports `--experts`, including `spann3r`.
- `train_router_only.py`: builds registry from oracle `expert_order`, adds optional class-balance alpha, and adds `--disable-critic-augmentation` for pure router ablations.
- `eval_router_ablation.py`: loads arbitrary expert order and records learned/oracle expert usage counts.
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
Stage 4 regression ablation: t4_3 = true
```

Artifacts:

```text
/hdd3/kykt26/code/dream3r/runs/stage5_s1_oracle_labels/oracle_expert_labels.json
/hdd3/kykt26/checkpoints/router_stage5_s1_v1/latest.pt
/hdd3/kykt26/code/dream3r/runs/stage5_s1_router_ablation/results.json
```

## Follow-Up

The next high-value task is a richer router-feature pass: include sequence stats or evidence-derived features so the learned router can separate cases where the same regime top label maps to different oracle experts.
