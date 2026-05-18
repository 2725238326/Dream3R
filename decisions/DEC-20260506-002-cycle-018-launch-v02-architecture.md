# DEC-20260506-002 cycle 018 launch + v0.2 architecture scope lock

decision_id: DEC-20260506-002

date: 2026-05-06

status: locked

cycle: closes cycle 017 paper-draft framing as static; seeds cycle 018 architecture v0.2 scope

parents:
- DEC-20260501-004 (Dream3R = candidate, not final thesis)
- DEC-20260504-002 (no all-in any single finalist)
- DEC-20260506-001 (mainline architecture-first; v0.1 spec authored)

linked_artifacts:
- TASK_SNAPSHOT.md (resume pointer; updated FIRST in sync chain)
- specs/SPEC-20260506-001-dream3r-architecture.md (v0.1; superseded in scope of v0.2 deltas only; v0.1 preserved as historical record per Honesty Override)
- specs/SPEC-20260506-002-dream3r-ablation-plan.md (v0.1; ABL coverage to be revisited under v0.2 deltas in a later sub-pass)
- specs/SPEC-20260506-003-dream3r-comparator-map.md (v0.1; comparator pool narrowed under v0.2; addendum will be issued)
- planning/COMPOSER_CAPABILITY_DESCRIPTORS.md (NEW; cycle 018 S2 deliverable)
- planning/NSA_MEMORY_INTEGRATION_MEMO.md (NEW; cycle 018 S3 deliverable)
- planning/DINOV3_C1_INTEGRATION_MEMO.md (NEW; cycle 018 S3 deliverable)
- specs/SPEC-20260506-004-dream3r-architecture-v02.md (NEW; cycle 018 S4 deliverable; v0.2 delta spec)

## One line summary

Lock the v0.2 architecture deltas surfaced during the 2026-05-06 design dialog: streaming-first inference budget, DINOv3-S backbone, NSA-style sparse attention as Memory implementation substrate, expanded heterogeneous Composer pool (drop VGGT / MapAnything / Kimi Linear / KDA; admit Spann3R / CUT3R / MASt3R / Fast3R / MoGe-2 / DepthAnything V2 / Test3R), and main-claim narrowing to two pillars (A. Verification-as-architecture, D. Heterogeneous best-of-N Composer).

## What user authorized in this session

User dialogue trail (2026-05-06):

```text
[user] reviewed v0.1; flagged that Composer pool was too narrow ("3R 那么多
       composer 才两三个"), that the new methods discussed in earlier
       dialog were not integrated, and that Memory module was hollow.
       Proposed: each 3R has a small set of innovation points but each
       sits on heterogeneous infrastructure; Composer should exploit this
       gap.

[user] requested architectural-optimization candidates and asked whether
       sparse attention and a (later-clarified-as-Kimi) attention residual
       mechanism would be useful.

[user] selected sparse attention as the optimization to keep; explicitly
       rejected the Kimi Linear / KDA attention-residual route ("注意力残差
       和咱这个没关系").

[user] requested recent vision/reconstruction papers usable as
       optimization. After candidate list (NSA / VGGT / MapAnything /
       DINOv3 / MoGe-2 / etc.), user rejected VGGT and MapAnything as too
       heavy ("我们的方案就是要快速些"), confirmed DINOv3-Small over
       DINOv2-Base.

[user] selected (a) inference real-time as primary speed priority, with
       (b) training-fast and (c) integration-fast as secondary.

[user] approved Memory direction A + B (anchor bank retrieval +
       hierarchical) + NSA implementation.

[user] requested agent recommendation on §3 main claim. Agent recommended
       A (Verification-as-architecture) + D (Heterogeneous best-of-N
       Composer). User approved by saying "你说哪个好啊" and then
       authorizing comprehensive forward push without further objection.

[user] selected v0.2 (new spec, NOT in-place v0.1 modification).

[user] "可以，我需要你全面推进和重整工作" (proceed comprehensively).
```

Evidence label for this DEC: `user-decided` for the scope locks; agent-recommended for the §3 main-claim narrowing (user-accepted). The deliverables listed under "Allowed by this DEC" carry per-section evidence labels per `paradigm/RESEARCH_CODE_DISCIPLINE.md` rule 5.

