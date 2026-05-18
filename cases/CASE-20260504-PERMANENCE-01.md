# CASE-20260504-PERMANENCE-01

Last updated: 2026-05-04 (cycle 010 S3; first Permanence L2 case card; cross-pair partner CASE-20260504-MEMORY-01 drafted as S2 in same cycle under v2 contract; producer side of CR-2 binding consumed by MEMORY-01)

## Identity

case_id: CASE-20260504-PERMANENCE-01

spec_id: SPEC-20260503-003 (Dynamic Object Permanence)

cycle: 010

evidence_label: paper-proven (for MonST3R upstream artifact: 48 frames + 96 dynamic masks + 96 per-frame confidence + scene.glb + pred_traj.txt as documented in the MonST3R paper; the existence of per-frame dynamic masks is the foundational paper-proven claim this card builds on); inferred (for every Dream Permanence A6 sub-action attachment per region, every threshold value `theta_pollution`, and every per-region pollution_score magnitude in this card; identity_consistency on the moving objects is inferred until cycle 010 case-card annotation lands per spec acceptance line 249-251).

evidence_label_propagation: per cross-spec contract CR-5 (`paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v2), each cross-spec read carries the producer's evidence_label. This card consumes `pose_novelty(t)` and `view_overlap(t)` from Memory's published evidence vector (CASE-20260504-MEMORY-01 cross-pair); both arrive carrying Memory's evidence_label (paper-proven on pred_traj.txt-derived camera deltas; inferred on per-window magnitudes).

paper_only: yes (cycle 010 D2' default carried forward from cycle 009; no KYKT-job-derived per-region segmentation re-execution is performed).

contract_version: **v2** (cycle 010 case cards are v2-default per `decisions/DEC-20260504-005-cycle-010-launch.md`; PERMANENCE-01 does not consume Composer's `cost_adjusted_match` in v2 because Permanence does not own A5; CR-4 is non-Permanence-owned and trivially honored).

## Input Artifact

job_id: 20260420-222928

upstream_model: MonST3R

upstream_outputs available (per cycle 009 Resource Inventory; SAME job as CASE-20260504-MEMORY-01 to enable in-cycle CR-2 cross-pair):

- 48 frames (input video sequence; dynamic content per MonST3R)
- 96 dynamic masks (per-frame; the foundational signal Permanence builds on)
- 96 per-frame confidence arrays (per-frame; cross-checked against dynamic masks)
- scene.glb (consolidated 4D-aware scene asset)
- pred_traj.txt (predicted camera trajectory across the 48 frames)

region partition used by Permanence:

```text
Permanence operates per-region per-frame. Default region partition = 8x8
grid over each frame, giving 64 regions per frame x 48 frames = 3072
region-frames. Per-region dynamic_ratio is derivable from the MonST3R
dynamic mask intersected with each grid cell. The 8x8 grid is inferred
(not paper-proven); cycle 010 closeout audit may surface a v3 candidate
if a finer / coarser partition shifts the suppress / admit decisions.
```

object track granularity:

```text
Per-frame moving regions cluster into object tracks via position + flow
consistency. Predicted per-track lifetimes on this 48-frame run:
  Track O1: ~frames 8-32  (~25 frame lifetime; primary moving object)
  Track O2: ~frames 16-44 (~29 frame lifetime; secondary moving object;
                           may share frames with O1 in 16-32 overlap)
  Track O3: ~frames 4-12  (~9 frame lifetime; brief)
  noise_track: aggregated low-confidence dynamic flickers across all 48
               frames (capped per spec line 218 to avoid mint_rate
               overflow)
All track ranges + counts are inferred per dynamic-mask coverage shape;
the existence of multiple distinct moving objects on this job is paper-
derivable from MonST3R's published demos.
```

## Evidence Signals

active_signals consumed by Permanence in this card (per `specs/SPEC-20260503-003-dynamic-object-permanence.md` lines 186-192):

```text
dynamic_ratio(r, t)              Permanence-OWNED publication; derived from
                                 MonST3R 96 dynamic masks intersected with the
                                 8x8 grid per frame; published outward to
                                 Memory (consumed by MEMORY-01 cross-pair) and
                                 to Composer (regime classification input)
optical_flow_conflict(r, t)      derived from inter-frame mask boundary
                                 inconsistency; Permanence-OWNED
object_track_stability(o, t)     per-object identity-confidence trace;
                                 Permanence-OWNED publication
pose_novelty(t)                  read from MEMORY-01 (cross-spec read; needed
                                 to disambiguate camera motion from object
                                 motion); paper-proven per-window shape from
                                 pred_traj.txt
view_overlap(t)                  read from MEMORY-01 (cross-spec read);
                                 inferred per-window magnitudes
```

cross-spec read signals (read-only by Permanence; producer evidence_label propagates per CR-5):

```text
pose_novelty(t)                  from CASE-20260504-MEMORY-01 (paper-proven
                                 qualitative shape; inferred magnitudes)
view_overlap(t)                  from CASE-20260504-MEMORY-01 (inferred)
pointmap_conflict, reprojection_residual:
                                 cycle 009 cards (CRITIC-01..03) published
                                 these on related but not identical job
                                 windows; Permanence reads as informational
                                 only, not gating any A6 trigger this card
```

derived_signals computed by Permanence:

```text
pollution_score(r, t)     = w_d * dynamic_ratio(r, t) + w_f * optical_flow_conflict(r, t)
                            (weights w_d, w_f inferred; default w_d = 0.7, w_f = 0.3
                            per spec line 209)
identity_break_score(o, t) = w_g * frame_gap(o, t) + w_p * position_jump(o, t)
                              + w_c * confidence_drop(o, t)
                            (all weights inferred)
```

published outward (consumed by other specs):

```text
dynamic_ratio(r, t)         48 frames x 64 regions = 3072 values; CR-2
                            consumer is MEMORY-01 (which derives skip_update
                            decisions from high-dynamic_ratio frames)
suppress_static_write(r)    fires per region when pollution_score(r, t) >
                            theta_pollution; CR-2 binding on Memory's A2;
                            MEMORY-01 honors via A2 = ignore on suppressed
                            regions
admit_static_write(r)       fires per region when pollution_score(r, t) low
                            AND object_track_stability(r, t) high
pollution_log(t)            append-only trace of per-frame
                            suppress / admit / defer decisions
object_track_set(t)         {O1, O2, O3, noise_track} per frame; lifetimes
                            given above
```

## Comparator Policies

| Policy | A6 behavior | Predicted P4 dynamic_pollution / static_preservation / identity_consistency vs GEM-3R |
| --- | --- | --- |
| comparator_1 no-policy (write everything) | writes every region every frame regardless of dynamic mask; never mints object IDs; never tracks identity | P4 dynamic_pollution highest (every dynamic region polluted into static map); static_preservation also highest (no suppression rejects valid static); identity_consistency undefined (no tracks) — clearly P4 fails on the headline pollution axis |
| comparator_2 mask-threshold-only | suppress writes when dynamic mask coverage > 0.5; admit otherwise; no object tracking | P4 dynamic_pollution moderate (threshold catches obvious dynamics; misses partial-coverage borderlines); static_preservation slightly reduced (some valid static suppressed); identity_consistency undefined (no tracks) — improves on comparator_1 on P4 but does not address identity |
| comparator_3 confidence-only | suppress writes when confidence below threshold; ignore dynamic mask entirely | P4 dynamic_pollution moderate (high-confidence dynamic regions still polluted); static_preservation slightly reduced (low-confidence static gets suppressed); identity_consistency undefined — orthogonal failure mode to comparator_2 |
| dream_policy GEM-3R (this card's prediction) | A6 mix per region: suppress_static_write fires on the high-pollution regions in frames 16-32 (where O1 + O2 tracks overlap with high-dynamic_ratio); admit_static_write fires on the static background regions all 48 frames; mint_object_id fires at frames 4 (O3), 8 (O1), 16 (O2); update_object_track maintains O1 across ~25 frames and O2 across ~29 frames (identity_consistency carrier); defer fires at borderline regions in frames 12-16 and 32-36 then resolves within dynamic_horizon | P4 dynamic_pollution(GEM-3R) <= dynamic_pollution(comparator_1) by a clear margin (acceptance directionally satisfied); static_preservation(GEM-3R) >= static_preservation(comparator_1) directionally; identity_consistency computable on O1 across ~25 frames and O2 across ~29 frames (both >= 8-frame minimum per spec line 250); CASE-20260504-PERMANENCE-02 (static control) confirms no hallucinated tracks on a static pair |

## Predicted Proxy Outcome

primary_metric: P4 dynamic_pollution

unit_of_measurement: number of region-frames written into the static_map that overlap a true dynamic mask region; lower is better; in [0, 3072] over the full 48-frame job (3072 = 64 regions x 48 frames upper bound).

threshold_for_useful_signal: per spec acceptance_threshold (lines 244-254), GEM-3R must satisfy:

```text
P4 dynamic_pollution(GEM-3R) <= dynamic_pollution(no-policy baseline)
                              [holds in this card by clear direction;
                              comparator_1 trivially loses]
P4 static_preservation(GEM-3R) >= static_preservation(no-policy)
                              [holds directionally; static regions are
                              admitted while dynamic regions are suppressed]
identity_consistency on MonST3R 48-frame job computable for >= 1 moving
object across >= 8 frames within 120 minutes annotation
                              [predicted satisfied: O1 ~25 frames + O2 ~29
                              frames; both >= 8; cycle 010 closeout
                              annotation effort is in scope per cycle 008 D4]
CASE-20260504-PERMANENCE-02 (static control) confirms no hallucinated tracks
                              [PERMANENCE-02 is cycle 010 S5; this card's
                              acceptance is conditional on PERMANENCE-02
                              showing zero mint_object_id calls on the MASt3R
                              static pair]
```

predicted_dream_value:

- P4 dynamic_pollution: ~150 region-frames out of ~3072 total (~5%, inferred); concentrated in unresolved-defer regions and partial-coverage borderlines
- P4 static_preservation: ~2400 region-frames out of ~3072 total (~78%, inferred); the rest are suppressed dynamic, deferred, or low-confidence regions
- identity_consistency on O1: predicted positive across ~25 frames (consistent track maintained)
- identity_consistency on O2: predicted positive across ~29 frames

predicted_best_comparator_value:

- comparator_1 no-policy: P4 dynamic_pollution ~1500 region-frames inferred (every dynamic region polluted); static_preservation ~3072 (nothing suppressed); identity undefined.
- comparator_2 mask-threshold-only: P4 dynamic_pollution ~600 inferred (threshold misses partial-coverage); static_preservation ~2700; identity undefined.
- comparator_3 confidence-only: P4 dynamic_pollution ~800 inferred (high-confidence dynamics not caught); static_preservation ~2500; identity undefined.

expected_gap_direction: dream_better on P4 dynamic_pollution vs all 3 comparators (large margin vs comparator_1; moderate margin vs 2 + 3); roughly tied on static_preservation vs comparator_1 (comparator_1 trivially wins by writing everything but that is the comparator that loses on the headline axis); identity_consistency is the only axis where GEM-3R is uniquely defined (comparators 1-3 have no identity head).

decision_signal_meaning:

```text
The decisive signal in this card is the conjunction of:
  (i)  P4 dynamic_pollution(GEM-3R) clearly below comparator_1 (no-policy)
  (ii) identity_consistency computable on at least one moving object
       across >= 8 frames
The card succeeds if (i) AND (ii) hold AND PERMANENCE-02 (cycle 010 S5)
confirms no hallucinated tracks on the static control. The card fails
if (i) holds but (ii) does not (signal-vector permanence is insufficient
for identity; spec lines 274-279 anticipate this and document it as a
paper-relevant negative). The card triggers spec fail_fast (lines 259-269)
if (i) fails OR if PERMANENCE-02 mints object tracks where none exist.
```

## Cross-Spec Contract Usage (CR-6)

Recorded per Cross-Spec Signal Contract rule CR-6 (`paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v2 line 149).

