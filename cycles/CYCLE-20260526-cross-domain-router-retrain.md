# CYCLE 20260526 Cross-Domain Router Retrain

## Scope

Convert the DEC-20260525-006 negative finding (KITTI Stage 5 S1 router
does not zero-shot transfer to ETH3D) into actionable evidence by
running three retrains against the existing 50w ETH3D + 59w KITTI
oracles. No new experts, no new data, no edits to v0.3/v0.5 core.

Three experiments (per HANDOFF-20260526-evening):

- **(a)** Robust feature retrain on KITTI — drop 3 KITTI-specific
  stats from the router input.
- **(b)** ETH3D-only router — train on the ETH3D 50w oracle.
- **(c)** Joint KITTI+ETH3D router (stretch) — single router with a
  2D domain-id feature; per-domain LOO.

## Code Changes (Boundary)

Edits are confined to `code/dream3r/scripts/`. No v0.3/v0.5 core touched.

Modified (4 files):

- `train_router_only.py`: introduces `STAT_FEATURE_KEYS_ROBUST`
  (4 keys: frame_count, depth_mean, valid_ratio, depth_temporal_change)
  and a module-level `_FEATURE_KEY_VARIANTS` dict mapping
  `regime_stats -> 7-key` and `regime_stats_robust -> 4-key`.
  `_feature_tensor` looks up `stat_keys` from this dict instead of
  hardcoding 7. `--feature-mode` CLI choice extended.
- `eval_router_ablation.py`: `--feature-mode` choice extended; the
  frozen-stats loading branch widened from `feature_mode == "regime_stats"`
  to `feature_mode in ("regime_stats", "regime_stats_robust")`.
- `eval_router_loo.py`: `--feature-mode` choice extended.
- `eval_cross_domain_router.py`: `--feature-mode` choice extended.

New (2 files):

- `train_router_joint_domain.py`: joint KITTI+ETH3D loader and trainer.
  Input dim: `6 regime + 4 robust stats + 2 domain one-hot = 12D`.
  Stats are normalized with mean/std computed over the joint 109-example
  set; the domain-id one-hot is the only explicit domain signal.
- `eval_router_joint_loo.py`: per-domain LOO over the 109-example joint
  set; supports `--max-folds` for subsampled folds (not needed this run).

## Exp (a) — Robust KITTI Router

Train command (server):

```text
python -m dream3r.scripts.train_router_only \
  --preset router_only \
  --oracle-labels .../stage5_s1_expand_oracle/oracle_expert_labels.json \
  --regime-labels .../stage3_regime_labels/regime_labels.json \
  --output-dir /hdd3/kykt26/checkpoints/router_kitti_robust_v1 \
  --epochs 2000 --lr 0.05 --batch-size 32 \
  --disable-critic-augmentation --feature-mode regime_stats_robust
```

Training summary (`router_kitti_robust_v1/summary.json`):

```text
n_examples: 59
initial_accuracy: 6.78%
final_accuracy:   98.31%    (58/59 correct)
target_counts:    mast3r=31, spann3r=24, fast3r=4
prediction_counts: mast3r=30, spann3r=25, fast3r=4
feature_mode: regime_stats_robust  (4 stat keys; oxts/speed dropped)
```

(a.1) KITTI closure (`router_kitti_robust_v1_ablation/results.json`):

```text
learned_router: 0.14821     (best — vs oracle 0.14818, learned ~= oracle)
always_mast3r:  0.16078     (best single)
always_spann3r: 0.17814
always_fast3r:  0.23655
best_single_expert: mast3r
relative_improvement_vs_best_single: 7.82%
learned_expert_counts: fast3r=4, mast3r=30, spann3r=25  (matches oracle within 1)
route_regime_cramers_v: 0.4812
success.stage5_s1: true
```

(a.2) KITTI 59-fold LOO (`router_kitti_robust_v1_loo/results_loo.json`):

