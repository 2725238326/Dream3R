# SPEC-20260506-001 Dream3R architecture v0.1

## Identity

spec_id: SPEC-20260506-001

branch_name:

```text
Dream3R / control-graph-as-architecture
```

date: 2026-05-06

status: draft v0.1 (cycle 016 S2; markdown only; no training, no GPU runs, no checkpoint creation; candidate per DEC-20260501-004)

cycle_of_origin: cycle 016 (mainline architecture-first; seeded by DEC-20260506-001)

supersedes: none (this is the first architecture spec; the 4 finalist specs SPEC-20260503-001..003 + SPEC-20260504-001 are mechanism specs, not architecture specs, and are NOT superseded by this file. They are INPUTS to this file.)

candidate_status:

```text
v0.1 is a candidate architecture proposal per DEC-20260501-004 (Dream3R is
candidate, not final thesis). The architecture can still be revised,
replaced, or merged with another candidate in a later cycle. v0.1 carries
a working substrate hypothesis (hybrid transformer + SSM + cross-spec
memory bus) chosen at S2 launch time; alternative substrate hypotheses
(pure SSM; transformer-only with slot memory) are NOT superseded by v0.1
and remain re-openable in v0.2 or a sibling spec.
```

## Approval

user_approval_for_architecture_spec_drafting: yes

approval_decision_id: DEC-20260506-001 (mainline architecture-first)

approval_note:

```text
DEC-20260506-001 redefines the Dream mainline as architecture-first: the
PRIMARY output is a markdown architecture spec + ablation plan + comparator
map. Paper Phase 2 blueprint is now SUPPORT, not primary. This spec is the
S2 deliverable seeded by that DEC.

DEC-20260506-001 explicitly authorizes design + ablation planning, NOT
training, NOT GPU ablation runs, NOT checkpoint creation. v0.1 contents
respect that boundary: every concrete number (parameter count, dimension,
layer count, schedule) is `inferred` or `paper-derived`, never `measured`,
because no training run has been authorized.

DEC-20260501-004 (Dream3R candidate-not-final) and DEC-20260504-002
(no-all-in any single finalist) BOTH still apply. The architecture must
(a) remain a candidate that can be revised or replaced and (b) preserve all
4 finalist mechanisms as composable modules, not collapse into one.
```

## Scope of v0.1

what v0.1 IS:

```text
- A markdown design pass synthesizing the 4 finalist specs
  (SPEC-20260503-001 Critic / SPEC-20260503-002 Memory /
  SPEC-20260503-003 Permanence / SPEC-20260504-001 Composer) into a
  single coherent architecture proposal.
- A token / state / core / read-write-protocol description that any
  future implementer could turn into PyTorch modules.
- A mapping of the A1-A8 actions in `planning/ACTION_TAXONOMY_AND_PROXY_
  METRICS.md` to specific layers, heads, or routes inside the
  architecture.
- A re-rendering of the v2.1 cross-spec signal contract
  (`paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md`) as an internal runtime API
  (the "memory bus") with publish / read / handoff semantics.
- A training-objective sketch: which losses would correspond to which
  proxy metrics if Dream3R were ever trained. The sketch is for
  ablation-plan input only.
- Per-section evidence labels (`paper-derived` / `inferred` /
  `architecture-novel` / `speculative`) per Discipline rule 5.
```

what v0.1 IS NOT:

```text
- Not a training authorization. No training run is implied or planned.
  See "Boundaries" section.
- Not a final thesis. Per DEC-20260501-004 it remains a candidate.
- Not a single-mechanism design. Per DEC-20260504-002 it preserves all
  four finalist mechanisms as composable modules.
- Not a comparator map. The lightweight comparator placeholder in this
  file is a stub; the full comparator map is the cycle 016 S4
  deliverable.
- Not an ablation plan. The training-objective sketch and load-bearing
  module flags here are inputs to the cycle 016 S3 ablation plan, not
  a substitute for it.
- Not an architectural spine for future Cross-Modal A7 or Active
  Perception A8 work. v0.1 reserves bus hooks for those but does NOT
  design them. They remain blocked pending separate user direction.
- Not a measured-performance claim. Every operational number is
  `inferred` or `paper-derived` per Discipline rule 5.
```

## The architectural claim

claim_paragraph:

```text
A 3R model is not just a perception backbone. The bottleneck for hard
3R cases (long sequence, dynamic content, fragmented model ecology,
geometric ambiguity) is not "a better encoder" but "a missing control
vocabulary over memory, verification, dynamics, and routing." Dream3R
makes that control vocabulary first-class architecture. The four
finalist mechanisms (Critic / Memory / Permanence / Composer) are
re-cast as four modules sharing a single cross-spec memory bus. The
bus carries the v2.1 cross-spec signal contract as its runtime API.
Conflict resolution rules CR-1..CR-6 become gating logic at the bus.
The evidence signal vector V1 becomes a fixed-width tensor projected
from token streams. The result is a control-graph-as-architecture: the
architectural artifact is the GRAPH (modules + bus + gates), not any
single module.
```

one_line_thesis:

```text
3R needs a control graph, not a bigger backbone.
```

what is architecturally novel here (not in any single source mechanism):

```text
1. The bus itself. Existing 3R models have implicit cross-module
   signals (anchor sets in Spann3R, cache in OVGGT, conflict scores
   in Test3R). v0.1 makes the bus EXPLICIT and FORMAL: signal owner
   table from CROSS_SPEC_SIGNAL_CONTRACT.md becomes a runtime tensor
   schema, not an implicit data flow.

2. The gates. CR-1..CR-6 conflict resolution rules become first-class
   architectural elements (gate modules), not embedded conditionals
   inside one mechanism's forward pass. CR-2 (Permanence
   suppress_static_write is binding on Memory) becomes a hard mask;
   CR-1 (Critic A5 reroute requires Composer agreement) becomes a
   spread-thresholded gate; CR-5 (evidence-label propagation) becomes
   a typed-tensor invariant.

3. The substrate split. Per-frame perception (transformer; DUSt3R /
   MASt3R / VGGT / Test3R lineage) and long-sequence executive memory
   (SSM; Spann3R / CUT3R / STream3R / Mamba-3R lineage) live in
   DIFFERENT computational substrates inside one architecture. v0.1's
   working hypothesis is that this split is load-bearing: per-frame
   work is local + parallel (transformers are good at that); memory
   work is sequential + compressed (SSMs are good at that); forcing
   either into a single substrate (transformer-only or SSM-only) is
   what makes existing 3R models tilt toward one regime or the other.

4. The reserved hooks. v0.1 leaves explicit empty slots on the bus
   for A7 Prior / Modality Arbitration (Cross-Modal) and A8 Evidence
   Acquisition / Adaptation Budget (Active Perception). The
   architecture does NOT design them, but it does NOT hard-code their
   absence either. This means a future Cross-Modal or Active spec can
   plug in without rewriting the bus.

5. The separation of routing from repair. A5 is split between
   Composer (routing facet) and Critic (repair facet) per cycle 008.5
   A5 split. v0.1 carries that split into the architecture: Composer
   is parameter-free (table join over capability cards), Critic is
   parametric (small head over evidence tokens). They cooperate via
   route_recommendation / route_history / capability_match tensors
   on the bus. CR-1 enforces the cooperation.
```

what is NOT architecturally novel here (carried from existing work):

```text
- The transformer perception backbone itself: same family as DUSt3R /
  MASt3R / VGGT / Test3R; v0.1 does NOT redesign the per-frame
  encoder. v0.1's claim is about WHAT IS ATTACHED to a perception
  backbone, not the backbone's internals.
- The SSM / Mamba style memory state: paper-proven by
  Spann3R / CUT3R / STream3R / Mamba-3R / LongStream / LONG3R /
  LoGeR. v0.1 inherits that primitive and applies it to the executive
  memory module.
- The dynamic / static split per frame: paper-proven by
  MonST3R / POMATO / D^2USt3R / Easi3R / RayMap3R. v0.1's Permanence
  module inherits the per-frame split mechanism and adds the
  persistent object_track_set on top.
- Capability cards and routing tables: cross-domain analogs in MoE
  routing literature. v0.1's Composer is the 3R-specific application
  of card-based routing; the routing primitive itself is not novel.
- Evidence-vector-conditioned policies: cross-domain analogs in
  CTRL-style critic-revision (LM domain) and reward-model gating.
  v0.1 applies the primitive to 3R-specific signals.
```

## Substrate hypothesis (v0.1 working assumption)

substrate_choice: hybrid (transformer perception + SSM/Mamba executive memory state + slot memory for Permanence + cross-spec memory bus)

substrate_choice_evidence_label: inferred (architecture-novel composition; substrates individually paper-proven)

per-substrate justification:

```text
1. PERCEPTION SUBSTRATE = transformer
   Why:
     - DUSt3R / MASt3R / VGGT / Test3R / MapAnything all use
       transformer encoders for per-frame or per-pair work.
     - Per-frame perception is local (within-image) + parallel
       (across patches); transformer attention is the default tool.
     - Pretrained ViT / CroCo encoders give a warm-start path
       (relevant only at L4 model-change time; not authorized in
       v0.1).
   Carries lineage from:
     CroCo, DUSt3R, MASt3R, VGGT, Test3R, MapAnything.
   Evidence label: paper-proven (per-frame perception transformer is
     the dominant 3R primitive in 2025-2026 literature).

2. EXECUTIVE MEMORY SUBSTRATE = SSM / Mamba
   Why:
     - Spann3R / CUT3R / STream3R / LONG3R / LoGeR / LongStream all
       maintain a persistent compressed state across a long input
       sequence. Attention over the full history is O(N^2) and
       infeasible past a few hundred frames; SSM is O(N) and
       compresses naturally.
     - Mamba-style selective SSMs add input-dependent gating which
       maps cleanly to A1 (state update control: full / pose-adaptive
       / Kalman / skip / reset).
     - The executive memory mechanism is INFORMATION-COMPRESSED
       memory (latent state) NOT enumerable memory (anchor set);
       v0.1 splits these (see "State ownership" below).
   Carries lineage from:
     Spann3R, CUT3R, STream3R, LONG3R, LongStream, Mamba, Mamba-3R.
   Evidence label: paper-derived (SSM-for-3R-memory is published in
     several 3R papers; Mamba-style selective gating tied to A1 is
     architecture-novel composition).

3. PERMANENCE SUBSTRATE = slot memory (transformer-readable)
   Why:
     - Object identity is SET-typed (a finite, evolving set of
       objects), not sequence-typed. Slot attention / slot memory
       handles set-typed state cleanly.
     - The per-object record {object_id, last_seen_t, last_position,
       identity_confidence} fits a slot exactly.
     - Slot updates can be per-frame; reads can be cross-attention
       from any other module.
   Carries lineage from:
     Slot Attention, OVGGT (anchor protection idea), MonST3R object
     tracks (per-frame), Permanence spec SPEC-20260503-003 owned A6.
   Evidence label: inferred (slot-memory-for-3R-object-permanence
     is architecture-novel; slot attention itself is paper-proven in
     non-3R domains).

4. CRITIC SUBSTRATE = small transformer head
   Why:
     - Critic reads the evidence tokens (projection of V1 vector)
       and emits scalar conflict_score plus discrete recommended
       action. This is light: ~1-2 transformer blocks suffice.
     - Reading per-window evidence + per-frame outputs needs
       attention (different windows have different evidence
       structure).
     - A4 verification and A5 repair facet both fit one head with
       a small action-classifier on top.
   Carries lineage from:
     Test3R verifier head, TTT3R trigger head, CTRL critic head
     (LM domain).
   Evidence label: inferred (small-head-Critic on V1 tokens is
     architecture-novel; verifier-head-on-3R is paper-proven).

5. COMPOSER SUBSTRATE = parameter-free table join
   Why:
     - Composer reads sample_regime_card (per-input metadata) and
       capability_card collection (per-model paper-derived
       characteristics); it computes capability_match by a weighted
       dot product. There are no parameters to learn at L1.
     - A learned router would be a v0.2 candidate (DEC-20260504-002
       no-all-in still applies; learned router needs separate user
       authorization).
     - Parameter-free Composer keeps the architecture L4-
       reproducible: someone could run Dream3R inference using the
       table join alone, which matters for the demo storyboard
       fidelity.
   Carries lineage from:
     MoE routing tables (LM / vision domain), capability-card style
     systems (mixture-of-engineers, broker patterns).
   Evidence label: paper-derived (table-based routing is well known;
     3R-regime-typed routing is architecture-novel).

6. THE BUS SUBSTRATE = explicit tensor schema (no parameters)
   Why:
     - The v2.1 cross-spec signal contract is a typed tensor schema
       at runtime: each cross-spec signal becomes a fixed-shape
       tensor with a producer module, consumer module(s), evidence
       label, and contract type (read-only / handoff / no-cross).
     - The bus is implemented as a "blackboard" pattern: each module
       publishes its outputs to a dictionary keyed by signal name;
       consumers read with assertion that the producer label is in
       the expected set.
     - Conflict resolution rules CR-1..CR-6 are compiled into gate
       modules that read from the bus and write back gating tensors.
       CR-2 (suppress_static_write binding on Memory) becomes a
       hard-mask write at the Memory write head; CR-1 (Critic A5
       reroute requires Composer agreement) becomes a Boolean gate
       on Critic A5 logits; etc.
   Carries lineage from:
     Blackboard architectures (classical AI), publish-subscribe
     patterns, typed-tensor frameworks.
   Evidence label: architecture-novel (3R-specific cross-spec signal
     bus with CR-rules-as-gates is not in any source).
```

