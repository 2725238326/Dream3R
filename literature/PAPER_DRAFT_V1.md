# Dream3R Paper Draft v1

Last updated: 2026-05-08 (cycle 026; v1.4 evidence-boundary correction after C2 Memory v0.3 addendum; cycle 024 measurements remain valid for component latency, parameter counts, adapter availability, and pipeline plumbing only; they do NOT validate C2 memory quality, reconstruction quality, routing quality, or C2 v0.3)

Status: draft (not submission-ready; cycle 024 contains bounded component measurements and an untrained pipeline trace; C2 Memory v0.3 supersedes v0.2 Delta 3 as the current memory design)

Supersedes: literature/PAPER_PHASE2_BLUEPRINT.md (demoted to SUPPORT per DEC-20260506-001)

Source anchors:
- specs/SPEC-20260506-001-dream3r-architecture.md (v0.1; §3.1–3.7 substrate)
- specs/SPEC-20260506-004-dream3r-architecture-v02.md (v0.2; §3.8 delta source)
- specs/SPEC-20260506-002-dream3r-ablation-plan.md (v0.1; planned experiments)
- specs/SPEC-20260506-003-dream3r-comparator-map.md (v0.1; §6.4 preserved)
- specs/SPEC-20260507-001-dream3r-comparator-map-v02.md (v0.2; §6.0–6.3 source)
- specs/SPEC-20260508-001-dream3r-c2-memory-v03-addendum.md (v0.3 C2 Memory addendum; supersedes v0.2 Delta 3 as current memory design)
- specs/SPEC-20260503-001..003 + SPEC-20260504-001 (4 finalist specs; inputs)
- paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md (v2.1)
- planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md (A1-A8 + V1 + P1-P6)
- planning/COMPOSER_CAPABILITY_DESCRIPTORS.md (v0.2; 7-expert pool)
- literature/PAPER_RELATED_WORK_SKELETON.md (prose draft; reused)
- cases/ L2 portfolio (13 cards)

---

## Working title

```text
Dream3R: A Control-Graph Architecture for Long-Context,
Dynamic-Aware, Multi-Model 3D Reconstruction
```

Evidence label: inferred.

## Abstract (draft)

```text
Post-DUSt3R 3D reconstruction (3R) models have diversified rapidly:
some handle long sequences via persistent memory, some separate dynamic
from static content, some verify geometric consistency at test time,
and some target specific input regimes. Yet each model addresses one
failure mode in isolation, and no shared control vocabulary governs
when to update memory, when to verify, when to reroute to a
different backbone, or when to suppress a static-map write because
a region is dynamic.

We propose Dream3R, a control-graph architecture that makes this
vocabulary first-class. Dream3R synthesizes four mechanisms — an
executive Memory controller (SSM-based), a Geometry Critic (small
transformer head), an Object Permanence module (slot memory), and a
regime-aware Composer (parameter-free table join) — onto a single
cross-specification memory bus. The bus carries a 17-signal evidence
vector and six conflict-resolution rules (CR-1..CR-6) rendered as
architectural gates. The result is a modular, falsifiable
architecture where each component can be independently ablated and
each cross-module interaction is governed by an explicit typed
contract.

We present the architecture design, a 10-experiment ablation plan
organized in three priority tiers, and a comparator map against 14+
existing 3R models showing that Dream3R's control graph, bus, and
gate mechanisms have no direct precedent in the 3R literature.
```

Evidence label: inferred (no training; no measured results; design contribution only).

## 1. Introduction

### 1.1 The fragmentation problem

The DUSt3R family converted 3D reconstruction from a pipeline problem into a single pose-free pointmap regression. Within two years, the follow-up landscape diversified along three axes: matching and speed (MASt3R, Fast3R, MV-DUSt3R+, NoPoSplat), temporal state for streaming (CUT3R, STream3R, Spann3R, LONG3R, LoGeR, LongStream), and dynamic-scene extensions (MonST3R, POMATO, D^2USt3R, Easi3R, RayMap3R). Universal claims such as VGGT and MapAnything compress those axes into single feed-forward backbones.

The field is past the point where one more backbone resolves the open failure modes. What is missing is not more pointmap accuracy on controlled benchmarks; what is missing is a *control vocabulary*: a compact set of typed actions a 3R system can take (update state, verify geometry, reroute model, suppress write, track object identity), and a typed set of regimes under which each action is appropriate.

### 1.2 Our contribution: control graph as architecture

Dream3R proposes that the architectural novelty is the *graph* — the modules, the bus connecting them, and the gates governing their interactions — not any single module's internals.

Concretely:

1. **Four modules on a shared bus.** Memory (SSM/Mamba; owns A1 state update, A2 spatial memory governance, A3 anchor budgeting), Critic (small transformer head; owns A4 verification, A5 repair), Permanence (slot memory; owns A6 dynamic/object separation), and Composer (parameter-free table join; owns A5 routing) share a cross-specification memory bus carrying a 17-signal evidence vector.