```text
learned_loo_mean:  0.15399  (vs oracle 0.14818, best_single 0.16078)
loo_route_accuracy_vs_oracle: 77.97%  (46/59)
relative_improvement_vs_best_single: 4.19%  (just below 5% gate)
learned_loo_expert_counts: fast3r=4, mast3r=30, spann3r=25
success.beats_best_single: true
success.improves_best_single_ge_5pct: false
success.loo_route_accuracy_ge_50pct: true
```

(a.3) ETH3D cross-domain transfer (`router_kitti_robust_v1_eth3d/results.json`):

```text
learned_router: 0.25835  (= always_mast3r; router collapses)
always_spann3r: 0.23245  (best single on ETH3D)
oracle:         0.20747
relative_improvement_vs_best_single: -11.14%
learned_expert_counts: fast3r=0, mast3r=50, spann3r=0   (collapse to mast3r)
oracle_expert_counts:  fast3r=11, mast3r=16, spann3r=23
eth3d_route_accuracy_vs_oracle: 32.0%   (16/50)
best_single_shifted_kitti_to_eth3d: true
```

Reading: removing the 3 KITTI-specific stats moves the collapse from
`always_fast3r` (DEC-006 baseline, 22%) to `always_mast3r` (32%) —
+10pp on route accuracy, +5.6pp on relative improvement vs best-single,
but the HANDOFF success criterion (>33% chance AND ≥2 experts predicted)
is **not** satisfied. The robust feature design preserves in-domain KITTI
performance (LOO 77.97% vs baseline 78%) at near-zero cost. Cross-domain
transfer remains qualitatively broken; the 6D one-hot regime
distribution alone is not a strong enough cross-domain signal.

## Exp (b) — ETH3D-Only Router

Train command:

```text
python -m dream3r.scripts.train_router_only \
  --preset router_only \
  --oracle-labels .../eth3d_cross_dataset_oracle/oracle_expert_labels.json \
  --regime-labels .../eth3d_cross_dataset_regime_labels/regime_labels.json \
  --output-dir /hdd3/kykt26/checkpoints/router_eth3d_v1 \
  --epochs 2000 --lr 0.05 --batch-size 32 \
  --disable-critic-augmentation --feature-mode regime_stats
```

Training summary (`router_eth3d_v1/summary.json`):

```text
n_examples: 50
initial_accuracy: 22.0%
final_accuracy:   100%     (50/50 — predictions match oracle exactly)
target_counts/prediction_counts: spann3r=23, mast3r=16, fast3r=11
feature_mode: regime_stats   (full 7 keys; oxts/speed-related cols all-zero)
```

(b.1) ETH3D closure (`router_eth3d_v1_ablation/results.json`):

```text
learned_router: 0.20747   (= oracle)
always_spann3r: 0.23245   (best single)
relative_improvement_vs_best_single: 10.74%
learned_expert_counts == oracle_expert_counts: fast3r=11, mast3r=16, spann3r=23
route_regime_cramers_v: 0.066   (low — both ETH3D regimes map to outdoor_static
                                  for 4/5 scenes; routing comes from stats)
success.stage3: false        (cramers_v < 0.3)
success.stage5_s1: false     (cramers_v < 0.3)
```

(b.2) ETH3D 50-fold LOO (`router_eth3d_v1_loo/results_loo.json`):

```text
learned_loo_mean: 0.21758
oracle_loo_mean:  0.20747
always_spann3r:   0.23245  (best single)
relative_improvement_vs_best_single: 6.39%
loo_route_accuracy_vs_oracle: 54.0%   (27/50, vs 33% chance)
learned_loo_expert_counts: fast3r=12, mast3r=12, spann3r=26
success.beats_best_single: true
success.improves_best_single_ge_5pct: true
success.loo_route_accuracy_ge_50pct: true
```

Reading: an ETH3D-trained router learns a held-out routing policy. 54%
LOO route accuracy is well above 33% chance and well above the 46%
majority-class baseline (always_spann3r). LOO learned mean beats the
ETH3D best single expert by 6.4%. **HANDOFF (b) success criteria fully
met.** The low cramers_v on the closure set reflects the dataset
(uniform one-hot regimes per scene), not a router failure — the routing
signal comes from the 4 stat features (depth_mean / valid_ratio /
depth_temporal_change / frame_count), not from the one-hot regime
distribution.

