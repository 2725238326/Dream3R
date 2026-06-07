# Dream3R v1.1 Publish Checklist

Date: 2026-06-08

## Complete Usable Package

```text
version: v1.1.0
api: dream3r.release_v11.build_dream3r_v11_release
KITTI / ETH3D: 0.1448 / 0.0570
doc: release/COMPLETE_MODEL_V1_1.md
verify: code/dream3r/scripts/verify_v11_release.py
smoke: code/dream3r/scripts/smoke_v11_release_model.py
```

The stable fallback remains `v1.0-rc1`.

## Ready

- Current effective model selected:

```text
domain-conditional state-conditioned proposal fusion
```

- Selected metrics documented:

```text
KITTI abs-rel: 0.1448
ETH3D abs-rel: 0.0570
```

- State-causality controls documented:

```text
KITTI state/no-state/shuffle: 0.1448 / 0.1553 / 0.1521
ETH3D state/no-state/shuffle: 0.0570 / 0.0583 / 0.0598
```

- Full-model smoke command added and run locally/server-side.
- v1.0 fallback verifier remains green.
- VGGT-Omega admitted as real backend and used only through the ETH3D branch.
- Qwen semantics excluded from RC.
- Reproduction notes written.
- Verification report written.
- Limitations and non-claims written.

## Must Not Claim

- SOTA performance.
- VGGT-Omega final model quality.
- Qwen/VLM geometry capability.
- Proposal-free native Dream3R decoding.
- Full long-sequence streaming deployment.

## Submit-Ready Minimum

Before external release or paper/demo circulation, prepare:

- A short method figure showing proposal teachers, StatePrior, frozen prior,
  bounded residual refinement, and shuffle-state control. Draft:
  `release/METHOD_FIGURE.md`.
- A compact result table with KITTI, ETH3D, best single expert, oracle, RC, and
  shuffled-state control. Draft: `release/RESULT_TABLE.md`.
- A limitations paragraph copied from `release/LIMITATIONS.md`.
- A reproducibility appendix pointing to `release/REPRODUCE.md`.
- A non-claims appendix pointing to `release/NON_CLAIMS.md`.

## Optional But Useful

- A one-slide VGGT-Omega teacher analysis:

```text
ETH3D oracle-positive, KITTI release-control-negative
```

- A one-slide Qwen analysis:

```text
semantic annotations diagnostic only; no Router/Critic promotion
```

- A short artifact manifest screenshot or table from `release/ARTIFACTS.json`.
- A slide sequence from `release/PRESENTATION_OUTLINE.md`.

## Current Stop Condition

Stop broad model exploration. For tonight, use `v1.1.0`; keep `v1.0-rc1`
as the stable fallback.

The next work should be presentation and manuscript packaging unless a new
experiment is explicitly scoped with a release gate and a rollback plan.
