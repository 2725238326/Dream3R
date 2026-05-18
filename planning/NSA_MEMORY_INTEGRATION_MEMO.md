# NSA × C2 Memory Integration Memo

artifact_id: planning/NSA_MEMORY_INTEGRATION_MEMO.md

date: 2026-05-06

cycle: 018 (S3 deliverable per DEC-20260506-002)

status: design memo (paper-derived sketch; no implementation)

length_target: ~1 page (this file is ~150 lines)

linked_artifacts:
- decisions/DEC-20260506-002-cycle-018-launch-v02-architecture.md (parent)
- specs/SPEC-20260506-001-dream3r-architecture.md (v0.1 C2 Memory section)
- specs/SPEC-20260503-002-executive-memory.md (Memory finalist spec)
- planning/COMPOSER_CAPABILITY_DESCRIPTORS.md (sibling cycle 018 deliverable)
- specs/SPEC-20260506-004-dream3r-architecture-v02.md (consumer; cycle 018 S4)

## Source paper

Native Sparse Attention (NSA), DeepSeek 2025 (arxiv 2502.11089).

Evidence label: `paper-known` for the mechanism; `inferred` for transfer
to vision / 3R; `speculative` for Dream3R-specific gating signals
(Critic confidence + Permanence anchor co-driving the selection gate).

NSA was published as a long-context LLM efficiency mechanism. There is
NO published 3R / vision validation. The transfer below is an
architectural hypothesis, not a measured result.

## What NSA contributes

NSA has three components per attention block:

```text
1. Compressed branch: a coarse global view of the full sequence
   (cheap; e.g., aggregated tokens at coarser granularity).

2. Selected branch: top-k full-attention tokens chosen by a
   learned selection gate (the unique mechanism — sparse but
   end-to-end trained).

3. Sliding branch: a fixed local window (cheap; preserves recency).

The three branches are gated and combined per query. Selection is
hardware-aware (block-level) so the sparsity translates to real
wall-clock speedup, not just FLOPs.
```

## Why NSA fits the v0.2 Memory module

v0.1 architecture specified C2 Memory as an SSM/Mamba layer over
evidence tokens, but did not specify what is stored, retrieved, or
evicted. The 2026-05-06 dialog reframed Memory along directions:

```text
A. anchor-based retrieval memory (k-v memory bank with explicit
   retrieval objective)
B. hierarchical memory (short-term window / medium-term state /
   long-term sparse anchors)
```

NSA's three-branch structure maps onto A+B almost cleanly:

```text
NSA branch         <-> v0.2 Memory hierarchy
-------------------     ---------------------------
Compressed         <-> long-term compressed scene summary
Selected (top-k)   <-> A: anchor bank retrieval (k-v lookup)
Sliding window     <-> short-term per-frame context
```