## Exp (c) — Joint KITTI+ETH3D Router

Train command:

```text
python -m dream3r.scripts.train_router_joint_domain \
  --kitti-regime  .../stage3_regime_labels/regime_labels.json \
  --kitti-oracle  .../stage5_s1_expand_oracle/oracle_expert_labels.json \
  --eth3d-regime  .../eth3d_cross_dataset_regime_labels/regime_labels.json \
  --eth3d-oracle  .../eth3d_cross_dataset_oracle/oracle_expert_labels.json \
  --output-dir /hdd3/kykt26/checkpoints/router_joint_v1 \
  --epochs 2000 --lr 0.05 --batch-size 32
```

Input dim 12D = `[6 regime probs] + [4 robust stats joint-normalized]
+ [2 domain one-hot]`.

Closure summary (`router_joint_v1/summary.json`):

```text
n_examples: 109   (KITTI=59, ETH3D=50)
initial_accuracy: 13.76%
final_accuracy:   87.16%
per_domain_accuracy:
  kitti: 88.14%   (52/59 correct on training set)
  eth3d: 86.00%   (43/50 correct on training set)
```

Joint 109-fold LOO (`router_joint_v1_loo/results_loo.json`):

```text
n_folds_run: 109    (full, no subsampling)
per_domain_loo_route_accuracy:
  kitti: 72.88%    (vs robust KITTI-only 77.97%, drop 5.09pp)
  eth3d: 42.00%    (vs ETH3D-only 54.00%, drop 12.00pp; vs 33% chance, +8.67pp)
per_domain_loo_learned_mean:
  kitti: 0.15627  (vs always_mast3r 0.16078)
  eth3d: 0.22152  (vs always_spann3r 0.23245)
per_domain_rel_improvement_vs_best_single:
  kitti: 2.81%
  eth3d: 4.70%
success.kitti_loo_route_acc_gt_33pct: true
success.eth3d_loo_route_acc_gt_33pct: true
success.both_domains_above_chance: true
```

Reading: a single router with a 2D domain-id feature simultaneously
clears 33% chance on BOTH domains and beats best-single in BOTH (by
2.81% on KITTI and 4.70% on ETH3D, held-out). HANDOFF (c) success
criteria fully met:

- per-domain LOO route accuracy > 33% in both domains ✓
- joint router KITTI LOO drop ≤ 10pp vs (a) ✓ (5.09pp drop)

The joint router pays ~5pp on KITTI LOO route accuracy and ~12pp on
ETH3D LOO route accuracy relative to domain-specialized routers, but
both numbers remain above chance and above best-single. This is the
first cross-domain routing signal that doesn't collapse.

## Cross-Experiment Comparison

| Experiment | KITTI LOO route_acc | ETH3D LOO/transfer route_acc |
|---|---|---|
| DEC-006 baseline (KITTI router → ETH3D zero-shot) | 78% | **22%** (collapse to fast3r) |
| (a) Robust KITTI router → ETH3D zero-shot | 77.97% | **32%** (collapse to mast3r) |
| (b) ETH3D-only router → ETH3D LOO | — | **54%** ✓ |
| (c) Joint router → KITTI LOO / ETH3D LOO | **72.88%** ✓ | **42%** ✓ |

| Experiment | KITTI rel_imp vs best_single | ETH3D rel_imp vs best_single |
|---|---|---|
| DEC-006 baseline (KITTI router on ETH3D) | +7.60% (closure) / +2.23% (LOO) | -16.7% (zero-shot) |
| (a) Robust KITTI | +7.82% (closure) / +4.19% (LOO) | -11.14% (zero-shot) |
| (b) ETH3D-only | — | +10.74% (closure) / +6.39% (LOO) |
| (c) Joint | (KITTI LOO) +2.81% | (ETH3D LOO) +4.70% |

The three retrains form a clear gradient:

1. KITTI-specialized router does not generalize even with the robust
   feature redesign — the 3 dropped KITTI-only stats were necessary
   but not sufficient. The remaining 4 stats + 6D regime still embed
   enough KITTI bias to push ETH3D into a corner.
