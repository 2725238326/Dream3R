# DEC-20260525-006 - Stage 5 Cross-Dataset Closure (ETH3D)

## Decision

Close Stage 5 fully with a real on-server cross-dataset transfer eval on
ETH3D Low-res many-view. Record the honest negative finding: the KITTI-
trained Stage 5 S1 expanded router (`router_stage5_s1_expand_v1`) does NOT
transfer zero-shot to ETH3D. It collapses to `always_fast3r` on all 50
ETH3D windows, gets 22% route accuracy (below 33% chance), and is 16.7%
worse than the ETH3D best single expert.

This closes the cross-dataset thread that DEC-20260525-005 deferred and
formally moves Stage 5 to `done` in `mainwork.md`. Cross-domain routing is
flagged as future work, not as a current claim.

## Rationale

DEC-20260525-005 deferred cross-dataset validation when neither server
network nor user bandwidth supported the ETH3D download. Trigger #2 (user
bandwidth) fired on 2026-05-25 evening: user downloaded ETH3D Low-res
many-view Training archives locally and scp'd them to the server (~3.9 GB
across 4 .7z files). The preserved plan in DEC-005 became the active work
plan; this decision records the closure.

Stage 5 had two open threads:

- S1 KITTI in-domain (closed by DEC-20260525-003 with 7.60% closure-set
  improvement and 78% LOO held-out route accuracy).
- Cross-dataset (deferred by DEC-005; now closed by this decision).

Closing the cross-dataset thread requires a real eval, regardless of
outcome direction (per HANDOFF C6: both strong-transfer and weak-transfer
are publishable evidence).

## ETH3D Pipeline (New Code Path)

Four new files were added (no edits to v0.3/v0.5 core modules):

- `code/dream3r/data/eth3d_long.py` — `ETH3DLongSequenceDataset`. Builds
  KITTI-shape windows (`images [N,3,H,W]`, `pointmap_gt [N,196,3]`,
  `pointmap_mask [N,196]`, intrinsics, camera poses) by parsing COLMAP
  `rig_calibration_undistorted/{cameras.txt, images.txt, points3D.txt}`
  for each scene, projecting visible SfM points to each image's camera
  frame, and bucketing into a 14x14 patch grid (median-z per bucket).
  Cameras with zero triangulated observations (cam6, cam7 in all 5 ETH3D
  scenes) are dropped at dataset construction.
- `code/dream3r/scripts/generate_eth3d_regime_labels.py` — emits an
  ETH3D regime labels JSON that mirrors KITTI's `regime_labels.json`
  schema. Regime probabilities are one-hot per scene per the HANDOFF
  mapping (`delivery_area, electro -> indoor_static`;
  `forest, playground, terrains -> outdoor_static`). The 7
  `STAT_FEATURE_KEYS` are computed per-window from the dataset itself
  (`frame_count=4`, `depth_mean` from SfM-projected medians, `valid_ratio`
  from mask, `depth_temporal_change` from across-frame deltas;
  `oxts_available = mean_speed = speed_std = 0` for the static rig).
- `code/dream3r/scripts/build_oracle_expert_labels_eth3d.py` — near-clone
  of `build_oracle_expert_labels.py` wired to ETH3D dataset; same metric
  (`_pointmap_abs_rel` with `align_scale=True`), same three real experts
  (Fast3R, MASt3R, Spann3R).
- `code/dream3r/scripts/eval_cross_domain_router.py` — thin wrapper over
  `evaluate_router_ablation` that adds cross-domain reporting fields
  (route distribution shift, ETH3D vs KITTI best-single, route accuracy
  comparison).

## ETH3D Window Set

50 windows total across 5 scenes (10 per scene), 4 frames per window,
patch grid 14x14, image-size 224. After dropping cam6/cam7, all windows
come from cam5. SfM points3D.txt provides per-window sparse depth GT
(mean ~hundreds of valid patches per window after bucketing).

Per-scene regime label (one-hot):

```text
delivery_area -> indoor_static
electro       -> indoor_static
forest        -> outdoor_static
playground    -> outdoor_static
terrains      -> outdoor_static
```

## ETH3D Oracle

Command:

```text
python -m dream3r.scripts.build_oracle_expert_labels_eth3d \
  --root /hdd3/kykt26/data \
  --regime-labels /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_regime_labels/regime_labels.json \
  --output /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_oracle/oracle_expert_labels.json \
  --experts fast3r mast3r spann3r \
  --align-scale
```

