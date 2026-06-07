# DEC-20260606-040: Unified domain-conditional gate

Date: 2026-06-06
Status: accepted as v1.1 promotion candidate; not packaged official
Scope: Dream3R post-v1.0-rc1 promotion gate

## Context

DEC-039 identified a domain-conditional policy:

```text
KITTI -> Dream3R v1.0-rc1 bounded StatePrior + residual
ETH3D -> VGGT-Omega-expanded SCF correct-state
```

The previous blocker was the lack of one explicit gate with matching state,
no-state, and shuffle controls across the declared domain policy.

## Decision

Add and run a read-only unified gate over the declared policy. The gate does
not train a model, edit frozen core files, or promote the official version by
itself.

Promotion requires all controls to separate:

```text
KITTI state < KITTI no-state
KITTI state < KITTI shuffle
ETH3D state < ETH3D no-state
ETH3D state < ETH3D shuffle
```

## Implementation

Added:

```text
code/dream3r/scripts/eval_unified_domain_conditional_gate.py
code/dream3r/tests/test_unified_domain_conditional_gate.py
```

The evaluator reads existing JSON artifacts and emits blockers instead of
silently promoting. It also accepts the server directory artifact convention
and the local flat mirror convention for VGGT control JSON files.

## Result

BUAA-Server output:

```text
runs/v22_admission/domain_conditional_teacher/unified_gate_candidate_with_kitti_no_state_server.json
```

Metrics:

```text
KITTI state/no-state/shuffle: 0.1448 / 0.1553 / 0.1521
ETH3D state/no-state/shuffle: 0.0570 / 0.0583 / 0.0598
```

Controls:

```text
KITTI state beats no-state: true
KITTI state beats shuffle: true
ETH3D state beats no-state: true
ETH3D state beats shuffle: true
```

Gate verdict:

```text
status: pass
promotion_blockers: []
promotable_to_official: true
```

Verification:

```text
local pytest: test_unified_domain_conditional_gate.py passed
BUAA-Server pytest: test_unified_domain_conditional_gate.py passed
BUAA-Server gate: status pass
```

## Boundary

This is a v1.1 promotion candidate, not a silent replacement for v1.0-rc1.
The official package remains:

```text
Dream3R v1.0-rc1
frozen StatePrior + bounded residual
KITTI / ETH3D: 0.1448 / 0.1475
```

Replacing it requires a deliberate v1.1 package update: version identity,
artifact manifest, verifier, reproducibility notes, and release docs.

## Rejected

- Rejected promoting raw VGGT-Omega 4-expert SCF globally, because KITTI
  release controls are weaker than the v1.0-rc1 path.
- Rejected more NativeStudent loss sweeps as the immediate route, because the
  latest objective gates stayed flat at `0.1451 / 0.1480`.
- Rejected Qwen-based geometry promotion, because Qwen gates remain diagnostic
  and non-promotable.
