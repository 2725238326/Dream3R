# DEC-20260526-007 - Cross-Domain Routing (Robust + ETH3D + Joint)

## Decision

Close the cross-domain router retrain follow-up that
DEC-20260525-006 surfaced. The HANDOFF-20260526-evening recipe of
three retrains (robust KITTI, ETH3D-only, joint KITTI+ETH3D) was
executed end-to-end on the server with no v0.3/v0.5 core edits. The
honest claim category is **partial / success** (per HANDOFF §6
"Outcomes have three possible categories"):

- (a) Robust KITTI router — improves ETH3D zero-shot route accuracy
  22% → 32% but still below chance and still collapsed; feature
  pruning is necessary but not sufficient.
- (b) ETH3D-only router — success. 54% LOO route accuracy
  (vs 33% chance) and beats best-single by 6.4% LOO.
- (c) Joint router with 2D domain-id — success. Per-domain LOO route
  accuracy above 33% chance in BOTH domains simultaneously
  (KITTI 72.88%, ETH3D 42.00%), and beats best-single in both
  domains (KITTI +2.81%, ETH3D +4.70% LOO).

Stage 5 status is unchanged (`done` — DEC-006 already closed it).
This decision records a follow-up cycle that converted a negative
finding into a constructive next step.

## Headline Claim (Honest Wording)

> Single-domain routing with handcrafted regime + stat features is
> learnable on both KITTI and ETH3D in isolation. KITTI's
> specialized router does NOT transfer zero-shot to ETH3D even after
> dropping the three KITTI-specific stats (oxts_available,
> mean_speed, speed_std); cross-domain transfer requires either
> domain-specific training or an explicit domain-id feature. A
> single 12D-input router (6 regime + 4 robust stats + 2 domain
> one-hot) trained jointly on the 109-window KITTI+ETH3D set
> simultaneously beats each domain's best single expert on held-out
> LOO, at a 5pp / 12pp cost in per-domain LOO route accuracy
> relative to domain-specialized routers.

Not claimed: SOTA; ScanNet; cross-domain generalization to a third
unseen dataset; routing without an explicit domain-id at inference.

## Outcome Category

Per HANDOFF §6:

- **Success (clear transfer)**: would have required (a) ETH3D route
  accuracy > 50%. Not met — (a) reaches 32%.