2. **Conflict resolution as gates.** Six rules (CR-1..CR-6) from the cross-spec signal contract are rendered as architectural elements: hard masks (CR-1, CR-2), input-feature weightings (CR-3), tiebreak modules (CR-4), label-propagation invariants (CR-5), and audit ledgers (CR-6).

3. **Hybrid substrate hypothesis.** Transformer perception (paper-proven), SSM executive memory (paper-derived), slot memory for object permanence (paper-proven outside 3R), parameter-free routing (paper-derived from MoE literature). The hypothesis is that forcing all substrates into one type degrades performance.

4. **Falsifiable by design.** Every architectural claim maps to a specific ablation (10 ablations in 3 tiers). The highest-priority ablation (ABL-1, bus removal) directly tests whether the bus adds value over flat module composition.

### 1.3 What this paper is and is not

This paper IS:
- An architecture proposal with explicit evidence labels per component
- An ablation plan specifying which experiments falsify which claims
- A comparator map showing where Dream3R sits relative to 14+ existing 3R models

This paper is NOT:
- A trained model
- A measured quality or architecture-performance claim
- A validation of C2 Memory v0.3
- A final thesis (Dream3R remains a candidate per DEC-20260501-004)

Cycle 024 adds bounded engineering measurements for component latency, parameter counts, adapter availability, and untrained pipeline plumbing. Those measurements do not validate reconstruction quality, routing quality, memory quality, or paper-level superiority.

## 2. Related work

### 2.1 Pose-free 3R foundations

DUSt3R introduced pose-free pointmap regression. MASt3R added dense local feature matching. VGGT produced per-frame pointmap, camera, and depth tokens in a single forward pass. Fast3R introduced efficient multi-view attention. These models define the perception substrate that Dream3R's Perceiver core (C1) inherits.

### 2.2 Long-context memory (F1)

CUT3R, STream3R, Spann3R, LONG3R, LoGeR, LongStream, and Mem3R each maintain persistent state across frames. Spann3R uses spatial memory with anchor-based retrieval; CUT3R uses full-update per frame; LONG3R adds gating; LoGeR combines local and global retrieval; LongStream decouples gauge from cache. Each picks one update/cache/store rule and shows it dominates their baseline.

Dream3R's Memory module (C2) asks a different question: given a workload spanning multiple streaming regimes and a state budget, which update rule should be selected per window? The A1 update_kind classifier (5-way: full, pose-adaptive, Kalman, skip, reset) makes this a first-class architectural choice rather than a fixed design decision.

### 2.3 Dynamic-static handling (F2)

MonST3R, POMATO, D^2USt3R, Easi3R, and RayMap3R handle dynamic content at the per-frame level. None targets persistent object identity across the dynamic-static split.

Dream3R's Permanence module (C3) adds object_track_set — a slot-memory-based persistent identity set — and the suppress_static_write handoff to Memory (CR-2). The contribution is identity persistence and static-map immunity, not per-frame motion estimation.

### 2.4 Verification and repair (F3)

Test3R enforces test-time consistency via a verifier head. TTT3R triggers test-time training on confidence drops. MASt3R-SfM adds classical SfM refinement. CTRL shows the critic-revision pattern in the LM domain.

All are scoped to one model family. Dream3R's Critic module (C4) asks whether a cross-model A5 reroute — bound to Composer's capability_match — can cross model families at inference time. The A5 action set (accept, rerun_local, reroute_model, open_anchor, request_prior, conflict_unresolved) is broader than simple re-run.

### 2.5 Model ecology and routing (F6)

No 3R paper publishes a routing metric. Capability cards exist informally in README comparison tables but produce no falsification axis.

Dream3R's Composer module (C5) defines route_regret as the first 3R-specific routing falsification axis: if the router chooses backbone X over backbone Y in regime R, how much was left on the table?

### 2.6 What has no 3R precedent

Five Dream3R elements have no close comparator in the existing 3R literature:

1. Cross-spec memory bus as explicit typed tensor schema
2. CR-rules as architectural gates (hard masks, invariants, ledgers)
3. Composer with route_regret falsification axis
4. A5 repair-facet action set beyond simple re-run
5. Object_track_set with persistent identity across frames

These carry the evidence label "architecture-novel" and represent the highest paper novelty — and highest risk.

## 3. Architecture

> **[v0.2 delta — cycle 022 — 2026-05-07]** Sections 3.1–3.7 are the v0.1 architecture (cycle 017; source: SPEC-20260506-001). Section 3.8 adds the six v0.2 deltas (DEC-20260507-002; source: SPEC-20260506-004 Deltas 1–6). v0.1 prose is preserved unchanged per Discipline rule 5. Main-claim narrows to pillars A (Verification-as-architecture) + D (Heterogeneous best-of-N Composer) per Delta 6.

### 3.1 Overview

Dream3R is a control-graph-as-architecture: six computational cores (C1 Perceiver, C2 Memory SSM, C3 Permanence slot memory, C4 Critic head, C5 Composer table join, C6 Memory Bus) connected by a typed bus carrying the v2.1 cross-spec signal contract as its runtime API.

