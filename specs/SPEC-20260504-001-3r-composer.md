# SPEC-20260504-001 3R Composer / Unified Model Ecology

## Identity

spec_id: SPEC-20260504-001

branch_name:

```text
3R Composer / Unified Model Ecology
```

date: 2026-05-04

status: draft (pending L2 case-card evidence in cycle 009)

cycle_of_origin: CYCLE-20260504-001 (cycle 008.5 closeout)

## Approval

user_approval_for_branch: yes

approval_decision_id: DEC-20260503-002 (original finalist authorization including Composer as supporting layer) + DEC-20260504-001 (composer upgrade timing)

approval_note:

```text
DEC-20260503-002 named Composer in the option-B finalist context as
supporting layer. DEC-20260504-001 promotes it to a fourth finalist
mechanism spec drafted now (cycle 008.5), per the user's "决策2改成升格吧"
direction. DEC-20260504-002 binds the no-all-in posture to Composer
symmetrically: this spec must not be treated as the thesis spine. It
does NOT authorize reproduction, training, checkpoint download, KYKT
navigation change, frontend implementation, or final thesis selection.
```

## Failure Modes

primary_failure_mode: F6 Fragmented Model Ecology

secondary_failure_modes:

- F3 Hard-Case Geometric Ambiguity (when Composer's `capability_match` informs Critic's A5 reroute_model)
- F1 Long-Context Drift / Forgetting (when Composer routes streaming inputs to memory-aware models)
- F2 Dynamic-Static Entanglement (when Composer routes dynamic inputs to dynamic-aware models)

failure_mode_evidence:

- `planning/RESEARCH_GRAPH_AND_PAPER_START.md` row F6 lists capability cards, unified pointmap / pose / confidence contracts, composer routing, benchmark matrix, and artifact evidence reports as the relevant mechanism nodes.
- F6 source mechanisms are paper-proven across DUSt3R / MASt3R / Fast3R / Spann3R / MonST3R / CUT3R / STream3R / SLAM3R / MV-DUSt3R+ / Splatt3R / InstantSplat / NoPoSplat. The Dream-specific *route_regret falsification axis* is `inferred`, not paper-proven.

## Owned Actions

owned_actions:

- A5 Repair / Reroute Decision (composer ownership; the routing aspect of A5)

support_actions:

