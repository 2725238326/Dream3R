# Dream3R-RC Method One-Pager

Date: 2026-06-06

## One-Line Claim

Dream3R-RC is a bounded state-conditioned proposal-fusion model that uses
Dream state only when it survives state-causality controls.

## Current Release Candidate

```text
frozen StatePrior + bounded residual refinement
```

Selected metrics:

```text
KITTI abs-rel: 0.1448
ETH3D abs-rel: 0.1475
```

Metric direction: lower is better.

## Architecture Summary

Dream3R-RC does not claim to be a proposal-free geometry foundation model.
It is a controlled proposal-fusion release candidate:

1. Real proposal teachers produce candidate geometry.
2. A learned StatePrior path estimates state-conditioned proposal preference.
3. The StatePrior is frozen before residual refinement.
4. A bounded residual refinement improves the fused output without allowing
   joint training to overwrite the state prior.
5. The candidate is accepted only if correct-state behavior beats shuffled
   state controls.

See `release/METHOD_FIGURE.md` for the presentation diagram.

## Evidence Boundary

The selected RC is supported by:

```text
correct-state KITTI/ETH3D: 0.1448 / 0.1475
shuffle-state KITTI/ETH3D: 0.1521 / 0.2467
```

This supports a narrow release claim: state-conditioned proposal fusion is
useful under the current bounded setup.

It does not support a broad SOTA claim.

See `release/RESULT_TABLE.md` for the compact result tables.

## Why VGGT-Omega Is Not The RC

VGGT-Omega is now a real admitted backend and a useful future teacher:

```text
KITTI oracle gain: +1.18%, VGGT wins 2/50
ETH3D oracle gain: +18.35%, VGGT wins 35/50
```

But the release-control gate failed:

```text
KITTI correct-state 0.2296, no-state 0.1966, shuffle-state 0.2180
ETH3D correct-state 0.0570, no-state 0.0583, shuffle-state 0.0598
```

Interpretation: VGGT-Omega is strong on ETH3D/indoor-like windows, but the
current 4-expert state-conditioned cache gate is not a robust release path.

## Why Qwen Is Not In The RC

Qwen3-VL semantics were tested as an offline semantic signal, not as geometry.
The controls did not justify promotion:

```text
50-window controller: real/shuffle/disabled all 0.2365
held-out calibrated gate: real 0.1813, shuffle 0.1776
semantic Critic-prior: geometry-only F1 0.9211, real+geometry F1 0.8947
```

Interpretation: Qwen remains diagnostic annotation evidence only.

## Honest Release Position

Release as:

```text
Dream3R-RC: controlled state-conditioned proposal fusion
```

Do not release as:

```text
SOTA 3R model
VGGT-Omega Dream3R
Qwen-guided geometry model
proposal-free native decoder
```

## Next Research Lane

The next high-value research lane is domain-conditional teacher integration:
use VGGT-Omega where its oracle evidence is strong, while keeping KITTI and
state-causality controls as hard gates.
