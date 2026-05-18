# Dream3R v0.2 comparator map addendum

artifact_id: specs/SPEC-20260507-001-dream3r-comparator-map-v02.md

date: 2026-05-07

cycle: 021 (S3 deliverable per DEC-20260507-001)

status: v0.2 comparator map delta-only addendum on SPEC-20260506-003 v0.1 (markdown only; NEW file; v0.1 body preserved unchanged per Discipline rule 5)

honesty_label: every comparator reclassification carries an inline evidence label. In-pool admission of 7 experts is `paper-known per expert + engineering-judgment per pool composition` (per DEC-20260506-002 + COMPOSER_CAPABILITY_DESCRIPTORS). Out-of-pool drops are `user-decided per DEC-20260506-002` for VGGT / MapAnything / Kimi-KDA. Threat ranking changes are `agent-decided` based on v0.2 main-claim narrowing to A + D. New axes (NSA / DINOv3 / Composer pool) inherit evidence labels from the underlying v0.2 deltas: NSA `speculative for 3R transfer`; DINOv3 `paper-derived`; Composer pool `paper-known per expert`.

linked_artifacts:

- decisions/DEC-20260507-001-cycle-021-launch-comparator-map-v02-and-path-c-review-activation.md (parent)
- decisions/DEC-20260506-002-cycle-018-launch-v02-architecture.md (v0.2 architecture deltas locked; out-of-pool drops authorized)
- specs/SPEC-20260506-003-dream3r-comparator-map.md (v0.1 substrate; preserved unchanged; cited by section + line anchor)
- specs/SPEC-20260506-004-dream3r-architecture-v02.md (v0.2 architecture; six deltas inform reorganization)
- specs/SPEC-20260506-005-dream3r-ablation-plan-v02.md (v0.2 ablation plan; ABL-v02-1..9 inform "what Dream3R must prove" mapping)
- planning/COMPOSER_CAPABILITY_DESCRIPTORS.md (cycle 018 S2; 7 admitted experts inform in-pool tier)
- planning/NSA_MEMORY_INTEGRATION_MEMO.md (cycle 018 S3; informs Axis 9 NSA-style sparse attention dimension)
- planning/DINOV3_C1_INTEGRATION_MEMO.md (cycle 018 S3; informs Axis 10 DINOv3 backbone tier dimension)

## Identity

This artifact is the v0.2 delta addendum to the v0.1 comparator map (`specs/SPEC-20260506-003-dream3r-comparator-map.md`, 625 lines, written cycle 016 S4). It does NOT replace v0.1; v0.1 remains the substrate document. This addendum carries only what changes under v0.2:

- Reorganization of the comparator pool into in-pool / out-of-pool / out-of-scope / foundation / orthogonal tiers per SPEC-20260506-004 Delta 5 (Composer pool admits 7 lightweight experts).
- Three NEW comparison axes introduced by v0.2 deltas (NSA / DINOv3 / Composer pool composition).
- Updated threat ranking against narrowed main-claim A (Verification-as-architecture) + D (Heterogeneous best-of-N Composer); pillar B (state-ownership) demoted to discipline; pillar C (reservation tokens A7/A8) demoted to future work; pillar E (Identity-anchored memory) supporting only.
- Architecture-novel elements with no comparator (carry from v0.1; add v0.2-introduced novelty: per-file/per-task review checklist pattern noted; review-pattern claim NOT promoted to architecture novelty per DEC-20260507-001 §"Open questions Q3").
- v0.1 → v0.2 traceability matrix.

## Approval

Approved scope: per `DEC-20260507-001` (cycle 021 launch + comparator map v0.2 addendum + Path C review activation; user-decided 2026-05-07 with "请你推进吧，我们也该开始全面落实了"). Approved closure of v0.2 markdown trio (architecture SPEC-004 + ablation plan SPEC-005 + comparator map this file).

NOT approved by this artifact:

- code execution; this is planning + comparison documentation only.
- modification of `specs/SPEC-20260506-003-dream3r-comparator-map.md` v0.1 body (preserved unchanged; only v0.1 Version history tail receives a v0.2 pointer entry).
- training, GPU runs, checkpoint download (gated per F-002).
- promotion of any in-pool expert to "approved-for-checkpoint-download" or "approved-for-execution".
- KYKT navigation change, frontend implementation, demo storyboard promotion past `draft`.
- finalization of Dream3R candidacy.
- retiring of any comparator entry from v0.1 (out-of-pool tier preserves all v0.1 entries with explicit reclassification reason).

## Scope of v0.2 comparator map addendum

```text
markdown only
candidate-not-final (DEC-20260501-004)
no-all-in (DEC-20260504-002)
architecture-first mainline (DEC-20260506-001)
v0.2 architecture deltas locked (DEC-20260506-002)
v0.2 ablation deltas locked (DEC-20260506-003)
v0.2 code structure planned (DEC-20260506-004 S2)
v0.2 implementation roadmap planned (DEC-20260506-004 S3)
v0.2 comparator map: this file (DEC-20260507-001 S3)
```

This file documents v0.2 comparator-pool reorganization + threat ranking under narrowed main-claim. It does NOT prescribe any new ABL or evaluation. ABL-v02-N execution gating per SPEC-005 unchanged.

## Reading order

```text
1. Read this file (you are here).
2. Read DEC-20260507-001 (parent decision).
3. Read SPEC-20260506-003 v0.1 comparator map (substrate; full file
   on first read; cite by line anchor thereafter — 625 lines).
4. Read SPEC-20260506-004 v0.2 architecture (six deltas drive
   reorganization).
5. Read SPEC-20260506-005 v0.2 ablation plan (ABL-v02-1..9 map
   to "what Dream3R must prove" tier).
6. Reference COMPOSER_CAPABILITY_DESCRIPTORS for per-expert detail
   on the 7 in-pool admitted experts.
```

## v0.2 architecture deltas affecting comparator map (recall from SPEC-004)

