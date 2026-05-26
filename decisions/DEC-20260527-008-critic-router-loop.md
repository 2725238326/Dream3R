# DEC-20260527-008 — Stage 4 ↔ Stage 5 Closed Loop (Critic → Router Feedback)

## Decision

Attempt to wire Stage 4 (Critic) into Stage 5 (Composer Router) as a
closed-loop reroute mechanism on the production cross-domain pipeline.
Per the approved plan (`.claude/plans/cheerful-snuggling-puppy.md`),
the goal was to recover seed-variance losses (seed=19 KITTI joint
LOO rel_imp = -2.00%) and turn two closed-but-disconnected stages
into a composable pipeline.

Outcome category: **partial / negative (mixed by domain)**. See
"Honest Claim" below.

## Honest Claim

> Stage 4's trained Critic does NOT generalize from its 12-sequence ×
> 2-expert training set to the Stage 5 S1 routing set
> (59 KITTI × 3 experts + 50 ETH3D × 3 experts). On the 327-entry
> per-(window, expert) cache, the trained conflict head's
> conflict_score has std=0.017 (vs the planned >0.1 gate) and picks
> the abs_rel-best expert on only 25.4% of KITTI windows
> (BELOW 33% chance). On 177+150=327 entries the trained head never
> recommends `repair_action=3 (reroute_model)`.
>
> The Critic's internal **deterministic geometric features**
> (sampson_distance, depth_inconsistency, computed without learned
> parameters) ARE informative — sampson_distance picks the
> abs_rel-best expert on **52.5% of KITTI windows** and **42% of
> ETH3D windows** (both above 33% chance). However, when used as an
> inference-time reroute heuristic on the joint v3 dense router,
> these signals do NOT improve aggregate LOO performance:
>
> | LOO (5 seeds, sampson m=0.10) | router-only | with reroute | delta |
> |---|---|---|---|
> | KITTI rel_imp mean | +2.16% ± 1.33 | +1.41% ± 1.01 | **-0.75pp** |
> | ETH3D rel_imp mean | +9.11% ± 1.64 | +6.99% ± 2.15 | **-2.12pp** |
>
> Per-seed KITTI deltas: -0.84, -0.77, -2.55, +0.12, +0.29 (worst seed=17
> drops by 2.55pp; best seeds=7,19 gain <0.3pp). Per-seed ETH3D deltas:
> -3.87, -1.50, -1.70, -3.90, +0.41 (4/5 seeds degrade by 1.5-3.9pp,
> only seed=19 marginally improves). **Plan criterion 4 FAILS** —
> no domain improved by ≥1pp on average.
>
> Reading: the Stage 5 router already extracts the routable signal
> from regime + stat features. These features (depth_mean,
> valid_ratio, depth_temporal_change, regime probability) are
> dataset-level proxies for the same scene geometry that produces
> sampson/depth_inconsistency. The geometric features carry partial
> signal (above chance, 42-52%) but lower per-window accuracy than
> the router (LOO 70-75%), so reroute overrides correct router picks
> more often than it fixes incorrect ones.

## Outcome Category

**NEGATIVE.** Per the plan's §Success Criteria "If criterion 4
produces NO improvement across all metrics, the honest outcome is
'negative: Critic signal does not transfer to Stage 5 S1 routing'
— that's still a valid closure". This closure matches DEC-007's
honesty norms.

The architectural ingredients (Critic outputs conflict_score, Router
accepts critic_confidence, RepairExecutor handles action=3 reroute)
ARE all in place. The plumbing works. The signal does not.

## Phase 0 — Backbone Sanity (PASS)

Built `scripts/phase0_backbone_sanity.py` to verify the DINOv3
backbone loads under the `small_real` preset. Result:

```text
backbone_type: dinov3_vitb16_onnx
is_loaded: true
backend: real
backbone_load_error: null
```

Critic produced non-trivial outputs on a real KITTI window (sampson
≈ 0.046, conflict_score sigmoid ≈ 0.524). Phase 0 PASS.

## Phase A — Per-(window, expert) Critic cache (BUILT)

Built two new scripts:

- `scripts/build_critic_cache.py` — KITTI 59w × 3 experts = 177
  entries. Each entry: conflict_score, repair_logits,
  geometric_consistency_log (sampson/depth/conf/covisible), abs_rel.
- `scripts/build_critic_cache_eth3d.py` — ETH3D 50w × 3 experts = 150
  entries, using dense GT from rig_scan_eval.

Caches at:

```text
/hdd3/kykt26/code/dream3r/runs/critic_cache/kitti_critic.json
/hdd3/kykt26/code/dream3r/runs/critic_cache/eth3d_critic.json
```

### Sanity gate FAILED — trained Critic conflict head

| metric | gate | KITTI | ETH3D |
|---|---|---|---|
| conflict_score_sigmoid std | > 0.1 | **0.017** | **0.038** |
| conflict-based expert-pick acc (vs 33% chance) | > 0.4 | **0.254** | (similar) |

The trained Critic (24-example training set) does NOT transfer.

### Sanity gate PASSED — geometric_log signals

