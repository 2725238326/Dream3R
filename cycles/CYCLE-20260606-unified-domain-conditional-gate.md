# Cycle 20260606: Unified Domain-Conditional Gate

Date: 2026-06-06
Status: closed positive; v1.1 promotion candidate
Decision: `decisions/DEC-20260606-040-unified-domain-conditional-gate.md`

## Goal

Close the previous architecture blocker by running one declared gate for the
domain-conditional policy:

```text
KITTI -> Dream3R v1.0-rc1 bounded StatePrior + residual
ETH3D -> VGGT-Omega-expanded SCF correct-state
```

## Action

Added a read-only evaluator and regression tests:

```text
code/dream3r/scripts/eval_unified_domain_conditional_gate.py
code/dream3r/tests/test_unified_domain_conditional_gate.py
```

Ran the gate locally and on BUAA-Server after adding the missing KITTI no-state
control artifact.

## Result

BUAA-Server artifact:

```text
runs/v22_admission/domain_conditional_teacher/unified_gate_candidate_with_kitti_no_state_server.json
```

Metrics:

```text
KITTI state/no-state/shuffle: 0.1448 / 0.1553 / 0.1521
ETH3D state/no-state/shuffle: 0.0570 / 0.0583 / 0.0598
```

Verdict:

```text
status: pass
promotion_blockers: []
promotable_to_official: true
```

## Boundary

The official release remains `v1.0-rc1` until a deliberate v1.1 package is
made. The next task is packaging/verifier work, not another architecture
branch or more Qwen/NativeStudent retries.

## Verification

```text
local:       test_unified_domain_conditional_gate.py passed
BUAA-Server: test_unified_domain_conditional_gate.py passed
BUAA-Server: eval_unified_domain_conditional_gate.py status pass
```