Result:

```text
n_sequences: 50
oracle_counts:
  spann3r: 23 (46%)
  mast3r:  16 (32%)
  fast3r:  11 (22%)
metric: scale_aligned_abs_rel
```

Cross-domain oracle comparison:

```text
                KITTI 59w       ETH3D 50w
mast3r          31 (53%)        16 (32%)
spann3r         24 (41%)        23 (46%)
fast3r           4  (7%)        11 (22%)
best_single     mast3r          spann3r       <- shifted
```

The per-window best expert shifts across domains, and Fast3R triples its
share. This itself is real cross-dataset evidence: the routing problem is
domain-dependent.

## Cross-Dataset Transfer Eval

Command:

```text
python -m dream3r.scripts.eval_cross_domain_router \
  --regime-labels /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_regime_labels/regime_labels.json \
  --oracle-labels /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_oracle/oracle_expert_labels.json \
  --router-checkpoint /hdd3/kykt26/checkpoints/router_stage5_s1_expand_v1/latest.pt \
  --kitti-oracle-labels /hdd3/kykt26/code/dream3r/runs/stage5_s1_expand_oracle/oracle_expert_labels.json \
  --output /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_router/results.json \
  --feature-mode regime_stats
```

Result:

```text
metrics:
  learned_router: 0.2712     <- matches always_fast3r exactly
  random_routing: 0.2536
  oracle_router:  0.2075
  always_fast3r:  0.2712
  always_mast3r:  0.2583
  always_spann3r: 0.2324     <- best single on ETH3D
best_single_expert: spann3r
relative_improvement_vs_best_single: -0.1668   # -16.7% (router worse than best single)
learned_expert_counts:  fast3r=50, mast3r=0, spann3r=0
oracle_expert_counts:   fast3r=11, mast3r=16, spann3r=23
eth3d_route_accuracy_vs_oracle: 0.22            # below 33% chance
best_single_shifted_kitti_to_eth3d: true        # mast3r -> spann3r
```

## Honest Claim Set

What is supported:

- All four new code modules (dataset, regime label generator, oracle
  builder, cross-domain eval) ran end-to-end on the server with the same
  three real experts used for KITTI S1 closure.
- ETH3D oracle covers all 3 experts: each is the per-window winner on
  >=11 of 50 windows. No expert is degenerate on ETH3D.
- The KITTI Stage 5 S1 expanded router collapses to `always_fast3r` on
  ETH3D (route accuracy 22% vs 33% chance) and underperforms the ETH3D
  best single expert by 16.7%.
- The per-domain best single expert shifts from MASt3R on KITTI to
  Spann3R on ETH3D. This is cross-dataset evidence that the routing
  problem itself depends on the domain.

What is NOT supported and must not be claimed:

- "The router transfers to ETH3D." It does not.
- "The router beats best-single on cross-dataset." It does not (it is
  16.7% worse than `always_spann3r`).
- SOTA, ScanNet, dense-depth ETH3D, 4+ expert. None of these were touched.

## Root Cause Analysis (Why Transfer Fails)

The router input is `[6D regime probs] + [7D normalized stats]`. KITTI's
frozen `stat_mean / stat_std` (used to normalize ETH3D inputs at eval time)
embed KITTI-specific feature support:

- `oxts_available` has stat_mean ~1.0 and stat_std ~1e-6 on KITTI
  (constant per dataset). ETH3D raw value is 0.0; normalized is
  `(0 - 1.0) / 1e-6 = -1e6`, far outside the router's training-time input
  manifold.
- `mean_speed` and `speed_std` have KITTI driving-velocity support
  (~10 m/s). ETH3D's static rig has 0 for both; normalized values are
  ~-1 std from the KITTI mean.

The first MLP layer of `ComposerRouter` was never trained on these
out-of-domain feature values; it produces a degenerate logit pattern that
deterministically picks Fast3R for every ETH3D window.

The right fix is in the router's input design (drop or robustly handle
oxts/motion stats that are KITTI-specific), not in the transfer pipeline
itself. This is recorded as future work below; no fix is attempted in this
decision.

## Stage 5 Status After This Decision

