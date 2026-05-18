# Dream3R architecture v0.2 (delta on v0.1)

spec_id: SPEC-20260506-004

spec_kind: architecture spec, delta-only (NOT a rewrite of v0.1)

parent_spec: SPEC-20260506-001 (v0.1; substrate; preserved as historical record per Honesty Override)

parent_decision: DEC-20260506-002 (v0.2 scope lock)

date: 2026-05-06

cycle: 018 (S4 deliverable; per DEC-20260506-002)

status: v0.2 (candidate-not-final per DEC-20260501-004; iteration on v0.1 within architecture-first mainline per DEC-20260506-001; deltas locked per DEC-20260506-002)

honesty_label: every delta below carries an inline evidence label (paper-known / paper-derived / inferred / speculative / engineering-judgment).

linked_artifacts:
- specs/SPEC-20260506-001-dream3r-architecture.md (v0.1 substrate; sections referenced by name; NOT re-stated here)
- decisions/DEC-20260506-002-cycle-018-launch-v02-architecture.md (parent decision; v0.2 deltas locked)
- decisions/DEC-20260506-001-mainline-architecture-first.md (mainline framing carried unchanged)
- decisions/DEC-20260501-004-dream3r-candidate-not-final.md (candidacy clause carried)
- decisions/DEC-20260504-002-no-all-in-finalist.md (no-all-in clause carried)
- planning/COMPOSER_CAPABILITY_DESCRIPTORS.md (cycle 018 S2; 7 admitted experts)
- planning/NSA_MEMORY_INTEGRATION_MEMO.md (cycle 018 S3; NSA × C2 Memory)
- planning/DINOV3_C1_INTEGRATION_MEMO.md (cycle 018 S3; DINOv3 × C1 Perceiver)
- specs/SPEC-20260506-002-dream3r-ablation-plan.md (v0.1 ablation plan; v0.2 addendum out of cycle 018 scope)
- specs/SPEC-20260506-003-dream3r-comparator-map.md (v0.1 comparator map; v0.2 addendum out of cycle 018 scope)

## Identity

This spec is a delta on `SPEC-20260506-001` v0.1. It does NOT restate v0.1's substrate hypothesis, top-level block diagram, token taxonomy, state-ownership invariant, bus runtime API, A1-A8 mapping, read-write window protocol, CR-1..CR-6 gates, or training-objective sketch. Those sections in v0.1 remain canonical except where this spec explicitly supersedes a numbered claim.

This spec defines six numbered deltas (Delta 1..Delta 6), each anchored to a v0.1 section by section heading reference. A reader who has not read v0.1 should read this delta first for orientation and then Grep v0.1 by section name only as the deltas reference them; full sequential re-reading of v0.1 (1821 lines) is explicitly NOT required and is discouraged per F-001.

## Approval

Approved scope-of-deltas: per `DEC-20260506-002` (cycle 018 launch + v0.2 architecture scope lock; user-decided 2026-05-06).

Approved sub-claim narrowing (main claim A+D pillars): agent-recommended, user-accepted on 2026-05-06 ("你说哪个好啊" + "可以，我需要你全面推进和重整工作").

NOT approved by this spec:

- training, GPU runs, checkpoint download, code execution (markdown only)
- finalization of Dream3R candidacy (DEC-20260501-004 still in force; v0.2 is iteration, not commitment)
- retiring of any non-finalist track (DEC-20260504-002 no-all-in still in force; B / C / E remain candidates, not deleted)
- in-place rewriting of v0.1 spec body (Surgical Edits rule 3 + Honesty Override rule 5)
- v0.2 addenda to ablation plan (SPEC-002) or comparator map (SPEC-003); those are separate later sub-passes
- KYKT navigation change, frontend implementation, demo storyboard promotion past `draft`, teacher-demo readiness claim, Phase 2 paper rewrite for v0.2

## Scope of v0.2

```text
markdown only
candidate-not-final (DEC-20260501-004)
no-all-in (DEC-20260504-002)
architecture-first mainline (DEC-20260506-001)
v0.2 delta-only (this spec; DEC-20260506-002)
```

v0.2 introduces six numbered deltas to v0.1. v0.1 sections not referenced by a delta are unchanged.

## Why v0.2 exists

The 2026-05-06 design dialog surfaced four structural weaknesses in v0.1:

```text
W1. C5 Composer pool was too narrow.
    v0.1 enumerates 5 backbones at coarse model-granularity. User
    reframed Composer's job as exploiting NON-uniform infrastructure
    across heterogeneous 3R foundation models, not selecting among
    monolithic models. Resolution -> Delta 5.

W2. C2 Memory module was hollow.
    v0.1 names C2 as SSM/Mamba but does not specify storage,
    retrieval, or eviction. User asked for "memory with substance".
    Direction A (anchor-bank retrieval) + B (hierarchical) selected.
    NSA emerged as the natural implementation substrate after sparse-
    attention was selected as the optimization to keep. Resolution
    -> Delta 3 + Delta 4.

W3. Backbone weight class was implicit.
    v0.1 inherits ViT-L from DUSt3R lineage. User's locked priority
    (a) inference real-time at 30-50 ms/frame at 30 FPS makes ViT-L
    too heavy. DINOv3-Small replaces it. VGGT and MapAnything drop
    from the Composer pool entirely. Resolution -> Delta 1 + Delta 2
    + Delta 5.

W4. Main claim was diffuse.
    v0.1 carries 5+ candidate innovations in parallel. For paper
    coherence, narrowing is needed. Agent recommended A
    (Verification-as-architecture) + D (Heterogeneous best-of-N
    Composer) as the two pillars; user-accepted. B / C demoted to
    discipline / future; E demoted to support. Resolution -> Delta 6.
```

