# Composer Capability Descriptors

artifact_id: planning/COMPOSER_CAPABILITY_DESCRIPTORS.md

date: 2026-05-06

cycle: 018 (S2 deliverable per DEC-20260506-002)

status: v0.1 (first enumeration; will be revised when capability_match values are measured rather than inferred)

linked_artifacts:
- decisions/DEC-20260506-002-cycle-018-launch-v02-architecture.md (parent)
- specs/SPEC-20260506-001-dream3r-architecture.md (v0.1; C5 Composer section)
- specs/SPEC-20260504-001-3r-composer.md (Composer mechanism finalist spec)
- paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md (v2.1 contract; capability_match axis)
- sources/FRONTIER_SOURCE_MAP.md (paper-known sources for the 7 admitted models)
- specs/SPEC-20260506-004-dream3r-architecture-v02.md (consumer; cycle 018 S4)

## Why this file exists

v0.1 architecture (SPEC-20260506-001) names C5 Composer as a parameter-free table-join over 5 backbones, but enumerates the capability vector at coarse model-granularity ("DUSt3R pair" / "MASt3R pair" / "MonST3R dynamic" / "Spann3R streaming" / "Fast3R many-view"). v0.2 dialog (2026-05-06) reframed Composer's job as exploiting **non-uniform infrastructure across heterogeneous 3R foundation models** — i.e., not "pick one model" but "pick which sub-mechanism of which model fits the current regime." This file enumerates the 7 admitted lightweight models with finer-granularity capability descriptors so that the v0.2 spec (SPEC-004) can reference them as a stable input.

## Pool admission criteria (v0.2)

A model is admitted into the v0.2 Composer pool only if:

```text
1. Streaming-compatible: per-frame inference fits the 30-50 ms budget
   on a single 24 GB GPU at 384x512 input resolution
   (paper-known or inferred from model size / architecture).

2. Has a publicly identifiable innovation point distinguishable from
   the others in the pool — i.e., admits a unique row in the capability
   table, not a duplicate.

3. Output schema can be mapped to the Bus token space (T2 pointmap /
   T3 evidence / T4 regime / T5 anchor + slot / T6 bus) via a
   non-trivial-but-feasible adapter sketched below.

4. License permits research use and the runtime stack does not
   require a different CUDA / PyTorch major version than the dream3r
   server env (torch 2.5.1 + cu121).
```

Models excluded by these criteria, with rationale:

```text
- VGGT (CVPR 2025; ~1.2B params): fails (1) streaming-compatible
  budget. Kept as future "slow-path expert" only if a separate DEC
  authorizes a heavyweight tier.

- MapAnything (Meta 2025): fails (1) on weight class; multi-modal
  foundation model. Same disposition as VGGT.

- DUSt3R (the original): admitted in spirit but downgraded; MASt3R
  superset of DUSt3R for the pair regime, so DUSt3R is shadowed in
  the pool unless an ablation requires it.

- MonST3R (dynamic): admissible in principle but its dynamic-aware
  fine-tuning bakes assumptions that overlap with C3 Permanence
  module's role. Holding for v0.3 readmission decision; not in the
  v0.2 pool.

- LONG3R / Point3R / PAS3R / LoGeR / Mem3R / RayMap3R: paper-known
  via cycle-013 source mining but not yet primary-verified for
  inference-time profile / license / checkpoint availability.
  Out of v0.2 pool; remain in `sources/FRONTIER_SOURCE_MAP.md` as
  candidates.
```

## Capability descriptor schema (per row)

Each model gets one row with axes:

```text
model_id              : short stable identifier
innovation_point      : the unique mechanism the model contributes
input_regime          : pair / multi-view / streaming / mono / triplet
output_schema         : pointmap / depth / pose / matching / mask
infrastructure_cost   : params (M) / latency (ms / 30FPS frame share) /
                        memory (MB / VRAM at 384x512) / dependencies
attention_regime      : full / linear / sparse (for §4 sparse-attention
                        Composer routing axis)
adapter_sketch        : how to map the model's native output to Bus
                        token space (T2 / T3 / T4 / T5 / T6)
capability_match_axes : per-regime suitability scores (inferred v0.1;
                        will be measured in a future ablation pass)
expected_failure_modes: what 3R failure modes this model handles vs.
                        does not handle (per F1..F6 in
                        ARCHITECTURE_MECHANISM_INTAKE.md)
evidence_label        : paper-known / paper-derived / inferred /
                        speculative for each axis
```