- CR-1 (Critic A5 reroute_model requires Composer agreement on capability_match spread): not Permanence-owned; trivially honored. Permanence does not invoke A5 reroute.
- CR-2 (Permanence suppress_static_write is binding on Memory): **producer-side closure of cycle 009 gap G1 in this card via in-cycle cross-pair**. Permanence publishes `suppress_static_write(r)` on the high-pollution regions across frames 16-32 (where pollution_score exceeds theta_pollution = 0.6 inferred). MEMORY-01 (cycle 010 S2 consumer side) honors the binding by emitting A2 = ignore on those candidate writes; MEMORY-01's `cross_spec_refusal` log is empty in the predicted run (Memory does not contest the suppression). G1 closed via this cross-pair: cycle 009 had zero CR-2 coverage; cycle 010 has the producer + consumer pair on a real KYKT job (paper-derived predictions, not measured). Cycle 010 S6 audit verifies the cross-pair is internally consistent.
- CR-3 (Memory drift signal does not gate Critic verification): not Permanence-owned; trivially honored. Permanence does not consume `latent_drift_proxy` in any A6 trigger.
- CR-4 (Composer route_recommendation does not bind Critic on capability_match ties): not Permanence-owned; trivially honored under v2 framing. Permanence does not consume Composer's `cost_adjusted_match` axis (or any Composer-owned signal beyond the regime card classification, which is a one-way read for Composer's downstream regime-conditional signals; not an A6 trigger).
- CR-5 (All cross-spec signals carry producer evidence label): honored. pose_novelty + view_overlap entries above carry Memory's evidence_label inline. Permanence's published dynamic_ratio / object_track_stability / suppress_static_write carry Permanence's own evidence_label (paper-proven on MonST3R-derived dynamic mask coverage shape; inferred on per-region threshold decisions and per-track lifetime magnitudes).
- CR-6 (cycle 010 case cards record contract usage under v2): satisfied by this section.