v0.2 addresses W1..W4 via six deltas; v0.1's control-graph-as-architecture thesis, six computational cores, bus + CR-1..CR-6 gates, and finalist-spec synthesis all carry forward unchanged.

## Reading order

```text
1. Read this spec (you are here).
2. Read DEC-20260506-002 (parent decision; v0.2 deltas locked).
3. Read the three cycle 018 planning artifacts (capability descriptors
   + NSA memo + DINOv3 memo) when a delta references them.
4. Reference v0.1 (SPEC-001) ONLY by Grep -n on the section names cited
   in each delta below. Do NOT re-read v0.1 in full (1821 lines, 95 KB;
   F-001 anti-32MB rule).
5. Reference DEC-20260506-001 for parent-cycle architecture-first
   framing.
```

## Delta 1 — Speed priority + frame budget

```text
v0.1 anchor:    "Scope of v0.1" (line 59), "Substrate hypothesis"
                (line 196), "Computational cores" (line 639). v0.1
                does not specify a per-frame latency budget.

v0.2 delta:     speed priority is locked as
                  (a) inference real-time PRIMARY (target 30-50 ms/
                      frame at 30 FPS streaming-first)
                  (b) training fast (secondary)
                  (c) integration fast (secondary)

                Per-frame component budget allocation (target):
                  C1 Perceiver           : 10-15 ms (DINOv3-S forward)
                  C2 Memory NSA retrieve : few ms (sparse top-k)
                  C3 Permanence slot     : few ms (bounded slots)
                  C4 Critic head         : few ms (small transformer)
                  C5 Composer route      : <1 ms (table join)
                  C6 Bus tick + handoff  : <1 ms
                  Total                  : 20-25 ms / frame; 5-25 ms
                                           reserve for downstream
                                           pointmap heads.

                Heavy verification path (EXPERT-07 Test3R) is OFF the
                streaming path; Critic-triggered lazy invocation only,
                on flagged tokens, with own latency budget that does
                NOT need to fit inside the 30-50 ms streaming envelope.

evidence label: inferred. Component-level estimates per integration
                memos; not measured under dream3r server env. Promotion
                to "measured" requires a separate benchmark DEC.

risk:           dream3r server runs TITAN RTX 24GB (not H100 / A100);
                NSA hardware-aware kernel benefits may not transfer in
                full; algorithmic sparsity still applies but practical
                wall-clock margin is narrower than published numbers.
                Mitigation: budget table treats numbers as targets,
                not commitments; SPEC-002 v0.2 addendum (later cycle)
                must include benchmark runs to anchor.
```

## Delta 2 — C1 Perceiver: DINOv3-S replaces ViT-L

```text
v0.1 anchor:    "Substrate hypothesis (v0.1 working assumption)"
                (line 196), "Computational cores" (line 639). v0.1's
                C1 Perceiver inherits DUSt3R-lineage ViT-L (~300M
                params).

v0.2 delta:     C1 backbone substituted with DINOv3-Small (~22M
                backbone params; default). DINOv3-Base (~85M) is
                a documented fallback if Small features prove
                insufficient for downstream pointmap head quality.
                DINOv3-Large (~300M) is a worst-case escape hatch
                that matches v0.1 weight class but exceeds 30 FPS
                budget; not in the v0.2 default.

                Backbone is FROZEN by default. Heads on top
                (pointmap_head, confidence_head, evidence_head) are
                trainable from scratch and DO NOT inherit ViT-L head
                weights (different feature space; cannot transfer).

                Input resolution carries 384x512 from v0.1. Patch
                size is 14 (DINOv3 family default) vs whatever v0.1
                pinned (Grep v0.1 if pinning is load-bearing for an
                ablation; default 14).

                Bus publication contract (carries from v0.1):
                  T1 frame_token        published per frame
                  T2 pointmap_token     published per patch
                  T3 evidence_token     published per patch (17-dim
                                        per cycle 016 convention)

inferred numbers (paper-derived; not measured):
                  backbone params:    ~300M -> ~22M  (~14x reduction)
                  backbone VRAM fp16: ~600 MB -> ~50 MB (~12x reduction)
                  forward latency:    ~50-80 ms -> ~10-15 ms (~5x speedup)

evidence label: paper-derived for the substitution itself (DUSt3R
                lineage well-documented; DINOv3 family backwards-
                compatible with DINOv2 usage patterns; published 2025
                3R works already use DINOv3 features). inferred for
                dream3r-server-specific latency / VRAM numbers.

risk:           pointmap quality may suffer at -S because DINOv3
                features are not purpose-trained for 3D regression
                (semantic > geometric content). Mitigation: -B
                fallback documented; optional top-N unfreezing as
                ablation candidate; multi-stage training (head
                warmup -> partial unfreeze) as later option.

reference:      planning/DINOV3_C1_INTEGRATION_MEMO.md for full
                migration sketch + 5-item risk list.
```

