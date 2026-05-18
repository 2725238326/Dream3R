# CASE-20260505-COMPOSER-02

Second Composer L2 case card per `specs/SPEC-20260504-001-3r-composer.md` line 275 reservation. Paper-derived per cycle 009 D2' (`decisions/DEC-20260504-003-cycle-009-launch.md`). No measurement claimed; no model invocation; no KYKT job artifact opened. All numeric ranges below are paper-derived or inferred and labeled accordingly per Cross-Spec Signal Contract rule CR-5.

This card is the **regime_card carrier**: it formalizes per-input regime classification and shows the comparator_3 (benchmark-matrix-average) collapse. Two different inputs of different regimes are routed to different models, which any "best on average" heuristic cannot do without losing on at least one of them.

## Identity

case_id: CASE-20260505-COMPOSER-02

proxy_id: P5 (primary; capability_match also carried prominently)

scenario_name: MASt3R vs MonST3R capability_card pair across static-pair and dynamic-video regimes; KYKT jobs 20260420-222729 + 20260420-222928

date: 2026-05-04

linked_failure_modes: F6

linked_actions: A5 (reroute_model facet)

linked_branches: Composer

linked_research_units: RU-002

linked_sources: MASt3R | MonST3R | DUSt3R | MASt3R-SfM (background; see `registry/source_registry.md`)

## Input Artifact

source_type: paper_example

artifact_pointer:

```text
- model_uploads/20260420-222729/  (MASt3R static pair; cross-referenced
  by CASE-20260504-CRITIC-01 from the Critic detection perspective)
- model_uploads/20260420-222928/  (MonST3R 48-frame dynamic video; cross-
  referenced by CASE-20260504-CRITIC-03 from the Critic detection
  perspective)
The two inputs are deliberately different regimes, not the same input run
through different models (which is the card 01 setup and the card 03
setup). Card 02 is the regime-distinction card.
```

evidence_label: paper-proven (for MASt3R and MonST3R capability profiles); inferred (for the regime_card classification probabilities, capability_match weighted-dot products, and the comparator_3 collapse argument)

input_summary:

```text
Two inputs of fundamentally different regimes are processed: a 2-frame
static pair (MASt3R's native sweet spot) and a 48-frame dynamic-content
video (MonST3R's native sweet spot). Composer's job is to classify each
input correctly and recommend the regime-fit model. The card's value is
the cross-regime spread: any "always model X" or "average across regimes"
heuristic must lose on at least one of the two inputs.

This card is the strongest defense against the spec's weakest_pressure
(line 117 "pure model routing reads as system engineering"): regime-typed
capability_match is what makes routing paper-grade, and a card that shows
two regimes routing differently is the cleanest way to demonstrate that.
```

## Evidence Signals

view_overlap: input 1 (static pair): predicted_low (narrow-baseline assumption; MASt3R paper failure-mode regime); input 2 (dynamic video): predicted_high overall, predicted_low on dynamic-occluded subwindows

pose_novelty: input 1: not_applicable (single transformation); input 2: predicted_present_per_frame (48-frame sequence)

dynamic_ratio: input 1: predicted_zero (static pair); input 2: predicted_high (96 dynamic masks per `specs/SPEC-20260503-001-geometry-critic.md` line 363)

blur_or_low_light_score: input 1: predicted_low; input 2: predicted_low (paper-derived; no evidence of low-light capture in either)

model_capability_match: this is Composer's PRIMARY internal signal. Computed below for both inputs.

```text
Regime cards (inferred):
  Input 1 (job 20260420-222729, MASt3R static pair):
    static_pair:        0.90
    static_collection:  0.10
    streaming:          0.00
    many_view_batch:    0.00
    dynamic_video:      0.00
  Input 2 (job 20260420-222928, MonST3R 48-frame):
    static_pair:        0.00
    static_collection:  0.15
    streaming:          0.00
    many_view_batch:    0.00
    dynamic_video:      0.85

Capability cards (paper-derived; relative ordering paper-proven, axis
scaling inferred):
  MASt3R:
    static_pair:        0.85
    static_collection:  0.70
    streaming:          0.40
    many_view_batch:    0.50
    dynamic_video:      0.20
  MonST3R:
    static_pair:        0.40
    static_collection:  0.55
    streaming:          0.65
    many_view_batch:    0.50
    dynamic_video:      0.85

capability_match per input per model (inferred; weighted dot product):
  Input 1 (static pair):
    MASt3R:  0.90*0.85 + 0.10*0.70 = 0.835
    MonST3R: 0.90*0.40 + 0.10*0.55 = 0.415
    spread = 0.420  (MASt3R >> MonST3R)
    recommendation: MASt3R
  Input 2 (dynamic video):
    MASt3R:  0.00*0.85 + 0.15*0.70 + 0.85*0.20 = 0.275
    MonST3R: 0.00*0.40 + 0.15*0.55 + 0.85*0.85 = 0.805
    spread = 0.530  (MonST3R >> MASt3R)
    recommendation: MonST3R
```

