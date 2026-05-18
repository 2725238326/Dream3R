# Dream3R C2 Memory v0.3 design study

Last updated: 2026-05-08

Status: design study, research-only.

Scope:

- Read CUT3R server code under `/hdd3/kykt26/code/cut3r/`.
- Read Spann3R server code under `/hdd3/kykt26/code/spann3r/`.
- Compare both memory mechanisms against Dream3R's current C2 implementation under `/hdd3/kykt26/code/dream3r/`.
- Propose a C2 Memory v0.3 direction.

Non-scope:

- No Dream3R source code change.
- No model run.
- No training.
- No checkpoint download.
- No claim that the proposal is empirically validated.

Evidence labels used below:

- `code-observed`: directly read in the server source code.
- `spec-observed`: directly read in Dream local architecture spec.
- `inferred`: architectural interpretation from code behavior.
- `speculative`: proposed Dream3R mechanism not yet implemented or measured.

## Executive summary

Dream3R C2 v0.2 currently looks like a control sketch with memory-shaped parts, not a 3R memory mechanism. The code has a GRU vector state, a bounded vector-only AnchorBank, and an NSA-style three-branch retrieval approximation. This is useful scaffolding, but it loses the two things that make CUT3R and Spann3R relevant:

1. CUT3R shows that persistent memory can be implemented as a learned state-token stream that exchanges information with frame tokens through repeated decoder cross-attention.
2. Spann3R shows that streaming 3R memory benefits from an explicit spatial key/value bank tied to DUSt3R decoded tokens and pointmap-derived values, with query-based readout, duplicate filtering, and usage-based pruning.

The v0.3 proposal is therefore:

```text
C2 Memory v0.3 = latent state tokens + explicit spatial bank + bus-gated write policy

Compressed branch: CUT3R-like state tokens.
Selected branch: Spann3R-like spatial memory readout.
Sliding branch: recent frame token/value buffer.
```

This should replace the single-vector GRU core as the conceptual center of C2. GRU may remain only as a small gate/controller, not as the memory substrate.

## CUT3R memory mechanism

### State definition and initialization

Evidence: `code-observed`.

Key locations:

- `/hdd3/kykt26/code/cut3r/src/dust3r/model.py:109-112`
- `/hdd3/kykt26/code/cut3r/src/dust3r/model.py:272-289`
- `/hdd3/kykt26/code/cut3r/src/dust3r/model.py:538-568`
- `/hdd3/kykt26/code/cut3r/src/dust3r/model.py:705-711`

CUT3R defines a fixed number of learned state tokens:

```text
state_size default: 324
state_pe default: 2d
state token source: nn.Embedding(state_size, enc_embed_dim)
decoder projection: decoder_embed_state
state token runtime shape: [B, state_size, dec_embed_dim]
```

The state positional encoding can be 1D, 2D, or absent. In the default 2D mode, the state tokens are arranged into a synthetic grid. This matters because the state is not a single vector. It is a small learned memory field that can participate in RoPE-aware attention like a token set.

Important limitation: `_init_state` does not appear to condition the initial state token values on the first frame content. It creates learned register tokens and projects them into decoder dimension. The first frame influences state only through the recurrent decoder interaction.

### State and frame cross-attention

Evidence: `code-observed`.

Key locations:

- `/hdd3/kykt26/code/cut3r/src/dust3r/blocks.py:178-243`
- `/hdd3/kykt26/code/cut3r/src/dust3r/blocks.py:246-297`
- `/hdd3/kykt26/code/cut3r/src/dust3r/model.py:660-698`

CUT3R uses a standard decoder block with:

```text
self-attention on x
cross-attention from x to y
MLP update
```

The recurrent decoder runs two parallel streams:

```text
f_state = state stream
f_img   = current frame stream, optionally with a pose token prepended

for each paired decoder layer:
  f_state attends to f_img through dec_blocks_state
  f_img attends to f_state through dec_blocks
```

This is the crucial mechanism. State is not updated by a scalar recurrent cell. It is updated by token-to-token interaction with the current frame. The frame stream also reads the state stream before downstream pointmap prediction. This makes memory bidirectional:

