# C2 Memory v0.3 P0 prototype plan

Last updated: 2026-05-08 (cycle 028 pointer added: ablation addendum now exists)

Status: engineering plan, markdown-only.

Parent spec:

```text
specs/SPEC-20260508-001-dream3r-c2-memory-v03-addendum.md
```

Parent decision:

```text
decisions/DEC-20260508-003-cycle-027-memory-p0-prototype-plan.md
```

## Purpose

P0 is a static tensor prototype plan for C2 Memory v0.3. It is meant to answer one narrow question before any server model integration:

```text
Does the v0.3 memory design have a testable interface that can separate
vector cache plumbing from spatial memory behavior and state-token
recurrence behavior?
```

P0 does not test reconstruction quality. It tests memory mechanics on controlled tensors.

## Non-scope

P0 planning does not authorize:

- Python implementation
- server code edit
- model run
- checkpoint use or download
- training or fine-tuning
- paper evidence promotion
- KYKT frontend or navigation change

Any implementation of this plan requires a separate DEC and per-step gate.

## Evidence labels

```text
code-observed:
  CUT3R / Spann3R / Dream3R C2 code read in cycle 025.

spec-observed:
  Existing Dream specs and cycle logs.

engineering plan:
  This document. No execution yet.

engineering-demonstrated:
  Only allowed after a future authorized P0 implementation runs.

speculative:
  Any claim that the v0.3 hybrid will improve 3R memory quality.
```

## P0 comparison matrix

| Variant | Purpose | Minimal mechanism | What it can prove | What it cannot prove |
| --- | --- | --- | --- | --- |
| V0 vector baseline | Keep cycle 024 as baseline | vector AnchorBank + top-k vector read + optional NSA branch gate | whether v0.2 plumbing is reproducible in tensor-only form | spatial recall, reconstruction, long-context memory |
| V1 spatial bank | Isolate Spann3R-style selected branch | query-to-key attention, value aggregation, confidence bias, duplicate skip, utility pruning | whether explicit key/value memory exposes retrieval quality and utility signals | state recurrence, reconstruction quality |
| V2 state tokens | Isolate CUT3R-style compressed branch | latent state tokens + state-frame cross-attention + update/reset masks | whether token state carries more structured continuity than one vector | explicit spatial recall |
| V3 hybrid + bus gates | Test C2 v0.3 interface | V1 + V2 + sliding tokens + conflict/dynamic/permanence write gates | whether bus-gated write policy is observable and falsifiable | final Dream3R performance |

## Tensor fixtures

The prototype should use deterministic tensors, not model outputs, in the first pass.

Default dimensions:

```text
B = 2              batch size
T = 12             windows
P = 64             frame tokens per window
E = 8              evidence tokens per window
D = 128            token dimension
S = 32             latent state tokens
M_max = 256        spatial bank capacity
W = 4              sliding window length
K = 8              selected spatial entries per query
G = 4              synthetic scene groups
```

Dimension rationale:

- `S=32` is the conservative state-token start. It keeps CUT3R-like recurrence small before testing 64/128.
- `P=64` is enough to simulate patch-level structure without large attention cost.
- `M_max=256` matches the v0.2 AnchorBank baseline capacity.
- `W=4` matches the v0.2 sliding branch default.

Required random seeds:

```text
seed_global = 20260508
seed_noise = 20260509
seed_dynamic = 20260510
```

## Synthetic regimes

P0 should generate controlled token sequences with known latent labels. These labels are not model ground truth. They are fixture metadata for memory tests.

### R1 stable loop

```text
Goal:
  test loop recall and duplicate filtering.

Construction:
  windows 0..5 introduce scene groups A, B, C.
  windows 6..11 revisit A, B, C with noise and token permutation.

Expected:
  spatial bank retrieves older matching groups.
  duplicate filter reduces redundant writes on revisit.
```

### R2 monotonic drift

```text
Goal:
  test state-token continuity and vector-state collapse.

Construction:
  frame tokens shift gradually along one latent direction.
  no hard loop closure.

Expected:
  state tokens produce lower continuity error than vector baseline
  at similar capacity, or fail this claim.
```

### R3 dynamic pollution

```text
Goal:
  test bus-gated write suppression.

Construction:
  25 percent of tokens are dynamic distractors.
  dynamic_ratio and suppress_static_write become high in selected windows.

Expected:
  hybrid gate writes fewer dynamic distractors to static memory
  than ungated spatial bank.
```

### R4 conflict quarantine

```text
Goal:
  test Critic-driven quarantine behavior.

Construction:
  conflict_score is high for windows with intentionally corrupted values.

Expected:
  hybrid writes are skipped, quarantined, or confidence-downweighted.
```

### R5 pressure and pruning

```text
Goal:
  test utility pruning vs LRU.

Construction:
  number of candidate memory items exceeds M_max.
  future queries repeatedly need a subset of older entries.

Expected:
  utility pruning keeps future-useful entries more often than LRU.
```

## Fixture tensors

A future implementation should emit the following tensors per run:

```text
frame_tokens:       [B, T, P, D]
evidence_tokens:    [B, T, E, D]
point_tokens:       [B, T, P, D]      optional value proxy
group_id:           [B, T, P]         fixture label, not model label
is_dynamic:         [B, T, P]
is_corrupt:         [B, T, P]
expected_loop_id:   [B, T]            -1 if no loop expected

bus.dynamic_ratio:          [B, T]
bus.suppress_static_write:  [B, T]
bus.conflict_score:         [B, T]
bus.permanence_link:        [B, T, P] or [B, T]
bus.capability_match:       [B, T]
```

The fixture generator should use normalized group prototypes:

```text
prototype[g] in R^D, ||prototype[g]|| = 1
frame_token[t,p] = prototype[group_id[t,p]] + drift[t] + noise
```

Dynamic and corrupt tokens should be traceable by fixture labels so metric failures are explainable.

## Variant interfaces

### V0 vector AnchorBank baseline

Inputs:

```text
summary_t: [B,D]
bank:      [B,M,D]
```

Operations:

```text
1. summarize frame tokens by mean pooling.
2. write summary_t into vector bank.
3. retrieve top-k cosine nearest vectors.
4. optionally fuse compressed, selected, sliding vectors with v0.2 gate.
```

Outputs:

```text
context_t:            [B,D]
selected_ids_t:       [B,K]
bank_occupancy_t:     [B]
retrieval_score_t:    [B,K]
write_action_t:       enum write/skip/evict
```

Expected weakness:

```text
Vector summaries cannot identify which spatial token was dynamic,
corrupt, or loop-useful.
```

### V1 spatial key/value bank

Inputs:

```text
query_tokens_t: [B,P,D]
key_tokens_t:   [B,P,D]
value_tokens_t: [B,P,D]
bus fields      optional confidence bias
```

Operations:

```text
1. normalize query and bank keys.
2. compute query-token to memory-key attention.
3. aggregate memory values.
4. record attention received by each memory item.
5. skip duplicate writes against recent working memory.
6. prune by attn_sum / read_count with young-entry protection.
```

Outputs:

```text
selected_values_t:       [B,P,D]
selected_ids_t:          [B,P,K] or compact top ids
retrieval_entropy_t:     [B]
attn_sum_update_t:       [B,M]
write_action_t:          enum write/skip/evict
memory_utility_t:        [B,M]
```

Expected strength:

```text
Spatial branch exposes retrieval entropy, token-level selected ids,
duplicate writes, and future-use utility.
```

### V2 state-token recurrence

Inputs:

```text
latent_tokens_prev: [B,S,D]
frame_tokens_t:     [B,P,D]
update_mask_t:      [B,1,1]
reset_mask_t:       [B,1,1]
```

Operations:

```text
1. state tokens attend to frame tokens.
2. frame tokens attend to state tokens.
3. apply update mask.
4. apply reset mask.
5. publish latent summary and state-token continuity metrics.
```

Outputs:

```text
latent_tokens_t:       [B,S,D]
frame_context_t:       [B,P,D]
state_delta_t:         [B]
reset_applied_t:       [B]
update_applied_t:      [B]
```

Expected strength:

```text
State tokens should retain structured continuity better than one
pooled vector under R2 monotonic drift.
```

### V3 hybrid plus bus-gated writes

Inputs:

```text
frame_tokens_t
evidence_tokens_t
point_tokens_t
latent_tokens_prev
spatial_bank_prev
working_tokens_prev
bus signals
```

Operations:

```text
1. read spatial bank with V1.
2. update state tokens with V2 using selected values as extra context.
3. fuse compressed, selected, and sliding branches.
4. decide write action from bus signals.
5. write, skip, quarantine, defer, or prune.
```

Outputs:

```text
memory_context_tokens_t:    [B,N,D]
latent_tokens_t:            [B,S,D]
spatial_bank_t:             structured bank state
retrieval_entropy_t:        [B]
dynamic_write_rate_t:       [B]
quarantined_write_count_t:  [B]
bank_occupancy_t:           [B]
retrieval_log_t:            structured log
```

Expected strength:

```text
Hybrid should make memory hygiene decisions observable: fewer dynamic
writes in R3, quarantine in R4, and better future-use retention in R5.
```

## Metrics

All P0 metrics are tensor-mechanism metrics, not 3R quality metrics.

### M1 loop retrieval precision

```text
For windows with expected_loop_id != -1:
  precision = selected_items_matching_expected_group / selected_items
```

Applies to:

- V0 selected vectors, using majority group id of stored summary
- V1/V3 selected spatial tokens

Primary regime: R1.

### M2 duplicate write rate

```text
duplicate_write_rate = duplicate_writes / loop_revisit_windows
```

Lower is better when the revisit is redundant. Too low is bad if it skips genuinely changed evidence.

Primary regime: R1.

### M3 dynamic pollution rate

```text
dynamic_pollution = dynamic_items_written_to_static_bank / total_static_bank_writes
```

Primary regime: R3.

### M4 quarantine accuracy

