# DEC-20260505-001 Cycle 011 launch + D3 first teacher demo target = Critic + v2.1 forward-reference null protocol

decision_id: DEC-20260505-001

date: 2026-05-05

scope: cycle 011 launch authorization + D3 first teacher demo target pick + cycle-011 v2 -> v2.1 contract revision (low-stakes, forward-reference null protocol formalization)

decision: Launch cycle 011 with three locked outcomes:

1. **D3 first teacher demo target = Geometry Critic / System-2 3R** (`specs/SPEC-20260503-001-geometry-critic.md`). Storyboard drafting authorized; demo showing remains a separate gate (no `approval-for-showing` granted by this DEC).
2. **Cycle 011 scope = G4 + G5 closure (primary) + Critic demo storyboard draft (secondary)**. G6 + G2 + KYKT-derived Composer capability card + L3 prototype + paper writing all deferred.
3. **v2 -> v2.1 contract revision** for the forward-reference null protocol formalization only. The other two v3 candidates (8x8 grid partition; identity_consistency threshold pinning) are deferred and not promoted.

status: accepted

requires_user_approval: yes (this DEC IS the user approval gate; user message 2026-05-05: "你给我决定吧，（1）（2）（3）" delegated the three cycle-011 launch decisions to the agent)

## Context

Cycle 010 closed 2026-05-04 with full 4-finalist L2 case-card coverage (12 cards: 6 from cycle 009 + 6 from cycle 010). The cycle 010 S8 user-facing report surfaced four cycle-011 launch decisions:

```text
(1) D3 first teacher demo target (now eligible after both deferral
    conditions met: audience profile populated + all 4 finalists have
    L2 case-card coverage)
(2) cycle 011 scope: close G4/G5/G6 (a) | KYKT-derived Composer
    capability card (b) | L3 prototype (c, gated) | paper writing
    (d, gated)
(3) v2 -> v3 candidates: 8x8 grid partition | forward-reference null
    protocol | identity_consistency threshold
(4) blocked items unchanged
```

User reply 2026-05-05: "你给我决定吧，（1）（2）（3）" — explicit delegation of (1)(2)(3) to the agent. (4) is not a decision, just an awareness.

This DEC consumes that delegation and locks the three decisions below.

## Evidence

- User verbatim: "你给我决定吧，（1）（2）（3）" (2026-05-05)
- DEC-005 line 103 reservation: "the user can record the override in `decisions/DEC-20260504-006-d3-demo-target-pick.md` (id reserved here) at any time" — that reserved id was for a same-day override; today is 2026-05-05, so this DEC carries the new date prefix `20260505-001` per ID convention. The reservation is consumed (cross-referenced) but not occupied; if a future override is needed, the reserved `DEC-20260504-006` slot remains available.
- DEC-20260504-002 deferral conditions: both met as of cycle 010 closeout (audience profile populated + all 4 finalists L2-covered).
- Cycle 010 closeout: `cycles/CYCLE-20260504-002.md` "Closeout (S7)" + S8 user-facing report.
- Audience profile: `paradigm/TEACHER_AUDIENCE_PROFILE.md` (cold start, first impression, no specific 3R praise/criticism, taste = 科研的训练 / 写作技巧 / 创新范式 / 讲好故事).

## (1) D3 first teacher demo target = Critic

**Pick**: Geometry Critic / System-2 3R (`specs/SPEC-20260503-001-geometry-critic.md`).

Five-axis comparison across the four finalists, scored on the audience profile (cold-start, first-impression, taste-aligned to 创新范式 + 讲好故事):

| Axis | Critic | Memory | Permanence | Composer |
|---|---|---|---|---|
| Surprise hook strength | **strong**: catches a near-failure that comparators silently accept | medium: anchor retention is a slow, plot-heavy story | medium: dynamic-static separation is visual but needs labeled object identity | weak for cold-start: routing logic is invisible without comparator output side-by-side |
| Mechanism legibility for cold-start audience | **clean**: "verify before commit" maps to general system-2 intuition | hard: requires explaining anchor / state / governance tower | medium: requires explaining 4D scene, dynamic objects, identity | hard: requires explaining capability cards + cost-adjusted ties + alpha |
| Connection to Dream3R thesis (system-2 + governance + composition) | **direct**: Critic is the system-2 anchor of the thesis | direct on governance | direct on 4D / dynamics | direct on composition; weakest of the four for system-2 framing |
| L2 portfolio depth | **3 cards** with CR-1 reroute_model + CR-3 forward-reference null protocol exercised | 3 cards with CR-2 consumer + CR-3 producer; primary card is on KYKT job 222928 | 3 cards: KYKT primary + MASt3R control + synthetic identity-validation; static-control closes a fail_fast condition | 3 cards including v1 -> v2 cost-typed canonical promotion |
| Demo failure-mode robustness | **high**: case-card markdown is a clean fall-back; comparator output IS the surprise | medium: long-context drift takes minutes to render visibly | medium: dynamic clip needs careful sample selection | low: route_regret is a number, not a visual difference |
| Risk of "looks like an existing paper" | **low**: Test3R / TTT3R lineage is exactly what Critic builds on; the visible behavior is repair-not-just-flag | medium: Spann3R has internal memory; cold-start audience may conflate | medium: MonST3R does dynamic-static; cold-start audience may conflate | high: MoE / model selection looks like a router |