what would falsify v0.1's substrate choice:

```text
- If at S3 ablation plan time we cannot identify a clean falsifying
  experiment that distinguishes "transformer-only with slot memory"
  from "transformer + SSM hybrid", the substrate hypothesis weakens.
- If a future cycle 017+ training run (NOT authorized in v0.1) shows
  pure SSM stack matching or beating the hybrid on the same
  benchmark with same parameter budget, v0.1 is falsified at the
  substrate level (the modular mapping survives but the substrate
  story does not).
- If the bus itself reduces to a single concatenated tensor with no
  CR-rule gates ever firing on benchmark inputs, the bus-as-novelty
  claim weakens; the architecture would still work but the paper
  story would have to retreat to mechanism composition rather than
  bus-as-architecture.
```

## Top-level architecture (block diagram)

block_diagram_evidence_label: inferred (composition is architecture-novel; individual blocks are paper-derived)

```text
                                Dream3R v0.1
                       control-graph-as-architecture

  +----------------+       +---------------------+       +----------------+
  |  raw frames    |  -->  |   Perceiver         |  -->  | per-frame      |
  | (image patches)|       | (transformer        |       | pointmap +     |
  |                |       |  per-frame backbone;|       | confidence +   |
  |                |       |  DUSt3R / MASt3R /  |       | pose +         |
  |                |       |  VGGT lineage)      |       | feature tokens |
  +----------------+       +---------------------+       +-------+--------+
                                                                 |
                                                                 v
            +------------------------------------------------------------+
            |                    cross-spec memory bus                   |
            |          (v2.1 contract instantiated as tensor schema)     |
            |                                                            |
            |   evidence tokens (V1 projection; 17 signals)              |
            |   per-spec signals (conflict_score, dynamic_ratio,         |
            |     latent_drift_proxy, anchor_set, object_track_set,      |
            |     capability_match, route_recommendation, ...)           |
            |   handoff signals (suppress_static_write,                  |
            |     admit_static_write, route_recommendation_handoff)      |
            |   gate tensors (CR-1, CR-2, CR-3, CR-4, CR-5, CR-6)        |
            +-+-----------+-----------+-----------+-----------+----------+
              |           |           |           |           |
              v           v           v           v           v
  +-----------+ +---------+ +---------+ +---------+ +---------+
  | Critic    | | Memory  | |Permanen.| |Composer | |reserved |
  | (small    | | (SSM /  | |(slot    | |(table   | |hooks:   |
  |  head;    | |  Mamba; | | memory; | | join,   | |A7 prior |
  |  A4 + A5  | |  A1 +   | | A6;     | | param-  | |A8 active|
  |  repair)  | |  A2 +   | |F2 owned)| | free;   | |perception|
  |           | |  A3;    | |         | | A5      | |         |
  |           | |F1 owned)| |         | | routing)| |         |
  +-----+-----+ +----+----+ +----+----+ +----+----+ +---------+
        |            |           |           |
        |            v           |           |
        |     +------+------+    |           |
        |     | latent_state|    |           |
        |     | anchor_set  |    |           |
        |     | cache_window|    |           |
        |     +------+------+    |           |
        |            |           |           |
        |            v           v           |
        |     +------+-----------+----+      |
        |     | static_map (pointer; |      |
        |     |  Memory store; not   |      |
        |     |  Dream3R-internal)   |      |
        |     +----------------------+      |
        |                                    |
        v                                    v
  +-----+------+                       +-----+------+
  | route_log  |                       | object_    |
  | policy_log |                       | track_set  |
  | pollution_ |                       +------------+
  | log        |
  +------------+

  ledgers (append-only; per-job; bus-readable):
    route_log         (Composer)
    policy_log        (Memory)
    pollution_log     (Permanence)
    critic_report_log (Critic)

  outputs to KYKT advisor / research lane:
    per-window critic timeline
    per-job memory policy summary
    per-job pollution + object-track tables
    per-input regime + capability_match table + route_regret bar

  out of scope v0.1:
    runner integration
    sample_matrix change
    KYKT navigation change
    frontend implementation
    4DGS asset path
    A7 Cross-Modal head
    A8 Active Perception head
```

## Tokens

token_classes_evidence_label: inferred (composition; individual token classes paper-derived)

The architecture works over six classes of tokens. Each class has a fixed shape, an owner module that produces it, and a reader set.

### T1: frame tokens

```text
producer    : Perceiver (per-frame transformer backbone)
shape       : [N_frames, N_patches, d_perceive]
              N_patches inferred 256-1024 per frame depending on resolution
              d_perceive inferred 768 (CroCo / ViT-base) or 1024 (ViT-large)
content     : per-frame image-patch features
readers     : Perceiver self-attention; Permanence cross-attention
              for object detection; Critic small head for evidence
              extraction
lineage     : DUSt3R / MASt3R / VGGT / Test3R / CroCo
evidence    : paper-proven (this token class is the standard 3R
              perception output)
```

### T2: pointmap tokens

```text
producer    : Perceiver pointmap head
shape       : [N_frames, N_patches, 3] for pointmap;
              [N_frames, N_patches, 1] for confidence;
              [N_frames, 7] for camera pose (quaternion + translation)
              when extracted (pose extraction is a separate head;
              architectural placement is in Perceiver per-frame
              output)
content     : per-frame 3D pointmap + confidence + (optional) pose
readers     : Critic A4 head for verification; Memory for state
              update; Permanence for region-level pollution score
              computation; Composer for none directly (Composer reads
              regime card from metadata, not from per-frame
              pointmaps)
lineage     : DUSt3R / MASt3R pointmap convention; VGGT explicit
              pointmap tokens
evidence    : paper-proven (pointmap-as-output is the defining 3R
              primitive)
```

### T3: evidence tokens

```text
producer    : Perceiver auxiliary projection head + cross-module
              projections (Permanence emits dynamic_ratio,
              optical_flow_conflict; Memory emits cache_pressure,
              latent_drift_proxy; etc.)
shape       : [N_windows, N_evidence_signals, d_evidence]
              N_evidence_signals = 17 (per V1 in
              ACTION_TAXONOMY_AND_PROXY_METRICS.md)
              d_evidence inferred 32-64
content     : projected scalar / per-region values for each of the
              17 V1 signals: pose_novelty, view_overlap,
              reprojection_residual, pointmap_conflict,
              confidence_drop, latent_drift_proxy, dynamic_ratio,
              optical_flow_conflict, object_track_stability,
              loop_candidate_score, anchor_importance,
              cache_pressure, external_memory_overlap,
              prior_rgb_conflict, blur_or_low_light_score,
              uncertainty_area, model_capability_match
readers     : Critic A4 head (primary); Memory A1 / A2 / A3 heads
              (read subset per spec); Permanence A6 head (read
              subset); Composer (reads model_capability_match,
              view_overlap, pose_novelty, dynamic_ratio,
              blur_or_low_light_score)
lineage     : V1 vector defined in
              `planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md`
              (cycle 006); 4 finalist specs each declare which
              signals they own / read.
evidence    : inferred (V1 vector itself is inferred per
              ACTION_TAXONOMY; signal definitions are
              paper-derived from comparator literature; bundling
              all 17 into one tensor schema is architecture-novel)
```

### T4: regime token

```text
producer    : Composer regime classifier (parameter-free in v0.1;
              metadata-derived from view_count, motion ratio,
              streaming flag, prior availability)
shape       : [N_inputs, N_regimes]
              N_regimes = 5 in v0.1 (static_pair, many_view,
              dynamic_video, streaming, sparse_view); extensible
content     : per-input probability distribution over regimes
readers     : Composer route_recommendation head; Critic for
              regime-conditioned A5 logic; Memory for regime-
              conditioned A1 update kind; Permanence for regime-
              conditioned theta_dynamic
lineage     : Composer spec SPEC-20260504-001 sample_regime_card
evidence    : inferred (5-regime taxonomy is inferred from
              comparator scope statements; not paper-proven as a
              taxonomy)
```

### T5: anchor + object tokens (slot memory)

```text
producer    : Memory A3 (anchor set) + Permanence A6 (object track
              set)
shape       : [N_anchors_max, d_anchor_slot] + [N_objects_max,
              d_object_slot]
              N_anchors_max inferred 64-128 per job
              N_objects_max inferred 16-64 per job
              d_anchor_slot inferred 128-256
              d_object_slot inferred 128-256
content     : anchor_set: protected memory pointers
                {anchor_id, frame_index, latent_summary,
                 protect_bit, importance_score}
              object_track_set: persistent object identity
                {object_id, last_seen_t, last_position,
                 last_velocity_estimate, identity_confidence,
                 frame_visibility_mask}
readers     : Memory cross-attention (anchors gate eviction);
              Permanence cross-attention (object slots gate
              identity assignment); Critic for context-cue read;
              Composer for none (Composer is parameter-free)
lineage     : Slot Attention (Locatello 2020); OVGGT anchor
              protection; Permanence spec SPEC-20260503-003
              object_track_set; Memory spec SPEC-20260503-002
              anchor_set
evidence    : inferred (slot-memory-as-anchor-and-object-track is
              architecture-novel; slot attention itself is paper-
              proven outside 3R; anchor protection in 3R is paper-
              proven in OVGGT)
```

