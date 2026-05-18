# Dream3R ablation plan v0.2 (delta on v0.1)

spec_id: SPEC-20260506-005

spec_kind: ablation plan addendum, delta-only (NOT a rewrite of v0.1)

parent_spec: SPEC-20260506-002 (v0.1 ablation plan; substrate; preserved as historical record per Honesty Override)

parent_decision: DEC-20260506-003 (cycle 019 launch + ablation plan v0.2 addendum scope lock)

date: 2026-05-06

cycle: 019 (S2 deliverable; per DEC-20260506-003)

status: v0.2 addendum (candidate-not-final per DEC-20260501-004; iteration on v0.1 ablation plan within architecture-first mainline per DEC-20260506-001; v0.2 architecture deltas locked per DEC-20260506-002; v0.2 ablation deltas locked per DEC-20260506-003)

honesty_label: every ablation below carries an inline evidence label (paper-known / paper-derived / inferred / speculative / engineering-judgment). Each ablation has an explicit review checklist subsection for other-agent handoff per user request 2026-05-06.

linked_artifacts:
- specs/SPEC-20260506-002-dream3r-ablation-plan.md (v0.1 substrate; sections referenced by name; NOT re-stated here)
- decisions/DEC-20260506-003-cycle-019-launch-ablation-plan-v02-addendum.md (parent decision)
- decisions/DEC-20260506-002-cycle-018-launch-v02-architecture.md (parent of parent; v0.2 architecture deltas locked)
- specs/SPEC-20260506-004-dream3r-architecture-v02.md (v0.2 architecture; six numbered deltas tested by ABL-v02-1..9)
- specs/SPEC-20260506-001-dream3r-architecture.md (v0.1 architecture; substrate)
- planning/COMPOSER_CAPABILITY_DESCRIPTORS.md (cycle 018 S2; INPUT for ABL-v02-4 + ABL-v02-5)
- planning/NSA_MEMORY_INTEGRATION_MEMO.md (cycle 018 S3; INPUT for ABL-v02-1 + ABL-v02-6 + ABL-v02-9)
- planning/DINOV3_C1_INTEGRATION_MEMO.md (cycle 018 S3; INPUT for ABL-v02-2 + ABL-v02-3 + ABL-v02-7)

## Identity

This spec is an addendum on `SPEC-20260506-002` v0.1 ablation plan. It does NOT restate v0.1's 10 ABLs (ABL-1..ABL-10), the falsification summary table, the dependency graph, the compute budget estimate, or the boundaries section. Those sections in v0.1 remain canonical. v0.2 introduces nine numbered ablations (ABL-v02-1..9) anchored to v0.2 architecture deltas (Delta 1..6 in SPEC-20260506-004).

A reader who has not read v0.1 should read this addendum first for orientation and then Grep v0.1 by section name only as the addendum references them; full sequential re-reading of v0.1 (~770 lines) is explicitly NOT required and is discouraged per F-001.

## Approval

Approved scope-of-deltas: per `DEC-20260506-003` (cycle 019 launch + ablation plan v0.2 addendum scope lock; user-decided 2026-05-06 from priority list).

Approved review-surface pattern: per user instruction 2026-05-06 ("其他agent审阅修改" + "你文档更新清楚哈"). Each ABL-v02-N includes an explicit review checklist subsection.

NOT approved by this spec:

- training, GPU runs, checkpoint download, code execution. SPEC-005 documents what would be tested; it does NOT authorize execution. Each ABL-v02-N execution requires a separate DEC + per-step micro gates per F-002.
- finalization of Dream3R candidacy (DEC-20260501-004 still in force).
- retiring of any non-finalist track or any v0.1 ABL (DEC-20260504-002 + Honesty Override).
- in-place rewriting of SPEC-002 v0.1 body (Surgical Edits rule 3 + Honesty Override rule 5).
- v0.2 addenda to architecture (SPEC-004 already exists) or comparator map (SPEC-003 v0.2 addendum is post-019 trajectory item 2).
- KYKT navigation change, frontend implementation, demo storyboard promotion past `draft`, teacher-demo readiness claim, paper Phase 2 rewrite for v0.2.

## Scope of v0.2 addendum

```text
markdown only
candidate-not-final (DEC-20260501-004)
no-all-in (DEC-20260504-002)
architecture-first mainline (DEC-20260506-001)
v0.2 architecture deltas locked (DEC-20260506-002)
v0.2 ablation deltas locked (DEC-20260506-003)
v0.2 addendum: delta-only (this spec)
```

v0.2 introduces nine numbered ablations (ABL-v02-1..9) over v0.1's 10 ABLs. v0.1 ABLs are NOT replaced; they remain canonical for v0.1 architecture testing. v0.2 ABLs cover surfaces opened by v0.2 architecture deltas that v0.1 ABLs do not address.

## Reading order

```text
1. Read this spec (you are here).
2. Read DEC-20260506-003 (parent decision; v0.2 ablation deltas
   locked + post-019 trajectory + review surface pattern).
3. Read DEC-20260506-002 (parent of parent; v0.2 architecture
   deltas locked).
4. Read SPEC-20260506-004 (v0.2 architecture; six numbered deltas
   that ABL-v02-1..9 test).
5. Reference the three cycle 018 planning artifacts (capability
   descriptors + NSA memo + DINOv3 memo) when an ABL-v02-N references
   them.
6. Reference v0.1 SPEC-002 ONLY by Grep -n on section names cited
   in the v0.1 ABL traceability matrix below. Do NOT re-read v0.1
   in full (F-001 anti-32MB rule).
```

## Why v0.2 addendum exists

DEC-20260506-003 §"Why this matters" enumerates eight ablation surfaces opened by v0.2 deltas that v0.1 SPEC-002 does not cover:

```text
S1. NSA-to-3R transfer is speculative (no published 3R use)
S2. DINOv3-S substitution risks pointmap quality regression
S3. Frame budget 30-50 ms/frame is inferred (not measured)
S4. Composer best-of-7 vs single-expert is the D-claim falsification
S5. Capability_match values per expert are inferred
S6. Selection-gate signal mix (Critic + Permanence) is speculative
S7. Heads-from-scratch training schedule is unspecified
S8. NSA hardware-aware kernel benefit on TITAN RTX is uncertain
```

ABL-v02-1..9 below address these eight surfaces (with one ABL covering two of them where natural; see traceability matrix).

## v0.1 ABL traceability matrix

Each v0.2 ABL is positioned against v0.1 ABLs as: `extends` (refines a v0.1 ABL with v0.2-specific variant), `independent` (tests a delta that has no v0.1 ABL counterpart), or `supersedes-in-v02-scope` (v0.1 ABL still applies to v0.1 architecture; v0.2 ABL replaces it for v0.2 architecture testing).