## Delta 3 — C2 Memory: bounded anchor bank + NSA-style retrieval

```text
v0.1 anchor:    "Substrate hypothesis (v0.1 working assumption)"
                (line 196), "Computational cores" (line 639) C2
                Memory subsection. v0.1 names C2 as SSM/Mamba over
                evidence tokens but does not specify what is stored,
                retrieved, or evicted.

v0.2 delta:     C2 implementation substantiated as
                  (a) bounded anchor bank (capacity K = 256 proposed;
                      hyperparameter, NOT pinned)
                      each entry: anchor_embedding (D-dim) +
                      scene_pose_metadata + freshness_counter +
                      permanence_link
                      eviction: LRU among non-permanence-anchored
                      entries; permanence-anchored entries are
                      evict-protected (C3 Permanence owns
                      permanence_link state; C2 reads it but does
                      not mutate it — preserves v0.1 state-ownership
                      invariant)
                  (b) NSA-style three-branch selective retrieval
                      Compressed branch  -> long-term scene summary
                                            (~32 compressed tokens)
                      Selected branch    -> top-k anchor lookup
                                            (proposed k = 8;
                                            hyperparameter)
                      Sliding branch     -> last W frames of evidence
                                            (proposed W = 4;
                                            hyperparameter)

                Selection gate INPUTS:
                  query_t            : current window's evidence
                                       summary
                  anchor_embedding   : per-anchor key
                  evidence_tokens_t  : T3 Bus read
                  critic_confidence_t: T3 Bus read (low confidence ->
                                       bias toward retrieving more
                                       anchors for verification)
                  permanence_link    : T5 Bus read (anchored objects
                                       always retrievable with
                                       priority)

                Mamba SSM is RETAINED as one option for the medium-
                term tier (B's middle layer). Either retained Mamba
                state or a second NSA layer with longer window can
                serve this slot. Pinning that choice is a v0.3
                question; v0.2 lists Mamba as optional medium-term
                substrate.

                Bus publications (per window tick t):
                  memory_state_t       -> T6
                  selected_anchors_t   -> T5 (read by C3 Permanence
                                          for identity update; read
                                          by C4 Critic for
                                          reprojection verification)
                  memory_retrieval_log -> contract_log (per cycle 016
                                          v2.1 contract handoff)

evidence label: paper-known for NSA mechanism (DeepSeek 2025;
                arxiv 2502.11089). speculative for 3R / vision
                transfer (NO published vision use). speculative
                for the cross-module-signal claim (Critic +
                Permanence co-driving the selection gate has no
                prior-art validation in 3R).

risk:           transfer is architectural-hypothesis-grade. SPEC-002
                v0.2 addendum (later cycle) must include "remove NSA
                -> fall back to plain anchor bank with cosine top-k"
                as a tier-1 ablation. NSA hardware-aware kernel
                benefit on TITAN RTX is uncertain (see Delta 1 risk
                note).

reference:      planning/NSA_MEMORY_INTEGRATION_MEMO.md for full
                three-branch -> hierarchy mapping + 5-item risk list.
```

## Delta 4 — Sparse attention as architectural optimization

```text
v0.1 anchor:    "Substrate hypothesis" (line 196). v0.1 does not
                specify an attention regime per module.

v0.2 delta:     NSA-style token-level sparse attention is the C2
                Memory selection-gate substrate (see Delta 3) AND
                the Composer routing axis (see Delta 5
                attention_regime per expert). It is an engineering
                optimization, NOT a paper main claim.

                The selection gate's signal mix (Critic confidence
                + Permanence anchor link) makes the sparse-attention
                gate itself a participant in v0.2's main claim A
                (Verification-as-architecture; see Delta 6): low
                Critic confidence biases the gate toward retrieving
                more for verification, anchoring sparse attention to
                the verification semantic.

                Per-module attention regime (v0.2):
                  C1 Perceiver         : full attention (DINOv3-S
                                         backbone; per-frame)
                  C2 Memory            : NSA three-branch (sparse +
                                         compressed + sliding)
                  C3 Permanence        : full attention within
                                         bounded slot set
                  C4 Critic            : full attention (small head)
                  C5 Composer          : routing logic (no attention
                                         in C5 itself; experts vary)
                  C6 Bus               : N/A (dataflow, not compute)

evidence label: paper-known for NSA's general sparse-attention
                story (LLM domain). speculative for the per-module
                assignment in 3R as listed above.

discipline:     paper main-claim is A+D (Delta 6), not "sparse
                attention". NSA in this spec is implementation-level;
                its absence does not falsify the paper's central
                thesis.
```

## Delta 5 — C5 Composer pool: 7 admitted lightweight experts

