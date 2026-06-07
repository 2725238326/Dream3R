# Dream3R-RC Result Tables

Date: 2026-06-06

Metric: absolute relative depth error. Lower is better.

## Selected RC Table

| Domain | Best single expert | Oracle | Patch oracle | Dream3R-RC | Shuffle-state control |
| --- | ---: | ---: | ---: | ---: | ---: |
| KITTI | 0.1523 | 0.1360 | 0.0976 | **0.1448** | 0.1521 |
| ETH3D | 0.1585 | 0.1468 | 0.0974 | **0.1475** | 0.2467 |

Interpretation:

- Dream3R-RC beats the best single expert on both reported domains.
- Dream3R-RC remains above the oracle and patch-oracle ceilings; do not claim
  oracle-level performance.
- Correct-state behavior beats the shuffled-state control, which is the key
  release-causality evidence.

## VGGT-Omega Oracle Admission

| Domain | Windows | Old oracle | Oracle with VGGT-Omega | Gain | VGGT wins |
| --- | ---: | ---: | ---: | ---: | ---: |
| KITTI | 50 | 0.1763 | 0.1742 | +1.18% | 2/50 |
| ETH3D | 50 | 0.1419 | 0.1158 | +18.35% | 35/50 |

Interpretation:

- VGGT-Omega is a real optional teacher candidate.
- The evidence is strong for ETH3D/indoor-like windows.
- KITTI evidence is weak, so VGGT-Omega is not a broad release replacement.

## VGGT-Omega 4-Expert State-Control Gate

| Domain | Correct-state | No-state | Shuffle-state | Release verdict |
| --- | ---: | ---: | ---: | --- |
| KITTI | 0.2296 | 0.1966 | 0.2180 | fail |
| ETH3D | 0.0570 | 0.0583 | 0.0598 | narrow pass |

Interpretation:

- KITTI correct-state is worse than no-state and worse than the selected RC.
- ETH3D is strong, but the mixed-domain release gate is not robust enough.
- VGGT-Omega remains a future domain-conditional teacher lane, not the RC.

## Qwen/VLM Semantic Gates

| Gate | Real semantic signal | Control | Verdict |
| --- | ---: | ---: | --- |
| 50-window controller | 0.2365 | shuffle/disabled 0.2365 | fail |
| Held-out calibrated controller | 0.1813 | shuffle 0.1776 | fail |
| Semantic Critic-prior | F1 0.8947 | geometry-only F1 0.9211 | fail |

Interpretation:

- Qwen3-VL semantics did not produce a promotable geometry-control signal.
- Qwen remains diagnostic annotation evidence only.
- Do not include Qwen in RC inference diagrams.

## Recommended Slide Table

| Component | Status | Reason |
| --- | --- | --- |
| Frozen StatePrior + bounded residual | RC | best controlled state-causal result |
| VGGT-Omega | future teacher | ETH3D oracle-positive, KITTI control-negative |
| Qwen3-VL semantics | diagnostic only | fails shuffle/geometry controls |
| Native proposal-free decoder | not ready | not competitive with bounded RC |

