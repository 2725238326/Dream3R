# DEC-20260523-006 — Stage 3 Composer Closure

## Decision

Close Stage 3 as complete.

## Rationale

Stage 3 required two real experts, supervised ComposerRouter training, and an ablation where learned routing beats both single-expert baselines.

The final ablation meets the criterion:

- learned_router `scale_aligned_abs_rel`: 0.1712338803
- always_mast3r `scale_aligned_abs_rel`: 0.2048148634
- always_fast3r `scale_aligned_abs_rel`: 0.2222443298
- route/regime Cramer's V: 1.0

The learned router selected Fast3R for dynamic_scene sequences and MASt3R for outdoor_static, sparse_view, and dense_sequential sequences, matching the oracle labels.

## Implementation Boundary

No closed core forward path was modified. The work added scripts and tests around:

- Fast3R real adapter loading
- KITTI regime label generation
- real expert oracle metric generation
- supervised `ComposerRouter` checkpoint training
- offline router ablation

The raw abs-rel oracle run selected MASt3R for all 8 sampled sequences. We therefore use an explicit scale-aligned abs-rel metric for Stage 3 so routing is not dominated by cross-expert depth scale conventions.

## Verification

- Local full suite: `219 passed, 2 skipped`
- Server full suite: `217 passed, 2 skipped`
- Stage 3 artifacts:
  - `/hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json`
  - `/hdd3/kykt26/code/dream3r/runs/stage3_oracle_labels/oracle_expert_labels.json`
  - `/hdd3/kykt26/checkpoints/router_only_v1/latest.pt`
  - `/hdd3/kykt26/code/dream3r/runs/stage3_router_ablation/results.json`

## Follow-Up

Stage 4 should replace the remaining Critic/Repair scaffold with real conflict labels and repair-triggered expert rerouting. The Stage 3 router checkpoint is ready to provide the reroute target distribution once Critic produces real triggers.