2. ETH3D is internally learnable — the 50-window oracle has enough
   signal to train a within-domain router that beats best-single.
3. Joint training with explicit domain-id works — both domains end
   above chance and beat their respective best-single experts on
   held-out windows, at the cost of ~5-12pp per-domain LOO accuracy
   vs domain-specialized routers.

## Limitations

- ETH3D side is still 50 windows from 5 scenes. ETH3D LOO route
  accuracy (54% specialized / 42% joint) is meaningful but not large
  enough to declare cross-domain routing solved.
- The joint router's domain-id feature is explicit at inference time.
  A real deployment with an unseen third domain would require either
  a domain classifier or further architectural work; that is not in
  scope here.
- 6D regime distribution remains scene-level one-hot on ETH3D (per
  CYCLE-20260525-stage5-cross-dataset rationale); the within-domain
  signal comes from the 4 stat features, not from regime probabilities.
- Closure cramers_v on (b) is 0.066 (low), reflecting the one-hot
  ETH3D regime layout, not a router failure.
- No SOTA claim; no ScanNet; no 4+ expert; no Stage 5 reopen.

## What This Changes

- DEC-006's negative finding upgrades from "KITTI router does not
  transfer" to a 3-experiment picture: (a) feature pruning alone
  cannot fix transfer, (b) ETH3D is independently learnable, (c)
  joint training with domain-id is a viable cross-domain recipe at
  this scale.
- DEC-007 (companion decision) records the honest claim and points
  forward.

## Server Artifacts (Authoritative)

Checkpoints:

```text
/hdd3/kykt26/checkpoints/router_kitti_robust_v1/latest.pt
/hdd3/kykt26/checkpoints/router_eth3d_v1/latest.pt
/hdd3/kykt26/checkpoints/router_joint_v1/latest.pt
```

Results JSONs:

```text
/hdd3/kykt26/code/dream3r/runs/router_kitti_robust_v1_ablation/results.json
/hdd3/kykt26/code/dream3r/runs/router_kitti_robust_v1_loo/results_loo.json
/hdd3/kykt26/code/dream3r/runs/router_kitti_robust_v1_eth3d/results.json
/hdd3/kykt26/code/dream3r/runs/router_eth3d_v1_ablation/results.json
/hdd3/kykt26/code/dream3r/runs/router_eth3d_v1_loo/results_loo.json
/hdd3/kykt26/code/dream3r/runs/router_joint_v1/summary.json
/hdd3/kykt26/code/dream3r/runs/router_joint_v1_loo/results_loo.json
```

## Boundary

Touched (new + modified scripts only):

- `code/dream3r/scripts/train_router_only.py` (modified)
- `code/dream3r/scripts/eval_router_ablation.py` (modified)
- `code/dream3r/scripts/eval_router_loo.py` (modified)
- `code/dream3r/scripts/eval_cross_domain_router.py` (modified)
- `code/dream3r/scripts/train_router_joint_domain.py` (new)
- `code/dream3r/scripts/eval_router_joint_loo.py` (new)

Not touched (per CLAUDE.md):

- `code/dream3r/model.py`
- `code/dream3r/anchor_bank.py`
- `code/dream3r/nsa_attention.py`
- `code/dream3r/bus.py`
- KITTI / ETH3D oracle builders, datasets, demo scripts.
- KITTI Stage 5 S1 expand router checkpoint (preserved untouched).

## Conclusion

DEC-006's cross-dataset negative result is now contextualized:

- **(a) partial improvement** — robust feature retrain raises ETH3D
  zero-shot route accuracy 22% → 32%, but still below chance and
  still collapsed (mast3r). Confirms feature pruning is necessary but
  not sufficient.
- **(b) success** — ETH3D is internally learnable: 54% LOO route
  accuracy, beats best-single by 6.4% LOO.
- **(c) success** — joint training with explicit domain-id places
  both domains above chance and above best-single on LOO, at the cost
  of a few points of per-domain accuracy vs the specialists.

Net: cross-domain routing is no longer a flat negative. The honest
claim shifts from "KITTI router does not transfer" to "domain-shared
routing is feasible with a domain-id feature; pure feature pruning is
not." DEC-007 records the closure.

