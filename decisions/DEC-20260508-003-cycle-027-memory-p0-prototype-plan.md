# DEC-20260508-003: Cycle 027 - C2 Memory P0 prototype plan

decision_id:    DEC-20260508-003
date:           2026-05-08
cycle:          027
status:         accepted
authorized_by:  user 2026-05-08: "continue and finish the task you described"
decision_type:  markdown-only prototype planning
parent_decision: DEC-20260508-002
parent_spec:    SPEC-20260508-001

---

## Context

Cycle 026 produced `SPEC-20260508-001-dream3r-c2-memory-v03-addendum.md`.
That addendum recommends the next step:

```text
Memory-state prototype plan, markdown only.
P0 static tensor prototype, server-side only if authorized.
```

The purpose of cycle 027 is to define the P0 prototype precisely enough that a later implementation agent can execute it without redesigning the research question.

## Decision

Cycle 027 will create:

```text
planning/MEMORY_V03_P0_PROTOTYPE_PLAN.md
```

The plan must compare four memory variants:

1. v0.2 vector AnchorBank baseline.
2. Spann3R-style spatial key/value read.
3. CUT3R-style state-token recurrence.
4. Hybrid with bus-gated write policy.

The plan must define:

- tensor fixtures
- deterministic synthetic regimes
- module inputs and outputs
- metric formulas
- kill conditions
- reviewer checklist
- future execution gate

## Scope

Allowed:

- Local markdown planning.
- Guidance-file sync.
- Cycle log update.

Not allowed and not done:

- No Python prototype.
- No server code edit.
- No model run.
- No checkpoint use or download.
- No training or fine-tuning.
- No paper claim promotion.
- No KYKT frontend or navigation change.

## Evidence boundary

This cycle produces an `engineering plan`, not `engineering-demonstrated` evidence.

No claim may be made that state-token recurrence, spatial bank retrieval, hybrid bus-gated writes, or C2 Memory v0.3 work until a later authorized prototype is implemented and measured.

## Version history

```text
v1  2026-05-08  cycle 027 launch decision. Markdown-only P0
                prototype plan authorized; execution remains gated.
```
