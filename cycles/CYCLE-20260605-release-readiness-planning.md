# Cycle 20260605: Release Readiness Planning

Date: 2026-06-05
Status: planning closed; next execution gate identified
Decision: `decisions/DEC-20260605-036-dream3r-release-readiness-gate.md`

## Goal

Convert the current Dream3R research state into a publishable-candidate path
with explicit stop gates, instead of continuing broad model exploration.

## Current Truth

- Current best bounded baseline: KITTI/ETH3D `0.1448/0.1475`.
- Qwen gates: not promotable.
- VGGT-Omega: one-window real-backend smoke admitted.
- VGGT-Omega oracle/cache admission: not yet run.
- New evaluator: implemented locally and local tests pass.
- Server sync for the evaluator: interrupted by SSH reset.

## New Local Surface

```text
code/dream3r/scripts/eval_vggt_omega_oracle_admission.py
code/dream3r/tests/test_vggt_integration.py
```

Local verification:

```text
25 passed
```

## Next Gate

Run 5 KITTI + 5 ETH3D VGGT-Omega oracle admission against the existing
MASt3R/Fast3R/Spann3R SCF caches.

Expected output:

```text
runs/v22_admission/vggt_omega_oracle/tiny_oracle_admission_5x2_20260605.json
```

## Branching Logic

If VGGT-Omega improves oracle ceiling:

1. build a 20-50 window VGGT-expanded cache;
2. run SCF/proposal-set decoder controls;
3. compare against `0.1448/0.1475`;
4. package the better state-causal candidate.

If VGGT-Omega does not improve oracle ceiling:

1. stop VGGT-Omega release work;
2. package frozen-StatePrior + bounded residual as the release candidate;
3. document VGGT-Omega as a real but non-improving optional teacher.

## Boundary

No frozen core edit. No Qwen promotion. No release claim until oracle/cache
admission and state-causality controls pass or the fallback release candidate is
explicitly selected.
