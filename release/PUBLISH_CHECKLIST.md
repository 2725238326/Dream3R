# Dream3R-RC Publish Checklist

Date: 2026-06-06

## Tonight Usable Package

```text
version: v1.1-rc1
api: dream3r.release_v11.build_dream3r_v11_release
KITTI / ETH3D: 0.1448 / 0.0570
doc: release/USABLE_MODEL_V1_1.md
verify: code/dream3r/scripts/verify_v11_release.py
```

The stable official fallback remains `v1.0-rc1`.

## Ready

- Release candidate selected:

```text
frozen StatePrior + bounded residual refinement
```

- Selected metrics documented:

```text
KITTI abs-rel: 0.1448
ETH3D abs-rel: 0.1475
```

- State-causality controls documented:

```text
correct-state KITTI/ETH3D: 0.1448 / 0.1475
shuffle-state KITTI/ETH3D: 0.1521 / 0.2467
```

- VGGT-Omega admitted as real backend but excluded from RC.
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

Stop broad model exploration. For tonight, use `v1.1-rc1`; keep `v1.0-rc1`
as the stable fallback.

The next work should be presentation and manuscript packaging unless a new
experiment is explicitly scoped with a release gate and a rollback plan.