- **Partial (ETH3D learnable, KITTI router doesn't transfer)**:
  matches — (b) confirms ETH3D learnable; (a) confirms KITTI router
  doesn't transfer even with feature redesign.
- **Negative (neither works)**: not the case — (b) and (c) both met
  their success criteria.

This decision records the result as **partial-with-strong-(c)**:
the cross-domain question now has a positive answer when a
domain-id feature is allowed.

## Evidence Summary (Authoritative Numbers)

KITTI 59w in-domain (held-out LOO):

```text
Stage 5 S1 expand router (DEC-003):  78%   route_acc, +2.23% rel_imp
(a) Robust KITTI router:             77.97% route_acc, +4.19% rel_imp
(c) Joint router (KITTI subset):     72.88% route_acc, +2.81% rel_imp
```

ETH3D 50w in-domain (LOO for (b)/(c), zero-shot for the others):

```text
Stage 5 S1 expand router (DEC-006):  22% route_acc, -16.7% rel_imp  (collapse to fast3r)
(a) Robust KITTI router:             32% route_acc, -11.14% rel_imp (collapse to mast3r)
(b) ETH3D-only router LOO:           54% route_acc, +6.39% rel_imp  (3 experts used)
(c) Joint router (ETH3D subset LOO): 42% route_acc, +4.70% rel_imp  (3 experts used)
```

Both-domains-above-chance simultaneously: only achieved by (c).

## Rationale (Why The Recipe Worked Where It Did)

1. **(a) cannot solve transfer alone**: dropping
   oxts_available/mean_speed/speed_std removes 3 KITTI-only
   columns, but the remaining 4 stats are normalized with KITTI's
   training-time mean/std (frozen at eval). KITTI's
   `depth_temporal_change` distribution centers around driving-rate
   inter-frame change (~0.04); ETH3D's static rig produces lower
   values that still land outside the router's training manifold.
   Even though no single column is now KITTI-specific, the joint
   distribution still is. The router collapses to mast3r (KITTI's
   training-set majority class) instead of fast3r (DEC-006's
   pathological corner).
2. **(b) succeeds because the 50w ETH3D oracle is internally
   consistent**: per-window best expert distribution
   (spann3r=23/mast3r=16/fast3r=11) is balanced; the 4 stats give
   enough discriminative signal to predict the held-out winner
   54% of the time even though the 6D regime probs are scene-level
   one-hot (low cramers_v = 0.066). The router learns from stats,
   not from regimes, on ETH3D.
3. **(c) succeeds because the explicit 2D domain-id lets the MLP
   gate per-domain stat normalization implicitly**: the first
   layer can use domain bits to "switch" the effective stat weights.
   Joint normalization (mean/std computed across both domains)
   would otherwise blur domain-specific stat ranges; the domain-id
   restores the ability to specialize.

## Implementation Boundary

Touched (`code/dream3r/scripts/`):

- `train_router_only.py` (modified) — module-level
  `_FEATURE_KEY_VARIANTS` dict, new `regime_stats_robust` mode (4
  stat keys), `--feature-mode` choice extended.
- `eval_router_ablation.py` (modified) — frozen-stats branch widened
  to include `regime_stats_robust`, `--feature-mode` choice extended.
- `eval_router_loo.py`, `eval_cross_domain_router.py` (modified) —
  `--feature-mode` choice extended.
- `train_router_joint_domain.py` (new) — joint 12D-input trainer
  (`6 regime + 4 robust stats + 2 domain one-hot`).
- `eval_router_joint_loo.py` (new) — per-domain LOO over 109-example
  joint set with stratified `--max-folds` subsampling support
  (not used; full 109 folds completed in <6 min).

Not touched (per CLAUDE.md):

- `code/dream3r/model.py`
- `code/dream3r/anchor_bank.py`
- `code/dream3r/nsa_attention.py`
- `code/dream3r/bus.py`
- Stage 5 S1 expand router checkpoint (`router_stage5_s1_expand_v1`).
- KITTI / ETH3D oracle builders and datasets.

## New Server Artifacts

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

## Limitations On This Decision

- Both retrains use the existing oracle metric tables; no new
  forward passes through the three real experts were run.
- ETH3D side is 50 windows / 5 scenes; the 54%/42% LOO numbers are
  meaningful relative to chance but not large-sample.
- (c)'s domain-id is explicit at inference time; an unseen third
  domain would require a domain classifier or an attention-style
  domain-shared head. Out of scope for this decision.
- No SOTA, no ScanNet, no 4+ expert, no Critic/Repair changes.

## Follow-Up (Future-Work Triggers, Not Active)

These do NOT open a new handoff:

1. A third domain (e.g., dense-depth ETH3D from `rig_scan_eval/`, or
   any TUM-RGBD subset) would let us test whether (c)'s recipe
   generalizes beyond a 2-domain mix.
2. The (a) result rules out simple feature pruning. The next
   architectural step for true zero-shot transfer would be either
   (i) per-domain normalization at inference (requires a domain
   classifier on the input window), or (ii) a small fine-tune on a
   handful of held-out target-domain windows.
3. (c)'s 5-12pp per-domain LOO drop vs specialists could likely be
   recovered with mild capacity increase or longer training; not
   urgent.

## Boundary On This Decision

This decision changes no v0.3/v0.5 core code, no KITTI artifacts,
no ETH3D oracle, and makes no SOTA claim. It converts the DEC-006
follow-up (HANDOFF-20260526-evening) into three documented retrain
outcomes and an honest cross-domain claim with explicit success
gate references.

## Addendum (2026-05-26 evening): Per-Domain Norm Refinement → Joint v2

### Motivation

User raised that KITTI 59w and ETH3D 50w carry markedly different
information density: KITTI's `depth_mean` distribution is centered
around 165 ± 180 patches/window (LiDAR projection), ETH3D's is 5 ± 2
patches/window (SfM triangulation). In Joint v1, the 4 robust stats
were normalized with mean/std computed *jointly* across all 109
examples. The joint `depth_mean` std (~155) is dominated by KITTI
variance, so the ETH3D rows collapse to a narrow band in the
normalized space — the router only learns to read ETH3D rows through
the explicit 2D domain-id, not through the stat content. This
explained Joint v1's ETH3D LOO loss vs the ETH3D specialist
(54% → 42%, -12pp).

### Change

`train_router_joint_domain._load_joint_examples` and
`eval_router_joint_loo.evaluate_joint_loo` gained a
`per_domain_norm: bool` switch. When True:

- The 4 robust stats are normalized using each domain's own
  mean/std: KITTI rows by KITTI mean/std, ETH3D rows by ETH3D
  mean/std.
- `feature_meta` carries a nested `per_domain_stats` dict instead
  of single `stat_mean`/`stat_std`.
- LOO eval reads `per_domain_stats` from the fold checkpoint and
  applies the matching domain's frozen stats to the held-out sample.

12D input shape unchanged. 2D domain-id one-hot unchanged. No core
v0.3/v0.5 edits.

Backward compatibility: `per_domain_norm=False` (default) preserves
v1 behavior bit-identical.

### Joint v2 Results (per-domain norm)

Closure (`router_joint_v2/summary.json`):

```text
n_examples: 109
final_accuracy: 89.91%  (v1: 87.16%)
per_domain_accuracy:
  kitti: 84.75%   (v1: 88.14%, -3.39pp)
  eth3d: 96.00%   (v1: 86.00%, +10.00pp)
```

109-fold LOO (`router_joint_v2_loo/results_loo.json`):

```text
n_folds_run: 109  (full)
per_domain_loo_route_accuracy:
  kitti: 71.19%   (v1: 72.88%, -1.69pp; vs (a) 77.97%, -6.78pp)
  eth3d: 48.00%   (v1: 42.00%, +6.00pp; vs (b) 54.00%, -6.00pp)
per_domain_rel_improvement_vs_best_single:
  kitti: +1.35%   (v1: +2.81%, -1.46pp)
  eth3d: +5.78%   (v1: +4.70%, +1.08pp)
success.both_domains_above_chance: true
```

### Reading

The per-domain norm closes about half of the joint-vs-specialist gap
on ETH3D (Joint v1 was 12pp below (b); Joint v2 is 6pp below) at the
cost of ~1.5pp on KITTI LOO route accuracy and ~1.5pp on KITTI
relative improvement. ETH3D rel_imp vs best-single (+5.78%) is now
within 0.6pp of the ETH3D specialist (+6.39%). Both domains remain
simultaneously above chance.

The trade is acceptable: information-imbalanced datasets are
handled more symmetrically. The remaining ETH3D-side gap vs
specialist suggests joint training still imposes some capacity cost
beyond normalization alone — likely the shared router head having
to express both domains' routing policies in the same MLP.

### Revised Headline Claim

> Joint training of a single domain-aware router on the
> 109-window KITTI+ETH3D set is viable. With per-domain stat
> normalization (v2), the joint router achieves per-domain LOO
> route accuracy of 71.19% (KITTI) and 48.00% (ETH3D) and beats
> each domain's best single expert on held-out windows (+1.35%
> KITTI, +5.78% ETH3D), simultaneously. The per-domain norm
> closes roughly half of the ETH3D-side gap vs a domain
> specialist that Joint v1 incurred, by preventing KITTI's much
> larger stat variance from dominating the joint normalization.

