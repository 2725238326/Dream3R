# STORY-20260505-004 Composer routes each scene to the right model

## Identity

storyboard_id: STORY-20260505-004

linked_spec: `specs/SPEC-20260504-001-3r-composer.md`

linked_finalist: 3R Composer

date: 2026-05-05

status: draft

cycle_of_origin: cycle 012 (`cycles/CYCLE-20260505-003.md`)

approval_decision_id: (absent — DEC-20260505-002 explicitly does NOT grant `approved-for-showing`)

## Title And Takeaway

title:

```text
Composer routes each scene to the right model — and pays for cost.
```

one_line_teacher_takeaway:

```text
A 3R system can pick the right model for each scene type, and when two
models are equally good, it picks the cheaper one. The decisions are
visible, not hidden.
```

## Audience Assumption

teacher_audience_profile_pointer: `paradigm/TEACHER_AUDIENCE_PROFILE.md`

assumed_prior_knowledge:

- 3R / DUSt3R-family familiarity: **partial** (cold start)
- specific comparator awareness: **none assumed**. Composer is harder than the other 3 storyboards on this axis because routing is comparator-vocabulary-dependent. Storyboard mitigates by showing the routing decision through a simple regime label, not by naming individual models.
- system-2 / test-time-compute familiarity: **partial**. Composer framing leans on "right tool for the job" intuition + "all else equal pick the cheaper one" intuition — universal.

## Panels (Visual Layout)

| Panel | What is shown | Source artifact | Functional vs placeholder |
|---|---|---|---|
| Panel A | Three input scenes side-by-side: a static pair, a dynamic 48-frame, a streaming sequence. Each labeled with regime type. | `cases/CASE-20260505-COMPOSER-04.md` Evidence Signals (4 KYKT jobs by regime); cycle-009 COMPOSER-01..03 paper-derived regime predictions | **placeholder**: paper-derived schematic; KYKT-metadata-anchored on regime labels |
| Panel B | Capability_card scoreboard for each regime: green/yellow/red per (model, regime) pair. Each scene routes to the green model. | COMPOSER-04 capability_card_per_model table (KYKT-metadata-derived numerics) | **placeholder**: paper-derived + KYKT-metadata-anchored |
| Panel C | A near-tie example (streaming regime, two models within tau_spread = 0.05). CR-4 cost-adjusted arrow points to the cheaper model. route_regret = near 0 under v2 cost-typed framing. | COMPOSER-04 P5 route_regret (cost-adjusted); cycle-009 COMPOSER-03 v2 row promoted canonical | **placeholder**: paper-derived prediction; tau_spread = 0.05 still inferred per G2 |

functional_vs_placeholder_boundary:

```text
ALL three panels are placeholder / paper-derived + KYKT-metadata-
anchored. No live inference. No measured route_regret (G2 still
inferred-with-real-inventory-anchor; closure gated). Per Discipline
rule 5 (Honesty Override).
```

## Narrative Beats

ordered_steps:

```text
1. start state: 3 input scenes arrive with 3 different regime types
   (static / dynamic / streaming).
2. trigger: a single-model system would run one model on all three
   scenes. Some scenes fit; some do not.
3. action: Composer reads each scene's regime and consults the
   capability_card scoreboard.
4. visible result: each scene routes to the model that is green on
   that regime; route_regret is near 0 across all three.
5. action: on a near-tie (two models both green on the same regime
   within tau_spread = 0.05), CR-4 picks the cheaper one.
6. visible result: same reconstruction quality, lower cost.
7. takeaway: visible routing decisions + cost-adjusted ties = a
   model ecology that does not silently waste compute.
```

surprise_hook:

```text
"Same reconstruction, less compute — when two models tie, pick the
cheaper one."
```

Locked. Retired alternatives:

- "MoE for 3R" — presupposes MoE vocabulary; cold-start audience does not have it.
- "Routing scoreboard" — too internal-mechanism.
- "Beats every single-model baseline" — overclaims; Composer ties single-model on its specialty regime, wins on cross-regime portfolios. The locked hook centers on the cost-adjusted tie which is Composer's most honest visible win.

## What Could Go Wrong On The Day

failure_modes_during_demo:

- routing decisions look invisible: Panel B's scoreboard makes them visible; pre-vet that the chosen 3 scenes have non-trivial routing variance.
- cost_normalized values look made up: opening slide states "cost values are inferred from public model size; not measured runtime"; this matches the COMPOSER-04 evidence label.
- audience asks "how do you know it's the right model?": redirect to the regime label coming from KYKT runner classification, anchored in COMPOSER-04. Do NOT improvise capability claims on the spot.
- audience asks "is tau_spread = 0.05 the right number?": acknowledge G2 (inferred-with-real-inventory-anchor; not measured). Honesty Override.
- comparator scene routing looks identical: pre-pick the near-tie example to make CR-4 cost arbitration visible.

## Fail-Safe Alternative

if_primary_demo_fails_in_30_seconds:

```text
Fall back to displaying CASE-20260505-COMPOSER-04.md directly:
read capability_card_per_model table + CR-4 cost-adjusted streaming
example. Story survives.
```

## Acceptance Criteria For Showing

**All items unchecked.** Cycle 012 produces draft only.

- [ ] linked_spec acceptance threshold met (COMPOSER-01..04 cover; mix of paper-derived and KYKT-metadata-derived)
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

linked_research_units: per COMPOSER-04 + cycle-009 COMPOSER cards

linked_sources: MASt3R, MonST3R, Fast3R, Spann3R (4 KYKT-confirmed regimes per COMPOSER-04)

linked_failure_modes: F6 Fragmented Model Ecology (Composer primary)

linked_actions: A5 routing facet

linked_proxy_metrics: P5 route_regret (cost-adjusted under v2), capability_match

linked_case_cards:

- `cases/CASE-20260505-COMPOSER-01.md` (CR-1 closure paired with CRITIC-02; paper-derived)
- `cases/CASE-20260505-COMPOSER-02.md` (regime-typed route_regret central thesis card; paper-derived)
- `cases/CASE-20260505-COMPOSER-03.md` (Fast3R vs MASt3R-SfM; v2 canonical row)
- `cases/CASE-20260505-COMPOSER-04.md` (**KYKT-metadata-derived; primary card for this storyboard's Panel B + C**)
- `cases/CASE-20260504-CRITIC-02.md` (CR-1 cross-spec dependency; Critic side of the agreement loop)

linked_cycle: `cycles/CYCLE-20260505-003.md`

linked_audience_profile: `paradigm/TEACHER_AUDIENCE_PROFILE.md`

## Next Step

planned_only: yes

next_action: refine_storyboard | request_user_approval_to_show | needs_user_decision

linked_next_artifact: future demo show authorization DEC if user picks Composer as a parallel-or-alternative demo target