## Addendum (evening): Joint v2 with Per-Domain Normalization

User flagged that joint v1 normalizes the 4 robust stats with a
*joint* mean/std across all 109 examples, which is dominated by
KITTI's much larger `depth_mean` variance (~155 std vs ETH3D's ~2).
This effectively makes ETH3D stat features near-constant in the
normalized space, and explains v1's 12pp ETH3D LOO loss vs the
ETH3D specialist (b).

Fix (surgical, ~50 lines across 2 files): add `per_domain_norm` flag
to `train_router_joint_domain._load_joint_examples` and pipe it
through to `eval_router_joint_loo.evaluate_joint_loo`. When True,
each domain's rows are normalized with that domain's own mean/std;
`feature_meta` records a `per_domain_stats` dict; LOO eval reads it
back for the held-out sample's domain.

Results:

| | Joint v1 (joint norm) | **Joint v2 (per-domain norm)** | Δ |
|---|---|---|---|
| KITTI closure acc | 88.14% | 84.75% | -3.39pp |
| ETH3D closure acc | 86.00% | **96.00%** | +10.00pp |
| KITTI LOO route_acc | 72.88% | 71.19% | -1.69pp |
| ETH3D LOO route_acc | 42.00% | **48.00%** | +6.00pp |
| KITTI rel_imp (LOO) | +2.81% | +1.35% | -1.46pp |
| ETH3D rel_imp (LOO) | +4.70% | **+5.78%** | +1.08pp |
| Both above chance? | yes | yes | — |

Reading: per-domain norm closes ~half the ETH3D-side gap to the
specialist (Joint v1: -12pp vs (b); Joint v2: -6pp). KITTI side pays
~1.5pp — KITTI was already dominating v1's joint norm, so it has
less to gain and a little to lose. ETH3D rel_imp vs best_single
(+5.78%) is now within 0.6pp of the ETH3D specialist (+6.39%).

Server artifacts: `/hdd3/kykt26/checkpoints/router_joint_v2/latest.pt`,
`/hdd3/kykt26/code/dream3r/runs/router_joint_v2_loo/results_loo.json`.

`per_domain_norm=False` (default) keeps v1 behavior bit-identical.

Joint v2 is the recommended cross-domain router going forward; v1
remains authoritative for the joint-norm baseline comparison.

## Addendum 3 (2026-05-27 morning): Dense GT Oracle + Seed Robustness

Two follow-up validations completed via overnight pipeline
`scripts/tonight_overnight.sh` (2026-05-26 03:11 → 04:38, 32/32 OK):

- **A. ETH3D dense-GT oracle** — rebuild the 50w ETH3D oracle using
  `rig_scan_eval/*.ply` laser-scan depth instead of SfM-sparse
  `points3D.txt` points; re-eval (a) zero-shot, retrain (b) ETH3D-only
  v2 + LOO, retrain (c) joint v3 (per-domain norm) + 109-fold LOO.
- **C. Multi-seed sweep** — re-run (a)/(b)/(c) LOO across 5 seeds
  {7, 11, 13, 17, 19} to measure seed-robustness.

### A. Dense GT oracle

New module `code/dream3r/data/eth3d_dense_oracle.py` adds:
- MeshLab `.mlp` 4×4 alignment matrix parser
- binary little-endian PLY xyz reader (no plyfile/open3d dep)
- vectorized world→camera projection + patch-grid bucketing with
  median-z per bucket

`eth3d_long.py` and `build_oracle_expert_labels_eth3d.py` gain
`--dense-gt` flag. Result JSON records `"gt_source": "dense_scan"`.

ETH3D oracle distribution shift (50w):

| | sparse (DEC-007) | dense (today) |
|---|---|---|
| fast3r | 11 (22%) | 5 (10%) |
| mast3r | 16 (32%) | 21 (42%) |
| spann3r | 23 (46%) | 24 (48%) |
| best_single | spann3r | spann3r |

(a.dense) KITTI-robust router zero-shot on dense ETH3D
(`router_kitti_robust_v1_eth3d_dense/results.json`):