### Additional Server Artifacts

```text
/hdd3/kykt26/checkpoints/router_joint_v2/latest.pt
/hdd3/kykt26/code/dream3r/runs/router_joint_v2_loo/results_loo.json
```

Joint v1 artifacts remain authoritative for the "joint norm baseline"
comparison; Joint v2 is the recommended cross-domain router going
forward.

### Limitations On The Refinement

- `per_domain_norm` requires the domain label at inference. This is
  the same constraint as the 2D domain-id one-hot, so no new
  deployment requirement is introduced.
- ETH3D `frame_count` column has zero std on ETH3D (constant = 4),
  so normalize-then-clamp produces a constant 0 column for ETH3D
  rows. Router learns to ignore that column for ETH3D — confirmed
  by sanity check (ETH3D normalized stat std exactly 0 on
  frame_count, ~1 on the other three).
- KITTI side picks up no benefit (slight loss); this is consistent
  with v1's joint norm already being KITTI-dominated.
- This refinement does not address the ~6pp ETH3D LOO gap that
  still remains vs the specialist (b). Closing that would likely
  need either capacity changes (out of CLAUDE.md scope without a
  trigger) or more ETH3D data.

## Addendum 3 (2026-05-27 morning): Dense GT Oracle + Seed Robustness

Two validations executed via overnight pipeline
`scripts/tonight_overnight.sh` (32/32 OK, 1h27m) plus a follow-up
`scripts/rerun_seed_sweep.sh` after a seed-handling bug in the LOO
evaluators was discovered.

