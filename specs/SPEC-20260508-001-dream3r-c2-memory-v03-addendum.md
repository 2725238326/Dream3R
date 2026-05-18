# Dream3R C2 Memory v0.3 addendum

spec_id: SPEC-20260508-001

spec_kind: architecture addendum, delta-only on C2 Memory

parent_spec: SPEC-20260506-004 (Dream3R architecture v0.2; Delta 3 is superseded by this addendum)

parent_decision: DEC-20260508-002 (cycle 026 C2 Memory v0.3 addendum and guidance correction)

date: 2026-05-08

cycle: 026

status: v0.3 addendum, candidate-not-final per DEC-20260501-004

honesty_label: every new mechanism claim below carries an evidence label.

linked_artifacts:
- planning/MEMORY_V03_DESIGN_STUDY.md (cycle 025 design study; CUT3R / Spann3R / Dream3R C2 code reading)
- cycles/CYCLE-20260508-002.md (cycle 025 mechanism-study log)
- decisions/DEC-20260508-002-cycle-026-c2-memory-v03-addendum-and-guidance-correction.md
- specs/SPEC-20260506-004-dream3r-architecture-v02.md (v0.2 architecture; Delta 3 superseded here)
- planning/NSA_MEMORY_INTEGRATION_MEMO.md (v0.2 C2 memory planning; historical input)
- cycles/CYCLE-20260508-001.md (cycle 024 scaffold and engineering smoke; baseline, not validation)
- specs/SPEC-20260508-002-dream3r-memory-v03-ablation-addendum.md (cycle 028 memory-specific ablation map; supersedes the candidate ablation sketch below)

---

## Identity

This addendum updates only the C2 Memory mechanism. It does not rewrite v0.1 or v0.2 architecture in place.

The addendum supersedes the conceptual center of `SPEC-20260506-004` Delta 3:

```text
old v0.2 center:
  bounded vector AnchorBank + NSA-style three-branch vector retrieval

new v0.3 center:
  latent state-token recurrence + explicit spatial key/value memory
  + geometry-aware bus-gated writes
```

The v0.2 AnchorBank and NSA files from cycle 024 remain a runnable scaffold and historical baseline. They are not the current research mechanism.

## Approval and boundaries

Approved in this spec:

- C2 Memory state schema.
- C2 read/write protocol.
- Bus publications and bus reads for C2 v0.3.
- Relationship to C1/C3/C4/C5/C6.
- Prototype and ablation sequence.
- Paper evidence-boundary correction.

Not approved by this spec:

- server code edit
- model run
- training or fine-tuning
- checkpoint download
- KYKT navigation or frontend change
- final thesis selection
- claim that the hybrid memory mechanism works empirically

Evidence labels:

```text
code-observed:
  directly read in CUT3R, Spann3R, or Dream3R source during cycle 025.

spec-observed:
  directly present in existing Dream specs or cycle logs.

engineering-demonstrated:
  cycle 024 runnable scaffold or smoke behavior; useful for plumbing,
  not for research-quality claims.

inferred:
  architectural interpretation from observed code/spec behavior.

speculative:
  proposed Dream3R v0.3 mechanism not yet implemented or measured.
```

## Superseded v0.2 Delta 3

`SPEC-20260506-004` Delta 3 made C2 more concrete by proposing:

```text
AnchorBank:
  K = 256 vector entries
  freshness counter
  permanence_link protection
  LRU among non-permanent entries

NSA-style retrieval:
  compressed branch
  selected top-k anchor branch
  sliding branch
  selection gate biased by Critic confidence and permanence_link
```

Evidence status: `spec-observed`.

Cycle 024 implemented this shape as a server-side scaffold. Evidence status: `engineering-demonstrated` for code plumbing only.

Cycle 025 then found the load-bearing gap:

```text
The memory item is not spatial enough.
The current C2 stores vectors, not spatial values or point payloads.
The current readout does not feed reconstruction tokens before pointmap prediction.
```

Evidence status: `code-observed` and `inferred`.

Therefore v0.3 supersedes Delta 3 as follows:

| Axis | v0.2 Delta 3 | v0.3 replacement | Evidence label |
| --- | --- | --- | --- |
| State shape | single vector GRU state | latent state tokens `[B,S,D]` | speculative, grounded in CUT3R code-observed |
| External memory | vector AnchorBank | spatial key/value bank with optional point payloads | speculative, grounded in Spann3R code-observed |
| Selected branch | top-k vector anchors | query-token attention over spatial keys/values | speculative |
| Compressed branch | vector long summary | CUT3R-like state-token recurrence | speculative |
| Sliding branch | recent vector evidence | recent frame/value tokens | speculative |
| Eviction | LRU among non-permanent anchors | duplicate filter + usefulness pruning + permanence protection | speculative |
| Decoder coupling | latent controller after C1 | memory context tokens available before reconstruction prediction | speculative |
| NSA role | named mechanism center | optional optimization vocabulary after payload semantics are fixed | inferred |

