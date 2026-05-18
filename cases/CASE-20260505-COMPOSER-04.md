# CASE-20260505-COMPOSER-04 KYKT-metadata-derived capability card grounded to real KYKT job inventory

Last updated: 2026-05-05 (cycle 012 S2; first KYKT-metadata-derived Composer L2 case card; advances G2 toward inferred-with-real-inventory-anchor; does NOT close G2)

This card is the first non-paper-derived Composer capability card. It anchors the Composer's `capability_card` schema and `capability_match` predictions to actual KYKT job inventory (4 known jobs in this workspace). Evidence label is **KYKT-metadata-derived** — one rung above paper-derived (it is grounded in real-world job inventory, not just paper claims), one rung below measured / demo-observed (it does NOT measure route_regret on actual model outputs because model outputs are not directly readable from disk in this workspace; only KYKT job metadata is).

## Identity

case_card_id: CASE-20260505-COMPOSER-04

linked_spec: `specs/SPEC-20260504-001-3r-composer.md`

linked_finalist: 3R Composer

date: 2026-05-05

cycle_of_origin: cycle 012 (`cycles/CYCLE-20260505-003.md`)

linked_research_units: RU-002 (Composer routing), RU-011 (capability_match)

linked_sources: MASt3R, MonST3R, Fast3R, Spann3R (capability anchors); see `registry/source_registry.md`

## Input Artifact

input_id: kykt_job_inventory_2026Q2

input_type: KYKT job metadata aggregate

evidence_label: KYKT-metadata-derived

input_description:

```text
The four KYKT job ids referenced across cycle 009 and cycle 010 case
cards are the input for this card:

  20260420-222928   MonST3R 48-frame dynamic-scene job
  20260420-222729   MASt3R static-pair job
  20260425-113002   Fast3R job
  20260425-113227   Spann3R transforms-timeline job

This card does NOT read the model output (pointmaps, confidence maps,
latency traces) from disk because those outputs are not directly
readable in this workspace. The card reads job metadata only:

  - model name (which model class produced the job)
  - regime classification (static-pair / dynamic-scene / streaming /
    long-context)
  - completion status (the four jobs all completed; KYKT issued no
    failure flag on any of them)
  - per-job KYKT runner contract surfaces (already cited verbatim in
    cycle-009 / cycle-010 case cards; treated as in-context anchors)

The capability_card values below are KYKT-metadata-derived: the regime
labels come from KYKT's runner classification (which is itself a paper-
derived + KYKT-engineered combination); the cost_normalized values are
inferred from public model size + iterations-to-completion conventions,
NOT measured from KYKT runner logs.
```

## Evidence Signals

regime_coverage_per_model:

```text
MASt3R   : static-pair  (paper-proven model specialty;
                         KYKT-metadata-confirmed via job 20260420-222729)
MonST3R  : dynamic-scene (paper-proven; KYKT-metadata-confirmed via
                          job 20260420-222928 = 48-frame dynamic)
Fast3R   : streaming / multi-frame (paper-proven; KYKT-metadata-
                                    confirmed via job 20260425-113002)
Spann3R  : long-context with internal memory (paper-proven; KYKT-
                                              metadata-confirmed via job
                                              20260425-113227 transforms
                                              timeline output type)
```

capability_card_per_model (KYKT-metadata-derived; v2 schema with cost_normalized axis):

```text
MASt3R   : capability_match[static_pair] = predicted_high (0.85 inferred)
           capability_match[dynamic]     = predicted_low  (0.20 inferred)
           capability_match[streaming]   = predicted_low  (0.25 inferred)
           cost_normalized               = 0.35 (small model; quick on
                                                  static pairs;
                                                  inferred from public
                                                  model size)

MonST3R  : capability_match[static_pair] = predicted_medium (0.60 inferred;
                                                              works but
                                                              not specialty)
           capability_match[dynamic]     = predicted_high   (0.85 inferred;
                                                              native specialty)
           capability_match[streaming]   = predicted_medium (0.55 inferred;
                                                              48-frame
                                                              completion
                                                              KYKT-confirmed)
           cost_normalized               = 0.65 (heavier than MASt3R;
                                                  inferred from iteration
                                                  count and 48-frame
                                                  completion)

Fast3R   : capability_match[static_pair] = predicted_medium (0.60 inferred)
           capability_match[dynamic]     = predicted_low    (0.30 inferred)
           capability_match[streaming]   = predicted_high   (0.85 inferred;
                                                              native specialty)
           cost_normalized               = 0.40 (designed for speed;
                                                  inferred)

Spann3R  : capability_match[static_pair] = predicted_medium (0.55 inferred)
           capability_match[dynamic]     = predicted_low    (0.30 inferred)
           capability_match[streaming]   = predicted_medium (0.65 inferred)
           capability_match[long_context]= predicted_high   (0.80 inferred;
                                                              internal memory
                                                              specialty;
                                                              transforms-
                                                              timeline output
                                                              KYKT-confirmed)
           cost_normalized               = 0.70 (heaviest of the four;
                                                  internal memory
                                                  bookkeeping; inferred)
```

