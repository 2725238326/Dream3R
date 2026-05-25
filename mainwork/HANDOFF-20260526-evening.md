# HANDOFF — 2026-05-26 evening (Cross-Domain Router Retrain)

**Mission:** Convert the cross-dataset negative finding from
DEC-20260525-006 into actionable evidence by training new routers on the
existing 50-window ETH3D + 59-window KITTI oracles. Three experiments,
prioritized so the most important results land first.

The current Stage 5 S1 expanded router does NOT zero-shot transfer to
ETH3D (collapses to `always_fast3r`, 22% route accuracy below chance).
DEC-006 diagnosed the root cause as KITTI-specific stats
(`oxts_available`, `mean_speed`, `speed_std`) being out-of-distribution
for ETH3D's static rig. This handoff tests three fixes in parallel and
records the outcomes.

Both source oracles are already on the server. No new data, no new
adapters, no edits to v0.3/v0.5 core modules.

---

## 1. Reading list (in order)

| # | File | Why |
|---|---|---|
| 1 | `CLAUDE.md` | Project rules: surgical changes, no model on Windows, scp pattern |
| 2 | `mainwork.md` §5 + §7 | Stage 5 closed; this handoff is a Stage 5 follow-up cycle |
| 3 | `decisions/DEC-20260525-006-cross-dataset-closure.md` | The negative result that motivates this work |
| 4 | `cycles/CYCLE-20260525-stage5-cross-dataset.md` | What infrastructure already exists |
| 5 | `code/dream3r/scripts/train_router_only.py` | Reference training script; `_feature_tensor` is the surface to extend |
| 6 | `code/dream3r/scripts/eval_router_loo.py` | LOO eval pattern; reuse for ETH3D LOO |
| 7 | `code/dream3r/scripts/eval_router_ablation.py` + `eval_cross_domain_router.py` | The eval surfaces to re-run with each new checkpoint |

---

## 2. Server access

Same as the previous handoff:

```text
ssh BUAA-Server   (user kykt26, host 172.17.140.97:22, key id_rsa_buaa)
Conda env: dream3r
Code root:   /hdd3/kykt26/code/dream3r/dream3r/
Checkpoints: /hdd3/kykt26/checkpoints/
Run artifacts: /hdd3/kykt26/code/dream3r/runs/
```

`matplotlib` was installed into the `dream3r` env during demo packaging
(2026-05-26); no other env changes needed.

---

## 3. Hard constraints (from CLAUDE.md)

- **Local Windows = edit + sync only**. Never run model code locally.
- Local edit → `scp` to `/hdd3/kykt26/code/dream3r/dream3r/<file>`.
- Do not touch `model.py`, `anchor_bank.py`, `nsa_attention.py`, `bus.py`
  unless fixing a real bug.
- Ask before: training >4h with no convergence, modifying v0.3/v0.5
  core modules, two-reasonable-design ties.

---

## 4. Existing artifacts (use, don't redo)

```text
KITTI 59w oracle:
  /hdd3/kykt26/code/dream3r/runs/stage5_s1_expand_oracle/oracle_expert_labels.json
  oracle_counts: mast3r=31, spann3r=24, fast3r=4   (53%/41%/7%)

KITTI 59w regime labels (with full 7D stats):
  /hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json

ETH3D 50w oracle:
  /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_oracle/oracle_expert_labels.json
  oracle_counts: spann3r=23, mast3r=16, fast3r=11   (46%/32%/22%)

ETH3D 50w regime labels (one-hot per scene + 7D stats):
  /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_regime_labels/regime_labels.json

Current KITTI router (will be retrained / extended below):
  /hdd3/kykt26/checkpoints/router_stage5_s1_expand_v1/latest.pt
  (feature_mode=regime_stats, 13D input, 96.6% closure, 78% LOO)
```

---

## 5. Experiment plan

Three experiments, designed to run in series tonight. The earlier ones
have lower compute + smaller code changes; if you only finish (a) and (b)
that's already strong evidence and DEC-007 can be written.

