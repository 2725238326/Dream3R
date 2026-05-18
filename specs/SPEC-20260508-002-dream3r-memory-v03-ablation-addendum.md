# Dream3R C2 Memory v0.3 ablation addendum

spec_id: SPEC-20260508-002

spec_kind: memory-specific ablation addendum

parent_spec: SPEC-20260508-001 (C2 Memory v0.3 addendum)

parent_plan: planning/MEMORY_V03_P0_PROTOTYPE_PLAN.md

parent_decision: DEC-20260508-004

date: 2026-05-08

cycle: 028

status: engineering plan, markdown-only

review_status: cycle 029 reviewed; surgical corrections applied

honesty_label: every ablation below is a plan, not a result.

linked_artifacts:
- specs/SPEC-20260508-001-dream3r-c2-memory-v03-addendum.md
- planning/MEMORY_V03_DESIGN_STUDY.md
- planning/MEMORY_V03_P0_PROTOTYPE_PLAN.md
- decisions/DEC-20260508-004-cycle-028-memory-ablation-addendum.md
- decisions/DEC-20260508-005-cycle-029-memory-ablation-review.md
- planning/MEMORY_V03_ABLATION_REVIEW.md
- specs/SPEC-20260506-005-dream3r-ablation-plan-v02.md
- specs/SPEC-20260507-002-dream3r-ablation-plan-v03-addendum.md

## Purpose

This addendum converts the C2 Memory v0.3 P0 plan into a falsifiable
ablation map.

The central question is:

```text
Which part of C2 Memory v0.3 is load-bearing:
  spatial key/value memory,
  state-token recurrence,
  bus-gated writes,
  utility pruning,
  branch uncertainty,
  or a later decoder-coupling choice?
```

This document does not authorize execution. It defines what a future
authorized implementation must measure and what outcomes would stop or
redirect C2 Memory v0.3.

## Non-scope

This addendum does not authorize:

- Python prototype
- server code edit
- model run
- checkpoint use or download
- training or fine-tuning
- paper evidence promotion
- KYKT frontend or navigation change

Any execution of an `ABL-memory-*` test requires a separate DEC and
per-step gate.

## Evidence labels

```text
code-observed:
  CUT3R / Spann3R / Dream3R C2 code read in cycle 025.

spec-observed:
  Existing Dream specs, cycle logs, and P0 plan.

engineering plan:
  This document. No execution yet.

engineering-demonstrated:
  Only allowed after a future authorized ablation implementation runs.

speculative:
  Any claim that a C2 Memory v0.3 mechanism improves 3R quality.
```

## Requirements summary

The ablation addendum must preserve five requirements.

1. Every C2 Memory v0.3 claim must have a matching ablation.
2. P0 tensor tests must be separated from later module, integration, and
   model-quality tests.
3. Vector AnchorBank from cycle 024 must remain a baseline, not a research
   validation claim.
4. ABL results must be interpretable even if the future P0 prototype fails.
5. Kill conditions must be strong enough to stop v0.3 before server model
   integration.

## Cycle 029 review corrections

Cycle 029 reviewed this addendum and applied four planning corrections:

1. P0 may use fixture-derived bus fields as oracle inputs, but variants
   must not read raw fixture labels such as `group_id`, `is_dynamic`, or
   `is_corrupt`.
2. State-token recurrence must not pass on smoothness alone. It must show
   continuity with drift responsiveness, or explicitly fail as stale-smooth.
3. P0 operation proxy cannot validate the streaming envelope. It can only
   decompose cost and name feasible fallbacks before a later module
   benchmark.
4. Tier 1 hard-fail and soft-fail rules must be explicit before any future
   execution.

## Oracle-bus boundary

P0 is allowed to synthesize bus fields from fixture metadata:

```text
bus.dynamic_ratio
bus.suppress_static_write
bus.conflict_score
bus.permanence_link
bus.capability_match
```

These fields are oracle controls in P0. They are allowed only because P0
tests whether the C2 write/read interface responds correctly to bus
signals.

Forbidden in P0:

```text
V0/V1/V2/V3 must not read group_id, is_dynamic, is_corrupt,
expected_loop_id, or future-use labels directly.
```

Required logging:

```text
Each bus field must be tagged as oracle_bus in P0 outputs.
Future non-oracle producers must be tested separately before any paper
claim or server integration.
```

## Claim map