## Writing Value

related_work_section: permanence

figure_or_taxonomy: extends the spec's Teacher Demo Form — a per-frame pollution-timeline panel showing suppress / admit / defer decisions across the 48 frames + an object-track table showing O1, O2, O3, noise_track lifetimes. This card supplies the canonical timeline + table; CASE-20260504-PERMANENCE-02 supplies the static-control panel; CASE-20260504-PERMANENCE-03 supplies the synthetic identity-validation panel.

novelty_claim_supported:

```text
"Object permanence as a small dedicated controller, not as a learned
identity head" (spec one_line_thesis line 109: "permanence is a budgeted
controller over dynamic-static separation"). This card carries the
signal-vector argument: dynamic_ratio + optical_flow_conflict +
object_track_stability are sufficient to suppress dynamic pollution AND
maintain >= 1 moving-object identity across >= 8 frames without any
learned identity head. The card succeeds in the positive case if both
P4 and identity_consistency hold; succeeds in the paper-relevant negative
case (per spec lines 274-279) if P4 holds but identity_consistency cannot
be labeled within the 120-minute annotation budget — that negative
motivates a learned identity head, which is itself a publication-relevant
finding.
```

## Risk And Boundaries

fail_fast_condition:

```text
This card fails its differentiation test if any of:
  (a) Predicted P4 dynamic_pollution(GEM-3R) >= dynamic_pollution(no-
      policy baseline). This would mean Permanence's signal-vector
      controller does not even win on the headline axis vs writing
      everything; spec retires per spec lines 259-269.
  (b) Predicted identity_consistency cannot be labeled on at least one
      moving object across at least 8 frames within the 120-minute
      annotation budget per cycle 008 D4. Cycle 010 S5 + S6 audits
      whether O1 (~25 frames) + O2 (~29 frames) actually clear the
      labeling cost; if not, fall back to the paper-relevant-negative
      framing per spec lines 272-280.
  (c) CASE-20260504-PERMANENCE-02 (cycle 010 S5; static control) shows
      GEM-3R minting object tracks on the MASt3R static pair where no
      objects exist. This would be the "hallucinated motion" failure
      per spec line 266; spec retires.
  (d) The CR-2 cross-pair with CASE-20260504-MEMORY-01 fails to close
      in cycle 010 S6 audit (e.g. MEMORY-01's predicted A2 = ignore
      decisions do not match the regions Permanence-01 actually
      suppresses).
  (e) Any predicted value (P4 magnitudes, per-track lifetimes,
      pollution_score thresholds) reads as paper-proven rather than
      inferred in a future review pass; the card violates Discipline
      rule 5 Honesty Override if so.
```