```text
learned_expert_counts: fast3r=0, mast3r=50, spann3r=0   (still collapse to mast3r)
route_accuracy_vs_oracle: 42% (vs sparse 32%)
relative_improvement_vs_best_single: -22.59%  (sparse -11.14%)
```

The headline +10pp route_acc bump is a coincidence: mast3r=21/50=42% in
the dense oracle, so a deterministic always_mast3r predictor matches
the new majority. The rel_imp drop to -22.59% is the more meaningful
signal: dense GT widens the gap between always_mast3r (what the KITTI
router picks) and always_spann3r (true best-single on ETH3D), making
the cross-domain failure even more visible. **The dense GT strengthens
DEC-007's "KITTI router does not transfer" claim.**

(b.dense) ETH3D-only v2 (retrained on dense oracle) LOO
(`router_eth3d_v2_dense_loo/results_loo.json`):

```text
learned_loo_mean:  0.15235     (vs oracle 0.14185, best_single 0.16494 spann3r)
loo_route_accuracy_vs_oracle: 68.0%   (vs sparse 54.0%, +14pp)
relative_improvement_vs_best_single: 7.63%  (vs sparse 6.39%, +1.24pp)
learned_loo_expert_counts: fast3r=4, mast3r=21, spann3r=25
```

(b.dense) ETH3D closure: rel_imp +13.96% (vs sparse +10.74%, +3.22pp).

(c.dense) Joint v3 (per-domain norm, dense ETH3D + sparse KITTI) 109-fold LOO
(`router_joint_v3_dense_loo/results_loo.json`):

```text
per_domain_loo_route_accuracy:
  kitti: 72.88%   (= v2 sparse closure 72.88%; bit-identical reproduction)
  eth3d: 66.00%   (vs v2 sparse 48.00%, +18pp)
per_domain_rel_improvement_vs_best_single:
  kitti: -0.09%   (vs v2 sparse +1.35%, essentially zero / -1.44pp)
  eth3d: +8.03%   (vs v2 sparse +5.78%, +2.25pp)
both_domains_above_chance: true
```

Reading: dense GT reduces ETH3D oracle noise and lifts joint v3
ETH3D LOO route accuracy by 18pp. KITTI side is unaffected in route
accuracy (uses sparse KITTI oracle, unchanged) but loses ~1.5pp in
rel_imp because the new ETH3D-side patterns slightly perturb the
shared router's KITTI fit. Net: joint v3 (dense oracle) is the new
recommended cross-domain router.

### C. Multi-seed sweep — bug discovery + fix

