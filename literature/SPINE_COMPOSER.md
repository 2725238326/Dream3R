# SPINE_COMPOSER: 3R Composer / Unified Model Ecology

Last updated: 2026-05-05 (cycle 013 refresh: VGGT SRC-2026-015 / MapAnything SRC-2026-009 / DUSt3R-MASt3R-VGGT MVS evaluation SRC-2026-013 / awesome-dust3r index SRC-2026-012 added to Advanced Reading; VGGT capability-card gap explicitly noted as cycle-014+ per-card candidate)

Linked spec: `specs/SPEC-20260504-001-3r-composer.md`

Linked finalist: 3R Composer / Unified Model Ecology

## One-Line Definition

A 3R routing controller that publishes regime cards (per-input regime classification) and capability cards (per-model regime fit), and exposes a `route_regret` falsification axis for the choice between models. Composer owns the routing facet of A5 only; the repair facet of A5 lives in Critic.

Important: per DEC-20260504-002, Composer is not the thesis spine, even if cycle 009 case-card data lands strongly. The capability-card axis is one of four borrowable components.

## Required Reading

These are the papers any Composer case-card author must read before adding a `capability_match` row.

### SRC-2024-001 DUSt3R (paper-proven)

What this paper actually claims: pose-free pointmap reconstruction; the founding paper of the family.

What people often misread it as: a single dominant model. DUSt3R was the start; the 2024-2026 follow-ups carved up the regime space. Composer's regime card argues that no single descendant covers all regimes.

### SRC-2024-002 MASt3R (paper-proven)

What this paper actually claims: 3D-grounded matching with sparse global alignment; matching head is the contribution.

What people often misread it as: replacing DUSt3R. MASt3R extends DUSt3R for matching-style regimes; the regime card encodes this.

### SRC-2025-001 Fast3R (paper-proven)

What this paper actually claims: many images in one forward pass; the regime is many-view.

What people often misread it as: a faster DUSt3R. Fast3R's contribution is the many-view regime fit, not raw speed; the capability card should reflect this.

### SRC-2024-011 Spann3R (paper-proven)

What this paper actually claims: spatial memory for global pointmap prediction; the regime is streaming-with-memory.

What people often misread it as: a memory paper that competes with Mem3R. Spann3R is a 3R model with memory; Mem3R is a hybrid memory architecture. Composer's regime card distinguishes them by regime fit, not memory size.

### Mixture-of-experts and routing literature (cross-domain analog; cited as inferred for 3R use)

What this literature claims: sample-conditioned routing among experts in language and vision.

What people often misread it as: a Composer comparator. MoE is sample-conditioned but not regime-typed; Composer's regime cards are 3R-specific (static_pair, many_view, dynamic_video, streaming, sparse_view). The borrow is the routing pattern, not the implementation.

## Advanced Reading

These are useful for second-round capability-card work.

### SRC-2024-009 MASt3R-SfM (paper-proven)

Matching + retrieval + global SfM. Useful for case-03 (many-view vs pair regime distinction). Capability card under "static_pair" is high; under "streaming" is low.

### SRC-2024-003 MonST3R (paper-proven)

Dynamic-video pointmap. Capability card under "dynamic_video" is high; under "static_pair" is low. Used in case-02 to demonstrate regime-driven routing flips.

### SRC-2025-002 CUT3R (paper-proven)

Persistent state continuous 3D perception. Capability card under "streaming" is high; static-pair is low.

### SRC-2026-001 STream3R (paper-proven)

Causal streaming geometry. Capability card under "streaming" is high; the difference vs CUT3R is causal vs persistent (see SPINE_MEMORY).

### SRC-2024-010 SLAM3R (paper-proven)

Sliding-window SLAM-shaped consumer of 3R outputs. Useful as a counter-example: SLAM3R is a *consumer* of 3R, not a 3R model family member. The capability card should not list SLAM3R as a peer to MASt3R; it operates downstream.

### SRC-2025-005 MV-DUSt3R+ (paper-proven)

Sparse-view multiview pose-free RGB reconstruction. Capability card under "sparse_view" is high; many-view is medium.

### SRC-2024-004 Splatt3R / SRC-2024-005 InstantSplat / SRC-2025-006 NoPoSplat (paper-proven)

Asset-path comparators. Their capability cards apply to the "asset_output" regime; Composer routes asset-path samples to them. They are not 3R-only models; they include Gaussian asset generation.

### SRC-2026-015 VGGT (paper-proven; comparator gap)