[Architecture block diagram: see SPEC-20260506-001 section "Top-level architecture"]

### 3.2 Token classes

Six token classes flow through the architecture:

- T1 frame tokens (Perceiver output; paper-proven)
- T2 pointmap tokens (Perceiver pointmap head; paper-proven)
- T3 evidence tokens (17-signal V1 projection; inferred)
- T4 regime token (Composer regime classifier; inferred)
- T5 anchor + object tokens (Memory + Permanence slot memory; inferred)
- T6 bus tokens (typed dict; all modules publish; architecture-novel)

### 3.3 Computational cores

**C1 Perceiver** (transformer, ~300-700M params inferred): per-frame perception backbone. Inherits DUSt3R/MASt3R/VGGT lineage. Evidence: paper-proven.

**C2 Memory SSM** (Mamba-style, ~50-150M params inferred): executive memory with A1 update_kind classifier (5-way), A2 write head, A3 anchor/cache controller. Evidence: paper-derived for SSM-as-3R-memory; inferred for A1 classifier composition.

**C3 Permanence slot memory** (~30-80M params inferred): slot attention over object_track_set + per-region A6 classifier (suppress/admit/defer) + object identity head. Evidence: inferred (slot-attention for 3R-object-permanence is novel; slot attention itself is paper-proven outside 3R).

**C4 Critic head** (small transformer, ~5-30M params inferred): A4 verifier head (scalar conflict_score) + A5 repair-facet classifier (5-way). Evidence: inferred (small-Critic over V1 tokens is novel; verifier-on-3R is paper-proven).

**C5 Composer** (parameter-free, 0 params): regime_card x capability_card -> capability_match -> route_recommendation. Evidence: paper-derived for table-based routing; architecture-novel for 3R-specific regime cards.

**C6 Bus** (no params): typed-dict tensor namespace with publish/read/handoff surfaces + CR-1..CR-6 gate modules. Evidence: architecture-novel.

### 3.4 The memory bus

The bus has three surfaces:

1. **Published signals** (read-only contract): each V1 signal is a typed slot; producer writes once per window, consumers read.

2. **Handoffs** (binding signals): Permanence's suppress_static_write binds Memory's A2 write head (CR-2). Composer's route_recommendation binds Critic's A5 reroute (CR-1 gated).

3. **Gates** (conflict resolution): CR-1 hard mask on reroute (capability_match spread); CR-2 hard mask on static write (suppress handoff); CR-3 input weighting (drift is context-cue-only for A4); CR-4 tiebreak (Critic-internal preference on ties); CR-5 evidence-label propagation (MIN invariant); CR-6 audit log.

### 3.5 Bus tick protocol

Per window: (1) Perceiver forward, (2) Memory pre-read, (3) Permanence forward, (4) Memory forward with CR-2 gate, (5) Composer forward (per-input), (6) Critic forward with CR-1/CR-3/CR-4 gates, (7) Gate housekeeping (CR-5/CR-6), (8) Output aggregation.

The order is deterministic. Reads of (t-1) state follow the v2.1 forward-reference null protocol.

### 3.6 State ownership

State is owned by exactly one module. Cross-module reads are read-only with evidence-label propagation (CR-5). Cross-module commands use handoff signals with refusal protocol.

| State | Owner | Mutability |
|---|---|---|
| latent_state | Memory | per-window (A1) |
| anchor_set | Memory | per-window (A3) |
| object_track_set | Permanence | per-frame (A6) |
| route_history | Critic | append per A5 |
| capability_card | Composer | static per cycle |

### 3.7 Substrate hypothesis

The hybrid substrate (transformer perception + SSM memory + slot permanence) is v0.1's most falsifiable choice. The claim: per-frame perception is local + parallel (transformers excel); memory is sequential + compressed (SSMs excel); forcing both into one substrate degrades performance. ABL-2 in the ablation plan tests this directly.

### 3.8 v0.2 architecture deltas [cycle 022 — 2026-05-07]

Source: SPEC-20260506-004 (Deltas 1–6); authorized per DEC-20260507-002. Every claim below carries an inline evidence label. v0.1 text in §3.1–3.7 is preserved unchanged.

**Delta 1 — Speed priority + frame budget** (engineering-judgment / inferred):

Speed priority locked: inference real-time PRIMARY (30–50 ms/frame at 30 FPS streaming-first); training fast and integration fast secondary. Per-frame component budget targets:

| Component | Target latency |
|---|---|
| C1 Perceiver (DINOv3-S forward) | 10–15 ms |
| C2 Memory NSA retrieve | few ms (sparse top-k) |
| C3 Permanence slot | few ms (bounded slots) |
| C4 Critic head | few ms (small transformer) |
| C5 Composer route | < 1 ms (table join) |
| C6 Bus tick + handoff | < 1 ms |
| **Total** | **20–25 ms/frame; 5–25 ms reserve for downstream pointmap heads** |