```text
Delta 1: Frame budget 30-50 ms/frame at 30 FPS streaming-first
         (changes practical scalability axis evaluation but does
          not reorganize the pool).
Delta 2: C1 Perceiver backbone ViT-L -> DINOv3-S; -B fallback;
         heads from scratch.
         -> introduces Axis 10 (DINOv3 backbone tier dimension);
            ViT-L moves to out-of-scope tier.
Delta 3: C2 Memory bounded anchor bank + NSA-style selective
         retrieval (A+B pattern; selection gate driven by Critic
         confidence + Permanence link).
         -> introduces Axis 9 (NSA-style sparse attention
            dimension).
Delta 4: NSA-style sparse attention as architectural optimization
         (engineering, not paper main claim).
         -> shared with Delta 3 axis; engineering-judgment label.
Delta 5: Composer pool admits 7 lightweight experts (MASt3R /
         Fast3R / Spann3R / CUT3R / MoGe-2 / DepthAnything-V2 /
         Test3R); drop VGGT, MapAnything (too heavy); drop
         Kimi Linear / KDA (LM-to-3R transfer not pursued).
         -> introduces Axis 11 (Composer expert pool composition
            dimension); drives top-level pool reorganization.
Delta 6: Main-claim narrowing to A (Verification-as-architecture)
         + D (Heterogeneous best-of-N Composer) as pillars; E
         (Identity-anchored memory) supporting; B (state-
         ownership) + C (reservation tokens A7/A8) demoted.
         -> drives threat ranking re-evaluation (some MEDIUM
            v0.1 threats become LOW under A+D; some LOW become
            MEDIUM if they threaten pillar D specifically).
```

## v0.1 comparator map relationship

`SPEC-20260506-003-dream3r-comparator-map.md` v0.1 (cycle 016 S4) is the substrate. Cited content:

- Section "Comparison axes" (line 35): defines 8 axes (Perception / Memory / Critic / Permanence / Routing / Bus / CR-rules / Scalability). v0.2 inherits all 8; adds 3 NEW (Axis 9 / 10 / 11; see below).
- Section "Full comparator table" (line 52): defines 16 comparator entries grouped by capability. v0.2 inherits all 16 entries with their per-axis content; reorganizes into 5 tiers (in-pool / out-of-pool / out-of-scope / foundation / orthogonal). v0.1 entries are NOT modified; only their pool classification changes.
- Section "Threat ranking" (line 465): v0.1 ranking (HIGH: Spann3R, LONG3R/LongStream/LoGeR, VGGT; MEDIUM: CUT3R/STream3R, Test3R, MonST3R, SLAM3R, Mamba-3R; LOW: DUSt3R, MASt3R, Fast3R, TTT3R, MapAnything, Gaussian/4DGS). v0.2 re-ranks against narrowed main-claim A + D; see "Updated threat ranking" below.
- Section "What Dream3R must prove against each threat tier" (line 500): v0.1 anchored to ABL-1..10 from SPEC-002 v0.1. v0.2 re-anchors HIGH-threat experiments to ABL-v02-N from SPEC-005.
- Section "Axes where Dream3R has NO existing comparator" (line 534): v0.1 listed bus + CR-rules + control-graph composition. v0.2 carries these forward; adds nothing new (per DEC-20260507-001 §"Open questions Q3" review-pattern is workflow contribution, not architecture novelty).
- Section "Relationship to ablation plan" (line 565): v0.1 anchored to SPEC-002 v0.1 ABL-1..10. v0.2 re-anchors to SPEC-005 ABL-v02-1..9.

v0.1 body is NOT modified. Only `specs/SPEC-20260506-003-dream3r-comparator-map.md` Version history tail receives a v0.2 pointer entry (sync-chain task, see Discipline notes).

## Reorganized comparator pool (per Delta 5 + Delta 6)

The v0.1 comparator pool of 16 entries is reorganized into 5 tiers. v0.1 entries are preserved without modification; only their tier classification is changed. Each entry is labeled with its v0.1 group ID (Group A / B / C / D from v0.1 line 54+) for traceability.

### Tier 1: In-pool — 7 admitted lightweight experts (per Delta 5)

These experts comprise the Composer C5 pool that v0.2 main-claim D rests on. Per `COMPOSER_CAPABILITY_DESCRIPTORS.md`, each is admitted on capability-card grounds (innovation point + capability_match coverage + cost normalization).

