# SPEC-20260506-003 Dream3R Comparator Map v0.1

## Identity

spec_id: SPEC-20260506-003

date: 2026-05-06

status: draft v0.1 (cycle 016 S4; markdown only; no reproduction, no benchmark runs)

cycle_of_origin: cycle 016

parent_spec: SPEC-20260506-001 (Dream3R architecture v0.1)

sibling_spec: SPEC-20260506-002 (Dream3R ablation plan v0.1)

## Purpose

This file is the full comparator map for Dream3R v0.1, expanding the lightweight quick map in the architecture spec (section "Comparator quick map"). It answers: "for each existing 3R model, what does Dream3R add, and what does the existing model already do that Dream3R reuses?"

The map also identifies which comparators are the most dangerous to Dream3R's novelty claim — models that already provide some of the control vocabulary Dream3R formalizes.

## Reading rule

```text
- "Has" means the comparator implements the capability (paper-proven
  or code-observed).
- "Partial" means the comparator has an implicit or limited version
  (inferred from paper description; not a formal mechanism).
- "None" means the comparator does not address the axis.
- "Dream3R adds" summarizes what v0.1 contributes beyond the
  comparator on that axis.
```

## Comparison axes

The map compares on 8 axes derived from the architecture spec:

```text
Axis 1: Perception substrate (what produces per-frame 3D output)
Axis 2: Memory / persistent state (whether state carries across frames)
Axis 3: Critic / verification (whether output is verified before commit)
Axis 4: Permanence / dynamic handling (whether dynamic content is separated)
Axis 5: Routing / model selection (whether inputs are matched to models)
Axis 6: Cross-module bus (whether modules communicate via explicit signals)
Axis 7: Conflict resolution rules (whether cross-module conflicts are governed)
Axis 8: Long-sequence scalability (O(N) vs O(N^2); practical frame limits)
```

---

## Full comparator table

### Group A: Per-pair / per-frame 3R (no persistent state)

#### DUSt3R (Wang et al. 2024)

```text
Axis 1 Perception    : transformer (CroCo-pretrained ViT; per-pair)
                        [paper-proven]
Axis 2 Memory        : none (per-pair; no state across pairs)
Axis 3 Critic        : none (single-pass; no verification)
Axis 4 Permanence    : none (static assumption; no dynamic handling)
Axis 5 Routing       : none (single model, single regime)
Axis 6 Bus           : none (no cross-module signals; monolithic)
Axis 7 CR-rules      : none
Axis 8 Scalability   : O(N^2) for global alignment post-hoc; practical
                        limit ~50-100 images with optimization

Dream3R adds         : Memory (A1-A3), Critic (A4-A5), Permanence (A6),
                        Composer (A5 routing), bus + CR-rules. Dream3R
                        reuses DUSt3R's perception substrate lineage as
                        the Perceiver core (C1).

Threat to Dream3R    : LOW. DUSt3R is the foundation, not a competitor.
                        Dream3R extends it; does not compete at the
                        same level.
```

#### MASt3R (Leroy et al. 2024)

```text
Axis 1 Perception    : transformer + matching head (per-pair, with
                        local feature matching) [paper-proven]
Axis 2 Memory        : none (per-pair)
Axis 3 Critic        : partial (MASt3R-SfM adds classical SfM
                        consistency checks post-hoc; not a learned
                        critic) [paper-proven for MASt3R-SfM variant]
Axis 4 Permanence    : none
Axis 5 Routing       : none
Axis 6 Bus           : none
Axis 7 CR-rules      : none
Axis 8 Scalability   : O(N^2) for pair graph; MASt3R-SfM adds SfM
                        pipeline for multi-view

Dream3R adds         : Memory, learned Critic (replacing classical SfM
                        verification), Permanence, Composer, bus +
                        CR-rules. MASt3R-SfM's classical verification
                        is the closest existing analog to Dream3R's
                        Critic A4, but it is post-hoc, not in-loop.

Threat to Dream3R    : LOW-MEDIUM. MASt3R-SfM's verification pipeline
                        covers some of A4's scope. Dream3R must show
                        that in-loop learned verification (A4) plus
                        repair actions (A5) outperform post-hoc SfM.
```