Heavy verification path (EXPERT-07 Test3R) is OFF the streaming path: Critic-triggered lazy invocation only, on flagged tokens, with its own latency budget outside the 30–50 ms streaming envelope. Evidence label: inferred; not measured on dream3r server (TITAN RTX 24GB); NSA hardware-aware kernel benefit may be narrower than published numbers.

**Delta 2 — C1 Perceiver: DINOv3-S replaces ViT-L** (paper-derived / inferred):

v0.1 C1 inherits DUSt3R-lineage ViT-L (~300–700M params). v0.2 default: DINOv3-Small (~22M backbone params, frozen). DINOv3-Base (~85M) is the documented fallback if Small features prove insufficient for downstream pointmap quality. Inferred impact: backbone VRAM fp16 ~600 MB → ~50 MB; forward latency ~50–80 ms → ~10–15 ms. T1/T2/T3 bus publications carry forward unchanged. Evidence: paper-derived for substitution (DINOv3 backward-compatible with DINOv2 usage patterns; published 2025 3R works already use DINOv3 features); inferred for dream3r-server-specific latency (not measured). Risk: DINOv3-S features are semantically oriented; pointmap quality may degrade relative to ViT-L. Mitigation: -B fallback documented; top-N partial unfreezing as ablation candidate.

**Delta 3 — C2 Memory: bounded anchor bank + NSA-style retrieval** (paper-known / speculative):

v0.1 C2 names SSM/Mamba without storage/retrieval spec. v0.2 substantiates C2 as:

(a) Bounded anchor bank (K = 256 proposed; hyperparameter). Each entry: anchor_embedding (D-dim) + scene_pose_metadata + freshness_counter + permanence_link. Eviction: LRU among non-permanence-anchored entries; permanence-anchored entries evict-protected (C3 Permanence owns permanence_link; C2 reads but does not mutate — preserves v0.1 state-ownership invariant).

(b) NSA-style three-branch selective retrieval: compressed branch (long-term scene summary, ~32 tokens) / selected branch (top-k anchor lookup, k = 8 proposed) / sliding branch (last W = 4 frames of evidence). Selection gate co-driven by Critic confidence (C4) and permanence_link (C3). Low Critic confidence biases gate toward retrieving more anchors for verification — this is the structural link between Delta 3 (C2 memory substantiation) and Delta 6 pillar A (Verification-as-architecture): the Critic shapes what the memory retrieves, not only what it accepts.

Mamba SSM retained as optional medium-term layer. Evidence: paper-known for NSA mechanism (DeepSeek 2025, arXiv 2502.11089); speculative for 3R/vision transfer (no published vision use of NSA); speculative for cross-module-signal claim (Critic + Permanence co-driving the selection gate).

**Delta 4 — Sparse attention as architectural optimization** (paper-known / speculative):

NSA-style token-level sparse attention is the C2 Memory selection-gate substrate and the Composer routing axis (per-expert attention_regime). This is an engineering optimization, NOT a paper main claim.

Per-module attention regime (v0.2):

| Module | Attention regime |
|---|---|
| C1 Perceiver | Full (DINOv3-S backbone; per-frame) |
| C2 Memory | NSA three-branch (sparse + compressed + sliding) |
| C3 Permanence | Full within bounded slot set |
| C4 Critic | Full (small head) |
| C5 Composer | Routing logic; no attention in C5 itself; per-expert varies |
| C6 Bus | N/A (dataflow, not compute) |

Evidence: paper-known for NSA story (LLM domain); speculative for per-module assignment in 3R.

**Delta 5 — C5 Composer pool: 7 admitted lightweight experts** (paper-known / inferred / engineering-judgment):

v0.1 lists 5 backbones at coarse granularity. v0.2 admits exactly 7 lightweight experts with finer-granularity capability descriptors (full descriptors in planning/COMPOSER_CAPABILITY_DESCRIPTORS.md):

| Expert | Role | Params | Attention |
|---|---|---|---|
| EXPERT-01 MASt3R | Pair / matching head | ~300M | full |
| EXPERT-02 Fast3R | Many-view single forward | ~580M | full |
| EXPERT-03 Spann3R | Streaming spatial anchor | ~250M | full |
| EXPERT-04 CUT3R | Online persistent state | ~300M | full |
| EXPERT-05 MoGe-2 | Mono pointmap recovery + bootstrap | ~200M | full |
| EXPERT-06 DepthAnything-V2 | Mono depth cheap prior | ~25M (S) | full |
| EXPERT-07 Test3R | Lazy test-time verification (off streaming path) | backbone+iter | full+iter |

Excluded (engineering-judgment; not retired): VGGT (~1.2B), MapAnything (too heavy for streaming). VGGT remains a known out-of-pool comparator whose offline-batch performance is a threat to pillar D (see §6.2).

Routing policy sketch (inferred v0.2; sub-millisecond table join in C5):