| signal | KITTI std | KITTI pick acc | ETH3D std | ETH3D pick acc |
|---|---|---|---|---|
| sampson_distance | 0.086 | 0.525 | 0.101 | 0.420 |
| depth_inconsistency | 0.281 | 0.525 | 0.298 | 0.420 |
| confidence_disagreement | 0.035 | 0.492 | 0.074 | **0.280** (sub-chance) |
| covisible_inconsistency | 0.015 | 0.508 | 0.057 | **0.280** (sub-chance) |

Sampson and depth_inconsistency are the only two signals that stay
above 33% chance on both domains. They are deterministic geometric
quantities (epipolar reprojection error + temporal z-axis
inconsistency), not learned, so they cannot overfit.

## Pivot Decision

Original plan called for "Critic-augmented joint router training"
(Phase B). Pivoted to "inference-time geometric reroute" because:

1. Trained Critic conflict head does not transfer → no useful
   augmentation signal.
2. Geometric_log signals are useful in raw form (above-chance
   expert-pick accuracy) AND require no retraining.
3. Closer to the original "composable closed loop" story — the
   geometric signals come from Stage 4's deterministic core.

User approved pivot to inference-time reroute.

## Phase B — Inference-time geometric reroute on closure set

`scripts/eval_router_geometric_reroute.py` evaluates the joint v3
dense router on the 109-window closure set with the following rule:

```text
top1 = argmax(router(window))
top2 = argmax_excluding_top1(router(window))
if geo(top1) > geo(top2) + margin:
    pick top2
else:
    pick top1
```

Closure-set margin sweep (sampson_distance):

| margin | KITTI reroute_count | KITTI Δ rel_imp | ETH3D reroute_count | ETH3D Δ rel_imp |
|---|---|---|---|---|
| 0.02 | 32/59 | -4.23pp | 26/50 | -27.09pp |
| 0.05 | 32/59 | -4.23pp | 21/50 | -26.37pp |
| 0.10 | 29/59 | -3.83pp | 19/50 | -26.35pp |
| 0.15 | 28/59 | -3.65pp | 12/50 | -22.93pp |
| 0.20 | 3/59 | -2.89pp | 1/50 | -0.47pp |

All margins WORSE than router-only on closure. The router on closure
already achieves 84.75% KITTI / 96.00% ETH3D accuracy (DEC-007 v2
sparse); reroute reverts correct picks.

## Phase C — LOO 5-seed sweep with reroute

Where the router is genuinely held-out (LOO ~70% accuracy), the
geometric reroute has more room to help. Re-ran 5 seeds {7, 11, 13,
17, 19} × per-domain norm + sampson_distance + margin=0.10 via
`scripts/run_geometric_reroute_sweep.sh`.

`scripts/eval_router_joint_loo.py` extended to compute both
`predicted_metric` (router-only LOO) and `reroute_metric` (with
geometric reroute) in the same pass.

### Results (5 seeds, sampson_distance, margin=0.10)

Run: `runs/geometric_reroute_loo_sweep/` 5 LOO runs, 1h 06min on GPU 1,
30min wall clock for the sweep, all 5/5 OK.

| seed | KITTI router rel_imp | KITTI reroute rel_imp | KITTI delta | KITTI reroute_n | ETH3D router rel_imp | ETH3D reroute rel_imp | ETH3D delta | ETH3D reroute_n |
|---|---|---|---|---|---|---|---|---|
| 7  | -0.09% | +0.04% | +0.12pp | 24 | +8.03% | +4.16% | -3.87pp | 14 |
| 11 | +2.92% | +2.08% | -0.84pp | 22 | +11.45% | +9.95% | -1.50pp | 12 |
| 13 | +2.35% | +1.58% | -0.77pp | 21 | +8.28% | +6.58% | -1.70pp | 11 |
| 17 | +3.34% | +0.79% | -2.55pp | 21 | +10.16% | +6.26% | -3.90pp | 14 |
| 19 | +2.27% | +2.55% | +0.29pp | 22 | +7.60% | +8.02% | +0.41pp | 12 |
| **mean** | **+2.16% ± 1.33** | **+1.41% ± 1.01** | **-0.75pp** | 22.0 | **+9.11% ± 1.64** | **+6.99% ± 2.15** | **-2.12pp** | 12.6 |

### Specifically: did reroute recover seed=19 KITTI?

The DEC-007 seed=19 KITTI rel_imp = -2.00% number was from the joint v2
**sparse** config. The joint v3 **dense** config (used here) does not
have this pathology — its seed=19 KITTI rel_imp is +2.27% router-only.
So criterion 4b is moot in the dense baseline.

Reroute on seed=19 KITTI is essentially neutral (+0.29pp, +2.55% with
reroute). seed=19 is also the only seed where ETH3D reroute marginally
improves (+0.41pp); on the other 4 seeds ETH3D degrades by 1.5-3.9pp.

### Route accuracy regression test (above-chance gate)

All 5 seeds × 2 domains stay well above 33% chance (router-only LOO):

