# Cycle 20260606: Domain-Conditional VGGT Teacher

Date: 2026-06-06
Status: closed experimental-positive, not official
Decision: `decisions/DEC-20260606-039-domain-conditional-vggt-teacher.md`

## Goal

Continue optimization without repeating NativeStudent loss sweeps or editing
frozen core files.

## Action

Added a read-only evaluator for a domain-conditional teacher rule:

```text
KITTI -> Dream3R v1.0-rc1 bounded StatePrior + residual
ETH3D -> VGGT-Omega-expanded SCF correct-state
```

## Result

```text
KITTI: 0.1448
ETH3D: 0.0570
ETH3D gain vs RC: 61.36%
```

Controls:

```text
KITTI bounded state < bounded shuffle
ETH3D VGGT state < VGGT no-state
ETH3D VGGT state < VGGT shuffle
```

## Boundary

The candidate passes domain-wise controls but is not an official replacement
for v1.0-rc1 because it does not yet come from a unified domain-conditional
benchmark/control rerun.

## Artifacts

```text
code/dream3r/scripts/eval_domain_conditional_teacher.py
code/dream3r/tests/test_domain_conditional_teacher.py
runs/v22_admission/domain_conditional_teacher/domain_conditional_candidate.json
runs/v22_admission/domain_conditional_teacher/domain_conditional_candidate_server.json
```