| v0.2 ABL | Tests v0.2 delta | Surface | v0.1 ABL relationship |
|---|---|---|---|
| ABL-v02-1 NSA-removal | Delta 3 + Delta 4 | S1 + S8 | independent (v0.1 has no NSA) |
| ABL-v02-2 DINOv3 backbone tier | Delta 2 | S2 | extends ABL-2 (substrate hypothesis adds backbone tier axis) |
| ABL-v02-3 Frozen vs partial-unfreeze | Delta 2 | S2 | independent (v0.1 had no frozen-backbone proposal) |
| ABL-v02-4 Composer best-of-N vs single-expert | Delta 5 + Delta 6 D | S4 | extends ABL-7 (Composer removal generalized to per-expert isolation) |
| ABL-v02-5 Capability_match measurement pass | Delta 5 | S5 | independent (v0.1 had no per-expert capability_match) |
| ABL-v02-6 Selection-gate signal subsetting | Delta 3 + Delta 6 A | S6 | independent (v0.1 had no NSA selection gate) |
| ABL-v02-7 Head training schedule | Delta 2 | S7 | independent (v0.1 had no head-from-scratch setup) |
| ABL-v02-8 Frame-budget benchmark | Delta 1 | S3 | independent (v0.1 had no per-frame budget) |
| ABL-v02-9 NSA kernel benefit decomposition | Delta 4 | S8 | independent |

Two v0.2 ABLs (ABL-v02-2 and ABL-v02-4) extend v0.1 ABLs with additional axes; the rest are independent because they test deltas with no v0.1 counterpart.

## Pillar tier placement

Each v0.2 ABL inherits SPEC-002 v0.1's three-tier ordering (Tier 1 load-bearing / Tier 2 should-run / Tier 3 nice-to-have):

```text
Tier 1 (load-bearing; if these fail, v0.2 architecture story collapses):
  ABL-v02-1 NSA-removal              -> falsifies Delta 3 + Delta 4
  ABL-v02-4 Composer best-of-N       -> falsifies Delta 5 + main-claim D
  ABL-v02-6 Selection-gate signal    -> falsifies Delta 3 verification
                                        signal mix; main-claim A linkage

Tier 2 (should-run; per-module substrate choices):
  ABL-v02-2 DINOv3 backbone tier     -> backbone weight class quality
  ABL-v02-3 Frozen vs unfreeze       -> training simplification cost
  ABL-v02-7 Head training schedule   -> DINOv3-S quality ceiling
  ABL-v02-8 Frame-budget benchmark   -> streaming compliance check

Tier 3 (nice-to-have; engineering refinement and honest reporting):
  ABL-v02-5 Capability_match pass    -> promotes inferred -> measured
  ABL-v02-9 NSA kernel decomposition -> algorithmic vs kernel benefit
```

## Ablation specifications

### ABL-v02-1: NSA-removal

```text
ablation_id:     ABL-v02-1
tests_delta:     SPEC-004 Delta 3 (C2 Memory NSA hierarchy A+B) +
                 Delta 4 (sparse attention as engineering optimization)
v01_relation:    independent (v0.1 had no NSA component)
tier:            1 (load-bearing)
evidence_label:  speculative (NSA-to-3R transfer has no published 3R prior art)
```

Baseline: full v0.2 C2 Memory with NSA three-branch retrieval (compressed + selected + sliding) per SPEC-004 Delta 3 + NSA_MEMORY memo.

Variant: replace NSA selected branch with plain anchor bank cosine top-k retrieval (k = 8, same as NSA selected). Compressed and sliding branches are retained. Selection gate input mix (Critic confidence + Permanence link) is replicated for both NSA and cosine variants.

Test setup:

- Benchmarks: B1 (static pair, sanity check), B2 (many-view static, anchor retention), B3 (long dynamic video, drift + retrieval recall), B5 (geometric ambiguity, verification routing).
- Metrics: P2 anchor retention, P3 memory growth, route_regret on B3, verification recall on B5.
- Compute (inferred): ~40 GPU-hours per variant on TITAN RTX 24 GB; two variants -> ~80 GPU-hours total. Server-side per F-002.

Expected outcome (evidence label: speculative):

- If NSA selection meaningfully improves retrieval recall over cosine top-k on B3 long-context, then NSA's contribution is non-zero and the speculative label was honest.
- If NSA selection is statistically indistinguishable from cosine top-k (P2 + retrieval recall within noise), then NSA contributes zero algorithmic value to v0.2 and Delta 3 + Delta 4 framing should be retracted in v0.3.

Falsification interpretation:

- A null result here falsifies Delta 3's "NSA as substrate for Memory" claim. v0.3 would either (a) drop NSA from Memory and use plain cosine retrieval, or (b) re-anchor NSA's role to a different module where it contributes (e.g., C5 Composer routing). It does NOT falsify the bounded anchor bank itself (the bank is independent of the retrieval mechanism on top).
- A positive result confirms NSA's algorithmic contribution but does not yet validate hardware-aware kernel benefit; that is ABL-v02-9.

Execution gate:

- Requires separate DEC + per-step micro gates (G_clone / G_install / G_download / G_run / G_log_use) similar to cycle 015's Critic L3 pilot scope. NOT authorized by SPEC-005 alone. Server-side per F-002.

Review checklist (for other agents picking up this ABL):

```text
[ ] Verify baseline NSA configuration matches SPEC-004 Delta 3 +
    NSA_MEMORY memo (k=8, compressed=32, sliding=4 windows).
[ ] Verify cosine top-k variant uses the SAME selection gate input
    mix (Critic confidence + Permanence link); the ablation tests
    NSA's selection mechanism, not the input signals.
[ ] Verify benchmarks B1+B2+B3+B5 cover both short-context (B1+B2)
    and long-context (B3) regimes; B5 covers verification triggering.
[ ] Verify P2 + P3 + retrieval recall + verification recall are all
    measured (not just one or two).
[ ] Verify GPU-hour estimate is dream3r-server-specific (TITAN RTX),
    not paper-derived A100/H100 numbers.
[ ] Verify expected-outcome reasoning does not collapse "NSA wins"
    and "cross-module signal mix wins" — those are separated by
    ABL-v02-6.
[ ] Verify execution gate is intact (no implicit authorization in
    SPEC-005 alone).
[ ] If modifying baseline / variant / metrics, supersede via a fresh
    DEC and a v0.3 addendum; do NOT edit this section in-place.
```

### ABL-v02-2: DINOv3 backbone tier (-S / -B / -L)

```text
ablation_id:     ABL-v02-2
tests_delta:     SPEC-004 Delta 2 (C1 Perceiver DINOv3-S replaces ViT-L)
v01_relation:    extends ABL-2 (substrate hypothesis adds backbone weight-class axis)
tier:            2 (should-run)
evidence_label:  paper-derived (DINOv3 family well-published; -S vs -B Pareto frontier inferred from feature benchmarks)
```

Baseline: DINOv3-Small backbone (~22M params) frozen, heads from scratch (pointmap_head + confidence_head + evidence_head per SPEC-004 Delta 2).

Variants:

- DINOv3-Base (~85M params), frozen, heads from scratch.
- DINOv3-Large (~300M params), frozen, heads from scratch (matches v0.1 ViT-L weight class; expected to exceed 30 FPS budget).
- v0.1 ViT-L (DUSt3R lineage; reference baseline for quality regression check).