- state receives current visual/geometric evidence
- current frame prediction receives accumulated state context

### Persistence across frames

Evidence: `code-observed`.

Key locations:

- `/hdd3/kykt26/code/cut3r/src/dust3r/model.py:735-814`
- `/hdd3/kykt26/code/cut3r/src/dust3r/model.py:816-900`
- `/hdd3/kykt26/code/cut3r/src/dust3r/model.py:1015-1099`
- `/hdd3/kykt26/code/cut3r/src/dust3r/inference.py:95-190`

CUT3R persists state by carrying `(state_feat, state_pos, init_state_feat, mem, init_mem)` across frames. The update rule is explicit:

```text
new_state_feat = recurrent_decoder(state_feat, current_frame_feat)
state_feat = new_state_feat * update_mask + state_feat * (1 - update_mask)
state_feat = init_state_feat * reset_mask + state_feat * (1 - reset_mask)
```

The same update/reset logic applies to a local pose memory `mem`.

This gives two stability controls:

- `update_mask`: prevents state mutation when a frame/window should not write.
- `reset_mask`: returns state to the initial learned state when sequence boundaries or invalid states require reset.

The training/inference code also detaches state between chunks in `inference.py:126-134`, which limits unbounded gradient propagation across long sequences. That is a training stability mechanism, not a semantic memory mechanism.

### Local pose memory

Evidence: `code-observed`.

Key locations:

- `/hdd3/kykt26/code/cut3r/src/dust3r/model.py:140-222`
- `/hdd3/kykt26/code/cut3r/src/dust3r/model.py:261-271`
- `/hdd3/kykt26/code/cut3r/src/dust3r/model.py:763-790`

CUT3R also has `LocalMemory`, used as `pose_retriever` when pose head is enabled. It contains:

```text
learned memory table: mem [1, local_mem_size, 2 * v_dim]
write: update_mem(mem, feat_k, feat_v)
read: inquire(query, mem)
```

Both read and write are decoder-block cross-attention operations. It is not a cosine top-k bank. It learns how to write image-level features and pose-token features into a compact table, then retrieves a pose token for future frames.

For Dream3R, this suggests that C2 should not treat "pose/global memory" and "spatial anchor memory" as the same object. CUT3R separates a latent state-token stream from a small local pose memory.

### Outputs

Evidence: `code-observed`.

The model outputs frame predictions through `_downstream_head` using image decoder tokens at selected depths. It can also return state arguments when `ret_state=True`.

So CUT3R has both:

- prediction outputs: pointmaps/confidence/pose depending on head configuration
- recurrent state outputs: latent state tokens and local pose memory

For Dream3R, the useful takeaway is not only "persistent state exists". The key is that state is a first-class token stream that participates in the reconstruction decoder.

## Spann3R memory mechanism

### Memory data structure

Evidence: `code-observed`.

Key locations:

- `/hdd3/kykt26/code/spann3r/spann3r/model.py:11-40`
- `/hdd3/kykt26/code/spann3r/spann3r/model.py:80-96`

Spann3R defines an explicit `SpatialMemory` object with:

```text
mem_k:     key tokens
mem_v:     value tokens
mem_c:     optional confidence weights
mem_count: age/read accounting
mem_attn:  accumulated attention received
mem_pts:   optional stored 3D points
mem_imgs:  optional stored image payloads
lm:        long-memory counter
wm:        working-memory counter
```

This is much closer to a 3R memory than Dream3R's current `AnchorBank`, because it can preserve spatial payloads and learned values, not just a state vector embedding.

### Query and key generation

Evidence: `code-observed`.

Key locations:

- `/hdd3/kykt26/code/spann3r/spann3r/model.py:221-248`
- `/hdd3/kykt26/code/spann3r/spann3r/model.py:299-320`
- `/hdd3/kykt26/code/spann3r/spann3r/model.py:491-508`

Spann3R wraps a pretrained DUSt3R model and uses DUSt3R features plus decoded tokens:

```text
feat_k = attn_head(concat(image_encoder_feat, decoder_feat))
cur_v  = value_encoder(pointmap_patch_embed(res1.pts3d))     when use_feat=False
cur_v  = value_encoder(dec1[-1])                             when use_feat=True
write value = cur_v + feat_k
```

The query for reading memory is the current or next frame key, especially `feat_k2` from the second view in a pair. In the online forward pass:

```text
if feat_k2 exists:
  feat_fuse = spatial_memory.memory_read(feat_k2, res=True)
else:
  feat_fuse = feat1

dec1, dec2 = DUSt3R_decoder(feat_fuse, pos1, feat2, pos2)
```

This is important: memory readout does not happen after reconstruction as a bookkeeping step. It alters the feature stream before the DUSt3R decoder predicts pointmaps.

### Retrieval

Evidence: `code-observed`.

Key locations:

- `/hdd3/kykt26/code/spann3r/spann3r/model.py:145-183`

Spann3R retrieves by normalized dot-product attention:

```text
affinity = einsum(norm_q(feat), norm_k(flatten(mem_k))) / sqrt(C)
if mem_c exists:
  affinity *= mem_c
attn = softmax(affinity)
if memory dropout exists:
  attn = dropout(attn)
if attn_thresh > 0:
  attn below threshold is zeroed
  attention is renormalized
out = einsum(attn, norm_v(flatten(mem_v)))
if residual:
  out = out + feat
```

Memory also records how much attention each stored item receives:

```text
mem_attn += sum(attn over query patches)
```

This gives Dream3R a concrete alternative to pure cosine top-k. It is query-token to memory-token attention with value aggregation, thresholding, and usage accounting.

### Write filtering and pruning

Evidence: `code-observed`.

Key locations:

- `/hdd3/kykt26/code/spann3r/spann3r/model.py:97-143`
- `/hdd3/kykt26/code/spann3r/spann3r/model.py:185-210`

Spann3R checks similarity against recent working memory before adding a new frame:

```text
mean patch correlation with working memory > sim_thresh -> skip write
```

It then manages two horizons:

- working memory: last `work_mem_size` frames
- long memory: bounded by `long_mem_size`, default 4000 tokens

When long memory exceeds the budget, it prunes by `mem_attn / mem_count`, while protecting young items by assigning high keep weight when `mem_count < work_mem_size + 5`.

This is a stronger memory policy than LRU. It keeps tokens that remain useful to future queries, not just tokens that are recent.

### Integration with DUSt3R

Evidence: `code-observed`.

Key locations:

- `/hdd3/kykt26/code/spann3r/spann3r/model.py:221-226`
- `/hdd3/kykt26/code/spann3r/spann3r/model.py:322-331`
- `/hdd3/kykt26/code/spann3r/spann3r/model.py:473-539`

Spann3R does not replace DUSt3R. It inserts memory around DUSt3R:

1. Use DUSt3R image encoder.
2. Read spatial memory to fuse a memory-informed feature for view 1.
3. Use DUSt3R decoder on fused view 1 and current view 2.
4. Use DUSt3R downstream head to regress pointmaps.
5. Encode pointmap or decoder tokens as new memory value.
6. Write current view evidence into `SpatialMemory`.

This is the right pattern for Dream3R if the goal is architecture-level novelty without building a new backbone from scratch.

## CUT3R and Spann3R comparison

Evidence: `code-observed` plus `inferred`.

| Axis | CUT3R | Spann3R | Dream3R implication |
| --- | --- | --- | --- |
| Memory form | Learned latent state tokens | Explicit key/value spatial memory | Use both, not one |
| Main state shape | `[B, S, D]` token grid | `[B, T * P, D]` memory bank | C2 should stop being only `[B, D]` |
| Read mechanism | Decoder cross-attention between state and frame | Query-token attention over stored keys/values | NSA selected branch should look more like Spann3R |
| Write mechanism | New state tokens from recurrent decoder | Append key/value after similarity check | Need separate state update and spatial write policy |
| Eviction | Reset/update masks, no explicit spatial eviction for state tokens | Usage-based pruning and duplicate skip | Add attention accounting to AnchorBank |
| Geometry payload | Implicit in frame decoder output | Optional stored points/images and pointmap-derived values | Dream anchors should carry geometry, not only embeddings |
| Decoder coupling | State directly influences frame decoder | Memory read directly influences DUSt3R decoder input | Memory must affect reconstruction tokens before prediction |
| Stability | Fixed token count, update/reset masks, chunk detach | Bounded long memory, working memory, thresholded attention | Combine fixed latent state with bounded explicit memory |