- first-frame / tracking-lost → EXPERT-05 + EXPERT-06 (mono recovery + cheap prior in parallel)
- N ≥ 4 views, budget allows → EXPERT-02 (avoid O(N²) pair fusion)
- streaming, prior state ok → EXPERT-03 and/or EXPERT-04 (best-of-N; pillar D primary demonstration)
- loop-closure pair candidate → EXPERT-01 (matching)
- Critic flag OR retrieval conflict → EXPERT-07 Test3R lazy off streaming path (pillar A primary demonstration)

Added routing axis: attention_regime per expert (full/linear/sparse) joins the v2.1 cross-spec contract's capability_match vector.

**Delta 6 — Main claim narrowing** (user-decided; agent-recommended):

v0.1 carries 5+ candidate innovations in parallel. v0.2 paper main-claim narrows to TWO PILLARS:

**Pillar A — Verification-as-architecture**: The Critic gate is a STRUCTURAL write-blocker wired into the bus (CR-1, CR-2 gates from v0.1) and into the Memory selection gate (Critic confidence biases retrieval; Delta 3). Test-time verification (EXPERT-07 Test3R) is invoked only when the Critic flags a region — verification at ARCHITECTURE LAYER, not at TRAINING LAYER.

**Pillar D — Heterogeneous best-of-N Composer**: Routing exploits NON-uniform infrastructure across 7 lightweight 3R foundation models. An explicit routing layer over heterogeneous experts beats any monolithic backbone in expected regret. route_regret is the first 3R-specific routing falsification axis.

Supporting (not deleted; not in main claim): Pillar E — Identity-anchored memory (Permanence × Memory coupling via permanence_link in Delta 3 selection gate; supports A and D by providing the cross-module signal mix that makes verification + routing semantically grounded).

Demoted to discipline / future (not deleted; per DEC-20260504-002 no-all-in): Pillar B (state-ownership invariant) → carried as discipline rule; Pillar C (A7/A8 reservation tokens) → reserved bus surfaces only; not designed in v0.2.

### 3.9 Pipeline demonstration [cycle 024 — 2026-05-08]

> **Evidence boundary correction [v1.4, cycle 026]**: this section contains bounded component measurements and an untrained pipeline trace. It upgrades some engineering facts from inferred to measured/demonstrated, but it does NOT validate C2 memory quality, reconstruction quality, routing quality, pillar A, pillar D, or C2 Memory v0.3. SPEC-20260508-001 supersedes the v0.2 C2 mechanism below as the current memory design.

We run the full Dream3R v0.2 control-graph pipeline on a pair of DTU scan24 images (224x224) using the `dinov2_s` preset (DINOv2-S frozen backbone, 21.6M + 7.8M trainable = 29.5M total params) on a single NVIDIA TITAN RTX 24GB.

**Pipeline trace (untrained model, single window):**

| Stage | Module | Output | Measured |
|---|---|---|---|
| C1 Perceiver | DINOv2-S (frozen) + trainable heads | 257 tokens x 768d per frame | 29.5M params (measured) |
| C2 Memory | GRU + AnchorBank + NSA | A1: reset (first frame); 1 anchor stored | engineering-demonstrated plumbing; superseded as current memory design by SPEC-20260508-001 |
| C3 Permanence | Slot attention (16 slots) | 13 admit / 3 suppress / 0 defer | dynamic_ratio=0.47 |
| C4 Critic | Transformer encoder | conflict=-0.36 → accept | no reroute triggered |
| C5 Composer | Regime classifier + table join | route_regret=0.00 (untrained) | selects DepthAnything-V2 |
| Expert | DepthAnything-V2 Small (24.8M) | depth 518x518 | **24.3 ms** (measured) |

**Measured latency (TITAN RTX 24GB, fp16):**

| Component | Measured | Budget target | Verdict |
|---|---|---|---|
| DepthAnything-V2 Small | 24.3 ms / image | < 30 ms | PASS |
| MASt3R ViT-Large (pair) | 342 ms / pair | off-streaming | expected |
| Test3R (DUSt3R base, pair) | 341 ms / pair | off-streaming (lazy) | expected |

**Routing decision logic demonstrated:**

The Critic evaluates conflict_score from 17 evidence signals. Low conflict (< 0) → accept → streaming-path expert (DepthAnything-V2). High conflict → reroute → lazy off-streaming expert (Test3R or MASt3R). This is pillar A (Verification-as-architecture) in action: the Critic gate structurally determines which expert runs, not a training-time loss.

**Bounded evidence label changes from this demonstration:**

| Claim | Previous label | New label |
|---|---|---|
| DINOv2-S backbone params (~22M) | inferred | measured (21.6M) |
| DINOv2-S backbone frozen | inferred | measured (174 param tensors, requires_grad=False) |
| DepthAnything-V2 latency (< 30 ms) | inferred | measured (24.3 ms TITAN RTX) |
| MASt3R pair latency | paper-derived | measured (342 ms TITAN RTX) |
| AnchorBank occupancy growth per window | inferred | engineering-demonstrated (1 → 2 → 3 → 4 → 5 over 5 windows; vector bank plumbing only) |
| NSA three-branch forward | speculative | engineering-demonstrated (gate weights functional; Critic confidence bias operative; not a validated 3R memory mechanism) |
| Bus contract log (3 cross-module reads) | architecture-novel | demonstrated (dynamic_ratio→memory, capability_match→critic, drift→critic) |
| Pipeline end-to-end on real images | none | demonstrated (DTU scan24 pair → depth output) |