| Claim id | C2 Memory v0.3 claim | Evidence before execution | Primary ablation | Failure implication |
| --- | --- | --- | --- | --- |
| C2M-C1 | Spatial key/value memory is more informative than vector summaries for controlled loop/revisit retrieval; overlap retrieval remains future-gated until an overlap fixture or recorded trace exists | speculative, grounded in Spann3R code-observed | ABL-memory-1 | Do not replace vector AnchorBank with spatial bank yet |
| C2M-C2 | Duplicate filtering is necessary for stable revisits | speculative | ABL-memory-2 | Keep simple write policy or redesign duplicate rule |
| C2M-C3 | State-token recurrence carries smoother temporal continuity than a single vector state | speculative, grounded in CUT3R code-observed | ABL-memory-3 | Do not add state-token recurrence to C2 |
| C2M-C4 | Bus-gated writes reduce dynamic pollution in static memory | speculative | ABL-memory-4 | Keep C3/C4 signals out of C2 write path until redesigned |
| C2M-C5 | Conflict quarantine is observable and useful | speculative | ABL-memory-5 | Do not claim Critic-gated memory hygiene |
| C2M-C6 | Utility pruning preserves future-useful entries better than LRU | speculative, grounded in Spann3R code-observed | ABL-memory-6 | Keep LRU or age-based policy |
| C2M-C7 | Branch entropy is useful as uncertainty for Composer and Critic | speculative | ABL-memory-7 | Do not route on memory entropy |
| C2M-C8 | Hybrid V3 cost can be decomposed and a feasible fallback can be named before streaming latency is claimed | inferred | ABL-memory-8 | Keep only cheaper sub-mechanisms |
| C2M-C9 | Value payload source matters and must be selected before server integration | unknown | ABL-memory-9 | Delay P1/P3 implementation until payload source is resolved |
| C2M-C10 | Memory context should inform reconstruction before prediction, not only after prediction | speculative | ABL-memory-10 | Treat C2 as logging or routing support, not reconstruction core |
| C2M-C11 | NSA-style branch gating adds value only after payload semantics exist | speculative | ABL-memory-11 | Drop NSA from C2 memory story |

## Tiering

```text
Tier 0: fixture and logging validity
  ABL-memory-0

Tier 1: P0 load-bearing tensor tests
  ABL-memory-1
  ABL-memory-3
  ABL-memory-4
  ABL-memory-5
  ABL-memory-6

Tier 2: P0 diagnostic tensor tests
  ABL-memory-2
  ABL-memory-7
  ABL-memory-8

Tier 3: future module or integration tests
  ABL-memory-9
  ABL-memory-10
  ABL-memory-11
```

If any Tier 1 test fails strongly, C2 v0.3 should not proceed to server
model integration without a redesign note.

## Tier 1 decision rule

Use these labels after future P0 execution:

```text
hard_fail:
  primary metric fails the stated condition, logs are valid, and no
  documented fixture bug explains the result.

soft_fail:
  primary metric is inconclusive, denominator is weak, or the variant
  exposes an interface issue that may be repairable without changing the
  research claim.

invalid:
  ABL-memory-0 or fixture/logging validity fails; no architecture
  conclusion may be drawn.
```

Decision rule:

```text
Any Tier 1 hard_fail requires a redesign note before server integration.
ABL-memory-1 hard_fail + ABL-memory-3 hard_fail stops C2 v0.3 as the
current Memory-core direction until a new memory mechanism is proposed.
```

## P0 variant mapping

| Variant | Role in ablations | Must be implemented before claim use |
| --- | --- | --- |
| V0 vector AnchorBank | baseline for C2M-C1, C2M-C3, C2M-C8 | yes, P0 |
| V1 spatial bank | isolates C2M-C1, C2M-C2, C2M-C6 | yes, P0 |
| V2 state tokens | isolates C2M-C3 | yes, P0 |
| V3 hybrid + bus gates | tests C2M-C4, C2M-C5, C2M-C7, C2M-C8 | yes, P0 |

## ABL-memory-0: Fixture and logging validity

```text
ablation_id:     ABL-memory-0
tier:            0
stage:           P0 tensor-only
claim:           measurement validity, not architecture value
primary_regimes: all R1-R5
primary_metrics: all fixture sanity checks
evidence_label:  engineering plan
```

Question:

```text
Are fixture labels, tensor shapes, random seeds, write logs, selected ids,
and metric denominators deterministic and inspectable?
```

Required checks:

- all tensors match the P0 plan dimensions
- all random seeds reproduce identical fixture labels
- `group_id`, `is_dynamic`, and `is_corrupt` are never used as hidden model inputs
- every write action records source variant, regime, item id, gate reason, and eviction reason
- every metric has a non-zero denominator or emits an explicit `not_applicable`

Fail condition:

```text
Any core metric can change without a fixture or variant change.
```

