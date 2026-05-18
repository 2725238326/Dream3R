# CASE-20260504-PERMANENCE-02

Last updated: 2026-05-04 (cycle 010 S5 first half; secondary Permanence L2 case card; MASt3R static-pair control; closes CASE-20260504-PERMANENCE-01 fail_fast condition (c) "no hallucinated tracks on static input")

## Identity

case_id: CASE-20260504-PERMANENCE-02

spec_id: SPEC-20260503-003 (Dynamic Object Permanence)

cycle: 010

evidence_label: paper-proven (for the MASt3R upstream artifact: matches.png + pointcloud.ply on a static pair as documented in the MASt3R paper); inferred (for the predicted Dream Permanence behavior on a static-pair regime; the central prediction is that Dream Permanence's A6 actions reduce to "admit_static_write everywhere; mint_object_id zero times; suppress_static_write zero times", which is the correct boundary behavior).

paper_only: yes (cycle 010 D2' default).

contract_version: **v2** (Permanence does not consume cost-axis signals; CR-4 trivially honored).

## Input Artifact

job_id: 20260420-222729

upstream_model: MASt3R

upstream_outputs available:

- matches.png (per-pair feature matches visualization)
- pointcloud.ply (consolidated points; entirely static content)

region partition used by Permanence:

```text
8x8 grid per frame. With 2 frames, 128 region-frames total. The expected
ground truth on this static pair: every region-frame is static; zero
dynamic regions; zero moving objects. This is the explicit static-control
input the spec uses (line 233-234) to test the spec's fail_fast
condition (line 266) "case 02 (static control) shows GEM-3R minting
object tracks where none exist".
```

input regime classification:

```text
regime_card(input) = {
  static_pair       : 0.95 (clearly the headline regime)
  many_view         : 0.05
  streaming         : 0.00
  dynamic_video     : 0.00
  static_collection : 0.00
}
all probabilities inferred; sum = 1.00
```

## Why This Card Exists

PERMANENCE-01 makes positive claims about A6 sub-action attachment on the dynamic-video regime (mint_object_id, update_object_track, suppress_static_write). For those claims to be paper-relevant, Dream Permanence must NOT exhibit the same sub-actions on inputs where there is nothing dynamic — otherwise the policy is not actually reading dynamic_ratio + optical_flow_conflict, it is hallucinating motion.

This card is the **negative-control** that closes PERMANENCE-01's fail_fast condition (c).

## Evidence Signals

active_signals consumed (subset of PERMANENCE-01's vector; most evaluate trivially):

```text
dynamic_ratio(r, t)              trivially zero across all 128 region-frames
                                 (static pair; no dynamic mask content)
optical_flow_conflict(r, t)      trivially zero (no inter-frame motion)
object_track_stability(o, t)     undefined (no objects to track)
pose_novelty(t)                  paper-proven minimal (a static pair has
                                 small SE(3) delta from pair geometry; well-
                                 defined but small)
view_overlap(t)                  paper-proven high (static pair = high view
                                 overlap by definition)
```

cross-spec read signals: trivially honored.

published outward:

```text
dynamic_ratio: trivially zero across all region-frames
suppress_static_write: zero firings predicted
admit_static_write: fires across all 128 region-frames (or aggregated as
                    "admit static_pair entirely")
pollution_log: empty (no suppress / defer events)
object_track_set: empty
```

## Comparator Policies

| Policy | A6 behavior on static pair | Predicted P4 / identity_consistency vs GEM-3R |
| --- | --- | --- |
| comparator_1 no-policy | writes everything; mints nothing | P4 dynamic_pollution = 0 (no dynamic content); identity undefined |
| comparator_2 mask-threshold-only | suppresses by mask threshold; zero suppressions on static input; mints nothing | P4 = 0; identity undefined |
| comparator_3 confidence-only | suppresses by confidence; on a high-confidence static pair, suppresses zero; mints nothing | P4 = 0; identity undefined |
| dream_policy GEM-3R | A6 mix predicted: admit_static_write fires across all regions; suppress_static_write fires zero times; mint_object_id fires **zero times** (this is the canonical success criterion); update_object_track / defer not invoked | P4 = 0 (matches comparators); zero hallucinated tracks (passes spec fail_fast condition c) |

On a static-pair regime, all reasonable policies converge on P4 = 0. The non-degenerate axis is **mint_object_id rate**: GEM-3R must equal zero. If it doesn't, the spec's fail_fast triggers.

## Predicted Proxy Outcome

primary_metric: mint_object_id rate (Dream-specific success-criterion axis on this regime)

secondary_metric: P4 dynamic_pollution (degenerate; all policies = 0)

predicted_dream_value:

- mint_object_id rate: **0** (this is the success criterion)
- P4 dynamic_pollution: 0 region-frames out of 128
- P4 static_preservation: 128 / 128 region-frames (full admit)
- pollution_log size: 0 entries (no suppress / defer events)
- object_track_set size: 0 (no objects)

predicted_best_comparator_value: comparators 1 + 2 + 3 all converge to P4 = 0; none have identity-tracking heads to fail on the mint_object_id axis.

expected_gap_direction: dream_tied with all comparators on P4; dream_uniquely_correct on the mint_object_id axis (no comparator has the mint mechanism to potentially fail at).

decision_signal_meaning:

```text
The decisive signal is a binary: GEM-3R either mints zero object IDs
on this static input (success), or it mints non-zero (fail_fast trigger
per spec line 266; spec retires).
```

## Cross-Spec Contract Usage (CR-6)

Recorded per Cross-Spec Signal Contract rule CR-6 v2.

- CR-1 / CR-3 / CR-4: trivial (Permanence does not own these rules; on this static input they are non-events).
- CR-2: this card publishes zero suppress_static_write firings. CASE-20260504-MEMORY-03 (cycle 010 S4; same MASt3R job from Memory side) consumes zero suppressions and proceeds with A2 = write on the single pointcloud entry. CR-2 is trivially honored from both sides on this regime; the cross-pair is structurally present but has no contention.
- CR-5: honored. The published zero-firing trace carries `paper-proven` on the qualitative shape (no dynamics on a static pair) and `inferred` on the precise zero count (vs. some-small-numerical-noise threshold).
- CR-6: satisfied.

## Writing Value

related_work_section: permanence (negative-control appendix)

figure_or_taxonomy: minimal panel showing GEM-3R's mint_object_id rate across the three Permanence cards (PERMANENCE-01: 3 distinct tracks + noise on dynamic-video; PERMANENCE-02: 0 tracks on static-pair; PERMANENCE-03: matches synthetic ground truth identity count). The trend visualizes regime-correctness of the mint controller.

novelty_claim_supported:

```text
"Dream Permanence does NOT hallucinate motion on static inputs"
(corollary of the bounded-controller framing). This card is the
canonical negative-control evidence; failure of this card retires the
entire spec per fail_fast line 266.
```

## Risk And Boundaries

fail_fast_condition:

```text
This card fails if predicted Dream Permanence mints any object IDs on
the static-pair input. This is the spec-retirement trigger (lines 259-
269; specifically (c)).
```

scope_boundaries:

```text
This card does NOT:
  - establish positive identity-consistency claims (those live in
    PERMANENCE-01 + PERMANENCE-03)
  - extend PERMANENCE-01's mechanism arguments to additional regimes
  - close any cycle 009 contract gap (G1 closes via PERMANENCE-01
    cross-pair; G2 / G3 close via cycle 010 v2 audit)
```

## Next Action

immediate next case card: `cases/CASE-20260504-PERMANENCE-03.md` (cycle 010 S5 second half; synthetic / public dynamic example with labeled object identity; closes PERMANENCE-01 fail_fast condition (b) "identity_consistency labeling within 120-minute budget").

deferred to cycle 010 closeout S6: this card's contract audit row is single-line; mint_object_id rate = 0 is the canonical success criterion.