```text
quarantine_precision = quarantined_corrupt_items / quarantined_items
quarantine_recall = quarantined_corrupt_items / corrupt_items_seen
```

Primary regime: R4.

### M5 future-use survival

```text
future_use_survival = useful_old_entries_kept_after_prune / useful_old_entries_before_prune
```

Primary regime: R5.

### M6 state continuity error

```text
state_continuity_error =
  mean_t || project(latent_tokens_t) - expected_drift_state_t ||_2
```

If no analytic expected drift is used:

```text
state_smoothness = mean_t || summary(latent_tokens_t) - summary(latent_tokens_{t-1}) ||_2
state_responsiveness = corr(summary_delta, true_drift_delta)
```

Primary regime: R2.

### M7 branch entropy

```text
retrieval_entropy = entropy(attention over selected memory entries)
branch_entropy = entropy(compressed/selected/sliding gate weights)
```

Useful for diagnosing whether selected memory is confident or diffuse.

### M8 latency proxy

P0 should not claim measured latency unless implemented. The plan should record operation counts:

```text
vector_topk_cost:       O(MD + M log K)
spatial_attention_cost: O(PMD)
state_attention_cost:   O(SPD + PSD)
hybrid_cost:            spatial + state + fusion + gate
```

Future implementation may measure p50/p95 wall-clock, but this plan does not.

## Success criteria

P0 is successful if a future implementation can produce a table like:

| Metric | V0 vector | V1 spatial | V2 state | V3 hybrid | Interpretation |
| --- | --- | --- | --- | --- | --- |
| M1 loop retrieval precision | value | value | N/A | value | selected branch utility |
| M2 duplicate write rate | value | value | N/A | value | duplicate filtering |
| M3 dynamic pollution | value | value | N/A | value | bus-gated hygiene |
| M4 quarantine precision/recall | N/A | value | N/A | value | Critic gate usefulness |
| M5 future-use survival | value | value | N/A | value | pruning policy |
| M6 state continuity | value | N/A | value | value | state-token value |
| M7 entropy | value | value | value | value | uncertainty signal |
| M8 op proxy / latency | value | value | value | value | feasibility |

The plan itself is successful if it defines all fields needed for that future table.

## Kill conditions

P0 should recommend against immediate C2 v0.3 implementation if any of these happen in future execution:

```text
K1. V1 spatial bank cannot outperform V0 vector bank on R1 loop retrieval.
K2. V3 hybrid does not reduce dynamic pollution relative to V1 on R3.
K3. V3 quarantine does not respond to conflict_score in R4.
K4. V2 state tokens show no continuity/responsiveness advantage over V0
    while carrying materially higher operation cost.
K5. Utility pruning does not preserve future-useful entries better than LRU.
K6. Retrieval and branch entropy do not correlate with fixture uncertainty.
K7. Tensor interface requires cross-module state mutation, violating C2/C3/C4/C5 ownership.
```

If K1 and K4 both fail, v0.3 should not proceed. The project should either:

- keep v0.2 vector memory as engineering baseline, or
- mine another memory mechanism before touching server code.

## Review checklist before execution

A reviewer should answer these before authorizing implementation:

```text
[ ] Does the plan compare v0.2 baseline against each new mechanism separately?
[ ] Are V1 spatial bank and V2 state tokens independently testable?
[ ] Are all bus-gated write decisions observable in logs?
[ ] Are fixture labels separate from model outputs and not used as hidden supervision?
[ ] Are metric formulas defined before any results exist?
[ ] Are kill conditions explicit enough to stop v0.3 implementation?
[ ] Does the plan avoid checkpoint use, model run, and training?
[ ] Does future execution require a separate DEC and per-step gate?
```

## Future execution gate

If the user later authorizes P0 implementation, the agent must create a new DEC before writing code.

Minimum future DEC fields:

```text
decision_id: DEC-YYYYMMDD-NNN
scope: implement P0 static tensor prototype only
allowed paths:
  likely planning or experiments prototype path, not server model path
not allowed:
  checkpoint download
  model import from CUT3R / Spann3R / Dream3R server code
  training
  paper evidence promotion
required outputs:
  script or notebook
  JSON/CSV metric table
  cycle log
  updated evidence boundary
```

Recommended future implementation path:

```text
Dream/experiments/prototypes/memory_v03_p0/
```

Do not place P0 directly into `/hdd3/kykt26/code/dream3r/dream3r/` unless the user explicitly authorizes server integration.

## Next after P0 plan

After this markdown plan, the next non-execution step was closed by
cycle 028:

```text
Memory-specific ablation addendum:
  specs/SPEC-20260508-002-dream3r-memory-v03-ablation-addendum.md
```

The next execution step, if authorized later, is:

```text
Implement P0 as a static tensor prototype.
```

No evidence label should advance beyond `engineering plan` until that execution happens.

## Version history

```text
v1  2026-05-08  cycle 027. Markdown-only P0 prototype plan for C2
                Memory v0.3. No execution authorized.
v1.1 2026-05-08 cycle 028 pointer. Memory-specific ablation addendum
                now exists as SPEC-20260508-002.
```