```text
v0.1 anchor:    "Computational cores" (line 639) C5 Composer
                subsection, "Per-spec cross-reference" (line 1276)
                Composer rows. v0.1 lists 5 backbones at coarse
                model-level granularity.

v0.2 delta:     Composer pool admits exactly 7 lightweight experts,
                each with a finer-granularity capability descriptor
                that distinguishes innovation point, input regime,
                output schema, infrastructure cost, attention regime,
                adapter sketch, capability_match axes, expected
                failure modes, and per-axis evidence labels.

                Admitted (full descriptors live in
                planning/COMPOSER_CAPABILITY_DESCRIPTORS.md):

                  EXPERT-01 MASt3R           : pair / matching head
                                               (~300M; full attn)
                  EXPERT-02 Fast3R           : many-view single fwd
                                               (~580M; full attn)
                  EXPERT-03 Spann3R          : streaming spatial
                                               anchor (~250M)
                  EXPERT-04 CUT3R            : online persistent
                                               state (~300M)
                  EXPERT-05 MoGe-2           : mono pointmap (~200M;
                                               recovery + bootstrap)
                  EXPERT-06 DepthAnything-V2 : mono depth foundation
                                               (~25M Small; cheap
                                               prior)
                  EXPERT-07 Test3R           : test-time consistency
                                               verification (lazy
                                               off-path; backbone+
                                               iteration)

                Dropped from v0.1 scope (engineering-judgment):
                  VGGT (~1.2B)           : exceeds streaming budget
                  MapAnything            : multi-modal foundation;
                                           too heavy
                  PE / Perception Encoder: too heavy

                Dropped (rejected for v0.2 scope; LM-to-3R transfer
                not pursued; preserved as RU-007 historical):
                  Kimi Linear / KDA / attention-residual route

                Shadowed in pool (admissible in spirit, not in v0.2):
                  DUSt3R     : MASt3R is superset for pair regime
                  MonST3R    : dynamic-aware fine-tuning overlaps
                               with C3 Permanence role; v0.3
                               readmission decision

                Deferred (paper-known via cycle-013 source mining
                but not primary-verified for inference profile /
                license / checkpoint availability; remain in
                FRONTIER_SOURCE_MAP):
                  LONG3R, Point3R, PAS3R, LoGeR, Mem3R, RayMap3R

                Routing axis added: attention_regime per expert
                (full / linear / sparse). This axis joins the
                v2.1 cross-spec contract's capability_match
                vector (additive; existing axes unchanged).

                Routing policy sketch (inferred v0.2; sub-millisecond
                table-join in C5):
                  first-frame / tracking-lost  -> EXPERT-05 + EXPERT-06
                                                  (mono recovery + cheap
                                                   prior in parallel)
                  N >= 4 views, budget allows  -> EXPERT-02 (avoid
                                                  O(N^2) pair fusion)
                  streaming, prior state ok    -> EXPERT-03 and/or
                                                  EXPERT-04 (best-of-N
                                                  over heterogeneous
                                                  streaming experts;
                                                  THIS is the Delta 6
                                                  main-claim D primary
                                                  demonstration)
                  loop-closure pair candidate  -> EXPERT-01 (matching)
                  Critic flag OR retrieval
                  conflict                     -> lazy invoke EXPERT-07
                                                  Test3R off the
                                                  streaming path (THIS
                                                  is the Delta 6 main-
                                                  claim A primary
                                                  demonstration)

evidence label: paper-known for innovation_point / params / latency
                target on each expert. paper-derived for streaming
                compatibility judgment. inferred for capability_match
                values and route_regret. engineering-judgment for
                pool exclusions (VGGT / MapAnything weight-class).

reference:      planning/COMPOSER_CAPABILITY_DESCRIPTORS.md for full
                7-row schema + cross-axis summary table + 5-item
                open-items list (capability_match measurement gate,
                CUT3R checkpoint inventory, scale-alignment for mono
                experts, Critic threshold pinning, v0.3 pool growth
                conditions).

discipline:     pool exclusions are NOT retiring of the rejected
                models. VGGT / MapAnything remain known to the
                project; they are out of the v0.2 STREAMING-FIRST
                pool. A future "slow-path tier" DEC could readmit
                them. Per DEC-20260504-002 no-all-in clause, no pool
                exclusion is final.
```

## Delta 6 — Main claim narrowing

