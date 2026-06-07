# Cycle 20260606: Native Student Objective Gates

Date: 2026-06-06
Status: closed implemented, causal, release-negative
Decision: `decisions/DEC-20260606-038-native-student-objective-gates.md`

## Goal

Try the smallest reversible native-student optimization that could improve the
release candidate without touching frozen core files.

## Actions

1. Added optional dropout-consistency, temporal proxy, and scale-drift proxy
   losses to `train_native_student_decoder.py`.
2. Added sweep-script environment flags for the new objective weights.
3. Added unit tests for target detachment and differentiable proxy losses.
4. Synced the changed trainer, sweep wrapper, and tests to BUAA-Server.
5. Ran local and server tests.
6. Ran GPU1 smoke and gate20 controls for P1 and P2.
7. Mirrored gate20 result directories back into local `runs/stage6_fusion/`.

## Result

P1 dropout-consistency gate20:

```text
correct-state: 0.1451 / 0.1480
no-state:      0.1557 / 0.1730
shuffle-state: 0.1525 / 0.2468
fallback:      0
```

P2 dropout + temporal/scale gate20:

```text
correct-state: 0.1451 / 0.1480
no-state:      0.1557 / 0.1730
shuffle-state: 0.1525 / 0.2468
fallback:      0
```

The controls remain causal, but neither gate beats the release candidate:

```text
RC: 0.1448 / 0.1475
```

## Boundary

No frozen core files were edited. Qwen remains diagnostic. VGGT-Omega remains a
future teacher lane and not the RC.

## Next

Do not continue blind native objective sweeps. The release candidate should be
packaged as frozen-StatePrior + bounded residual. If model improvement is still
required, the next meaningful optimization surface is a larger bounded redesign,
not another pass over the same loss weights.