#### VGGT (Wang et al. 2025)

```text
Axis 1 Perception    : large transformer with explicit per-frame
                        pointmap, camera, and depth tokens (single
                        forward pass for N views) [paper-proven]
Axis 2 Memory        : none (single-pass over all views; no
                        persistent state; limited by context window)
Axis 3 Critic        : none (single-pass; no verification)
Axis 4 Permanence    : none
Axis 5 Routing       : none
Axis 6 Bus           : none (implicit cross-view attention in the
                        transformer; not a formal bus)
Axis 7 CR-rules      : none
Axis 8 Scalability   : O(N^2) attention over all views; practical
                        limit ~30-50 views in a single forward pass

Dream3R adds         : everything beyond perception. Dream3R can use
                        VGGT as an alternative Perceiver core (C1).
                        VGGT's single-pass, no-memory design is the
                        opposite of Dream3R's control-graph approach.

Threat to Dream3R    : MEDIUM. VGGT achieves strong results with a
                        very simple architecture (no memory, no critic,
                        no routing). If VGGT's single-pass results
                        generalize to long sequences and dynamic scenes,
                        Dream3R's additional complexity is hard to
                        justify. The key test: does VGGT degrade on
                        100+ frame sequences (where Memory matters) and
                        dynamic scenes (where Permanence matters)?
```

#### Fast3R (2025)

```text
Axis 1 Perception    : transformer with efficient multi-view attention
                        [paper-proven]
Axis 2 Memory        : none
Axis 3 Critic        : none
Axis 4 Permanence    : none
Axis 5 Routing       : none
Axis 6 Bus           : none
Axis 7 CR-rules      : none
Axis 8 Scalability   : better than DUSt3R/MASt3R for many-view
                        (linear-time multi-view attention); still
                        bounded by context window

Dream3R adds         : Memory, Critic, Permanence, Composer, bus +
                        CR-rules. Fast3R's efficient attention could
                        be adopted inside Dream3R's Perceiver core.

Threat to Dream3R    : LOW. Fast3R solves a different problem
                        (efficient multi-view attention) at the
                        perception level.
```

### Group B: Sequential / streaming 3R (persistent state)

#### Spann3R (2024)

```text
Axis 1 Perception    : transformer (DUSt3R lineage) [paper-proven]
Axis 2 Memory        : HAS persistent spatial memory (paper-proven);
                        learned memory encoder/decoder; anchor-based
                        retrieval
Axis 3 Critic        : none
Axis 4 Permanence    : none (static assumption)
Axis 5 Routing       : none
Axis 6 Bus           : none (memory is internal; no cross-module signals)
Axis 7 CR-rules      : none
Axis 8 Scalability   : O(N) streaming (memory state is fixed-size);
                        practical limit tested up to hundreds of frames

Dream3R adds         : Critic (A4-A5), Permanence (A6), Composer
                        (A5 routing), bus + CR-rules. Spann3R's memory
                        is the closest existing analog to Dream3R's
                        Memory module (C2). Dream3R adds A1 update-kind
                        classifier (Spann3R uses a single update mode)
                        and A3 anchor budgeting policy.

Threat to Dream3R    : MEDIUM-HIGH. Spann3R already has persistent
                        memory. Dream3R must show that A1 update
                        control + A3 anchor budgeting + bus integration
                        with other modules outperform Spann3R's simpler
                        memory design. If Spann3R's memory is "good
                        enough," Memory-as-controller loses its
                        justification.
```

#### CUT3R (2025)

```text
Axis 1 Perception    : transformer (DUSt3R lineage) [paper-proven]
Axis 2 Memory        : HAS persistent state (paper-proven); full update
                        per frame; unidirectional causal processing
Axis 3 Critic        : none
Axis 4 Permanence    : none (static assumption)
Axis 5 Routing       : none
Axis 6 Bus           : none
Axis 7 CR-rules      : none
Axis 8 Scalability   : O(N) causal (state updates per frame); tested
                        on long sequences

Dream3R adds         : Critic, Permanence, Composer, bus + CR-rules,
                        and A1 multi-mode update control (CUT3R uses
                        full_update only). The A1 update_kind classifier
                        is Dream3R's differentiation from CUT3R on the
                        memory axis.

Threat to Dream3R    : MEDIUM. CUT3R's simple full-update memory works
                        well. Dream3R's A1 multi-mode update must
                        demonstrably outperform CUT3R's single-mode on
                        sequences with mixed dynamics.
```