Feed-forward visual-geometry transformer (Meta open-source). What it actually claims: a direct feed-forward 3R model operating over multiple views without iterative optimization; published as code + paper under the DUSt3R / MASt3R / Fast3R family.

What people often misread it as: a one-shot replacement for the whole family. VGGT is strong in several regimes but its regime-conditioned capability profile is not yet encoded in Composer capability cards (CASE-20260505-COMPOSER-01..04 do NOT include a VGGT row). This is a cycle-014+ per-card revision candidate, not a contract revision. See `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v2 schema note in cycle 013 closeout.

### SRC-2026-009 MapAnything (paper-proven)

Universal feed-forward metric 3D reconstruction (v3 Jan 2026). What it actually claims: a feed-forward 3R that targets "regime-agnostic" coverage; references spatial-memory 3R as neighbor work.

What people often misread it as: a Composer-style router inside one model. MapAnything compresses regime-conditioning into a single model's input handling; Composer's argument is that such compression leaves a measurable `route_regret` signature. Useful comparator for L3 regime-label verification (EXP-20260505-004).

### SRC-2026-013 DUSt3R-MASt3R-VGGT MVS evaluation (paper-proven)

Empirical MVS evaluation across DUSt3R + MASt3R + VGGT on high-resolution + multi-camera videos. What it actually claims: per-model MVS results on a shared evaluation; useful as a published capability_card sanity check.

What people often misread it as: a Composer result. It is a comparison paper, not a routing paper; the per-model rows serve as ground truth for capability_card entries when L3 measurements are not yet available. Cycle-014+ per-card revision can pull from this directly.

### SRC-2026-012 awesome-dust3r curated index (code-curated)

Regularly-updated DUSt3R / MASt3R follow-up index (VGGT, MASt3R-SLAM, Light3R-SfM, pi3, MoGe-2, STream3R, Dens3R, ViPE, etc.). Meta-resource, not a paper.

Use pattern: pull individual rows when a specific capability-card gap appears. Do not cite the index itself as a Composer comparator; cite the underlying paper, and log an evidence label per source row on the paper's registry entry.

## Skip With Reason

- robotics / VLA / active perception papers: out of scope; Composer routes 3R inputs, not embodied actions. Active perception A8 is a separate spec.
- pure benchmark / leaderboard papers without per-regime breakdown: cite as background only; capability cards need regime-typed claims, not aggregate metrics.
- VLM / scene-understanding papers without 3R routing: skip unless adding a CRITICAL_NOTES.md entry.

## Cross-Paper Disagreement

- **What is a "regime"?** No published 3R paper defines a regime taxonomy explicitly. Composer's regime list (static_pair, many_view, dynamic_video, streaming, sparse_view, asset_output) is an `inferred` taxonomy drawn from the union of comparator papers' "scope" sections. Different papers implicitly assume different regime cuts.
- **MASt3R vs MASt3R-SfM as separate entries**: should they be one capability card or two? Composer treats them as two because their input regimes differ (matching vs SfM-aligned multiview). Some readers expect one card per published paper rather than per regime variant; the distinction is `inferred`.
- **MoE-routing as comparator**: cycle 009 must be careful here. MoE is the closest cross-domain analog but is not a 3R comparator. Treat MoE references as related-work positioning, not as a "Composer comparator".

## Interface To SPEC-20260504-001

- Composer publishes `capability_card`, `sample_regime_card`, `capability_match`, `route_recommendation`, and `route_regret` per `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md`.
- Critic A5 reroute_model consumes `route_recommendation`; per CR-1, if `capability_match` has zero spread, Critic must downgrade to `conflict_unresolved` rather than reroute.
- P5 route_regret is the primary Composer falsification axis.
- Capability cards are paper-derived (paper-proven for per-paper claims) but the regime card weighting and the join is `inferred`.

## Evidence Labels Summary

- DUSt3R, MASt3R, MASt3R-SfM, Fast3R, Spann3R, MonST3R, CUT3R, STream3R, SLAM3R, MV-DUSt3R+, Splatt3R, InstantSplat, NoPoSplat, VGGT, MapAnything, DUSt3R-MASt3R-VGGT MVS evaluation: paper-proven for their published per-regime claims.
- awesome-dust3r: code-curated index (meta-resource); evidence labels propagate from the underlying registry rows it links to.
- Composer regime taxonomy (static_pair / many_view / dynamic_video / streaming / sparse_view / asset_output): inferred.
- capability_match weights, regime probability weights, epsilon_tie: inferred.
- MoE routing borrowed pattern: inferred for 3R use.