```text
v0.1 anchor:    "The architectural claim" (line 104), "Module-level
                evidence labels (summary)" (line 1202), "Comparator
                quick map" (line 1253). v0.1 carries 5+ candidate
                innovations in parallel.

v0.2 delta:     paper main-claim narrows to TWO PILLARS:

                A. Verification-as-architecture
                   The Critic gate is a STRUCTURAL write-blocker, not
                   a loss term. Verification is wired into the bus
                   (CR-1, CR-2 gates from v0.1) and into the Memory
                   selection gate (Critic confidence biases retrieval;
                   see Delta 3). Test-time verification (EXPERT-07
                   Test3R) is invoked only when the Critic flags a
                   region; this is verification AT ARCHITECTURE LAYER,
                   not AT TRAINING LAYER.
                   primary demonstration:
                     - v0.1 CR-1..CR-6 gates (already specified)
                     - Delta 3 NSA selection gate driven by Critic
                       confidence
                     - Delta 5 EXPERT-07 lazy invocation routed by C4

                D. Heterogeneous best-of-N Composer
                   Routing exploits NON-uniform infrastructure across
                   7 lightweight 3R foundation models. The claim is
                   that no single 3R backbone covers all regimes
                   well; an explicit routing layer over heterogeneous
                   experts beats any monolithic backbone in expected
                   regret.
                   primary demonstration:
                     - Delta 5 7-expert pool with capability descriptors
                     - v0.1 C5 Composer (already specified) + v2.1
                       contract route_regret signal
                     - Cycle 010 + cycle 011 case-card portfolio
                       provides the inferred-anchor evidence (per
                       cycle-014 paper blueprint)

                Supporting (NOT deleted; not in main claim):
                  E. Identity-anchored memory
                     Permanence × Memory coupling (preserved from
                     v0.1; reinforced in Delta 3 selection gate via
                     permanence_link signal). E supports A and D
                     by providing the cross-module signal mix
                     that makes verification + routing meaningful.

                Demoted to discipline / future (NOT deleted; per
                DEC-20260504-002 no-all-in):
                  B. State-ownership invariant
                     Carried as a discipline rule (each piece of
                     state owned by exactly one module; cross-module
                     reads are read-only). Preserved unchanged in
                     v0.2 Memory bank ownership (see Delta 3 anchor
                     bank entries: C2 owns the bank, C3 owns
                     permanence_link). NOT a paper main-claim pillar.
                  C. Reservation tokens A7 / A8
                     Cross-Modal (A7) and Active Perception (A8)
                     remain RESERVED bus surfaces in v0.2. Not
                     designed in v0.2 either; pushed to a future
                     spec.

evidence label: agent-recommended; user-accepted on 2026-05-06
                ("你说哪个好啊" + comprehensive forward authorization).
                Per DEC-20260506-002 and TASK_SNAPSHOT 2026-05-06.

discipline:     "narrowing" is a paper-coherence move, not a
                project-scope move. The 4 finalist mechanism specs
                (SPEC-001..003 + SPEC-20260504-001) all remain
                inputs; B / C are demoted in MAIN-CLAIM ordering, not
                in project scope. DEC-20260504-002 no-all-in is
                preserved.
```

## What carries forward unchanged from v0.1

```text
- Control-graph-as-architecture central thesis (v0.1 §"The
  architectural claim").
- Hybrid substrate hypothesis (transformer perception + SSM/Mamba
  optional medium-term + slot Permanence + parameter-free Composer
  + cross-spec memory bus). DINOv3-S (Delta 2) substitutes ONLY the
  C1 backbone; the substrate hypothesis as a working assumption is
  unchanged.
- Six computational cores C1..C6 (v0.1 §"Computational cores"). Delta
  2 substitutes C1 weight class; Delta 3 substantiates C2 storage /
  retrieval / eviction; C3 / C4 / C5 / C6 unchanged in structure.
- Token taxonomy T1..T6 (v0.1 §"Tokens"). Delta 2 + Delta 3 publish
  on existing token surfaces; no new token type added.
- State ownership invariant (v0.1 §"State ownership"). Delta 3
  preserves it explicitly (anchor bank owned by C2; permanence_link
  owned by C3; cross-module reads are read-only).
- Memory bus runtime API (v0.1 §"The Memory Bus as runtime API").
  Delta 3 selected_anchors_t + memory_retrieval_log publications
  are additive on existing T5 + contract_log surfaces.
- A1..A8 mapping (v0.1 §"A1-A8 mapping"). A7 / A8 still RESERVED.
  Demoted to "discipline / future" in Delta 6 main-claim ordering;
  reservation surface unchanged.
- Read-write protocol per window (v0.1 §"Read-write protocol per
  window"). Delta 3 fits inside the existing 8-step bus tick (C2's
  retrieval is one of the existing reads; selected_anchors publish
  is one of the existing writes).
- CR-1..CR-6 conflict-resolution gates (v0.1 §"Conflict resolution
  as architectural elements"). v0.2 main-claim A reinforces CR-1 and
  CR-2 framing as Verification-as-architecture (Delta 6).
- Training-objective sketch (v0.1 §"Training-objective sketch"). v0.2
  does NOT authorize training; sketch carries unchanged as INPUT to
  the (deferred) ablation plan v0.2 addendum.
- Per-spec cross-reference to 4 finalist specs (v0.1 §"Per-spec
  cross-reference"). v0.2 does NOT delete any finalist spec
  reference; it adds 7-expert capability descriptors as a finer
  layer below.
- Risks R1..R7 (v0.1 §"Risks"). Carried unchanged. v0.2 adds three
  delta-specific risks below.
- Boundaries (v0.1 §"Boundaries"; 13 explicit boundaries).
  Carried unchanged. v0.2 adds four delta-specific boundaries below.
- DEC-20260501-004 candidate-not-final and DEC-20260504-002
  no-all-in clauses. Both in force; v0.2 deltas do NOT modify them.
```

## Open Questions Q1..Q6 from v0.1 — resolution status