#### STream3R (2025)

```text
Axis 1 Perception    : causal transformer [paper-proven]
Axis 2 Memory        : HAS sequential state (paper-proven); causal
                        attention over frame history
Axis 3 Critic        : none
Axis 4 Permanence    : none
Axis 5 Routing       : none
Axis 6 Bus           : none
Axis 7 CR-rules      : none
Axis 8 Scalability   : O(N) via causal design; efficient for streaming

Dream3R adds         : same as CUT3R entry. STream3R and CUT3R are
                        both single-mode sequential memory systems.

Threat to Dream3R    : MEDIUM (same threat profile as CUT3R).
```

#### LONG3R / LongStream / LoGeR (2025-2026)

```text
Axis 1 Perception    : transformer [paper-proven]
Axis 2 Memory        : HAS long-range state management (paper-proven);
                        various mechanisms for very long sequences
                        (LONG3R: compression; LongStream: hierarchical;
                        LoGeR: local-global retrieval)
Axis 3 Critic        : none
Axis 4 Permanence    : none
Axis 5 Routing       : none
Axis 6 Bus           : none
Axis 7 CR-rules      : none
Axis 8 Scalability   : O(N) with long-range mechanisms; tested on
                        1000+ frame sequences

Dream3R adds         : Critic, Permanence, Composer, bus + CR-rules.
                        Memory A3 anchor budgeting addresses the same
                        problem these models solve (which frames to
                        keep in long sequences) but with an
                        evidence-driven policy rather than a fixed
                        strategy.

Threat to Dream3R    : MEDIUM-HIGH. These models solve the long-
                        sequence problem without a control graph.
                        Dream3R must show that its control-graph
                        approach (evidence-driven anchor budgeting
                        via A3) outperforms their fixed strategies.
```

### Group C: Verification / consistency models

#### Test3R (Naver 2025)

```text
Axis 1 Perception    : transformer (DUSt3R lineage) [paper-proven]
Axis 2 Memory        : none
Axis 3 Critic        : HAS test-time consistency verification
                        (paper-proven); verifier head checks output
                        quality and triggers re-inference
Axis 4 Permanence    : none
Axis 5 Routing       : none
Axis 6 Bus           : none (verification is monolithic; no cross-
                        module signals)
Axis 7 CR-rules      : none
Axis 8 Scalability   : per-pair/few-view; not streaming

Dream3R adds         : Memory, Permanence, Composer, bus + CR-rules.
                        Dream3R's Critic (C4) is the direct descendant
                        of Test3R's verifier head. Dream3R adds the
                        A5 repair-facet action set (Test3R only
                        re-runs; Dream3R can reroute, open anchor
                        budget, or request prior).

Threat to Dream3R    : MEDIUM. Test3R proves that verification helps
                        in 3R. Dream3R's Critic must show that the
                        ADDITIONAL repair actions (beyond simple
                        re-run) provide measurable benefit. If
                        simple re-run is sufficient, Dream3R's A5
                        action set is over-engineered.
```

#### TTT3R / test-time training variants (2025)

```text
Axis 1 Perception    : transformer with test-time adaptation [paper-proven]
Axis 2 Memory        : partial (TTT3R maintains adaptation state)
Axis 3 Critic        : partial (trigger mechanism decides when to adapt)
Axis 4 Permanence    : none
Axis 5 Routing       : none
Axis 6 Bus           : none
Axis 7 CR-rules      : none
Axis 8 Scalability   : per-input; adaptation cost per input

Dream3R adds         : formal Critic with multi-action A5 (TTT3R
                        triggers adaptation; Dream3R triggers repair,
                        reroute, or anchor budget expansion); Memory
                        controller; Permanence; Composer; bus.

Threat to Dream3R    : LOW-MEDIUM. TTT3R's test-time adaptation is
                        orthogonal to Dream3R's architecture. Could
                        be adopted as a repair action inside Critic A5.
```