evidence_label_propagation: every numeric in the table above carries `KYKT-metadata-derived` (regime label) + `inferred` (numeric value). Per CR-5, downstream readers of this card see both labels.

## Comparator Policies

| comparator | policy | regime coverage claim | KYKT-metadata coverage |
|---|---|---|---|
| comparator_1: paper-claim only (cycle-009 COMPOSER-01..03 baseline) | use paper-claimed regime fit only | broad but unanchored | none — paper-derived only |
| comparator_2: KYKT-metadata anchored (this card) | regime labels from KYKT runner; numerics inferred from public model size + completion patterns | grounded to 4 jobs in this workspace | 4 of 4 KYKT jobs covered |
| comparator_3: measured route_regret (gated; future cycle) | requires reading actual model output from KYKT runner logs | not yet attempted | requires user-approved L3 OR KYKT-runner-log access |
| comparator_4: hand-tuned capability_card per regime | single-mechanism comparator; loses Composer's multi-model ecology benefit | narrow | trivially anchored but defeats purpose |

route_regret prediction (cost-adjusted, v2):

```text
On the dynamic regime: routing to MonST3R = predicted_optimal (regret
near 0). Routing to MASt3R / Fast3R / Spann3R = predicted_nonzero
regret. Sign: dream_better with KYKT-metadata-anchored capability_card
than with paper-claim-only. Magnitude: inferred (cannot measure
without model output access).

On the streaming regime: routing to Fast3R = predicted_optimal. Routing
to Spann3R is predicted_close-second when long-context is also a
factor; CR-4 cost-adjusted tie arbitration is the canonical resolver
(Fast3R wins on cost_normalized = 0.40 vs Spann3R = 0.70 if
capability_match is within tau_spread = 0.05).
```

## Predicted Proxy Outcome

P5 route_regret (cost-adjusted under v2):

```text
expected_value (cycle-012 KYKT-metadata-anchored):
  dynamic regime, MonST3R chosen        -> route_regret near 0
  dynamic regime, MASt3R chosen         -> route_regret = inferred high
  static_pair regime, MASt3R chosen      -> route_regret near 0
  static_pair regime, Spann3R chosen     -> route_regret = inferred medium
                                             (cost-penalized vs MASt3R)
  streaming regime, Fast3R chosen        -> route_regret near 0
  streaming regime, Fast3R vs Spann3R tie -> CR-4 cost-adjusted picks
                                              Fast3R; route_regret near 0
                                              under v2 cost-typed framing

expected_gap_direction: dream_better against comparator_1 (paper-claim
only baseline) by tightening the regime labels to KYKT job metadata;
tie or dream_better against comparator_2 = self (this card IS
comparator_2); ambiguous against comparator_3 = measured (not yet
attempted; gated).
```

P_capability_match: covers all 4 KYKT jobs; predicted high coverage on the regime each model was designed for; predicted low coverage on regimes outside specialty.

G2 status update:

```text
Before cycle 012: G2 (tau_spread = 0.05 in CR-1 closure remains
inferred). status = inferred.

After cycle 012 (this card): tau_spread = 0.05 still inferred (this card
does not measure route_regret), but the capability_match values it feeds
into CR-1 are now KYKT-metadata-derived rather than paper-derived. This
upgrades the *anchoring* of CR-1 closure from paper-derived to KYKT-
metadata-derived, while leaving tau_spread itself inferred.

status after cycle 012: inferred-with-real-inventory-anchor.
G2 NOT closed. Closure still requires measured route_regret; gated on
L3 prototype OR KYKT runner log access.
```