```text
Expert 1: MASt3R (v0.1 Group A; line 80)
  Role in pool: best-of-N for static pair geometry; matching-head
  precision; cost mid-range; capability_match excels on static-
  collection regime (per COMPOSER_CAPABILITY_DESCRIPTORS).
  Reclassification: v0.1 LOW threat -> v0.2 in-pool (capability
  source, not threat). Threat against pillar D itself is now
  internal: does Dream3R's best-of-N over the pool genuinely
  outperform a single MASt3R run? See ABL-v02-4.
  Evidence label: paper-known + capability-card derived.

Expert 2: Fast3R (v0.1 Group A; line 140)
  Role in pool: best-of-N for many-view efficient attention;
  better Axis 8 scalability than DUSt3R/MASt3R; cost low;
  capability_match excels on dense multi-view regime.
  Reclassification: v0.1 LOW threat -> v0.2 in-pool. Same
  internal-threat framing as MASt3R.
  Evidence label: paper-known + capability-card derived.

Expert 3: Spann3R (v0.1 Group B; line 166)
  Role in pool: best-of-N for streaming with built-in memory;
  capability_match excels on streaming regime; persistent state
  inside expert (does NOT replace Dream3R Memory C2; the expert's
  internal state is upstream of bus signals).
  Reclassification: v0.1 HIGH threat -> v0.2 in-pool (most
  significant reclassification in the addendum). Rationale: under
  v0.2 main-claim narrowing, Spann3R is no longer a "single-
  mechanism persistence" threat to Dream3R's Memory; it becomes a
  capability source. The threat to pillar D persists in a
  different form: Dream3R must demonstrate that best-of-N
  routing + Spann3R's strengths beats Spann3R alone (ABL-v02-4).
  Threat to pillar A (Verification): orthogonal — Spann3R has no
  built-in verification head, so does not threaten A.
  Evidence label: paper-known + capability-card derived; Axis 11
  inclusion engineering-judgment.

Expert 4: CUT3R (v0.1 Group B; line 197)
  Role in pool: best-of-N for streaming with simpler full-update
  memory; cost low; capability_match excels on dynamic-tolerant
  streaming regime.
  Reclassification: v0.1 MEDIUM threat -> v0.2 in-pool. Threat
  to pillar D persists internally (ABL-v02-4 covers).
  Evidence label: paper-known + capability-card derived.

Expert 5: MoGe-2 (NEW in v0.2; not in v0.1 entry list)
  Role in pool: monocular depth specialist; pole-position on
  single-view per-frame depth quality; admitted to provide
  monocular regime coverage that the multi-view experts lack.
  Reclassification: NEW pool admission per Delta 5 (engineering-
  judgment per DEC-20260506-002).
  Evidence label: paper-known per MoGe paper; pool admission
  engineering-judgment.

Expert 6: DepthAnything-V2 (NEW in v0.2; not in v0.1 entry list)
  Role in pool: depth-foundation specialist; broad-coverage
  monocular depth; admitted as a second monocular regime expert
  with different tradeoffs from MoGe-2 (per
  COMPOSER_CAPABILITY_DESCRIPTORS).
  Reclassification: NEW pool admission per Delta 5.
  Evidence label: paper-known per DepthAnything-V2 paper; pool
  admission engineering-judgment.

Expert 7: Test3R (v0.1 Group D; line 274)
  Role in pool: verification-aware best-of-N candidate; expert
  whose internal verifier head OUTPUT can be cross-checked with
  Dream3R's Critic (A4); admitted for verification-regime
  coverage.
  Reclassification: v0.1 MEDIUM threat -> v0.2 in-pool, but
  with caveat. Threat to pillar A (Verification-as-architecture)
  PERSISTS: if Test3R's built-in verifier already provides
  sufficient verification, Dream3R's Critic A4 must demonstrably
  outperform "use Test3R alone with its verifier". This is
  ABL-v02-1 (NSA-removal) sibling concern: pillar A robustness.
  Evidence label: paper-known + capability-card derived; threat-
  persistence agent-decided.
```

In-pool ABL anchoring: ABL-v02-4 (Composer best-of-N vs single-expert; Tier 1 load-bearing) covers the internal pool-vs-single-expert comparison; ABL-v02-5 (capability_match measurement; Tier 3) advances inferred → measured for the 7-expert capability_match values.

### Tier 2: Out-of-pool — explicit drops with reason (per Delta 5 + DEC-002)

These v0.1 entries are NOT in the v0.2 expert pool. v0.1 entries preserved unchanged; only pool-tier classification is changed. Each drop has an explicit reason.

```text
Drop 1: VGGT (v0.1 Group A; line 108)
  v0.1 threat: HIGH ("achieves strong results with minimal
                     architecture; threatens 'complexity is
                     justified'").
  v0.2 reclassification: out-of-pool (too heavy per
                         DEC-20260506-002).
  Reason: VGGT's compute cost is incompatible with v0.2 frame
  budget (30-50 ms/frame at 30 FPS streaming-first; Delta 1).
  Per DEC-002, "drop VGGT (too heavy)" is user-decided.
  Threat to v0.2: REDUCED. Under v0.2 streaming-first framing,
  VGGT cannot meet frame budget, so does NOT threaten Dream3R's
  streaming-regime claims directly. Threat persists indirectly
  on offline-batch quality benchmarks (B1-B6 from SPEC-002 v0.1
  carried into SPEC-005); see "Updated threat ranking" below.
  Evidence label: user-decided (DEC-002).

Drop 2: MapAnything (v0.1 Group D; line 433)
  v0.1 threat: LOW ("different application domain").
  v0.2 reclassification: out-of-pool (too heavy per DEC-002).
  Reason: MapAnything's compute cost incompatible with frame
  budget (Delta 1). Per DEC-002, dropped together with VGGT.
  Threat to v0.2: REMAINS LOW (different application; not a
  streaming-3R competitor).
  Evidence label: user-decided (DEC-002).

Drop 3: Kimi Linear / KDA / attention-residual route (NOT in
        v0.1 entry list; surfaced in cycle 018 dialog)
  v0.1 threat: not catalogued in v0.1 (SPEC-003 v0.1 was written
               cycle 016; Kimi-KDA route surfaced cycle 018
               dialog).
  v0.2 reclassification: out-of-pool (LM-to-3R transfer not
                         pursued per DEC-002).
  Reason: Kimi Linear / KDA / attention-residual approaches are
  language-model-derived efficient-attention schemes whose
  transfer to 3R streaming is speculative; v0.2 chose NSA-style
  sparse attention (Delta 3 + 4) instead. Not a comparator
  Dream3R must prove against; not a Composer pool member.
  Threat to v0.2: speculative. Could become a comparator if a
  future paper demonstrates Kimi-style attention residual on
  3R; until then, treated as out-of-pool.
  Evidence label: user-decided (DEC-002); speculative.
```

### Tier 3: Out-of-scope — architectural assumptions changed (per Delta 2)

```text
Out-of-scope 1: ViT-L backbone
  v0.1 status: assumed C1 Perceiver substrate.
  v0.2 reclassification: out-of-scope (replaced by DINOv3-S per
                         Delta 2; ~14x param reduction; ~5x
                         latency speedup).
  Reason: v0.2 backbone choice is DINOv3-S (DINOv3-B fallback);
  ViT-L is no longer the substrate. Comparators previously
  framed against "Dream3R uses ViT-L like X" no longer apply;
  comparators framed against "Dream3R uses DINOv3-S unlike X"
  apply (see new Axis 10 below).
  Evidence label: paper-derived (DINOv3-S substitution per
  DINOV3_C1_INTEGRATION_MEMO).
```

### Tier 4: Foundation / lineage — cited but not in expert pool

These v0.1 entries are foundations Dream3R builds on; not threats; not Composer pool members.