### Group D: Dynamic-aware 3R

#### MonST3R (2024-2025)

```text
Axis 1 Perception    : transformer + dynamic mask head [paper-proven]
Axis 2 Memory        : none (per-pair/few-view)
Axis 3 Critic        : none
Axis 4 Permanence    : HAS per-frame dynamic/static split (paper-proven);
                        motion-aware pointmap; dynamic mask head
Axis 5 Routing       : none
Axis 6 Bus           : none
Axis 7 CR-rules      : none
Axis 8 Scalability   : per-pair; not streaming

Dream3R adds         : Memory, Critic, Composer, bus + CR-rules.
                        Permanence (C3) inherits MonST3R's per-frame
                        dynamic split as its substrate ancestor.
                        Dream3R adds object_track_set (persistent
                        object identity across frames) and the
                        suppress_static_write handoff to Memory (CR-2).

Threat to Dream3R    : MEDIUM. MonST3R already does the dynamic split.
                        Dream3R's Permanence must show that
                        object_track_set (persistent identity) and
                        CR-2 (suppress handoff to Memory) provide
                        measurable benefit beyond per-frame split.
```

#### POMATO / D^2USt3R / Easi3R / RayMap3R (2025)

```text
Axis 1 Perception    : transformer variants [paper-proven]
Axis 2 Memory        : none or minimal
Axis 3 Critic        : none
Axis 4 Permanence    : HAS per-frame dynamic handling (paper-proven);
                        various approaches to motion-aware reconstruction
Axis 5 Routing       : none
Axis 6 Bus           : none
Axis 7 CR-rules      : none
Axis 8 Scalability   : per-pair or few-view

Dream3R adds         : same differentiation as MonST3R entry.
                        Dream3R's persistent object identity
                        (object_track_set) is the key addition over
                        all Group D models.

Threat to Dream3R    : MEDIUM (same profile as MonST3R).
```

### Group E: SSM-based / Mamba-based 3R

#### Mamba-3R variants (2025-2026)

```text
Axis 1 Perception    : SSM / Mamba-based encoder [paper-proven for
                        some variants; emerging]
Axis 2 Memory        : HAS SSM state (implicit in the SSM architecture)
Axis 3 Critic        : none
Axis 4 Permanence    : none
Axis 5 Routing       : none
Axis 6 Bus           : none
Axis 7 CR-rules      : none
Axis 8 Scalability   : O(N) by design; SSM is inherently streaming

Dream3R adds         : Critic, Permanence, Composer, bus + CR-rules.
                        Dream3R's v0.1 substrate hypothesis uses SSM
                        for Memory (C2) but transformer for Perception
                        (C1). A pure SSM model uses SSM for both.
                        ABL-2c in the ablation plan tests whether
                        SSM-for-perception matches transformer-for-
                        perception.

Threat to Dream3R    : MEDIUM. If a pure SSM stack matches the hybrid
                        on all axes, Dream3R's substrate hypothesis
                        (transformer perception + SSM memory) is
                        falsified at the substrate level.
```

### Group F: Multi-model / composition approaches

#### SLAM3R (2025)

```text
Axis 1 Perception    : transformer [paper-proven]
Axis 2 Memory        : partial (SLAM-style state management)
Axis 3 Critic        : partial (SLAM-style consistency checks)
Axis 4 Permanence    : partial (SLAM handles dynamic objects implicitly)
Axis 5 Routing       : none (single model)
Axis 6 Bus           : none (SLAM pipeline is monolithic)
Axis 7 CR-rules      : none
Axis 8 Scalability   : real-time streaming (SLAM heritage)

Dream3R adds         : formal modular decomposition (SLAM3R is
                        monolithic); Composer routing; explicit
                        bus + CR-rules. SLAM3R has implicit versions
                        of Memory + Critic + Permanence inside a
                        monolithic pipeline. Dream3R makes these
                        explicit and composable.

Threat to Dream3R    : MEDIUM. SLAM3R shows that a monolithic system
                        can integrate memory + verification + dynamics.
                        Dream3R must show that EXPLICIT modular
                        decomposition (bus + gates) outperforms
                        IMPLICIT monolithic integration.
```