The medium-term tier (B's middle layer) is the bridge: it can be
served by retained Mamba SSM state (v0.1 substrate hypothesis) OR by
a second NSA layer with longer window. Either is consistent with v0.2
spec; pinning that choice is a v0.3 question.

## Concrete v0.2 design sketch

```text
C2 Memory module structure (v0.2):

  Inputs (per window tick t):
    - perception_summary_t  from C1 Perceiver
    - evidence_tokens_t     from C4 Critic (T3 Bus)
    - permanence_anchors_t  from C3 Permanence (T5 Bus, read-only)
    - critic_confidence_t   from C4 Critic (T3 Bus)

  Anchor bank A_t (bounded; maintained by C2):
    - capacity K (proposed K = 256; param)
    - each entry: anchor_embedding (D-dim) + scene_pose_metadata
                + freshness_counter + permanence_link
    - eviction policy: LRU among non-permanence-anchored entries;
      permanence-anchored entries are evict-protected
      (interaction with C3 Permanence ownership: C3 owns
       permanence_link state; C2 reads it but does not mutate it)

  NSA-style retrieval per tick:
    Compressed branch:
        - aggregate A_t into ~32 compressed summary tokens
        - cheap full-attention to a coarse "scene context"

    Selected branch (the load-bearing path):
        - selection gate g(query_t, anchor_embedding, evidence,
                          critic_confidence) -> top-k (proposed k = 8)
        - selection gate INPUT includes Bus signals:
            * critic_confidence_t (low confidence -> bias toward
              retrieving more anchors for verification)
            * permanence_link (anchored objects always retrievable
              with priority)
        - retrieved top-k anchors -> full-attention with current
          window's evidence tokens

    Sliding branch:
        - last W frames of evidence (proposed W = 4) -> full attention
        - guarantees short-term coherence

  Outputs (per window tick t):
    - memory_state_t       published to T6 Bus
    - selected_anchors_t   published to T5 Bus (read by C3 Permanence
                           for identity update)
    - memory_retrieval_log published to Bus contract_log (per cycle 016
                           v2.1 contract handoff)

  Update path:
    - new anchor candidates (from C3 Permanence T5 publish) admitted
      to bank if (a) bank has capacity OR (b) candidate beats lowest-
      LRU non-protected entry in a proposed-merit metric (inferred
      v0.2; needs measured definition in a later pass).
```

## How this resolves "Memory hollow" critique

v0.1's C2 was a black-box SSM with no specified content. v0.2's C2 has:

```text
- explicit storage: bounded anchor bank with eviction policy
- explicit retrieval: NSA-style gated selection over the bank
- explicit gating signal: Critic confidence + Permanence link
- explicit cross-module contract: bus publishes selected anchors,
  Permanence reads them for identity update, Critic reads them for
  verification reprojection
- explicit eviction: LRU with Permanence protection
```

This is the v0.2 main-claim D (Heterogeneous Composer) +
main-claim A (Verification-as-architecture) connection point: the
selection gate is itself a Critic-driven decision (low confidence
-> retrieve more for verification), and the retrieval-driven
verification path can route to EXPERT-07 Test3R when retrieval
disagrees with current pointmap.

## Risk / honest limits

```text
1. NSA is an LM-domain mechanism. No published vision / 3R use.
   The transfer is architectural-hypothesis-grade, not validated.
   v0.2 spec MUST carry this as `speculative` evidence label; any
   ablation plan addendum should include "remove NSA -> fall back
   to plain anchor bank with cosine top-k retrieval" as a tier-1
   ablation.

2. NSA's hardware-aware kernel is FlashAttention-3 era. The
   dream3r server runs torch 2.5.1 + cu121 on TITAN RTX (not
   H100). The kernel-level wall-clock speedup may not transfer;
   the algorithmic sparsity still applies but the practical
   latency benefit is reduced. v0.2 spec should NOT claim
   measured streaming budget compliance until benchmarked.

3. Bounded anchor bank with K=256 is a guess. Real K depends on
   scene complexity, sequence length, and per-anchor embedding
   dimension. v0.2 lists this as a hyperparameter `tbd`, not
   pinned.

4. Selection gate input (critic_confidence + permanence_link)
   is the speculative cross-module-signal claim. There is no
   prior-art validation that mixing these signals into an NSA
   selection gate produces useful 3R retrieval. This is a
   first-class ablation candidate (ABL addendum needed).

5. The interaction between NSA selected branch and Mamba state
   (if both are kept) is not specified here. If v0.3 keeps both,
   a "which owns medium-term state" decision is needed. v0.2
   defers this; lists Mamba as optional medium-term substrate.
```

## What this memo does NOT authorize

```text
- No NSA implementation. No code touch. No checkpoint download.
- No claim that v0.2 streaming budget is met by NSA-augmented
  C2 Memory. Budget table in SPEC-004 carries "inferred"
  evidence label.
- No new dependency add to dream3r server env.
- No retroactive edit of v0.1 architecture spec body. v0.1's C2
  description remains as-was; v0.2 SPEC-004 is the consumer of
  this memo.
```

## Reading order for next pass

If a future cycle authorizes NSA-Memory implementation, the reading
order is:

```text
1. This memo (architectural hypothesis)
2. NSA paper (arxiv 2502.11089) — primary verification pass needed
3. specs/SPEC-20260503-002-executive-memory.md (Memory finalist
   spec; v2.1 cross-spec contract for what Memory must publish/read)
4. specs/SPEC-20260506-004 v0.2 spec (consumer)
5. specs/SPEC-20260506-002 ablation plan v0.1 + a v0.2 addendum
   defining NSA-removal ablation
```

Implementation gate (separate DEC) would specify: which 3R sequence
benchmark, how many anchors K, retrieval top-k, evaluation metrics
(retrieval recall, route_regret reduction, drift over long sequence).
