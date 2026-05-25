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