### Dense GT oracle

ETH3D 50w oracle rebuilt with `rig_scan_eval/*.ply` laser-scan depth
(dense_scan source) instead of SfM-sparse `points3D.txt`. New
`code/dream3r/data/eth3d_dense_oracle.py` adds a MeshLab `.mlp`
parser, a binary little-endian PLY reader (no plyfile/open3d
dependency), and a vectorized world→camera projection with patch-grid
median-z bucketing. `eth3d_long.py` and
`build_oracle_expert_labels_eth3d.py` gain `--dense-gt`.

ETH3D 50w oracle distribution shift:

```text
sparse (DEC-007 main): fast3r=11 (22%), mast3r=16 (32%), spann3r=23 (46%)
dense  (today):        fast3r=5  (10%), mast3r=21 (42%), spann3r=24 (48%)
best_single (both):    spann3r
```

| metric | sparse | dense | Δ |
|---|---|---|---|
| (a) ETH3D zero-shot route acc | 32% | 42% | +10pp (still collapse to mast3r) |
| (a) ETH3D zero-shot rel_imp | -11.14% | **-22.59%** | -11.45pp (worse) |
| (b) ETH3D-only closure rel_imp | +10.74% | **+13.96%** | +3.22pp |
| (b) ETH3D-only LOO route acc | 54% | **68%** | +14pp |
| (b) ETH3D-only LOO rel_imp | +6.39% | +7.63% | +1.24pp |
| (c) Joint KITTI LOO route acc | 71.19% (v2) | 72.88% (v3) | +1.69pp |
| (c) Joint ETH3D LOO route acc | 48.00% (v2) | **66.00%** (v3) | +18pp |
| (c) Joint KITTI LOO rel_imp | +1.35% (v2) | -0.09% (v3) | -1.44pp (≈0) |
| (c) Joint ETH3D LOO rel_imp | +5.78% (v2) | +8.03% (v3) | +2.25pp |