Test setup:

- Benchmarks: B1 (static pair, pointmap quality), B2 (many-view, multi-view consistency), B5 (geometric ambiguity, feature quality under degenerate baselines).
- Metrics: pointmap end-point error (EPE), per-pixel confidence calibration, per-frame latency on TITAN RTX (for budget compliance check; cross-references ABL-v02-8).
- Compute (inferred): ~20 GPU-hours per variant on TITAN RTX; four variants -> ~80 GPU-hours total. Server-side per F-002.

Expected outcome (evidence label: paper-derived):

- DINOv3-S: feature quality match DINOv2-B claim per paper (paper-known); pointmap quality regression vs ViT-L is `inferred`; expected EPE within ~10-20 percent of ViT-L baseline.
- DINOv3-B: closer to ViT-L pointmap quality; latency ~45-60 ms on TITAN RTX (borderline 30 FPS compliance).
- DINOv3-L: matches or exceeds ViT-L pointmap quality; exceeds 30 FPS budget at full res — tested only as escape hatch.

Falsification interpretation:

- If DINOv3-S EPE regression vs ViT-L exceeds ~30 percent on B1, then frozen-backbone simplification is NOT viable at -S; v0.2 must fall back to -B (per SPEC-004 Delta 2 fallback documentation) or unlock partial unfreezing (ABL-v02-3).
- If DINOv3-B is within 5 percent of ViT-L AND fits 30 FPS budget, the v0.2 backbone choice may be revised in v0.3 to default -B over -S.
- A null result (DINOv3-S matches ViT-L on B1+B2+B5) confirms paper-derived claim and validates Delta 2 default.

Execution gate:

- Requires separate DEC + per-step micro gates. NOT authorized by SPEC-005 alone. Server-side per F-002. DINOv3 weights download requires a fresh G_download gate (not yet authorized).

Review checklist (for other agents picking up this ABL):

```text
[ ] Verify all four variants use identical training data, schedule,
    and head architectures; only the backbone weight class varies.
[ ] Verify ViT-L baseline uses DUSt3R checkpoint (not random init);
    this is a quality-regression check, not from-scratch comparison.
[ ] Verify benchmarks B1+B2+B5 include both static and ambiguity
    regimes; B5 is critical because feature quality under degenerate
    baselines is where DINOv3-S vs ViT-L differences are largest.
[ ] Verify EPE metric is computed at the same input resolution
    (384x512 per SPEC-004 Delta 2) for all variants.
[ ] Verify per-frame latency is measured on TITAN RTX, not paper-
    claim A100; budget compliance is the integration constraint.
[ ] Verify DINOv3 license terms allow research use under the project's
    license posture (per DINOV3_C1 memo §"Risk / honest limits" item 5).
[ ] Verify execution gate is intact.
[ ] If modifying baseline / variants / metrics, supersede via fresh
    DEC and v0.3 addendum.
```

### ABL-v02-3: Frozen vs partial-unfreeze

```text
ablation_id:     ABL-v02-3
tests_delta:     SPEC-004 Delta 2 (frozen-backbone default)
v01_relation:    independent (v0.1 had no frozen-backbone proposal)
tier:            2 (should-run)
evidence_label:  inferred (no published frozen-backbone numbers for 3R pointmap regression on DINOv3)
```

Baseline: DINOv3-S backbone fully frozen, heads trainable.

Variants:

- Top-2 DINOv3 blocks unfrozen + heads trainable.
- Top-4 DINOv3 blocks unfrozen + heads trainable.
- Full backbone unfrozen + heads trainable (full fine-tune; reference upper bound).

Test setup:

- Benchmarks: B1 + B2 + B5 (pointmap quality regimes).
- Metrics: pointmap EPE, training cost (GPU-hours to convergence), final pointmap quality.
- Compute (inferred): ~25 GPU-hours per variant; four variants -> ~100 GPU-hours total. Server-side per F-002.

Expected outcome (evidence label: inferred):

- Frozen-backbone: cheapest training; pointmap quality is the empirical question. If DINOv3-S features carry sufficient geometric content, frozen-backbone is viable.
- Top-2 / Top-4 unfreeze: incrementally better quality; diminishing returns expected.
- Full unfreeze: best quality; highest training cost; likely overkill if Top-4 closes the gap.

Falsification interpretation:

- If frozen-backbone EPE is within 5 percent of full-unfreeze, frozen is the v0.2 default and the simplification holds.
- If frozen-backbone EPE exceeds full-unfreeze by more than 15 percent, v0.2 should default to Top-N unfreeze (with N determined by Pareto curve), not frozen.
- Result feeds into ABL-v02-7 (head training schedule).

Execution gate:

- Requires separate DEC + per-step micro gates. Server-side per F-002.

Review checklist:

```text
[ ] Verify all variants use identical learning rate schedule, batch
    size, and dataset; only unfreeze depth varies.
[ ] Verify "block" granularity matches DINOv3 family architecture
    (DINOv3 typically has 12 blocks for -S; pin block count in
    execution DEC).
[ ] Verify training cost is reported in GPU-hours-to-convergence,
    not fixed-budget GPU-hours (some variants may converge faster).
[ ] Verify pointmap EPE is reported on a held-out test split, not
    training set.
[ ] Verify frozen-backbone variant truly freezes (no batch-norm
    statistics drift; verify via parameter gradient check).
[ ] Verify execution gate is intact.
[ ] If modifying baseline / variants / metrics, supersede via fresh
    DEC and v0.3 addendum.
```

### ABL-v02-4: Composer best-of-N vs single-expert per regime

```text
ablation_id:     ABL-v02-4
tests_delta:     SPEC-004 Delta 5 (7-expert pool) + Delta 6 main-claim D
                 (Heterogeneous best-of-N Composer)
v01_relation:    extends ABL-7 (Composer removal -> per-expert isolation refinement)
tier:            1 (load-bearing; main-claim D primary demonstration)
evidence_label:  paper-derived (per-expert paper-known innovation_points; route_regret is an inferred Composer-level metric)
```

Baseline: full v0.2 Composer with all 7 experts (MASt3R / Fast3R / Spann3R / CUT3R / MoGe-2 / DepthAnything-V2 / Test3R) and capability descriptor routing per COMPOSER_CAPABILITY_DESCRIPTORS routing policy sketch.

Variants (per-regime single-expert isolation):

- Single-expert variant per pool member (7 variants total): force route to one expert always; measure per-regime quality vs best-of-N.
- "Best static expert" variant: pick the single expert that minimizes overall route_regret across all regimes; compare best-of-N vs this.

Test setup:

- Benchmarks: B1 (static pair, MASt3R home regime), B2 (many-view, Fast3R home regime), B3 (long dynamic, Spann3R + CUT3R streaming regime), B4 (mixed-regime batch, Composer routing primary target), B5 (geometric ambiguity, Critic + Test3R triggering).
- Metrics: route_regret per regime (P5), pointmap EPE per regime, latency per regime, route accuracy (does Composer pick the expected expert?).
- Compute (inferred): ~10 GPU-hours per variant per benchmark; 8 variants × 5 benchmarks -> ~400 GPU-hours total. Server-side per F-002.

