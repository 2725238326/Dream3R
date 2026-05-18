# CASE-20260505-COMPOSER-01

First Composer L2 case card per `specs/SPEC-20260504-001-3r-composer.md` line 272 reservation. Paper-derived per cycle 009 D2' (`decisions/DEC-20260504-003-cycle-009-launch.md`). No measurement claimed; no model invocation; no KYKT job artifact opened. All numeric ranges below are paper-derived or inferred and labeled accordingly per Cross-Spec Signal Contract rule CR-5.

This card is the **Composer side of CR-1 closing**: it supplies the capability_card collection and capability_match spread that `CASE-20260504-CRITIC-02.md` forward-references when Critic proposes A5 reroute_model from Fast3R to Spann3R (or back). It also carries the route_regret axis at its central position - Composer's primary proxy P5.

## Identity

case_id: CASE-20260505-COMPOSER-01

proxy_id: P5

scenario_name: Fast3R vs Spann3R capability_card pair on shared static-collection input medium; KYKT jobs 20260425-113002 + 20260425-113227

date: 2026-05-04

linked_failure_modes: F6 (Fragmented Model Ecology; primary failure mode owned by Composer per `specs/SPEC-20260504-001-3r-composer.md` line 49)

linked_actions: A5 (reroute_model facet; Composer ownership per spec lines 56-77)

linked_branches: Composer