If this fails, no later ABL-memory result is admissible.

## ABL-memory-1: Vector AnchorBank vs spatial bank retrieval

```text
ablation_id:     ABL-memory-1
tier:            1
stage:           P0 tensor-only
claim:           C2M-C1
primary_regime:  R1 stable loop
primary_metric:  M1 loop retrieval precision
secondary:       M7 retrieval entropy
variants:        V0 vs V1 vs V3
kill_link:       K1
```

Question:

```text
Does explicit spatial key/value retrieval beat vector summaries on loop
and overlap recall under controlled revisits?
```

Expected interpretation:

- Pass: V1 and/or V3 exceed V0 on M1 with lower or more meaningful entropy.
- Weak pass: V1 improves token-level selection but V3 adds no value.
- Fail: V1 cannot beat V0 on R1.

Hard stop:

```text
If V1 does not beat V0 on R1, do not proceed to a full C2 v0.3
implementation. Keep vector AnchorBank as baseline or redesign spatial
key construction.
```

## ABL-memory-2: Duplicate filtering under loop revisit

```text
ablation_id:     ABL-memory-2
tier:            2
stage:           P0 tensor-only
claim:           C2M-C2
primary_regime:  R1 stable loop
primary_metric:  M2 duplicate write rate
variants:        V1 with duplicate filter vs V1 without duplicate filter;
                 V3 with duplicate filter vs V3 without duplicate filter
```

Question:

```text
Does duplicate filtering reduce redundant writes without suppressing
genuinely changed evidence?
```

Acceptance criteria:

- duplicate write rate drops on pure revisits
- writes are still allowed when fixture drift or corruption label changes
- skip reasons are recorded as explicit write actions

Fail condition:

```text
The filter either writes nearly everything or suppresses changed evidence.
```

## ABL-memory-3: State-token recurrence vs vector state

```text
ablation_id:     ABL-memory-3
tier:            1
stage:           P0 tensor-only
claim:           C2M-C3
primary_regime:  R2 monotonic drift
primary_metric:  M6 state continuity error
secondary:       M8 op proxy
variants:        V0 vs V2 vs V3
kill_link:       K4
```

Question:

```text
Do state tokens provide a measurable continuity or responsiveness
advantage over vector state under monotonic drift?
```

Expected interpretation:

- Pass: V2 or V3 improves continuity and drift responsiveness at acceptable op cost.
- Weak pass: V2 improves continuity but V3 coupling adds cost or instability.
- Fail: V2 shows no advantage over V0 while increasing op count materially,
  or produces smooth but stale state that does not track drift.

Hard stop:

```text
If ABL-memory-1 and ABL-memory-3 both fail, C2 v0.3 should not proceed.
```

## ABL-memory-4: Bus-gated dynamic write suppression

```text
ablation_id:     ABL-memory-4
tier:            1
stage:           P0 tensor-only
claim:           C2M-C4
primary_regime:  R3 dynamic pollution
primary_metric:  M3 dynamic pollution rate
variants:        V1 ungated vs V3 gated
kill_link:       K2
```

Question:

```text
Do C3/C6 dynamic signals reduce dynamic distractor writes into static
memory?
```

Acceptance criteria:

- V3 has lower dynamic pollution than V1.
- `suppress_static_write` and `dynamic_ratio` are visible in the write log.
- static useful entries are not reduced enough to damage R1 retrieval.

Fail condition:

```text
Ungated V1 matches gated V3 on dynamic pollution, or V3 drops useful
static memory to avoid dynamic writes.
```

## ABL-memory-5: Conflict quarantine

```text
ablation_id:     ABL-memory-5
tier:            1
stage:           P0 tensor-only
claim:           C2M-C5
primary_regime:  R4 conflict quarantine
primary_metric:  M4 quarantine precision and recall
variants:        V1 no quarantine vs V3 quarantine
kill_link:       K3
```

Question:

```text
Can Critic-style conflict signals produce observable quarantine behavior
without letting C4 own C2 state?
```

Acceptance criteria:

- corrupted items are skipped, quarantined, or confidence-downweighted
- clean items under low conflict are still writeable
- quarantine action includes source item id and reason
- C4 signal is read-only through the bus

Fail condition:

```text
V3 quarantine does not respond to conflict_score, or the design requires
C4 to mutate C2 memory state.
```

## ABL-memory-6: Utility pruning vs LRU

```text
ablation_id:     ABL-memory-6
tier:            1
stage:           P0 tensor-only
claim:           C2M-C6
primary_regime:  R5 pressure and pruning
primary_metric:  M5 future-use survival
variants:        V1 utility pruning vs V1 LRU;
                 V3 utility pruning vs V3 LRU
kill_link:       K5
```