```text
seed=7  | K=72.88% E=66%
seed=11 | K=71.19% E=72%
seed=13 | K=74.58% E=68%
seed=17 | K=69.49% E=66%
seed=19 | K=72.88% E=70%
```

No reroute-induced regression below chance.

## Server Artifacts

```text
# Critic caches
/hdd3/kykt26/code/dream3r/runs/critic_cache/kitti_critic.json     (177 entries, 59 seqs × 3 experts)
/hdd3/kykt26/code/dream3r/runs/critic_cache/eth3d_critic.json     (150 entries, 50 seqs × 3 experts)

# Closure-set reroute sweep
/hdd3/kykt26/code/dream3r/runs/geometric_reroute/joint_v3_dense_sampson_m*/results.json

# LOO reroute sweep (5 seeds)
/hdd3/kykt26/code/dream3r/runs/geometric_reroute_loo_sweep/joint_v3_dense_sampson_m0.10_s{7,11,13,17,19}/results_loo.json
/hdd3/kykt26/code/dream3r/runs/geometric_reroute_loo_sweep/progress.log
```

## New Code Files

```text
code/dream3r/scripts/phase0_backbone_sanity.py            (new, ~110 lines)
code/dream3r/scripts/build_critic_cache.py                (new, ~220 lines)
code/dream3r/scripts/build_critic_cache_eth3d.py          (new, ~200 lines)
code/dream3r/scripts/eval_router_geometric_reroute.py     (new, ~240 lines)
code/dream3r/scripts/run_geometric_reroute_sweep.sh       (new, ~55 lines)
code/dream3r/scripts/eval_router_joint_loo.py             (modified: added 4 reroute fields + CLI flags)
```

## Files NOT Modified (per CLAUDE.md)

- `code/dream3r/model.py`, `anchor_bank.py`, `nsa_attention.py`,
  `bus.py`, `orchestrator.py`, `repair.py` — sacred v0.3/v0.5 core.
- `code/dream3r/modules.py` — Critic and ComposerRouter class
  definitions unchanged.
- KITTI 59w oracle, ETH3D dense oracle, regime labels, all router
  checkpoints — preserved as baselines.

## Limitations

- Critic was trained on only 24 examples (12 seq × 2 experts), with
  spann3r absent. Retraining a Critic on 327 examples might
  generalize better but was deferred (out of scope for this DEC).
- Geometric features are correct on 52% (KITTI) / 42% (ETH3D) of
  windows; the joint v3 router is correct on 73% (KITTI LOO) / 51%
  (ETH3D LOO) per DEC-007 addendum 3. The geometric signal has lower
  per-window accuracy than the router on the windows we care about.
- No demo update (Phase D demo was contingent on Phase C showing a
  meaningful improvement).
- No new dataset, no v0.3/v0.5 core edit, no SOTA claim.

## Out of Scope (not pursued)

1. Critic retrain on 59-seq KITTI + 50-seq ETH3D (would need new
   training data builder for both domains; ~1.5 day effort).
2. Geometric features as router INPUT (per-window per-expert feature
   integration into ComposerRouter; complex architecture change).
3. Conditional reroute (only reroute when router's logit gap is
   small) — would need second-pass calibration sweep.

These remain candidates for a future closure if the user wants to
pursue Stage 4↔Stage 5 integration further.

## Conclusion

The Stage 4 ↔ Stage 5 closed loop was attempted end-to-end and
**fails to improve cross-domain routing held-out performance** at this
architectural scale (joint v3 dense router, 109 windows, 3 experts).
Two distinct sub-findings explain why:

1. **Stage 4's trained Critic does not transfer** beyond its
   24-example training set. 0.834 conflict↔abs_rel correlation on
   Stage 4's own training set drops to 25.4% expert-pick accuracy
   (below 33% chance) on Stage 5's broader 109-window cross-domain
   set. The Critic head saturates near 0.55 sigmoid and never
   recommends `repair_action=3 (reroute_model)` across 327 entries.
2. **The geometric features that drive Critic geometry are
   informative but redundant** with the Stage 5 router's
   regime+stat input. Sampson distance picks the best expert 52%
   (KITTI) / 42% (ETH3D) — above chance, but below the router's
   ~70% LOO accuracy. Using them as inference-time reroute reverts
   correct router picks more often than it fixes incorrect ones.

The wiring works. The signal does not. Stage 5 router on joint v3
dense already extracts the available routable signal at this data
scale; closing the loop with the existing Critic does not add value.

This is a negative architectural finding, not a wiring bug. Future
trigger conditions for revisiting:

- **Critic retrain on Stage 5 windows (327 examples × 3 experts)**:
  would address Finding #1; might shift conflict_score variance to
  match the data; ~1.5 day effort.
- **Geometric features as router INPUT** (per-window per-expert):
  rather than reroute heuristic, fold geometry into router training
  so it learns when to trust regime vs geometry. Requires non-trivial
  architecture change.
- **Different ablation set**: the joint v3 dense router is already
  near oracle on closure; reroute has more room on harder
  out-of-distribution windows (e.g., a third dataset).

DEC-007's "joint v3 dense router" remains the recommended cross-domain
router. No regressions to existing baselines.
