# Cycle 20260605: VGGT-Omega Cache/Control Gate

Date: 2026-06-05
Status: closed oracle-positive, release-control negative
Decision: `decisions/DEC-20260605-037-vggt-omega-cache-control-gate.md`

## Goal

Determine whether VGGT-Omega can become the release model path, not just an
admitted smoke backend.

## Actions

1. Synced `eval_vggt_omega_oracle_admission.py` and VGGT tests to BUAA-Server.
2. Ran server tests: 27 passed.
3. Ran 5+5, 20+20, and 50+50 oracle admission.
4. Extended the evaluator to write 4-expert SCF caches.
5. Ran VGGT-expanded SCF correct-state / no-state / shuffle-state controls.

## Result

Oracle admission is positive:

```text
KITTI 50: old 0.1763 -> new 0.1742, +1.18% oracle gain, VGGT wins 2/50
ETH3D 50: old 0.1419 -> new 0.1158, +18.35% oracle gain, VGGT wins 35/50
```

State-causality release control is negative:

```text
KITTI correct-state 0.2296 vs no-state 0.1966 vs shuffle 0.2180
ETH3D correct-state 0.0570 vs no-state 0.0583 vs shuffle 0.0598
```

## Boundary

No frozen core edit. No Qwen promotion. VGGT-Omega should not be marketed as
the publishable Dream3R model. It is a real teacher/proposal source with strong
ETH3D evidence and weak KITTI evidence.

## Next

Package frozen StatePrior + bounded residual as the release candidate:

```text
KITTI/ETH3D: 0.1448 / 0.1475
```

Keep VGGT-Omega in the release notes as an admitted optional teacher and future
domain-conditional proposal source.