Interpretation:

- CUT3R is better for compressed scene context and temporal continuity.
- Spann3R is better for explicit spatial retrieval, relocalization, and remembering surfaces/points.
- Dream3R should use CUT3R for the compressed branch and Spann3R for the selected branch.

## Dream3R current C2 gap

Evidence: `code-observed` and `spec-observed`.

Key current code:

- `/hdd3/kykt26/code/dream3r/dream3r/modules.py:140-287`
- `/hdd3/kykt26/code/dream3r/dream3r/memory_anchor_bank.py:1-53`
- `/hdd3/kykt26/code/dream3r/dream3r/nsa_attention.py:1-68`
- `/hdd3/kykt26/code/dream3r/dream3r/model.py:116-137`

Current C2:

```text
perception_summary + evidence_flat + bus context
  -> input projection
  -> stacked GRUCell state update
  -> optional NSA retrieval from AnchorBank vector embeddings
  -> soft mixture of update modes
  -> vector state stored into AnchorBank
```

Problems:

1. State is a single vector `[B, d_state]`, while both CUT3R and Spann3R use token sets.
2. AnchorBank stores only embeddings, freshness, valid mask, and permanence flag. It does not store pointmap/value tokens, frame/source metadata, confidence, or usage statistics.
3. NSAThreeBranch gathers selected keys but not stored values. It averages compressed, selected, and sliding branches into a vector output. This is not yet a 3R memory readout.
4. C2 receives pooled evidence after C1, but memory does not feed back into a reconstruction decoder before pointmap prediction. That makes memory mostly a latent controller, not a spatial reconstruction mechanism.
5. Eviction is LRU among non-permanent entries. Spann3R suggests usefulness-based pruning is more appropriate.

The v0.2 spec already labels NSA-to-3R transfer as speculative in `SPEC-20260506-004-dream3r-architecture-v02.md:269-279` and `616-622`. The code reading confirms that concern. NSA is not the weak part by itself. The weak part is that the memory item is not spatial enough.

## C2 Memory v0.3 proposal

Evidence: `speculative`, grounded in `code-observed` mechanisms above.

### Core design

Replace current `MemorySSM` center with a two-plane memory:

```text
C2MemoryV03State
  latent_tokens: [B, S, D]       # CUT3R-like implicit compressed state
  spatial_bank:
    key:        [M, D] or [B, M, D]
    value:      [M, D]
    points3d:   optional [M, P, 3] or compact point anchors
    confidence: optional [M, 1]
    source:     frame/window/expert id metadata
    freshness:  recency counter
    attn_sum:   accumulated future retrieval attention
    read_count: age/read denominator
    permanent:  C3-owned permanence link as read-only flag
  working_tokens: last W frame/value tokens
```

C2 should expose two outputs:

```text
memory_context_tokens: tokens injected into C1/C2/C4 or a reconstruction decoder
memory_state_t: compact latent summary for bus and next window
selected_anchors_t: spatial bank entries for C3/C4 verification
retrieval_log_t: branch weights, selected ids, attention entropy, write decision
```

### Per-window flow