### Exp (a) — Robust feature retrain on KITTI

**Hypothesis**: Removing the three KITTI-specific stats (`oxts_available`,
`mean_speed`, `speed_std`) yields a router that transfers better. Cost:
KITTI in-domain LOO route accuracy may drop a few points (we lose
KITTI-specific motion signal), but cross-domain transfer should no
longer collapse.

**Code change**: Add a `regime_stats_robust` feature mode in
`code/dream3r/scripts/train_router_only.py`:

- Define `STAT_FEATURE_KEYS_ROBUST = ['frame_count', 'depth_mean',
  'valid_ratio', 'depth_temporal_change']` (drop the bottom 3 KITTI-only
  stats).
- In `_feature_tensor`, when `feature_mode == "regime_stats_robust"`, use
  the robust key list. Keep `regime_stats` (full 7 keys) unchanged for
  backward compatibility.
- Mirror the change in `_load_router` / `_feature_tensor` callsites in
  `eval_router_ablation.py` and `eval_cross_domain_router.py`. The
  `feature_meta.feature_mode` check in `_load_router` should accept the
  new mode.
- Optional: factor the stat-key list into a module-level mapping
  `_FEATURE_KEY_VARIANTS = {"regime_stats": [...7 keys...],
  "regime_stats_robust": [...4 keys...]}` to keep the registry in one
  place.

**Training command**:

```text
python -m dream3r.scripts.train_router_only \
  --preset router_only \
  --oracle-labels /hdd3/kykt26/code/dream3r/runs/stage5_s1_expand_oracle/oracle_expert_labels.json \
  --regime-labels /hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json \
  --output-dir /hdd3/kykt26/checkpoints/router_kitti_robust_v1 \
  --epochs 2000 --lr 0.05 --batch-size 32 \
  --disable-critic-augmentation --feature-mode regime_stats_robust
```

**Eval commands**:

```text
# (a.1) KITTI closure
python -m dream3r.scripts.eval_router_ablation \
  --regime-labels ...stage3_regime_labels/regime_labels.json \
  --oracle-labels ...stage5_s1_expand_oracle/oracle_expert_labels.json \
  --router-checkpoint /hdd3/kykt26/checkpoints/router_kitti_robust_v1/latest.pt \
  --output /hdd3/kykt26/code/dream3r/runs/router_kitti_robust_v1_ablation/results.json \
  --feature-mode regime_stats_robust

# (a.2) KITTI LOO (59 folds, like DEC-003)
python -m dream3r.scripts.eval_router_loo \
  --regime-labels ...stage3_regime_labels/regime_labels.json \
  --oracle-labels ...stage5_s1_expand_oracle/oracle_expert_labels.json \
  --output /hdd3/kykt26/code/dream3r/runs/router_kitti_robust_v1_loo/results_loo.json \
  --work-dir /hdd3/kykt26/code/dream3r/runs/router_kitti_robust_v1_loo/folds \
  --epochs 2000 --lr 0.05 --batch-size 58 --feature-mode regime_stats_robust

# (a.3) Cross-domain transfer to ETH3D
python -m dream3r.scripts.eval_cross_domain_router \
  --regime-labels ...eth3d_cross_dataset_regime_labels/regime_labels.json \
  --oracle-labels ...eth3d_cross_dataset_oracle/oracle_expert_labels.json \
  --router-checkpoint /hdd3/kykt26/checkpoints/router_kitti_robust_v1/latest.pt \
  --kitti-oracle-labels ...stage5_s1_expand_oracle/oracle_expert_labels.json \
  --output /hdd3/kykt26/code/dream3r/runs/router_kitti_robust_v1_eth3d/results.json \
  --feature-mode regime_stats_robust
```

**Success criteria for (a)**:

