# CYCLE 20260527 Critic↔Router Closed Loop

## Scope

Wire Stage 4 (Critic + Repair) into Stage 5 (Composer Router) as an
inference-time closed loop on the production cross-domain pipeline
(joint v3 dense router, KITTI 59w + ETH3D 50w). Per the approved
plan, the goal was to recover seed-variance losses (seed=19 KITTI
joint LOO rel_imp = -2.00%) and unify two closed-but-disconnected
stages.

Triggers (per DEC-007 / mainwork.md §7): user-driven follow-up,
"推进方向 = Stage 4↛Stage 5 闭环（推荐）".

## Code Boundary

Only `code/dream3r/scripts/` touched. v0.3/v0.5 core
(`model.py`, `anchor_bank.py`, `nsa_attention.py`, `bus.py`,
`orchestrator.py`, `repair.py`, `modules.py`) unchanged.

New scripts (4):

- `phase0_backbone_sanity.py` — verify DINOv3 backbone is real.
- `build_critic_cache.py` — per-(KITTI window, expert) Critic forward + cache.
- `build_critic_cache_eth3d.py` — same for ETH3D dense GT.
- `eval_router_geometric_reroute.py` — closure-set reroute eval.
- `run_geometric_reroute_sweep.sh` — 5-seed LOO orchestrator.

Modified (1):

- `eval_router_joint_loo.py` — added optional `--kitti-critic-cache`,
  `--eth3d-critic-cache`, `--geometric-signal`, `--reroute-margin`
  flags; computes `reroute_metric` alongside `predicted_metric` in
  every fold; backward-compatible (default off, results unchanged
  without cache).

## Phase 0 — Backbone Sanity (PASS)

Built and ran `phase0_backbone_sanity.py` with the `small_real` preset.

```text
backbone_type: dinov3_vitb16_onnx
is_loaded: true
backend: real
sampson_distance: 0.046 (one KITTI window probe)
```

Phase 0 PASS — proceeded to Phase A.

## Phase A — Per-(window, expert) Critic cache

KITTI: 59w × 3 experts = 177 entries built in 44s on GPU 1.
ETH3D: 50w × 3 experts = 150 entries built in similar time with dense GT.

Per (window, expert) we cached:

- `abs_rel` (sanity check against existing oracle)
- `conflict_score_raw` and `conflict_score_sigmoid` from trained Critic
- `repair_logits` (6-way)
- `recommended_action_raw` (argmax of repair_logits)
- `geometric_log` dict: sampson_distance, depth_inconsistency,
  confidence_disagreement, covisible_inconsistency

### KEY FINDING #1 — Trained Critic does NOT generalize

| metric | gate | KITTI | ETH3D |
|---|---|---|---|
| conflict_score_sigmoid std | > 0.1 (plan gate) | **0.017** ✗ | **0.038** ✗ |
| conflict-based expert-pick accuracy | > 33% chance | **25.4%** ✗ | (similar) |
| recommended_action_raw count for "reroute_model"(action=3) | >0 | **0/177** | 0/150 |

The trained Critic was fit on 24 examples (12 KITTI sequences × 2
experts) and does NOT extend to the broader 59 + 50 seq × 3 expert
set. Its conflict head saturates around 0.55 (sigmoid) and never
recommends reroute on the new windows. spann3r was entirely absent
from training.

### KEY FINDING #2 — Critic's deterministic geometric features DO carry signal

| signal | KITTI std | KITTI pick acc | ETH3D std | ETH3D pick acc |
|---|---|---|---|---|
| sampson_distance | 0.086 | **0.525** ✓ | 0.101 | **0.420** ✓ |
| depth_inconsistency | 0.281 | **0.525** ✓ | 0.298 | **0.420** ✓ |
| confidence_disagreement | 0.035 | 0.492 ✓ | 0.074 | 0.280 ✗ |
| covisible_inconsistency | 0.015 | 0.508 ✓ | 0.057 | 0.280 ✗ |

`sampson_distance` and `depth_inconsistency` are the two signals
that stay above 33% chance on both domains. They are computed
deterministically by `Critic.compute_geometric_consistency` — no
learned parameters, no risk of overfitting to a small training set.

## Pivot Decision

Original plan B was "train Critic-augmented router". Given Finding #1,
this would mean training a router against signals that don't transfer
— pure noise. User approved pivot to "use deterministic geometric
features as inference-time reroute heuristic" (no training).

## Phase B — Closure-set geometric reroute

`eval_router_geometric_reroute.py` evaluates the joint v3 dense
router on all 109 windows: load top-1 and top-2 picks, look up
sampson(top-1) and sampson(top-2); if `sampson(top-1) > sampson(top-2)
+ margin`, reroute to top-2.

Margin sweep on closure set:

| margin | KITTI Δ rel_imp | ETH3D Δ rel_imp | reroute fired |
|---|---|---|---|
| 0.02 | -4.23pp | -27.09pp | 32+26 |
| 0.05 | -4.23pp | -26.37pp | 32+21 |
| 0.10 | -3.83pp | -26.35pp | 29+19 |
| 0.15 | -3.65pp | -22.93pp | 28+12 |
| 0.20 | -2.89pp | -0.47pp | 3+1 |

ALL margins make closure performance worse. Reading: on the closure
set the joint v3 router is already at 84.75% (KITTI) / 96.00% (ETH3D)
accuracy. Reroute overrides correct picks more often than it fixes
incorrect ones.

## Phase C — LOO 5-seed sweep with reroute

LOO is the real held-out test where router accuracy drops to ~70%
and reroute has more room to help. Extended `eval_router_joint_loo.py`
to compute `reroute_metric` alongside `predicted_metric` in every
fold. Ran 5 seeds {7, 11, 13, 17, 19} × per-domain norm +
sampson_distance + margin=0.10.