```text
Q1. Substrate ablation priority
    v0.1: open. Asked which ablation tier comes first.
    v0.2: RESOLVED in cycle 016 S3 ablation plan
          (SPEC-20260506-002): hybrid first; SSM-only second;
          transformer-only third. ABL-2 in SPEC-002 specifies
          all three. v0.2 inherits this resolution.

Q2. Adversarial vs natural CR-rule triggering
    v0.1: open. Asked which mode of CR-rule triggering is the
          primary falsifying experiment.
    v0.2: RESOLVED in cycle 016 S3: both. B1-B5 for performance;
          B6 for CR-rule firing verification (per
          SPEC-20260506-002).

Q3. A7 Cross-Modal / A8 Active Perception concretization timing
    v0.1: open. Asked when the reserved hooks should be filled.
    v0.2: SUPERSEDED by Delta 6 main-claim narrowing. C
          (reservation tokens A7/A8) demoted from main-claim
          pillar to discipline / future. Concretization is now
          post-A+D-paper work; explicitly NOT cycle 018 scope.

Q4. v0.1 -> v0.2 trigger
    v0.1: open. Asked what would trigger v0.2 revision.
    v0.2: RESOLVED by THIS spec being v0.2. The trigger was
          (a) user critique 2026-05-06 (Composer too narrow,
              Memory hollow, backbone too heavy, claim too diffuse)
          (b) DEC-20260506-002 v0.2 scope lock.
          Closes Q4 with the answer: "user-driven re-design
          dialog after candidate review".

Q5. KYKT integration for evidence anchoring
    v0.1: open. Asked when KYKT runner / sample matrix should
          be wired in as evidence anchor.
    v0.2: CARRIED. Cycle 015 Critic L3 pilot infrastructure
          remains paused at S9 done; G_run NOT resumed in cycle
          018. v0.2 main-claim A primary demonstration uses CR-
          gates + NSA selection gate + lazy Test3R routing as
          ARCHITECTURE-LEVEL evidence. KYKT-derived measured
          evidence is a separate later cycle, gated on a fresh
          DEC.

Q6. Paper integration path
    v0.1: open. Asked how the architecture spec connects to the
          paper Phase 2 blueprint.
    v0.2: PARTIALLY RESOLVED. Delta 6 narrows main-claim to A+D,
          which directly maps to paper Section 3 (architecture)
          and Section 6 (comparators). PAPER_DRAFT_V1.md (cycle
          017) needs Section 3 + Section 6 update to reflect v0.2
          deltas; that update is NOT cycle 018 scope and requires
          a separate DEC. Q6 remains open until paper rewrite is
          authorized.
```

## Risks (v0.2 delta)

```text
R-v02-1. NSA-to-3R transfer is unvalidated.
         NSA is an LM-domain mechanism; no published vision use.
         Delta 3 + Delta 4 hinge on architectural-hypothesis-grade
         transfer. Mitigation: SPEC-002 v0.2 addendum (later cycle)
         must include "remove NSA -> plain anchor bank with cosine
         top-k retrieval" as a tier-1 ablation; speculative evidence
         label carried throughout.

R-v02-2. DINOv3-S pointmap quality may underperform ViT-L baseline.
         Frozen-backbone setup with re-init heads is a fresh-train
         configuration; DUSt3R-quality pointmaps are the de facto
         baseline. Mitigation: -B fallback documented (Delta 2);
         optional top-N unfreezing as ablation candidate; multi-
         stage training (head warmup -> partial unfreeze) listed
         in SPEC-002 v0.2 addendum scope.

R-v02-3. Frame budget is inferred, not measured.
         30-50 ms / frame target relies on component-level estimates
         under TITAN RTX; NSA hardware-aware kernel benefit is
         uncertain on non-H100 hardware. Mitigation: budget table
         framed as target, not commitment; benchmark gate is a
         separate later DEC.
```

R-v02-1 .. R-v02-3 are ADDITIVE on v0.1 R1..R7. v0.1 risks remain in force.

## Boundaries (v0.2 delta + carry)

v0.1's 13 explicit boundaries (v0.1 §"Boundaries (carried + new)") are carried in full. v0.2 adds:

```text
B-v02-1. v0.2 is a delta-only spec. v0.1 spec body is NOT modified
         in-place. v0.1 receives only a Version history pointer at
         its tail (per DEC-20260506-002 Discipline notes + Surgical
         Edits rule 3 + Honesty Override rule 5).

B-v02-2. v0.2 does NOT authorize training, GPU runs, checkpoint
         download, code execution, or environment changes. NSA /
         DINOv3 / Composer-pool integration memos are paper-derived
         design sketches, not implementation gates. Any code touch
         requires a separate DEC.

B-v02-3. v0.2 does NOT retire any non-finalist track or any rejected
         candidate. VGGT / MapAnything / Kimi-KDA are dropped from
         the v0.2 streaming-first pool but remain in the project's
         historical record (RU-007 status updated to "rejected for
         v0.2 scope; LM-to-3R transfer not pursued"; FRONTIER_SOURCE
         _MAP rows preserved). Per DEC-20260504-002 no-all-in.

B-v02-4. v0.2 does NOT issue ablation plan or comparator map
         addenda in cycle 018. SPEC-20260506-002 (ablation plan v0.1)
         and SPEC-20260506-003 (comparator map v0.1) need v0.2-
         specific updates; those are separate later sub-passes,
         out of cycle 018 scope.
```