Expected outcome (evidence label: paper-derived):

- Best-of-N should beat any single-expert variant on B4 (mixed-regime batch) by route_regret. This is the paper-derived expectation: heterogeneous pool exploits non-uniform infrastructure.
- Single-expert variants should win their home regime (e.g., MASt3R on B1, Fast3R on B2, Spann3R on B3 streaming).
- "Best static expert" should approach but not beat best-of-N on B4 (the routing layer adds value when regime distribution is mixed).

Falsification interpretation:

- If best-of-N does NOT beat the best static expert on B4 by a meaningful margin (~5+ percent route_regret reduction), main-claim D collapses. v0.3 would need to either (a) reframe Composer as a different mechanism, or (b) drop the best-of-N pillar entirely.
- If best-of-N wins on B4 but loses to a single expert on B1+B2+B3 home regimes, the routing policy needs refinement (likely capability_match weights from ABL-v02-5).
- A clean win across B4 confirms paper-derived claim D and validates the 7-expert pool composition.

Execution gate:

- Requires separate DEC + per-step micro gates. Server-side per F-002. CUT3R checkpoint is not yet inventoried on dream3r server (per COMPOSER_CAPABILITY_DESCRIPTORS open items); a separate G_download gate is required for CUT3R before this ablation runs.

Review checklist:

```text
[ ] Verify all 7 single-expert variants are tested; do NOT cherry-pick
    a subset.
[ ] Verify B4 (mixed-regime batch) construction is documented:
    composition of B1+B2+B3 inputs, ratio per regime.
[ ] Verify route_regret metric definition is anchored to v2.1 cross-
    spec contract (paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md); do NOT
    invent a new metric.
[ ] Verify capability_match values used for routing are sourced
    (inferred from COMPOSER_CAPABILITY_DESCRIPTORS or measured per
    ABL-v02-5; if measured, this ablation depends on ABL-v02-5
    completing first).
[ ] Verify CUT3R checkpoint provenance + license before download.
[ ] Verify Test3R lazy-invocation path is correctly off-streaming
    (does NOT contribute to per-frame latency in best-of-N variant).
[ ] Verify falsification interpretation does not silently re-promote
    VGGT or MapAnything (those remain dropped per DEC-20260506-002).
[ ] Verify execution gate is intact.
[ ] If modifying pool composition / variant set / metrics, supersede
    via fresh DEC and v0.3 addendum.
```

### ABL-v02-5: Capability_match measurement pass

```text
ablation_id:     ABL-v02-5
tests_delta:     SPEC-004 Delta 5 (7-expert capability descriptors)
v01_relation:    independent (v0.1 had no per-expert capability_match)
tier:            3 (nice-to-have; honest reporting + dependency for ABL-v02-4 routing)
evidence_label:  inferred -> measured-if-executed (capability_match values in
                 COMPOSER_CAPABILITY_DESCRIPTORS are currently inferred per row)
```

This is a measurement plan, not a counterfactual ablation. Its purpose is to promote each capability_match value from `inferred` to `measured` for the 7 admitted experts.

Baseline: capability_match values per expert as listed in COMPOSER_CAPABILITY_DESCRIPTORS §"Pool members" (all `inferred` v0.1).

Variant: re-measure each axis on a held-out micro-benchmark.

Test setup:

- Benchmarks: held-out micro-benchmark = 5 scenes × 4 regimes (pair / multi-view / streaming / mono); explicitly NOT B1-B6 (those are for ABL-v02-1..4 and v0.1 ABLs).
- Metrics: per-expert per-regime quality score; per-expert per-regime latency; combined into capability_match axis values per the COMPOSER_CAPABILITY_DESCRIPTORS schema.
- Compute (inferred): ~5 GPU-hours per expert per regime; 7 experts × 4 regimes -> ~140 GPU-hours total. Server-side per F-002.

Expected outcome (evidence label: inferred):

- capability_match values in COMPOSER_CAPABILITY_DESCRIPTORS will shift; some expected directions:
  - MASt3R streaming may be lower than 0.2 inferred (matching head is not streaming-natural).
  - Spann3R streaming may exceed 0.95 inferred if anchor mechanism extends to longer contexts than tested.
  - Fast3R per-frame share at N=8 may differ from ~50-80 ms inferred.
- Measurement results feed back into COMPOSER_CAPABILITY_DESCRIPTORS as a measured-evidence revision (which itself requires a fresh DEC because the file is a planning artifact, not auto-modifiable).

Falsification interpretation:

- A measurement pass cannot "falsify" — it produces measured values. The interpretation is whether measured values support v0.2 routing policy.
- If measured capability_match values diverge from inferred by more than ~30 percent on multiple axes, ABL-v02-4 routing policy needs revision; main-claim D framing may need to be revisited.

Execution gate:

- Requires separate DEC + per-step micro gates. Server-side per F-002. Multiple checkpoint downloads required (one per expert; CUT3R + Test3R + MoGe-2 + DepthAnything-V2 are not all currently inventoried). Dependency: ABL-v02-4 should run AFTER this if measured values are to be used in best-of-N routing.

Review checklist:

```text
[ ] Verify held-out micro-benchmark is documented (which 5 scenes,
    which 4 regimes, why those choices).
[ ] Verify per-expert measurement uses the SAME benchmark inputs
    across experts (not cherry-picked per expert).
[ ] Verify quality + latency metrics are reported separately, not
    fused into a single capability_match number prematurely.
[ ] Verify COMPOSER_CAPABILITY_DESCRIPTORS update path is documented
    (separate DEC + v0.3 update; not auto-modified).
[ ] Verify checkpoint provenance + license for each of 7 experts
    (some are already on server per F-002; CUT3R + others need
    fresh G_download gates).
[ ] Verify measurement does NOT re-introduce dropped experts (VGGT,
    MapAnything, Kimi-KDA).
[ ] Verify execution gate is intact.
[ ] If modifying micro-benchmark / measurement methodology,
    supersede via fresh DEC and v0.3 addendum.
```

### ABL-v02-6: Selection-gate signal subsetting

```text
ablation_id:     ABL-v02-6
tests_delta:     SPEC-004 Delta 3 (selection gate driven by Critic +
                 Permanence) + Delta 6 main-claim A (Verification-as-
                 architecture)
v01_relation:    independent (v0.1 had no NSA selection gate)
tier:            1 (load-bearing; main-claim A linkage to Memory
                 retrieval semantic)
evidence_label:  speculative (cross-module signal mix has no prior-art
                 3R validation per NSA_MEMORY memo)
```

Baseline: NSA selection gate driven by both Critic confidence + Permanence link (full v0.2 Delta 3).

Variants:

- Critic-only: gate input is critic_confidence only; permanence_link is masked out.
- Permanence-only: gate input is permanence_link only; critic_confidence is masked out.
- Neither: gate is signal-agnostic (uses query embedding only, like vanilla NSA).
- Both (= baseline): control.

Test setup:

- Benchmarks: B3 (long dynamic, drift detection sensitive to verification signal), B5 (geometric ambiguity, Critic confidence is the primary gating signal here), B6 (adversarial CR-rule-triggering, verification path stress test).
- Metrics: retrieval precision under verification triggering (does the gate retrieve the right anchors when Critic flags a region?), verification recall on B5, drift-correction rate on B3.
- Compute (inferred): ~30 GPU-hours per variant; four variants -> ~120 GPU-hours total. Server-side per F-002.

Expected outcome (evidence label: speculative):

- Both (baseline): expected best on B3 + B5 + B6.
- Critic-only: expected to match baseline on B5 + B6 (Critic-driven verification regimes); regress on B3 long-context (no permanence_link to bias retrieval toward anchored objects).
- Permanence-only: expected to match baseline on B3 long-context; regress on B5 + B6 (no Critic signal to bias retrieval toward verification).
- Neither: expected worst across all three benchmarks.

Falsification interpretation:

- If "Neither" is statistically indistinguishable from "Both" on B3 + B5 + B6, the cross-module signal mix is NOT load-bearing; main-claim A's NSA-linkage framing collapses. v0.3 would need to reframe Verification-as-architecture without the Memory-selection-gate hook (CR-1..CR-6 + Test3R lazy invocation can stand alone).
- If "Critic-only" and "Permanence-only" each match "Both" on their own benchmark but underperform on the other, the signal mix IS additive — confirms speculative claim.

Execution gate:

- Requires separate DEC + per-step micro gates. Server-side per F-002. Depends on ABL-v02-1 having validated NSA itself (otherwise this tests a mechanism that may not contribute).

Review checklist:

```text
[ ] Verify gate masking is implemented at input level (forced-zero
    or forced-uniform), not at training level (would conflate
    training signal with inference signal).
[ ] Verify benchmark coverage spans long-context (B3) AND verification
    triggering (B5 + B6); single-benchmark results are insufficient.
[ ] Verify all four variants share identical NSA hyperparameters
    (k=8, compressed=32, sliding=4); only signal mix varies.
[ ] Verify "drift-correction rate" metric is operationally defined
    (e.g., reduction in pointmap EPE drift over a 100-frame window
    after a triggered retrieval).
[ ] Verify dependency: ABL-v02-1 (NSA-removal) should run first;
    if NSA itself contributes nothing, this ablation is moot.
[ ] Verify falsification interpretation does NOT silently re-introduce
    a different gating signal (the test is the four explicit subsets).
[ ] Verify execution gate is intact.
[ ] If modifying signal subset definitions / metrics, supersede via
    fresh DEC and v0.3 addendum.
```

### ABL-v02-7: Head training schedule

```text
ablation_id:     ABL-v02-7
tests_delta:     SPEC-004 Delta 2 (heads from scratch; ViT-L head
                 weights cannot transfer)
v01_relation:    independent (v0.1 had no head-from-scratch training setup)
tier:            2 (should-run)
evidence_label:  inferred (training schedule effects on DINOv3-S +
                 from-scratch heads are not paper-known for 3R)
```

Baseline: heads trained from scratch with frozen DINOv3-S backbone (per SPEC-004 Delta 2 default).

Variants:

- Head-only training (baseline): heads trained, backbone frozen.
- Head warmup + Top-N unfreeze (multi-stage): train heads first, then unfreeze top-N DINOv3 blocks for joint fine-tuning.
- Full joint training from scratch (heads + full backbone unfrozen): reference upper bound.

Test setup:

- Benchmarks: B1 + B2 + B5 (pointmap quality regimes; same as ABL-v02-3 for cross-comparison).
- Metrics: pointmap EPE, training cost (GPU-hours-to-convergence), final pointmap quality, training stability (loss variance across runs).
- Compute (inferred): ~30 GPU-hours per variant; three variants × 3 seeds for stability -> ~270 GPU-hours total. Server-side per F-002.

Expected outcome (evidence label: inferred):

- Head-only: cheapest; quality depends on DINOv3-S feature geometric content (per ABL-v02-3 frozen-backbone result).
- Head warmup + Top-N unfreeze: expected best quality-vs-cost ratio; multi-stage training is standard for transfer learning.
- Full joint: best quality; highest cost; potentially unstable from scratch.

Falsification interpretation:

- If multi-stage and head-only are within 5 percent EPE, head-only is the v0.2 default; multi-stage is unnecessary complexity.
- If full-joint exceeds multi-stage by more than 10 percent, full-joint is the recommended schedule despite cost; v0.2 frozen-backbone default is overly conservative.
- Result feeds into v0.3 spec revision for default training schedule.

Execution gate:

- Requires separate DEC + per-step micro gates. Server-side per F-002. Depends on ABL-v02-3 (frozen vs unfreeze) for backbone unfreeze depth choice.

Review checklist:

```text
[ ] Verify all variants share identical dataset, batch size, learning
    rate scheduler family; only training-stage structure varies.
[ ] Verify "head warmup" duration is documented (e.g., N epochs head-
    only, then unfreeze).
[ ] Verify multi-seed reporting (mean + variance across at least 3
    seeds); single-seed numbers are insufficient for stability claim.
[ ] Verify full-joint variant initializes backbone from DINOv3-S
    pre-trained weights (NOT random init); the test is fine-tune
    schedule, not train-from-scratch.
[ ] Verify metric set includes training stability (loss variance),
    not just final EPE.
[ ] Verify execution gate is intact.
[ ] If modifying schedule definitions / variants, supersede via
    fresh DEC and v0.3 addendum.
```

### ABL-v02-8: Frame-budget benchmark

```text
ablation_id:     ABL-v02-8
tests_delta:     SPEC-004 Delta 1 (30-50 ms/frame at 30 FPS streaming-first)
v01_relation:    independent (v0.1 had no per-frame budget table)
tier:            2 (should-run; compliance check before any streaming-
                 first claim publishes)
evidence_label:  inferred (component budget allocations are paper-
                 derived; total budget on TITAN RTX is unmeasured)
```

Baseline: full v0.2 streaming pipeline (DINOv3-S + NSA Memory + Permanence + Critic + Composer + Bus) per SPEC-004 Delta 1 component allocation.

Variants:

- Per-component latency profiling: measure each of C1..C6 individually under realistic streaming load (not isolated forward passes).
- End-to-end streaming: measure total per-frame latency under continuous 30 FPS input.
- Lazy-path off-streaming: measure latency with EXPERT-07 Test3R lazy invocation triggered at low / medium / high frequency; verify off-streaming claim (Test3R does NOT block 30 FPS budget).

Test setup:

- Benchmarks: B3 (long dynamic, realistic streaming), B4 (mixed-regime, routing latency stress), B5 (geometric ambiguity, Critic + verification triggering frequency).
- Metrics: per-component latency (ms), end-to-end latency (ms), per-frame budget compliance rate (percent of frames under 50 ms), tail latency p95 / p99.
- Compute (inferred): ~5 GPU-hours per variant; three variants × 3 benchmarks -> ~45 GPU-hours total. Server-side per F-002.

