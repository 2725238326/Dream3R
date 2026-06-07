# Dream3R Release Candidate Card

Date: 2026-06-05
Status: release candidate selected

## Selected Candidate

```text
frozen StatePrior + bounded residual refinement
```

This is the current release candidate because it is the best bounded,
state-causal result in the workspace:

```text
KITTI: 0.1448
ETH3D: 0.1475
```

## Why Not VGGT-Omega As The Release Model

VGGT-Omega is now a real admitted backend and a useful teacher candidate, but
the release-control gate failed.

Oracle admission:

```text
KITTI 50: +1.18% oracle gain, VGGT wins 2/50
ETH3D 50: +18.35% oracle gain, VGGT wins 35/50
```

SCF state controls:

```text
KITTI correct-state 0.2296, no-state 0.1966, shuffle 0.2180
ETH3D correct-state 0.0570, no-state 0.0583, shuffle 0.0598
```

This means VGGT-Omega is a strong domain-conditional teacher, especially for
ETH3D/indoor-like windows, but not yet a publishable state-causal Dream3R
model path.

## Release Claim

Dream3R-RC is a bounded state-conditioned proposal-fusion candidate that:

- uses real MASt3R/Fast3R/Spann3R proposal caches;
- uses a frozen StatePrior path;
- applies bounded residual refinement;
- preserves state-causality against shuffled-state controls.

## Non-Claim

This release candidate does not claim:

- SOTA performance;
- VGGT-Omega-based final model quality;
- Qwen/VLM geometry capability;
- a native proposal-free Dream3R decoder;
- full long-sequence streaming deployment.