All numeric values labeled `inferred` are based on paper claims, model
sizes, or analogous-model wall-clock; they are NOT measured under the
dream3r server env. Promotion of any value from `inferred` to
`measured` requires a separate DEC + a benchmark pass.

## Pool members (7 admitted)

### EXPERT-01: MASt3R (pair / fast matching)

```text
model_id              : MASt3R
innovation_point      : Dense local feature matching grounded in 3D;
                        fast reciprocal matching head on top of
                        DUSt3R pair-pointmap regression. The "matching
                        head" is the unique mechanism — extractable
                        independently of the full pipeline.
input_regime          : pair (two RGB images, no intrinsics)
output_schema         : pointmap (per pixel) + dense local features
                        + reciprocal matches
infrastructure_cost   : params ~300M (ViT-Large encoder + decoder)
                        latency: paper-derived ~200-400 ms/pair on A100
                        for full pipeline; matching head alone
                        sub-100 ms inferred.
                        memory: ~5-8 GB VRAM at 512x384 (inferred)
                        dependencies: torch 2.x + xformers; license
                        non-commercial (verify before any release path)
attention_regime      : full attention (cross-image + self)
adapter_sketch        : MASt3R pair pointmap -> T2 (pointmap token,
                        per-patch). MASt3R dense features -> T3
                        (evidence token, sparse subset via top-k
                        confidence). MASt3R reciprocal matches ->
                        T5 (anchor candidates for Permanence). Bus
                        signal: cross_pair_match_quality ->
                        publish to T6 for Critic A4 reprojection
                        verification.
capability_match_axes : pair_quality 0.95 inferred; multi_view_scale
                        0.4 inferred (no native multi-view path);
                        streaming 0.2 inferred; mono 0.0 inferred;
                        dynamic 0.3 inferred; texture_low 0.7
                        inferred (matching head is feature-rich).
expected_failure_modes: handles F3 (matching conflict in textured
                        scenes); fails F6 (compute budget for
                        many-view); fails F2 (dynamic objects).
evidence_label        : paper-known for innovation_point, output_schema,
                        params; paper-derived for latency on A100;
                        inferred for matching-head-alone timing,
                        capability_match values.
```

### EXPERT-02: Fast3R (many-view / parallel)

```text
model_id              : Fast3R
innovation_point      : Single forward pass over many images without
                        pairwise / global alignment bottleneck. The
                        "many-view in one shot" is the unique
                        mechanism — replaces O(N^2) pair fusion with
                        O(N) parallel processing.
input_regime          : multi-view (N images, N up to ~50 paper-claim)
output_schema         : pointmap (per image, all in shared coord)
                        + camera pose
infrastructure_cost   : params: paper-derived ~580M (large)
                        latency: paper-claim seconds for ~50 views
                        on A100 single forward; per-frame shared
                        cost across N inputs. Per-frame share at
                        N=8 would be ~50-80 ms inferred.
                        memory: heavy at N>=20 (inferred 12+ GB)
                        dependencies: torch 2.x; checkpoint via
                        their CVPR release (paper-known).
attention_regime      : full attention across all N images
adapter_sketch        : Fast3R pointmap -> T2 (per-image pointmap).
                        Fast3R inferred poses -> Bus signal (camera
                        pose published to T6). For Composer routing:
                        invoked when N >= 4 and latency budget
                        permits; falls back to MASt3R pair for N=2.
capability_match_axes : pair_quality 0.7 inferred; multi_view_scale
                        0.95 inferred (the unique strength);
                        streaming 0.5 inferred (chunkable but not
                        natively online); mono 0.0; dynamic 0.2.
expected_failure_modes: handles F6 (compute budget for many-view by
                        avoiding pair fusion); fails F1 (no native
                        long-context state across forward passes);
                        fails F2 (static-only).
evidence_label        : paper-known for innovation_point, params,
                        multi-view performance claim; inferred for
                        per-frame share and capability_match.
```

### EXPERT-03: Spann3R (streaming / spatial memory)