### T6: bus tokens

```text
producer    : every module (each writes its declared bus signals)
shape       : varies per signal; structured as a typed dict
              indexed by signal_name
              {
                conflict_score:     [N_windows, 1]  + label,
                recommended_action: [N_windows, A]  + label,
                route_history:      [N_windows, K]  + label,
                latent_drift_proxy: [N_windows, 1]  + label,
                anchor_set:         [N_anchors, d]  + label,
                policy_log:         [...]           + label,
                dynamic_ratio:      [N_regions, 1]  + label,
                object_track_stab:  [N_objects, 1]  + label,
                suppress_static_write: bool mask    + label,
                admit_static_write:    bool mask    + label,
                pollution_log:      [...]           + label,
                capability_card:    [N_models, R]   + label,
                sample_regime_card: [N_inputs, R]   + label,
                capability_match:   [N_models, N_in]+ label,
                route_recommendation:[N_inputs, K]  + label,
                route_regret:       [N_windows, 1]  + label,
                ... (CR-1..CR-6 gate tensors are added at the
                 gate modules; see "Conflict resolution as gates")
              }
              every signal carries an evidence_label tag
              propagated per CR-5
content     : the v2.1 contract published-signal table, one tensor
              per signal, per window or per input
readers     : per-spec consumers per the v2.1 signal owner table
              (CROSS_SPEC_SIGNAL_CONTRACT.md "Signal Owner Table")
lineage     : v2.1 cross-spec signal contract, formalized as a
              tensor schema rather than a markdown table
evidence    : architecture-novel (the contract itself is paper-
              derived from the 4 finalist specs; rendering it as
              a runtime tensor schema is novel; CR-rule gates are
              novel)
```

## State ownership

state_ownership_evidence_label: inferred (composition; individual state primitives paper-derived)

State is OWNED by exactly one module. Other modules may READ; only the owner mutates.

| State | Owner | Mutability | Read-by | Lifetime |
|---|---|---|---|---|
| `latent_state(t)` (SSM compressed state) | Memory | per-window (A1) | Critic for read-only context cue | per job |
| `anchor_set(t)` | Memory | per-window (A3) | Permanence (read-only); Critic (read-only) | per job |
| `cache_window(t)` | Memory | per-window (A2 / A3) | Composer (read-only for route_history check); Permanence (none) | per job |
| `policy_log(t)` | Memory | append-only | Composer (informational); cycle audit | per job |
| `object_track_set(t)` | Permanence | per-frame (A6) | Memory (read-only for write decisions); Critic (read-only) | per job |
| `dynamic_field(t)` | Permanence | per-frame, evict after dynamic_horizon | none external | per window |
| `pollution_log(t)` | Permanence | append-only | Composer (informational); cycle audit | per job |
| `route_history(t)` | Critic | append per A5 fire | Composer (read-only) | per window |
| `route_log` | Composer | append per input | none external | per job |
| `critic_report_log` | Critic | append per window | Memory (informational); Permanence (informational) | per job |
| `capability_card(model_id)` | Composer | static for cycle | all (read-only) | per cycle (versioned) |
| `sample_regime_card(input)` | Composer | per-input | all (read-only) | per input |
| `static_map(t)` | external Memory store (NOT Dream3R-internal) | via Memory A2 write head + Permanence handoff (CR-2) | external | inter-job (depends on store contract; out of scope v0.1) |

state_ownership_invariants:

```text
1. No module writes another module's state. Cross-spec mutation
   happens via handoff signals on the bus, not via direct write.
   Permanence's `suppress_static_write(r)` IS a handoff signal that
   Memory MUST honor (CR-2); Permanence does NOT directly mutate
   Memory's static_map.

2. Read-only state is read with evidence-label propagation (CR-5).
   If Memory reads dynamic_ratio from Permanence and dynamic_ratio
   carries label `inferred`, Memory cannot upgrade the resulting
   policy decision to label `paper-proven`.

3. Append-only ledgers (policy_log, pollution_log, route_log,
   critic_report_log) are bus-readable and audit-readable; no
   module deletes from them.

4. Cross-job state propagation is OUT OF SCOPE for v0.1. Memory's
   contract is per-job per the v2.1 contract scope. Cross-job
   memory consolidation requires a separate future contract; if
   added, it would touch the static_map row above (which is the
   only inter-job state pointer in v0.1).

5. The static_map is OWNED EXTERNALLY by the (assumed) Memory
   store. Dream3R-internal modules treat it as a write-only
   pointer for now. The store contract `{write(anchor),
   read(query), merge(a,b), ignore(window)}` is assumed by
   Memory spec SPEC-20260503-002 and remains assumed in v0.1.
```

## Computational cores

cores_evidence_label: inferred (composition; per-core substrates paper-derived)

### C1: Perceiver (transformer per-frame backbone)

```text
input       : raw image patches per frame (T1-input)
output      : T1 frame tokens, T2 pointmap tokens, plus auxiliary
              projection that feeds the evidence-token T3 head
substrate   : transformer (e.g. CroCo / ViT-large with cross-view
              attention for pair / triplet / many-view inputs;
              v0.1 inferred backbone size at d_model = 1024,
              N_layers = 24 for encoder, N_layers = 12 for
              decoder, matching DUSt3R / MASt3R conventions)
parameters  : inferred 300M-700M (matches DUSt3R / MASt3R / VGGT
              ranges; NOT a training claim, this is for
              architecture sizing)
parallelism : per-frame parallel; pair / many-view via cross-view
              attention as in DUSt3R / Fast3R / VGGT
warm_start  : would consume CroCo-pretrained or DUSt3R-pretrained
              weights at L4 model-change time IF training were
              ever authorized (NOT in v0.1 scope)
lineage     : CroCo (Weinzaepfel 2022), DUSt3R (Wang 2024),
              MASt3R (Leroy 2024), VGGT (Wang 2025), Test3R
              (Naver 2025), MapAnything
evidence    : paper-proven (transformer 3R perception backbone)
```

### C2: Executive Memory SSM

```text
input       : per-window summary of T1 frame tokens (pooled or
              attention-summarized) + T3 evidence tokens (relevant
              subset: pose_novelty, confidence_drop,
              latent_drift_proxy)
output      : updated latent_state(t); A1 update_kind label;
              latent_drift_proxy signal published to bus
substrate   : selective SSM (Mamba-style) with input-dependent
              gating
parameters  : inferred 50M-150M (much smaller than perception
              backbone; SSM compresses temporal state densely so
              high width is not needed)
              N_layers inferred 6-12; d_state inferred 256-512
parallelism : sequential along time axis (SSM-native); recurrent
              on a per-window basis at inference; trainable in
              parallel via SSM scan kernel
warm_start  : would consume Mamba pretrained weights at L4 IF
              training authorized (NOT in v0.1)
lineage     : Mamba (Gu+Dao 2023), Mamba-2, Spann3R, CUT3R,
              STream3R, LONG3R, LoGeR, LongStream
evidence    : paper-derived (SSM-for-3R-memory paper-proven;
              Mamba-style selective gating tied to A1 sub-actions
              architecture-novel)
              
sub-heads (still inside the SSM core):
  A1 update_kind classifier: 5-way softmax over
    {full_update, pose_adaptive_update, kalman_update,
     skip_update, reset_state}
  A1 update gate: input-dependent gain modulating SSM update
    magnitude (not the kind, the strength)
  
note: A1 is OWNED by Memory per SPEC-20260503-002. The SSM core
      is the substrate that implements A1. The classifier and
      the gate together IS A1 in concrete form.
```

### C3: Permanence slot memory + small head

```text
input       : T2 pointmap tokens + dynamic_mask tokens (from
              Perceiver auxiliary head OR from a comparator-style
              dynamic-aware backbone like MonST3R; inferred)
              + T3 evidence tokens (relevant subset:
              dynamic_ratio, optical_flow_conflict,
              object_track_stability, pose_novelty, view_overlap)
              + T5 object_track_set(t-1) (own state, read)
output      : updated T5 object_track_set(t); A6 sub-action
              decisions {suppress_static_write,
              admit_static_write, mint_object_id,
              update_object_track, defer}; pollution_log entry;
              dynamic_ratio published to bus; object_track_
              stability published to bus
substrate   : slot attention (object_track_set lives as slots) +
              small transformer head for per-region A6 decisions
parameters  : inferred 30M-80M (slot attention + small head)
              N_slots = N_objects_max (16-64)
parallelism : per-frame parallel for region decisions; sequential
              for object identity assignment via slot update
warm_start  : NONE (slot memory has no obvious 3R-pretrained
              starting point; would train from scratch IF training
              authorized; NOT in v0.1)
lineage     : Slot Attention (Locatello+ 2020), MonST3R / POMATO
              / D^2USt3R / Easi3R / RayMap3R per-frame dynamic
              split, OVGGT anchor protection (idea applied to
              objects)
evidence    : inferred (slot-memory-for-Permanence is
              architecture-novel; slot attention is paper-proven
              outside 3R; per-frame dynamic split paper-proven
              in 3R)

sub-heads (still inside the Permanence core):
  A6 region classifier: 3-way softmax per region over
    {suppress_static_write, admit_static_write, defer}
  A6 object identity head: similarity score over current
    object_track_set slots; argmax with theta_match threshold;
    mint new id if no slot above threshold
  A6 mint_rate budget gate: hard cap on mint per frame to avoid
    object explosion (failure-aware fallback per Permanence spec)
```

### C4: Critic small head

```text
input       : T2 pointmap tokens + T3 evidence tokens (active
              subset per Critic spec: pose_novelty, view_overlap,
              reprojection_residual, pointmap_conflict,
              confidence_drop, model_capability_match,
              prior_rgb_conflict (read-only)) + T6 bus tokens
              (capability_match read-only from Composer;
              latent_drift_proxy read-only from Memory)
output      : conflict_score(t) scalar; recommended_action label;
              route_regret_estimate (Composer-derived);
              critic_report_log entry
substrate   : small transformer (1-2 blocks) over evidence
              tokens; small classifier on top
parameters  : inferred 5M-30M (Critic is intentionally light)
              d_critic inferred 256-512; N_layers 1-2
parallelism : per-window parallel
warm_start  : optionally CTRL-style critic head at L4 IF training
              authorized (NOT in v0.1)
lineage     : Test3R verifier head, TTT3R trigger, CTRL critic
              (LM domain), MASt3R-SfM consistency
evidence    : inferred (small-Critic-head over V1 tokens
              architecture-novel; verifier-on-3R paper-proven)

sub-heads:
  A4 verifier head: scalar conflict_score regression over
    weighted evidence subset
  A5 repair-facet classifier: 5-way over
    {accept, rerun_local_region, reroute_model,
     open_anchor_budget, request_prior, conflict_unresolved}
  
note: A5 reroute_model output of Critic is GATED by CR-1
      (Composer must publish nonzero capability_match spread for
      reroute to fire). The gate is at the bus, not inside this
      head.
```