**What this demonstration does NOT prove:**

- Reconstruction quality (model untrained; pointmap/depth values are random projections)
- Routing quality (Composer capability_match is uniformly initialized; route_regret=0)
- Streaming performance (single window only; no multi-window streaming test with real data)
- Pillar A Critic discrimination (untrained Critic accepts everything; ABL-v02-10 needed)
- C2 memory quality (v0.2 vector AnchorBank/NSA plumbing is superseded by SPEC-20260508-001 for v0.3)
- C2 Memory v0.3 (not implemented, not run, not trained, not measured)
- Pillar D best-of-N advantage (needs trained regime classifier; ABL-v02-4 needed)

## 4. A1-A8 action mapping

Each action from the taxonomy maps to a specific module, concrete layer, trigger condition, and bus signals:

| Action | Module | Layer | Bus writes | Bus reads |
|---|---|---|---|---|
| A1 State Update | Memory C2 | 5-way classifier + gate | latent_state, policy_log | pose_novelty, dynamic_ratio |
| A2 Memory Write | Memory C2 | 4-way write head | static_map writes | suppress_static_write (CR-2) |
| A3 Anchor Budget | Memory C2 | anchor + cache controller | anchor_set | anchor_importance, cache_pressure |
| A4 Verification | Critic C4 | scalar regression | conflict_score | T3 evidence subset |
| A5 Repair | Critic C4 | 5-way classifier | route_history | capability_match (CR-1 gated) |
| A5 Routing | Composer C5 | table join | route_recommendation | regime_card, route_history |
| A6 Dynamic Split | Permanence C3 | 3-way + identity head | object_track_set, suppress handoff | T2 pointmap, T3 subset |
| A7 Prior | Reserved | bus hook only | (none in v0.1) | (would read prior_rgb_conflict) |
| A8 Active | Reserved | bus hook only | (none in v0.1) | (would read uncertainty_area) |

## 5. Planned experiments

### 5.1 Ablation plan overview

10 ablations in 3 priority tiers, designed so each architectural claim has a specific kill condition:

**Tier 1 (must-run):**
- ABL-1: Bus removal (flat baseline). Kill: flat matches full on 4+/6 metrics.
- ABL-2: Substrate hypothesis (hybrid vs transformer-only vs SSM-only). Kill: single-substrate matches hybrid.
- ABL-3: Gradient isolation (stop_gradient on cross-spec reads vs free flow). Kill: isolated is worse on all metrics.

**Tier 2 (should-run):**
- ABL-4..7: Per-module removal (Critic, Memory, Permanence, Composer).

**Tier 3 (refinement):**
- ABL-8: Per-CR-rule ablation (6 sub-experiments).
- ABL-9: Evidence signal leave-one-out (17 signals).
- ABL-10: Training loss weight sensitivity.

### 5.2 Benchmark categories

- B1: Static pair (sanity check)
- B2: Many-view static (anchor retention)
- B3: Long dynamic video (drift + pollution)
- B4: Mixed-regime batch (route regret)
- B5: Hard-case ambiguity (conflict detection)
- B6: Adversarial CR-triggering (bus verification)

### 5.3 Proxy metrics

- P1: Conflict detection rate + false alarm rate
- P2: Anchor retention (protected important / total important)
- P3: Memory growth + reuse rate
- P4: Dynamic pollution (static-map purity)
- P5: Route regret (cost-adjusted, per-regime)
- P6: Action entropy (controller validity guard)

## 6. Comparator positioning

> **[v0.2 delta — cycle 022 — 2026-05-07]** Section 6 restructured for v0.2 main-claim A+D framing (DEC-20260507-002; source: SPEC-20260507-001 — v0.2 comparator map addendum). §6.0–6.3 are new v0.2 content. §6.4 preserves the v0.1 threat table (cycle 017) for traceability per Discipline rule 5.

### 6.0 v0.2 positioning framing

v0.2 main-claim narrows to two pillars (Delta 6, SPEC-20260506-004):

- **Pillar A** — Verification-as-architecture: Critic gate as structural write-blocker wired to bus (CR-1/CR-2); NSA selection gate biased by Critic confidence; EXPERT-07 Test3R invoked lazily off streaming path when Critic flags a region.
- **Pillar D** — Heterogeneous best-of-N Composer: 7 admitted lightweight experts; route_regret as the first 3R-specific routing falsification axis; no single backbone covers all regimes well.

Threat analysis and comparator positioning are now anchored to A+D only. Pillars B (state-ownership invariant) and C (reservation tokens A7/A8) are discipline/future-work items, not paper novelty claims. Pillar E (identity-anchored memory) is a supporting mechanism for A and D.

### 6.1 Composer pool — 5-tier structure (v0.2)