```text
Foundation 1: DUSt3R (v0.1 Group A; line 56)
  v0.1 threat: LOW ("foundation, not competitor").
  v0.2 reclassification: foundation (unchanged).
  Reason: DUSt3R's CroCo-pretrained per-pair pointmap is the
  perception lineage of all 3R experts (including the 7 in-pool).
  Used as architectural lineage; not in pool because in-pool
  experts subsume DUSt3R's capabilities with extensions.
  Evidence label: paper-derived (lineage).
```

### Tier 5: Orthogonal / out-of-claim — useful comparators on non-pillar axes

These v0.1 entries are NOT in pool but provide legitimate comparison on non-pillar axes (e.g., scalability, dynamic handling, monolithic-vs-modular).

```text
Orthogonal 1: STream3R (v0.1 Group B; line 223)
  v0.1 threat: MEDIUM (same threat profile as CUT3R).
  v0.2 reclassification: orthogonal (CUT3R admitted in-pool;
                         STream3R kept as orthogonal because
                         per DEC-002 + COMPOSER_CAPABILITY_
                         DESCRIPTORS, only one of CUT3R/STream3R
                         is admitted to keep pool size bounded).
  Reason: Pool size bounded at 7 per cycle 018 admission criteria.
  Threat to v0.2: REMAINS MEDIUM on Axis 2 (Memory) but does NOT
  threaten pillar A or D directly under v0.2 narrowing.
  Evidence label: agent-decided (pool-size boundedness).

Orthogonal 2: LONG3R / LongStream / LoGeR (v0.1 Group B; line 242)
  v0.1 threat: HIGH ("solve long-sequence without control graph;
                     threaten 'control graph is needed' claim").
  v0.2 reclassification: orthogonal (v0.2 demoted pillar B
                         state-ownership; control-graph claim
                         is now discipline-level, not pillar-
                         level).
  Reason: Under v0.2 main-claim narrowing to A + D, the
  "control-graph-is-needed" claim is no longer a paper-pillar
  claim; LONG3R-class long-sequence work no longer threatens
  pillar A or D directly. Threat to discipline-level claim
  persists; not a comparator Dream3R must prove against under
  pillar-level evaluation.
  Evidence label: agent-decided (v0.2 pillar narrowing).

Orthogonal 3: TTT3R / test-time training variants (v0.1 Group D;
                                                    line 304)
  v0.1 threat: LOW ("test-time adaptation; orthogonal").
  v0.2 reclassification: orthogonal (unchanged).
  Reason: TTT3R is orthogonal to Dream3R's architecture; not in
  pool, not a foundation, not a threat.
  Evidence label: paper-known.

Orthogonal 4: MonST3R (v0.1 Group C; line 328)
  v0.1 threat: MEDIUM ("dynamic split; Dream3R's Permanence must
                       add to per-frame split").
  v0.2 reclassification: orthogonal.
  Reason: Under v0.2 pillar E (Identity-anchored memory)
  supporting status, MonST3R-style dynamic split is no longer a
  pillar threat. Pillar A + D do not depend on dynamic-split
  superiority over MonST3R.
  Evidence label: agent-decided.

Orthogonal 5: POMATO / D^2USt3R / Easi3R / RayMap3R (v0.1 Group
                                                     C; line 355)
  v0.1 threat: not individually ranked (grouped low).
  v0.2 reclassification: orthogonal.
  Reason: Niche dynamic-handling variants; not pool, not threat.
  Evidence label: paper-known.

Orthogonal 6: Mamba-3R variants (v0.1 Group A/B; line 378)
  v0.1 threat: MEDIUM ("SSM-only; substrate hypothesis test").
  v0.2 reclassification: orthogonal (v0.2 substrate is hybrid
                         transformer + SSM; Mamba-3R is a
                         legitimate substrate ablation).
  Reason: Under v0.2, Mamba-3R is the natural SSM-only baseline
  in the substrate-ablation axis (still planned for SPEC-005
  ABL-v02 if substrate ablation is reauthorized). Not a
  threat; a comparator on Axis 1.
  Evidence label: paper-known + agent-decided ablation framing.

Orthogonal 7: SLAM3R (v0.1 Group D; line 407)
  v0.1 threat: MEDIUM ("monolithic integration; Dream3R must
                       show modular > monolithic").
  v0.2 reclassification: orthogonal (pillar B state-ownership
                         demoted; modular-vs-monolithic is now
                         discipline-level claim, not pillar-
                         level).
  Reason: Same logic as LONG3R reclassification; pillar
  narrowing demotes the modularity claim from pillar to
  discipline.
  Evidence label: agent-decided (v0.2 pillar narrowing).

Orthogonal 8: Splatt3R / InstantSplat / NoPoSplat / 4DGS variants
              (v0.1 Group D; line 452)
  v0.1 threat: LOW ("different stack layer").
  v0.2 reclassification: orthogonal (unchanged).
  Reason: Rendering / Gaussian-splatting downstream layer; not
  pool, not threat.
  Evidence label: paper-known.
```

### Pool tier summary

```text
Tier 1 In-pool (7):           MASt3R / Fast3R / Spann3R / CUT3R /
                              MoGe-2 / DepthAnything-V2 / Test3R
Tier 2 Out-of-pool (3 drops): VGGT / MapAnything / Kimi-KDA
Tier 3 Out-of-scope (1):      ViT-L backbone
Tier 4 Foundation (1):        DUSt3R
Tier 5 Orthogonal (8):        STream3R / LONG3R+LongStream+LoGeR /
                              TTT3R / MonST3R / POMATO+D2USt3R+
                              Easi3R+RayMap3R / Mamba-3R / SLAM3R /
                              Splatt3R+4DGS variants

v0.1 entry count: 16
v0.2 in-pool count: 7 (5 from v0.1 + 2 NEW: MoGe-2 + DepthAnything-V2)
v0.2 out-of-pool: 3 (1 from v0.1 reclassified: VGGT; 1 from v0.1
                     reclassified: MapAnything; 1 NEW: Kimi-KDA)
v0.2 out-of-scope: 1 (architectural assumption: ViT-L)
v0.2 foundation: 1 (DUSt3R; unchanged)
v0.2 orthogonal: 8 (covering all remaining v0.1 entries)

Reclassification audit: every v0.1 entry has been assigned to
exactly one v0.2 tier; no v0.1 entry is silently dropped or
unassigned.
```

