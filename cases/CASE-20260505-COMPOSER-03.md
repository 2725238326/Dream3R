# CASE-20260505-COMPOSER-03

Third Composer L2 case card per `specs/SPEC-20260504-001-3r-composer.md` line 278 reservation. Paper-derived per cycle 009 D2' (`decisions/DEC-20260504-003-cycle-009-launch.md`). No measurement claimed; no model invocation; no KYKT job artifact opened. All numeric ranges below are paper-derived or inferred and labeled accordingly per Cross-Spec Signal Contract rule CR-5.

This card is the **cost-asymmetric route_regret carrier**. Unlike cards 01 and 02, where the route_regret axis as defined in `specs/SPEC-20260504-001-3r-composer.md` line 187 (capability_match gap only) is sufficient, this card surfaces a v1 contract limit: when two models have similar capability_match but very different cost, capability-only route_regret is degenerate. The card produces a concrete v2 candidate for the route_regret signal definition and is therefore the most paper-relevant of the three Composer cards.

## Identity

case_id: CASE-20260505-COMPOSER-03

**Status note (2026-05-04, cycle 010 launch)**: per `decisions/DEC-20260504-004-cross-spec-contract-v2.md`, the cross-spec signal contract was promoted from v1 to v2 at cycle 010 launch. v2 makes `route_regret` regime-typed AND cost-typed by adding a `cost_normalized` axis to `capability_match` and exposing `cost_adjusted_match` as an additional output (alpha = 0.5 initial; inferred). On this card, the **v2 (cost-adjusted) recommendation is the canonical reading**: input 1 -> Fast3R (cost-leaning); input 2 -> tied at alpha = 0.5, surfaces to Advisor via CR-4. The **v1 (capability-only) recommendation is preserved** in the Comparator Policies table (`dream_policy v1` row) and in this card's "Predicted Proxy Outcome" -> `predicted_dream_value` block, per Discipline rule 5 (Honesty Override); v1 picked MASt3R-SfM unconditionally on input 2. Below text is unchanged from the cycle 009 draft except for this status note and the CR-4 entry in "Cross-Spec Contract Usage (CR-6)" (updated to v2-canonical).

proxy_id: P5

scenario_name: Fast3R vs MASt3R-SfM capability_card pair across many-view-batch and sparse-view-pair regimes; KYKT job 20260425-113002 (Fast3R many-view) + paper example for MASt3R-SfM (no fresh job per spec line 280)

date: 2026-05-04

linked_failure_modes: F6

linked_actions: A5 (reroute_model facet)

linked_branches: Composer

linked_research_units: RU-002

linked_sources: Fast3R | MASt3R-SfM | MASt3R | DUSt3R (background; see `registry/source_registry.md`)

## Input Artifact

source_type: paper_example

artifact_pointer:

```text
- model_uploads/20260425-113002/  (Fast3R many-view run; cross-referenced
  by CASE-20260505-COMPOSER-01 for the static-collection regime; here
  re-used for the many-view-batch regime classification)
- paper_example for MASt3R-SfM on a pair regime (no fresh KYKT job per
  spec line 280; the paper-example pointer is the MASt3R-SfM paper's
  reported pair-regime numbers)
```

evidence_label: paper-proven (for Fast3R and MASt3R-SfM capability profiles + paper-reported cost characteristics); inferred (for the regime classifications, the capability_match values, and the proposed cost-adjusted v2 route_regret formula)

input_summary:

```text
The card pairs a many-view-batch input (Fast3R native sweet spot) with
a sparse-view-pair regime example (where MASt3R-SfM extends MASt3R into
the small-collection regime). Capability scores favor each model on its
own regime, but the capability spread is much narrower than card 02's,
because both models can technically handle both regimes - the difference
is cost, not capability. This is exactly the regime where the spec's
current route_regret definition (capability_match gap only) is degenerate.
```

## Evidence Signals

view_overlap: input 1 (many-view): predicted_high; input 2 (paper-example pair): predicted_low (narrow-baseline)

pose_novelty: input 1: predicted_high (many distinct viewpoints); input 2: not_applicable (single-pair transformation)

