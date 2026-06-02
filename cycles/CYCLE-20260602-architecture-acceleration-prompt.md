# CYCLE-20260602: architecture acceleration prompt

Date: 2026-06-02
Status: closed
Decision: `decisions/DEC-20260602-023-architecture-acceleration-prompt.md`

## Trigger

The user asked for a prompt that can make the project advance architecture
quickly and effectively instead of continuing small incremental tweaks, and
asked that the surrounding documents be updated.

## Work completed

- Added `planning/DREAM3R_ARCHITECTURE_ACCELERATION_PLAN_20260602.md`.
- Added `handoff/ARCHITECTURE_V10_ACCELERATED_CONVERGENCE_AGENT_PROMPT.md`.
- Added this cycle log and the corresponding DEC.
- Synced the prompt into the project entry documents.

## Architectural posture

Current best verified baseline:

```text
proposal teachers + Dream state
-> frozen trained StatePrior
-> bounded convex fusion
-> disagreement-bounded residual refinement
```

Next target:

```text
native student decoder/distillation candidate over the existing proposal caches
```

Fallback next target:

```text
VGGT-Omega one-window teacher admission, only if it changes proposal bounds
```

## Explicit non-goals

- no new model run;
- no server mutation;
- no checkpoint download;
- no frozen-core edit;
- no broad route search;
- no residual-head micro-sweep.

## Verification

Documentation-only cycle. Verified by file creation and guidance sync.