## Comparator Policies

| Policy | Action chosen | Predicted route_regret on input 1 / input 2 / mean | Notes |
| --- | --- | --- | --- |
| comparator_1 always-MASt3R | route to MASt3R unconditionally | 0 / 0.53 / 0.265 | wins input 1, loses input 2 |
| comparator_1' always-MonST3R | route to MonST3R unconditionally | 0.42 / 0 / 0.21 | wins input 2, loses input 1 |
| comparator_2 single-feature heuristic ("if dynamic_ratio > 0, use MonST3R") | classify by dynamic_ratio alone | 0 / 0 / 0 on this 2-input setup | the strongest comparator on this specific card; would fail on a card with sparse-view-pair regime where dynamic_ratio = 0 but MASt3R is still wrong (e.g. many-view batch) |
| comparator_3 benchmark-matrix-average ("use the model with highest mean capability across regimes") | tied: MASt3R mean = 0.59, MonST3R mean = 0.59; tiebreaker pick one (e.g. always-first MASt3R) | 0 / 0.53 / 0.265 (if MASt3R picked) or 0.42 / 0 / 0.21 (if MonST3R picked) | **the comparator_3 collapse**: averaging across regimes destroys the regime signal; cannot win both inputs |
| dream_policy capability_card x regime_card | route per input: MASt3R for input 1, MonST3R for input 2 | 0 / 0 / 0 | wins both inputs because it does NOT collapse the regime axis |

## Predicted Proxy Outcome

primary_metric: P5 route_regret

unit_of_measurement: gap between chosen route capability_match and best-known route capability_match for this regime, in [0, 1]; reported per input and as cross-input mean

threshold_for_useful_signal: spec acceptance_threshold requires route_regret nonzero spread across the three Composer cards. Card 02 carries the largest predicted spread among the three (0.42 on input 1, 0.53 on input 2; mean 0.475); this card is the spread-carrier load-bearer.

predicted_dream_value: 0.0 / 0.0 / 0.0 (Composer correctly recommends the regime-fit model on each input)

