# DEC-20260525-003 - Stage 5 S1 KITTI Expansion Closure

## Decision

Promote the Stage 5 S1 closure evidence from the 12-window oracle to the
59-window oracle. The 12-window result stays as a smaller-N reference point;
the 59-window result is the new headline evidence.

## Rationale

Stage 5 S1 asks whether the Composer can be extended to a >=3 real-expert
candidate set on KITTI and whether the learned router beats single-expert
baselines.

On the original 12-window oracle the closure passed but LOO showed
chance-level held-out route accuracy (33%), so the 14.13% closure-set gain
was largely training-set memorization rather than a generalizable routing
policy. To probe whether the router actually learns at larger N, we
re-built the oracle with `--max-per-regime 25`, getting 59 windows across 4
KITTI regimes (outdoor_static 25, dense_sequential 25, sparse_view 6,
dynamic_scene 3).

Closure-set ablation on the 59-window oracle:

```text
expert_order: [fast3r, mast3r, spann3r]
n_sequences: 59
oracle_counts:    mast3r=31, spann3r=24, fast3r=4
prediction_counts: mast3r=31, spann3r=24, fast3r=4
learned_router: 0.1485612884
oracle_router:  0.1481787252
always_mast3r:  0.1607782668  (best single)
relative_improvement_vs_best_single: 0.0759865040   # 7.60%, passes 5% gate
route_regime_cramers_v: 0.4717845326
stage5_s1: true
```

Held-out leave-one-out cross-validation (59 folds, each fold retrains on
58 remaining windows with frozen normalization stats and predicts the
held-out expert):

```text
learned_loo_mean: 0.1571985500
oracle_loo_mean:  0.1481787252
always_mast3r:    0.1607782668
relative_improvement_vs_best_single: 0.0222649297   # 2.23%, below 5% gate
loo_route_accuracy_vs_oracle: 0.7796610169          # 46/59 held-out routes correct
learned_loo_expert_counts: fast3r=6, mast3r=26, spann3r=27
oracle_expert_counts:      fast3r=4, mast3r=31, spann3r=24
```

Reading:

- The 78% held-out route accuracy (vs 33% chance for 3-class) is strong
  evidence that the router learns a real, generalizable routing policy on
  KITTI in-domain at N=59. The 12-window LOO chance-level result was an
  N-too-small artefact.
- The 2.23% held-out abs_rel margin is modest because MASt3R and Spann3R are
  close to each other on outdoor_static KITTI. Total oracle headroom over
  best single expert is `(0.1608 - 0.1482) / 0.1608 = 7.86%`; LOO captures
  2.23% / 7.86% = 28% of that ceiling held-out.

## Honest Claim Set

What is supported:

- Three real experts (Fast3R, MASt3R, Spann3R) are in the candidate set.
- All three are oracle winners on real KITTI windows (Fast3R on 4, MASt3R on
  31, Spann3R on 24 of 59 windows).
- The strengthened `regime_stats` learned router matches the oracle expert
  distribution exactly on the 59-window closure set and improves over the
  best single expert by 7.60% (passes the 5% gate).
- Held-out 59-fold LOO predicts the oracle expert on 78% of held-out
  windows, well above 33% chance for 3-class routing.

What is NOT supported and must not be claimed:

- SOTA or cross-dataset generalization.
- Held-out abs_rel improvement >= 5% over best single expert. The held-out
  margin is 2.23% because the two best experts are close on most windows.
- Generalization beyond KITTI in-domain.

## Important Limitation

The 12-window oracle distribution {mast3r=8, fast3r=2, spann3r=2} was a
biased snapshot dominated by mast3r-winning windows. The 59-window oracle
distribution {mast3r=31, spann3r=24, fast3r=4} is much more balanced and
shows that Spann3R is competitive on a large fraction of KITTI outdoor
scenes, not just two isolated windows.

KITTI raw data has near-zero coverage of `indoor_static` and
`feed_forward_manyview` regimes; further KITTI-only expansion would not
broaden regime support beyond `{outdoor_static, dense_sequential,
sparse_view, dynamic_scene}`.

## Implementation Boundary

Touched in this decision: only re-ran existing scripts with `--max-per-regime
25`. No source code changed in this cycle.

Previously closed code-hygiene fixes (DEC-20260525-002 follow-up) are still
in effect: `_feature_tensor` accepts `frozen_stats`,
`evaluate_router_ablation` consumes ckpt frozen stats, `_load_router`
validates `feature_mode` compatibility. Re-verified by the strengthened
closure reproduction in CYCLE-20260525-stage5-s1-three-expert.md.

## Verification

Server artifacts (all from this cycle):

```text
/hdd3/kykt26/code/dream3r/runs/stage5_s1_expand_oracle/oracle_expert_labels.json
/hdd3/kykt26/checkpoints/router_stage5_s1_expand_v1/latest.pt
/hdd3/kykt26/code/dream3r/runs/stage5_s1_expand_router_ablation/results.json
/hdd3/kykt26/code/dream3r/runs/stage5_s1_expand_router_loo/results_loo.json
```

Stage 4 repair pipeline regression: unaffected (no change to its router
loader interface beyond the `_load_router` tuple unpack already covered by
DEC-20260525-002 follow-up).

## Follow-Up

Recommended next stretch options, in order:

1. ETH3D second dataset (server-side download). This is the right next step
   to convert "router learns in-domain on KITTI" into a cross-dataset
   claim. User has authorized server-side dataset downloads.
2. Permanence real signal (S2): still blocked on dynamic data; KITTI
   tracking subset or Waymo would be required. Lower priority.
3. CUT3R or VGGT as a fourth real expert (S1 extension): adapter and
   capability card already present; checkpoint download requires user
   authorization.

The Stage 5 S1 expanded result is sufficient to close S1 as a Composer
multi-expert ablation milestone. Any "router learns useful routing" claim
in papers or presentations must cite the 78% held-out route accuracy, not
the 7.60% closure-set abs_rel improvement.