### C5: Composer table join (parameter-free)

```text
input       : sample_regime_card (computed per-input from
              metadata) + capability_card collection (static for
              cycle; one card per comparator model_id) + T6 bus
              tokens (route_history from Critic, read-only)
output      : capability_match per (model_id, input);
              route_recommendation ordered list;
              route_regret per chosen route; regime_card
              published to bus
substrate   : table join + weighted dot product; NO learned
              parameters in v0.1 (parameter-free)
parameters  : 0 (zero) at v0.1
parallelism : per-input single forward; trivially batchable
warm_start  : N/A (no parameters)
lineage     : MoE routing tables (LM / vision); Composer spec
              SPEC-20260504-001
evidence    : paper-derived (table-based routing well known);
              architecture-novel for 3R-specific regime cards
              and route_regret axis

note: Composer being parameter-free in v0.1 means Dream3R
      inference can run Composer ON CPU at near-zero cost. This
      is an architectural feature: Composer's load-bearing role
      (CR-1 gating Critic A5 reroute_model) does not gate on
      training. v0.2 may promote Composer to a learned router;
      that requires separate user authorization and DEC-20260504-
      002 no-all-in still applies.
```

### C6: Memory Bus (no parameters)

```text
input       : every module's published bus tokens
output      : a typed-dict tensor namespace passed to every
              module's read interface; CR-1..CR-6 gate tensors
              computed on the fly
substrate   : no learned parameters; pure routing + masking
parameters  : 0 (zero)
parallelism : a single bus-tick per window
warm_start  : N/A
lineage     : v2.1 cross-spec contract; blackboard architecture
              pattern
evidence    : architecture-novel

implementation note: at runtime the bus is a Python dict (or
PyTorch ModuleDict) that lives one level above the modules. Each
module returns its bus contributions; the orchestrator merges
them; the next forward sub-step reads from the merged dict. CR-
gates are pytorch.nn.Module instances reading from the dict and
writing back gate tensors before the next consumer fires.
```

## The Memory Bus as runtime API

bus_design_evidence_label: architecture-novel (3R-specific composition; pattern itself paper-derived from blackboard / pub-sub)

The bus is the architectural rendering of the v2.1 cross-spec signal contract. It has three surfaces:

### Bus surface 1: published signals (read-only contract)

Every signal in the v2.1 "Signal Owner Table" becomes a typed slot on the bus. Producer modules write once per window; consumer modules read multiple times.

```text
publish(signal_name, tensor, evidence_label, producer)
  -> assert producer == owner_of(signal_name)
  -> bus[signal_name] = (tensor, evidence_label, producer, t)

read(signal_name, consumer)
  -> assert consumer in consumers_of(signal_name)
  -> return bus[signal_name]
```

assertions enforce the v2.1 owner table. Violations are runtime errors at design time (intentional; we want to find contract drift early).

evidence_label propagates: when a consumer derives a new signal from a read, the new signal's label is the MIN of the read's label (paper-proven > paper-derived > inferred > unknown). This is CR-5 enforced as a label-propagation invariant.

### Bus surface 2: handoffs (binding signals)

Some signals are not informational; they are binding. The producer COMMANDS the consumer to do something or refuse and log.

```text
handoff(signal_name, command_tensor, producer, consumer)
  -> assert (producer, consumer, signal_name) in handoff_table
  -> bus_handoff[signal_name] = (command_tensor, producer, t)
  -> consumer must, on its next forward sub-step:
       (a) execute the command, OR
       (b) emit cross_spec_refusal(producer, signal_name, reason)

handoff_table at v0.1:
  {
    (Permanence, Memory, suppress_static_write):
      Memory's A2 write head must mask out the suppressed regions,
    (Permanence, Memory, admit_static_write):
      Memory's A2 write head SHOULD process the candidate (still
      subject to Memory-internal write_value_estimate; admit is
      permission, not command),
    (Composer, Critic, route_recommendation_handoff):
      Critic's A5 reroute_model, when it fires, must use Composer's
      ordered list rather than inventing one,
  }
```

CR-2 is enforced at handoff registration: Permanence's suppress_static_write IS binding on Memory. Memory may NOT silently override.

### Bus surface 3: gates (conflict resolution as runtime modules)

CR-1..CR-6 each compile to a small gate module that reads bus state and either masks a downstream output or surfaces a refusal. Gates are stateless (no parameters); they implement the contract rules.

```text
gate_CR1(bus):
  # CR-1: Critic A5 reroute requires Composer agreement
  cap_match    = read(capability_match)
  spread       = max(cap_match) - min(cap_match)
  reroute_mask = (spread > epsilon_spread)  # epsilon_spread = 0.05 inferred
  # apply mask to Critic A5 reroute_model logit BEFORE softmax
  return reroute_mask

gate_CR2(bus):
  # CR-2: Permanence suppress_static_write is binding on Memory
  suppress = read_handoff(Permanence, Memory, suppress_static_write)
  # this is a bool mask over per-region static-write candidates
  # gate is applied as a hard multiply at Memory's A2 write head
  return suppress

gate_CR3(bus):
  # CR-3: Memory drift signal does not gate Critic verification
  # this gate is more architectural: it asserts that Critic's A4
  # input vector does NOT include latent_drift_proxy as a primary
  # signal. The architectural enforcement is at Critic's evidence-
  # token weighting layer: weight on latent_drift_proxy is fixed
  # at zero in v0.1 for A4 score, nonzero only for context cue.
  drift = read(latent_drift_proxy)
  drift_role_mask = (drift_is_context_cue_only())
  return drift_role_mask

gate_CR4(bus):
  # CR-4: Composer route_recommendation does not bind Critic on
  # ties. If top-1 and top-2 capability_match are within
  # epsilon_tie (0.05 inferred; 0.05 inferred for v2 cost-adjusted
  # spread per DEC-20260504-004), Critic picks among them by
  # Critic-internal preference (cached models, untried in
  # route_history).
  cap_match     = read(capability_match)
  ties          = nearby_within(cap_match, epsilon_tie)
  route_history = read(route_history)
  pick          = critic_internal_tiebreak(ties, route_history)
  # gate publishes a "tied_set_to_pick_from" tensor, not a binding
  # command
  return pick

gate_CR5(bus):
  # CR-5: All cross-spec signals carry their producer's evidence
  # label; consumers must propagate, not silently upgrade.
  # gate is a label-min propagation over every read.
  for read_op in current_window_reads:
    consumer_label = MIN(read_op.label, current_consumer_label)
  return consumer_label_map

gate_CR6(bus):
  # CR-6: cycle 009 / cycle 010 case cards record contract usage.
  # In a runtime system, this is an audit log: every (read,
  # producer, label, consumer) tuple is appended to a contract_
  # usage_log. This is bookkeeping, not gating.
  contract_usage_log.append(current_window_reads)
  return None
```

CR-1 and CR-2 are HARD gates that mask outputs. CR-3, CR-4 are architectural / soft gates that constrain how a head reads its inputs. CR-5 is an invariant on label propagation. CR-6 is a bookkeeping ledger.

### Bus tick order per window

```text
per window t:
  step 1 (perception):      Perceiver forward over input frames; emit T1, T2, T3-perceive-portion
  step 2 (memory pre-read): Memory reads dynamic_ratio (Permanence, t-1 unless first window) and conflict_score (Critic, t-1 unless first window)
  step 3 (permanence):      Permanence forward; emit object_track_set(t), dynamic_ratio(t), suppress / admit handoffs, pollution_log entry
  step 4 (memory):          Memory forward; A1 update of latent_state; A2 write decisions GATED by CR-2 suppress_static_write; A3 anchor / cache decisions; emit policy_log, anchor_set, latent_drift_proxy
  step 5 (composer):        Composer forward (per-input, not per-window; runs once at input start with regime card + capability cards); emit capability_match, route_recommendation, route_regret, regime_card
  step 6 (critic):          Critic forward; A4 score; A5 repair-facet decision GATED by CR-1 (capability_match spread) and CR-3 (latent_drift_proxy is context-cue-only)
  step 7 (gates):           CR-1, CR-2 masks already applied at producing modules; CR-4 tiebreak on Critic A5 reroute_model output; CR-5 label propagation over all reads; CR-6 audit log append
  step 8 (output):           per-window aggregated output: pointmap + critic_report + memory_policy + pollution_decisions + route_recommendation_for_next_input
```

The bus tick is deterministic. The 8 steps run in this order; reads of (t-1) state from a downstream-of-this-window module are explicit (step 2 above for first window has no t-1 to read; null protocol per v2.1 forward-reference null applies).

## A1-A8 mapping to concrete layers

mapping_evidence_label: inferred (composition; per-action substrates paper-derived)

This section closes the loop between the action taxonomy in `planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md` and the architecture. Each action lands on a specific module + sub-head + bus signal.

| Action | Owner module | Concrete layer | Triggered by | Bus signals (writes) | Bus signals (reads) |
|---|---|---|---|---|---|
| A1 State Update Control | Memory (SSM core C2) | A1 update_kind classifier (5-way) + A1 update gate | every window | latent_state delta (internal), policy_log (A1 row), latent_drift_proxy | pose_novelty (T3), confidence_drop (T3), conflict_score (Critic, t-1), dynamic_ratio (Permanence, t) |
| A2 Spatial Memory Governance | Memory (SSM core C2; A2 write head) | A2 write decision head (4-way: write / merge / ignore / defer) | per candidate write per window | static_map writes (external), policy_log (A2 row) | write_value_estimate (T3 derived), suppress_static_write handoff (CR-2 enforced HARD mask), dynamic_ratio (T3) |
| A3 Context / Anchor Budgeting | Memory (slot memory part of C2 + cache controller) | A3 anchor head + cache eviction policy + global retrieval head | every window | anchor_set delta (own state), cache_window delta (own state), policy_log (A3 row) | anchor_importance (T3), loop_candidate_score (T3), cache_pressure (T3), conflict_score (Critic, read-only) |
| A4 Geometry Verification | Critic (small head C4) | A4 verifier head (scalar regression) | every window | conflict_score, recommended_action, critic_report_log | T3 evidence subset {pose_novelty, view_overlap, reprojection_residual, pointmap_conflict, confidence_drop, model_capability_match, prior_rgb_conflict} |
| A5 Repair / Reroute (split: repair facet) | Critic (small head C4) | A5 repair-facet classifier (5-way: accept / rerun_local / reroute_model / open_anchor / request_prior / conflict_unresolved) | conflict_score > theta_conflict AND repair_budget > 0 | route_history append (own state), critic_report_log entry | capability_match (Composer, read; CR-1 gated for reroute_model branch) |
| A5 Repair / Reroute (split: routing facet) | Composer (parameter-free C5) | route_recommendation table-join | every input | capability_match, route_recommendation, route_regret, regime_card, capability_card | route_history (Critic), sample_regime_card metadata (input) |
| A6 Dynamic / Object State Separation | Permanence (slot memory C3) | A6 region classifier (3-way: suppress / admit / defer) + A6 object identity head + A6 mint_rate budget gate | every frame | object_track_set delta (own state), dynamic_ratio, object_track_stability, suppress_static_write handoff, admit_static_write handoff, pollution_log | T3 evidence subset {dynamic_ratio (own derived), optical_flow_conflict, object_track_stability (own), pose_novelty (read), view_overlap (read)}, conflict_score (read-only); prior_rgb_conflict (read-only) |
| A7 Prior / Modality Arbitration | RESERVED HOOK | reserved bus surface for Cross-Modal head; not implemented in v0.1 | NOT triggered in v0.1 | (none) | (would read prior_rgb_conflict and blur_or_low_light_score) |
| A8 Evidence Acquisition / Adaptation Budget | RESERVED HOOK | reserved bus surface for Active Perception head; not implemented in v0.1 | NOT triggered in v0.1 | (none) | (would read uncertainty_area) |