```text
Inputs:
  current frame/window tokens from C1
  evidence tokens T3
  optional pointmap/value tokens from expert outputs
  bus signals: dynamic_ratio, conflict_score, suppress_static_write, permanence_link

1. Build query tokens
   q_spatial = key_head(concat(current visual tokens, decoder/evidence tokens))
   q_state   = projection(current visual/evidence summary)

2. Read explicit spatial bank
   selected_values = attention(q_spatial, bank.key, bank.value)
   selected_points = gather associated point anchors and metadata
   apply confidence and permanence bias

3. Update latent state tokens
   latent_tokens, frame_tokens = recurrent cross-attention(
     latent_tokens,
     current frame tokens + selected_values
   )

4. Produce memory context
   context = fuse(latent_tokens, selected_values, working_tokens)

5. Decide writes
   if suppress_static_write is true:
     block static writes
   if similarity to working memory is too high:
     skip duplicate write
   if critic_conflict is high:
     downweight or quarantine write
   else:
     write key/value/points/confidence/source metadata

6. Prune
   protect recent working memory
   protect C3 permanent anchors
   keep high utility entries by attn_sum / read_count
```

### NSA branch reinterpretation

Evidence: `inferred` from CUT3R and Spann3R code.

Dream3R should keep the three-branch vocabulary, but reinterpret the branches as actual 3R memory mechanisms:

```text
Compressed branch:
  CUT3R-like latent state tokens.
  Output: fixed-size scene context tokens.
  Best for: temporal continuity, global scene layout, coarse pose context.

Selected branch:
  Spann3R-like query attention over explicit spatial bank.
  Output: value tokens plus associated points/confidence/source ids.
  Best for: loop closure, relocalization, occlusion recovery, view overlap.

Sliding branch:
  Recent W frame/value tokens, not only a vector buffer.
  Output: local temporal context.
  Best for: short-range motion and avoiding stale long-memory reads.
```

The branch gate should not be a generic MLP over three averaged vectors only. It should also read:

- attention entropy of selected branch
- critic conflict score
- dynamic ratio from C3 Permanence
- pointmap confidence from source expert
- cache pressure and bank occupancy

### Minimal API sketch

Evidence: `speculative`.

```python
class C2MemoryV03(nn.Module):
    def init_state(self, batch_size, device):
        return {
            "latent_tokens": learned_state_tokens.expand(batch_size, -1, -1),
            "spatial_bank": SpatialAnchorBank(...),
            "working_tokens": None,
        }

    def forward(self, frame_tokens, evidence_tokens, prev_state, bus_reads, pointmap_tokens=None):
        q = self.key_head(torch.cat([frame_tokens, evidence_tokens], dim=-1))
        selected = prev_state["spatial_bank"].read(q, bus_reads)
        latent_tokens, frame_context = self.state_frame_decoder(
            prev_state["latent_tokens"],
            torch.cat([frame_tokens, selected.value_tokens], dim=1),
        )
        context = self.branch_fuser(latent_tokens, selected.value_tokens, prev_state["working_tokens"], bus_reads)
        write = self.write_policy(q, pointmap_tokens, selected, bus_reads)
        next_bank = prev_state["spatial_bank"].write_and_prune(write)
        return context, {"latent_tokens": latent_tokens, "spatial_bank": next_bank, ...}
```

This is intentionally not a full implementation. It states the architectural boundary: token memory first, GRU controller second.

## Relation to Dream3R modules

Evidence: `speculative`, constrained by current Dream3R C1-C6 design.

### C1 Perceiver

C1 should output frame/window tokens suitable for memory, not only a pooled `perception_summary`. Current C2 can still receive a summary for gates, but v0.3 needs token-level input.

Required future C1 outputs:

```text
frame_tokens: [B, P, D]
evidence_tokens: [B, E, D]
optional point/value tokens from expert adapters
```

### C2 Memory

C2 owns:

- latent state tokens
- spatial anchor bank keys/values/accounting
- write policy
- retrieval logs

C2 may read C3 permanence flags but must not mutate C3 identity state.

### C3 Permanence

C3 should provide:

- permanent anchor flags
- suppress_static_write
- dynamic_ratio
- identity/slot links for selected anchors

In v0.3, C3 becomes more useful because selected anchors carry geometry payloads and source ids, not just vector embeddings.

### C4 Critic

C4 should read:

- selected anchors
- selected point/value payloads
- retrieval entropy
- conflict score history