scope_boundaries:

```text
This card predicts A6 sub-action attachment per region per frame AND
predicts the qualitative shape of pollution_score(r, t) and object_track_
set(t) across the 48-frame timeline. It does NOT:
  - run any inference (no MonST3R re-execution; no Permanence module
    code; paper-derived only)
  - claim measured magnitudes for any P4 number (all magnitudes inferred;
    relative-ordering vs the 3 comparators directionally inferred)
  - close identity_consistency labeling effort in this card alone;
    that closure is cycle 010 S6 audit + CASE-PERMANENCE-03 synthetic
    validation
  - bind Memory's CR-2 consumer-side decisions; MEMORY-01 is canonical
    for Memory-side prediction
  - mint object identities for downstream paper claims; identity
    publication is conditional on identity_consistency labeling closure
```

## Next Action

immediate next case card: `cases/CASE-20260504-MEMORY-02.md` (cycle 010 S4, secondary Memory card on Spann3R transforms timeline; cross-comparator anchor-retention card; not a CR-2 pair).

deferred to cycle 010 S5: `cases/CASE-20260504-PERMANENCE-02.md` (MASt3R static control; closes fail_fast condition (c) above) + `cases/CASE-20260504-PERMANENCE-03.md` (synthetic identity validation; closes fail_fast condition (b) above).

deferred to cycle 010 closeout S6: contract usage audit verifies CR-2 closure (this card's predicted suppress_static_write list matches MEMORY-01's predicted A2 = ignore list); v2 spillover check (none expected; Permanence does not consume cost-axis signals).

deferred to cycle 010 closeout S8: D3 first teacher demo target re-surfaced for user decision under full 4-finalist L2 coverage; Permanence's identity_consistency annotation closure is one input to the D3 decision (whether identity-tracking demo is usable).
