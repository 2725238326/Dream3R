# DINOv3-S × C1 Perceiver Integration Memo

artifact_id: planning/DINOV3_C1_INTEGRATION_MEMO.md

date: 2026-05-06

cycle: 018 (S3 deliverable per DEC-20260506-002)

status: design memo (paper-derived sketch; no implementation)

length_target: ~1 page (this file is ~120 lines)

linked_artifacts:
- decisions/DEC-20260506-002-cycle-018-launch-v02-architecture.md (parent)
- specs/SPEC-20260506-001-dream3r-architecture.md (v0.1 C1 Perceiver section)
- planning/COMPOSER_CAPABILITY_DESCRIPTORS.md (sibling cycle 018 deliverable)
- planning/NSA_MEMORY_INTEGRATION_MEMO.md (sibling)
- specs/SPEC-20260506-004-dream3r-architecture-v02.md (consumer)

## Source paper

DINOv3 (Meta, 2025).

Evidence label: `paper-known` for the model family and feature
quality claims; `paper-derived` for substitution into 3R pipelines
(several published 2025 3R works already use DINOv3 features);
`inferred` for specific Dream3R latency / VRAM numbers under the
dream3r server env.

## Why DINOv3-S replaces v0.1's ViT-L

v0.1's C1 Perceiver inherits the DUSt3R lineage convention of
ViT-Large (~300M params). Under v0.2's user-locked priority
(a) inference real-time with 30-50 ms / frame budget at 30 FPS, ViT-L
is too heavy:

```text
ViT-L forward:        paper-derived ~50-80 ms/frame at 384x512 on A100;
                      likely 100+ ms on TITAN RTX 24GB (dream3r server)
DINOv3-S forward:     paper-derived ~10-15 ms/frame at 384x512 on A100;
                      likely 20-30 ms on TITAN RTX (still feasible)
DINOv3-B forward:     paper-derived ~25-35 ms/frame at 384x512 on A100;
                      ~45-60 ms on TITAN RTX (borderline; back-up
                      option)

Component budget (target 30-50 ms / frame):
  C1 Perceiver        : 10-15 ms (DINOv3-S) — reserves 20-40 ms for
                        downstream modules.
  C2 Memory NSA       : few ms (sparse retrieval)
  C3 Permanence       : few ms (bounded slots)
  C4 Critic           : few ms (small transformer)
  C5/C6 routing+bus   : <1 ms

ViT-L would consume the entire frame budget alone.
```

## What DINOv3 contributes beyond DINOv2

```text
1. Stronger features at smaller scale: DINOv3-S claims to match
   or exceed DINOv2-B on dense feature benchmarks (paper-known).
   For 3R, dense features are what matters (per-patch correspondence
   quality), so the DINOv3 family pushes the Pareto frontier.

2. Better handling of high-resolution and dense prediction tasks:
   DINOv3 paper emphasizes dense prediction quality (segmentation,
   depth estimation), which directly serves Dream3R's pointmap
   regression head.

3. Reduced reliance on fine-tuning: DINOv3 features are claimed
   strong enough for some downstream tasks with frozen backbone.
   For Dream3R v0.2, this opens the option of frozen-backbone
   experiments (cheaper training, faster ablation iteration).

4. Continuity with DUSt3R lineage: DUSt3R / MASt3R / Spann3R use
   DINOv2 ViT-L features. Migrating to DINOv3-S preserves
   architectural lineage while reducing weight class.
```

Evidence label: claims (1)-(3) are `paper-known`; claim (4) is
`paper-derived` (DUSt3R lineage is well-documented; DINOv3 family
backwards-compatible with DINOv2-style usage patterns).

## Concrete v0.2 design sketch

```text
C1 Perceiver module structure (v0.2):

  Backbone:
    - DINOv3-Small (default) or DINOv3-Base (fallback if DINOv3-S
      features prove insufficient for pointmap quality at downstream
      heads)
    - frozen weights for v0.2 baseline; unfreezing is a separate
      decision (potentially unfreezing top N layers if downstream
      pointmap quality requires it; tracked as future ablation)

  Input:
    - per-frame RGB image at 384x512 (paper-derived budget; tunable)
    - patch size 14 (DINOv3 default)
    - patch tokens count: ~864 per frame at 384x512

  Output (per frame):
    - per-patch feature embeddings (D=384 for Small, D=768 for Base)
    - published to T1 frame_token Bus signal

  Heads on top of DINOv3 features (NEW; trainable):
    - pointmap_head: multi-layer MLP -> per-patch pointmap (3D + conf)
    - confidence_head: multi-layer MLP -> per-patch confidence
    - evidence_head: multi-layer MLP -> 17-dim evidence token
                    (cycle 016 architecture spec convention; published
                     to T3 Bus for C4 Critic consumption)

  Bus publication:
    - T1 frame_token: dense feature embeddings (read by C2 Memory
                     NSA selection gate; read by C3 Permanence slot
                     attention as input keys)
    - T2 pointmap_token: per-patch pointmap (read by Bus for
                        downstream alignment + Critic verification)
    - T3 evidence_token: per-patch evidence (read by C4 Critic)
```