A7 and A8 are RESERVED hooks. v0.1 declares the bus surface they would use (signal names + types) but does NOT design heads or substrates. Adding A7 / A8 in a future cycle requires a separate user direction (Cross-Modal spec authorization or Active Perception spec authorization). The hooks ensure the architecture does not need rewiring when those specs land.

## Read-write protocol per window (sequence diagram)

protocol_evidence_label: inferred (composition)

A single window of input flows through the architecture in this order:

```text
Window boundary at frame index [t_start, t_end]:

1. Perceiver
   reads:  raw frames in window
   writes: T1 frame tokens, T2 pointmap tokens, T3 perceive-side
           evidence subset (pose_novelty, view_overlap,
           reprojection_residual, pointmap_conflict,
           confidence_drop)
   bus:    publish T1, T2, T3-partial

2. Permanence (per-frame split decisions)
   reads:  T2 pointmap tokens, dynamic_mask tokens (auxiliary
           or from comparator-style head), T3 evidence subset
           (dynamic_ratio derived in this step,
           optical_flow_conflict from optical flow, prior reads
           are no-op in v0.1), object_track_set(t-1) (own state)
   writes: object_track_set(t), pollution_log, dynamic_ratio
           into T3, object_track_stability into T3,
           suppress_static_write handoff for this window's static
           write candidates, admit_static_write handoff
   bus:    publish dynamic_ratio, object_track_stability,
           suppress_static_write, admit_static_write

3. Memory (state update + write decisions + budget)
   reads:  T1 perception summary, T3 evidence subset
           (pose_novelty, confidence_drop), conflict_score(t-1),
           dynamic_ratio(t), suppress_static_write handoff
   writes: latent_state(t), anchor_set(t), cache_window(t),
           static_map writes via A2 write head GATED by CR-2,
           policy_log entries, latent_drift_proxy
   bus:    publish latent_drift_proxy, anchor_set, policy_log
   gate:   CR-2 hard-mask on A2 write head; if Memory cannot
           honor (e.g. internal structural reason), publish
           cross_spec_refusal{producer=Permanence, signal=
           suppress_static_write} per CR-2's refusal protocol
           and surface to Advisor

4. Composer (per-input, run once at input start; here repeated
   reference for completeness)
   reads:  sample_regime_card(input) (computed from metadata),
           capability_card collection (static for cycle),
           route_history (Critic, read-only; null on first
           window per forward-reference null protocol)
   writes: capability_match, route_recommendation, route_regret,
           regime_card
   bus:    publish capability_match, route_recommendation,
           route_regret, regime_card, capability_card

5. Critic (verify + repair-facet decision)
   reads:  T2 pointmap tokens, T3 evidence subset (pose_novelty,
           view_overlap, reprojection_residual, pointmap_
           conflict, confidence_drop, model_capability_match,
           prior_rgb_conflict (read-only)),
           latent_drift_proxy (Memory; read-only, CR-3 makes
           this context-cue-only for A4),
           capability_match (Composer; read-only)
   writes: conflict_score, recommended_action, route_history
           append (when A5 fires), route_regret_estimate,
           critic_report_log
   bus:    publish conflict_score, recommended_action,
           route_history (after own append), route_regret_
           estimate
   gates:  CR-1 (capability_match spread > epsilon_spread)
           masks the reroute_model branch BEFORE softmax;
           CR-3 already applied via input weighting;
           CR-4 tiebreak applied AFTER softmax if top-2 match
           within epsilon_tie

6. Gates (orchestrator-level)
   CR-5 propagates evidence labels over every read in this
        window
   CR-6 appends contract usage to audit log
   gate output: none binding (CR-5 / CR-6 are invariants /
                bookkeeping)

7. Output aggregation
   per-window output bundle:
     pointmap (Perceiver)
     critic_report (Critic)
     memory_policy_summary (Memory; from policy_log this window)
     permanence_summary (Permanence; pollution_log this window)
     route_summary (Composer; if input boundary in this window)
   These bundles are written to the per-job ledgers and surfaced
   to KYKT advisor at job-end (out of scope v0.1; advisor surface
   list is in each finalist spec).
```

protocol invariants:

```text
- Every read of state from a different module is read-only
  (CR-5 propagation enforced).
- Every cross-module command is via handoff signal (CR-2
  binding; CR-1 gating; refusal logged per CR-2 protocol).
- The first window of a job has no t-1; reads of t-1 state
  return null per v2.1 forward-reference null protocol; each
  consumer must declare a fallback (e.g. Memory's A1 update_
  kind defaults to skip_update for t=0 to avoid acting on null
  conflict_score).
- The order of steps 2..6 is fixed. Step 1 (Perceiver) is the
  only step with no upstream module dependency. Step 4
  (Composer) runs once per input rather than per window;
  positionally, it is computed at input start and read by
  Critic at every window thereafter. The ordering above shows
  Composer in the per-window bus tick for completeness.
```

## Conflict resolution as architectural elements (CR-1..CR-6)

cr_rendering_evidence_label: architecture-novel (CR-rules-as-architecture)

The v2.1 contract has six conflict resolution rules. Each becomes a structural element of the architecture, not an embedded conditional inside a module's forward pass.

### CR-1 as a hard mask

Inputs : capability_match (Composer, t-1 unless first window), epsilon_spread = 0.05 (inferred)

Mechanism : compute spread = max(capability_match) - min(capability_match) over the comparator pool. If spread <= epsilon_spread, force Critic A5 reroute_model output logit to -inf BEFORE softmax. The remaining Critic A5 outputs (accept / rerun_local / open_anchor / request_prior / conflict_unresolved) are unaffected; if the softmax now puts highest mass on conflict_unresolved, that is the correct behavior per CR-1.

Architectural placement : the CR-1 gate module sits between Composer's forward and Critic's A5 head. It produces a 1-bit reroute_allowed mask that multiplies Critic's A5 logits.

Falsifiable : if a future cycle's training run shows that Critic's reroute_model branch never fires anyway because spread is always large in benchmark inputs, CR-1's load-bearing role weakens. v0.1 keeps it as a guarantee against silent capability assumption drift.

### CR-2 as a hard mask + refusal protocol

Inputs : suppress_static_write handoff (Permanence, t)

Mechanism : at Memory's A2 write head, the per-region write logit is multiplied by (1 - suppress_mask). The mask is hard: a suppressed region cannot be written even if Memory's internal write_value_estimate would otherwise admit it.

If Memory cannot apply the mask (e.g. structural limitation, like the static_map store rejecting region-level masks), Memory emits cross_spec_refusal on the bus rather than silently overriding. The cross_spec_refusal is read by an audit / Advisor module at job-end.

Architectural placement : the CR-2 gate is at Memory's A2 write head, computed from the Permanence handoff at the bus.

### CR-3 as input-feature weighting

Inputs : latent_drift_proxy (Memory, t)

Mechanism : Critic's A4 verifier head reads the evidence vector. The weight on latent_drift_proxy in the A4 score computation is fixed at zero in v0.1. latent_drift_proxy is read by Critic ONLY as a context cue (input to a separate context head, not the A4 verifier head). This decouples Memory's drift estimation from Critic's verification scoring.

Architectural placement : structural, in Critic's evidence-token weighting matrix. Not a runtime gate.

Falsifiable : a future cycle could surface the question "would A4 score benefit from latent_drift_proxy as a primary feature?" That would be a v0.2 candidate and would require revising the v2.1 contract (CR-3 is part of it). v0.1 holds the rule because cycle 009's parallel-track design depends on Memory and Critic remaining independently falsifiable.

### CR-4 as a tiebreak module (Critic-internal preference)

Inputs : capability_match top-K (Composer), route_history (Critic, own state), epsilon_tie = 0.05 (inferred)

Mechanism : after Critic's A5 reroute_model logit is computed (and after CR-1 mask is applied), if more than one model is within epsilon_tie of the top capability_match, the tie-break selects the model not yet in route_history this window. If all tied models are already in route_history, escalate to conflict_unresolved.

Architectural placement : the CR-4 gate sits AFTER Critic A5 softmax. It produces a final picked-model tensor read by downstream consumers.

Note : per DEC-20260504-004, CR-4 also arbitrates ties on the v2 cost_adjusted_match (alpha = 0.5 inferred). v0.1 holds both arbitration paths (capability-only spread tie + cost-adjusted spread tie) per the v2.1 contract.

### CR-5 as a label-propagation invariant

Mechanism : every bus read returns (tensor, evidence_label). When a consumer module derives a new signal from one or more reads, the new signal's label is the MIN of input labels (paper-proven > paper-derived > inferred > unknown). The invariant is checked at publish time: if a module tries to publish a signal with a label STRICTLY HIGHER than min(its read labels), the bus raises a contract violation.

Architectural placement : invariant on the bus publish layer. Not a forward-pass gate.

Falsifiable : if at training time a module is found to "earn" a higher label via some statistical regularization (uncertainty calibration, ensemble agreement, etc.), the strict MIN propagation may relax to a learned label. v0.1 holds strict MIN because no such mechanism exists yet.

### CR-6 as an audit log

Mechanism : every bus read appends a (read_signal, producer, producer_label, consumer, t) tuple to contract_usage_log. The log is bus-readable and surfaces at job-end for cycle audit / case-card-derivation purposes.

Architectural placement : ledger; no forward-pass effect.

## Training-objective sketch (for ablation planning input only; NOT a training authorization)

training_sketch_evidence_label: speculative (no training authorized; this is INPUT to S3 ablation plan, not a plan itself)

If Dream3R were ever trained (NOT in v0.1 scope; requires separate user direction per DEC-20260506-001 not allowed list), the loss surface would decompose along the action taxonomy:

```text
L_total = w_pointmap   * L_pointmap            (Perceiver; standard 3R)
        + w_critic_p1  * L_critic_P1           (Critic A4; conflict detection)
        + w_critic_p5  * L_critic_P5           (Critic A5 repair; route regret)
        + w_memory_p2  * L_memory_P2           (Memory A3; anchor retention)
        + w_memory_p3  * L_memory_P3           (Memory A2; memory growth /
                                                usefulness)
        + w_perm_p4    * L_permanence_P4       (Permanence A6; dynamic
                                                pollution)
        + w_perm_id    * L_identity_consistency(Permanence A6 secondary)
        + w_composer_p5* L_composer_P5         (Composer A5 routing; route
                                                regret cost-adjusted)
        + w_action_p6  * L_action_entropy      (controller-validity guard;
                                                P6 from ACTION_TAXONOMY)
        + w_contract   * L_contract_usage      (CR-1..CR-6 invariant
                                                violations should be zero;
                                                this is a regularizer that
                                                penalizes any cross_spec_
                                                refusal)
```