Source: SPEC-20260507-001 §"5-tier pool reorganization"; Delta 5 (SPEC-20260506-004).

| Tier | Models | Basis |
|---|---|---|
| In-pool (7) | MASt3R, Fast3R, Spann3R, CUT3R, MoGe-2, DepthAnything-V2, Test3R | Streaming-compatible, lightweight; admitted per Delta 5 |
| Out-of-pool (3) | VGGT, MapAnything, Kimi-KDA | Exceed streaming budget (VGGT ~1.2B; MapAnything heavy) or LM-to-3R transfer not pursued (Kimi-KDA) |
| Out-of-scope (1) | ViT-L | Replaced as C1 backbone by DINOv3-S (Delta 2); no longer a comparator |
| Foundation (1) | DUSt3R | Parent lineage; not a competitor; Dream3R builds on it |
| Orthogonal (8) | MonST3R, POMATO, D²USt3R, Easi3R, RayMap3R, SLAM3R, TTT3R, Mamba-3R | Single-axis overlap; not Composer-pool candidates |

Most significant reclassification from v0.1: Spann3R moves from HIGH threat to IN-POOL. Spann3R's spatial anchor streaming is an implementation substrate Dream3R exploits as EXPERT-03, not a competing approach. Evidence: paper-derived (Spann3R capability profile); engineering-judgment (pool admission).

### 6.2 Threat ranking against pillars A + D (v0.2)

Source: SPEC-20260507-001 §"Updated threat ranking against v0.2 main-claim A + D".

| Pillar | Threat | Model | Threat axis | Dream3R differentiation |
|---|---|---|---|---|
| A (Verification-as-arch) | HIGH | Test3R | Built-in verifier head could substitute for C4 Critic + EXPERT-07 lazy path | Dream3R's Critic is a structural gate (CR-1/CR-2) driving Memory retrieval (Delta 3 NSA gate); Test3R verifier is single-model-scoped; Dream3R crosses model families at inference time |
| A | MEDIUM | TTT3R | Test-time training on confidence drop triggers revision | Dream3R uses Critic gate (no re-training); broader A5 action set (5-way repair classifier) |
| D (Heterogeneous best-of-N) | HIGH | VGGT | Single feed-forward backbone strong on offline batch; no routing needed | VGGT out-of-pool (exceeds streaming budget; engineering-judgment); pillar D offline-batch framing is an open gap: ABL-v02-4 + Q2 open question acknowledge this; no measured numbers claimed |
| D | MEDIUM | CUT3R | Strong single streaming expert; online persistent state | CUT3R is IN the pool (EXPERT-04); Dream3R's Composer runs best-of-N ACROSS CUT3R + 6 other experts; single-expert coverage = no route_regret axis |
| D | MEDIUM | Spann3R | Spatial anchor streaming; v0.1 HIGH threat | Reclassified in-pool (EXPERT-03); see §6.1 note |

Evidence discipline: all threat claims are paper-derived from published abstracts/results; no measured route_regret numbers exist (inferred from capability descriptors; not measured on dream3r server).

### 6.3 Three new comparison axes (v0.2)

Source: SPEC-20260507-001 §"New comparison axes (Axis 9–11)".

| Axis | What it measures | v0.2 relevance |
|---|---|---|
| Axis 9 — NSA-style sparse attention | Whether model uses token-level sparse attention for memory retrieval | C2 Memory uses NSA three-branch; no published 3R model uses NSA-equivalent (paper-known for LLM domain; speculative for 3R transfer) |
| Axis 10 — DINOv3 backbone tier | S / B / L weight class for perception backbone | C1 = DINOv3-S (~22M frozen) default; comparators using ViT-L lineage are heavier; DINOv3-B used by some 2025 3R works |
| Axis 11 — Composer expert pool | Number of heterogeneous experts admitted; attention_regime variety | Dream3R = 7 experts (full/full/full/full/full/full/full+iter); no published 3R paper has a multi-expert routing pool with route_regret falsification axis |

### 6.4 v0.1 comparator positioning (cycle 017 — preserved for traceability)

v0.1 framing below is the cycle 017 (DEC-20260506-001) text. It is preserved unchanged per Discipline rule 5. It uses full-architecture-level threat tiers, not the A+D-pillar-specific framing of §6.2 above.

Dream3R is NOT a competitor at any single substrate axis. It is a control graph that REUSES existing 3R substrates as its modules. The novelty is the graph + bus + gates.

Threat ranking by novelty overlap:

| Tier | Models | Threat axis | Dream3R differentiation |
|---|---|---|---|
| HIGH | Spann3R, LONG3R/LongStream/LoGeR, VGGT | Persistent memory; long-sequence; strong single-pass | A1 multi-mode update; bus + CR-rules; multi-module control |
| MEDIUM | CUT3R/STream3R, Test3R, MonST3R, SLAM3R, Mamba-3R | Single-axis overlap | Broader action set; explicit bus; composable modules |
| LOW | DUSt3R, MASt3R, Fast3R, TTT3R, MapAnything, 4DGS | Foundation or orthogonal | Dream3R builds on these, does not compete |