## C2 Memory v0.3 state schema

Evidence status: `speculative`, grounded in cycle 025 `code-observed` findings.

```text
C2MemoryV03State:

  latent_tokens:
    shape: [B, S, D]
    owner: C2
    purpose: compressed scene continuity and temporal state
    source: learned registers plus optional first-frame initialization

  spatial_bank:
    key:
      shape: [B, M, D] or [M, D]
      purpose: query address for spatial recall
    value:
      shape: [B, M, D] or [M, D]
      purpose: memory payload injected into frame/reconstruction tokens
    points3d:
      optional compact point anchors or pointmap patch summaries
    confidence:
      optional source confidence or Critic-adjusted confidence
    source:
      frame id, window id, expert id, adapter id, timestamp
    freshness:
      recency counter
    attn_sum:
      accumulated future retrieval attention
    read_count:
      accounting denominator for utility pruning
    permanent:
      read-only C3 permanence flag or link id
    quarantine:
      C4-driven flag for uncertain writes

  working_tokens:
    last W frame/value token sets
    purpose: short-horizon local continuity and duplicate filtering

  retrieval_log:
    selected ids, branch weights, attention entropy, cache pressure,
    write action, prune action, bus reads used
```

Required invariant:

```text
C2 owns memory storage and retrieval.
C3 owns permanence identity and dynamic/static state.
C4 owns conflict judgment.
C5 owns expert routing.
C6 owns typed publication and read contracts.

C2 may read C3/C4/C5/C6 signals through the bus.
C2 must not mutate C3 identity state, C4 confidence history, or C5 route tables.
```

Evidence status: `spec-observed` for state ownership from v0.1/v0.2, `speculative` for new fields.

## Per-window C2 protocol

Evidence status: `speculative`.

```text
Inputs:
  frame_tokens from C1
  evidence_tokens T3
  optional decoder/value tokens from expert outputs
  optional pointmap patch summaries
  bus reads:
    conflict_score
    dynamic_ratio
    suppress_static_write
    permanence_link
    capability_match
    cache_pressure

Step 1. Build memory queries
  q_spatial = key_head(frame_tokens, evidence_tokens)
  q_state = state_query_head(summary(frame_tokens, evidence_tokens))

Step 2. Read explicit spatial bank
  selected = attention(q_spatial, bank.key, bank.value)
  apply confidence bias
  apply permanence bias
  return selected value tokens, point payloads, source ids, entropy

Step 3. Update latent state tokens
  latent_tokens_t, frame_context_t =
    state_frame_decoder(latent_tokens_{t-1},
                        concat(frame_tokens, selected.value_tokens, working_tokens))

Step 4. Fuse branch context
  compressed_branch = latent_tokens_t
  selected_branch = selected.value_tokens + selected point metadata
  sliding_branch = working_tokens
  memory_context_tokens = branch_fuser(
    compressed_branch,
    selected_branch,
    sliding_branch,
    bus reads,
    retrieval entropy,
    bank occupancy)

Step 5. Decide writes
  if suppress_static_write:
    block static-map write
  elif duplicate_against_working_memory:
    skip duplicate write
  elif conflict_score is high:
    quarantine or lower confidence
  elif dynamic_ratio is high:
    write to dynamic/temporary partition or defer
  else:
    write key/value/points/confidence/source

Step 6. Prune
  protect recent working memory
  protect C3 permanent anchors
  keep high utility by attn_sum / read_count
  evict low utility and stale non-permanent entries

Step 7. Publish bus signals
  memory_context_tokens
  memory_state_summary
  selected_anchor_ids
  selected_anchor_confidence
  retrieval_entropy
  write_action
  bank_occupancy
  cache_pressure
  quarantined_write_count
```

## Branch reinterpretation

Evidence status: `inferred` from cycle 025 code reading.

The three-branch vocabulary can remain, but the branch meaning changes.

### Compressed branch

```text
Mechanism:
  CUT3R-like latent state tokens with recurrent state-frame cross-attention.

Payload:
  fixed-size scene context tokens, not one vector.

Use:
  global continuity, temporal smoothing, coarse pose/context memory.

Failure mode:
  too many state tokens breaks latency budget.
```

### Selected branch

```text
Mechanism:
  Spann3R-like query attention over explicit spatial keys and values.

Payload:
  value tokens plus optional points3d, confidence, source ids, permanence ids.

Use:
  loop/overlap recall, relocalization, occlusion recovery, static scene support.

Failure mode:
  stale or dynamic memory pollution.
```

### Sliding branch

