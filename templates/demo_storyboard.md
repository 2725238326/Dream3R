# Demo Storyboard Template

Status: branch-neutral storyboard skeleton. One storyboard per finalist demo.

Use after the corresponding finalist SPEC has L2 case-card data, and only after the user has approved a teacher demo target.

Filling this template does **not** authorize showing the demo. Demo authorization is a separate decision per `AGENT_MASTER_PROMPT.md` section 6 ("declaring teacher-demo readiness").

## Identity

storyboard_id: STORY-YYYYMMDD-NNN

linked_spec: `specs/SPEC-...`

linked_finalist: Critic | Memory | Permanence | Composer | Cross_Modal | Active_Perception

date:

status: draft | reviewed | approved-for-showing | retired

cycle_of_origin:

approval_decision_id: (the decision memo that authorized this demo to be shown; absent until granted)

## Title And Takeaway

title: short, plain, descriptive. No marketing tone.

```text
example: "Critic catches near-failure on a hard MASt3R pair and reroutes."
```

one_line_teacher_takeaway:

```text
What the teacher should remember after the demo, in one sentence. Not the
mechanism; the visible behavior. If the takeaway can be read as praise of
a specific paper rather than the Dream contribution, rewrite.
```

## Audience Assumption

teacher_audience_profile_pointer: `paradigm/TEACHER_AUDIENCE_PROFILE.md` (must be populated; see Boundaries)

assumed_prior_knowledge:

- 3R / DUSt3R-family familiarity: yes | no | partial
- specific comparator awareness (Test3R / TTT3R / MonST3R / OVGGT / etc.): list
- system-2 / test-time-compute framing familiarity: yes | no | partial

If the profile file is empty, do NOT fill these fields by inference.

## Panels (Visual Layout)

Each panel = one rendering surface visible to the teacher. Keep ≤ 3 panels for clarity.

| Panel | What is shown | Source artifact | Functional vs placeholder |
|---|---|---|---|
| Panel A |  |  |  |
| Panel B |  |  |  |
| Panel C |  |  |  |

functional_vs_placeholder_boundary:

```text
Mark every visible element. If the demo includes an element that looks
functional but is precomputed / mocked, label it explicitly. Discipline
rule 5 (Honesty Override) governs.
```

## Narrative Beats

ordered_steps: numbered list, each step ≤ 1 sentence, total ≤ 7 steps

```text
1. start state: ...
2. trigger: ...
3. action: ...
4. visible result: ...
5. ...
```

surprise_hook:

```text
The single moment the teacher should feel "this is different from the
papers I have seen". One sentence. If the storyboard has multiple
candidate hooks, pick one and retire the rest; multi-hook demos blur.
```

## What Could Go Wrong On The Day

failure_modes_during_demo:

- comparator output looks identical to Dream output (no visible difference)
- chosen sample turns out to be too easy (no conflict / no dynamics / no regime distinction)
- annotation labels look subjective when shown
- offline post-processing is mistaken for live inference
- Q&A surfaces a comparator the spec did not address

per_failure mitigations:

```text
For each failure mode listed above, write one sentence on the response.
If a failure mode has no mitigation, retire the storyboard rather than
showing.
```

## Fail-Safe Alternative

if_primary_demo_fails_in_30_seconds:

```text
What is the visible artifact if the demo cannot run? Typical answer:
fall back to the case-card markdown report, which is always offline and
reproducible. Do NOT fall back to a different finalist's demo; that
breaks the storyboard's takeaway.
```

## Acceptance Criteria For Showing

Each item must be true before approval-for-showing status:

- [ ] linked_spec has at least one case card past acceptance threshold
- [ ] `paradigm/TEACHER_AUDIENCE_PROFILE.md` is populated by the user
- [ ] all panels label functional vs placeholder explicitly
- [ ] all narrative beats trace to a SPEC action or evidence signal (no invented behavior)
- [ ] surprise hook is named and singular
- [ ] failure modes during demo each have a written mitigation OR a fail-fast retirement reason
- [ ] DEC-... entry recorded in `registry/decision_registry.md` granting demo authorization

## Boundaries

no_kykt_navigation_change_required: yes

no_frontend_implementation_required_to_storyboard: yes

```text
Storyboard fills are markdown only. Frontend implementation of the demo
panels is a separate downstream task that goes through
handoff/FRONTEND_DESIGN_HANDOFF_PROMPT.md to Gemini CLI ONLY after demo
authorization.
```

approval_required_for_showing: yes

```text
Showing requires a decision memo with status accepted, linked here as
approval_decision_id. Without that memo, this storyboard is design
content only.
```

## Linked Artifacts

linked_research_units:

linked_sources:

linked_failure_modes:

linked_actions:

linked_proxy_metrics:

linked_case_cards:

linked_cycle:

linked_audience_profile: `paradigm/TEACHER_AUDIENCE_PROFILE.md`

## Next Step

planned_only: yes

next_action: refine_storyboard | fill_audience_profile_first | request_user_approval_to_show | retire | needs_user_decision

linked_next_artifact:
