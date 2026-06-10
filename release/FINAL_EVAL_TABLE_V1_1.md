# Dream3R v1.1.0 Final Evaluation Table

Date: 2026-06-10

This table summarizes existing verified release artifacts. It is not a new benchmark rerun.

## Official v1.1.0 Metrics

| Domain | Policy | Correct-state AbsRel | No-state AbsRel | Shuffle-state AbsRel | Controls | Source |
| --- | --- | ---: | ---: | ---: | --- | --- |
| KITTI | Dream3R v1.0-rc1 bounded StatePrior + residual | 0.1448 | 0.1553 | 0.1521 | pass | `runs/v22_admission/domain_conditional_teacher/unified_gate_candidate_with_kitti_no_state_server.json` |
| ETH3D | VGGT-Omega-expanded SCF correct-state | 0.0570 | 0.0583 | 0.0598 | pass | `runs/v22_admission/domain_conditional_teacher/unified_gate_candidate_with_kitti_no_state_server.json` |

## Stable Fallback

| Model | KITTI AbsRel | ETH3D AbsRel | Source |
| --- | ---: | ---: | --- |
| v1.0-rc1 frozen StatePrior + bounded residual | 0.1448 | 0.1475 | `runs/stage6_fusion/bounded_refine_sweep/frozen_prior_state_seed_7/results.json` |

## Runtime Cache Demo

| Domain | Status | Entries run | Matched cache entries | Mean AbsRel vs cache GT | Source |
| --- | --- | ---: | ---: | ---: | --- |
| KITTI | pass | 1 | 246/246 | 0.1479 | `runs/release/v11_cache_demo/cache_demo_kitti.json` |
| ETH3D | pass | 1 | 50/50 | 0.0815 | `runs/release/v11_cache_demo/cache_demo_eth3d.json` |

## Fusion Improvement Attempt

| Candidate | Mechanism | Metric gate | Verdict | Source |
| --- | --- | --- | --- | --- |
| v1.1.1-candidate-conflict-dampening | ETH3D SCF conflict_dampening_strength=0.35 logit shrinkage | not_evaluated_on_real_benchmark | neutral_not_promoted_keep_v1.1.0_official | `runs/release/v11_final_eval/conflict_dampening_attempt.json` |

## Claim Boundary

- Safe claim: Dream3R v1.1.0 is a state-conditioned proposal-fusion 3R release package.
- Not claimed: proposal-free foundation 3R, image-only inference, Qwen geometry, universal SOTA, or long-sequence deployment.
- Qwen, Foundation3R, proposal-free decoding, and v1.2-exp0 remain non-official unless future controls pass.
