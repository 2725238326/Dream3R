# DEC-20260606-039: Domain-conditional VGGT teacher candidate

Date: 2026-06-06
Status: accepted as experimental optimization candidate; not official release
Scope: Dream3R post-v1.0-rc1 optimization

## Context

The official release candidate remains:

```text
Dream3R v1.0-rc1
frozen StatePrior + bounded residual
KITTI / ETH3D: 0.1448 / 0.1475
```

NativeStudent objective gates were causal but flat, so the next meaningful
optimization surface is the already-admitted VGGT-Omega teacher.

VGGT evidence is domain-asymmetric:

```text
KITTI oracle gain: +1.18%, VGGT wins 2/50
ETH3D oracle gain: +18.35%, VGGT wins 35/50
```

## Decision

Evaluate a domain-conditional teacher policy:

```text
KITTI -> v1.0-rc1 bounded StatePrior + residual
ETH3D -> VGGT-Omega-expanded SCF correct-state
```

This is not a new official release because the KITTI and ETH3D artifacts are
domain-wise artifacts from different gates, not one unified benchmark/control
rerun.

## Implementation

Added:

```text
code/dream3r/scripts/eval_domain_conditional_teacher.py
code/dream3r/tests/test_domain_conditional_teacher.py
```

The evaluator is read-only. It combines existing result JSON files and reports
domain-wise controls plus a promotion blocker.

## Result

Local and server outputs:

```text
runs/v22_admission/domain_conditional_teacher/domain_conditional_candidate.json
runs/v22_admission/domain_conditional_teacher/domain_conditional_candidate_server.json
```

Metrics:

```text
KITTI: 0.1448  (same as v1.0-rc1)
ETH3D: 0.0570  (vs v1.0-rc1 ETH3D 0.1475)
ETH3D relative gain vs RC: 61.36%
```

Controls:

```text
KITTI bounded state beats shuffle: true
ETH3D VGGT state beats no-state: true
ETH3D VGGT state beats shuffle: true
```

Server verification:

```text
test_domain_conditional_teacher.py: 1 passed
eval_domain_conditional_teacher.py: output written on BUAA-Server
```

## Verdict

This is the best current optimization direction:

```text
passes_domainwise_controls: true
promotable_to_official: false
```

It should become the next official candidate only after a unified
domain-conditional cache/control rerun that uses one declared evaluation
protocol for both domains.