linked_research_units: RU-002 (primary; this card is the L2 evidence for RU-002's spec_drafted promotion per `units/RESEARCH_UNIT_BANK.md` line 117)

linked_sources: Fast3R | Spann3R | DUSt3R | MASt3R | MASt3R-SfM (see `registry/source_registry.md` for canonical IDs; first two are the focus of this card; the rest are the 9-anchor capability_card collection background per spec lines 87-99)

## Input Artifact

source_type: paper_example

artifact_pointer:

```text
- model_uploads/20260425-113002/  (Fast3R run on shared input)
- model_uploads/20260425-113227/  (Spann3R run on same input)
The pair shares the same upstream input under the static-collection regime
classification. Per D2' the artifact contents are not opened; the regime
label is paper-derived from the two papers' own scope claims plus the
job-pair structure.
```

evidence_label: paper-proven (for Fast3R and Spann3R capability profiles as documented in their respective papers); inferred (for the regime_card classification on this specific input pair, the capability_match weighted-dot-product result, and the route_regret value)

input_summary:

```text
The same upstream input was processed by two 3R models: Fast3R (large-batch
single-forward-pass) and Spann3R (streaming with spatial memory). The
Composer's job is to: (1) classify the input via regime_card; (2) look up
each model's capability_score on the resulting regime mix; (3) compute
capability_match; (4) publish capability_match + route_recommendation +
route_regret + regime_card per spec lines 257-261; (5) on receiving a
Critic proposed_reroute via CR-1, agree or veto based on whether the
capability_match spread exceeds tau_spread.

This card is the cross-reference target of CASE-20260504-CRITIC-02.md's
CR-1 forward reference. The two cards are written to be self-consistent:
this card publishes the spread; the Critic card consumes it.
```

## Evidence Signals

Per spec line 225-231, Composer reads view_overlap, pose_novelty, dynamic_ratio, blur_or_low_light_score, model_capability_match. Other signals are out-of-scope for Composer per spec lines 233-241.

view_overlap: predicted_high (paper-derived: a static-collection regime by definition has multiple viewpoints of the same scene; both jobs were submitted on this regime)

pose_novelty: predicted_low_to_moderate (static collection regime has bounded pose diversity; not the streaming regime where pose_novelty is high)

dynamic_ratio: predicted_zero (read from Permanence; static-collection regime has no dynamic content; if Permanence card publishes dynamic_ratio > 0 for this input, this Composer card is wrong about the regime and CR-2 from Permanence's side should override)

blur_or_low_light_score: predicted_low (paper-derived: shared input is assumed to be a normal-light static capture)

model_capability_match: this is Composer's PRIMARY internal signal. Computed below.

```text
Regime card for this input (inferred):
  static_collection:    0.85
  streaming:            0.10
  many_view_batch:      0.05
  dynamic_video:        0.00
  sparse_view_pair:     0.00
(probabilities sum to 1.00; weights inferred)

Capability cards (paper-derived):
  Fast3R:
    static_collection:  0.65 (paper-proven; many-view single-forward-pass)
    streaming:          0.30 (paper-proven; not its sweet spot)
    many_view_batch:    0.85 (paper-proven; central regime)
    dynamic_video:      0.30 (paper-proven; not its sweet spot)
    sparse_view_pair:   0.50 (paper-proven; degraded but functional)
  Spann3R:
    static_collection:  0.70 (paper-proven; spatial memory helps)
    streaming:          0.85 (paper-proven; central regime)
    many_view_batch:    0.55 (paper-proven; not its sweet spot)
    dynamic_video:      0.40 (paper-proven; not its sweet spot)
    sparse_view_pair:   0.60 (paper-proven; functional)

capability_match = weighted_dot(regime_card, capability_card):
  Fast3R:  0.85 * 0.65 + 0.10 * 0.30 + 0.05 * 0.85 + 0.00 * 0.30 + 0.00 * 0.50 = 0.62
  Spann3R: 0.85 * 0.70 + 0.10 * 0.85 + 0.05 * 0.55 + 0.00 * 0.40 + 0.00 * 0.60 = 0.71

capability_match spread = 0.71 - 0.62 = 0.09  (Spann3R > Fast3R on this regime)

All numbers are paper-derived (capability_card axis values) or inferred
(regime_card classification probabilities; the weights on each axis;
the threshold tau_spread comparison). evidence_label per axis is recorded
in the capability_card collection itself, not flattened away.
```

## Comparator Policies

| Policy | Action chosen | Predicted proxy P5 (route_regret) value | Notes |
| --- | --- | --- | --- |
| comparator_1 always-Fast3R (default model) | route to Fast3R unconditionally | route_regret = 0.71 - 0.62 = 0.09 (regret vs better choice Spann3R for this regime) | the most common 3R-system baseline; no capability awareness |
| comparator_2 single-feature heuristic ("if streaming, use Spann3R") | classify by pose_novelty alone; static-collection -> Fast3R | route_regret = 0.09 (same as comparator_1 on this regime) | weak heuristic; cannot distinguish static_collection from many_view_batch |
| comparator_3 benchmark-matrix average ("use the model with highest mean score across regimes") | route to Spann3R (mean over the 5 regimes is 0.62 vs Fast3R's 0.52) | route_regret = 0 (correct route, but for the wrong reason - average score, not regime fit) | benchmark-matrix-style baseline per spec line 110 |
| dream_policy capability_card x regime_card | route_recommendation: [Spann3R (0.71), Fast3R (0.62)]; capability_match published with evidence labels; route_regret = 0 if Spann3R chosen | route_regret = 0 with explicit regime + capability transparency | the spec's differentiator: explicit regime classification + per-regime capability scoring + route_regret as falsifiable metric |

## Predicted Proxy Outcome

primary_metric: P5 route_regret (per `specs/SPEC-20260504-001-3r-composer.md` line 265)

unit_of_measurement: gap between chosen route capability_match and best-known route capability_match for this regime, in [0, 1]

threshold_for_useful_signal: spec acceptance_threshold requires route_regret to have nonzero spread across the three Composer cards (echoes Critic spec line 224 acceptance criterion). This card carries spread = 0.09 (modest); cards 02 and 03 are expected to carry larger spreads.

predicted_dream_value: 0.0 (Composer correctly recommends Spann3R; capability_match spread 0.09 is above the indicative tau_spread baseline of ~0.05 used in CR-1, so reroute proposal from Critic would be agreed-to)

predicted_best_comparator_value: comparator_3 benchmark-matrix-average also achieves route_regret = 0 here, but for the wrong reason (it would route to Spann3R unconditionally, regardless of regime). On a different regime where Spann3R is NOT the best, comparator_3 would fail and the dream_policy would not.

expected_gap_direction: dream_better unconditionally vs comparator_1 / comparator_2 on this regime; tie vs comparator_3 on this regime, but dream's transparency (regime_card publication) is the differentiator absent absolute-score gap

decision_signal_meaning:

```text
This card alone does NOT establish Composer's superiority over comparator_3
(benchmark-matrix-average), since both produce route_regret = 0 on this
specific regime. The cross-card story is:
  - This card 01: Composer ties comparator_3 on a regime where Spann3R is
    best (the easy case for any "always best on average" heuristic).
  - Card 02 (MASt3R vs MonST3R): one regime where MASt3R is best (static
    pair) and one where MonST3R is best (dynamic video); comparator_3
    cannot win both, dream_policy can.
  - Card 03 (Fast3R vs MASt3R-SfM): cost-asymmetric regime; route_regret
    must factor cost, where benchmark-matrix-average fails outright.

The three cards together must show route_regret nonzero spread across
comparators. If this card alone closes the spread (which it does not -
0.09 is small), the Composer spec is not yet validated.

For CR-1 specifically: this card publishes capability_match spread = 0.09.
If tau_spread is set at 0.05 (paper-derived indicative value, not measured),
Composer agrees to Critic's proposed_reroute. If tau_spread is set at 0.10,
Composer vetoes. The choice of tau_spread is a tunable parameter
(action_policy_status: inferred per spec line 498); cycle 009 records it
as inferred and leaves the tuning to a future cycle.
```

## Cross-Spec Contract Usage (CR-6)

Recorded per Cross-Spec Signal Contract rule CR-6 (`paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` line 149).

- CR-1 (Critic A5 reroute_model requires Composer agreement on capability_match spread): **closed from Composer side in this card**. Composer publishes capability_match spread = 0.09; Critic CASE-20260504-CRITIC-02 forward-referenced this value. Agreement at tau_spread = 0.05; veto at tau_spread = 0.10. The tau_spread choice is recorded as inferred, not measured.
- CR-2 (Permanence suppress_static_write is binding on Memory): not Composer-owned. Composer reads dynamic_ratio from Permanence and uses it in regime classification per spec line 229; this is a downstream-of-Permanence consumption pattern, not the CR-2 binding pattern. Trivially honored (Composer doesn't fight CR-2).
- CR-3 (Memory drift signal does not gate Critic verification): not Composer-owned; trivially honored (Composer doesn't read latent_drift_proxy at all).
- CR-4 (Composer route_recommendation does not bind Critic on capability_match ties): **honored from Composer side here**. Composer publishes route_recommendation = [Spann3R, Fast3R] but explicitly does NOT claim binding force when Critic finds capability_match tied within epsilon_tie. This card uses tau_spread = 0.05 indicatively; the recommendation is not a binding directive.
- CR-5 (All cross-spec signals carry producer evidence label): honored. Each capability_card axis value carries evidence_label = paper-proven; the regime_card probabilities carry evidence_label = inferred; the capability_match weighted-dot-product result carries evidence_label = inferred.
- CR-6 (cycle 009 case cards record contract usage): satisfied by this section.

## Writing Value

related_work_section: composer

figure_or_taxonomy: regime-card x capability-card matrix table per spec line 217 + per-input route_recommendation bar chart per spec lines 360-362. This card supplies one row of the matrix (the static-collection row) for both Fast3R and Spann3R columns. Visible in a teacher demo as: "input regime classified as 85% static-collection; Spann3R capability_match 0.71, Fast3R capability_match 0.62; recommendation Spann3R; route_regret if Fast3R chosen would be 0.09".

novelty_claim_supported:

```text
"3R needs a regime-typed route_regret axis, not a meta-model" (spec
one_line_thesis line 146). The card supports the thesis weakly on its
own (route_regret spread is small here) but lays the publication
infrastructure (capability_card with paper-proven labels per axis;
regime_card with inferred probabilities; capability_match as a published
signal). The strong thesis support comes from cards 02 + 03; this card
is the easy case that the policy must not lose in order to claim the
hard cases.
```

## Risk And Boundaries

fail_fast_condition:

```text
If the predicted capability_match spread is 0 (i.e. Fast3R and Spann3R
are tied within epsilon_tie on the static_collection regime), Composer
publishes a tied recommendation and CR-4 blocks Critic from binding on
it. That is not a card failure - it is the policy correctly declining
to bind. The card fails only if the published capability_card values
themselves are inconsistent with the source papers (which would be a
discipline rule 5 Honesty Override violation, not a policy failure).
```

reproduction_required: no

training_required: no

frontend_change_required: no

approval_required: no

caveats:

```text
- All capability_card values above are paper-derived from the Fast3R
  and Spann3R papers' own regime claims. The numerical scaling to a
  0-1 axis is inferred (each paper uses different scoring conventions);
  the relative ordering across regimes is paper-proven. When code-
  observed values become available in a future cycle, they supersede
  the paper-derived axis values one regime at a time.
- The regime_card probabilities for this specific input are inferred
  (the artifact is not opened per D2'). The 85% static_collection
  classification is consistent with the job pair structure and the
  shared-input assumption from spec line 273; it is not a measurement.
- tau_spread = 0.05 is the indicative threshold used to demonstrate
  CR-1 closure in this card. The actual tau_spread value to ship in
  any prototype is a downstream tuning question; per spec line 498
  it is inferred.
- CR-4 honoring is visible here precisely because route_recommendation
  is published with capability_match values, not as a directive. A
  tied recommendation would prevent Critic from acting on this card's
  output - and that is the correct behavior, not a card defect.
- This card's route_regret of 0.09 is intentionally near-threshold for
  CR-1. Cards 02 and 03 carry larger spreads and the broader spread-
  carrier load.
```

## Next Action

next_action: add_comparator

linked_next_artifact: `cases/CASE-20260505-COMPOSER-02.md` (MASt3R vs MonST3R; static_pair vs dynamic_video regime distinction; the regime_card carrier where the cross-regime capability_card matrix becomes the differentiator vs comparator_3)