Question:

```text
Does usage-aware utility pruning preserve future-useful memory better
than LRU under capacity pressure?
```

Acceptance criteria:

- future-use survival improves over LRU
- young-entry protection prevents immediate deletion of new useful entries
- permanent or high-confidence items are protected only when justified by
  future use

Fail condition:

```text
Utility pruning has no survival or retrieval advantage over LRU.
```

## ABL-memory-7: Entropy as uncertainty signal

```text
ablation_id:     ABL-memory-7
tier:            2
stage:           P0 tensor-only
claim:           C2M-C7
primary_regime:  all R1-R5
primary_metric:  M7 retrieval entropy and branch entropy
variants:        V0, V1, V2, V3
kill_link:       K6
```

Question:

```text
Do retrieval entropy and branch entropy track fixture uncertainty well
enough to publish as bus signals for C4/C5?
```

Acceptance criteria:

- entropy rises under conflict, corruption, or ambiguous retrieval
- entropy falls under stable loop retrieval
- entropy is not just a constant or capacity artifact

Fail condition:

```text
Entropy does not correlate with fixture uncertainty or changes only with
memory size.
```

If this fails, C2 may still use memory internally, but should not expose
entropy as a routing or Critic signal.

## ABL-memory-8: Operation proxy and latency envelope

```text
ablation_id:     ABL-memory-8
tier:            2
stage:           P0 tensor-only, later module benchmark
claim:           C2M-C8
primary_metric:  M8 op proxy
variants:        V0, V1, V2, V3
```

Question:

```text
Can the V3 hybrid cost be decomposed well enough to name a feasible
fallback before any streaming latency claim is made?
```

P0 records operation counts only:

```text
V0: O(B * M * D) vector top-k style proxy
V1: O(B * P * M * D) spatial selected read proxy
V2: O(B * S * P * D) state-frame attention proxy
V3: V1 + V2 + gate/write bookkeeping
```

Acceptance criteria:

- V3 cost is decomposed by component
- a cheaper fallback is named if V3 is too expensive
- no latency or streaming-envelope claim is made before actual implementation

Fail condition:

```text
V3 cost is dominated by an unbounded P*M or S*P term with no pruning,
chunking, or fallback.
```

## ABL-memory-9: Value payload source selection

```text
ablation_id:     ABL-memory-9
tier:            3
stage:           future P1/P3 module test
claim:           C2M-C9
primary_regime:  recorded token trace or authorized model trace
primary_metric:  retrieval usefulness and payload inspectability
variants:        C1 token values vs point-token values vs expert decoder
                 values vs verified-point values
```

Question:

```text
What should the spatial bank store as value payload before server model
integration?
```

Why this is not P0:

- P0 uses synthetic tokens and can only prove interface separability.
- Payload source quality depends on real model tensors or recorded traces.

Execution gate:

```text
Requires a separate DEC because it may need recorded model traces or
server-side tensor extraction.
```

Fail condition:

```text
No payload source is inspectable enough to support memory-context tokens.
```

## ABL-memory-10: Memory before decoder vs after decoder

```text
ablation_id:     ABL-memory-10
tier:            3
stage:           future integration test
claim:           C2M-C10
primary_metric:  reconstruction or pointmap stability, not P0 metric
variants:        memory-context before reconstruction prediction vs
                 post-hoc memory summary after prediction
```

Question:

```text
Must memory context inform reconstruction tokens before pointmap
prediction?
```

This is the first ablation that can speak to reconstruction quality.
It is intentionally excluded from P0.

Fail condition:

```text
Post-hoc memory summary matches pre-decoder memory on reconstruction
quality and stability.
```

If this fails, C2 Memory may remain useful for logging, routing, or
Critic support, but not as the paper's reconstruction-memory mechanism.

## ABL-memory-11: NSA gate value after payload semantics

```text
ablation_id:     ABL-memory-11
tier:            3
stage:           future P3/P4 integration test
claim:           C2M-C11
primary_metric:  retrieval quality, branch entropy, op cost
variants:        plain spatial attention vs NSA-style selected branch
```

Question:

```text
Does NSA-style branch gating add algorithmic value after spatial payload
semantics are fixed?
```

Rule:

```text
Do not run or prioritize this before ABL-memory-1 and ABL-memory-9.
NSA terminology must not hide the actual memory payload question.
```

Fail condition:

```text
NSA gate adds no retrieval gain, no uncertainty value, or too much cost.
```

## Acceptance criteria

This addendum is complete if it defines:

- one ablation for each C2M claim
- P0-only tests separated from future module and integration tests
- kill links back to K1-K7 where applicable
- a clear no-go rule before server model integration
- evidence labels for every test stage
- review checklist before execution

Future P0 execution is successful only if it can fill this table:

| ABL | Stage | Required output | Go/no-go |
| --- | --- | --- | --- |
| ABL-memory-0 | P0 | fixture sanity report | all later ABLs admissible or blocked |
| ABL-memory-1 | P0 | V0/V1/V3 M1 table | spatial bank go/no-go |
| ABL-memory-2 | P0 | duplicate write table | duplicate rule go/no-go |
| ABL-memory-3 | P0 | V0/V2/V3 M6 table | state-token go/no-go |
| ABL-memory-4 | P0 | dynamic pollution table | bus dynamic gate go/no-go |
| ABL-memory-5 | P0 | quarantine precision/recall | conflict gate go/no-go |
| ABL-memory-6 | P0 | utility vs LRU table | pruning go/no-go |
| ABL-memory-7 | P0 | entropy correlation table | C4/C5 entropy signal go/no-go |
| ABL-memory-8 | P0 | op proxy table | hybrid cost go/no-go |
| ABL-memory-9 | future | payload source comparison | module integration go/no-go |
| ABL-memory-10 | future | reconstruction comparison | paper mechanism go/no-go |
| ABL-memory-11 | future | NSA vs plain attention comparison | NSA retention go/no-go |

## Implementation steps for a future authorized executor

These steps are planning only.

1. Open a separate DEC for P0 execution.
2. Implement only ABL-memory-0..8 in a non-server-model prototype path.
3. Emit deterministic fixture metadata and write logs.
4. Emit one metrics table per ABL plus a summary go/no-go table.
5. Update the evidence boundary without promoting paper claims.
6. If Tier 1 passes, open a separate DEC for ABL-memory-9 payload-source
   work.
7. Only after ABL-memory-9 should the project consider ABL-memory-10 or
   ABL-memory-11.

Recommended execution path, if later authorized:

```text
Dream/experiments/prototypes/memory_v03_p0/
```

Do not place the prototype directly into:

```text
/hdd3/kykt26/code/dream3r/dream3r/
```

unless the user explicitly authorizes server integration.

## Risks and mitigations

| Risk | Why it matters | Mitigation |
| --- | --- | --- |
| P0 overfits synthetic fixtures | A clean tensor result may not transfer to real 3R | Treat P0 as interface evidence only |
| V3 wins by cheating through labels | Hidden use of fixture labels would invalidate metrics | ABL-memory-0 forbids fixture labels as model inputs |
| State tokens improve smoothness but lag drift | Smoothness alone may hide stale memory | Require responsiveness or drift correlation |
| Bus gates suppress too much useful memory | Dynamic hygiene could damage retrieval | Check R1 retrieval after R3 gating |
| NSA distracts from payload semantics | Old v0.2 vocabulary could hide the real issue | Delay ABL-memory-11 until payload source is fixed |
| Paper claims advance too early | Research story becomes invalid | Keep evidence at `engineering plan` until execution |

## Review checklist before execution

```text
[ ] Does every C2M claim have one primary ablation?
[ ] Are ABL-memory-0..8 P0-only and checkpoint-free?
[ ] Are ABL-memory-9..11 explicitly future gated?
[ ] Is V0 retained as baseline rather than dismissed?
[ ] Does each Tier 1 ablation have a stop or redesign condition?
[ ] Are fixture labels excluded from variant inputs?
[ ] Are write logs required for every gate and eviction decision?
[ ] Is any reconstruction-quality claim excluded from P0?
[ ] Does execution require a separate DEC and per-step gate?
```

## Decision rule

After future P0 execution:

```text
Proceed to module implementation only if:
  ABL-memory-0 passes,
  at least one of ABL-memory-1 or ABL-memory-3 passes strongly,
  ABL-memory-4 and ABL-memory-5 do not fail strongly,
  ABL-memory-8 names a feasible cost path.

Stop or redesign if:
  ABL-memory-1 and ABL-memory-3 both fail,
  or bus-gated writes are not observable,
  or the tensor interface violates C2/C3/C4/C5 ownership.
```

## Version history

```text
v1  2026-05-08  cycle 028. Memory-specific ablation addendum
                mapping P0 variants V0-V3 to ABL-memory-* tests.
                Markdown-only. No execution authorized.
v1.1 2026-05-08 cycle 029 review corrections. Added oracle-bus
                boundary, hard/soft fail rule, narrowed C2M-C1 and
                C2M-C8, and strengthened ABL-memory-3.
```