predicted_best_comparator_value: comparator_2 single-feature heuristic predicted 0/0/0 on this specific card (because dynamic_ratio happens to be a sufficient discriminator for this 2-regime split). This is a coincidence of the chosen inputs, not a property of the heuristic; on a card with three regimes (e.g. card 03's many-view vs pair distinction layered on dynamic-vs-static), the heuristic fails. Comparator_3 collapses to 0.265 mean route_regret in the worst tiebreak.

expected_gap_direction: dream_better unconditionally vs comparator_1 / comparator_1' / comparator_3; tie vs comparator_2 on this specific card, dream_better in the broader 5-regime taxonomy (which is what the spec one_line_thesis is actually about per line 146)

decision_signal_meaning:

```text
This is the strongest card for the Composer spec's central thesis ("3R
needs a regime-typed route_regret axis, not a meta-model"). The
comparator_3 collapse here is the primary novelty signal: any heuristic
that flattens the regime axis cannot win cross-regime inputs. Composer's
job is precisely not to flatten that axis.

Card portfolio interpretation:
  - This card 02: regime-distinction proven; comparator_3 collapses;
    route_regret spread = 0.475 mean (the spread-carrier).
  - Card 01 (Fast3R vs Spann3R, single regime): CR-1 closing; small
    spread (0.09); does not on its own beat comparator_3.
  - Card 03 (Fast3R vs MASt3R-SfM, cost-asymmetric): cost-adjusted
    route_regret; another comparator_3 failure mode (different from
    this card's regime-distinction failure).

If this card's predicted spread collapses (e.g. if the regime_card
classifications are wrong and both inputs end up being classified as
the same regime), the spec's central differentiator weakens and the
fail_fast_threshold (Composer retires to support-layer) is closer to
firing.
```

## Cross-Spec Contract Usage (CR-6)

Recorded per Cross-Spec Signal Contract rule CR-6 (`paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` line 149).

- CR-1 (Critic A5 reroute_model requires Composer agreement on capability_match spread): not exercised in this card. Critic A5 reroute_model on these specific inputs would not fire (CASE-20260504-CRITIC-01 explicitly chose rerun_local_region not reroute_model on input 1; CASE-20260504-CRITIC-03 explicitly chose between rerun_local_region and open_anchor_budget on input 2 with capability_match for alternatives predicted_low). CR-1 closure on these jobs lives in CASE-20260504-CRITIC-02 + CASE-20260505-COMPOSER-01 cross-pair.
- CR-2 (Permanence suppress_static_write is binding on Memory): trivially honored (Composer reads dynamic_ratio from Permanence as input to regime classification; does not interact with the suppress_static_write binding).
- CR-3 (Memory drift signal does not gate Critic verification): not Composer-owned; trivially honored.
- CR-4 (Composer route_recommendation does not bind Critic on capability_match ties): honored. capability_match spreads on this card are large (0.42 and 0.53), well above any plausible epsilon_tie; CR-4's binding-prevention does not need to fire here. Recorded as honored, not exercised.
- CR-5 (All cross-spec signals carry producer evidence label): honored. Each capability_card value carries paper-proven on the relative-ordering axis and inferred on the absolute-scaling axis; each regime_card probability carries inferred; each capability_match weighted-dot-product result carries inferred.
- CR-6 (cycle 009 case cards record contract usage): satisfied by this section.

## Writing Value

related_work_section: composer

figure_or_taxonomy: regime-card x capability-card matrix table per spec line 217 (this card supplies the static_pair and dynamic_video rows of the matrix for both MASt3R and MonST3R columns) + per-input route_recommendation table showing two different recommendations for two different regimes. The clearest teacher-visible artifact is a 2x2 grid: rows = inputs, columns = candidate models, cell = capability_match, recommendation highlighted per row.

novelty_claim_supported:

```text
"3R needs a regime-typed route_regret axis, not a meta-model" (spec
one_line_thesis line 146). This card carries the central thesis:
regime-typed routing wins where regime-collapsed routing cannot. The
comparator_3 collapse is the cleanest paper-grade demonstration of the
thesis on cycle 009 paper-derived data.
```

## Risk And Boundaries

fail_fast_condition:

```text
If the regime classifications collapse (both inputs classified as the
same regime, or both regimes assigned similar probabilities for both
inputs), the cross-regime spread disappears and the central thesis is
not demonstrated. Per spec fail_fast_threshold (Composer retires to
support-layer), this card carrying a degenerate spread is the most
informative single-card failure mode.
```

reproduction_required: no

training_required: no

frontend_change_required: no

approval_required: no

caveats:

```text
- Capability_card axis values are paper-derived on relative ordering
  and inferred on absolute scaling. The 0-1 axis is a Dream-internal
  normalization; each source paper uses different scoring conventions
  that do not directly compose. The relative ordering (MASt3R higher
  on static_pair, MonST3R higher on dynamic_video) is paper-proven;
  the magnitude of the gap is inferred.
- Regime_card probabilities are inferred from input-pair structure and
  spec line 363 (MonST3R 48-frame + 96 dynamic masks). The artifact is
  not opened per D2'; misclassification in either direction would
  collapse the predicted spread.
- The comparator_3 collapse argument depends on the assumption that
  benchmark-matrix-average is a credible comparator. It is the
  benchmark-style comparator named in spec line 110, and any "best on
  average" routing heuristic is structurally subject to the same
  collapse. The argument is not tied to a specific published comparator.
- Comparator_2 single-feature heuristic happens to win on this card
  because dynamic_ratio is a sufficient discriminator for the
  static-vs-dynamic distinction. This coincidence is acknowledged
  explicitly; card 03 carries the broader-regime case where single-
  feature heuristics fail.
```

## Next Action

next_action: add_comparator

linked_next_artifact: `cases/CASE-20260505-COMPOSER-03.md` (Fast3R vs MASt3R-SfM; many-view vs pair regime AND cost-asymmetric route_regret; the third comparator_3-collapse mode plus the cost-axis carrier)