## Cross-Spec Contract Usage (CR-6)

Recorded per Cross-Spec Signal Contract rule CR-6 v2.1.

- CR-1 (Critic A5 reroute_model requires Composer agreement on capability_match spread): **exercised in this card** as the producer side. Critic CRITIC-02 forward-referenced this kind of capability_card collection; this card now provides a KYKT-metadata-derived version. Critic-side fallback path documented in CRITIC-02 line 210 still applies (pre-cycle-012 Critic readers used paper-derived spread; cycle-012-or-later readers may use KYKT-metadata-derived spread).
- CR-2: trivial; this card does not produce or consume suppress_static_write.
- CR-3: trivial; this card does not produce or consume latent_drift_proxy.
- CR-4 (cost-adjusted ties as canonical arbitration trigger): **exercised in this card** as the canonical example. Fast3R vs Spann3R tie on streaming regime (capability_match within tau_spread = 0.05 inferred) -> CR-4 picks Fast3R on cost_normalized = 0.40 vs 0.70.
- CR-5 (evidence-label propagation): honored. Every numeric in the capability_card_per_model table carries `KYKT-metadata-derived` (regime label) + `inferred` (numeric value).
- CR-6: satisfied; this entry IS the recording.

v2.1 forward-reference null protocol: not exercised on this card (no signal forward-referenced; all signals self-contained).

## Writing Value

related_work_section: composer (KYKT-metadata anchoring; bridges paper-claimed regime fit and measured route_regret without claiming the latter)

figure_or_taxonomy: 4-row x 4-column capability_match table (rows = MASt3R / MonST3R / Fast3R / Spann3R; columns = static_pair / dynamic / streaming / long_context); cost_normalized as a fifth column; CR-4 arrow from streaming-tie row to Fast3R selection.

central_argument:

```text
A capability_card grounded to actual KYKT job inventory + KYKT runner
regime classifications is not the same as a capability_card derived
from paper claims. The grounding tightens regime labels (KYKT runner
has already classified the 4 jobs into static / dynamic / streaming /
long-context types) but does NOT measure route_regret on actual model
output. The card is therefore one rung above paper-derived (anchored
to real inventory) and one rung below demo-observed (no measurement).
This is the maximum non-gated upgrade available to Composer in this
workspace.
```

## Risk And Boundaries

risks:

- **Confusing KYKT-metadata-derived with measured**: the card is NOT measured. Numerics are inferred. This card does NOT close G2; it advances G2 toward `inferred-with-real-inventory-anchor`.
- **KYKT runner regime classification could itself be wrong**: KYKT runner inherits from paper conventions; if the paper conventions are wrong on a regime boundary (e.g. "is 48 frames streaming or long-context?"), this card inherits that wrongness. Recorded as gap, not closed.
- **Numerics drift if KYKT job inventory grows**: 4 jobs is small. A future Composer card on a larger KYKT inventory may need different numerics. The schema (capability_match per regime + cost_normalized) is stable; the numbers are not.

boundaries:

- This card does not reroute any actual model. Composer's A5 routing facet is described, not exercised on a real input.
- This card does not gate G2 closure. G2 still requires measured route_regret via L3 or KYKT runner log access.
- This card does not authorize Composer demo target promotion. Composer storyboard `STORY-20260505-004-composer.md` is `draft` only; D3 first demo target remains Critic per cycle 011 DEC-001.
- This card does not surface a v2.2 contract candidate. The KYKT-metadata-derived numerics fit cleanly into the existing v2 schema (capability_match + cost_normalized); no new sub-axis needed.

## Next Action

immediate next: cycle 012 S6 contract usage audit (`cycles/CYCLE-20260505-003.md` "Contract Usage Audit (S6) under v2.1") records this card as CR-1 producer side for any future Critic CR-1 reads from cycle 012 onward; G2 status update from `inferred` to `inferred-with-real-inventory-anchor`; v2.2 candidate enumeration (none from this card).

deferred next (gated): measured route_regret card requiring L3 prototype OR KYKT runner log access. Both gated on user approval.
