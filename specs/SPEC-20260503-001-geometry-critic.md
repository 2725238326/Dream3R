# SPEC-20260503-001 Geometry Critic / System-2 3R

## Identity

spec_id: SPEC-20260503-001

branch_name:

```text
Geometry Critic / System-2 3R
```

date: 2026-05-03

status: draft (pending L2 case-card evidence in cycle 009)

cycle_of_origin: CYCLE-20260503-002

## Approval

user_approval_for_branch: yes

approval_decision_id: DEC-20260503-002

approval_note:

```text
User approved option B (Critic + Memory + Permanence finalists; Composer support).
This decision authorizes drafting this spec and filling its L2 proxy case cards.
It does NOT authorize reproduction, training, checkpoint download, KYKT navigation
change, frontend implementation, or final thesis selection.
```

## Failure Modes

primary_failure_mode: F3 Hard-Case Geometric Ambiguity

secondary_failure_modes:

- F6 Fragmented Model Ecology (when A5 reroutes to a different 3R model)
- F1 Long-Context Drift / Forgetting (when critic gates memory write or context retrieval)

failure_mode_evidence:

- `planning/RESEARCH_GRAPH_AND_PAPER_START.md` rows F3, F6, F1
- F3 Karpathy-style label: source mechanisms paper-proven in Test3R / TTT3R / CTRL; the *Dream-specific* critic action set is `inferred`, not paper-proven.

## Owned Actions

owned_actions:

- A4 Geometry Verification
- A5 Repair / Reroute Decision

support_actions:

- A3 Context / Anchor Budgeting (used when critic gates anchor protection in long sequences; owned by Executive Memory spec)
- A7 Prior / Modality Arbitration (used when critic detects prior/RGB mismatch; owned by future Cross-Modal spec)

action_ownership_justification:

```text
Discipline rule 2 caps owned actions at <=3. Critic must own A4 to be a verifier
and A5 to avoid being diagnostic-only (the explicit weakest-pressure point
flagged in BRANCH_SHORTLIST_DECISION_SURFACE.md). Supporting A3 and A7 are
explicitly NOT owned here so they remain free for the Memory and (future)
Cross-Modal specs.
```

## Comparator Set

comparator_anchors:

- Test3R (test-time geometric self-check)
- TTT3R (test-time training trigger)
- MASt3R-SfM (matching-based geometric verification baseline)
- SLAM3R (SLAM-style consistency loop)
- G-CUT3R (guided pointmap with prior conflict)
- CTRL-style critic-revision (general critic-revise pattern outside 3R)

closest_comparator: Test3R + TTT3R combined

weakest_comparator_pressure:

```text
If Dream Critic only emits a "conflict score" without attaching a concrete A5
action (rerun region / reroute model / open context budget / request prior),
the spec collapses into yet another consistency report. Test3R already covers
that.
```

novelty_gap_against_comparators:

- Test3R / TTT3R operate inside a single model family. Dream Critic is a *cross-model* verifier with explicit A5 reroute targets in the comparator pool (MASt3R, MonST3R, Spann3R, Fast3R).
- CTRL-style critic-revision is general-purpose. Dream Critic specializes A5 against the 3R action vocabulary (route to a 3R comparator, reissue with anchor budget, request prior) rather than free-text revision.
- MASt3R-SfM verifies via classical SfM pipeline. Dream Critic verifies on per-frame evidence signal vector before SfM-stage refinement, using existing KYKT job outputs.

## Core Claim

claim_paragraph:

```text
A 3R system should not return a single-pass pointmap as final answer when the
evidence signal vector indicates geometric ambiguity. It should run a verify
step, score conflict, and trigger one of a small set of repair-or-reroute
actions (rerun local region, reroute to a different 3R model, open anchor
budget, request prior) before committing the output. The Dream contribution
is the closed loop A4 -> A5, not the existence of a critic alone.
```

one_line_thesis:

```text
Hard 3R cases need a verify-then-act loop, not a verify-then-report loop.
```