Decisive reasons:

- **Single most legible surprise hook for a cold-start audience**: "Catch a near-failure that other 3R systems silently accept, and repair it on the spot." This is a one-sentence first-impression story that does not require the audience to already know what 3R is failing on.
- **Audience taste alignment**: 创新范式 + 讲好故事 reward a single-mechanism story over a multi-mechanism portfolio; Critic is the cleanest single mechanism among the four. Memory + Permanence both require a tower of supporting concepts; Composer requires a comparator vocabulary the audience does not have.
- **Robust fall-back**: if the live demo fails in 30 seconds, the case-card markdown is itself the artifact (CRITIC-01..03 are paper-derived and reproducible offline). The other three finalists also have markdown fall-backs but the Critic story survives the fall-back better — "here is the catch the comparator missed" reads the same on screen and on paper.
- **Lowest "this is just paper X" collapse risk**: Test3R / TTT3R lineage is the *acknowledged* prior; the demo's repair behavior (A4 + A5 repair facet) is what Dream adds, and that addition is visible.

This pick does NOT collapse the project onto Critic. Per `decisions/DEC-20260504-002-no-all-in-on-single-finalist.md` (still in force), no non-finalist track is retired and the other three finalists keep their L2 portfolios. D3 is "first demo target", not "selected thesis".

storyboard_id reserved: STORY-20260505-001 (filed under `templates/demo_storyboard.md` in cycle 011 S2).

## (2) Cycle 011 scope

**In scope (primary)**:

- **G4 closure**: CR-2 partial on the synthetic identity-validation clip (`cases/CASE-20260504-PERMANENCE-03.md`) — close the consumer side. Mechanism: Memory consumer-side card or in-place edit of MEMORY-03 documenting the synthetic-clip consumer behavior. To be decided in cycle-011 S3 once the actual gap shape is re-read; either form is anti-F-001-budget-friendly.
- **G5 closure**: forward-reference null protocol formalization. Folded into v2.1 contract revision (see decision (3) below). One Edit on `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` adding a "Forward-reference null protocol" subsection under Versioning + a v2.1 entry to "v2 Change Log".

**In scope (secondary)**:

- **Critic demo storyboard draft** (`STORY-20260505-001-critic.md` under `templates/demo_storyboard.md`). Markdown only. Functional vs placeholder boundary explicit. Acceptance criteria for showing **left unchecked**; this DEC does NOT authorize showing.

**Deferred (explicitly out of cycle 011 scope)**:

- **G6** (Memory governance externalization on Spann3R-internal-memory-equipped models) — needs L3 prototype evidence; gated per `AGENT_MASTER_PROMPT.md` section 6 ("training or fine-tuning" + "running reproduction or smoke tests").
- **G2** (tau_spread = 0.05 in CR-1 closure remains inferred) — upgrading to demo-observed requires KYKT-job-derived measured `route_regret` OR L3 prototype work; both gated.
- **KYKT-derived Composer capability card** — defer to cycle 012 or beyond; not gated, just out-of-scope this cycle to keep cycle 011 budget tight.
- **L3 prototype** — gated; user has not authorized.
- **Paper writing / related-work expansion** — Phase 2 work; premature at L2-portfolio-just-completed stage.

**Discipline note on the secondary scope**: drafting a storyboard is a markdown-only L1.5-grade artifact under `templates/demo_storyboard.md`; the template explicitly states "Filling this template does not authorize showing the demo." This DEC reaffirms that boundary. A separate DEC (id reserved: `DEC-YYYYMMDD-NNN-critic-demo-show-authorization.md`) will be required before the Critic storyboard moves from `draft` to `approved-for-showing`.

## (3) v2 -> v2.1 contract revision: forward-reference null protocol formalization

**Promote**: forward-reference null protocol from informal pattern (used in cycle-009 CRITIC-03 + cycle-010 G5 carry-forward) to explicit contract clause. v2.1 only — does NOT touch alpha, signal owner table, CR-1..CR-6 substantive rules, or evidence-label propagation.