- A3 Context / Anchor Budgeting (read-only; consumed when long-context routing requires Memory anchor data; owned by Memory spec)
- A4 Geometry Verification (read-only; Composer reads Critic's `conflict_score` to refine `route_recommendation`; owned by Critic spec)
- A7 Prior / Modality Arbitration (read-only; Composer routes prior-augmented samples differently; owned by future Cross-Modal spec)

action_ownership_justification:

```text
Discipline rule 2 (Minimum Viable Mechanism) caps owned actions at <=3 and
prefers the smallest set. Composer owns A5 only because Composer's
leverage is the capability-card matrix, not a wide action set. Owning
multiple actions would either fragment the route signal across specs or
duplicate the work Critic already does on A5's repair facet.

Importantly, A5 has two facets:
  - "repair / rerun_local_region" lives in Critic SPEC-20260503-001
  - "reroute_model" lives in Composer SPEC-20260504-001

Both specs own A5 along this functional split. Critic owns the per-window
repair facet because repair is verification-coupled. Composer owns the
across-model routing facet because routing is regime-coupled. The
cross-spec signal contract (`paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md`)
formalizes the handoff: when Critic decides reroute_model, it consumes
Composer's `route_recommendation` rather than inventing one.
```

## Comparator Set

comparator_anchors:

- DUSt3R (pose-free pointmap baseline)
- MASt3R (3D-grounded matching; sparse global alignment)
- MASt3R-SfM (matching + retrieval + global SfM)
- Fast3R (many-image one-shot pass)
- Spann3R (spatial memory for global pointmap)
- MonST3R (dynamic 4D pointmap)
- CUT3R (persistent state continuous 3D perception)
- STream3R (causal streaming geometry)
- SLAM3R (sliding-window SLAM)
- MV-DUSt3R+ (sparse-view multiview)
- Splatt3R (Gaussian asset path)
- InstantSplat (sparse-view Gaussian)
- NoPoSplat (sparse unposed Gaussian)

closest_comparator:

```text
There is no directly published "3R composer" comparator. The nearest
analogs are:
  - mixture-of-experts (MoE) routing in language and vision
  - SLAM front-end model selection
  - benchmark matrix style evaluation papers
None of these define a route_regret axis specific to 3R input regimes.
```

weakest_comparator_pressure:

```text
Pure model routing reads as system engineering rather than paper-grade
architecture. The risk is that L1 capability cards alone duplicate work
already done by individual model papers' "scope" sections. The novelty
must live in the route_regret falsification axis and the regime card
formalization, not in the routing itself.
```

novelty_gap_against_comparators:

- No single 3R paper publishes a regime-fit profile against the rest of the 3R model family. Each paper claims its own regime; cross-regime fit is left implicit.
- Mixture-of-experts routing in language is sample-conditioned but not regime-card-based. Composer's `sample_regime_card` is regime-typed (static_pair, many_view, dynamic_video, streaming, sparse_view, ...) rather than learned.
- Benchmark matrix papers report metrics but do not publish a `route_regret` falsification metric: a Composer that is no better than picking a single default model has zero route_regret spread.

## Core Claim

claim_paragraph:

```text
3R fragmentation is itself the research problem. A controller that maps
input regimes (static_pair, many_view, dynamic_video, streaming,
sparse_view, ...) to capability profiles produces a falsifiable
route_regret signal that downstream finalists (Critic A5) can read. The
Dream contribution is the regime-card + capability-card pair plus the
route_regret metric, not the act of routing itself.
```

one_line_thesis:

```text
3R needs a regime-typed route_regret axis, not a meta-model.
```

## Mechanism Pseudocode

inputs:

- a sample input (image pair, image set, video, streaming feed)
- the comparator set capability_card collection (one card per model_id)
- the sample's `sample_regime_card` (computed from input metadata)
- optional read-only Critic `route_history(t)` for windows already attempted
- evidence signal vector `e` from `ACTION_TAXONOMY_AND_PROXY_METRICS.md` (Composer reads model_capability_match, view_overlap, blur_or_low_light_score, dynamic_ratio)

state_variables:

- `capability_card(model_id)`: per-model capability profile across regimes; static for the cycle; structured as {regime_id -> {capability_score: float, evidence_label: paper-proven | code-observed | inferred | unknown, source_id: SRC-...}}
- `sample_regime_card(input)`: per-input regime classification; structured as {regime_id -> probability}
- `route_history`: read-only from Critic
- `route_log(input)`: append-only log of (model_id, capability_match, chosen) tuples per input

trigger_conditions:

- Composer runs once per input window. It is cheap; computation is a card join, not a model invocation.
- Composer does not trigger on internal model state. It triggers on input regime + (optional) Critic route_history.

action_logic:

```text
on each input window w:

  regime_card = compute_regime_card(w.metadata)
  # regime_card values are inferred from view_count, motion ratio,
  # streaming flag, presence of priors, etc.

  matches = []
  for model_id in comparator_set:
    cc = capability_card(model_id)
    cm = capability_match(cc, regime_card)
    matches.append((model_id, cm))

  # capability_match is a weighted dot product of regime probabilities
  # against per-regime capability scores; weights are inferred

  matches_sorted = sort_descending_by_score(matches)
  best = matches_sorted[0]
  best_score = best.cm
  spread = best_score - matches_sorted[-1].cm

  # if Critic already tried best, fall through to next
  if best.model_id in route_history(w):
    next_candidate = first model_id in matches_sorted not in route_history
    if next_candidate exists:
      route_recommendation = [next_candidate, best, ...]
    else:
      route_recommendation = matches_sorted

  else:
    # tie handling per CR-4 in CROSS_SPEC_SIGNAL_CONTRACT.md
    ties = [m for m in matches_sorted if best_score - m.cm < epsilon_tie]
    route_recommendation = ties + matches_sorted not in ties

  route_regret(chosen, w) = best_score - capability_match(chosen, regime_card)

  publish capability_match, route_recommendation, route_regret,
          regime_card, capability_card to consumers per cross-spec contract

  log to route_log(w)
```

output_artifacts:

- per-input regime_card and capability_match table
- per-input route_recommendation (ordered list)
- per-job route_log
- per-job route_regret distribution (one entry per chosen route)
- capability_card collection (static, but versioned)

## Evidence Signal Vector Used

active_signals:

- view_overlap (helps regime classification: low overlap -> sparse-view regime)
- pose_novelty (helps streaming vs collection regime classification)
- dynamic_ratio (read from Permanence; helps dynamic vs static regime classification)
- blur_or_low_light_score (helps prior-augmented regime classification when Cross-Modal exists)
- model_capability_match (Composer's primary internal signal; computed from regime_card + capability_card)

inactive_signals:

- pointmap_conflict (held by Critic; Composer does not own conflict detection)
- reprojection_residual (held by Critic)
- confidence_drop (held by Memory)
- latent_drift_proxy (held by Memory)
- loop_candidate_score (held by Memory)
- anchor_importance (held by Memory)
- cache_pressure (held by Memory)
- external_memory_overlap (held by Memory)
- prior_rgb_conflict (held by future Cross-Modal A7)
- object_track_stability (held by Permanence; informational read only)
- uncertainty_area (held by future Active Perception A8)

derived_signals:

- regime_card (per-input; weighted regime probabilities)
- capability_match (per-model-per-input; card join)
- route_regret (per-chosen-route-per-input; gap to best-known match)
- spread (per-input; max - min across comparator pool)

## Action Policy Definition

| Action | Trigger condition | Scope of effect | Failure-aware fallback |
|---|---|---|---|
| A5 publish_capability_match | every input window | informational publication; downstream specs may consume | if `capability_card` has unknown evidence label for a model, publish anyway with `unknown` label propagated; do not silently fill |
| A5 publish_route_recommendation | every input window | ordered list of model_ids; downstream Critic A5 reroute_model may bind | if all candidates have been tried (per Critic route_history), recommendation is empty; Critic must downgrade to conflict_unresolved per CR-1 |
| A5 publish_route_regret | every input window after route is chosen | informational; primary axis for P5 falsification | if no route was chosen (e.g. Critic accepted first output), route_regret is undefined for the window; log "no_route_chosen" rather than zero |
| A5 publish_regime_card | every input window | informational; downstream specs may use it for regime-conditioned policy | if regime classification is ambiguous (multiple regimes near 0.5 probability), publish as multi-regime card with explicit ambiguity flag; do not pick |

## Proxy Validation Plan

primary_proxy: P5 route regret

secondary_proxy: capability_match

case_cards_to_fill:

```text
CASE-20260505-COMPOSER-01  Fast3R vs Spann3R on shared input (static
                            collection medium); existing KYKT job pair
                            20260425-113002 + 20260425-113227
CASE-20260505-COMPOSER-02  MASt3R vs MonST3R for static pair vs dynamic
                            video regime distinction; existing KYKT
                            jobs 20260420-222729 + 20260420-222928
CASE-20260505-COMPOSER-03  Fast3R vs MASt3R-SfM for many-view vs pair
                            regime distinction; existing KYKT job
                            20260425-113002 (Fast3R many-view) + paper
                            example for MASt3R-SfM (no fresh job)
```

These IDs are reserved here; cycle 009 fills them via `templates/proxy_case_card.md`.

acceptance_threshold:

```text
On the labeled L2 cases (3 case cards):
  route_regret(Composer) < route_regret(single-default-model baseline)
      on at least 2 of 3 case cards
  AND capability_match has nonzero spread on every case card (i.e. the
      cards distinguish at least two model regimes)
  AND `policy_log` shows that on at least 1 case card the recommendation
      flipped between cards (i.e. Composer is regime-conditioned, not a
      hidden single-policy)
  AND the cross-spec signal contract test (Critic A5 consuming
      Composer's `capability_match`) succeeds: at least 1 Critic case
      card in cycle 009 reads a Composer-published `capability_match`
      and produces a non-trivial reroute_model decision.
```

fail_fast_threshold:

```text
If after the cycle 009 case cards:
  route_regret has zero spread across all three case cards (Composer
      cannot distinguish any regime)
  OR capability_card collection has fewer than 2 models with
      paper-proven evidence labels (Composer is leaning entirely on
      inferred capabilities)
  OR Critic A5 reroute_model cannot consume Composer's
      `capability_match` because of a contract mismatch
then retire Composer to "support layer only" status (no cycle 010
redraft of this finalist spec). Capability cards may still be used
informally by Critic, but Composer does not return as a finalist.
```

writing_value_if_only_negative_result:

```text
A clean negative is paper-relevant: it shows that capability cards
without learned weighting cannot beat single-default-model selection,
which precisely frames the F6 problem and motivates a learned router
or a hybrid card-plus-feedback router as future work. The negative
result documented via route_regret distribution + per-case capability
spread is acceptable cycle 009 output.
```

## Teacher Demo Form

what_is_visible:

```text
A two-panel demo over an existing KYKT job pair:
  Panel A: input thumbnail + computed regime_card bar chart (showing
           the input is X% static_pair, Y% dynamic_video, Z%
           sparse_view, etc.)
  Panel B: capability_match table for the comparator set, sorted; the
           chosen model is highlighted; the route_regret value is
           rendered as a bar against the best-known match.

Side-by-side: same input run under "default model only" policy versus
"Composer route_recommendation" policy, with the route_regret gap
visible.
```

why_it_surprises_a_teacher:

```text
The teacher sees the system explain *why* one 3R model is chosen over
another for this specific input regime, with a quantified regret if the
default model had been used. This is not an evaluation table from a
paper; it is a per-input, per-regime decision trace. Most published 3R
demos show one model on one input; this shows the choice itself.
```

artifact_format:

- markdown report with embedded image references and capability_match tables
- no live model inference; everything is offline post-processing of existing KYKT job artifacts plus paper-derived capability cards
- demo can be rendered alongside a Critic timeline (Critic consumes Composer's signals at cycle 009 case-card time)

approval_required_for_demo: yes

```text
Per DEC-20260504-002, the first teacher demo target is deferred until
cycle 009 case-card data exists. This demo form is described for
planning, not authorized for showing. KYKT navigation change is
separately approval-gated and is NOT part of this spec.
```

## KYKT Integration Surface

surface_list:

- research_lane (Composer route_log as research artifact)
- advisor_report (per-job route_recommendation + route_regret attaches to Advisor output)

NOT in scope this spec:

- runner (no runner change; Composer reads existing job outputs and paper-derived capability cards)
- sample_matrix (no scoring matrix change; Composer publishes capability_match, not a metric value)
- system_readiness (no system change)
- management_area (no navigation change)
- a new model_catalog entry (no new model)

backend_contract_needed:

```text
Read-only access to existing job artifact paths under model_uploads/
plus paper-derived capability cards stored as markdown / JSON inside
Dream. No new backend service. No schema migration. No new endpoint.
```

frontend_handoff_needed: no

frontend_handoff_brief_id: not_applicable_yet

```text
Frontend display of the Composer panel is a downstream decision. It
would go through handoff/FRONTEND_DESIGN_HANDOFF_PROMPT.md to Gemini
CLI ONLY after user approval of the demo and a KYKT navigation
decision.
```

## Engineering Cost

L1_design_cost: low

```text
This spec plus three case cards in cycle 009. ~4-6 hours of synthesis
work. Annotation budget per case card: 90-120 minutes per cycle 008 D4
(DEC-20260504-002 implies the same ceiling for parallel tracking).
Composer's annotation cost is regime classification + capability card
verification, not pixel-level labeling, so the 90-minute end of the
range is the expected actual labeling time.
```

L2_proxy_cost: low

```text
Lower than Memory and Permanence. Capability cards are paper-derived
markdown / JSON; sample regime cards are metadata classifications;
route_regret is a card join. No model invocation. No checkpoint
download. No fresh KYKT job required (case 03 uses paper example for
MASt3R-SfM since no MASt3R-SfM job exists yet in KYKT).
```

L3_prototype_cost: blocked_until_approval

L4_model_change_cost: blocked_until_approval

## Risks

novelty_risk:

```text
Highest of the four finalists if route_regret has zero spread across
case cards. Mitigated by the explicit fail-fast threshold: if zero
spread, Composer retires to support-layer status; no redraft. The
route_regret axis is the falsifying lever; a Composer that cannot
distinguish regimes has no paper claim.
```

overlap_with_comparator:

```text
No direct 3R comparator. Closest analog is MoE routing literature.
Mitigated by 3R-specific regime card definition (static_pair,
many_view, dynamic_video, streaming, sparse_view) rather than learned
expert ids. The paper claim is "regime-typed route_regret on 3R", not
"routing in general".
```

engineering_risk:

```text
Low. Capability cards are paper-derived; sample regime cards are
metadata-derived. The risk is capability card *staleness* if a
comparator paper publishes a new regime claim mid-cycle; mitigated by
the version stamp on each capability_card and by Discipline rule 5
(retracted card claims must be visible).
```

demo_risk:

```text
Composer demo is text-heavy (capability_match tables, regime bar
charts) compared to Permanence's visual timeline. Mitigated by
explicitly pairing Composer demo with a Critic timeline panel so the
combined demo has a visual narrative axis.
```

paper_writing_risk:

```text
"Composer" is rhetorically system-flavored. The paper claim must shift
to "regime-typed route_regret on 3R" with the F6 fragmentation framing,
or risk being read as engineering. Mitigated by the
`literature/SPINE_COMPOSER.md` framing (drafted in this same session)
that anchors the claim against MoE routing as the cross-domain analog.
```

## Evidence Labels

mechanism_status: inferred

```text
Capability cards are paper-derived (paper-proven for the per-model
claims they cite). Sample regime cards are inferred (no published
3R-specific regime taxonomy). The composition (regime_card x
capability_card -> capability_match) is inferred. The closed loop
A5 reroute_model -> Composer recommendation -> Critic consume is
inferred; not yet demonstrated in any single source.
```

action_policy_status: inferred

```text
epsilon_tie, regime probability weights, capability_match weighting,
and the route_recommendation tie-handling order are inferred. No
measurement yet.
```

performance_status: unknown

```text
No benchmark numbers. No claim of accuracy improvement over any
single-default-model baseline. Cycle 009 case cards produce L2 proxy
evidence only.
```

contract_status: inferred

```text
The cross-spec signal contract (`paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md`)
v1 has not been exercised by any case card. Cycle 009 is the first
test. Contract revisions move to a new version per the contract's own
versioning rules.
```

## Boundaries

no_reproduction_yet: yes

no_training_yet: yes

no_checkpoint_download_yet: yes

no_kykt_navigation_change: yes

no_frontend_implementation_yet: yes

no_thesis_spine_status: yes

```text
Per DEC-20260504-002, Composer is not the thesis spine. Even if cycle
009 case cards strongly support the route_regret claim, that does NOT
authorize promoting Composer to thesis status without a separate user
decision.
```

approval_gates_required_to_advance:

- moving from L2 case-card evidence to L3 prototype runner: requires user approval
- adding a KYKT navigation surface for the Composer panel: requires user approval
- declaring this spec the final Dream thesis: requires user approval (and DEC-20260504-002 explicitly forbids treating any single finalist as thesis spine)
- training a learned router: requires user approval
- adding new comparator models to the capability_card collection beyond those already in `registry/source_registry.md`: requires user approval (because it implies a new source intake pass)

## Linked Artifacts

linked_research_units:

- RU-002 3R Composer Controller (primary; this spec is the SPEC drafting that promotes RU-002 to `spec_drafted`)
- RU-008 Pose-Free Gaussian Demo Bridge (related; Composer routes asset-path samples to Splatt3R / NoPoSplat / InstantSplat)
- RU-014 Long-Context Hybrid Memory Benchmark (related; Composer's regime card complements the benchmark spine)

linked_sources: DUSt3R, MASt3R, MASt3R-SfM, Fast3R, Spann3R, MonST3R, CUT3R, STream3R, SLAM3R, MV-DUSt3R+, Splatt3R, InstantSplat, NoPoSplat (see `registry/source_registry.md` for IDs)

linked_failure_modes: F6 (primary), F3, F1, F2

linked_actions: A5 (owned, routing facet), A3 (read-only support), A4 (read-only support), A7 (read-only support)

linked_proxy_metrics: P5 (primary), capability_match (secondary; defined in P5 protocol)

linked_cycle: CYCLE-20260504-001 (cycle 008.5 closeout)

linked_kykt_jobs:

- 20260420-222729 (MASt3R static pair)
- 20260420-222928 (MonST3R 48-frame dynamic)
- 20260425-113002 (Fast3R many-view)
- 20260425-113227 (Spann3R many-view)
- pending: paper example for MASt3R-SfM in case-03 (no fresh KYKT job; per `cycles/CYCLE-20260503-002.md` Operating Constraints)

linked_cross_spec_contract: `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v1

## Next Step

planned_only: yes

next_action: fill_case_cards

linked_next_artifact:

- `templates/proxy_case_card.md` -> populated as CASE-20260505-COMPOSER-01..03 in cycle 009

## Next Discussion Point For The User

```text
Composer is the cheapest-to-falsify finalist by route_regret spread.
Three open user decisions:

  1. Cycle 009 ordering: Critic case cards run first per cycle 008 D1.
     Should Composer case cards run in parallel with Critic (because
     Critic A5 consumes Composer's capability_match), or sequentially
     after Critic? Default: parallel; the cross-spec contract is the
     test path.
  2. Capability card source: paper-derived only (cheaper, may miss
     regime nuance) vs paper-derived + KYKT-job-derived (slower, more
     specific to KYKT inputs). Default: paper-derived only for cycle
     009; KYKT-derived deferred to cycle 010.
  3. Per DEC-20260504-002 the first teacher demo target is deferred.
     If Composer case cards land first with strong route_regret spread,
     this spec's two-panel form becomes a candidate. The agent will not
     pick on the user's behalf; resurface this question after cycle 009
     case-card data exists.
```
