# DEC-20260508-004: Cycle 028 - Memory v0.3 ablation addendum

decision_id:    DEC-20260508-004
date:           2026-05-08
cycle:          028
status:         accepted
authorized_by:  user 2026-05-08: "arrange the plan and keep advancing"
decision_type:  markdown-only ablation planning
parent_spec:    SPEC-20260508-001
parent_plan:    planning/MEMORY_V03_P0_PROTOTYPE_PLAN.md

---

## Context

Cycle 026 established C2 Memory v0.3 as the current Memory-core design:

```text
state-token recurrence + explicit spatial key/value bank
+ geometry-aware bus-gated writes
```

Cycle 027 then wrote a P0 static tensor prototype plan comparing:

```text
V0 vector AnchorBank baseline
V1 Spann3R-style spatial key/value bank
V2 CUT3R-style state-token recurrence
V3 hybrid state tokens + spatial bank + bus-gated writes
```

The next useful non-execution step is to convert those variants, metrics,
and kill conditions into a memory-specific ablation addendum.

## Decision

Cycle 028 will create:

```text
specs/SPEC-20260508-002-dream3r-memory-v03-ablation-addendum.md
```

The addendum must:

- map P0 variants V0-V3 to `ABL-memory-*` tests
- connect each test to C2 v0.3 claims and kill conditions
- separate tensor-only P0 tests from future module, integration, and model-quality tests
- define acceptance criteria and evidence labels
- keep execution gated behind a separate DEC

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

This cycle produces `engineering plan` evidence only.

The new addendum may say what would falsify C2 Memory v0.3, but it cannot
claim that any variant works until a later authorized implementation runs.

## Version history

```text
v1  2026-05-08  cycle 028 launch decision. Markdown-only Memory v0.3
                ablation addendum authorized; execution remains gated.
```