Each loss above corresponds to a proxy metric defined in `planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md`. The architectural mapping makes the loss decomposition concrete (which module produces which output, which target the loss is computed against). The weights w_* are inferred and would be tuned at training time if training were ever authorized.

what this sketch IS: an input to the cycle 016 S3 ablation plan. The S3 plan will use it to specify which ablations falsify which architectural claims (e.g. "ablating the bus = removing CR-1..CR-6 gates and forcing each module to operate in isolation; expected impact: X").

what this sketch IS NOT: a training plan. No training is authorized. No GPU runs are authorized. Any move to training requires a separate DEC.

## Module-level evidence labels (summary)

Per Discipline rule 5 (Honesty Override), each major architectural element carries an evidence label. This is the section where they all aggregate.

| Element | Lineage | Evidence label |
|---|---|---|
| Perceiver substrate (transformer) | DUSt3R / MASt3R / VGGT / Test3R / MapAnything / CroCo | paper-proven |
| Perceiver token output (T1, T2) | DUSt3R pointmap convention; VGGT explicit pointmap tokens | paper-proven |
| Memory substrate (Mamba-style SSM) | Mamba; Spann3R / CUT3R / STream3R / LONG3R / LongStream / LoGeR | paper-derived |
| Memory A1 update_kind classifier | Mamba selective gating; A1 sub-actions per Memory spec | inferred (architecture-novel composition) |
| Memory A2 write head | Memory spec SPEC-20260503-002 | inferred |
| Memory A3 anchor + cache controller | OVGGT anchor protection idea; Memory spec | inferred (3R-specific composition) |
| Permanence substrate (slot memory) | Slot Attention (Locatello+ 2020) | paper-proven (outside 3R) |
| Permanence A6 region classifier | MonST3R / POMATO / Easi3R / D^2USt3R per-frame split | paper-proven |
| Permanence A6 object identity head | architecture-novel; Permanence spec SPEC-20260503-003 | inferred |
| Permanence object_track_set | architecture-novel for 3R; OVGGT anchor concept extended | inferred |
| Critic substrate (small transformer head) | Test3R verifier; TTT3R trigger; CTRL critic (LM domain) | paper-derived |
| Critic A4 verifier head | Test3R; A4 per Critic spec | inferred |
| Critic A5 repair-facet classifier | CTRL critic-revision pattern; A5 split per cycle 008.5 | inferred |
| Composer substrate (parameter-free) | MoE routing; capability cards | paper-derived |
| Composer regime card | inferred per Composer spec | inferred |
| Composer capability_match | paper-derived per Composer spec | paper-derived (per-claim) but inferred for the join weight |
| Cross-spec memory bus (signal table + typed slots) | v2.1 contract rendering | architecture-novel |
| CR-1 (reroute requires spread) | v2.1 contract; rendered as hard mask | architecture-novel |
| CR-2 (suppress_static_write binding) | v2.1 contract; rendered as hard mask + refusal protocol | architecture-novel |
| CR-3 (drift does not gate verify) | v2.1 contract; rendered as input-feature weighting | architecture-novel |
| CR-4 (tiebreak on capability ties) | v2.1 contract; rendered as Critic-internal preference module | architecture-novel |
| CR-5 (label propagation) | v2.1 contract + Discipline rule 5; rendered as bus invariant | architecture-novel |
| CR-6 (contract usage audit) | v2.1 contract; rendered as ledger | architecture-novel |
| A7 reserved hook | future Cross-Modal spec; signal slots reserved | speculative |
| A8 reserved hook | future Active Perception spec; signal slots reserved | speculative |
| Hybrid substrate hypothesis (transformer + SSM + slot) | v0.1 working assumption | inferred |

aggregate evidence-label distribution v0.1:

```text
paper-proven       : ~5 elements   (perception substrate; token outputs;
                                    per-frame dynamic split;
                                    slot attention outside 3R)
paper-derived      : ~5 elements   (SSM-for-3R-memory; Critic substrate
                                    pattern; Composer routing pattern;
                                    capability cards per-claim)
inferred           : ~10 elements  (per-action heads; per-module
                                    compositions; v0.1 substrate hypothesis)
architecture-novel : ~7 elements   (the bus, CR-1..CR-6 as gates,
                                    v0.1 substrate composition)
speculative        : 2 elements    (A7 / A8 reserved hooks)
```

architecture-novel elements are the load-bearing novelty story. paper-proven elements are the reuse story. inferred elements are the falsification surface (these are the parts an ablation plan should target).

## Comparator quick map (lightweight; full at S4)

comparator_quick_map_evidence_label: inferred (the full comparator map is the cycle 016 S4 deliverable; this section is a placeholder for v0.1)

This is the v0.1 placeholder. Full comparator map lands in cycle 016 S4 as a separate file (location TBD at S4 launch).

| Comparator | Substrate | Memory | Critic | Permanence | Composer | What Dream3R adds |
|---|---|---|---|---|---|---|
| DUSt3R | transformer | (none, per-pair) | (none) | (none) | (none) | bus + Memory + Critic + Permanence + Composer; everything beyond perception |
| MASt3R | transformer + matching | (none, per-pair) | (none, classical SfM) | (none) | (none) | bus + Memory + Permanence + Composer; Critic A4 supplants classical SfM verification |
| MASt3R-SfM | transformer + classical SfM | (matching graph) | (classical SfM consistency) | (none) | (none) | bus + Memory persistent latent state + Permanence object identity + Composer routing-facet |
| VGGT | transformer (large; explicit pointmap tokens) | (none) | (none, single-pass) | (none) | (none) | bus + Memory + Critic + Permanence + Composer; Dream3R is VGGT-as-perceiver + control graph |
| MapAnything | transformer | (latent state, learned) | (none) | (none) | (none) | bus + Critic + Permanence + Composer |
| Spann3R | transformer + spatial memory | (paper-proven persistent state) | (none) | (none) | (none) | bus + Critic + Permanence + Composer; Spann3R-as-Memory-core |
| CUT3R | transformer + persistent state | (paper-proven; full_update style) | (none) | (none) | (none) | bus + Critic + Permanence + Composer |
| STream3R | causal transformer | (sequential state) | (none) | (none) | (none) | bus + Critic + Permanence + Composer |
| Test3R | transformer + test-time consistency | (none) | (paper-proven A4) | (none) | (none) | bus + Memory + Permanence + Composer; Test3R-as-Critic-A4-source |
| MonST3R | transformer + dynamic mask head | (none) | (none) | (paper-proven per-frame split) | (none) | bus + Memory + Critic + Composer; MonST3R-as-Permanence-substrate-ancestor |
| Mamba-3R / SSM-3R variants | SSM throughout | SSM | (none, depending on variant) | (none) | (none) | bus + Critic + Permanence + Composer; v0.1 substrate hypothesis says SSM is the right Memory substrate, NOT the right perception substrate |
| 4DGS / Splatt3R / InstantSplat / NoPoSplat | transformer or Gaussian | (none) | (none) | (graphics-tooled, not memory-tooled) | (none) | Dream3R routes asset-path inputs to these models via Composer; the asset-path itself is OUT OF SCOPE per Permanence spec 4DGS exclusion |

what this map shows v0.1: Dream3R is NOT a competitor at any single substrate axis. It is a control graph THAT REUSES existing 3R substrates as its modules. The novelty is the graph + bus + gates, not any module's internal computation.

## Per-spec cross-reference (each finalist spec re-mapped to architecture)

cross_reference_evidence_label: inferred (composition; per-spec contents paper-derived from each finalist spec)

This section makes explicit how each of the 4 finalist specs lands inside Dream3R v0.1.

### Critic SPEC-20260503-001 -> Critic core C4

```text
Owned actions     : A4, A5 repair-facet (cycle 008.5 split)
Architecture role : small transformer head over T2 + T3 evidence
                    tokens; emits conflict_score, recommended_action,
                    route_regret_estimate, route_history append
Substrate         : transformer (1-2 blocks; ~5-30M params inferred)
Bus participation : reads T2, T3 evidence subset, capability_match
                    (Composer), latent_drift_proxy (Memory; CR-3
                    context-cue-only)
                    publishes conflict_score, recommended_action,
                    route_history, route_regret_estimate,
                    critic_report_log
Gates             : CR-1 (HARD mask on A5 reroute_model),
                    CR-3 (input weighting; latent_drift_proxy
                    is context-cue-only),
                    CR-4 (tiebreak on Critic A5 reroute_model
                    after softmax)
Demo surface      : two-panel critic timeline per Critic spec
                    "Teacher Demo Form" (markdown); demo
                    promotion is OUT OF SCOPE v0.1
Comparator anchors: Test3R (A4 head); TTT3R (trigger); MASt3R-SfM
                    (geometric verification baseline); CTRL (LM
                    critic pattern)
What v0.1 holds   : the closed A4 -> A5 loop on a small head; the
                    cross-3R-model A5 reroute_model action set
                    bound by Composer's capability_match
What v0.1 defers  : a learned weighted combination of evidence
                    signals for A4 score (held as inferred weights
                    in v0.1); the L3 prototype runner from cycle
                    015 is paused at S9 done; G_run can resume if
                    architecture spec needs measured A4 evidence
```

### Memory SPEC-20260503-002 -> Memory core C2 (SSM)

```text
Owned actions     : A1 (state update control), A2 (spatial
                    memory governance), A3 (context / anchor
                    budgeting)
Architecture role : SSM core over per-window summaries +
                    evidence subset; A1 update_kind classifier
                    on top; A2 write head on top; A3 anchor +
                    cache controller as side modules sharing
                    latent_state
Substrate         : selective SSM (Mamba-style; ~50-150M params
                    inferred)
Bus participation : reads T1 perception summary, T3 evidence
                    subset (pose_novelty, confidence_drop),
                    conflict_score (Critic, t-1), dynamic_ratio
                    (Permanence, t), suppress_static_write
                    handoff (Permanence, t)
                    publishes latent_drift_proxy, anchor_set,
                    cache_window (informational), policy_log
Gates             : CR-2 (HARD mask on A2 write head from
                    suppress_static_write handoff)
Demo surface      : five-row MonST3R 48-frame timeline per
                    Memory spec "Teacher Demo Form" (markdown);
                    demo promotion is OUT OF SCOPE v0.1
Comparator anchors: CUT3R, STream3R, LONG3R, LoGeR, Mem3R,
                    PAS3R, FILT3R, OVGGT, Point3R, LongStream
What v0.1 holds   : the controller-as-architecture framing
                    (policy bank over evidence vector, not a
                    new memory primitive); SSM substrate
                    matches the controller's per-window state
                    update granularity
What v0.1 defers  : the memory store itself (Memory does not
                    own the store; v0.1 treats static_map as a
                    pointer into an external store); the
                    cross-job memory consolidation contract
                    (out of v0.1 scope per CR-7-not-yet)
```

### Permanence SPEC-20260503-003 -> Permanence core C3 (slot memory)