dynamic_ratio: predicted_zero on both inputs (neither input is a dynamic-content video)

blur_or_low_light_score: predicted_low on both

model_capability_match: this is Composer's PRIMARY internal signal. Computed below.

```text
Regime cards (inferred):
  Input 1 (job 20260425-113002, Fast3R many-view):
    many_view_batch:    0.90
    static_collection:  0.10
    sparse_view_pair:   0.00
    dynamic_video:      0.00
  Input 2 (paper-example pair regime):
    sparse_view_pair:   0.90
    static_collection:  0.10
    many_view_batch:    0.00
    dynamic_video:      0.00

Capability cards (paper-derived; relative ordering paper-proven):
  Fast3R:
    many_view_batch:    0.85  (sweet spot per Fast3R paper)
    static_collection:  0.65
    sparse_view_pair:   0.50  (degraded but functional)
    dynamic_video:      0.30
    streaming:          0.30
  MASt3R-SfM:
    many_view_batch:    0.65  (functional but heavyweight; SfM scales
                              poorly with input count by paper claim)
    static_collection:  0.75
    sparse_view_pair:   0.85  (sweet spot; extends MASt3R-pair to small
                              collections via retrieval + global SfM)
    dynamic_video:      0.20
    streaming:          0.20

capability_match per input per model (inferred):
  Input 1 (many-view):
    Fast3R:     0.90*0.85 + 0.10*0.65 = 0.830
    MASt3R-SfM: 0.90*0.65 + 0.10*0.75 = 0.660
    capability spread = 0.170  (Fast3R wins on capability)
  Input 2 (pair):
    Fast3R:     0.90*0.50 + 0.10*0.65 = 0.515
    MASt3R-SfM: 0.90*0.85 + 0.10*0.75 = 0.840
    capability spread = 0.325  (MASt3R-SfM wins on capability)

Cost cards (paper-derived; the v2 candidate axis not currently on the
capability_card, recorded here as a separate axis to surface the gap):
  Fast3R:
    cost_normalized: 0.20  (paper claims one-forward-pass over many images)
  MASt3R-SfM:
    cost_normalized: 0.85  (paper claims SfM-stage refinement is the
                            cost-dominating step)

cost-adjusted capability_match (v2 candidate; alpha = 0.5 illustrative):
  cost_adjusted = capability_match - alpha * cost_normalized
  Input 1:
    Fast3R:     0.830 - 0.5 * 0.20 = 0.730
    MASt3R-SfM: 0.660 - 0.5 * 0.85 = 0.235
    cost-adjusted spread = 0.495  (Fast3R wins by much wider margin)
  Input 2:
    Fast3R:     0.515 - 0.5 * 0.20 = 0.415
    MASt3R-SfM: 0.840 - 0.5 * 0.85 = 0.415
    cost-adjusted spread = 0.000  (TIE: MASt3R-SfM's pair-regime advantage
                                   is exactly offset by its cost overhead
                                   at alpha = 0.5)

The alpha tie is the v2 route_regret signature: the spec's current
capability-only definition declares MASt3R-SfM the winner on input 2 by
0.325; cost-adjusted definition declares it a tie. Whether to ship the
recommendation as MASt3R-SfM (capability-leaning) or Fast3R (cost-
leaning) becomes the user-facing decision, and CR-4 prevents Critic from
binding on the tie.
```

## Comparator Policies