## New comparison axes introduced by v0.2

v0.1 had 8 axes (Perception / Memory / Critic / Permanence / Routing / Bus / CR-rules / Scalability). v0.2 adds 3 NEW axes anchored to v0.2 deltas.

### Axis 9: NSA-style sparse attention dimension (per Delta 3 + 4)

```text
What it measures:
  Whether a model uses NSA-style three-branch (compressed +
  selected + sliding) sparse attention vs. dense attention vs.
  alternative sparse schemes.

Categories:
  A. Dense attention only (v0.1 baseline; e.g., DUSt3R, MASt3R,
     VGGT)
  B. NSA-style three-branch (v0.2 Dream3R Memory C2; per Delta 3)
  C. Linear attention (e.g., Mamba-3R variants — orthogonal)
  D. Other sparse attention (e.g., longformer, sparse top-k)
  E. Sliding-window only (no compression / no selection)

Comparator landing:
  Dream3R v0.2 lands in B.
  In-pool experts: most land in A (dense attention internally;
                   their attention scheme is upstream of NSA in
                   Dream3R's pipeline).
  Mamba-3R variants: land in C (orthogonal substrate alternative).

Evidence label:
  Per delta inheritance: NSA for 3R is `speculative`. Dense
  attention as baseline is `paper-proven` for the experts.

Ablation anchoring:
  ABL-v02-1 (NSA-removal; Tier 1 load-bearing) tests whether
  v0.2 Dream3R's NSA branch is necessary; ABL-v02-9 (NSA kernel
  benefit decomposition; Tier 3) decomposes contribution by
  branch.
```

### Axis 10: DINOv3 backbone tier dimension (per Delta 2)

```text
What it measures:
  Backbone choice for C1 Perceiver and its capacity tier.

Categories:
  A. ViT-L (v0.1 baseline; out-of-scope under v0.2)
  B. DINOv3-S (v0.2 default; ~14x param reduction; ~5x latency
     speedup vs ViT-L; per Delta 2)
  C. DINOv3-B (v0.2 fallback)
  D. CroCo-pretrained ViT (e.g., DUSt3R lineage; foundation
     comparator)
  E. Other ViT backbones (e.g., experts using ViT-base/Large
     internally)

Comparator landing:
  Dream3R v0.2 lands in B (default) or C (fallback).
  DUSt3R foundation: lands in D (CroCo-pretrained ViT).
  In-pool experts: each carries its own ViT internally; not
                   directly comparable (their internal backbone
                   is upstream of the C1 substitution).

Evidence label:
  Per delta inheritance: DINOv3 substitution is `paper-derived`.
  Tier choice (-S over -B) is `paper-derived` (DINOv3 paper +
  DINOV3_C1_INTEGRATION_MEMO).

Ablation anchoring:
  ABL-v02-2 (DINOv3 backbone tier sweep -S/-B/-L; Tier 2)
  measures the tier choice; ABL-v02-3 (frozen vs partial-
  unfreeze; Tier 2) measures finetuning posture; ABL-v02-7
  (head training schedule; Tier 2) covers heads-from-scratch
  scheduling.
```

### Axis 11: Composer expert pool composition dimension (per Delta 5)

```text
What it measures:
  Whether a model uses heterogeneous expert routing (best-of-N)
  vs single-expert vs simple ensemble vs no routing.

Categories:
  A. No routing (single expert; v0.1 baseline; most 3R papers
     including DUSt3R, MASt3R, Spann3R alone)
  B. Heterogeneous best-of-N over diverse expert pool (v0.2
     Dream3R Composer C5; 7 experts; per Delta 5)
  C. Simple ensemble (uniform-weight averaging over experts;
     no capability-aware routing)
  D. Capability-aware single-expert routing (no best-of-N;
     just route input to ONE expert per regime)

Comparator landing:
  Dream3R v0.2 lands in B.
  In-pool experts (alone): each lands in A (their own internal
                            architecture is single-expert from
                            Dream3R's perspective).
  Other multi-model 3R systems: rare in v0.1 catalog; not a
  highly populated axis. The pillar D claim rests on B being
  measurably superior to A on multi-regime workloads.

Evidence label:
  Per delta inheritance: pool composition is `paper-known per
  expert + engineering-judgment per pool selection`.

Ablation anchoring:
  ABL-v02-4 (Composer best-of-N vs single-expert; Tier 1 load-
  bearing) is the primary pillar-D test; ABL-v02-5 (capability_
  match measurement; Tier 3) advances per-expert capability
  values from inferred -> measured.
```

### Axis summary

```text
Carried from v0.1 (unchanged): 8 axes (1-8)
NEW in v0.2 addendum:          3 axes (9-11)
Total v0.2 axes:               11
```

## Updated threat ranking against v0.2 main-claim A + D

v0.1 ranked threats against the full architectural claim (control-graph + bus + 4 finalist mechanisms). v0.2 narrows main-claim to A (Verification-as-architecture) + D (Heterogeneous best-of-N Composer); E (Identity-anchored memory) supporting; B/C demoted. Threat ranking re-evaluates against this narrower target.