## Why this matters (interpretation)

v0.1 was authored in cycle 016 as a comprehensive synthesis (1821 lines) but carried four structural weaknesses surfaced by the 2026-05-06 dialog:

1. **Composer routing pool was too narrow.** v0.1 lists 5 backbones in the routing table but does not enumerate per-3R-model capability descriptors at finer granularity ("MASt3R matching head" vs. "MASt3R full pipeline"). User reframed Composer's job as exploiting the non-uniform infrastructure across 7+ heterogeneous 3R foundation models, not selecting among 2-3 monolithic models.

2. **Memory module was hollow.** v0.1 names C2 Memory as SSM/Mamba but does not specify what is actually stored, retrieved, or evicted. User asked for "memory with substance"; agent surfaced three candidate directions (A anchor-bank retrieval, B hierarchical, C consolidation); user picked A+B; NSA emerged as the natural implementation substrate after the user's sparse-attention preference was locked in.

3. **Backbone weight class was implicit.** v0.1 inherits ViT-Large from DUSt3R lineage. User clarified speed priority (real-time inference) makes ViT-L too heavy; DINOv3-Small replaces it. VGGT (~1.2B params) and MapAnything (multi-modal foundation) drop from the Composer pool entirely.

4. **Main claim was diffuse.** v0.1 carries 5+ candidate innovations (verification-as-architecture, state-ownership invariant, reservation tokens, heterogeneous best-of-N Composer, identity-anchored memory). For paper coherence, narrowing is needed. Agent recommended A + D pair as the two pillars of "control-graph-as-architecture"; user approved.

v0.2 is a delta on v0.1, NOT a rewrite. v0.1 is preserved as historical record (Honesty Override).

## Allowed by this DEC

Cycle 018 may produce, in order:

```text
S1  This DEC + TASK_SNAPSHOT.md redirect block update      -> done by this commit
S2  planning/COMPOSER_CAPABILITY_DESCRIPTORS.md (NEW)
    Enumerate 7 admitted Composer pool members with axes:
    - innovation point (what unique mechanism)
    - input regime (image pair / multi-view / streaming / mono)
    - output schema (pointmap / depth / pose / matching / Gaussian)
    - infrastructure cost (params / latency / memory / dependencies)
    - integration adapter sketch (how to map to Bus token space)
    - capability descriptor for Composer routing                -> pending
S3  planning/NSA_MEMORY_INTEGRATION_MEMO.md (NEW)
    planning/DINOV3_C1_INTEGRATION_MEMO.md (NEW)
    1-page each. Map paper mechanism to Dream3R module slot.
    Carry evidence labels (paper-known / inferred / speculative).  -> pending
S4  specs/SPEC-20260506-004-dream3r-architecture-v02.md (NEW)
    Delta-only spec. References v0.1 as substrate; documents:
    - speed priority (a) and frame budget table
    - C1 Perceiver substitution: ViT-L -> DINOv3-S
    - C2 Memory implementation: bounded anchor bank + NSA-style
      selective retrieval (A+B pattern)
    - sparse attention as architectural optimization (NSA-style;
      Critic confidence + Permanence anchor co-drive selection gate)
    - C5 Composer pool: 7 admitted models; drop VGGT / MapAnything
      / Kimi Linear / KDA; reference COMPOSER_CAPABILITY_DESCRIPTORS
    - main-claim narrowing: A (Verification-as-architecture) + D
      (Heterogeneous best-of-N Composer); B/C demoted to discipline /
      future work; E demoted to support claim
    - Open Questions Q1..Q6 from v0.1 -> resolved/superseded/carried
                                                                    -> pending
S5  Sync chain (TASK_SNAPSHOT first per F-001 rule 6;
    cycles/CYCLE-20260506-003.md NEW; decision_registry append;
    research_unit_registry RU-007 status update;
    WORKFLOW_STATUS / RESEARCH_STATE / INDEX light sync;
    SPEC-001 v0.1 amended only with a "v0.2 delta exists" pointer
    in its Version history section, no in-place rewriting)         -> pending
```