```text
model_id              : Spann3R
innovation_point      : Spatial memory token + anchor-based global
                        pointmap streaming, eliminating optimization-
                        heavy global alignment per frame. Anchor
                        token is the unique mechanism — extractable
                        as a lightweight "memory contribution" in
                        Dream3R's C2 Memory module.
input_regime          : streaming (frame-by-frame, online)
output_schema         : pointmap (incremental, in shared coord)
                        + spatial anchor tokens
infrastructure_cost   : params ~250M (paper-derived; ViT-L encoder
                        + lightweight decoder + memory head)
                        latency: paper-claim ~30-50 ms / frame on
                        A100 (paper-known target); fits dream3r
                        streaming budget.
                        memory: 4-6 GB VRAM at standard res
                        dependencies: torch 2.x; checkpoint
                        spann3r.pth already on dream3r server.
attention_regime      : full attention within frame; sparse anchor
                        retrieval cross-frame
adapter_sketch        : Spann3R anchor tokens -> T5 (anchor +
                        object slot). Spann3R incremental pointmap
                        -> T2. Spann3R memory state -> Bus signal
                        published to C2 Memory module's NSA anchor
                        bank as initial seeding.
capability_match_axes : pair_quality 0.7 inferred; multi_view_scale
                        0.6 inferred; streaming 0.95 inferred (the
                        unique strength); mono 0.3 inferred (single-
                        image bootstrap weak); dynamic 0.3 inferred;
                        long_context 0.85 inferred (memory anchor).
expected_failure_modes: handles F1 (long-context drift via anchor
                        retention); handles F6 (compute via
                        avoiding pair fusion); fails F2 (dynamic);
                        partial F3 (matching is implicit, not
                        explicit).
evidence_label        : paper-known for innovation_point, latency
                        target; checkpoint code-observed (already
                        on server); inferred for capability_match.
```

### EXPERT-04: CUT3R (online state / continuous update)

```text
model_id              : CUT3R
innovation_point      : Continuous Updating Transformer with persistent
                        state across the stream — the state is the
                        unique mechanism, separate from anchor-based
                        memory. CUT3R's state is "always-on, always-
                        updated"; complements Spann3R's "anchor on
                        keyframe" model.
input_regime          : streaming (frame-by-frame, online)
output_schema         : pointmap (incremental) + persistent state vector
infrastructure_cost   : params ~300M paper-derived
                        latency: paper-claim ~40-60 ms / frame on
                        A100 (similar weight class to Spann3R)
                        memory: 4-6 GB VRAM
                        dependencies: torch 2.x; checkpoint TBD
                        on dream3r server (not currently inventoried)
attention_regime      : full self-attention + cross-frame state
                        recurrence
adapter_sketch        : CUT3R state vector -> Bus signal published
                        to C2 Memory as medium-term state input
                        (the SSM/Mamba-equivalent slot in v0.2
                        hierarchical memory). CUT3R pointmap -> T2.
capability_match_axes : pair_quality 0.7; multi_view_scale 0.55;
                        streaming 0.9; mono 0.4; dynamic 0.4
                        (CUT3R has some dynamic-aware framing);
                        long_context 0.8.
expected_failure_modes: handles F1 (long-context via state) — same
                        regime as Spann3R but different mechanism
                        (state vs anchor). Expert-03 + Expert-04
                        co-routing tests Composer's heterogeneous
                        best-of-N premise.
evidence_label        : paper-known for innovation_point; latency
                        paper-derived; capability_match inferred.
```

### EXPERT-05: MoGe-2 (mono / single-image fallback)