## 7. Discussion

### 7.1 Evidence status

The aggregate evidence distribution of Dream3R v0.2/v0.3 (corrected cycle 026):

- ~5 elements paper-proven (perception substrate, token outputs, per-frame dynamic split, slot attention outside 3R)
- ~5 elements paper-derived (SSM-for-3R-memory, Critic substrate pattern, Composer routing pattern)
- ~10 elements inferred (per-action heads, per-module compositions, substrate hypothesis)
- ~7 elements architecture-novel (bus, CR-1..CR-6 as gates, substrate composition)
- 2 elements speculative (A7/A8 reserved hooks)

> **[v1.4 evidence-boundary correction - cycle 026 - 2026-05-08]** Cycle 024 measurements are bounded:
> - parameter counts and component latencies may be labeled `measured`
> - AnchorBank/NSA/Bus behavior may be labeled `engineering-demonstrated` for plumbing only
> - C2 memory quality, reconstruction quality, routing quality, and C2 v0.3 remain unvalidated
> - SPEC-20260508-001 supersedes v0.2 Delta 3 as the current memory design
> - Architecture-novel elements remain highest risk until memory-specific prototype and ablation execution

### 7.2 Limitations

1. No training has been conducted. All parameter counts and performance expectations are inferred.
2. The substrate hypothesis (hybrid > single-substrate) is untested; ABL-2 is the critical experiment.
3. If ABL-1 (bus removal) shows the bus is inert, the architecture story collapses to "modular composition with conventions."
4. A7 (Cross-Modal) and A8 (Active Perception) are reserved hooks, not designed mechanisms.
5. Object_track_set identity consistency has no 3R-specific training target; the loss function is speculative.
6. The 17-signal evidence vector V1 may contain redundant signals; ABL-9 tests this.
7. CR-rule firing rates on natural benchmarks are unknown; adversarial B6 inputs may be needed to demonstrate bus utility.

### 7.3 Risks

- R1: Substrate hypothesis falsification at training time
- R2: Bus-as-novelty collapse if CR-rules never fire
- R3: State-ownership invariant violation under gradient flow
- R5: Storytelling vs measurement asymmetry
- R7: "Control graph" framing may be read as "modular composition" without the bus gates

## 8. Conclusion

Dream3R proposes that the bottleneck for hard 3R cases is not a better encoder but a missing control vocabulary over memory, verification, dynamics, and routing. The architecture makes this vocabulary first-class: four modules sharing a typed memory bus with conflict-resolution gates. Every architectural claim maps to a falsifiable ablation experiment.

The contribution is the graph — not any single node.

---

## Evidence discipline notes

```text
- Every section carries evidence labels per Discipline rule 5
- No measured quality or architecture-performance claim is made
- Comparator claims are restricted to what papers report in
  abstracts/results
- Four finalists are treated as parallel modules, not contestants
  for a single thesis spine (DEC-20260504-002 still in force)
- Dream3R remains a candidate, not final thesis
  (DEC-20260501-004 still in force)
```

## Version history

```text
v1  2026-05-06  cycle 017. Architecture-centric paper rewrite per
                DEC-20260506-001. Central contribution = Dream3R
                architecture (control-graph-as-architecture). Sections
                1-8 drafted. Supersedes PAPER_PHASE2_BLUEPRINT.md as
                primary paper artifact. No training; no measured
                results; all claims carry evidence labels.

v1.2  2026-05-07  cycle 022. Section 3 + Section 6 updated for v0.2
                A+D framing per DEC-20260507-002. §3.8 added:
                six v0.2 architecture deltas (source: SPEC-004
                Deltas 1–6). §6.0–6.3 added: v0.2 comparator
                positioning (5-tier pool, A+D threat table, 3 new
                axes; source: SPEC-20260507-001). §6.4 = v0.1
                threat table preserved for traceability. Sections
                1, 2, 4, 5, 7, 8 unchanged. Source anchors updated
                to include v0.2 specs.

v1.3  2026-05-08  cycle 024. §3.9 pipeline demonstration added:
                first measured/demonstrated evidence from server-
                side deployment. 8 evidence labels promoted (see
                §3.9 table). DepthAnything-V2 latency measured
                24.3ms (PASS). MASt3R 342ms / Test3R 341ms
                measured (off-streaming). DINOv2-S 21.6M frozen
                measured. AnchorBank + NSA + Bus demonstrated on
                real DTU images. §7.1 evidence status updated.
                Honest "what this does NOT prove" section added.

v1.4  2026-05-08  cycle 026. Evidence-boundary correction after
                SPEC-20260508-001 C2 Memory v0.3 addendum. Cycle
                024 measurements remain valid only for component
                latency, parameter counts, adapter availability, and
                untrained pipeline plumbing. AnchorBank/NSA evidence
                relabeled as engineering-demonstrated plumbing, not
                validated C2 memory quality. C2 v0.3 not implemented
                or measured.
```