| Policy | Action chosen | Predicted route_regret on input 1 / input 2 / mean | Notes |
| --- | --- | --- | --- |
| comparator_1 always-Fast3R | route to Fast3R unconditionally | 0 / 0.325 / 0.163 (capability-only); 0 / 0 / 0 (cost-adjusted at alpha=0.5) | wins on cost; loses on input 2 capability |
| comparator_1' always-MASt3R-SfM | route to MASt3R-SfM unconditionally | 0.170 / 0 / 0.085 (capability-only); 0.495 / 0 / 0.248 (cost-adjusted) | symmetric baseline; loses heavily on cost-adjusted axis |
| comparator_2 single-feature heuristic ("if input_count > 10, use Fast3R, else MASt3R-SfM") | routes correctly on this 2-regime split | 0 / 0 / 0 (capability-only); 0 / 0 / 0 (cost-adjusted) | wins on this card by coincidence (input_count is a sufficient discriminator); the spec's "single-feature heuristics break" argument requires more regimes than this card alone exercises |
| comparator_3 benchmark-matrix-average | tied: Fast3R mean = 0.52, MASt3R-SfM mean = 0.55; picks MASt3R-SfM by tiebreak | 0.170 / 0 / 0.085 (capability); 0.495 / 0 / 0.248 (cost-adjusted) | comparator_3 collapse appears here too: averaging across regimes loses the cost signal entirely |
| dream_policy v1 (capability_match only, per spec line 187) | route per input by capability_match: Fast3R for input 1, MASt3R-SfM for input 2 | 0 / 0 / 0 (capability-only) | passes the spec's current acceptance gate but ignores cost |
| dream_policy v2 candidate (cost-adjusted) | route per input by cost_adjusted match: Fast3R for input 1, undecided/tied for input 2; CR-4 prevents Critic binding on the tie | 0 / 0 / 0 (cost-adjusted at alpha=0.5) | the v2 proposal: route_regret incorporates cost; ties become explicit user-facing decisions instead of silent capability-leaning picks |

## Predicted Proxy Outcome

primary_metric: P5 route_regret

unit_of_measurement: gap between chosen route capability_match (or cost_adjusted match) and best-known route value for this regime, in [0, 1]

threshold_for_useful_signal: spec acceptance_threshold requires nonzero route_regret spread across the three Composer cards. This card's spread under v1 is 0.170 / 0.325 across the two inputs; under v2 it is 0.495 / 0 (with the v2 tie surfacing as the user-facing decision).

predicted_dream_value:

- v1 dream_policy: 0 / 0 / 0
- v2 dream_policy: 0 / 0 / 0 with explicit tie publication on input 2

predicted_best_comparator_value: comparator_2 single-feature heuristic ties dream_policy on this specific 2-regime card; comparator_3 collapse mean is 0.085 (capability-only) or 0.248 (cost-adjusted)

expected_gap_direction: dream_better unconditionally vs comparator_1 / comparator_1' / comparator_3; tie vs comparator_2 on this specific card; dream's transparency about cost is the differentiator absent absolute-score gap

decision_signal_meaning:

```text
The decisive signal in this card is NOT the route_regret value itself
(comparator_2 ties dream on this 2-regime card). The decisive signal is
that the v1 route_regret definition (capability_match gap only) is
inadequate for cost-asymmetric regimes - which the cost_normalized axis
above demonstrates with a single illustrative alpha value.

Three concrete v1 -> v2 candidates surfaced by this card:

  v2-A: Add cost_normalized axis to the capability_card collection.
        Each axis value carries its own evidence_label per CR-5.
  v2-B: Define route_regret as cost_adjusted_match instead of
        capability_match. Specify alpha as a tunable parameter on the
        Composer side.
  v2-C: Publish capability_match and cost_normalized as separate
        signals; let downstream consumers (Critic A5, Advisor) decide
        the alpha tradeoff per their own use case.

Recommendation surfaced for cycle 010 (NOT executed in cycle 009): adopt
v2-C, because it preserves CR-5 evidence-label discipline (cost data has
its own evidence_label, separate from capability data) and avoids
hardcoding alpha at the Composer level.
```

## Cross-Spec Contract Usage (CR-6)

Recorded per Cross-Spec Signal Contract rule CR-6 (`paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` line 149).

