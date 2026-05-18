# DEC-20260508-002: Cycle 026 - C2 Memory v0.3 addendum and guidance correction

decision_id:    DEC-20260508-002
date:           2026-05-08
cycle:          026
status:         accepted
authorized_by:  user 2026-05-08: read TASK_SNAPSHOT, fully advance, check prior Dream progress, correct omissions and unreasonable content, and think through next directions for research validity
decision_type:  markdown-only architecture correction and guidance sync
parent_decision: DEC-20260506-001 (architecture-first mainline)
parent_artifact: planning/MEMORY_V03_DESIGN_STUDY.md (cycle 025)

---

## Context

Cycle 025 corrected Dream's direction after cycle 024 had drifted toward framework and scaffold execution. The cycle 025 code-reading study compared:

- CUT3R learned state-token recurrence and LocalMemory
- Spann3R explicit SpatialMemory key/value bank
- current Dream3R C2 code centered on GRU state, vector AnchorBank, and NSAThreeBranch

The study concluded that Dream3R C2 v0.3 should stop treating "GRU + vector cache + NSA label" as the memory mechanism. It should specify:

```text
state-token recurrence + explicit spatial key/value memory + geometry-aware bus-gated writes
```

This cycle turns that study into a formal architecture addendum and fixes stale guidance pointers that still referenced cycle 015 / cycle 022 next actions.

## Decision

Cycle 026 is launched as a markdown-only correction and specification pass.

Accepted deliverables:

1. Write `specs/SPEC-20260508-001-dream3r-c2-memory-v03-addendum.md`.
2. Explicitly supersede `SPEC-20260506-004` Delta 3's bounded vector AnchorBank + NSA-style retrieval as the conceptual C2 center.
3. Preserve v0.2 scaffold artifacts as implementation baseline / engineering smoke, not as research validation.
4. Repair guidance files so the default next direction is C2 Memory v0.3 specification and evidence design, not stale cycle 015 G_clone or cycle 022 Path C follow-up.
5. Add a small correction to `literature/PAPER_DRAFT_V1.md` so cycle 024 measured/demo evidence is bounded to component latency and plumbing demonstration, not C2 memory efficacy.

## Scope

Allowed:

- Local markdown edits under `Dream/`.
- New DEC, SPEC, and cycle log files.
- Guidance sync across `TASK_SNAPSHOT.md`, `WORKFLOW_STATUS.md`, `RESEARCH_STATE.md`, `INDEX.md`, `README.md`, `AGENT_MASTER_PROMPT.md`, and `registry/decision_registry.md`.
- Paper draft evidence-boundary correction.

Not allowed and not done:

- No server code edit.
- No model run.
- No training.
- No checkpoint download.
- No KYKT frontend or navigation change.
- No claim that C2 v0.3 is empirically validated.
- No final thesis selection.

## Supersession rule

This decision does not delete or rewrite prior artifacts. It adds a supersession layer:

```text
SPEC-20260506-004 Delta 3:
  v0.2 implementation scaffold and historical baseline.

SPEC-20260508-001:
  v0.3 architectural direction for C2 Memory.
  Supersedes Delta 3 as the current research design.
```

Cycle 024 server scaffold remains useful for:

- codebase shape
- smoke-test harnesses
- latency measurement hooks
- adapter interface evidence

Cycle 024 does not validate:

- state-token recurrence
- explicit spatial key/value memory
- geometry-aware write policy
- long-context memory quality
- reconstruction quality
- routing quality

Those require future v0.3 prototype and ablation work.

## Research-validity guardrails

1. Treat CUT3R and Spann3R mechanisms as `code-observed`, not as proof that the Dream3R hybrid will work.
2. Treat the C2 v0.3 hybrid as `speculative` until implemented and measured.
3. Treat cycle 024 C2 evidence as `engineering-demonstrated` for vector AnchorBank/NSA plumbing only.
4. Do not use cycle 024 synthetic dry-run or untrained DTU demo as evidence for memory quality.
5. Future implementation must start with a small v0.3 memory-state prototype and a reviewer checklist before touching the server model path.

## Version history

```text
v1  2026-05-08  cycle 026 launch decision. C2 Memory v0.3 addendum
                authorized as markdown-only; stale guidance pointers
                and paper evidence boundaries to be corrected.
```
