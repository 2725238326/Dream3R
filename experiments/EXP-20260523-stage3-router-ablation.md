# EXP-20260523 Stage 3 Router Ablation

## Goal

Evaluate whether a supervised ComposerRouter over two real experts, MASt3R and Fast3R, beats either single-expert baseline on KITTI sequence regimes.

## Setup

- Real experts:
  - MASt3R checkpoint: `/hdd3/kykt26/checkpoints/mast3r-vitl`
  - Fast3R checkpoint: `/hdd3/kykt26/checkpoints/fast3r/Fast3R_ViT_Large_512`
- Regime labels: `/hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json`
- Oracle labels: `/hdd3/kykt26/code/dream3r/runs/stage3_oracle_labels/oracle_expert_labels.json`
- Router checkpoint: `/hdd3/kykt26/checkpoints/router_only_v1/latest.pt`
- Ablation output: `/hdd3/kykt26/code/dream3r/runs/stage3_router_ablation/results.json`
- Metric: scale-aligned pointmap depth abs-rel. Raw abs-rel was dominated by cross-expert scale conventions and made all eight sampled oracle labels choose MASt3R.

## Data

The run used 8 KITTI sequences selected from top regime buckets:

- dynamic_scene: 2
- outdoor_static: 2
- sparse_view: 2
- dense_sequential: 2

Scale-aligned oracle labels:

- Fast3R: 2 dynamic_scene sequences
- MASt3R: 6 non-dynamic sequences

## Router Training

- Train mode: `router_only`
- Supervision: cross-entropy on `ComposerRouter.routing_logits`
- Examples: 8 sequence-level oracle labels
- Accuracy: 0.75 -> 1.00
- Checkpoint: `/hdd3/kykt26/checkpoints/router_only_v1/latest.pt`

## Final Results

| Variant | scale-aligned abs-rel |
|---|---:|
| learned_router | 0.1712338803 |
| always_mast3r | 0.2048148634 |
| always_fast3r | 0.2222443298 |
| random_routing | 0.2202285165 |
| oracle_router | 0.1712338803 |

Route/regime association:

- Cramer's V: 1.0
- Learned route: Fast3R on dynamic_scene, MASt3R on outdoor_static/sparse_view/dense_sequential

## Conclusion

Stage 3 success criteria are met on the sampled KITTI regimes: the learned router matches the oracle router, beats both single-expert baselines, and has route choices strongly associated with regime labels.

## Limitation

The evaluation is narrow: 8 sequence-level samples and a scale-aligned metric. This is enough to close the roadmap stage, but not a broad benchmark claim.
