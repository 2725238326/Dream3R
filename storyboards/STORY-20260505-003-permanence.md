# STORY-20260505-003 Permanence keeps the dynamic objects out of the static map

## Identity

storyboard_id: STORY-20260505-003

linked_spec: `specs/SPEC-20260503-003-dynamic-object-permanence.md`

linked_finalist: Permanence

date: 2026-05-05

status: draft

cycle_of_origin: cycle 012 (`cycles/CYCLE-20260505-003.md`)

approval_decision_id: (absent — DEC-20260505-002 explicitly does NOT grant `approved-for-showing`)

## Title And Takeaway

title:

```text
Permanence keeps dynamic objects out of the static map.
```

one_line_teacher_takeaway:

```text
A 3R system can separate "the room" from "the things moving in the
room", so the persistent geometry stays clean even when the scene is
busy with motion.
```

## Audience Assumption

teacher_audience_profile_pointer: `paradigm/TEACHER_AUDIENCE_PROFILE.md`

assumed_prior_knowledge:

- 3R / DUSt3R-family familiarity: **partial** (cold start)
- specific comparator awareness: **none assumed**. Storyboard introduces "Model A (no dynamic-static separation)" vs "Dream Permanence" by visible behavior.
- system-2 / test-time-compute familiarity: **partial**. Permanence framing leans on "permanent vs transient" intuition — universal.

## Panels (Visual Layout)

| Panel | What is shown | Source artifact | Functional vs placeholder |
|---|---|---|---|
| Panel A | 48-frame dynamic scene: people / objects moving across a static room. Color-coded "dynamic region" union per frame (Permanence's suppress_static_write input) | `cases/CASE-20260504-PERMANENCE-01.md` Evidence Signals (MonST3R 48-frame; 8x8 grid x 48 = 3072 region-frames) | **placeholder**: paper-derived schematic |
| Panel B | Side-by-side static map: Model A's static map gets polluted with motion blur ghosts (~150/3072 dynamic_pollution); Dream's static map stays clean (~2400/3072 static_preservation) | PERMANENCE-01 Predicted Proxy Outcome | **placeholder**: paper-derived |
| Panel C | Object identity timeline: O1 / O2 / O3 tracks across 48 frames; mint_object_id rate = 0 on the static-control comparison (per PERMANENCE-02 MASt3R static-pair); identity_consistency ~0.7 inferred per PERMANENCE-03 synthetic clip | PERMANENCE-01 + PERMANENCE-02 + PERMANENCE-03 | **placeholder**: paper-derived |

functional_vs_placeholder_boundary:

```text
ALL three panels are placeholder / paper-derived. No live inference.
Per Discipline rule 5 (Honesty Override).
```

## Narrative Beats

ordered_steps:

```text
1. start state: a dynamic scene streams in. Some pixels belong to the
   room (static); some belong to moving objects (dynamic).
2. trigger: comparator runs without dynamic-static separation. Every
   pixel goes into the static map.
3. visible result (comparator): static map gets polluted with ghost
   trails where moving objects passed through.
4. action: Dream Permanence emits suppress_static_write on dynamic
   region union; Memory consumes the signal per CR-2.
5. action: Permanence assigns object identities to dynamic regions
   (O1 / O2 / O3); identity persists across frames.
6. visible result (Dream): static map is clean; dynamic objects have
   stable IDs across the sequence.
7. takeaway: separating dynamic from static is not optional for long
   sequences — it is what keeps the persistent map persistent.
```

surprise_hook:

```text
"Watch the static map stay clean while the scene moves."
```

Locked. Retired alternatives:

- "Object permanence in 3R" — too jargon-heavy for cold-start audience.
- "Identity tracks through occlusion" — too narrow; the bigger story is dynamic-static separation, identity persistence is downstream.
- "MonST3R does this already" — false framing; MonST3R produces dynamic masks, Dream Permanence acts on them via CR-2 binding.

## What Could Go Wrong On The Day

failure_modes_during_demo:

- comparator's pollution looks invisible at small render scale: zoom in on a specific region known from PERMANENCE-01 (8x8 grid; ~150 polluted region-frames are localized).
- chosen sample lacks enough motion: pre-vet via PERMANENCE-01's 48-frame MonST3R job 20260420-222928 anchor.
- identity labels look subjective: show only the binary "this region got an object id" indicator; quantitative threshold ~0.7 stays in markdown.
- offline mistaken for live: every panel labeled "schematic"; opening slide states no live inference.
- Q&A on whether MonST3R's own dynamic mask suffices: redirect to MEMORY-01 + PERMANENCE-01 cross-pair (CR-2 binding); the dynamic mask is an input, not the mechanism.

## Fail-Safe Alternative

if_primary_demo_fails_in_30_seconds:

```text
Fall back to displaying CASE-20260504-PERMANENCE-01.md directly:
read Evidence Signals + Predicted Proxy Outcome (P4 dynamic_pollution
prediction). Story survives.
```

## Acceptance Criteria For Showing

**All items unchecked.** Cycle 012 produces draft only.

- [ ] linked_spec acceptance threshold met (PERMANENCE-01..03 cover; paper-derived)
- [ ] audience profile populated (yes)
- [ ] panels labeled (yes)
- [ ] beats trace to SPEC actions (yes)
- [ ] hook named and singular (yes)
- [ ] mitigations written (yes)
- [ ] DEC granting demo authorization (NO; gated)

## Boundaries

no_kykt_navigation_change_required: yes

no_frontend_implementation_required_to_storyboard: yes

approval_required_for_showing: yes (separate DEC required)

## Linked Artifacts

linked_research_units: per PERMANENCE-01 line 23

linked_sources: MonST3R (KYKT-confirmed dynamic regime per COMPOSER-04); MASt3R (static control)

linked_failure_modes: F2 Dynamic-Static Entanglement (Permanence primary)

linked_actions: A6 Dynamic / Object State Separation

linked_proxy_metrics: P4 dynamic_pollution, identity_consistency

linked_case_cards:

- `cases/CASE-20260504-PERMANENCE-01.md` (primary; MonST3R 48-frame; CR-2 producer)
- `cases/CASE-20260504-PERMANENCE-02.md` (MASt3R static control; mint_object_id rate = 0)
- `cases/CASE-20260504-PERMANENCE-03.md` (synthetic dynamic identity-validation; G4 closure under v2.1)
- `cases/CASE-20260504-MEMORY-01.md` (cross-pair; Memory consumes suppress_static_write per CR-2)
- `cases/CASE-20260505-COMPOSER-04.md` (KYKT-metadata anchor for MonST3R dynamic regime classification)

linked_cycle: `cycles/CYCLE-20260505-003.md`

linked_audience_profile: `paradigm/TEACHER_AUDIENCE_PROFILE.md`

## Next Step

planned_only: yes

next_action: refine_storyboard | request_user_approval_to_show | needs_user_decision

linked_next_artifact: future demo show authorization DEC if user picks Permanence as a parallel-or-alternative demo target