```text
Owned actions     : A6 (dynamic / object state separation)
Architecture role : slot memory over object_track_set + small
                    head for per-region A6 decisions + small
                    head for A6 object identity assignment
Substrate         : slot attention (Locatello 2020 lineage) +
                    small transformer head (~30-80M params
                    inferred; N_slots = 16-64)
Bus participation : reads T2 pointmap tokens, dynamic_mask
                    tokens (auxiliary or comparator-style),
                    T3 evidence subset (dynamic_ratio derived
                    here, optical_flow_conflict, object_track_
                    stability (own), pose_novelty (read),
                    view_overlap (read)), conflict_score (read-
                    only)
                    publishes dynamic_ratio, object_track_
                    stability, suppress_static_write handoff,
                    admit_static_write handoff, pollution_log,
                    object_track_set
Gates             : produces CR-2's input handoff
                    (suppress_static_write), Memory enforces it
Demo surface      : three-layer 48-frame MonST3R timeline per
                    Permanence spec "Teacher Demo Form"
                    (markdown); demo promotion is OUT OF SCOPE
                    v0.1
Comparator anchors: MonST3R, POMATO, D^2USt3R, Easi3R, RayMap3R,
                    G-CUT3R; 4DGS variants explicitly excluded
What v0.1 holds   : object_track_set as architectural state
                    (slot memory); identity_consistency proxy
                    is computable from object_track_set
                    timeline
What v0.1 defers  : 4DGS asset path (excluded per Permanence
                    spec boundary); learned identity head (would
                    require training; not in v0.1)
```

### Composer SPEC-20260504-001 -> Composer core C5 (parameter-free table join)

```text
Owned actions     : A5 routing facet (cycle 008.5 split)
Architecture role : parameter-free table join: regime_card x
                    capability_card -> capability_match -> route_
                    recommendation; v0.1 has zero learned
                    parameters in this core
Substrate         : table join + weighted dot product (no SSM,
                    no transformer, no CNN)
Bus participation : reads sample_regime_card metadata,
                    capability_card collection (static for
                    cycle), route_history (Critic, read-only;
                    null on first input per forward-reference
                    null protocol)
                    publishes capability_match, route_
                    recommendation, route_regret, regime_card,
                    capability_card
Gates             : Composer is the producer for CR-1's input
                    (capability_match spread); the gate is at
                    Critic, not at Composer
Demo surface      : two-panel regime + capability_match table
                    per Composer spec "Teacher Demo Form"
                    (markdown); demo promotion is OUT OF SCOPE
                    v0.1
Comparator anchors: no direct 3R comparator; cross-domain MoE
                    routing literature
What v0.1 holds   : parameter-free routing keeps Dream3R
                    inference cheap; route_regret-as-falsifier
                    axis is the central novelty
What v0.1 defers  : learned router (would be v0.2 candidate;
                    DEC-20260504-002 no-all-in still applies);
                    cost_adjusted alpha tuning (v2 alpha = 0.5
                    inferred per DEC-20260504-004)
```

## Risks

risks_evidence_label: inferred

### R1: substrate hypothesis falsification at training time

```text
The hybrid substrate (transformer + SSM + slot) is v0.1's most
falsifiable architectural choice. If a future cycle's training run
(NOT authorized in v0.1) shows that pure SSM stack matches the
hybrid on benchmark with same parameter budget, the substrate story
collapses. Mitigation: v0.1 declares the substrate hypothesis as
INFERRED. The S3 ablation plan must include a substrate ablation
("transformer-only"; "SSM-only"; "hybrid") as a falsifying
experiment. If training is ever authorized, that ablation is a
priority.
```

### R2: bus-as-novelty collapse if CR-rules never fire

```text
If, on real benchmark inputs, capability_match spread is always
above epsilon_spread, CR-1 never fires. If suppress_static_write is
always issued for all dynamic regions and Memory always honors,
CR-2 never produces a refusal. The bus reduces to plain dataflow.
The architecture still works but the paper claim of "bus + gates as
architecture" weakens to "modular composition with conventions".
Mitigation: the cycle 016 S3 ablation plan must specify CR-rule
firing rate as a measured axis, and the cycle 016 S4 comparator map
must show that absence of CR-rules in existing models is the
distinguishing axis (i.e. existing models routinely violate what
CR-1..CR-6 enforce).
```

### R3: state-ownership invariant violation under training

```text
v0.1 specifies that state is owned by exactly one module and others
read read-only. If at training time, gradients flow from a consumer
back through a producer's state in ways that effectively let the
consumer "mutate" the producer's state via backward pass, the
ownership invariant is statistically violated even if syntactically
held. Mitigation: training-time stop_gradient on cross-spec reads
in the v0.1 sketch; the S3 ablation plan should include a
"gradient-isolated" vs "gradient-flowing" cross-spec read ablation
to measure the impact.
```

### R4: A7 / A8 reserved hooks may conflict with future spec design

```text
v0.1 reserves bus surfaces for A7 Cross-Modal and A8 Active
Perception. The reserved signal names (would-be entries in the
T3 evidence vector + would-be handoff signals) are inferred from
the action taxonomy. If a future Cross-Modal spec or Active
Perception spec finds that the actual signal shapes diverge from
the inferred reservation, the bus needs revision. Mitigation:
the reservation is an inferred placeholder, not a binding contract.
A v0.2 architecture spec or a separate Cross-Modal / Active
Perception spec can adjust the bus surface; the architecture spec
versioning rule (similar to the v2.1 contract versioning) governs
how reservations evolve.
```

### R5: storytelling vs measurement asymmetry

```text
v0.1 leans hard on the "control-graph-as-architecture" story
(audience profile preference for 创新范式 + 讲好故事). If a future
cycle ever produces measured numbers (training authorized) and the
numbers do not support the control-graph narrative (e.g. the bus
is inert; the gates do not fire; the substrate hypothesis is
falsified), the story-architecture asymmetry could collapse the
paper claim. Mitigation: every section in v0.1 carries an evidence
label. Any future training results must be reflected back into
this spec as label upgrades or downgrades per Discipline rule 5;
the story does not survive failed measurements.
```

### R6: scope creep into KYKT integration

```text
v0.1 declares KYKT runner / sample_matrix / system_readiness /
management_area / frontend implementation OUT OF SCOPE. Future
cycles may pressure the architecture to integrate (e.g. dispatch
Dream3R inference via ssh_runner.py to /hdd3/kykt26/code/dream3r/).
Mitigation: any KYKT integration is a separate gate per
AGENT_MASTER_PROMPT.md section 6 hard rules. v0.1 explicitly does
NOT design the integration; that is a future decision tied to
training authorization (which itself is gated).
```

### R7: paper writing risk

```text
"Control graph as architecture" is rhetorically attractive but
non-standard. The paper claim must (a) anchor against MoE routing
in LM domain (cross-domain analog), (b) anchor against blackboard
architectures in classical AI (architectural pattern lineage), and
(c) anchor against existing 3R papers' implicit cross-module
signals (DUSt3R confidence; Spann3R anchors; MonST3R masks). v0.1
sets up these anchors via the comparator quick map and lineage
fields per core. Without explicit anchoring, the paper claim risks
being read as "modular composition with conventions" rather than
architecture-novel.
```

## Boundaries (carried + new)

boundaries_evidence_label: user-decided (per DEC-20260506-001)

```text
1. NO TRAINING. v0.1 is markdown only. Any move to training
   requires a separate user direction.

2. NO GPU RUNS. The substrate hypothesis is inferred. No
   experimental run is authorized to test it.

3. NO CHECKPOINT CREATION. Even a randomly-initialized Dream3R
   checkpoint would imply training; not authorized.

4. NO REPRODUCTION. v0.1 cites paper claims but does not run any
   comparator model.

5. NO KYKT NAVIGATION CHANGE. None of the KYKT app surfaces are
   touched by v0.1.

6. NO FRONTEND IMPLEMENTATION. The teacher demo forms in each
   finalist spec remain markdown drafts.

7. NO DEMO STORYBOARD PROMOTION. STORY-20260505-001..004 remain
   `draft`. Critic / Memory / Permanence / Composer demos are
   not promoted to `approved-for-showing`.

8. NO 4DGS ASSET PATH. Per Permanence spec boundary, 4DGS asset
   rendering is explicitly excluded from v0.1.

9. NO CROSS-MODAL A7 / ACTIVE PERCEPTION A8 IMPLEMENTATION. v0.1
   reserves bus hooks but does NOT design heads or substrates
   for A7 / A8.

10. NO RETIRING OF ANY FINALIST. Per DEC-20260504-002 all 4
    finalists are preserved as composable modules in v0.1.

11. NO RETROACTIVE SUPERSEDE OF EXISTING ARTIFACTS. The 4
    finalist specs, v2.1 contract, A1-A8 taxonomy, mechanism
    intake, frontier source map, paper Phase 2 blueprint, all
    case cards, all storyboards, all cycle logs remain
    unchanged. v0.1 references them; it does not edit them.

12. NO THESIS FINALIZATION. Per DEC-20260501-004 v0.1 is a
    candidate. Even if a future cycle's measurements support
    v0.1, promotion to thesis requires a separate user
    direction.

13. NO CROSS-JOB STATE PROPAGATION. v0.1 holds Memory's per-
    job contract per the v2.1 contract scope. Cross-job memory
    consolidation is a future contract decision.
```

approval gates required to advance from v0.1:

```text
- moving from v0.1 spec to v0.2 spec: agent decision, allowed
  (v0.2 is an in-scope architectural revision per DEC-20260506-
  001; v0.2 must carry version history per Discipline rule 5)
- promoting any single finalist's role inside v0.1 to "thesis
  spine": user approval (DEC-20260504-002 forbids; a separate
  decision would be required)
- training v0.1 (full or any single module): user approval
- running v0.1 inference on any KYKT job: user approval (this
  would require Test3R / DUSt3R / etc. server-side dispatch;
  cycle 015 G_run paused at S9 done can be resumed under a
  separate gate for this purpose if the architecture spec
  needs measured evidence)
- adding A7 Cross-Modal head: user approval + Cross-Modal spec
- adding A8 Active Perception head: user approval + Active
  Perception spec
- KYKT integration of Dream3R inference: user approval +
  separate KYKT plan revision
- 4DGS asset path: user approval (separate decision; per
  Permanence spec boundary)
```

## Linked artifacts

linked_decisions:

- DEC-20260506-001 (mainline architecture-first; this spec is its S2 deliverable)
- DEC-20260501-004 (Dream3R candidate-not-final; still in force)
- DEC-20260504-002 (no-all-in any single finalist; still in force)
- DEC-20260504-001 (Composer finalist upgrade; informs A5 split)
- DEC-20260504-004 (cross-spec contract v2; informs CR-4 cost-adjusted tiebreak)
- DEC-20260505-001 (cycle 011 launch; informs v2.1 forward-reference null protocol)
- DEC-20260505-005 (cycle 015 launch / Critic L3 pilot; cycle 015 paused at S9 done; reusable as future evidence anchor)

linked_finalist_specs (INPUTS to this architecture spec; not superseded):

- specs/SPEC-20260503-001-geometry-critic.md (Critic; A4 + A5 repair facet; lands as core C4)
- specs/SPEC-20260503-002-executive-memory.md (Memory; A1 + A2 + A3; lands as core C2)
- specs/SPEC-20260503-003-dynamic-object-permanence.md (Permanence; A6; lands as core C3)
- specs/SPEC-20260504-001-3r-composer.md (Composer; A5 routing facet; lands as core C5)