## Mechanism Pseudocode

inputs:

- per-frame or per-pair 3R outputs from one or more comparator models (pointmap, confidence, pose, intrinsics if available)
- evidence signal vector `e` from `ACTION_TAXONOMY_AND_PROXY_METRICS.md` Evidence Signal Vector V1
- comparator capability cards (which model is plausible for which input regime)

state_variables:

- `conflict_score(t)`: scalar from A4 over signal subset {pose_novelty, view_overlap, reprojection_residual, pointmap_conflict, confidence_drop, prior_rgb_conflict}
- `route_history(t)`: which models / actions have already been tried for this input window
- `repair_budget(t)`: bounded integer (default 1 reroute + 1 local rerun per window) to prevent runaway loops

trigger_conditions:

- A4 triggers on every input window. It is cheap and runs over already-produced outputs; it does not require model invocation.
- A5 triggers when `conflict_score(t) > theta_conflict` AND `repair_budget(t) > 0` AND at least one alternative route in the comparator pool has positive `capability_match` for the regime.

action_logic:

```text
1. score = A4(e, current_output)
2. if score <= theta_conflict:
     accept current_output; emit "verified" label
3. else if repair_budget == 0:
     accept current_output; emit "conflict_unresolved" label; surface to Advisor
4. else:
     pick A5 sub-action with smallest expected route_regret:
       - rerun_local_region: same model, narrowed window
       - reroute_model:      next-best comparator by capability_match
       - open_anchor_budget: hand off to Memory (A3 support, NOT owned here)
       - request_prior:      hand off to Cross-Modal (A7 support, NOT owned here)
     decrement repair_budget; rerun pipeline; emit critic-revision report
```

output_artifacts:

- per-window critic report: `{conflict_score, conflict_type, recommended_action, route_regret_estimate}`
- per-job critic timeline: aggregate of per-window reports
- A5 action log: which actions fired, what changed, whether conflict cleared

## Evidence Signal Vector Used

active_signals:

- pose_novelty
- view_overlap
- reprojection_residual
- pointmap_conflict
- confidence_drop
- model_capability_match
- prior_rgb_conflict (read-only; A7 ownership lives in Cross-Modal spec)

inactive_signals:

- dynamic_ratio (handed to Permanence spec)
- optical_flow_conflict (handed to Permanence spec)
- object_track_stability (handed to Permanence spec)
- loop_candidate_score (handed to Memory spec)
- anchor_importance (handed to Memory spec)
- cache_pressure (handed to Memory spec)
- external_memory_overlap (handed to Memory spec)
- blur_or_low_light_score (handed to Cross-Modal spec)
- uncertainty_area (handed to Active Perception)
- latent_drift_proxy (handed to Memory spec)

derived_signals:

- conflict_score (weighted sum over active signals; weights `inferred`, not learned)
- route_regret_estimate (gap between chosen route capability_match and best-known route capability_match for this regime)

## Action Policy Definition

| Action | Trigger condition | Scope of effect | Failure-aware fallback |
|---|---|---|---|
| A4 verify | every input window | per-window report; no state change to upstream model | if A4 itself disagrees with all signals (signal contradiction), emit `critic_unstable` and skip A5 for this window |
| A5 rerun_local_region | A4 conflict_score over reprojection_residual or pointmap_conflict, repair_budget > 0 | rerun same model on narrowed window | if rerun keeps conflict, escalate to A5 reroute_model |
| A5 reroute_model | A4 conflict_score + at least one comparator with higher capability_match for this regime | switch model for this window only; not a global model change | if no comparator improves, emit `route_exhausted`, surface to Advisor, stop |
| A5 open_anchor_budget | A4 detects long-context drift signal (latent_drift_proxy via cross-spec read), repair_budget > 0 | hand-off to Memory spec; Critic does NOT own anchor protection | Memory spec returns a budget decision; Critic logs the hand-off in route_history |
| A5 request_prior | A4 detects prior_rgb_conflict signal | hand-off to (future) Cross-Modal spec | if Cross-Modal not active, emit `prior_unavailable`, surface to Advisor |