#### MapAnything (2025)

```text
Axis 1 Perception    : transformer [paper-proven]
Axis 2 Memory        : HAS learned latent state [paper-proven]
Axis 3 Critic        : none
Axis 4 Permanence    : none
Axis 5 Routing       : none
Axis 6 Bus           : none
Axis 7 CR-rules      : none
Axis 8 Scalability   : varies

Dream3R adds         : Critic, Permanence, Composer, bus + CR-rules.

Threat to Dream3R    : LOW.
```

### Group G: Gaussian / asset-path models (excluded from v0.1 scope)

#### Splatt3R / InstantSplat / NoPoSplat / 4DGS variants

```text
These models produce Gaussian splat or 4DGS assets from 3R outputs.
They are CONSUMERS of 3R, not competitors. Dream3R routes inputs to
these via Composer but does not compete with them on the asset-path
axis (excluded per Permanence spec 4DGS boundary).

Threat to Dream3R    : NONE (different layer of the stack).
```

---

## Threat ranking

Models ranked by threat to Dream3R's novelty claim:

```text
HIGH THREAT (closest to Dream3R's claims):
  1. Spann3R           — already has persistent memory; Dream3R's
                         Memory module must demonstrably exceed it
  2. LONG3R/LongStream/LoGeR — solve long-sequence without control
                         graph; threaten the "control graph is needed"
                         claim
  3. VGGT              — achieves strong results with minimal
                         architecture; threatens "complexity is
                         justified"

MEDIUM THREAT (overlap on one axis):
  4. CUT3R/STream3R    — persistent state, simpler than Dream3R's
                         Memory
  5. Test3R            — verification head; Dream3R's Critic must
                         outperform simple re-run
  6. MonST3R           — dynamic split; Dream3R's Permanence must
                         add to per-frame split
  7. SLAM3R            — monolithic integration; Dream3R must show
                         modular > monolithic
  8. Mamba-3R          — SSM-only; substrate hypothesis test

LOW THREAT (foundation models, not competitors):
  9. DUSt3R            — foundation; Dream3R builds on it
  10. MASt3R           — foundation + matching
  11. Fast3R           — efficient attention (orthogonal)
  12. TTT3R            — test-time adaptation (orthogonal)
  13. MapAnything      — different application domain
  14. Gaussian/4DGS    — different stack layer
```

## What Dream3R must prove against each threat tier

```text
Against HIGH THREAT models:
  The bus + CR-rules + multi-module control graph provides
  measurable benefit over single-mechanism persistence (Spann3R),
  single-mechanism compression (LONG3R), or brute-force attention
  (VGGT). The key experiments are:
  - ABL-1 (bus removal): full Dream3R vs. flat baseline must show
    bus value
  - ABL-5 (Memory removal): Dream3R with Memory vs. Dream3R
    without Memory, compared against Spann3R baseline
  - Direct benchmark comparison on long sequences: Dream3R vs.
    LONG3R / LongStream / LoGeR on 500+ frame sequences

Against MEDIUM THREAT models:
  Each Dream3R module must outperform the comparator's partial
  version of the same capability:
  - Critic A4+A5 vs. Test3R re-run (P1 conflict detection +
    downstream quality improvement)
  - Permanence A6 vs. MonST3R dynamic split (P4 dynamic pollution +
    object identity consistency)
  - Memory A1 multi-mode vs. CUT3R full-update (P2 anchor retention
    + P3 memory growth on mixed sequences)
  - Bus + modules vs. SLAM3R monolithic (interpretability +
    per-module falsifiability)

Against LOW THREAT models:
  No direct comparison needed. These models are foundations or
  orthogonal tools. Dream3R should demonstrate that it reuses
  their strengths (perception substrate, efficient attention,
  test-time adaptation) rather than replacing them.
```

## Axes where Dream3R has NO existing comparator