B-v02-1..B-v02-4 are ADDITIVE on v0.1 boundaries. v0.1 boundaries remain in force.

## Evidence label distribution (v0.2 deltas only)

```text
paper-known          : NSA mechanism (DeepSeek 2025); DINOv3 family
                       (Meta 2025); 7 expert innovation_points;
                       latency targets per expert.
paper-derived        : DINOv3-S substitution (DUSt3R lineage well-
                       documented; DINOv3 backwards-compatible with
                       DINOv2 usage); per-expert streaming
                       compatibility; component-level latency
                       estimates.
inferred             : 30-50 ms/frame budget on dream3r server;
                       per-expert capability_match values; selection
                       gate hyperparameters K=256 / k=8 / W=4;
                       routing policy thresholds; route_regret
                       expectations.
speculative          : NSA-to-3R/vision transfer; Critic + Permanence
                       co-driving the NSA selection gate (no prior-art
                       3R validation); per-module attention regime
                       assignment in Delta 4.
engineering-judgment : pool exclusions (VGGT, MapAnything on weight-
                       class grounds); shadowed pool entries (DUSt3R
                       superseded by MASt3R for pair); deferred-pool
                       entries (LONG3R / Point3R / PAS3R / LoGeR /
                       Mem3R / RayMap3R primary-verification gap).
agent-recommended /  : main-claim narrowing to A+D pillars (Delta 6);
user-accepted          B/C demotion; E support framing.
```

v0.1's evidence-label distribution (~5 paper-proven / ~5 paper-derived / ~10 inferred / ~7 architecture-novel / 2 speculative) is unchanged for v0.1 sections; v0.2 deltas add the distribution above.

## Comparator quick map (v0.2 delta)

v0.1 §"Comparator quick map" listed comparators at coarse model granularity. v0.2 narrows the comparator set to match the streaming-first scope:

```text
In-pool comparators (v0.2 admitted):
  MASt3R, Fast3R, Spann3R, CUT3R, MoGe-2, DepthAnything-V2, Test3R
  (each a row in COMPOSER_CAPABILITY_DESCRIPTORS.md; Composer's
   value vs each is the route_regret reduction over best-single-
   expert per regime; main-claim D primary demonstration target).

Out-of-pool comparators (v0.2 dropped from streaming scope but
retained as paper-level baselines):
  DUSt3R           : pair baseline (shadowed by MASt3R in pool)
  MonST3R          : dynamic-aware (overlaps with C3; v0.3 readmit?)
  VGGT             : heavyweight slow-path baseline (FUTURE tier)
  MapAnything      : multi-modal foundation baseline (FUTURE tier)

Out-of-scope comparators (deferred or rejected):
  Kimi Linear / KDA: rejected for v0.2 (RU-007 status update)
  PE / Perception
  Encoder          : too heavy
  LONG3R, Point3R,
  PAS3R, LoGeR,
  Mem3R, RayMap3R  : primary-verification gap; remain in source map
```

A v0.2 addendum to SPEC-003 (comparator map) is needed to reflect this narrowing; that is OUT of cycle 018 scope.

## Linked artifacts (full list)

Decisions:
- DEC-20260506-002 (v0.2 scope lock; parent)
- DEC-20260506-001 (mainline architecture-first; parent of parent)
- DEC-20260501-004 (Dream3R candidate-not-final)
- DEC-20260504-002 (no-all-in any single finalist)
- DEC-20260505-001 (D3 first demo target = Critic; carried)

Specs:
- SPEC-20260506-001 (v0.1 architecture; substrate; NOT rewritten)
- SPEC-20260506-002 (v0.1 ablation plan; v0.2 addendum deferred)
- SPEC-20260506-003 (v0.1 comparator map; v0.2 addendum deferred)
- SPEC-20260503-001 (Critic / System-2 3R finalist)
- SPEC-20260503-002 (Executive Memory finalist)
- SPEC-20260503-003 (Permanence Engine finalist)
- SPEC-20260504-001 (3R Composer finalist)

Planning artifacts (cycle 018):
- planning/COMPOSER_CAPABILITY_DESCRIPTORS.md
- planning/NSA_MEMORY_INTEGRATION_MEMO.md
- planning/DINOV3_C1_INTEGRATION_MEMO.md

Paradigm / contract:
- paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md (v2.1; capability_match
  vector + route_regret; Delta 5 adds attention_regime axis as
  additive)
- paradigm/RESEARCH_CODE_DISCIPLINE.md (rules 1-5 carried)
- paradigm/ARCHITECTURE_MECHANISM_INTAKE.md (F1..F6 failure modes
  used in capability descriptors)

Failure modes:
- F-001 (32 MB request-limit; this spec stays under ~600 lines)
- F-002 (server topology; v0.2 is markdown only; no server-side
  execution)

Cycle log:
- cycles/CYCLE-20260506-003.md (cycle 018 log)

