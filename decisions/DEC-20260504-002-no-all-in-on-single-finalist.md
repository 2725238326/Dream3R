# DEC-20260504-002 No All-In On Any Single Finalist

decision_id: DEC-20260504-002

date: 2026-05-04

scope: thesis selection posture

decision: No single finalist (Critic / Memory / Permanence / Composer) is treated as the thesis spine. Memory in particular is borrowable as one component of a larger story rather than the headline. Cycle 009 runs case cards for all four finalists on parallel tracks (with Critic first per DEC-20260504-001 lineage, see below). The first teacher demo target (cycle 008 D3) is deferred until cycle 009 case-card data exists; do not pick a demo target unilaterally.

status: accepted

requires_user_approval: yes (this DEC IS the user approval gate)

## Context

Cycle 008 closed with four explicit user discussion points:

```text
D1. Which spec gets the first L2 case-card pass in cycle 009? Default: Critic.
D2. Composer L1 vs L2 framing.
D3. First teacher-facing demo target.
D4. Annotation cost ceiling for cycle 009.
```

In the same session that produced `handoff/SESSION-HANDOFF-20260504-001-cycle-008-closeout-and-cycle-009-prep.md`, the user resolved:

- D1: Critic first (locked)
- D2: upgrade Composer to a fourth finalist spec, drafted now (locked; recorded in DEC-20260504-001)
- D4: 90 to 120 minutes per case card (locked)

For D3, the user explicitly declined to pick a demo target. The user's framing was that no single finalist deserves "all-in" status; memory is one borrowable component, not the spine. This DEC captures that framing as a directional decision in its own right rather than letting it silently propagate as agent inference.

The directional decision matters because:

- it constrains how the cycle log and `WORKFLOW_STATUS.md` describe the four finalists
- it forbids the agent from quietly upgrading any finalist to "preferred" status mid-cycle on the basis of cheaper case-card evidence
- it explicitly defers D3 rather than inviting the agent to pick on the user's behalf

## Evidence

- User verbatim: "我觉得记忆系统啥的只是我们借鉴优点的一个部分，我觉得不能all in"
- Translation context: "Memory systems and similar are just one component whose strengths we borrow; we cannot all-in on any of them."
- Coupling with D2 in the same turn ("决策2改成升格吧") shows the user explicitly chose to widen the finalist set rather than narrow it. The four-spec posture is therefore intentional, not a side effect of acceleration.
- `paradigm/RESEARCH_CODE_DISCIPLINE.md` rule 5 (Honesty Override) requires capturing this directional decision rather than letting it remain implicit. Without this DEC, future cycle logs could drift toward describing one finalist as the "leading" candidate, which contradicts the user's stated posture.

## Options

A. Treat one finalist as the working thesis spine and the others as supporting evidence. *(declined by user; user explicitly forbids "all-in")*

B. Treat all four finalists as parallel borrowable components; defer thesis selection until case-card data lands. *(approved by user)*

C. Pick a teacher demo target now to give cycle 009 a concrete artifact target. *(declined; D3 deferral was explicit)*

D. Drop one of the four finalists to reduce annotation budget pressure. *(declined; D2 widened the finalist set; this would contradict the same-turn decision)*

## Decision

1. The four finalists (Critic / Memory / Permanence / Composer) are treated as parallel candidates. None is the thesis spine. Their case-card outcomes in cycle 009 are evaluated on individual merits without preferential rescue.

2. D3 (first teacher demo target) is deferred until cycle 009 case-card data exists. The agent must not pick a demo target unilaterally. The deferral is surfaced in `WORKFLOW_STATUS.md` Recommended Next User Decision so the user can revisit it after seeing case-card evidence.

3. Memory in particular must not be described as the "leading" or "headline" candidate in any artifact created during this session. Existing `RESEARCH_STATE.md` "Current Strongest Candidate" framing of GEM-3R as a candidate (not final) is preserved per Discipline rule 3 (Surgical Edits); no retroactive rewrite. Future cycle logs adopt the no-all-in posture going forward.

4. Cycle 009 begins with Critic case cards (per the user's D1 lock from the same session). Once Critic case cards land, the agent does not auto-promote Critic to "leading" status; it surfaces results back to the user for the next decision turn.

5. The teacher audience profile required to inform D3 is recorded as a placeholder file `paradigm/TEACHER_AUDIENCE_PROFILE.md` for the user to fill. The agent must not invent its content. Until the placeholder is populated, D3 stays open.

6. This posture binds the new Composer finalist (DEC-20260504-001) symmetrically: Composer also is not the thesis spine.

## Risks

- **Four-way parallel evaluation may overrun annotation budget faster than three-way.** Mitigated by the per-card 90 to 120 minute cap (D4) and by the cross-SPEC risk register `planning/WORK_RISK_REGISTER.md` (drafted in this same session). If aggregate budget overruns, the user is notified before any rescue; no agent-side preference selection.
- **Demo target deferral may delay teacher-facing visibility.** Accepted by the user as the cost of avoiding premature commitment. The deferred D3 is surfaced as a still-open decision; it does not silently disappear.
- **"No all-in" posture may read as indecision in a paper narrative.** Mitigated by `literature/PAPER_RELATED_WORK_SKELETON.md` (drafted in this same session) framing the four finalists as orthogonal mechanisms over a shared failure-mode taxonomy. The paper claim becomes the integration story, not any single mechanism.
- **Risk of implicit drift toward one finalist via case-card prioritization order** (Critic first per D1). Mitigated by an explicit reminder in `cycles/CYCLE-20260504-001.md` and `WORKFLOW_STATUS.md` that D1 sets execution order, not preference order.

## User Approval Required

This DEC IS the user approval gate for the no-all-in posture and for deferring D3.

User approval IS still required for, and is NOT granted by this decision:

- final thesis selection (still gated)
- picking a teacher demo target (deferred per this DEC; not granted)
- any L3 / L4 actions on any finalist
- KYKT navigation change
- frontend implementation
- discarding any non-finalist track (Cross-Modal, Active Perception remain alive at lower priority)

## Next Action

1. Surface D3 (first teacher demo target) in `WORKFLOW_STATUS.md` Recommended Next User Decision as deferred-pending-case-card-data.
2. Create `paradigm/TEACHER_AUDIENCE_PROFILE.md` as a placeholder file the user populates; the agent does not invent its content.
3. In cycle 009, run case cards for all four finalists; do not promote any single result to "leading" status without a user decision turn.
4. Re-surface D3 to the user once cycle 009 case-card data exists and the teacher audience profile is populated.