```text
The following Dream3R features have NO close comparator in the
existing 3R literature:

1. Cross-spec memory bus as explicit typed tensor schema
   Closest analog: blackboard architectures (classical AI), but
   not applied to 3R.

2. CR-rules as architectural gates
   No 3R model has formal conflict resolution rules between
   modules. Closest: implicit conventions in SLAM pipelines.

3. Composer with route_regret falsification axis
   No 3R model routes inputs to different 3R models by regime.
   Closest: MoE routing in LM/vision (different domain).

4. A5 repair-facet action set (beyond re-run)
   Test3R re-runs; Dream3R additionally reroutes, opens anchor
   budget, or requests prior. No 3R model has this action set.

5. Object_track_set with persistent identity across frames
   MonST3R does per-frame dynamic split; no 3R model maintains
   a persistent object identity set across a long sequence.

These are the architecture-novel elements (per SPEC-20260506-001
evidence label: architecture-novel). They carry the highest paper
novelty but also the highest risk: they are untested by definition.
```

## Relationship to ablation plan

```text
The comparator map and ablation plan are designed together:

- ABL-1 (bus removal) targets axis 6+7 (bus + CR-rules), where
  Dream3R has NO comparator. If ABL-1 fails, the "no comparator"
  claim is irrelevant.

- ABL-4 (Critic removal) should be benchmarked AGAINST Test3R
  (Group C comparator) to show that Dream3R's Critic adds value
  beyond Test3R's verifier.

- ABL-5 (Memory removal) should be benchmarked AGAINST Spann3R /
  CUT3R (Group B comparators) to show Memory-as-controller exceeds
  memory-as-state.

- ABL-6 (Permanence removal) should be benchmarked AGAINST MonST3R
  (Group D comparator) to show Permanence adds to per-frame split.

- ABL-7 (Composer removal) has no direct 3R comparator (Group F is
  sparse). The benchmark is Dream3R with single model vs. Dream3R
  with Composer routing, measured by P5 route regret.
```

## Boundaries

```text
1. NO REPRODUCTION. This file describes comparators from published
   papers. No comparator model is run, downloaded, or benchmarked.

2. NO PERFORMANCE CLAIMS. All comparator capabilities are described
   from paper claims, not from measured reproduction.

3. NO RANKING. The threat ranking is about novelty overlap, not
   performance ordering. Dream3R v0.1 has no measured performance.

4. SCOPE: 3R models only. General vision models, LLMs, and robotics
   systems are out of scope except as cross-domain analogs.
```

## Linked artifacts

- SPEC-20260506-001 (Dream3R architecture v0.1; comparator quick map section; module lineage fields)
- SPEC-20260506-002 (Dream3R ablation plan v0.1; ablation-to-comparator mapping)
- planning/BRANCH_COMPARISON_MATRIX.md (cycle 004 branch comparison; predecessor to this map)
- sources/FRONTIER_SOURCE_MAP.md (full source inventory; paper-level detail)
- literature/SPINE_CRITIC.md, SPINE_MEMORY.md, SPINE_PERMANENCE.md, SPINE_COMPOSER.md (per-finalist reading guides)
- literature/PAPER_RELATED_WORK_SKELETON.md (paper related work; informed by this map)

## Version history

```text
v0.1  2026-05-06  cycle 016 S4 deliverable. First full comparator map
                  for Dream3R v0.1 architecture. 14+ comparator models
                  across 7 groups. Threat ranking by novelty overlap.
                  Per-axis comparison (8 axes). Architecture-novel
                  elements with no comparator identified. Ablation
                  plan cross-referenced. No reproduction; no benchmark
                  runs.

v0.2  2026-05-07  cycle 021 S3 pointer entry. v0.2 delta addendum
                  lives in NEW file specs/SPEC-20260507-001-dream3r-
                  comparator-map-v02.md per Discipline rule 5 NEW-file
                  pattern (this v0.1 body NOT modified). v0.2 addendum:
                  reorganizes 16-entry pool into 5 tiers (in-pool 7 /
                  out-of-pool 3 / out-of-scope 1 / foundation 1 /
                  orthogonal 8) per SPEC-004 Delta 5; adds 3 NEW axes
                  (Axis 9 NSA / Axis 10 DINOv3 / Axis 11 Composer pool)
                  per Deltas 2-5; re-ranks threats against pillar A +
                  D narrowing per DEC-20260506-002. v0.1 → v0.2
                  traceability matrix preserved. See SPEC-20260507-
                  001 for full delta content.
```