## Not allowed by this DEC

```text
1. No training. No GPU runs to "test" v0.2 architecture. v0.2 is
   markdown spec + planning artifacts; execution remains gated.
   Train-first remains deferred / blocked.

2. No final thesis selection. Dream3R-the-architecture remains a
   candidate per DEC-20260501-004; v0.2 is iteration, not commitment.

3. No retiring of B (state-ownership invariant), C (reservation
   tokens A7/A8), or E (identity-anchored memory) as candidates;
   they are demoted in main-claim ordering, not deleted. Per
   DEC-20260504-002 no-all-in still applies.

4. No retroactive rewriting of SPEC-20260506-001 v0.1 body. v0.2
   is a NEW file (SPEC-004). v0.1 receives only a Version history
   pointer at its tail, not in-place edits to its sections. (Surgical
   Edits rule 3 + Honesty Override rule 5.)

5. No new repo clones / installs / checkpoints. NSA / DINOv3 / MoGe-2
   integration memos are paper-derived sketches, not implementation
   gates. Any subsequent code touch requires a separate DEC.

6. No retroactive rewriting of SPEC-002 ablation plan or SPEC-003
   comparator map. v0.2-specific addenda will be issued in a later
   sub-pass; cycle 018 scope is the four NEW artifacts above plus
   sync chain.

7. No KYKT navigation change. No frontend implementation. No demo
   storyboard promotion past `draft`. No reusable Codex skill
   packaging. No teacher-demo readiness claim.

8. No silent supersede of DEC-20260506-001 mainline-architecture-
   first. v0.2 is iteration WITHIN architecture-first mainline,
   not a re-direction.

9. No rejected-candidate erasure. The Kimi Linear / KDA / attention-
   residual line is dropped from active integration but remains in
   RU-007 with status updated to "rejected for v0.2 scope; LM-to-3R
   transfer not pursued". Honesty Override forbids deleting prior
   candidate framing.
```

## v0.2 deltas summary (locked)

```text
Backbone (C1 Perceiver):
   v0.1: ViT-Large (DUSt3R lineage; ~300M params)
   v0.2: DINOv3-Small or DINOv3-Base (no G/7B; 8-10x param reduction
         vs ViT-L; rationale: streaming-first frame budget)

Memory implementation (C2):
   v0.1: SSM/Mamba over evidence tokens (substrate hypothesis hybrid)
   v0.2: bounded anchor bank + NSA-style selective retrieval
         + hierarchical short/medium/long memory (directions A+B
         from cycle-018 design dialog).
         Mamba retained as one option for medium-term state; NSA
         retrieval is the substrate that gives Memory actual semantic
         content (anchor embeddings, eviction policy, retrieval queries).

Sparse attention (architectural optimization):
   v0.1: not specified
   v0.2: NSA-style token-level sparse attention. Selection gate driven
         by Critic confidence (low-confidence tokens get full-attention
         escape) + Permanence anchor (anchored objects persist in
         attention budget). Engineering optimization, not paper main
         claim.

Composer pool (C5):
   v0.1: 5 backbones in routing table, granularity at model-level
   v0.2: 7 admitted lightweight models with capability descriptors:
         - Spann3R, CUT3R (streaming)
         - MASt3R, Fast3R (pair / multi-view fast path)
         - MoGe-2, DepthAnything V2 (mono fallback)
         - Test3R (lazy verification)
         dropped: VGGT, MapAnything (too heavy for streaming budget)
         dropped: Kimi Linear / KDA (LM-to-3R transfer not pursued)
         routing axis added: "attention regime" (full / linear /
         sparse) per expert.

Frame budget (streaming-first):
   v0.1: not specified
   v0.2: target 30-50 ms/frame at 30 FPS. Component allocation:
         C1 DINOv3-S forward 10-15 ms, C2 SSM/sparse-retrieve few ms,
         C3 bounded slot attention few ms, C4 critic few ms, C5/C6
         routing+bus < 1 ms. Critic-triggered lazy invocation of
         heavy verification (Test3R) only on flagged tokens.

Main claim narrowing:
   v0.1: 5+ candidates carried in parallel
   v0.2: two paper pillars
         (A) Verification-as-architecture: Critic gate is structural
             write-blocker, not loss term
         (D) Heterogeneous best-of-N Composer: routing exploits
             non-uniform infrastructure across 7 lightweight 3R
             foundation models
         supporting: (E) Identity-anchored memory (Permanence x
             Memory coupled)
         demoted to discipline / future: (B) state-ownership
             invariant, (C) reservation tokens A7/A8

Drops vs v0.1 scope:
   - VGGT, MapAnything (too heavy)
   - Kimi Linear / KDA / attention-residual route (RU-007 status:
     rejected for v0.2 scope; preserved as historical RU)
   - PE / Perception Encoder (too heavy)
   - "uniform composer routing table" (replaced by capability
     descriptors)

Carries forward unchanged:
   - control-graph-as-architecture thesis
   - 6 computational cores C1-C6
   - bus + CR-1..CR-6 gates
   - state-ownership invariant (now discipline-level)
   - 4 finalist mechanism specs as input synthesis
   - DEC-20260501-004 candidate-not-final
   - DEC-20260504-002 no-all-in any single finalist
```