**Why v2.1 and not v3**: the change is documentation-grade. It formalizes a pattern that already worked in practice across two cycles. v3 is reserved for substantive signal additions / removals / repurposings; this is none of those.

**What v2.1 adds**:

- a "Forward-reference null protocol" subsection under Versioning, defining: (a) when a CR-X read is allowed to return null, (b) what the reading card MUST document (fallback path, expected close-out cycle, producer card id), (c) what the cycle closeout audit MUST verify (forward-reference null closed against producer card's actual published value, OR retired with stated reason).
- a v2.1 entry to "v2 Change Log".
- preservation of the v2 prose verbatim under "Superseded Versions" is NOT required (v2.1 is additive, not modificatory).

**Defer**:

- **8x8 grid partition for Permanence regions**: keep per-card. Reason: this is a Permanence implementation detail; formalizing it in the contract conflates contract-level (cross-spec channels) with implementation-level (single-spec parameters). If a different finalist later needs grid partitions, the right home is a per-spec parameter table, not the cross-spec contract.
- **identity_consistency threshold pinning at ~0.7**: defer. Reason: current value is `inferred` (per `cases/CASE-20260504-PERMANENCE-03.md`); promoting to v3 before measured data exists would violate Discipline rule 5 (Honesty Override). Re-surface when L3 prototype evidence or a labeled benchmark provides a measured anchor.

## What Cycle 011 Will Produce

new artifacts (3):

```text
decisions/DEC-20260505-001-cycle-011-launch-and-d3-demo-target.md  (this file)
cycles/CYCLE-20260505-002.md                                        cycle 011 cycle log
storyboards/STORY-20260505-001-critic.md                            Critic demo storyboard (draft)
```

contract revision (1):

```text
paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md  v2 -> v2.1 (additive; forward-reference null protocol formalization)
```

case-card edits (≤1):

```text
cases/CASE-20260504-PERMANENCE-03.md  potential CR-2 consumer-side documentation (G4 closure path; final form decided in cycle-011 S3 after re-read)
```

cycle 011 explicitly does NOT produce:

- any L3 prototype code or reproduction (gated)
- any KYKT-job-derived capability / route_regret measurement (out of scope this cycle)
- any teacher-demo `approved-for-showing` status (separate DEC required)
- any retroactive change to cycle 009 / cycle 010 case cards beyond the documented G4 path
- any retiring of any non-finalist track

## Discipline Compliance

- Discipline rule 1 (Falsifiability): cycle 011 fail-fast condition recorded in `cycles/CYCLE-20260505-002.md` Discipline-Required Header.
- Discipline rule 2 (Minimum Viable Mechanism): no new finalists, no new specs, no new proxy metrics. Storyboard is a markdown form of an existing finalist; v2.1 is documentation-grade.
- Discipline rule 3 (Surgical Edits): every edit in cycle 011 must trace to (a) G4/G5 closure, (b) Critic storyboard draft per `templates/demo_storyboard.md`, (c) v2.1 contract revision, or (d) Sync Rule chain. Anything outside those lanes is out-of-scope and must wait.
- Discipline rule 4 (Falsifiable Research Goals): cycle 011 primary failure modes carry forward F1/F2/F3/F6 from cycle 010 closeout; no new failure modes added.
- Discipline rule 5 (Honesty Override): D3 demo target is "agent-decided per user delegation", not "user-picked"; storyboard remains `draft` (not `approved-for-showing`); v3 candidates that need measured data are deferred, not silently smuggled in.
- F-001 working rules: cycle 011 sub-passes follow snapshot-first sync; each sub-pass = one anti-F-001 unit; no full-file Read of any in-context guidance file.

## Companion Files

- `decisions/DEC-20260504-002-no-all-in-on-single-finalist.md` (still in force; D3 = "first demo target", not retiring of other finalists)
- `decisions/DEC-20260504-005-cycle-010-launch.md` (cycle 010 launch + D3 deferral with override path; this DEC consumes that override path)
- `decisions/DEC-20260504-004-cross-spec-contract-v2.md` (v2 base; v2.1 in this cycle is additive)
- `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` (revision target this cycle)
- `paradigm/TEACHER_AUDIENCE_PROFILE.md` (audience profile consumed by D3 pick rationale)
- `specs/SPEC-20260503-001-geometry-critic.md` (D3 demo target spec)
- `cases/CASE-20260504-CRITIC-01..03.md` (L2 evidence consumed by Critic storyboard)
- `templates/demo_storyboard.md` (storyboard form)
- `cycles/CYCLE-20260505-002.md` (cycle 011 cycle log; carries S1..S7 board)
- `cycles/CYCLE-20260504-002.md` "Closeout (S7)" (cycle 010 closeout this DEC reads from)