```text
HIGH THREAT to pillar A (Verification-as-architecture):
  1. Test3R alone (in-pool but threat persists)
     Test3R has built-in verifier head; if Dream3R's Critic A4
     is not measurably better than "Test3R alone with its
     verifier", pillar A collapses. ABL-v02-1 (NSA-removal
     does NOT directly test this; needs separate "Test3R-alone
     vs Dream3R-Critic" comparator pass — see Open question Q1).

  2. TTT3R / test-time training (orthogonal but threat persists)
     If verification can be replaced by test-time adaptation,
     pillar A's "explicit verification module" claim weakens.
     Test-time adaptation is orthogonal to verification in
     theory but functionally substitutable in some failure
     modes.

HIGH THREAT to pillar D (Heterogeneous best-of-N Composer):
  3. VGGT (out-of-pool but threat persists indirectly)
     v0.1 ranked VGGT HIGH for "complexity is justified" claim.
     Under v0.2 streaming-first framing, VGGT cannot meet 30-50
     ms/frame budget, so direct streaming threat is REDUCED.
     But on offline-batch quality benchmarks (B1-B6 from SPEC-002
     v0.1, carried into SPEC-005 unchanged), VGGT remains a
     strong single-model baseline. ABL-v02-4 (Composer best-of-
     N vs single-expert) is the test; if best-of-7 beats VGGT
     on offline batch, pillar D survives.

  4. Each in-pool expert alone (internal threat to pillar D)
     If best-of-7 Composer does NOT outperform the BEST single
     expert per regime, pillar D collapses. ABL-v02-4 covers.

MEDIUM THREAT (overlap on one axis but not pillar-collapsing):
  5. Spann3R (in-pool; pillar D internal threat per Expert 3)
     Same framing as item 4.

  6. CUT3R/STream3R (CUT3R in-pool; STream3R orthogonal)
     Same framing.

  7. Mamba-3R (orthogonal substrate alternative)
     If pure-SSM substrate beats Dream3R hybrid on streaming-
     first benchmarks, substrate hypothesis is challenged. Not
     pillar A or D directly; but architectural assumption.

LOW THREAT (foundation / orthogonal-on-non-pillar / no-direct-
              comparison-needed):
  8. DUSt3R (foundation; not competitor)
  9. MASt3R / Fast3R / MoGe-2 / DepthAnything-V2 (in-pool;
                                                  capability
                                                  source, not
                                                  threat)
  10. MonST3R / POMATO+D2USt3R+Easi3R+RayMap3R (orthogonal;
                                                pillar E
                                                demoted to
                                                supporting)
  11. SLAM3R / Splatt3R+4DGS / MapAnything (orthogonal;
                                            different stack
                                            layer or
                                            application)
  12. LONG3R / LongStream / LoGeR (orthogonal under v0.2 pillar
                                   B demotion)
  13. Kimi Linear / KDA (out-of-pool; LM-to-3R speculative)
```

### v0.1 → v0.2 threat ranking traceability

```text
v0.1 HIGH (Spann3R, LONG3R, VGGT) ->
  v0.2 Spann3R demoted to in-pool MEDIUM (pillar D internal);
  v0.2 LONG3R demoted to LOW orthogonal (pillar B demoted);
  v0.2 VGGT remains HIGH for pillar D on offline-batch.
v0.1 MEDIUM (CUT3R/STream3R, Test3R, MonST3R, SLAM3R, Mamba-3R) ->
  v0.2 CUT3R/STream3R: CUT3R in-pool MEDIUM, STream3R orthogonal
                       LOW;
  v0.2 Test3R: in-pool but pillar A HIGH (most significant
               threat under v0.2);
  v0.2 MonST3R: orthogonal LOW (pillar E demoted to supporting);
  v0.2 SLAM3R: orthogonal LOW (pillar B demoted);
  v0.2 Mamba-3R: orthogonal MEDIUM (substrate hypothesis test).
v0.1 LOW (DUSt3R, MASt3R, Fast3R, TTT3R, MapAnything, Gaussian) ->
  v0.2 DUSt3R: foundation LOW (unchanged);
  v0.2 MASt3R, Fast3R: in-pool LOW (capability source);
  v0.2 TTT3R: orthogonal but PILLAR A MEDIUM (test-time
              adaptation as substitute for verification);
  v0.2 MapAnything: out-of-pool LOW (drop reason: too heavy);
  v0.2 Gaussian: orthogonal LOW (unchanged).

Audit: every v0.1 ranking has a v0.2 reclassification with
explicit rationale; no silent rerank.
```

## What Dream3R v0.2 must prove against each threat tier (anchored to ABL-v02-N)

```text
Against pillar A HIGH threats (Test3R alone; TTT3R):
  Primary: ABL-v02-6 (Selection-gate signal subsetting; Tier 1
           load-bearing). If selection gate works only with
           Critic confidence + Permanence link, NOT with
           Test3R's internal verifier alone, pillar A is
           validated.
  Secondary: ABL-v02-1 (NSA-removal; Tier 1 load-bearing).
             Validates the upstream Memory selection that
             pillar A depends on.
  Open question: explicit "Test3R-alone vs Dream3R-Critic"
                 comparator pass (NOT in ABL-v02-1..9; see
                 Open question Q1).

Against pillar D HIGH threats (VGGT on offline-batch; in-pool
                                experts alone):
  Primary: ABL-v02-4 (Composer best-of-N vs single-expert; Tier
           1 load-bearing). Tests pillar D directly.
  Secondary: ABL-v02-5 (capability_match measurement pass; Tier
             3). Advances inferred -> measured for the 7-expert
             pool.
  Open question: VGGT-as-single-baseline addition to ABL-v02-4
                 (NOT currently in SPEC-005 ABL-v02-4 baseline
                 list; see Open question Q2).

Against pillar D MEDIUM threats (Spann3R in-pool internal;
                                  CUT3R in-pool internal;
                                  Mamba-3R substrate):
  Covered by ABL-v02-4 internally for Spann3R + CUT3R.
  Mamba-3R substrate test: NOT in ABL-v02-1..9 (cycle 018 dropped
  substrate-only ablation per pillar narrowing); reauthorize via
  separate DEC if pillar A or D claims explicitly require
  substrate-alternative comparator.

Against pillar E supporting threats (MonST3R; LONG3R):
  Pillar E is supporting, not pillar; ABLs do not directly
  target pillar E threats. If pillar E claims fail, pillar A +
  D are unaffected.

Against demoted-claim threats (LONG3R; SLAM3R; for old pillar
                                B/C):
  No dedicated ABL. Demotion is honest; comparators on these
  claims are documented but not load-bearing.
```