C4 should write back conflict signals that affect future C2 writes:

```text
high conflict -> quarantine or lower confidence for current write
low conflict  -> allow consolidation
```

### C5 Composer

C5 can route based on memory state:

- if selected branch has high confidence and low entropy, prefer cheap local reconstruction path
- if memory read is uncertain, route to Test3R or stronger expert
- if bank occupancy/cache pressure is high, trigger compression/pruning policy

This keeps Memory and Composer coupled by bus signals, not by hidden side effects.

## Ablation plan for v0.3

Evidence: `speculative`.

The smallest meaningful ablations are:

1. Baseline: current Dream3R C2 v0.2 vector GRU + AnchorBank + NSAThreeBranch.
2. CUT3R-only: replace vector state with state tokens and state-frame cross-attention, no explicit spatial bank.
3. Spann3R-only: keep vector gate but replace AnchorBank with spatial key/value memory and attention read.
4. Hybrid: state tokens plus spatial bank, simple fixed branch weights.
5. Hybrid plus bus gates: add Critic/Permanence-driven write and retrieval gates.
6. Hybrid plus NSA gate: learned branch fusion over compressed, selected, and sliding branches.

Useful metrics:

- frame-to-frame pointmap stability
- long-sequence drift proxy
- loop/overlap retrieval precision
- memory write redundancy rate
- bank survival utility, measured by future attention
- route_regret when C5 uses memory uncertainty
- wall-clock per frame on TITAN RTX

## Risks and open questions

### Risks

1. Token-state compute may exceed the 30-50 ms target.
   Evidence: `inferred`. CUT3R uses decoder cross-attention across state and image tokens. Dream3R must keep state token count small or compress aggressively.

2. Spatial bank may become stale under dynamic scenes.
   Evidence: `inferred`. Spann3R has duplicate filtering and pruning, but not a full dynamic-object memory policy. Dream3R needs C3/C4 gates for moving objects.

3. NSA terminology may hide the actual mechanism.
   Evidence: `spec-observed` plus `code-observed`. Current NSA code is branch averaging over vector embeddings. v0.3 should define memory payloads and read/write semantics first, then use NSA as an optimization label second.

4. Value-token source is unresolved.
   Evidence: `unknown`. Spann3R can use pointmap patch embedding or decoder features. Dream3R must decide whether values come from C1 tokens, expert pointmaps, C4-verified points, or a learned value encoder.

5. Training path is nontrivial.
   Evidence: `inferred`. CUT3R and Spann3R are trained around their memory mechanisms. Dream3R cannot claim the hybrid works without a later training or at least fine-tuning plan.

### Open questions

1. Should Dream3R state tokens be learned registers like CUT3R, or initialized from the first frame?
2. Should spatial values be pointmap-derived like Spann3R or expert-output-derived from the Composer pool?
3. How many latent state tokens are acceptable under the frame budget: 32, 64, 128, or 324?
4. Should C2 use one shared spatial bank or separate banks for static scene, dynamic objects, and pose/global context?
5. Does NSA add value after a Spann3R-style read is implemented, or should the first v0.3 prototype use plain attention plus pruning?
6. How should C4 Critic mark a write as "quarantined" without violating C2 state ownership?
7. What is the smallest server-side smoke test that can compare current v0.2 C2 against CUT3R-only and Spann3R-only memory without training?

## Recommended next step

Do not implement the full hybrid immediately.

Recommended sequence:

1. Write a v0.3 C2 spec addendum that supersedes Delta 3 from vector AnchorBank to token state plus spatial bank.
2. Define the exact memory state schema and bus publications.
3. Build a small read-only prototype notebook or script that feeds recorded token tensors through:
   - vector AnchorBank retrieval
   - Spann3R-style attention read
   - CUT3R-style state-token cross-attention
4. Only after that, touch `/hdd3/kykt26/code/dream3r/dream3r/modules.py`.

The main research correction is:

```text
Dream3R C2 should stop being "GRU + vector cache + NSA label".
It should become "state-token recurrence + spatial key/value memory + geometry-aware bus-gated writes".
```