linked_paradigm_artifacts:

- paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md (v2.1; rendered as runtime bus)
- paradigm/RESEARCH_CODE_DISCIPLINE.md (rules 3 Surgical Edits + 5 Honesty Override; both honored)
- paradigm/TEACHER_AUDIENCE_PROFILE.md (audience preference for 创新范式 + 讲好故事 informs paper-writing risk R7)

linked_planning_artifacts:

- planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md (A1-A8 + V1 evidence vector + P1-P8 proxies; lands as token T3 + per-action heads + training-objective sketch)
- planning/ARCHITECTURE_MECHANISM_INTAKE.md (broad mechanism pool; some elements reserved as A7 / A8 hooks)
- planning/RESEARCH_GRAPH_AND_PAPER_START.md (F1-F6 failure modes; Dream3R modules are mapped to F1 = Memory, F2 = Permanence, F3 = Critic, F6 = Composer)

linked_failure_modes (per the failure-mode graph):

- F1 Long-Context Drift / Forgetting -> Memory (primary), Permanence (secondary), Critic (informational)
- F2 Dynamic-Static Entanglement -> Permanence (primary), Memory (secondary)
- F3 Hard-Case Geometric Ambiguity -> Critic (primary), Memory (secondary), Permanence (secondary)
- F4 Active-View Knowledge Gaps -> A8 reserved hook (NOT designed in v0.1)
- F5 Sensor / Modality Limits -> A7 reserved hook (NOT designed in v0.1)
- F6 Fragmented Model Ecology -> Composer (primary), Critic (secondary via A5 reroute_model)

linked_kykt_artifacts (NOT to integrate; for evidence anchor when allowed):

- existing KYKT jobs: 20260420-222729 (MASt3R static pair), 20260420-222928 (MonST3R 48-frame), 20260425-113002 (Fast3R), 20260425-113227 (Spann3R)
- existing server runner inventory per F-002 / feedback_kykt_server_topology.md
- cycle 015 L3 infrastructure: test3r conda env on server; DUSt3R-weight-loadable Test3R via launch.py:103 patch; reusable as Critic evidence anchor at future G_run

linked_storyboards (NOT promoted; remain `draft`):

- storyboards/STORY-20260505-001-critic.md (Critic demo)
- storyboards/STORY-20260505-002-memory.md (Memory demo)
- storyboards/STORY-20260505-003-permanence.md (Permanence demo)
- storyboards/STORY-20260505-004-composer.md (Composer demo)

linked_paper_artifacts (now SUPPORT, not primary, per DEC-20260506-001):

- literature/PAPER_PHASE2_BLUEPRINT.md (control-graph theory becomes the THEORY behind the architecture; was the primary output before mainline redirect)
- literature/PAPER_RELATED_WORK_SKELETON.md (Sections 1-9 prose draft; informs the comparator quick map)

## Next step

planned_only: yes

next_action: cycle 016 S3 (ablation plan)

next_artifact (S3): a NEW file specifying which ablations falsify which architectural claims. Proposed location: planning/DREAM3R_ABLATION_PLAN.md OR specs/SPEC-20260506-002-dream3r-ablation-plan.md. User-pickable at S3 launch.

S3 ablation plan inputs (from this spec):

```text
- substrate hypothesis ablations (transformer-only / SSM-only /
  hybrid) per R1
- bus-as-novelty ablations (CR-rule firing rates; bus-removed
  baseline that flattens cross-spec signals into shared input)
  per R2
- state-ownership ablations (gradient-isolated vs gradient-flowing
  cross-spec reads) per R3
- per-action proxy losses (P1-P5 + identity_consistency + P6
  action_entropy) tied to the training-objective sketch
- per-module load-bearing flags: which modules can be removed
  without architectural collapse (e.g. removing Composer reduces
  to "default model only" routing; removing Permanence reduces to
  static-3R; removing Critic reduces to single-pass output;
  removing Memory reduces to per-window only)
```

next_action_after_S3: cycle 016 S4 (comparator map; full version of the lightweight quick map in this spec; new file).

next_action_after_S4: cycle 016 S5 (sync chain: TASK_SNAPSHOT first, then WORKFLOW_STATUS, RESEARCH_STATE, INDEX, decision_registry, AGENT_MASTER_PROMPT, README).

## Open questions for next session

These are NOT decisions; they are surfaced for the next session to either resolve or carry forward.

```text
Q1. Substrate ablation priority:
    R1 names "transformer-only / SSM-only / hybrid" as the
    falsifying experiment for the v0.1 substrate hypothesis. The
    S3 ablation plan must order these. Default: hybrid first
    (carries v0.1's bet); SSM-only second (highest substrate
    contrast); transformer-only third (lowest contrast). Open:
    user may want a different ordering.

Q2. Bus-as-novelty falsifying experiment design:
    R2 names CR-rule firing rate as a measured axis. But CR-rule
    firing depends on benchmark input distribution. The S3 plan
    must specify which benchmark inputs are likely to surface
    CR-1 / CR-2 / CR-4 firing. Open question for S3: do we
    construct adversarial inputs (designed to trigger CR-rules)
    or rely on existing KYKT job inputs (which may show low
    CR-rule firing because the cases are filtered)?

Q3. A7 / A8 reserved hook concretization:
    R4 acknowledges that the reservation is inferred. Should v0.2
    or a sibling Cross-Modal / Active Perception spec be drafted
    in cycle 017+? Or hold the reservation indefinitely?
    Default: hold; A7 / A8 concretization requires user direction.

Q4. v0.1 -> v0.2 trigger:
    What causes a v0.1 -> v0.2 transition? Candidates: (a) the
    S3 ablation plan surfaces an architectural choice that
    requires substrate revision, (b) a future Cross-Modal spec
    surfaces a bus-surface conflict with the A7 reservation,
    (c) a future training run (separately authorized) produces
    measured falsification of the substrate hypothesis. v0.1
    does not pre-decide the trigger; v0.2 will be a new file with
    explicit version history per Discipline rule 5.

Q5. KYKT integration path for evidence anchoring:
    Cycle 015 paused at S9 done. The test3r conda env on the
    server can run Test3R inference end-to-end. If the
    architecture spec ever wants to anchor the Critic A4 head
    against measured Test3R conflict scores on a real KYKT job,
    that requires resuming cycle 015 G_run. Should we surface
    that gate in cycle 017+ as part of S3 ablation plan, or hold
    it until v0.1 is reviewed?
    Default: hold; resuming G_run is a separate user gate per
    DEC-20260505-005.

Q6. Paper integration path:
    Per DEC-20260506-001 the paper Phase 2 blueprint is now
    SUPPORT, not primary. The architecture spec is primary. But
    the paper still needs to be a coherent artifact. When does
    the paper get re-written to feature Dream3R-the-architecture
    as the central claim, with the control-graph framework as
    its theoretical scaffolding? Default: not in cycle 016;
    cycle 016 produces only architecture spec + ablation plan +
    comparator map; paper rewrite is a separate cycle.
```

## Discipline notes (this section per Discipline rule 5)

```text
- Surgical Edits (rule 3): this spec is a NEW file. It does NOT
  edit any of the 4 finalist specs, the v2.1 contract, the
  A1-A8 taxonomy, or any case card / storyboard / cycle log.
  Every reference to those files is read-only citation.

- Honesty Override (rule 5): every architectural element above
  carries an evidence label. The aggregate distribution
  (~5 paper-proven; ~5 paper-derived; ~10 inferred; ~7
  architecture-novel; 2 speculative) is the honest accounting
  of v0.1 evidence status. Any future training-time results
  must be reflected back into this spec as label upgrades or
  downgrades; if a substrate hypothesis is falsified, the
  inferred label becomes a superseded label and the v0.2 spec
  carries the corrected label.

- Minimum Viable Mechanism (rule 2): each module owns a small
  action subset (Memory: 3; Critic: 2; Permanence: 1; Composer:
  1). The architecture preserves the per-spec ownership rather
  than centralizing actions in a master controller.

- F-001 anti-32MB rule 6: TASK_SNAPSHOT.md will be updated FIRST
  in the cycle 016 S5 sync chain (S5 is deferred to next session
  / next cycle 016 sub-pass). This file (the architecture spec)
  is large but is a NEW file, so Write is appropriate per F-001
  rule 3.

- F-002 server-topology: this spec does NOT propose any local
  Windows model installs. All future training / GPU runs (NOT
  authorized in v0.1) would target the server-side topology
  (/hdd3/kykt26 + ssh_runner.py). The local cycle 015 shallow
  clones remain code-reading anchors, not execution copies.

- Hard rules (carried from AGENT_MASTER_PROMPT.md): no
  reproduction / no checkpoint download / no training / no
  KYKT navigation change / no frontend implementation / no
  thesis finalization / no retiring of any non-finalist track /
  no demo storyboard promotion. All in force; v0.1 adds none
  and breaks none.
```

## Version history

```text
v0.1  2026-05-06  cycle 016 S2 deliverable. First architecture
                  spec for Dream3R. Hybrid substrate working
                  hypothesis (transformer perception + SSM/Mamba
                  executive memory + slot memory for Permanence
                  + parameter-free Composer + cross-spec memory
                  bus). 4 finalist specs synthesized as 4 cores
                  on the bus. v2.1 contract rendered as runtime
                  API. CR-1..CR-6 rendered as gates. A1-A8
                  mapped to concrete layers (A7 / A8 as reserved
                  hooks). Per-section evidence labels carried.
                  No training authorized; no GPU runs; no
                  checkpoint creation; markdown only.

v0.2  2026-05-06  cycle 018 S4 deliverable; v0.2 lives in a NEW
                  file specs/SPEC-20260506-004-dream3r-architecture-
                  v02.md (delta-only; this v0.1 file body is NOT
                  rewritten per DEC-20260506-002 + Surgical Edits +
                  Honesty Override). v0.2 introduces six numbered
                  deltas: (1) speed priority + frame budget table
                  (30-50 ms/frame at 30 FPS streaming-first;
                  inferred); (2) C1 Perceiver substitution ViT-L
                  -> DINOv3-Small (paper-derived; ~14x param
                  reduction; -B fallback documented); (3) C2 Memory
                  bounded anchor bank (K=256 proposed) + NSA-style
                  three-branch retrieval (compressed / selected /
                  sliding mapped to long / anchor-bank / short
                  hierarchy A+B; speculative for 3R transfer);
                  (4) NSA-style sparse attention as engineering
                  optimization (not paper main claim); (5) C5
                  Composer pool admits 7 lightweight experts
                  (MASt3R / Fast3R / Spann3R / CUT3R / MoGe-2 /
                  DepthAnything-V2 / Test3R) with capability
                  descriptors; drop VGGT, MapAnything, Kimi
                  Linear / KDA from streaming-first scope;
                  (6) main-claim narrowing to A (Verification-
                  as-architecture) + D (Heterogeneous best-of-N
                  Composer); B (state-ownership) + C (reservation
                  tokens A7/A8) demoted to discipline / future;
                  E (identity-anchored memory) supporting.
                  v0.1 sections referenced by name from SPEC-004;
                  v0.1 body unmodified.
```