```text
model_id              : MoGe-2
innovation_point      : High-quality monocular geometry from a single
                        image — pointmap regression with affine-
                        invariant supervision. The "mono fallback"
                        is the unique mechanism: when streaming state
                        breaks (tracking lost, scene cut, single-image
                        query), MoGe-2 provides a recovery point.
input_regime          : mono (single RGB image)
output_schema         : pointmap (single-view) + scale-invariant depth
infrastructure_cost   : params ~200M paper-derived (ViT-L based)
                        latency: paper-claim ~50-100 ms / image on
                        A100; per-frame budget feasible.
                        memory: 4-5 GB VRAM
                        dependencies: torch 2.x; license MIT or
                        Apache (verify); checkpoint via Microsoft
                        release (paper-known).
attention_regime      : full attention (single-image, no cross)
adapter_sketch        : MoGe-2 single-view pointmap -> T2 (pointmap
                        token, scale-normalized to current Bus frame
                        of reference via Bus alignment signal).
                        Bus signal published: mono_recovery_pointmap
                        -> read by Critic A4 verification (does new
                        mono estimate agree with prior streaming
                        estimate within tolerance? if not, escalate).
capability_match_axes : pair_quality 0.3 inferred (single-image is
                        not pair-natural); multi_view_scale 0.2;
                        streaming 0.4 (per-frame independent, no
                        cross-frame coherence); mono 0.95 inferred
                        (the unique strength); dynamic 0.5; texture
                        _low 0.6.
expected_failure_modes: handles F4 (no input ambiguity recovery
                        when only one view); handles F5 (single-
                        image new-scene init); fails F1 (no state);
                        fails F3 (no cross-image matching).
evidence_label        : paper-known for innovation_point, params;
                        paper-derived for latency; inferred for
                        capability_match.
```

### EXPERT-06: DepthAnything V2 (mono depth prior)

```text
model_id              : DepthAnything-V2
innovation_point      : Foundation monocular depth estimation trained
                        at scale on synthetic + real data. Depth is
                        a cheap geometry prior that complements MoGe-2
                        (depth only vs full pointmap; cheaper).
input_regime          : mono (single RGB image)
output_schema         : relative depth map (single channel)
infrastructure_cost   : params ~25M (Small) / ~100M (Base) / ~340M
                        (Large) — pick Small for streaming budget.
                        latency: paper-claim < 30 ms / image on A100
                        for Small; very cheap.
                        memory: 1-2 GB VRAM Small
                        dependencies: torch 2.x; license Apache 2.0;
                        checkpoint readily available.
attention_regime      : full attention (DPT decoder over ViT-S/B/L)
adapter_sketch        : DepthAnything-V2 depth -> Bus signal
                        published as T3 evidence token (depth as
                        cheap prior). Critic A4 reprojection
                        verification can use this as a baseline
                        cross-check against MASt3R / Spann3R / CUT3R
                        pointmap outputs ("does our pointmap project
                        to a depth profile consistent with the
                        foundation depth model?").
capability_match_axes : pair_quality 0.2; multi_view_scale 0.2;
                        streaming 0.6 (per-frame, cheap); mono 0.85
                        (depth not pointmap, lower than MoGe-2);
                        dynamic 0.5; texture_low 0.7.
expected_failure_modes: handles F5 (universal cheap depth prior);
                        handles texture-low partial; cannot do F3
                        matching alone.
evidence_label        : paper-known for innovation_point, params,
                        latency; paper-derived for streaming
                        compatibility; inferred for capability_match.
```

### EXPERT-07: Test3R (lazy verification)

```text
model_id              : Test3R
innovation_point      : Test-time geometric consistency objective
                        over image triplets — a verification-only
                        mechanism, not a primary reconstruction
                        backbone. Fits the "Critic-triggered lazy
                        invocation" slot: only run when C4 Critic
                        flags low confidence on a region.
input_regime          : triplet (3 images selected by Critic for
                        re-verification)
output_schema         : consistency score (per triplet) + revision
                        suggestion
infrastructure_cost   : params: builds on top of DUSt3R / MASt3R
                        backbone; test-time refinement loop adds
                        iteration cost.
                        latency: paper-derived several seconds per
                        triplet (test-time iterative); only invoked
                        on flagged regions (sparse).
                        memory: 6-8 GB VRAM (carries backbone)
                        dependencies: torch 2.x; checkpoint via
                        Test3R repo (already cloned in cycle 015
                        S6; available for v0.2 reference).
attention_regime      : full attention (test-time iterative
                        refinement)
adapter_sketch        : Test3R triplet selection -> Bus read from
                        C4 Critic's flagged-region signal.
                        Test3R consistency score -> Bus signal
                        published as T3 evidence (revision verdict).
                        Used as the "expensive verification path"
                        — Composer routes to Test3R only when
                        Critic confidence < threshold AND latency
                        budget permits (off the streaming path).
capability_match_axes : pair_quality 0.85 (with backbone); multi_
                        view_scale 0.5; streaming 0.1 (NOT a
                        streaming model — verification-only);
                        mono 0.2; dynamic 0.4; verification 0.95.
expected_failure_modes: handles F3 (matching conflict via test-
                        time iteration); handles F1 (drift detection
                        via consistency check); the verification
                        slot is its primary value.
evidence_label        : paper-known for innovation_point; cycle 015
                        S6 cloned-and-readable for full code-observed
                        verification; inferred for capability_match.
```

