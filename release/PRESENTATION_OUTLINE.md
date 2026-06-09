# Dream3R v1.1.0 Final Presentation Outline

Date: 2026-06-09
Status: current closing/final-defense outline

This file supersedes the earlier `Dream3R-RC` outline for presentation use.
The old `v1.0-rc1` outline is now historical fallback material only.

## Current Presentation Claim

```text
Dream3R v1.1.0 is a runnable and verifiable state-conditioned
proposal-fusion 3R model package.
```

Main metric:

```text
KITTI / ETH3D AbsRel: 0.1448 / 0.0570
```

Stable fallback:

```text
v1.0-rc1, KITTI / ETH3D AbsRel: 0.1448 / 0.1475
```

## Recommended Slide Flow

1. Problem: front-feed 3R models now produce diverse candidate geometry.
2. Model identity: `v1.1.0` is proposal-fusion, not proposal-free foundation 3R.
3. Architecture: images -> teachers -> proposal bank -> Dream state/conflict -> domain policy -> pointmap.
4. Branch policy: KITTI keeps `v1.0-rc1`; ETH3D uses VGGT-Omega-expanded SCF.
5. Main result table: `v1.1.0` keeps KITTI stable and improves ETH3D.
6. State controls: normal/no-state/shuffle pass on both domains.
7. VGGT-Omega status: ETH3D teacher branch, not the whole model.
8. Verification: verifier, smoke, demo, fallback verifier, cache-demo evidence.
9. Non-promoted branches: Qwen, Foundation3R, `v1.2-exp0`.
10. Deliverables: release docs, scripts, final report, final PPT.
11. Limitations: proposal-bank dependency, narrow domains, real-cache demo boundary.
12. Conclusion: clear official model package with honest non-claims.

## Use These Current Tables

Main model:

| Version | KITTI | ETH3D | Role |
| --- | ---: | ---: | --- |
| `v1.0-rc1` | 0.1448 | 0.1475 | stable fallback |
| `v1.1.0` | 0.1448 | 0.0570 | official final deliverable |

State controls:

| Domain | Normal | No-state | Shuffle-state |
| --- | ---: | ---: | ---: |
| KITTI | 0.1448 | 0.1553 | 0.1521 |
| ETH3D | 0.0570 | 0.0583 | 0.0598 |

Non-promoted branch table:

| Branch | Status | Reason |
| --- | --- | --- |
| Qwen3-VL semantics | diagnostic only | no stable geometry-control gain |
| Foundation3R proposal-free | future research | metrics and state controls are not promotable |
| `v1.2-exp0` core bridge | experimental | no real-cache metric/control promotion |

## Final Deck Artifact

The current editable deck is:

```text
reports/pptx/Dream3R_Final_Defense_20260609.pptx
```

The source outline and script are:

```text
reports/final/DREAM3R_FINAL_PPT_OUTLINE_AND_SCRIPT_20260609.md
```

## Claim Boundary

Safe:

```text
state-conditioned proposal-fusion 3R release package
```

Do not claim:

```text
proposal-free foundation 3R
image-only inference
Qwen geometry model
Foundation3R promotion
universal SOTA
```