## Implications for prior cycles

```text
- Cycle 015 (Critic L3 pilot) remains paused at S9 done. v0.2 does NOT
  resume G_run; if measured Critic evidence is needed for v0.2's
  Verification-as-architecture claim, that is a separate later DEC.

- Cycle 016 (architecture v0.1 + ablation plan + comparator map) closed
  cleanly. v0.2 builds on it, does not invalidate it. Ablation plan
  (SPEC-002) and comparator map (SPEC-003) need v0.2 addenda but those
  are out of cycle 018 scope.

- Cycle 017 (paper draft v1) may need Section 3 (architecture) and
  Section 6 (comparators) updated to reflect v0.2 deltas. That is a
  later cycle, NOT cycle 018 scope. PAPER_DRAFT_V1.md remains as-is
  until a separate DEC authorizes paper rewrite for v0.2.

- RU-007 (Attention-Residual / KDA 3R Memory Update) status updated
  from "speculative only; keep for survey" to "rejected for v0.2 scope;
  LM-to-3R transfer not pursued in active branch". Source row in
  FRONTIER_SOURCE_MAP retained for historical reference. Honesty
  Override: do not delete; supersede via status change with reason.
```

## Discipline notes

```text
- Surgical Edits: v0.2 is a NEW spec file (SPEC-004), NOT in-place
  edits to SPEC-001. SPEC-001 v0.1 receives only a Version history
  tail pointer to v0.2. v0.1 sections are not rewritten.

- Honesty Override: every v0.2 delta carries an evidence label.
  NSA-to-3R transfer is `inferred / speculative` (LM-domain mechanism;
  no published 3R validation). DINOv3-S substitution is `paper-derived`
  (DUSt3R lineage well-established; DINOv3 family published). Frame
  budget is `inferred` (component-level estimates, not measured).
  Composer capability descriptors are `paper-known` for the 7 admitted
  models; pool exclusions (VGGT, MapAnything) are `engineering-judgment`
  on weight-class grounds.

- F-001 anti-32MB: TASK_SNAPSHOT.md is updated FIRST in the sync
  chain. v0.1 spec (1821 lines, 95 KB) is NOT re-Read in cycle 018;
  cited via existing TOC in TASK_SNAPSHOT and via Grep -n for any
  specific section references. Capability descriptors and integration
  memos are bounded under ~300 lines each. v0.2 spec body kept under
  ~600 lines (delta-only).

- F-002 server topology: cycle 018 is markdown only; no server-side
  execution; the 172.17.140.97 / kykt env stays untouched. Any
  subsequent code touch requires a separate DEC.

- Hard rules carried from AGENT_MASTER_PROMPT.md section 6: no
  reproduction / no checkpoint download / no training / no KYKT
  navigation change / no frontend implementation / no thesis
  finalization / no retiring of any non-finalist track. All in
  force; this DEC adds none.
```