```text
Mechanism:
  recent W frame/value token buffer.

Payload:
  short-range frame tokens, recent point summaries, local source ids.

Use:
  short-term motion, duplicate filtering, low-latency continuity.

Failure mode:
  over-reliance on recent evidence under loop closure.
```

NSA is now a possible optimization for sparse selected reads and branch gating, not the architectural novelty by itself.

## Bus contract changes

Evidence status: `speculative`.

C2 v0.3 should publish:

| Signal | Shape or type | Consumer | Purpose |
| --- | --- | --- | --- |
| `memory_context_tokens` | `[B,N,D]` | C1/C4/C5 or decoder | memory-informed feature context |
| `memory_state_summary` | `[B,D]` | C6/C5 | compact status for routing and logging |
| `selected_anchor_ids` | id list | C3/C4 | inspect which memory entries were used |
| `selected_anchor_confidence` | scalar/vector | C4/C5 | assess reliability of recall |
| `retrieval_entropy` | scalar | C4/C5 | uncertainty and route trigger |
| `write_action` | enum | C6/logging | skip/write/quarantine/defer/reset |
| `bank_occupancy` | scalar | C5/C6 | cache pressure and benchmark logging |
| `cache_pressure` | scalar | C5 | trigger compression or slow-path expert |
| `quarantined_write_count` | scalar | C4/C6 | monitor conflict-driven memory suppression |

C2 v0.3 should read:

| Signal | Owner | Use in C2 |
| --- | --- | --- |
| `conflict_score` | C4 | block, quarantine, or downweight writes |
| `dynamic_ratio` | C3 | route dynamic evidence away from static bank |
| `suppress_static_write` | C3 | hard gate for static memory writes |
| `permanence_link` | C3 | protect or bias selected anchors |
| `capability_match` | C5 | weight value source from selected expert |
| `route_history` | C5/C6 | avoid repeated bad expert-derived writes |
| `cache_pressure` | C2/C6 | self-pressure for pruning and compression |

## Relation to other cores

### C1 Perceiver

Evidence status: `speculative`.

C1 must expose token-level outputs for C2:

```text
frame_tokens: [B,P,D]
evidence_tokens: [B,E,D]
optional value seed tokens from pointmap/expert heads
```

Pooled `perception_summary` is still useful for gates, but it is not enough for spatial memory.

### C3 Permanence

Evidence status: `speculative`.

C3 should provide identity and dynamic/static context. C2 should read those signals and store read-only links inside the bank. C2 must not own object identity.

### C4 Critic

Evidence status: `speculative`.

C4 should affect writes before they become durable:

```text
high conflict:
  quarantine write or lower confidence

low conflict:
  allow consolidation

uncertain conflict:
  defer write and trigger Composer slow-path if needed
```

The Critic's value is not only "reroute expert". It becomes a memory hygiene controller.

### C5 Composer

Evidence status: `speculative`.

C5 should route with memory uncertainty:

```text
selected branch confident:
  prefer cheap or local expert

retrieval entropy high:
  route to stronger expert or Test3R verification

cache pressure high:
  trigger compression/pruning policy
```

### C6 Memory bus

Evidence status: `speculative`.

C6 should enforce typed reads and writes so the memory system remains inspectable. The retrieval log is a research artifact, not only debug output.

## Minimal prototype sequence

Evidence status: `engineering plan`.

Do not implement the full hybrid first. Use the following sequence:

```text
P0. Static tensor prototype
    Local script or notebook only.
    Inputs: recorded or synthetic token tensors.
    Compare vector AnchorBank, spatial-bank attention, and state-token update.
    No checkpoint download. No training.

P1. SpatialAnchorBank module
    Add key/value/points/confidence/source/accounting schema.
    Unit tests for read, write, duplicate filter, utility prune, permanence protect.

P2. State-token recurrence module
    Small state-token cross-attention block.
    Unit tests for shape, reset/update mask, latency envelope.

P3. Bus-gated write policy
    Implement conflict/dynamic/permanence gates.
    Unit tests for skip/write/quarantine/defer.

P4. Integration behind feature flag
    Keep v0.2 C2 path as baseline.
    Add C2 v0.3 path behind config flag.
    Smoke test only.

P5. Measurement
    Compare v0.2 vector C2, state-token-only, spatial-bank-only,
    hybrid, hybrid+bus-gates.
```

Server execution requires a separate DEC and per-step gate. This addendum does not authorize P0-P5 execution.

## Ablation update

Evidence status: `speculative`.

The ablation plan should gain a future v0.4 memory-specific addendum. Candidate ablations:

Cycle 028 note:

```text
The memory-specific addendum now exists as:
  specs/SPEC-20260508-002-dream3r-memory-v03-ablation-addendum.md

That file is the current ablation map. The table below is retained as
the original candidate sketch.
```

