# Dream3R v1.1.0 Method One-Pager

Date: 2026-06-09
Status: current closing one-pager

## One-Line Claim

Dream3R v1.1.0 is a state-conditioned proposal-fusion 3R model package. It
uses existing 3R teacher outputs as candidate geometry, then applies Dream
state, confidence, conflict, and domain policy to produce the final pointmap.

## Current Official Model

```text
version: v1.1.0
candidate: domain_conditional_vggt_teacher
KITTI / ETH3D AbsRel: 0.1448 / 0.0570
stable fallback: v1.0-rc1
```

Domain policy:

```text
KITTI -> v1.0-rc1 bounded StatePrior + residual
ETH3D -> VGGT-Omega-expanded SCF correct-state
```

Metric direction: lower is better.

## Architecture Summary

Dream3R v1.1.0 is a controlled proposal-fusion release package:

1. Real proposal teachers produce candidate geometry.
2. Candidate geometry and confidence are normalized into a proposal bank.
3. Dream state / memory context and conflict score condition fusion.
4. A domain policy selects the verified KITTI or ETH3D branch.
5. The candidate is accepted only because normal-state behavior beats no-state
   and shuffled-state controls.

See `release/ARCHITECTURE_DIAGRAM_V1_1.md` for the current diagram.

## Evidence Boundary

Official state controls:

```text
KITTI normal/no-state/shuffle: 0.1448 / 0.1553 / 0.1521
ETH3D normal/no-state/shuffle: 0.0570 / 0.0583 / 0.0598
```

This supports a narrow release claim: state-conditioned proposal fusion is
useful under the current branch policy and verification protocol.

It does not support a universal SOTA claim.

## Why VGGT-Omega Is In The ETH3D Branch Only

VGGT-Omega is a real admitted backend and a useful teacher:

```text
KITTI oracle gain: +1.18%, VGGT wins 2/50
ETH3D oracle gain: +18.35%, VGGT wins 35/50
```

The earlier broad 4-expert release-control gate failed on KITTI:

```text
KITTI correct-state 0.2296, no-state 0.1966, shuffle-state 0.2180
ETH3D correct-state 0.0570, no-state 0.0583, shuffle-state 0.0598
```

Interpretation: VGGT-Omega is strong on ETH3D/indoor-like windows, while KITTI
keeps the stable fallback branch. The later unified domain-conditional gate is
what promoted `v1.1.0`.

## Why Qwen Is Not In The Official Model

Qwen3-VL semantics were tested as an offline semantic signal, not as geometry.
The controls did not justify promotion:

```text
50-window controller: real/shuffle/disabled all 0.2365
held-out calibrated gate: real 0.1813, shuffle 0.1776
semantic Critic-prior: geometry-only F1 0.9211, real+geometry F1 0.8947
```

Interpretation: Qwen remains diagnostic annotation evidence only.

## Why Foundation3R Is Future Work

Foundation3R and proposal-free decoders have executable contracts and training
entrypoints, but current metrics and state controls are not promotable. The
next proposal-free attempt must change target, data scale, representation, or
architecture before it can challenge the `v1.1.0` release line.

## Final Release Position

Release as:

```text
Dream3R v1.1.0: controlled state-conditioned proposal fusion
```

Do not release as:

```text
proposal-free foundation 3R
image-only geometry model
Qwen-guided geometry model
Foundation3R promotion
universal SOTA
```