## Routing policy sketch (v0.2 default)

```text
Per-frame routing decision (Composer C5 forward):

  if first frame of a new scene OR tracking lost:
      route -> EXPERT-05 MoGe-2 (mono recovery)
      AND   -> EXPERT-06 DepthAnything-V2 (cheap depth prior in parallel)
      goal  : establish initial pointmap + depth signal for Bus init

  elif N >= 4 input views AND latency budget allows:
      route -> EXPERT-02 Fast3R (many-view single forward)
      goal  : avoid O(N^2) pair fusion

  elif streaming (one new frame, prior state available):
      route -> EXPERT-03 Spann3R AND/OR EXPERT-04 CUT3R
              (Composer best-of-N over heterogeneous streaming experts;
               this is the §3 main-claim D primary demonstration)
      goal  : per-frame incremental update + anchor / state push to C2 Memory

  elif new pair available (e.g., loop closure candidate):
      route -> EXPERT-01 MASt3R (pair + matching)
      goal  : high-quality pair matching for loop verification

  if Critic C4 flags region OR C2 Memory retrieval conflict detected:
      lazy invoke -> EXPERT-07 Test3R (off-path verification)
      goal  : §3 main-claim A primary demonstration (Verification-as-
              architecture: Critic gate triggers expensive path)
```

This sketch is **inferred** v0.2 routing policy; the real values for
gate thresholds, capability_match weights, and route_regret would be
measured under a separate ablation pass (out of cycle 018 scope).

## Cross-axis summary table

| Expert | Innovation | Params | Latency target | Streaming | Mono | Pair | Multi-view | Verify |
|---|---|---|---|---|---|---|---|---|
| MASt3R | matching head | ~300M | 200-400 ms/pair | low | no | yes | partial | partial |
| Fast3R | many-view single fwd | ~580M | seconds for 50 views | medium | no | partial | yes | no |
| Spann3R | spatial memory anchor | ~250M | 30-50 ms/frame | yes | weak | partial | partial | no |
| CUT3R | online state | ~300M | 40-60 ms/frame | yes | weak | partial | partial | no |
| MoGe-2 | mono pointmap | ~200M | 50-100 ms/image | partial | yes | no | no | no |
| DepthAnything-V2 | mono depth foundation | ~25M (S) | < 30 ms/image | yes | yes | no | no | partial |
| Test3R | test-time consistency | (backbone+) | seconds/triplet | no | no | partial | partial | yes |

All numbers `inferred` or `paper-derived`; not measured under dream3r
server env.

## Open items for future passes

```text
1. Capability_match values are inferred. A measured pass requires
   running each expert on a held-out micro-benchmark (e.g., 5 scenes
   x 4 regimes) and recording route_regret per regime. This is gated
   on a separate DEC; not in cycle 018 scope.

2. CUT3R checkpoint not yet inventoried on dream3r server. Adding
   it requires a download gate similar to cycle 015's G_download.
   Not authorized in this DEC.

3. MoGe-2 and DepthAnything-V2 are mono experts; their integration
   benefits from Bus-level scale alignment. The scale-alignment
   protocol is not specified in v0.1 architecture; v0.2 spec needs
   to either reference an existing alignment (e.g., MoGe-2 affine-
   invariant claim) or open a TBD.

4. EXPERT-07 Test3R triggers a question about the C4 Critic's
   threshold pinning. v0.1 spec carried this as deferred (cycle
   011 D5'' deferred); v0.2 inherits the deferral. Threshold
   pinning still needs measured anchors before promotion.

5. Pool may grow in v0.3 if MonST3R / Mem3R / LoGeR / Point3R /
   PAS3R / RayMap3R prove primary-verifiable. Currently those are
   in the source map but not in the active pool.
```