| Sub-stage | State | Evidence |
|---|---|---|
| S1 KITTI in-domain | done | DEC-20260525-003 (59w, 78% LOO) |
| S1 cross-dataset | done | this decision (ETH3D 50w, weak transfer) |
| S2 Permanence | deferred | needs dynamic-scene data, out of scope |
| S3 GaussianHead | deferred | 1-week branch, out of scope |
| S4 ScanNet/ETH3D dense | deferred | dense GT not consumed; 4+ expert deferred |
| S5 tttLRM (real TTT) | deferred | future Track B per HANDOFF |

Stage 5 row in `mainwork.md §5` is updated to `done` with this decision as
the closing DEC.

## Implementation Boundary

Touched (new files):

- `code/dream3r/data/eth3d_long.py`
- `code/dream3r/scripts/generate_eth3d_regime_labels.py`
- `code/dream3r/scripts/build_oracle_expert_labels_eth3d.py`
- `code/dream3r/scripts/eval_cross_domain_router.py`

Not touched (per CLAUDE.md rules):

- `code/dream3r/model.py`
- `code/dream3r/anchor_bank.py`
- `code/dream3r/nsa_attention.py`
- `code/dream3r/bus.py`
- KITTI Stage 5 S1 pipeline (`build_oracle_expert_labels.py`,
  `train_router_only.py`, `eval_router_ablation.py`,
  `eval_router_loo.py`) — reused with no edits.

New server artifacts:

- `/hdd3/kykt26/data/eth3d/low_res_many_view/training/{5 scenes}` (extracted ETH3D)
- `/hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_regime_labels/regime_labels.json`
- `/hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_oracle/oracle_expert_labels.json`
- `/hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_router/results.json`

KITTI S1 artifacts remain unchanged and authoritative.

## Verification

Reproduce end-to-end from a clean clone:

```text
# 1. Extract ETH3D (one-time)
cd /hdd3/kykt26/data/eth3d/low_res_many_view/training && \
  7z x ../raw/multi_view_training_rig_undistorted.7z && \
  7z x ../raw/multi_view_training_rig_scan_eval.7z

# 2. Regime labels
python -m dream3r.scripts.generate_eth3d_regime_labels \
  --root /hdd3/kykt26/data \
  --output /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_regime_labels/regime_labels.json \
  --sequence-length 4 --max-windows-per-scene 10

# 3. Oracle
python -m dream3r.scripts.build_oracle_expert_labels_eth3d \
  --regime-labels /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_regime_labels/regime_labels.json \
  --output /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_oracle/oracle_expert_labels.json \
  --experts fast3r mast3r spann3r --align-scale

# 4. Cross-domain router eval
python -m dream3r.scripts.eval_cross_domain_router \
  --regime-labels /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_regime_labels/regime_labels.json \
  --oracle-labels /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_oracle/oracle_expert_labels.json \
  --router-checkpoint /hdd3/kykt26/checkpoints/router_stage5_s1_expand_v1/latest.pt \
  --kitti-oracle-labels /hdd3/kykt26/code/dream3r/runs/stage5_s1_expand_oracle/oracle_expert_labels.json \
  --output /hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_router/results.json \
  --feature-mode regime_stats
```

## Follow-Up

Future-work items surfaced by this closure (all out of scope for current
Stage 5):

1. **Robust router input design** for cross-domain transfer: drop KITTI-
   specific stats (`oxts_available`, `mean_speed`, `speed_std`) from the
   feature set, or normalize per-domain. Likely requires a new training
   cycle.
2. **ETH3D oracle retrain**: train a router on ETH3D oracle (with LOO)
   to verify ETH3D-side learnability. Mirror DEC-003's KITTI structure
   but with the ETH3D 50-window oracle.
3. **Dense ETH3D depth GT**: project `rig_scan_eval/scan*.ply` into each
   image instead of SfM points3D for higher-density depth supervision.
   Optional; current sparse GT already gives valid abs_rel comparisons.
4. **Multi-domain joint training**: combine KITTI 59w + ETH3D 50w into
   one router training run with a domain-id feature, see if shared
   routing policy is learnable.

None of these are needed to close Stage 5. They are recorded for a future
"cross-domain routing" cycle if and when the project goal moves from demo
to cross-dataset claim.

## Boundary on This Decision

This decision changes no v0.3/v0.5 core code, no KITTI artifacts, and
makes no SOTA or 4+ expert claim. It strictly converts the deferral in
DEC-20260525-005 into a concrete closure with documented evidence
(positive cross-dataset signals: best-expert shifts, oracle distribution
shifts; negative cross-dataset signal: KITTI router does not transfer
zero-shot to ETH3D).