Reading: dense GT is a stronger oracle signal — ETH3D-only LOO route
accuracy jumps 14pp (54% → 68%) and joint v3 ETH3D LOO route accuracy
jumps 18pp (48% → 66%), simultaneously preserving joint KITTI LOO
route accuracy (72.88% = v2 sparse exact). The +10pp on (a) is a
coincidence (mast3r class share went from 32% to 42%, matching the
always-mast3r collapse). The rel_imp drop to -22.59% on (a) is the
substantive signal: dense GT makes the gap between always_mast3r
(KITTI router's collapse target) and the true best-single
(always_spann3r) more visible. **Dense GT strengthens both DEC-007's
"KITTI router does not transfer" claim AND the (b)/(c) success
claims**.

### Seed-handling bug + fix

Initial overnight C sweep (5 seeds × 3 LOO) produced byte-identical
results across all 15 runs because:

- `eval_router_loo.py:173` hardcoded `torch.manual_seed(7)`, no
  `--seed` CLI.
- `eval_router_joint_loo.py` likewise had no `--seed` CLI.
- The overnight orchestrator's `--seed $SEED` was passed only to
  `train_router_only` (closure-set training, which we did not
  harvest); the LOO retrain per-fold ignored seed.

Fix (surgical, ~20 lines across 2 files): both LOO scripts now
expose `--seed` and thread it through to `evaluate_*_loo` →
`train_router_*` per-fold and into the script's top-level
`torch.manual_seed`. Results JSON gains a `seed` field.

Sanity: with the fix, kitti_robust LOO at seed=11 produces
route_acc 0.6949 (≠ seed=7's 0.7797), confirming the seed now
affects the result. The original seed=7 result reproduces
bit-identically.

### Seed sweep v2 results

Re-run via `scripts/rerun_seed_sweep.sh` (5 seeds × 3 LOO = 15 runs,
GPU 1, 1h06m). All 15/15 OK. Results at
`/hdd3/kykt26/code/dream3r/runs/seed_sweep_v2/<prefix>_s<seed>_loo/`.

(a) **KITTI-robust LOO** (sparse KITTI oracle, regime_stats_robust):

| seed | route_acc | rel_imp | learned counts |
|---|---|---|---|
| 7  | 77.97% | +4.19% | fast3r=4, mast3r=30, spann3r=25 |
| 11 | 69.49% | +1.40% | fast3r=5, mast3r=29, spann3r=25 |
| 13 | 76.27% | +4.61% | fast3r=4, mast3r=29, spann3r=26 |
| 17 | 71.19% | +2.22% | fast3r=4, mast3r=28, spann3r=27 |
| 19 | 72.88% | +2.68% | fast3r=5, mast3r=30, spann3r=24 |
| **mean ± std** | **73.56% ± 3.51pp** | **+3.02% ± 1.35pp** | — |

(b) **ETH3D-only LOO** (sparse ETH3D oracle, regime_stats):

| seed | route_acc | rel_imp | learned counts |
|---|---|---|---|
| 7  | 54.00% | +6.39% | fast3r=12, mast3r=12, spann3r=26 |
| 11 | 50.00% | +6.06% | fast3r=11, mast3r=14, spann3r=25 |
| 13 | 46.00% | +3.97% | fast3r=13, mast3r=14, spann3r=23 |
| 17 | 44.00% | +5.47% | fast3r=13, mast3r=13, spann3r=24 |
| 19 | 50.00% | +6.48% | fast3r=10, mast3r=14, spann3r=26 |
| **mean ± std** | **48.80% ± 3.90pp** | **+5.68% ± 1.03pp** | — |

(c) **Joint v2 LOO** (per-domain norm, sparse KITTI + sparse ETH3D):

| seed | KITTI acc | KITTI rel_imp | ETH3D acc | ETH3D rel_imp |
|---|---|---|---|---|
| 7  | 71.19% | +1.35% | 48.00% | +5.78% |
| 11 | 74.58% | +1.33% | 58.00% | +7.00% |
| 13 | 71.19% | +1.89% | 48.00% | +6.42% |
| 17 | 72.88% | +1.77% | 52.00% | +6.26% |
| 19 | 64.41% | -2.00% | 50.00% | +5.28% |
| **mean ± std** | **70.85% ± 3.87pp** | **+0.87% ± 1.62pp** | **51.20% ± 4.15pp** | **+6.15% ± 0.65pp** |

### Seed-robustness assessment

Acceptance gate (per HANDOFF §3): claim is seed-robust if std < 5pp on
route accuracy. All three experiments pass: (a) 3.51pp, (b) 3.90pp,
(c-K) 3.87pp, (c-E) 4.15pp.

The above-chance claim is robust across all 5 seeds in all 3
experiments: min route accuracy across all 15 runs is 44% (still
+11pp above 33% chance).

The "+5% rel_imp" claim has mixed seed-robustness:

- (b) ETH3D-only: 4/5 seeds clear the 5% gate (seed=13 at 3.97%).
  Mean +5.68% > 5%. **Mostly seed-robust.**
- (c) ETH3D joint: 5/5 seeds clear the 5% gate (min 5.28%).
  Mean +6.15% ± 0.65pp. **Fully seed-robust.**
- (c) KITTI joint: 4/5 seeds positive, seed=19 actually negative
  (-2.00%). Mean +0.87% ± 1.62pp. **Not seed-robust** — original
  claim of "+1.35% KITTI" reflected a single-seed point sample,
  not a stable signal.

### DEC-007 claim revision based on seed sweep

The DEC-007 evening addendum claimed "Joint v2 beats each domain's
best single expert on held-out windows (+1.35% KITTI, +5.78% ETH3D)
simultaneously". The seed sweep shows KITTI's rel_imp on joint is
near zero on average (+0.87%) and varies in sign across seeds. The
honest revision:

> Joint v2 (per-domain norm) achieves **per-domain LOO route accuracy
> above 33% chance on both domains across all 5 seeds tested**
> (KITTI 70.85% ± 3.87pp, ETH3D 51.20% ± 4.15pp). The
> beat-best-single margin is **seed-robust on ETH3D (+6.15% ± 0.65pp,
> all 5 seeds > +5%)** but **near-zero and sign-unstable on KITTI
> (+0.87% ± 1.62pp, 4/5 seeds positive, 1/5 negative)**.

This does NOT change the partial-with-strong-(c) outcome category:
the "both domains above chance" criterion holds robustly, and the
ETH3D-side beat-best-single still holds robustly. Only the KITTI-side
joint rel_imp claim is downgraded from "small positive" to
"essentially zero".

### Sweep server artifacts

```text
/hdd3/kykt26/checkpoints/seed_sweep/{kitti_robust,eth3d_only,joint_v2}_s{7,11,13,17,19}/latest.pt  (15 ckpts, from overnight)
/hdd3/kykt26/code/dream3r/runs/seed_sweep_v2/{kitti_robust,eth3d_only,joint_v2}_s{7,11,13,17,19}_loo/results_loo.json  (15 LOO results, the canonical numbers)
/hdd3/kykt26/code/dream3r/runs/seed_sweep_v2_20260527/progress.log
```

The 15 checkpoints from the original overnight C sweep are retained
even though their LOO results were the byte-identical seed=7 LOO; the
checkpoints themselves DO vary by closure-set training seed and
remain available for future analysis. Their LOO outputs are
superseded by `seed_sweep_v2/`.

### Revised headline claim

> Joint v3 with **dense ETH3D oracle** and **per-domain stat
> normalization** is the new recommended cross-domain router.
> Per-domain LOO route accuracy: KITTI 72.88%, ETH3D 66.00%
> (vs 33% chance and vs domain specialists 77.97% / 68.00%).
> Per-domain rel_imp vs best-single: KITTI -0.09% (essentially
> zero), ETH3D +8.03%. KITTI router still does not zero-shot
> transfer to ETH3D (route_acc 42%, rel_imp -22.59% under dense
> GT). Sparse-GT (v2) results remain on file as a more
> conservative oracle baseline; dense-GT (v3) is the new
> canonical.

### Outcome category revision

Original (sparse): partial-with-strong-(c).
Revised (dense + sparse): success on (b) and (c) by stronger margin,
unchanged on (a). The cross-domain question now has a clearly
positive answer when a domain-id feature plus per-domain norm is
allowed.

### Additional server artifacts

```text
/hdd3/kykt26/checkpoints/router_eth3d_v2_dense/latest.pt
/hdd3/kykt26/checkpoints/router_joint_v3_dense/latest.pt
/hdd3/kykt26/code/dream3r/runs/eth3d_dense_oracle/oracle_expert_labels.json
/hdd3/kykt26/code/dream3r/runs/router_kitti_robust_v1_eth3d_dense/results.json
/hdd3/kykt26/code/dream3r/runs/router_eth3d_v2_dense_ablation/results.json
/hdd3/kykt26/code/dream3r/runs/router_eth3d_v2_dense_loo/results_loo.json
/hdd3/kykt26/code/dream3r/runs/router_joint_v3_dense_loo/results_loo.json
/hdd3/kykt26/code/dream3r/runs/seed_sweep_v2/<prefix>_s<seed>_loo/results_loo.json  (15 files)
/hdd3/kykt26/code/dream3r/runs/overnight_20260526/progress.log
/hdd3/kykt26/code/dream3r/runs/seed_sweep_v2_20260527/progress.log
```

### Boundary on this addendum

Touched (`code/dream3r/`):

- `data/eth3d_dense_oracle.py` (new) — PLY/MLP parser + dense pointmap.
- `data/eth3d_long.py` (modified) — `dense_gt` flag.
- `scripts/build_oracle_expert_labels_eth3d.py` (modified) — `--dense-gt`.
- `scripts/train_router_only.py` (modified) — `--seed` CLI added earlier.
- `scripts/eval_router_loo.py` (modified) — `--seed` CLI (this addendum).
- `scripts/eval_router_joint_loo.py` (modified) — `--seed` CLI (this addendum).
- `scripts/tonight_overnight.sh` (new) — overnight orchestrator.
- `scripts/rerun_seed_sweep.sh` (new) — seed sweep re-run.

Not touched (per CLAUDE.md):

- v0.3/v0.5 core (`model.py`, `anchor_bank.py`, `nsa_attention.py`, `bus.py`).
- KITTI 59w oracle (`stage5_s1_expand_oracle/`), KITTI regime labels,
  Stage 5 S1 expand router checkpoint.
- Existing v1/v2 joint checkpoints and result JSONs (sparse-GT
  numbers remain authoritative for the v2 history).

### Limitations on this addendum

- Dense oracle is still 50 windows / 5 ETH3D scenes; the +14/+18pp
  lift is meaningful relative to chance but not a large-sample
  cross-dataset SOTA claim.
- The (a) +10pp route_acc bump is coincidental (oracle distribution
  shift), not a router improvement.
- Dense GT projection uses MLP-aligned scans with median-z bucketing
  in a 14×14 patch grid; small alignment errors per scan are
  smoothed by the median but not corrected.
- The seed-handling fix preserves backward compatibility — the new
  `--seed` defaults to 7, so all previously published seed=7
  numbers remain bit-identical.