## Architecture-novel elements with no comparator (carry from v0.1 + v0.2 additions)

Carry from v0.1 (line 534-565):

```text
1. Bus + CR-rules architectural primitive (v0.1; carried)
2. Control-graph composition over multi-module substrates (v0.1;
   demoted from pillar to discipline; carried)
3. Reservation tokens A7/A8 (v0.1; demoted to future work;
   carried as architecture-novel-but-deferred)
```

v0.2 addition (per DEC-20260507-001 §"Open questions Q3"):

```text
NOT promoted in v0.2 addendum:
  per-file/per-task review checklist pattern from CODE_STRUCTURE
  + IMPLEMENTATION_ROADMAP. This is a research-workflow
  contribution, not a 3R architecture novelty. Re-surface as
  paper Section discussion if/when Phase 2 paper writing
  cycle includes methodology section.
```

No NEW v0.2 architecture-novel elements. v0.2 deltas (DINOv3 / NSA / 7-expert pool) all have comparators (DINOv3 paper, NSA paper, individual experts).

## v0.1 -> v0.2 traceability matrix

```text
v0.1 element                          v0.2 status
-----------------------------------   --------------------------
8 comparison axes                     carried unchanged
16 comparator entries                 carried unchanged in v0.1
                                      body; reclassified into
                                      5 tiers in v0.2 addendum
v0.1 threat tiers (HIGH/MEDIUM/LOW)   re-ranked against pillar
                                      A + D narrowing; full
                                      traceability matrix above
v0.1 ABL-1..10 anchoring              superseded by ABL-v02-1..9
                                      from SPEC-005; v0.1
                                      anchoring preserved in
                                      v0.1 body
"Axes where Dream3R has no            carried + 1 NOT-promoted
 comparator" section                  candidate (review-pattern)
                                      per Open question Q3

NEW in v0.2:
  Axis 9 NSA-style sparse attention   anchored to Delta 3 + 4
  Axis 10 DINOv3 backbone tier        anchored to Delta 2
  Axis 11 Composer expert pool        anchored to Delta 5

NOT modified:
  v0.1 SPEC-003 file body              preserved unchanged per
                                       Discipline rule 5
  v0.1 SPEC-003 Version history       receives v0.2 pointer
                                       entry (sync chain)
```

## Risks (R-cm-1..R-cm-N for comparator-map-specific risks)

```text
R-cm-1: Pool admission of MoGe-2 + DepthAnything-V2 is
        engineering-judgment (NEW v0.2; not in v0.1 catalog).
        If a future capability-card pass reveals these two add
        no measurable best-of-N value, pool size could drop to
        5 and pillar D weakens. Mitigation: ABL-v02-5 capability_
        match measurement pass (Tier 3) is the test.
        Severity: MEDIUM.

R-cm-2: Test3R in-pool admission carries a pillar-A threat
        persistence (Test3R's internal verifier could
        functionally substitute for Dream3R Critic A4). Open
        question Q1 surfaces a comparator pass not currently
        in ABL-v02-1..9.
        Severity: HIGH for pillar A.

R-cm-3: VGGT out-of-pool drop is justified by frame budget
        (Delta 1) but does NOT eliminate offline-batch threat.
        ABL-v02-4 baseline list does not include VGGT (per
        SPEC-005); if VGGT-on-offline-batch beats best-of-7,
        pillar D weakens on the offline-batch story even if
        streaming-first survives. Open question Q2.
        Severity: MEDIUM-HIGH for pillar D offline-batch
        framing.

R-cm-4: Pillar B (state-ownership) + pillar C (reservation
        tokens A7/A8) demotion is honest but loses what v0.1
        treated as architectural novelty. Future paper writing
        may need to clarify that demoted claims are NOT
        retracted, just deferred to discipline / future work.
        Severity: LOW (paper-writing concern, not architecture
        risk).

R-cm-5: Mamba-3R substrate-alternative comparator is not in
        ABL-v02-1..9. If the paper claims hybrid > pure-SSM
        substrate, it must either reauthorize substrate
        ablation (separate DEC) or downgrade the hybrid-vs-SSM
        claim from pillar to discipline.
        Severity: MEDIUM (paper-writing concern).
```

## Boundaries

```text
1. Markdown only. No comparator entry triggers code execution.
2. v0.1 SPEC-003 body NOT modified (Surgical Edits +
   Discipline rule 5 NEW-file pattern).
3. No promotion of any in-pool expert to "approved-for-
   checkpoint-download" or "approved-for-execution"; those
   gates are per-expert per-task DEC + per-step micro gates
   per F-002.
4. No retiring of any v0.1 entry. Out-of-pool / out-of-scope
   classifications preserve v0.1 entries with reclassification
   reason, not deletion.
5. No silent revision of v0.2 main-claim narrowing (pillars
   A + D + E supporting; B/C demoted) per DEC-002.
6. No introduction of NEW comparator entries beyond MoGe-2 +
   DepthAnything-V2 + Kimi-KDA out-of-pool. Future comparator
   additions go to v0.3 addendum cycle.
7. No silent revision of v0.1 threat ranking; full traceability
   matrix preserves v0.1 → v0.2 reclassification reasons.
8. No paper Section 3+6 rewrite per cycle 022 deferral.
9. No code touch. code/dream3r/ files NOT Read in this cycle
   (Path C agent A may Read them in its own context; main
   agent does NOT).
10. No KYKT navigation change. No frontend implementation.
    No demo storyboard promotion past `draft`.
```

## Linked artifacts