### Results (5 seeds, sampson_distance, margin=0.10)

5 LOO runs, 30min wall on GPU 1, all OK
(`runs/geometric_reroute_loo_sweep/progress.log`):

| seed | KITTI router | KITTI reroute | KITTI Δ | reroute_n | ETH3D router | ETH3D reroute | ETH3D Δ | reroute_n |
|---|---|---|---|---|---|---|---|---|
| 7  | -0.09% | +0.04% | +0.12pp | 24 | +8.03% | +4.16% | -3.87pp | 14 |
| 11 | +2.92% | +2.08% | -0.84pp | 22 | +11.45% | +9.95% | -1.50pp | 12 |
| 13 | +2.35% | +1.58% | -0.77pp | 21 | +8.28% | +6.58% | -1.70pp | 11 |
| 17 | +3.34% | +0.79% | -2.55pp | 21 | +10.16% | +6.26% | -3.90pp | 14 |
| 19 | +2.27% | +2.55% | +0.29pp | 22 | +7.60% | +8.02% | +0.41pp | 12 |
| **mean** | **+2.16% ± 1.33** | **+1.41% ± 1.01** | **-0.75pp** | 22.0 | **+9.11% ± 1.64** | **+6.99% ± 2.15** | **-2.12pp** | 12.6 |

### Seed=19 KITTI specifically

The DEC-007 seed=19 KITTI rel_imp = -2.00% was the joint v2 **sparse**
config. Joint v3 **dense** baseline used here has seed=19 KITTI
rel_imp = +2.27% (no pathology). Reroute moves it to +2.55%
(+0.29pp), so criterion 4b is moot — the dense baseline doesn't have
the failure mode that the plan targeted.

## Reading

The geometric reroute heuristic **fails on both domains in mean** at
margin=0.10:

- KITTI: 1/5 seeds gain (+0.12 to +0.29pp), 4/5 lose (-0.77 to -2.55pp).
  Mean delta -0.75pp.
- ETH3D: 1/5 seeds marginally gain (+0.41pp on seed=19), 4/5 lose
  (-1.50 to -3.90pp). Mean delta -2.12pp.

Crucially, the **router-only baseline is already strong**: KITTI mean
+2.16%, ETH3D mean +9.11% rel_imp on 5-seed LOO. The joint v3 dense
router extracts most of the routable signal from regime+stat inputs.
Sampson distance's 52% (KITTI) / 42% (ETH3D) per-window accuracy is
lower than the router's ~70-75% LOO accuracy; on the residuals where
the router is wrong, sampson is only slightly better than chance, so
reroute frequently overrides correct picks.

This is a real architectural finding: at the current data scale and
architectural choice (handcrafted 12D input), the Stage 5 router has
already saturated the available routable signal; Stage 4 closed-loop
augmentation does not add value.

## Server Artifacts

```text
# Critic caches (Phase A)
/hdd3/kykt26/code/dream3r/runs/critic_cache/kitti_critic.json
/hdd3/kykt26/code/dream3r/runs/critic_cache/eth3d_critic.json

# Closure-set reroute sweep (Phase B)
/hdd3/kykt26/code/dream3r/runs/geometric_reroute/joint_v3_dense_sampson_m{0.02,0.05,0.10,0.15,0.20}/results.json

# LOO reroute sweep (Phase C)
/hdd3/kykt26/code/dream3r/runs/geometric_reroute_loo_sweep/joint_v3_dense_sampson_m0.10_s{7,11,13,17,19}/results_loo.json
/hdd3/kykt26/code/dream3r/runs/geometric_reroute_loo_sweep/progress.log
```

## What This Changes

- DEC-007's "router 78% LOO route accuracy" story is unchanged.
- Adds a closed-loop attempt that surfaces the limits of:
  (a) the 24-example Critic's generalization (DOES NOT)
  (b) the geometric features as router refinement (LIMITED)
- DEC-008 records the honest claim and points forward to
  Critic retraining as a future-work trigger.

## Boundary

Not touched:

- v0.3/v0.5 core
- KITTI/ETH3D oracles and regime labels
- joint v3 dense router checkpoint (reused as-is)
- All Stage 4 closure artifacts (`stage4_*`)
- All DEC-007 documentation

## Conclusion

NEGATIVE outcome (matches DEC-007 honesty norms; plan §goal explicitly
allowed this).

The Stage 4 ↔ Stage 5 closed loop has been **attempted end-to-end and
does not improve cross-domain routing** at the current architectural
scale:

- The trained Critic (24-example training set) does NOT transfer to
  Stage 5's 109-window cross-domain set; conflict head saturates near
  0.55 sigmoid, picks below chance, never recommends action 3.
- The Critic's deterministic geometric features (sampson,
  depth_inconsistency) ARE informative individually (52% / 42%
  expert-pick accuracy) but redundant with the regime+stat features
  the router already consumes.
- 5-seed LOO sweep shows reroute degrades mean rel_imp by 0.75pp
  (KITTI) and 2.12pp (ETH3D); plan criterion 4 FAILS.

What this DEC closes:

- Wiring infrastructure proves the closed loop CAN be assembled
  without v0.3/v0.5 core edits.
- Critic transfer limitation surfaced (Finding #1) — this informs
  future Critic retrain decisions.
- Geometric-vs-router redundancy quantified (Finding #2) — this
  informs whether future architectural changes should add raw
  geometry as router INPUT (rather than reroute).

Trigger conditions for revisit are listed in DEC-20260527-008
§Out of Scope.