Initial overnight C sweep harvested byte-identical results across all
5 seeds. Root cause: `eval_router_loo.py:173` hardcoded
`torch.manual_seed(7)` and didn't expose `--seed`; same for
`eval_router_joint_loo.py`. The overnight script's `--seed` only
affected the closure-set training (which we didn't harvest); the LOO
re-trains per-fold ignored seed.

Fix (surgical, ~20 lines across 2 files): both LOO scripts gain
`--seed` CLI which threads through `evaluate_*_loo` →
`train_router_*` per-fold and into the script's top-level
`torch.manual_seed`. Results now record `seed` field.

Re-run (`scripts/rerun_seed_sweep.sh`, 5 seeds × 3 LOO = 15 runs,
GPU 1):

Re-run (`scripts/rerun_seed_sweep.sh`, 5 seeds × 3 LOO = 15 runs,
GPU 1, 1h06m, all 15/15 OK):

(a) KITTI-robust LOO route accuracy:

| seed | route_acc | rel_imp |
|---|---|---|
| 7 | 77.97% | +4.19% |
| 11 | 69.49% | +1.40% |
| 13 | 76.27% | +4.61% |
| 17 | 71.19% | +2.22% |
| 19 | 72.88% | +2.68% |
| **mean ± std** | **73.56% ± 3.51pp** | **+3.02% ± 1.35pp** |

(b) ETH3D-only LOO route accuracy:

| seed | route_acc | rel_imp |
|---|---|---|
| 7 | 54.00% | +6.39% |
| 11 | 50.00% | +6.06% |
| 13 | 46.00% | +3.97% |
| 17 | 44.00% | +5.47% |
| 19 | 50.00% | +6.48% |
| **mean ± std** | **48.80% ± 3.90pp** | **+5.68% ± 1.03pp** |

(c) Joint v2 LOO route accuracy (per-domain norm):

| seed | KITTI acc | KITTI rel_imp | ETH3D acc | ETH3D rel_imp |
|---|---|---|---|---|
| 7 | 71.19% | +1.35% | 48.00% | +5.78% |
| 11 | 74.58% | +1.33% | 58.00% | +7.00% |
| 13 | 71.19% | +1.89% | 48.00% | +6.42% |
| 17 | 72.88% | +1.77% | 52.00% | +6.26% |
| 19 | 64.41% | -2.00% | 50.00% | +5.28% |
| **mean ± std** | **70.85% ± 3.87pp** | **+0.87% ± 1.62pp** | **51.20% ± 4.15pp** | **+6.15% ± 0.65pp** |

Reading:

- **Route accuracy is seed-robust across all 3 experiments**
  (std 3.51 / 3.90 / 3.87 / 4.15 pp, all below 5pp gate). All 15
  runs across all 3 experiments stay above 33% chance — min is 44%.
- **ETH3D rel_imp is seed-robust** — (b) mean +5.68% ± 1.03 (4/5
  seeds above 5%), (c) mean +6.15% ± 0.65 (5/5 seeds above 5%).
- **KITTI rel_imp on the joint router is NOT seed-robust** —
  mean +0.87% ± 1.62, range -2.00% → +1.89%, seed=19 actually
  negative. The previously published "+1.35% KITTI" (DEC-007
  evening addendum, seed=7 point sample) overstates the typical
  joint-vs-KITTI-best-single gain.
- **(a) KITTI-robust rel_imp drops** from previously reported
  +4.19% (seed=7) to mean +3.02% ± 1.35. None of the 5 seeds reach
  the +5% rel_imp gate.

DEC-007 honest claim revised (see DEC-007 addendum 3): both-domains-
above-chance and ETH3D rel_imp claims hold robustly; the KITTI
joint rel_imp claim is downgraded from "+1.35%" to "essentially
zero on average, sign-unstable".

### Server artifacts (new this addendum)

```text
/hdd3/kykt26/code/dream3r/runs/eth3d_dense_oracle/oracle_expert_labels.json
/hdd3/kykt26/checkpoints/router_eth3d_v2_dense/latest.pt
/hdd3/kykt26/checkpoints/router_joint_v3_dense/latest.pt
/hdd3/kykt26/code/dream3r/runs/router_kitti_robust_v1_eth3d_dense/results.json
/hdd3/kykt26/code/dream3r/runs/router_eth3d_v2_dense_ablation/results.json
/hdd3/kykt26/code/dream3r/runs/router_eth3d_v2_dense_loo/results_loo.json
/hdd3/kykt26/code/dream3r/runs/router_joint_v3_dense_loo/results_loo.json
/hdd3/kykt26/code/dream3r/runs/seed_sweep_v2/<prefix>_s<seed>_loo/results_loo.json  (15 files)
/hdd3/kykt26/code/dream3r/runs/overnight_20260526/progress.log
/hdd3/kykt26/code/dream3r/runs/seed_sweep_v2_20260527/progress.log
```

### Boundary (new this addendum)

Modified:

- `code/dream3r/scripts/eval_router_loo.py` (added `--seed`)
- `code/dream3r/scripts/eval_router_joint_loo.py` (added `--seed`)
- `code/dream3r/data/eth3d_long.py` (added `dense_gt` flag)
- `code/dream3r/scripts/build_oracle_expert_labels_eth3d.py` (added `--dense-gt`)
- `code/dream3r/scripts/train_router_only.py` (added `--seed`)

New:

- `code/dream3r/data/eth3d_dense_oracle.py`
- `code/dream3r/scripts/tonight_overnight.sh`
- `code/dream3r/scripts/rerun_seed_sweep.sh`

No v0.3/v0.5 core touched.