## Migration path from v0.1

```text
v0.1 -> v0.2 changes for C1:

  - Backbone weight: ViT-L (~300M, DUSt3R checkpoint) -> DINOv3-S
    (~22M backbone, separately downloadable Meta weight)
  - Input resolution: keeps 384x512 (no change)
  - Patch size: 14 (DINOv2/v3 convention; v0.1 may have used 16,
    confirm against SPEC-001 v0.1 if pinning matters)
  - Heads: re-init from scratch (new task heads; the v0.1 task
    head weights are tied to ViT-L feature space and do not
    transfer; this is a fresh-train setup)
  - Frozen vs trainable: backbone frozen by default; only new
    heads trained. Optional: unfreeze top-N DINOv3 blocks for
    adaptation. v0.2 ablation spec addendum should list both.

  Memory savings (inferred):
  - Backbone params: ~300M -> ~22M (~14x reduction)
  - Backbone VRAM at fp16: ~600 MB -> ~50 MB (~12x reduction)
  - Forward latency: ~50-80 ms -> ~10-15 ms (~5x speedup)

  Risk: pointmap quality may suffer. DUSt3R-quality pointmaps are
  the de facto baseline; if DINOv3-S features cannot match this,
  v0.2 falls back to DINOv3-B (still <100M backbone) or, in the
  worst case, retains DINOv3-L (~300M; matches ViT-L weight
  class but with stronger features). Frame budget impact at -B
  / -L: -B is borderline feasible at 30 FPS, -L exceeds budget.
```

## Risk / honest limits

```text
1. Frozen-backbone setup may underperform end-to-end fine-tuned
   ViT-L pipelines (DUSt3R-style). This is the main quality
   risk. Mitigation: optional top-N unfreezing; ablation listed.

2. DINOv3 features have strong semantic content but may have
   weaker geometric content than purpose-trained DUSt3R features.
   Mitigation: pointmap_head capacity; possibly multi-stage
   training (head warmup -> partial unfreeze).

3. Migration to DINOv3 weights does NOT come with DUSt3R-style
   pretraining over multi-view 3D. v0.2 must re-train the
   pointmap_head + confidence_head + evidence_head from scratch
   on a 3R dataset. Training data scope is OUT of cycle 018
   scope; v0.2 spec lists "training plan TBD; gated on separate
   DEC".

4. DINOv3-Small at 22M params may be too small for the joint
   demands of (a) pointmap regression + (b) feature quality for
   downstream cross-image matching (used by C5 Composer routing
   to MASt3R). Pre-empt: spec lists -S as default with -B as
   automatic fallback if benchmark gap exceeds threshold.

5. License / availability check: DINOv3 weights, license terms,
   and Hugging Face hub paths need primary verification before
   any download gate. v0.2 spec carries this as "TBD; primary
   verification needed before checkpoint download authorization".
```

## What this memo does NOT authorize

```text
- No DINOv3 implementation. No checkpoint download. No code touch.
- No claim that DINOv3-S meets pointmap quality bar of DUSt3R
  ViT-L. Quality claim is `inferred from feature benchmark
  transfer`; pointmap-specific quality is unmeasured.
- No new dependency add to dream3r server env (DINOv3 weights
  are accessible via Meta hub; download requires future gate).
- No retroactive edit of v0.1 architecture spec body. v0.1's C1
  description remains as-was; v0.2 SPEC-004 is the consumer.
```

## Reading order for next pass

If a future cycle authorizes DINOv3-Memory-Critic integration, the
reading order is:

```text
1. This memo (architectural hypothesis)
2. DINOv3 paper (Meta 2025) — primary verification pass needed
3. DUSt3R / MASt3R / Spann3R source code (already on dream3r server
   under /hdd3/kykt26/) for ViT-L head architecture reference
4. specs/SPEC-20260506-004 v0.2 spec (consumer)
5. SPEC-002 ablation plan v0.1 + v0.2 addendum (DINOv3-S vs -B
   ablation; frozen vs partial unfreeze ablation)
```

Implementation gate (separate DEC) would specify: which DINOv3
checkpoint, frozen vs unfrozen scope, training data, head
architectures, evaluation metric.