- KITTI LOO route accuracy ≥ 60% (vs 78% baseline; some loss expected).
- ETH3D cross-domain route accuracy > 33% chance (the headline number).
- Router does NOT collapse to a single expert on ETH3D (≥2 experts
  predicted across the 50 windows).

### Exp (b) — ETH3D-only router

**Hypothesis**: The ETH3D 50-window oracle is internally consistent
enough to learn a within-domain routing policy. If route accuracy LOO
exceeds chance, then ETH3D side IS learnable; if not, the dataset is
too small or the oracle is too noisy.

**Code change**: None. `train_router_only.py` already accepts arbitrary
regime + oracle JSONs.

**Training command**:

```text
python -m dream3r.scripts.train_router_only \
  --preset router_only \
  --oracle-labels /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_oracle/oracle_expert_labels.json \
  --regime-labels /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_regime_labels/regime_labels.json \
  --output-dir /hdd3/kykt26/checkpoints/router_eth3d_v1 \
  --epochs 2000 --lr 0.05 --batch-size 32 \
  --disable-critic-augmentation --feature-mode regime_stats
```

Use full `regime_stats` (7 stats). On ETH3D, oxts_available/mean_speed/
speed_std are all 0 so their normalized values are 0; not a problem
within-domain. Their `stat_std` from ETH3D's own normalization will be
tiny but not zero; the `clamp_min(1e-6)` in `_feature_tensor` already
handles that.

**Eval commands**:

```text
# (b.1) ETH3D closure
python -m dream3r.scripts.eval_router_ablation \
  --regime-labels ...eth3d_cross_dataset_regime_labels/regime_labels.json \
  --oracle-labels ...eth3d_cross_dataset_oracle/oracle_expert_labels.json \
  --router-checkpoint /hdd3/kykt26/checkpoints/router_eth3d_v1/latest.pt \
  --output /hdd3/kykt26/code/dream3r/runs/router_eth3d_v1_ablation/results.json \
  --feature-mode regime_stats

# (b.2) ETH3D LOO (50 folds)
python -m dream3r.scripts.eval_router_loo \
  --regime-labels ...eth3d_cross_dataset_regime_labels/regime_labels.json \
  --oracle-labels ...eth3d_cross_dataset_oracle/oracle_expert_labels.json \
  --output /hdd3/kykt26/code/dream3r/runs/router_eth3d_v1_loo/results_loo.json \
  --work-dir /hdd3/kykt26/code/dream3r/runs/router_eth3d_v1_loo/folds \
  --epochs 2000 --lr 0.05 --batch-size 49 --feature-mode regime_stats
```

**Success criteria for (b)**:

- ETH3D LOO route accuracy > 33% chance.
- ETH3D LOO learned-router abs_rel < always_spann3r abs_rel
  (i.e., beats the ETH3D best single expert).

### Exp (c) — Joint KITTI+ETH3D training (stretch)

**Hypothesis**: A single router trained on both domains, with a
domain-id feature, can route correctly within each domain. Tests
whether the routing policy is fundamentally domain-shared or
domain-specific.

**Code change**: New file
`code/dream3r/scripts/train_router_joint_domain.py`. Outline:

- Load both regime + oracle JSONs.
- Build x by concatenating: KITTI examples + ETH3D examples (n=59+50=109).
- Domain feature: append a 2D one-hot per example
  (`[1, 0]` for KITTI, `[0, 1]` for ETH3D). The robust feature input
  becomes `[6 regime] + [4 robust stats] + [2 domain] = 12D`. (Use
  robust stats so domain-specific stats don't dominate.)
- Use `_expert_registry` and `ComposerRouter` with `n_regimes = 12` (the
  router treats the input as one flat vector; `n_regimes` here is the
  first MLP input width, not the regime count).
- Train with same hyperparameters as KITTI router.

**LOO eval**: Hold out 1 sequence at a time across both domains
(109 folds). Report:

- Overall LOO route accuracy.
- Per-domain LOO route accuracy (KITTI subset accuracy, ETH3D subset
  accuracy).
- Per-domain abs_rel improvement vs best single in that domain.

**Success criteria for (c)**:

- Per-domain LOO route accuracy > 33% chance in BOTH domains
  simultaneously.
- Joint router does not degrade KITTI LOO performance by more than 10
  points vs the (a) robust KITTI-only router.

(c) is a stretch and can be deferred to the next handoff if (a) and (b)
take longer than expected.

---

## 6. Deliverables checklist

By end of handoff:

- [ ] `code/dream3r/scripts/train_router_only.py` updated with
      `regime_stats_robust` feature mode (and any callsites).
- [ ] (Exp a) `/hdd3/kykt26/checkpoints/router_kitti_robust_v1/latest.pt`
      + 3 results JSONs (closure / LOO / ETH3D transfer).
- [ ] (Exp b) `/hdd3/kykt26/checkpoints/router_eth3d_v1/latest.pt`
      + 2 results JSONs (closure / LOO).
- [ ] (Exp c, stretch) joint router checkpoint + per-domain LOO results.
- [ ] `cycles/CYCLE-20260526-cross-domain-router-retrain.md` with
      experiment outcomes.
- [ ] `decisions/DEC-20260526-007-cross-domain-routing.md` with honest
      claim wording. Outcomes have three possible categories:
  - **Success (clear transfer)**: (a) gets ETH3D route accuracy > 50%
    or (c) clearly beats baselines.
  - **Partial (ETH3D learnable, KITTI router doesn't transfer)**: (b)
    works but (a) doesn't reach > 33% on ETH3D.
  - **Negative (neither works)**: both retrains underperform. Still a
    valid finding — cross-domain routing needs more than feature
    redesign.
- [ ] `mainwork.md` updated with a "Stage 5 follow-up: cross-domain
      routing experiments" section pointing to CYCLE-20260526 + DEC-007.

---

## 7. Out of scope (do NOT start)

- New expert (CUT3R, VGGT).
- New dataset beyond KITTI + ETH3D.
- 4th expert distillation (DEC-004 trigger still not met).
- Track B (S5 tttLRM real TTT). That is a separate handoff.
- ScanNet. No data.
- Critic / repair pipeline changes.

---

## 8. Risks / things that may bite

1. **`_load_router` accepts only `regime_stats` and `regime`**: it
   `expected_feature_mode` check in `eval_router_ablation.py` will reject
   `regime_stats_robust` unless you also add it to the allowed list.
2. **ETH3D LOO at N=50 with 49-batch**: the LOO eval script uses
   `--batch-size 58` for KITTI's 59 windows; for ETH3D, use `--batch-size
   49` (one less than the count, matching the LOO pattern).
3. **ETH3D oracle features may have stat_std ~= 0 for oxts/speed**:
   `_feature_tensor` already does `clamp_min(1e-6)`, but the normalized
   value of the all-zero column will then be 0 (mean) for every example.
   The router will simply ignore that input dimension. Not a bug, but
   worth noting in the cycle doc.
4. **Joint training (c) domain-id placement**: appending the 2D domain
   feature AT THE END means `regime_encoder.0.weight` shape changes from
   `[d_routing, 10]` (robust) to `[d_routing, 12]` (robust+domain).
   Make sure your new training script doesn't try to load any prior
   checkpoint state.
5. **LOO at N=109 (Exp c) is the slowest job**: each fold retrains for
   2000 epochs on 108 examples. Estimated 30-60 min on GPU. If wall
   time is short, set `--max-folds` (or equivalent) to subsample 30-40
   folds and report `loo_n_folds < n_total` explicitly in the eval JSON.

---

## 9. When you finish

Send the user a short message:

- All three experiments done? List the numbers (LOO route accuracy per
  experiment + ETH3D transfer accuracy).
- Some not done? Say which and why.
- DEC-007 path + headline claim.
- Recommended next direction (or "no active handoff" if Stage 5 follow-up
  is complete).
