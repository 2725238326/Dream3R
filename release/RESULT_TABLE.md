# Dream3R v1.1.0 Result Tables

Date: 2026-06-09
Status: current official result table plus historical fallback context

Metric: absolute relative depth error. Lower is better.

## Current Official Model

| Version | KITTI AbsRel | ETH3D AbsRel | Role |
| --- | ---: | ---: | --- |
| `v1.0-rc1` | 0.1448 | 0.1475 | stable fallback |
| `v1.1.0` | 0.1448 | 0.0570 | official final deliverable |

Interpretation:

- `v1.1.0` preserves the stable KITTI branch from `v1.0-rc1`.
- `v1.1.0` uses the VGGT-Omega-expanded state-conditioned fusion branch for
  ETH3D, where the verified candidate is stronger.
- The current official claim is narrow: state-conditioned proposal fusion with
  a domain policy, not a universal SOTA model.

## Official State-Control Table

| Domain | Normal state | No-state | Shuffle-state | Verdict |
| --- | ---: | ---: | ---: | --- |
| KITTI | 0.1448 | 0.1553 | 0.1521 | pass |
| ETH3D | 0.0570 | 0.0583 | 0.0598 | pass |

Interpretation:

- Correct-state behavior beats both controls on both official domains.
- This table is the state-causality table to use in final report and defense
  material.

## Historical v1.0 RC Fallback Table

The table below is retained as historical `v1.0-rc1` fallback evidence. Do not
use it as the current official `v1.1.0` result table.

| Domain | Best single expert | Oracle | Patch oracle | `v1.0-rc1` | Shuffle-state control |
| --- | ---: | ---: | ---: | ---: | ---: |
| KITTI | 0.1523 | 0.1360 | 0.0976 | 0.1448 | 0.1521 |
| ETH3D | 0.1585 | 0.1468 | 0.0974 | 0.1475 | 0.2467 |

## Historical VGGT-Omega Admission Evidence

This table explains why VGGT-Omega became the ETH3D branch teacher, not why it
replaced every branch.

| Domain | Windows | Old oracle | Oracle with VGGT-Omega | Gain | VGGT wins |
| --- | ---: | ---: | ---: | ---: | ---: |
| KITTI | 50 | 0.1763 | 0.1742 | +1.18% | 2/50 |
| ETH3D | 50 | 0.1419 | 0.1158 | +18.35% | 35/50 |

Historical 4-expert state-control gate before the unified domain policy:

| Domain | Correct-state | No-state | Shuffle-state | Historical verdict |
| --- | ---: | ---: | ---: | --- |
| KITTI | 0.2296 | 0.1966 | 0.2180 | fail for broad release |
| ETH3D | 0.0570 | 0.0583 | 0.0598 | narrow pass |

Interpretation:

- The old mixed 4-expert gate failed on KITTI.
- The later unified domain-conditional gate fixed the release policy by keeping
  KITTI on `v1.0-rc1` and using VGGT-Omega only for ETH3D.

## Qwen/VLM Semantic Gates

| Gate | Real semantic signal | Control | Verdict |
| --- | ---: | ---: | --- |
| 50-window controller | 0.2365 | shuffle/disabled 0.2365 | fail |
| Held-out calibrated controller | 0.1813 | shuffle 0.1776 | fail |
| Semantic Critic-prior | F1 0.8947 | geometry-only F1 0.9211 | fail |

Interpretation:

- Qwen3-VL semantics did not produce a promotable geometry-control signal.
- Qwen remains diagnostic annotation evidence only.
- Do not include Qwen in official inference diagrams.

## Final Defense Summary Table

| Component | Current status | Reason |
| --- | --- | --- |
| `v1.1.0` domain policy | official | both domain controls pass |
| `v1.0-rc1` | stable fallback | conservative KITTI/stability anchor |
| VGGT-Omega | official ETH3D branch teacher | ETH3D evidence strong, KITTI broad gate failed historically |
| Qwen3-VL semantics | diagnostic only | fails semantic geometry controls |
| Foundation3R proposal-free | future research | not competitive or state-causal enough for promotion |