## Proxy Validation Plan

primary_proxy: P1 conflict detection

secondary_proxy: P5 route regret

case_cards_to_fill:

```text
CASE-20260504-CRITIC-01  on 20260420-222729 (MASt3R static pair, matches.png + ply)
CASE-20260504-CRITIC-02  on 20260425-113002 vs 20260425-113227 (Fast3R vs Spann3R, route comparison)
CASE-20260504-CRITIC-03  on 20260420-222928 sampled frames (MonST3R per-frame conflict labels)
```

These IDs are reserved here; cycle 009 fills them via `templates/proxy_case_card.md`.

acceptance_threshold:

```text
On the labeled L2 cases (~3 case cards, ~10-30 windows total):
  conflict_detection >= 0.6 over labeled conflict windows
  AND false_alarm_rate <= 0.5 over labeled non-conflict windows
  AND at least one A5 sub-action attaches a concrete recommendation per
      detected conflict (no orphan critic reports)
  AND route_regret on Fast3R vs Spann3R route choice has nonzero spread
      (i.e. critic distinguishes the two regimes at all)
```

fail_fast_threshold:

```text
If after the cycle 009 case cards:
  false_alarm_rate > 0.5 on labeled non-conflict cases
  OR no concrete A5 action attaches to A4 trigger in any case
  OR route_regret has zero spread across all three case cards
then retire Critic spec back to "close reserve" and re-allocate cycle 010
budget to the remaining two finalists. Do not redraft to keep alive.
```

writing_value_if_only_negative_result:

```text
A clean negative still has paper value: it shows that signal-vector-only
critics are insufficient for cross-model 3R routing, and motivates a learned
or capability-card-aware critic in future work. Negative result documented
with case cards is acceptable cycle 009 output.
```

## Teacher Demo Form

what_is_visible:

```text
A two-panel timeline over an existing KYKT job:
  Panel A: original 3R output (pointcloud / matches / per-frame pose).
  Panel B: critic overlay - red zones for detected conflicts, action label
           ("rerun region" / "reroute to MASt3R" / "open anchor budget")
           and a route-regret bar against the alternative comparator.
```

why_it_surprises_a_teacher:

```text
Most 3R demos show a successful reconstruction. This demo shows the model
catching its own near-failure and choosing a corrective action - i.e. a
System-2 step that current single-pass 3R does not have.
```

artifact_format:

- markdown report with embedded image references to existing KYKT job artifacts
- no live model inference required for the demo (everything is offline post-processing)

approval_required_for_demo: yes

```text
Approval is required before showing this demo to anyone outside the immediate
research loop. KYKT navigation change is separately approval-gated and is NOT
part of this spec.
```

## KYKT Integration Surface

surface_list:

- research_lane (Critic timeline as a research artifact)
- advisor_report (per-job critic report attaches to Advisor output)

NOT in scope this spec:

- runner (no runner change; Critic post-processes existing job outputs)
- sample_matrix (no scoring matrix change)
- system_readiness (no system change)
- management_area (no navigation change)

backend_contract_needed:

```text
Read-only access to existing job artifact paths under model_uploads/. No new
backend service. No schema migration. No new endpoint.
```

frontend_handoff_needed: no

frontend_handoff_brief_id: not_applicable_yet

```text
Frontend display of the critic timeline is a downstream decision. It would
go through handoff/FRONTEND_DESIGN_HANDOFF_PROMPT.md to Gemini CLI ONLY
after user approval of the demo and a KYKT navigation decision.
```

## Engineering Cost

L1_design_cost: low

```text
This spec file plus three case cards in cycle 009. ~4-6 hours of synthesis
work. Annotation budget per case card: 90-120 minutes per cycle 008 D4
(DEC-20260504-002 implies the same ceiling for parallel tracking). Critic
remains the cheapest of the four finalists; the 30-60 minute median is
still the expected actual labeling time, just with headroom inside the
shared 90-120 minute cap.
```