Expected outcome (evidence label: inferred):

- Per-component: C1 ~10-15 ms, C2 ~few ms, C3 ~few ms, C4 ~few ms, C5/C6 <1 ms (paper-derived; matches DINOV3_C1 + NSA_MEMORY memos).
- End-to-end on TITAN RTX: ~25-40 ms under realistic streaming (paper-derived A100 numbers may not transfer).
- Lazy-path: Test3R triggered at high frequency may starve streaming budget if poorly scheduled; verify scheduler design.

Falsification interpretation:

- If end-to-end p95 exceeds 50 ms / frame on TITAN RTX, Delta 1 streaming-first claim must be retracted in v0.3 or qualified ("on H100; on TITAN RTX the budget is X").
- If per-component sums to less than measured end-to-end by more than 20 percent, integration overhead is significant and Delta 1 component allocation is incomplete.
- A clean compliance result on B3+B4+B5 confirms paper-derived budget claim.

Execution gate:

- Requires separate DEC + per-step micro gates. Server-side per F-002. Lighter compute than other ABLs; primarily measurement, not training.

Review checklist:

```text
[ ] Verify TITAN RTX (24 GB) is the target hardware; do NOT report
    A100 or H100 numbers as if they were dream3r-server-applicable.
[ ] Verify per-component measurement uses identical input / context
    state across components; latency depends on context.
[ ] Verify end-to-end measurement runs continuously over multiple
    seconds (not single-frame averages); tail latency matters for
    streaming compliance.
[ ] Verify lazy-path measurement explicitly triggers Test3R at known
    frequencies; document the scheduler used.
[ ] Verify reported numbers include p50 + p95 + p99 (mean alone is
    insufficient for streaming compliance).
[ ] Verify execution gate is intact.
[ ] If modifying component allocations, supersede via fresh DEC and
    v0.3 architecture addendum (not just ablation revision).
```

### ABL-v02-9: NSA kernel benefit decomposition

```text
ablation_id:     ABL-v02-9
tests_delta:     SPEC-004 Delta 4 (NSA as engineering optimization)
v01_relation:    independent
tier:            3 (nice-to-have; engineering refinement + honest reporting)
evidence_label:  inferred (NSA kernel was developed for H100; TITAN RTX
                 transfer benefit is unmeasured)
```

Baseline: NSA selected branch with hardware-aware kernel (per NSA paper implementation; if available for cu121 / TITAN RTX).

Variants:

- Algorithmic-only NSA: NSA selection logic with naive (non-fused) attention kernel; isolates algorithmic sparsity benefit.
- Plain dense attention with NSA-equivalent k=8 top-k masking (post-hoc): tests whether the speed benefit comes from the selection mechanism or just the reduced attention size.
- Hardware-aware NSA kernel (= baseline): control.

Test setup:

- Benchmarks: synthetic latency benchmark (single Memory layer, fixed sequence length 1024, batch 8).
- Metrics: forward latency on TITAN RTX, peak memory, FLOPs.
- Compute (inferred): ~2 GPU-hours total (light measurement). Server-side per F-002.

Expected outcome (evidence label: inferred):

- Hardware-aware NSA: paper-claim large speedup on H100; on TITAN RTX likely smaller speedup due to architectural mismatch.
- Algorithmic-only NSA: still faster than dense attention due to k=8 top-k reduction.
- Plain dense + post-hoc top-k: similar latency to algorithmic-only (validates that selection mechanism is the source of benefit).

Falsification interpretation:

- If hardware-aware kernel and algorithmic-only are within ~10 percent latency on TITAN RTX, the kernel benefit does NOT transfer; Delta 4 framing should explicitly note "algorithmic sparsity gain only on dream3r-server hardware".
- If hardware-aware kernel is significantly faster, the kernel itself is load-bearing and v0.2 should pin a specific kernel implementation.

Execution gate:

- Requires separate DEC. Lighter compute. Server-side per F-002. Depends on a usable NSA kernel implementation existing for cu121 + TITAN RTX (uncertain; check prior to launching).

Review checklist:

```text
[ ] Verify NSA kernel implementation provenance (DeepSeek release vs
    third-party port); pin commit / version.
[ ] Verify cu121 + TITAN RTX compatibility before running (kernel
    may not compile on non-H100).
[ ] Verify "algorithmic-only" variant disables kernel-level fusion
    explicitly (not just "no FlashAttention"; NSA has its own fused
    path).
[ ] Verify benchmark uses realistic sequence length (1024 chosen as
    compromise; v0.2 actual context may differ).
[ ] Verify reported numbers separate latency / memory / FLOPs (the
    three are not perfectly correlated for NSA).
[ ] Verify execution gate is intact.
[ ] If kernel is unavailable for cu121, this ablation defers to a
    later cycle; document the deferral honestly rather than running
    a meaningless test.
```

## Falsification mapping table (v0.2 main-claim pillars)

| Main claim | Pillar | Primary falsifying ABLs | Secondary falsifying ABLs |
|---|---|---|---|
| A. Verification-as-architecture | Critic gate is structural write-blocker; verification routes to Test3R lazily | ABL-v02-6 (selection-gate signal) | ABL-v02-1 (NSA-removal indirectly) |
| D. Heterogeneous best-of-N Composer | Pool of 7 lightweight experts; routing exploits non-uniform infrastructure | ABL-v02-4 (best-of-N vs single-expert) | ABL-v02-5 (capability_match measurement) |
| E. Identity-anchored memory (supporting) | Permanence × Memory coupling | ABL-v02-6 (Permanence-only variant tests E linkage) | ABL-v02-1 (anchor bank itself) |

Pillars B (state-ownership invariant) and C (reservation tokens A7/A8) are demoted to discipline / future per DEC-20260506-002 + SPEC-20260506-004 Delta 6; they do NOT have v0.2-specific falsifying ablations. v0.1 ABL-3 (state-ownership isolation) covers B at v0.1 architecture level; that remains canonical.

## Benchmark input mapping

v0.1 B1-B6 categories (per SPEC-002 §"Benchmark input selection for ablations" line 537+) are reused without modification. v0.2 ablations use them as follows:

| ABL-v02 | B1 | B2 | B3 | B4 | B5 | B6 |
|---|---|---|---|---|---|---|
| ABL-v02-1 NSA-removal | yes | yes | yes | — | yes | — |
| ABL-v02-2 DINOv3 tier | yes | yes | — | — | yes | — |
| ABL-v02-3 Frozen vs unfreeze | yes | yes | — | — | yes | — |
| ABL-v02-4 Composer best-of-N | yes | yes | yes | yes | yes | — |
| ABL-v02-5 Capability_match | (held-out micro-benchmark; not B1-B6) |
| ABL-v02-6 Selection-gate signal | — | — | yes | — | yes | yes |
| ABL-v02-7 Head training schedule | yes | yes | — | — | yes | — |
| ABL-v02-8 Frame-budget | — | — | yes | yes | yes | — |
| ABL-v02-9 NSA kernel | (synthetic latency benchmark; not B1-B6) |

