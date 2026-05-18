# CASE-20260504-PERMANENCE-03

Last updated: 2026-05-05 (cycle 011 S3 G4 closure: CR-2 consumer-side forward-reference null documented under v2.1 protocol; G4 closed-by-documentation, not by new Memory card; cycle 010 closeout content unchanged)

## Identity

case_id: CASE-20260504-PERMANENCE-03

spec_id: SPEC-20260503-003 (Dynamic Object Permanence)

cycle: 010

evidence_label: paper-proven (for the qualitative existence of public dynamic-3R datasets with labeled object identity, e.g. tracking-benchmark-derived clips with frame-level identity labels referenced in the broader 3D vision literature); inferred (for the specific synthetic clip used here, the per-frame identity label assignment, and the labeling-effort estimate; this card explicitly does NOT pin to a specific public dataset because the goal is to validate the labeling protocol, not the dataset choice).

paper_only: yes (no inference; no real annotation in this draft; cycle 010 D2' default).

contract_version: **v2** (Permanence does not consume cost-axis signals; CR-4 trivially honored).

## Input Artifact

job_id: synthetic / public clip placeholder; concrete dataset deferred to cycle 011 if cycle 010 audit closes the labeling protocol; the placeholder reservation is `synthetic_dynamic_clip_001`.

upstream_model: any 3R model that produces per-frame depth + dynamic mask on a short clip (e.g. MonST3R applied to a labeled tracking-benchmark clip; specific model pinned at cycle 011 if the labeling protocol passes audit).

clip structure used by Permanence:

```text
Short clip (~8-16 frames) containing:
  - 1-2 known moving objects with unique identity throughout the clip
  - the rest of the scene either static or with motion that is not a
    distinct object (e.g. global flow / camera shake)
The clip's identity ground truth comes from the dataset's existing
labels, not from re-annotation. The Dream prediction is: for each
labeled moving object, Dream Permanence assigns a single object_track_
set entry across the object's frame range, and that entry's
identity_consistency score (per spec acceptance line 250) computes from
the dataset labels within the 120-minute budget.
```

input regime classification:

```text
regime_card(input) = {
  static_pair       : 0.00
  many_view         : 0.05 (~8-16 frames; small)
  streaming         : 0.10
  dynamic_video     : 0.85 (the headline regime)
  static_collection : 0.00
}
all probabilities inferred; sum = 1.00
```

## Why This Card Exists

PERMANENCE-01 makes positive claims about identity_consistency on the MonST3R 48-frame KYKT job (spec line 249-251 acceptance). However, the MonST3R job does NOT come with frame-level identity ground truth; computing identity_consistency on it requires manual annotation under the 120-minute budget per cycle 008 D4. The spec records (line 261-263) that this annotation cost is the headline fail_fast condition (b).

This card is the **labeling-protocol validation**: use a public clip with known identity labels to verify that Dream Permanence's predicted object_track_set entries align with ground truth in a way that is computable within budget. If yes, the protocol transfers to the MonST3R job. If no, the protocol needs revision OR the spec needs to fall back to the paper-relevant negative framing (spec lines 272-280).

## Evidence Signals

active_signals consumed (same vector as PERMANENCE-01; values inferred per the placeholder clip):

```text
dynamic_ratio(r, t)              non-trivial across the 8-16 frames; the
                                 dynamic regions are concentrated around
                                 the labeled objects
optical_flow_conflict(r, t)      well-defined per frame
object_track_stability(o, t)     this is the headline signal this card
                                 validates
pose_novelty(t)                  read; small (short clip)
view_overlap(t)                  read; high (short clip)
```

cross-spec read signals: minimal; no cycle 010 cross-pair partner on this clip.

published outward:

```text
object_track_set(t): predicted to contain 1-2 entries matching the
                     labeled moving objects; identity_break_score per
                     object computable within the labeling budget
suppress_static_write(r): fires on the dynamic-region union; specific
                          firings inferred per the placeholder clip
identity_consistency: computable within ~60-90 minutes labeling effort
                      (inferred; well under the 120-minute spec ceiling)
```

## Comparator Policies

| Policy | A6 behavior on labeled dynamic clip | Predicted identity_consistency vs GEM-3R |
| --- | --- | --- |
| comparator_1 no-policy | writes everything; mints nothing | undefined (no track set) |
| comparator_2 mask-threshold-only | suppresses by mask; mints nothing | undefined |
| comparator_4 mask-threshold + naive-tracking | suppresses by mask; mints object IDs by frame-to-frame mask overlap (no flow / position consistency check) | identity_consistency partial (track IDs flicker when masks fragment); fails on object_track_stability score |
| dream_policy GEM-3R | A6 mix: suppress_static_write fires on dynamic region union; mint_object_id fires once per labeled object at first dynamic-mask appearance; update_object_track maintains across the object's lifetime by position + flow consistency (per spec line 219); defer fires on borderline frames (object enters / exits) | identity_consistency for each labeled object computable from dataset labels; predicted to clear the 8-frame minimum from spec line 249-250 within a 60-90 minute annotation budget |

## Predicted Proxy Outcome

primary_metric: identity_consistency (per spec line 249-250)

annotation_budget_metric: human-effort minutes to compute identity_consistency from the dataset labels (per cycle 008 D4 = 120 minute ceiling)

predicted_dream_value:

- identity_consistency on object 1 (primary labeled object): >= 0.8 across its labeled frame range (inferred); annotation effort ~30-45 minutes
- identity_consistency on object 2 (if present): >= 0.7 across its labeled frame range (inferred); annotation effort ~25-40 minutes
- total annotation effort: ~60-90 minutes (well under the 120 minute ceiling)
- mint_object_id calls: matches the number of labeled objects (1-2)

predicted_best_comparator_value: comparator_4 mask-threshold + naive-tracking is the only comparator with track output; identity_consistency partial (~0.5-0.6 inferred); track flickering produces lower scores than GEM-3R's flow-consistency-aware mint policy.

expected_gap_direction: dream_better than comparator_4 directionally; comparators 1 + 2 are out of scope for the identity axis (no track output to score).

decision_signal_meaning:

```text
The decisive signal is a binary: identity_consistency on >= 1 labeled
moving object computes within the 120-minute budget AND scores above
some threshold (inferred ~0.7+) -- success; or the labeling effort
exceeds budget OR the identity_consistency score is below threshold
-- fail_fast for spec lines 261-269.
The threshold is inferred at this draft; cycle 010 closeout S6 audit
is when the threshold gets pinned.
```

## Cross-Spec Contract Usage (CR-6)

Recorded per Cross-Spec Signal Contract rule CR-6 v2.

- CR-1 / CR-3 / CR-4: trivial.
- CR-2: this card publishes suppress_static_write on the dynamic region union. No Memory cross-pair partner on this synthetic clip in cycle 010 (Memory cards are on MonST3R / Spann3R / MASt3R real KYKT jobs). CR-2 is structurally present from the producer side; the consumer side is forward-referenced to a hypothetical future Memory card on the same clip.
  - **Forward-reference null protocol (per v2.1, formalized in cycle 011)**: this card uses the protocol with the following declared fields:
    - fallback path: in absence of a Memory consumer card on this synthetic clip, no Memory state writes are issued for the clip; the synthetic clip is identity-validation only and does not exercise long-context drift, so the null fallback is benign (Memory's `latent_drift_proxy(t)` is not consumed downstream because no Memory card reads from the synthetic clip; no anchor write happens that would need suppression).
    - expected close-out cycle: cycle 012 or later, only if a Memory card is later drafted on a synthetic identity-validation clip. If no such card is drafted, the consumer side is retired with the stated reason "synthetic identity-validation clip is producer-only by design; CR-2 consumer is N/A on this regime" and the audit closes G4 by retirement, not by closure.
    - producer card id: this card (`cases/CASE-20260504-PERMANENCE-03.md`).
  - This documentation closes cycle-010 gap G4 ("CR-2 partial on synthetic identity-validation clip") under cycle-011 DEC-20260505-001 (2). Status: **closed-by-documentation under v2.1 protocol**, not by drafting a new Memory card. The choice is recorded in `cycles/CYCLE-20260505-002.md` S3.
- CR-5: honored. Per-object identity scores carry inferred evidence_labels; dataset identity labels carry paper-proven (assumed; the "public clip with labels" framing is paper-derived).
- CR-6: satisfied.

## Writing Value

related_work_section: permanence (identity-validation appendix; gates positive identity claims in PERMANENCE-01 + main paper text)

figure_or_taxonomy: side-by-side panel showing dataset ground-truth labels on the left and Dream object_track_set predictions on the right, frame-by-frame; identity_break_score timeline below.

novelty_claim_supported:

```text
"Dream Permanence's identity_consistency is computable within the
annotation budget on labeled dynamic clips" -- this is the gating
condition for any positive identity claim downstream. If this card
fails (annotation budget exceeded or identity_consistency score below
threshold), the spec's identity-related claims fall back to the paper-
relevant negative framing per spec lines 272-280; that negative is
itself paper-relevant (signal-vector permanence is insufficient for
identity; learned head needed). Either outcome is paper-relevant.
```

## Risk And Boundaries

fail_fast_condition:

```text
This card fails if either:
  (a) Annotation effort to compute identity_consistency from existing
      dataset labels exceeds 120 minutes per cycle 008 D4 (this is the
      spec's stated fail_fast condition (b) for Permanence)
  (b) Predicted identity_consistency score on the primary object is
      below the inferred threshold (~0.7); this means signal-vector
      permanence cannot hold identity even on labeled inputs
```

scope_boundaries:

```text
This card does NOT:
  - pin to a specific public dataset; the placeholder reservation
    `synthetic_dynamic_clip_001` lets cycle 011 (or later) bind the
    actual clip when the dataset choice is made
  - run the annotation effort in this draft; the predicted 60-90
    minute estimate is inferred, not measured
  - claim identity_consistency on the MonST3R 48-frame job; that
    transfer is the cycle 010 closeout S6 audit's job
  - bind D3 demo target choice; identity_consistency labeling closure
    is one input, not the deciding factor
```

## Next Action

immediate next: cycle 010 S6 contract usage audit (`cycles/CYCLE-20260504-002.md` "Contract Usage Audit (S6) under v2" section) verifies CR-2 cross-pair (PERMANENCE-01 + MEMORY-01); CR-3 forward-reference closure (CRITIC-03 forward-reference null + MEMORY-01 published latent_drift_proxy); v2 spillover (none expected); G1 / G2 / G3 status under cycle 010 closure.

deferred to cycle 010 closeout S8: this card's outcome (identity_consistency labelable Y/N) feeds the D3 first-demo-target re-surfacing decision.