- Parent: `decisions/DEC-20260507-001-cycle-021-launch-comparator-map-v02-and-path-c-review-activation.md`
- v0.1 substrate: `specs/SPEC-20260506-003-dream3r-comparator-map.md` (preserved unchanged)
- v0.2 architecture INPUT: `specs/SPEC-20260506-004-dream3r-architecture-v02.md`
- v0.2 ablation plan INPUT: `specs/SPEC-20260506-005-dream3r-ablation-plan-v02.md`
- v0.2 architecture deltas authorization: `decisions/DEC-20260506-002-cycle-018-launch-v02-architecture.md`
- 7-expert pool descriptors: `planning/COMPOSER_CAPABILITY_DESCRIPTORS.md`
- NSA integration memo: `planning/NSA_MEMORY_INTEGRATION_MEMO.md`
- DINOv3 integration memo: `planning/DINOV3_C1_INTEGRATION_MEMO.md`
- Sibling cycle 020 deliverables (referenced by Path C reviews; not by this addendum directly): `planning/DREAM3R_V02_CODE_STRUCTURE.md` + `planning/DREAM3R_V02_IMPLEMENTATION_ROADMAP.md`

## Open questions for cycle 022+

```text
Q1. Test3R-alone vs Dream3R-Critic comparator pass: ABL-v02-1..9
    do not include a direct "use Test3R alone with its built-in
    verifier" comparator. Pillar A robustness depends on showing
    Critic A4 outperforms Test3R-alone-verifier. Decision needed
    in cycle 022+: add this as ABL-v02-10 (separate DEC + SPEC-
    005 v0.3 addendum) OR fold into ABL-v02-1 baseline list (in-
    place SPEC-005 v0.3 addendum) OR document as out-of-scope
    falsification gap.
    Severity: HIGH for pillar A. Recommended: ABL-v02-10 in
    cycle 022 v0.3 addendum.

Q2. VGGT-on-offline-batch baseline: ABL-v02-4 baseline list
    does not include VGGT as a single-model baseline. Pillar D
    on offline-batch quality benchmarks needs VGGT comparison.
    Decision needed: extend ABL-v02-4 baseline list (in-place
    SPEC-005 v0.3 addendum) OR document as offline-batch out-
    of-scope under v0.2 streaming-first.
    Severity: MEDIUM-HIGH for pillar D offline-batch framing.

Q3. Review-pattern as architecture novelty: per-file/per-task
    review checklist pattern from cycle 020 was NOT promoted
    to architecture-novel-element in this addendum (decision
    per DEC-20260507-001 §"Open questions Q3"). Re-surface
    decision in cycle 022 paper writing if Methodology section
    surfaces it.
    Severity: LOW (paper-writing concern).

Q4. Mamba-3R substrate ablation: pillar A + D do not directly
    require substrate-alternative comparator, but pillar
    discipline may. Decision: keep as orthogonal (current
    state) OR reauthorize substrate ablation in cycle 023+
    (separate DEC).
    Severity: MEDIUM (paper-writing concern).

Q5. Pool admission criteria for v0.3: if user authorizes
    additional expert admission in v0.3 (e.g., a NEW 3R
    paper from 2026-Q2), what gates the admission? Cycle
    018 admission criteria are documented in COMPOSER_
    CAPABILITY_DESCRIPTORS but not in spec form. Decision:
    formalize admission criteria in v0.3 addendum
    (separate cycle).
    Severity: LOW (process concern).
```

## Discipline notes

```text
1. NEW-file pattern preserved (Surgical Edits + Discipline rule
   5): v0.1 SPEC-003 body NOT modified. v0.2 addendum lives in
   this NEW file (SPEC-20260507-001). Only v0.1 Version history
   tail receives a v0.2 pointer entry (sync-chain task in S5).

2. Honesty Override consummated: every reclassification carries
   inline evidence label (`paper-known per expert + engineering-
   judgment per pool composition` for in-pool admission;
   `user-decided per DEC-002` for out-of-pool drops; `agent-
   decided` for threat reranks; `paper-derived` for DINOv3
   axis; `speculative for 3R transfer` for NSA axis). v0.1 →
   v0.2 traceability matrix preserves all v0.1 rankings with
   reclassification reasons; no silent rerank.

3. Pre-existing markdown lint warnings on prior files (TASK_
   SNAPSHOT historical block; WORKFLOW_STATUS / decision_
   registry / INDEX table separators; SPEC-001 line 593;
   SPEC-002 line 633 falsification table) NOT fixed in cycle
   021 per Surgical Edits rule 3.

4. F-001 rule 1 honored in writing this file: SPEC-003 v0.1
   (625 lines) NOT full-Read in main-agent context; targeted
   Grep -n + offset/limit Read used to anchor section references
   and comparator-name list. SPEC-004 v0.2 + SPEC-005 v0.2 +
   COMPOSER_CAPABILITY_DESCRIPTORS already in main-agent context
   from prior cycles; no re-Read.

5. F-002 honored: cycle 021 markdown only; server-side
   /hdd3/kykt26/code/dream3r/ untouched; no clones, no installs,
   no checkpoints, no GPU runs, no training.

6. Cycle 022+ v0.3 addendum candidates surfaced in Open
   questions Q1-Q5: Q1 (ABL-v02-10 Test3R-alone) recommended
   for cycle 022 inclusion; Q2 (VGGT offline-batch) recommended
   for cycle 022 inclusion; Q3-Q5 deferred to later cycles.

7. Pool size boundedness (7 in-pool experts) is engineering-
   judgment per DEC-002 + COMPOSER_CAPABILITY_DESCRIPTORS;
   not paper-derived. Re-surfaced as Open question Q5 for
   formalization.

8. Paper writing implication: this v0.2 comparator map
   addendum closes the v0.2 markdown trio (architecture +
   ablation + comparator). Cycle 022 paper Section 3 + 6
   rewrite for A+D framing has this trio as INPUT.
```

## Version history

```text
2026-05-07 (cycle 021 S3): v0.2 comparator map addendum NEW.
  Reorganizes v0.1 16-entry pool into 5 tiers (in-pool 7 / out-
  of-pool 3 / out-of-scope 1 / foundation 1 / orthogonal 8) per
  Delta 5. Adds 3 NEW axes (Axis 9 NSA / Axis 10 DINOv3 / Axis
  11 Composer pool) per Deltas 2-5. Re-ranks threats against
  pillar A + D narrowing. v0.1 SPEC-003 body preserved
  unchanged.
```