Future / pending v0.2 addenda (NOT cycle 018 scope):
- SPEC-20260506-002 v0.2 addendum (NSA-removal ablation; DINOv3-S
  vs -B ablation; frozen vs partial unfreeze; route_regret
  measurement plan)
- SPEC-20260506-003 v0.2 addendum (comparator narrowing per
  in-pool / out-of-pool / out-of-scope tiers above)
- literature/PAPER_DRAFT_V1.md Section 3 + Section 6 update
  (paper rewrite for v0.2 main-claim A+D framing)

## Next step (post-cycle 018)

Cycle 018 closes when this spec is written and S5 sync chain completes (per DEC-20260506-002). Candidate next-cycle directions, in agent-recommended order:

```text
1. SPEC-002 v0.2 addendum (ablation plan deltas).
   Define NSA-removal ablation, DINOv3-S vs -B vs -L ablation,
   frozen vs partial-unfreeze ablation, route_regret per-regime
   sweep, capability_match measurement plan. Markdown only. New
   cycle launch DEC required.

2. SPEC-003 v0.2 addendum (comparator map deltas).
   Reflect in-pool / out-of-pool / out-of-scope tiering per Delta 5.
   Markdown only.

3. Paper Phase 2 rewrite for v0.2 main-claim A+D.
   Update PAPER_DRAFT_V1.md Section 3 (architecture) + Section 6
   (comparators). Re-anchor Section 4 (claim narrative) to A+D
   pillars; B/C/E framed as supporting / discipline. New cycle
   launch DEC required.

4. Cycle 015 G_run resumption (Critic A4 measured anchor).
   Architecture spec v0.2 main-claim A would benefit from
   measured Critic-confidence-driven verification evidence.
   G_run is paused at S9 done; resumption requires fresh DEC.

5. Capability-match measurement pass.
   Route 7 experts on a held-out micro-benchmark (5 scenes x
   4 regimes); record route_regret per regime. Promotes Delta 5
   capability_match values from inferred to measured. New cycle
   launch DEC + server-side execution gate required.
```

User direction needed before any of (1)..(5) launches. Cycle 018 itself does NOT authorize them.

## Discipline notes

```text
- Surgical Edits (rule 3): this spec is a NEW file. v0.1 spec body
  is NOT modified. v0.1 receives only a Version history pointer at
  its tail. The 3 cycle 018 planning artifacts and DEC-002 are
  cited as existing artifacts; their content is not duplicated here.

- Honesty Override (rule 5): every v0.2 delta carries an inline
  evidence label. NSA-to-3R is `speculative`. DINOv3-S is `paper-
  derived`. Frame budget is `inferred`. Composer descriptors are
  `paper-known` per row (with `inferred` capability_match values).
  Pool exclusions are `engineering-judgment`. Main-claim narrowing
  is `agent-recommended / user-accepted`.

- F-001 anti-32MB: this spec stays under ~600 lines (target met).
  v0.1 spec is NOT re-Read in cycle 018; section anchors cited by
  name + line number from prior Grep results. Each delta references
  the parent v0.1 section by line anchor so the reader can Grep
  precisely without full re-read.

- F-002 server topology: cycle 018 is markdown only. The 172.17.140.97
  / kykt env is untouched. Any subsequent code touch (NSA / DINOv3 /
  expert integration) requires a separate DEC and goes server-side
  per F-002 rules.

- Hard rules from AGENT_MASTER_PROMPT.md section 6 (carried): no
  reproduction; no checkpoint download; no training; no KYKT
  navigation change; no frontend implementation; no thesis
  finalization; no retiring of any non-finalist track; no demo
  storyboard promotion past `draft`. All in force; this spec adds
  none and modifies none.

- DEC-20260501-004 candidate-not-final and DEC-20260504-002 no-all-in
  carried unchanged. v0.2 is iteration on a candidate, not commitment.
  B / C / E are demoted in main-claim ordering but preserved as
  project candidates.
```

## Version history

```text
v0.1  2026-05-06  cycle 016 S2 deliverable (SPEC-20260506-001).
                  First architecture spec for Dream3R. Hybrid
                  substrate working hypothesis. 4 finalist specs
                  synthesized. v2.1 contract rendered as runtime API.
                  CR-1..CR-6 rendered as gates. A1-A8 mapped to
                  concrete layers (A7/A8 reserved). Per-section
                  evidence labels carried. Markdown only. (1821 lines.)

v0.2  2026-05-06  cycle 018 S4 deliverable (this file;
                  SPEC-20260506-004). Delta-only spec on v0.1.
                  Six numbered deltas: (1) speed priority + frame
                  budget, (2) C1 Perceiver DINOv3-S substitution,
                  (3) C2 Memory bounded anchor bank + NSA-style
                  retrieval (A+B hierarchy), (4) sparse attention
                  as architectural optimization (NSA; not main
                  claim), (5) C5 Composer pool admits 7 lightweight
                  experts with capability descriptors (drop VGGT,
                  MapAnything, Kimi-KDA), (6) main-claim narrowing
                  to A (Verification-as-architecture) + D
                  (Heterogeneous best-of-N Composer); B/C demoted to
                  discipline/future; E supporting. v0.1 body
                  preserved unchanged per Surgical Edits + Honesty
                  Override.
```
