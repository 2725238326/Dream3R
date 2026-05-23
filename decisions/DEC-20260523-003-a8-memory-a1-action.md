# DEC-20260523-003: Close v0.5 Axis A8 - Memory A1 sub-action scaffold

decision_id: DEC-20260523-003
date: 2026-05-23
axis: A8
parent_spec: SPEC-20260522-001-dream3r-v05-axes.md
evidence_cycle: CYCLE-20260523-002
status: proposed (pending user ratification)

---

## Decision

**Close Axis A8 as a policy-scaffold closure.**

Dream3R now has a typed Memory A1 sub-action vocabulary, a state-update policy module, and a W25 plan for replacing the scaffolded test-time-training updater with a real tttLRM-style gradient step. This closes the v0.5 design/code gap where A1 sub-actions existed only in the Memory finalist spec and had no concrete code vocabulary.

This DEC does **not** claim that the tttLRM-style update is trained, quality-improving, or server-validated. Those claims are deferred to W25.

## closes_iff satisfaction

Per SPEC-20260522-001 §A8:

| Criterion | Satisfied | Evidence |
|---|---|---|
| A1 sub-action enum added with names matching SPEC-20260503-002 | Yes | `memory_action.py` `MemoryA1Action` defines 6 actions: `full_update`, `pose_adaptive_update`, `kalman_update`, `skip_update`, `reset_state`, `test_time_train` |
| `SpatialMemory.forward` or new policy chooses among A1 sub-actions from evidence/drift/conflict signals | Yes | `StateUpdatePolicy` consumes `drift_proxy`, `conflict_score`, `confidence_mean`, and `window_index` |
| tttLRM-style sub-action implemented as distinct from `full_update` | Deferred / scaffolded | `TEST_TIME_TRAIN` exists and `TTTStateUpdater` is separate, but the real gradient step is intentionally deferred to W25 |
| W25 `TTT_PLAN.md` drafted | Yes | `planning/TTT_PLAN.md` defines milestones, risks, dependencies, and exit criteria |
| server tick records policy choosing tttLRM-style A1 on a long sequence | Deferred | Requires W25 training/integration run after the scaffold is connected to long-sequence evaluation |

## Waived sub-conditions

The trained tttLRM update and server tick are waived for this v0.5 scaffold closure. They require a real self-supervised TTT loss, trained policy behavior, and a long-sequence server run. `planning/TTT_PLAN.md` records those as W25 milestones rather than claiming them here.

## Consequence

- Memory A1 now has a concrete, testable sub-action vocabulary.
- `StateUpdatePolicy` can emit typed `A1PolicyDecision` objects for batch elements.
- `TTTStateUpdater` provides a shape-safe scaffold and keeps the future real gradient-step implementation isolated.
- A8 moves from "no code path selects among A1 sub-actions" to "scaffolded policy-selection surface exists; training and server evidence deferred."

## Linked artifacts

- `code/dream3r/memory_action.py`
- `code/dream3r/tests/test_memory_action_policy.py`
- `planning/TTT_PLAN.md`
- Local test pass rerun in CYCLE-20260523-002: 195 passed
- Server test pass recorded by handoff: 194 passed
- A8-specific tests: 14 unit tests in `test_memory_action_policy.py`