No new B-category is needed for v0.2; B1-B6 cover all ABL-v02 surfaces. ABL-v02-5 introduces a held-out micro-benchmark (5 scenes × 4 regimes) that is explicitly NOT a new B-category but a measurement-specific sample set.

## Dependency graph (v0.2 ABLs)

```text
ABL-v02-1 (NSA-removal)
    -> required-before -> ABL-v02-6 (selection-gate; tests gate
                                     mechanism on top of NSA)
    -> required-before -> ABL-v02-9 (kernel decomp; tests kernel
                                     benefit only if NSA itself
                                     contributes)

ABL-v02-2 (DINOv3 tier)
    -> required-before -> ABL-v02-3 (frozen vs unfreeze; depends on
                                     -S being the chosen tier)
    -> required-before -> ABL-v02-7 (head training; backbone tier
                                     determines head capacity)

ABL-v02-5 (capability_match measurement)
    -> recommended-before -> ABL-v02-4 (best-of-N routing benefits
                                       from measured capability_match)

ABL-v02-8 (frame-budget) is INDEPENDENT of all other ABLs (compliance
check; can run anytime).

ABL-v02-4 (best-of-N vs single-expert) is INDEPENDENT of NSA chain
(Composer routing does not rely on Memory NSA).
```

Recommended execution order if executed:

```text
1. ABL-v02-8 (frame-budget; cheapest; compliance check first)
2. ABL-v02-2 (DINOv3 tier; backbone choice anchors all training)
3. ABL-v02-3 (frozen vs unfreeze)
4. ABL-v02-7 (head training schedule)
5. ABL-v02-1 (NSA-removal; tests Memory mechanism)
6. ABL-v02-9 (NSA kernel decomposition; only if ABL-v02-1 positive)
7. ABL-v02-6 (selection-gate signal; only if ABL-v02-1 positive)
8. ABL-v02-5 (capability_match measurement)
9. ABL-v02-4 (best-of-N vs single-expert; depends on ABL-v02-5)
```

## Compute budget estimate addendum (v0.2 ABLs only)

```text
ABL-v02-1 NSA-removal              : ~80 GPU-hours
ABL-v02-2 DINOv3 backbone tier     : ~80 GPU-hours
ABL-v02-3 Frozen vs unfreeze       : ~100 GPU-hours
ABL-v02-4 Composer best-of-N       : ~400 GPU-hours
ABL-v02-5 Capability_match         : ~140 GPU-hours
ABL-v02-6 Selection-gate signal    : ~120 GPU-hours
ABL-v02-7 Head training schedule   : ~270 GPU-hours
ABL-v02-8 Frame-budget benchmark   : ~45 GPU-hours
ABL-v02-9 NSA kernel decomposition : ~2 GPU-hours
                                     -----------
Total (all 9 v0.2 ABLs)            : ~1237 GPU-hours
```

All numbers are `inferred` on TITAN RTX 24 GB. Per F-002, server-side per /hdd3/kykt26/ env. This is ABLATION-PHASE estimate only; downstream training (full v0.2 model from scratch) is NOT included and would be a separate budget entry.

v0.1 SPEC-002 §"Compute budget estimate (for future authorization)" carries an inferred v0.1 budget; v0.2 addendum's budget is ADDITIVE (running both v0.1 and v0.2 ABL suites would sum).

## Boundaries (v0.2 addendum delta + carry from v0.1)

v0.1's boundaries (per SPEC-002 §"Boundaries" line 705+) are carried unchanged. v0.2 addendum adds:

```text
B-v02-A.  v0.2 ablation addendum is a NEW file. SPEC-002 v0.1 body is
          NOT modified. v0.1 receives only Version history tail
          pointer (per DEC-20260506-003 + Surgical Edits + Honesty
          Override).

B-v02-B.  No ABL-v02-N is implicitly authorized by SPEC-005 alone.
          Each requires a separate DEC + per-step micro gates per F-002.

B-v02-C.  v0.2 ablation addendum does NOT introduce new main-claim
          pillars. Pillars A + D + E (supporting) + B + C (demoted)
          per DEC-20260506-002 are unchanged.

B-v02-D.  v0.2 ablation addendum does NOT re-introduce dropped
          candidates (VGGT, MapAnything, Kimi-KDA). Pool composition
          per SPEC-004 Delta 5 is fixed for v0.2 testing.

B-v02-E.  Capability_match values in COMPOSER_CAPABILITY_DESCRIPTORS
          are NOT silently updated by SPEC-005. ABL-v02-5 produces
          measurement results; updating the descriptors file requires
          a separate DEC.

B-v02-F.  Per-ABL review checklist subsections in SPEC-005 are
          informative for other-agent handoff. Modifying them in-place
          is NOT allowed; supersede via a v0.3 addendum + fresh DEC
          (Honesty Override; do not edit informative content silently).
```

B-v02-A..F are ADDITIVE on v0.1 boundaries.

## Linked artifacts (full list)

Decisions:

- DEC-20260506-003 (cycle 019 launch + this addendum scope lock; parent)
- DEC-20260506-002 (v0.2 architecture deltas locked; parent of parent)
- DEC-20260506-001 (mainline architecture-first)
- DEC-20260501-004 (Dream3R candidate-not-final)
- DEC-20260504-002 (no-all-in any single finalist)
- DEC-20260505-005 (cycle 015 Critic L3 pilot scope; G_run paused at S9
  done; reusable as anchor for ABL-v02-6 verification regime testing)

Specs:

- SPEC-20260506-002 (v0.1 ablation plan; substrate; NOT rewritten)
- SPEC-20260506-001 (v0.1 architecture)
- SPEC-20260506-003 (v0.1 comparator map; v0.2 addendum is post-019
  trajectory item 2)
- SPEC-20260506-004 (v0.2 architecture; six numbered deltas)
- SPEC-20260503-001 (Critic finalist; informs ABL-v02-6 verification
  signal interpretation)
- SPEC-20260503-002 (Memory finalist; informs ABL-v02-1 retrieval
  semantics)
- SPEC-20260503-003 (Permanence finalist; informs ABL-v02-6 permanence
  signal interpretation)
- SPEC-20260504-001 (Composer finalist; informs ABL-v02-4 + ABL-v02-5)

Planning artifacts:

- planning/COMPOSER_CAPABILITY_DESCRIPTORS.md (cycle 018 S2)
- planning/NSA_MEMORY_INTEGRATION_MEMO.md (cycle 018 S3)
- planning/DINOV3_C1_INTEGRATION_MEMO.md (cycle 018 S3)

Paradigm / contract:

- paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md (v2.1; route_regret defined)
- paradigm/RESEARCH_CODE_DISCIPLINE.md (rules 3 + 5)
- paradigm/ARCHITECTURE_MECHANISM_INTAKE.md (F1..F6 failure modes;
  used in ABL outcome interpretation)

Failure modes:

- F-001 (32 MB request-limit; this spec stays under ~700 lines)
- F-002 (server topology; all v0.2 ABL execution goes server-side)

Cycle log:

- cycles/CYCLE-20260506-004.md (cycle 019 log)