- CR-1 (Critic A5 reroute_model requires Composer agreement on capability_match spread): not exercised; this card is not the Critic-paired card. CR-1 closure for this regime would happen in a future Critic card targeting Fast3R-on-pair or MASt3R-SfM-on-many-view, neither of which is in cycle 009 scope.
- CR-2: trivially honored.
- CR-3: not Composer-owned; trivially honored.
- CR-4 (Composer route_recommendation does not bind Critic on capability_match ties): **exercised under v2 (canonical)**. Per `decisions/DEC-20260504-004-cross-spec-contract-v2.md`, the contract was promoted to v2 at cycle 010 launch; CR-4 now arbitrates ties on the cost_adjusted spread routinely, and on this card the tie at alpha = 0.5 on input 2 is the canonical CR-4 firing. The v1 framing — where CR-4 only protected against rare exact ties on capability-only spread — is preserved in this card's "Comparator Policies" table (the `dream_policy v1` row) and in `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` "Superseded versions" section, but is no longer the canonical interpretation.
- CR-5 (All cross-spec signals carry producer evidence label): honored. The proposed cost_normalized axis is recorded as a separate axis precisely to preserve its independent evidence_label (paper-proven from cost claims in respective papers; not flattened into the capability score).
- CR-6 (cycle 009 case cards record contract usage): satisfied by this section + the v1 -> v2 candidate enumeration above.

## Writing Value

related_work_section: composer

figure_or_taxonomy: a side-by-side capability_match table (v1) and cost_adjusted_match table (v2 candidate) on the same input. The v1-vs-v2 contrast is the central pedagogical artifact of this card; it shows that route_regret is regime-typed AND cost-typed, not just regime-typed.

novelty_claim_supported:

```text
"Regime-typed route_regret axis" thesis (spec line 146) is supported by
this card AND extended: the axis is also cost-typed in cost-asymmetric
regimes. This is the v1 -> v2 evolution path that the spec explicitly
allows for via Discipline rule 5 Honesty Override (paper-derived
predictions can be superseded; the v1 -> v2 transition is recorded
transparently rather than smuggled in).
```

## Risk And Boundaries

fail_fast_condition:

```text
If the cost_normalized values for Fast3R and MASt3R-SfM are similar
(both papers report comparable cost regimes), the v2 framing collapses
back to v1 and this card no longer carries the cost-asymmetry argument.
Mitigation: the cost asymmetry between one-forward-pass (Fast3R) and
SfM-pipeline (MASt3R-SfM) is large in both papers' own claims; the
risk of a degenerate cost_normalized spread is low.

If the user explicitly rejects the v2 candidate at the cycle 010
decision packet, this card downgrades to a v1-only card and the
narrative shifts to "regime-typed routing is the only Composer
differentiator", which is a weaker but still defensible thesis.
```

reproduction_required: no

training_required: no

frontend_change_required: no

approval_required: no

caveats:

```text
- The cost_normalized values are paper-derived from each paper's own
  cost discussion. The 0-1 normalization is inferred (papers use
  different cost units: GPU-seconds, FLOPs, batch latency).
- alpha = 0.5 is illustrative, not specified. Choosing alpha is itself
  a downstream tunable; cycle 009 records alpha as inferred and surfaces
  it as a cycle 010 decision.
- The MASt3R-SfM input is a paper example, not a fresh KYKT job (per
  spec line 280). The card is therefore even more paper-derived than
  cards 01 and 02; manual labeling on a fresh job for MASt3R-SfM is
  out of cycle 009 scope.
- The v2 contract candidate emerges from card 03 specifically; cards
  01 and 02 do not surface this gap because their regimes are not
  cost-asymmetric (cards 01 and 02 compare models with similar cost
  characteristics).
- The three Composer cards together exercise: capability_match
  publication (all 3); regime_card publication (all 3, with non-trivial
  classification in 02 and 03); route_recommendation (all 3); CR-1
  closing (01 only); regime-distinction differentiator vs comparator_3
  (02 + 03); cost-adjusted route_regret v2 surfacing (03 only). CR-2
  and CR-3 are not Composer-owned and not exercised by these three
  cards.
```

## Next Action

next_action: escalate_to_spec (the three Composer L2 cards now constitute the L2 evidence packet for SPEC-20260504-001; next move is cycle 009 S6 cross-spec contract usage audit, where the v1 -> v2 candidate from this card is one of the audit findings)

linked_next_artifact: cycle 009 S6 in `cycles/CYCLE-20260505-001.md` (contract usage audit; this card's v1 -> v2 candidate enumeration is one of the v2 promotion candidates the audit will weigh)