| New candidate | Question | Kill condition |
| --- | --- | --- |
| ABL-v03-C2-1 vector vs token state | Does state-token recurrence improve continuity over GRU vector state? | no improvement on drift/stability but higher latency |
| ABL-v03-C2-2 vector AnchorBank vs spatial bank | Does spatial key/value payload improve retrieval quality? | no retrieval or reconstruction gain |
| ABL-v03-C2-3 spatial bank without C3/C4 gates | Are geometry-aware write gates necessary? | ungated bank matches gated bank under dynamic scenes |
| ABL-v03-C2-4 usage pruning vs LRU | Does future-attention utility beat LRU? | no survival/retrieval advantage |
| ABL-v03-C2-5 NSA gate vs plain attention | Does NSA branch gate add value after payload semantics exist? | no gain over plain attention, or latency too high |
| ABL-v03-C2-6 memory before decoder vs after decoder | Must memory inform reconstruction tokens before prediction? | post-hoc memory matches pre-decoder memory |

Metrics:

- frame-to-frame pointmap stability
- long-sequence drift proxy
- loop/overlap retrieval precision
- memory write redundancy rate
- future-attention survival utility
- dynamic pollution rate
- retrieval entropy calibration
- route_regret under memory uncertainty
- p50/p95 latency on TITAN RTX

## Paper correction

Evidence status: `spec-observed`.

`literature/PAPER_DRAFT_V1.md` v1.3 currently contains cycle 024 demonstration language. That evidence should be bounded:

```text
Allowed:
  component latency measurements
  parameter counts
  adapter availability checks
  vector AnchorBank/NSA plumbing demonstration
  end-to-end untrained pipeline trace

Not allowed:
  memory quality claim
  reconstruction quality claim
  routing quality claim
  validation of C2 v0.3
  validation of pillar A or D
```

The paper should carry a v1.4 note stating that C2 v0.3 supersedes v0.2 Delta 3 as the current memory design, while cycle 024 remains an engineering smoke baseline.

## Risks

### R1 token-state latency

Evidence status: `inferred`.

CUT3R-like state-frame cross-attention may exceed the 30-50 ms streaming budget. Mitigation: start with 32 or 64 state tokens, measure p95 latency, and keep v0.2 vector path as baseline.

### R2 spatial bank staleness

Evidence status: `inferred`.

Spann3R-style memory can become stale in dynamic scenes. Mitigation: C3 dynamic gates, C4 quarantine, working-memory duplicate filter, and utility pruning.

### R3 payload source unresolved

Evidence status: `unknown`.

Values may come from C1 tokens, expert decoder features, pointmap patch embeddings, or C4-verified points. Mitigation: prototype all four with fixed token tensors before server integration.

### R4 NSA terminology hides mechanism

Evidence status: `code-observed` and `inferred`.

Current NSA code works as branch plumbing, but "NSA" alone does not make a 3R memory. Mitigation: define payload schema and read/write semantics first, then optimize.

### R5 cycle 024 evidence overreach

Evidence status: `spec-observed`.

Cycle 024 produced useful engineering smoke evidence, but some paper phrasing could be read as stronger than it is. Mitigation: v1.4 paper correction and this addendum's boundary.

## Open questions

1. Should `latent_tokens` be learned registers, first-frame initialized, or hybrid?
2. What is the starting state-token count: 32, 64, 128, or 324?
3. Should `spatial_bank` have separate static, dynamic, and pose partitions?
4. What is the first value-token source: C1 tokens, expert decoder tokens, pointmap patch embeddings, or verified points?
5. Should v0.3 keep the NSA gate in the first prototype, or start with plain attention and add NSA later?
6. How should C4 quarantine be represented without letting C4 own C2 state?
7. Which minimal dataset or recorded token trace is allowed for P0 without a new checkpoint or training step?

## Recommended next direction

After this addendum, do not jump directly to full server integration.

Recommended order:

```text
1. Paper v1.4 boundary correction and guidance sync.          done in cycle 026
2. Memory-state prototype plan, markdown only.                done in cycle 027
3. Memory-specific ablation addendum and reviewer checklist.  done in cycle 028
4. P0 static tensor prototype, only if separately authorized.
5. C2 v0.3 implementation behind feature flag.
6. Only then consider training or fine-tuning.
```

The research result remains valid only if the project separates:

```text
mechanism design
from runnable scaffold
from empirical validation
from paper claim.
```

## Version history

```text
v0.2  2026-05-06  SPEC-20260506-004 Delta 3. Bounded vector
                  AnchorBank + NSA-style retrieval.

v0.3  2026-05-08  SPEC-20260508-001. This addendum. Delta 3
                  superseded as current C2 Memory design by
                  state-token recurrence + explicit spatial bank
                  + bus-gated writes. Markdown only.
v0.3a 2026-05-08  Cycle 028 pointer. SPEC-20260508-002 now carries
                  the current memory-specific ablation map.
```