Future / pending v0.2 addenda (NOT cycle 019 scope; per DEC-003
post-019 trajectory):

- SPEC-20260506-003 v0.2 comparator map addendum (cycle 020 candidate)
- planning/DREAM3R_V02_CODE_STRUCTURE.md (cycle 021 candidate)
- planning/DREAM3R_V02_IMPLEMENTATION_ROADMAP.md (cycle 022 candidate)
- literature/PAPER_DRAFT_V1.md Section 3 + 6 update (cycle 023 candidate)

## Open questions

```text
Q-v02-1. Is ABL-v02-4 (best-of-N) the direct paper-claim D primary
         demonstration, or is a tighter sub-ablation needed (e.g.,
         Composer-with-fixed-policy vs Composer-with-learned-policy)?
         Currently the addendum frames ABL-v02-4 as direct D-falsification;
         a sub-ablation refinement may be added in v0.3.

Q-v02-2. Should ABL-v02-5 (capability_match measurement) be combined
         with ABL-v02-4 (best-of-N) into a single execution sweep,
         or kept separate? Combined execution amortizes setup cost
         but couples falsification semantics. Currently kept separate
         per dependency graph.

Q-v02-3. Is the ~1237 GPU-hours total budget realistic on a single
         TITAN RTX 24 GB box, or does it require multi-box server
         coordination per F-002? This is a server-resource-planning
         question; defer to execution-cycle launch DEC.

Q-v02-4. Should B7 (streaming-specific benchmark category) be added
         to v0.1 B1-B6? Currently v0.2 reuses B3 (long dynamic) for
         streaming testing; a dedicated streaming category may be
         cleaner for ABL-v02-1 + ABL-v02-8. Defer to v0.3.

Q-v02-5. The post-019 trajectory in DEC-003 enumerates cycles 020-025;
         is this ordering still optimal after seeing v0.2 ablation
         scope? Specifically: should ABL execution start before
         comparator map addendum (cycle 020) and code structure
         planning (cycle 021)? Currently order is markdown-first;
         user direction needed before any execution-cycle launches.
```

## Discipline notes

```text
- Surgical Edits (rule 3): this addendum is a NEW file. SPEC-002 v0.1
  body is NOT modified. v0.1 receives only Version history tail
  pointer. The 3 cycle 018 planning artifacts and SPEC-004 v0.2
  architecture are cited as existing artifacts; their content is
  not duplicated here. Same pattern as cycle 018's SPEC-001 ->
  SPEC-004 v0.2 architecture handling. Pre-existing markdown lint
  warnings on parent files NOT fixed in cycle 019.

- Honesty Override (rule 5): every ABL-v02-N carries an inline
  evidence label. NSA-removal is `speculative` (no 3R prior art);
  DINOv3 tier is `paper-derived`; frame budget is `inferred`;
  capability_match measurement is `inferred -> measured-if-executed`.
  Per-ABL review checklist subsections explicitly forbid in-place
  modification (B-v02-F); supersede via fresh DEC + v0.3 addendum.

- F-001 anti-32MB: this addendum stays under ~700 lines. SPEC-002
  v0.1 (~770 lines) is NOT re-Read in cycle 019; section anchors
  cited via Grep -n results from cycle 019 launch (B1-B6 line 537;
  Falsification summary line 630; Version history line 761).
  SPEC-001 / SPEC-004 already in context from cycle 018; no re-Read.

- F-002 server topology: cycle 019 is markdown only. All v0.2 ABL
  execution (when authorized in future cycles) goes server-side
  per F-002 rules (172.17.140.97 / kykt env / /hdd3/kykt26/).
  CUT3R / Test3R / MoGe-2 / DepthAnything-V2 checkpoint downloads
  require fresh G_download gates per per-ABL launch DEC.

- Hard rules from AGENT_MASTER_PROMPT.md section 6 (carried): no
  reproduction; no checkpoint download; no training; no KYKT
  navigation change; no frontend implementation; no thesis
  finalization; no retiring of any non-finalist track; no demo
  storyboard promotion past `draft`. All in force; this spec
  adds none and modifies none.

- DEC-20260501-004 candidate-not-final and DEC-20260504-002 no-all-in
  carried unchanged. v0.2 ablation addendum tests v0.2 architecture
  candidacy; it does NOT commit to v0.2 as the final thesis. v0.2
  main-claim narrowing to A+D from DEC-20260506-002 is the load-
  bearing pillar ordering; ABL-v02-1..9 falsification mapping does
  NOT re-promote demoted pillars (B / C) or reduce E to absent.

- Review surface for other agents: per user instruction 2026-05-06,
  every ABL-v02-N includes a review checklist subsection. The
  checklist is the explicit handoff hook; other agents (per user
  "其他agent审阅修改") use it to verify each ABL before execution-
  authorization recommendations or modifications. Modifications go
  via fresh DEC + v0.3 addendum (B-v02-F); no in-place edits.
```

## Version history

```text
v0.1 (SPEC-20260506-002)  2026-05-06
                          cycle 016 S3 deliverable. First ablation
                          plan for Dream3R v0.1 architecture. 10
                          ablations in 3 tiers. Falsification table
                          for each architectural claim. Benchmark
                          input categories B1-B6 defined. Dependency
                          graph specified. No training authorized.

v0.2 (SPEC-20260506-005)  2026-05-06
                          cycle 019 S2 deliverable; this file. Delta-
                          only addendum on v0.1. Nine v0.2 ablations
                          (ABL-v02-1..9) anchored to SPEC-004 v0.2
                          architecture deltas: NSA-removal / DINOv3
                          backbone tier / frozen vs unfreeze / Composer
                          best-of-N / capability_match measurement /
                          selection-gate signal subsetting / head
                          training schedule / frame-budget benchmark /
                          NSA kernel decomposition. Per-ABL review
                          checklist subsection added per user request
                          for other-agent handoff. v0.1 body NOT
                          modified (only Version history tail pointer
                          appended). Pillar tier placement: ABL-v02-1
                          + 4 + 6 in Tier 1 (load-bearing); 2 + 3 +
                          7 + 8 in Tier 2; 5 + 9 in Tier 3.
                          Falsification mapping table covers main-
                          claim A + D + E (supporting). Compute budget
                          estimate addendum: ~1237 GPU-hours total
                          across all 9 v0.2 ABLs (inferred on TITAN
                          RTX). No training authorized; markdown only.

v0.3 (SPEC-20260507-002)  2026-05-07
                          cycle 023 S3 deliverable. Delta-only addendum
                          on this v0.2 spec. Adds ABL-v02-10 (Test3R-
                          alone comparator; Tier 1; Q1 from comparator
                          map v0.2). Pillar A falsification coverage
                          map (RA-07 from cycle 022 Path C Agent B).
                          ABL-v02-4 VGGT offline-batch baseline
                          annotation (Q2 from comparator map v0.2).
                          v0.2 body NOT modified; see specs/SPEC-
                          20260507-002-dream3r-ablation-plan-v03-
                          addendum.md for full v0.3 addendum.
```