L2_proxy_cost: low

```text
Scripted reading of existing job outputs + manual conflict labels +
spreadsheet-style scoring. No model invocation. No checkpoint download.
```

L3_prototype_cost: blocked_until_approval

L4_model_change_cost: blocked_until_approval

## Risks

novelty_risk:

```text
Test3R / TTT3R already cover in-family critic. Dream's cross-model A5 reroute
is the differentiator and must be visible in every case card. If the case
cards reduce to "we re-derived Test3R", the novelty story collapses.
```

overlap_with_comparator:

```text
Heavy overlap with Test3R on A4 itself. Mitigated by owning A5 explicitly and
restricting A5 sub-actions to the cross-3R-model action set.
```

engineering_risk:

```text
Low. All inputs are already on disk. The risk is annotation quality, not code.
```

demo_risk:

```text
Demo could look unimpressive if the existing KYKT jobs do not contain a
clearly hard case. Mitigation: case card 03 uses MonST3R 48-frame job,
which has 96 dynamic masks and is the most likely to surface conflicts.
```

paper_writing_risk:

```text
"System-2 3R" is rhetorically attractive but already used by Test3R. The
paper claim must shift to "cross-model A5 action set" or risk being read as
relabeling.
```

## Evidence Labels

mechanism_status: inferred

```text
A4 (verification) is paper-proven in Test3R / TTT3R. The closed A4 -> A5
loop with the Dream-specific A5 sub-action set is inferred; not yet
demonstrated in any single source.
```

action_policy_status: inferred

```text
theta_conflict, repair_budget defaults, and the action priority order are
inferred from the comparator literature. No measurement yet.
```

performance_status: unknown

```text
No benchmark numbers. No claim of accuracy improvement over any comparator.
The cycle 009 case cards produce L2 proxy evidence only.
```

## Boundaries

no_reproduction_yet: yes

no_training_yet: yes

no_checkpoint_download_yet: yes

no_kykt_navigation_change: yes

no_frontend_implementation_yet: yes

approval_gates_required_to_advance:

- moving from L2 case-card evidence to L3 prototype runner: requires user approval
- adding a KYKT navigation surface for the critic: requires user approval
- declaring this spec the final Dream thesis: requires user approval
- training a learned critic: requires user approval

## Linked Artifacts

linked_research_units:

- RU-003 Test-Time Geometry Self-Check (primary)
- RU-011 Geometry Critic-Revision Loop (primary)
- RU-002 3R Composer Controller (support; A5 reroute leans on Composer capability cards)

linked_sources:

- Test3R, TTT3R, CTRL, MASt3R-SfM, SLAM3R, G-CUT3R (see `registry/source_registry.md` for IDs)

linked_failure_modes: F3 (primary), F6, F1

linked_actions: A4 (owned), A5 (owned), A3 (support), A7 (support)

linked_proxy_metrics: P1 (primary), P5 (secondary)

linked_cycle: CYCLE-20260503-002

linked_kykt_jobs:

- 20260420-222729 (MASt3R static pair)
- 20260420-222928 (MonST3R 48-frame)
- 20260425-113002 (Fast3R)
- 20260425-113227 (Spann3R)

## Next Step

planned_only: yes

next_action: fill_case_cards

linked_next_artifact:

- `templates/proxy_case_card.md` -> populated as CASE-20260504-CRITIC-01..03 in cycle 009

## Next Discussion Point For The User

```text
Critic is the cheapest finalist to falsify. Cycle 009 default plan is to fill
its three case cards first. Two open user decisions:

  1. Should Critic case cards run before, in parallel with, or after the
     Memory and Permanence case cards? Default: before (cheapest, fastest
     yes/no).
  2. If A5 reroute_model recommends switching to a comparator that requires
     a fresh KYKT job, do we authorize that job, or restrict A5 to the four
     existing job IDs only? Default: restrict to existing jobs in cycle 009;
     revisit after the case cards land.
```
