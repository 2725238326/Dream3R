# Memory v0.3 P0 execution DEC template

Last updated: 2026-05-08

Status: template only. Not an active execution decision.

Decision:

```text
decisions/DEC-20260508-006-cycle-030-p0-execution-dec-template.md
```

## Purpose

This file is a future authorization packet for the C2 Memory v0.3 P0
static tensor prototype. It is designed so a later user decision can
authorize or reject execution with exact scope.

This file does not authorize implementation by itself.

## Parent chain

```text
planning/MEMORY_V03_DESIGN_STUDY.md
specs/SPEC-20260508-001-dream3r-c2-memory-v03-addendum.md
planning/MEMORY_V03_P0_PROTOTYPE_PLAN.md
specs/SPEC-20260508-002-dream3r-memory-v03-ablation-addendum.md
planning/MEMORY_V03_ABLATION_REVIEW.md
```

## Future decision block

Copy this block into a new DEC only if the user explicitly authorizes
execution in the active conversation.

```text
decision_id:      DEC-YYYYMMDD-NNN
date:             YYYY-MM-DD
cycle:            NNN
status:           proposed | accepted | rejected
authorized_by:    user YYYY-MM-DD: "<exact active authorization>"
decision_type:    P0 static tensor prototype execution
execution_scope:  implement local static tensor prototype for
                  ABL-memory-0..8 only

allowed_paths:
  Dream/experiments/prototypes/memory_v03_p0/
  Dream/cycles/
  Dream/registry/
  Dream/planning/

forbidden_paths:
  /hdd3/kykt26/code/dream3r/dream3r/
  Dream/code/
  any server model runtime path
  any checkpoint directory

allowed_actions:
  create local prototype files under the allowed prototype path
  generate deterministic tensor fixtures
  implement V0 vector AnchorBank baseline
  implement V1 spatial key/value bank
  implement V2 state-token recurrence
  implement V3 hybrid plus bus-gated writes
  emit JSON, JSONL, CSV, and Markdown metric artifacts
  update cycle log and evidence boundary

not_allowed:
  checkpoint download or use
  importing CUT3R, Spann3R, Dream3R, or server model code
  training or fine-tuning
  real model inference
  server integration
  paper evidence promotion
  frontend or navigation work
  ABL-memory-9, ABL-memory-10, or ABL-memory-11 execution
```

## Execution boundary

Future execution, if authorized, is P0 tensor-only:

- deterministic fixture tensors only
- no model outputs
- no checkpoint
- no training
- no server code
- no reconstruction-quality claim
- no paper mechanism claim

The execution scope is limited to:

```text
ABL-memory-0
ABL-memory-1
ABL-memory-2
ABL-memory-3
ABL-memory-4
ABL-memory-5
ABL-memory-6
ABL-memory-7
ABL-memory-8
```

Explicitly excluded:

```text
ABL-memory-9: value payload source selection
ABL-memory-10: memory before decoder vs after decoder
ABL-memory-11: NSA gate value after payload semantics
```

## Oracle-bus boundary

P0 may synthesize bus fields from fixture metadata, but those fields are
oracle controls and must be tagged as `oracle_bus` in every output.

Allowed oracle bus fields:

```text
dynamic_ratio
conflict_score
permanence_score
expected_future_use
reset_mask
```

Forbidden as variant inputs:

```text
raw group_id
raw is_dynamic
raw is_corrupt
expected_loop_id
future-use labels not represented through the oracle bus contract
```

Future non-oracle producers must be tested separately before server
integration or paper claims.

## Required output files

Future execution must emit at least:

```text
Dream/experiments/prototypes/memory_v03_p0/fixtures_manifest.json
Dream/experiments/prototypes/memory_v03_p0/write_log.jsonl
Dream/experiments/prototypes/memory_v03_p0/metrics_abl_memory_0_8.csv
Dream/experiments/prototypes/memory_v03_p0/summary_go_no_go.md
Dream/experiments/prototypes/memory_v03_p0/evidence_boundary_update.md
Dream/cycles/CYCLE-YYYYMMDD-NNN.md
```

Optional supporting outputs:

```text
Dream/experiments/prototypes/memory_v03_p0/metrics_by_seed.json
Dream/experiments/prototypes/memory_v03_p0/abl_memory_0_8_report.md
```

## Required ablation outputs

| ABL | Stage | Required output | Go/no-go focus |
| --- | --- | --- | --- |
| ABL-memory-0 | P0 | fixture sanity report | later ABLs admissible or invalid |
| ABL-memory-1 | P0 | V0/V1/V3 M1 table | spatial bank go/no-go |
| ABL-memory-2 | P0 | duplicate write table | duplicate rule go/no-go |
| ABL-memory-3 | P0 | V0/V2/V3 M6 and M8 table | state-token go/no-go |
| ABL-memory-4 | P0 | dynamic pollution table | bus dynamic gate go/no-go |
| ABL-memory-5 | P0 | quarantine precision/recall | conflict gate go/no-go |
| ABL-memory-6 | P0 | utility vs LRU table | pruning go/no-go |
| ABL-memory-7 | P0 | entropy correlation table | C4/C5 entropy signal go/no-go |
| ABL-memory-8 | P0 | op proxy table | hybrid cost decomposition go/no-go |

## Stop gates

Future execution should use these gates unless a later DEC explicitly
changes them.

```text
G0 authorization:
  User explicitly approves the execution DEC in the active conversation.

G1 path setup:
  Create or confirm only the local prototype path.
  Stop if implementation would touch server or model paths.

G2 fixture implementation:
  Generate deterministic fixtures and fixtures_manifest.json.
  Stop if ABL-memory-0 validity cannot be checked.

G3 variant implementation:
  Implement V0, V1, V2, and V3 in local prototype code only.
  Stop if a variant needs raw fixture labels as hidden inputs.

G4 metrics:
  Emit ABL-memory-0..8 metric tables and write logs.
  Stop if write gates or evictions are not observable.

G5 summary:
  Write summary_go_no_go.md and evidence_boundary_update.md.
  Stop if the summary would promote paper claims or reconstruction
  quality.
```

## Result labels

Use these labels after future P0 execution:

```text
pass:
  metric condition is met, logs are valid, and no boundary violation is
  observed.

hard_fail:
  primary metric fails the stated condition, logs are valid, and no
  documented fixture bug explains the result.

soft_fail:
  primary metric is inconclusive, denominator is weak, or the variant
  exposes a repairable interface issue.

invalid:
  ABL-memory-0 or fixture/logging validity fails; no architecture
  conclusion may be drawn.
```

## Decision rules

Future P0 execution is admissible only if `ABL-memory-0` passes.

Proceed toward module planning only if:

```text
ABL-memory-0 passes,
at least one of ABL-memory-1 or ABL-memory-3 passes strongly,
ABL-memory-4 and ABL-memory-5 do not hard_fail,
ABL-memory-8 names a feasible cost path.
```

Stop or redesign if:

```text
ABL-memory-0 is invalid,
any Tier 1 hard_fail lacks a redesign note,
ABL-memory-1 and ABL-memory-3 both hard_fail,
bus-gated writes are not observable,
the tensor interface violates C2/C3/C4/C5 ownership,
or any variant needs forbidden raw fixture labels as inputs.
```

If `ABL-memory-1` and `ABL-memory-3` both hard_fail, C2 Memory v0.3
must stop as the current Memory-core direction until a new memory
mechanism is proposed.

## Evidence boundary after execution

If future P0 execution succeeds, the strongest allowed claim is:

```text
engineering-demonstrated:
  The local tensor mechanics for Memory v0.3 ABL-memory-0..8 produced
  valid fixture logs and metric tables under synthetic P0 conditions.
```

Still not allowed:

```text
validated 3R reconstruction quality
validated spatial retrieval quality on real scenes
validated state-token recurrence quality on real model traces
validated streaming latency
paper mechanism claim
teacher-demo readiness
server integration readiness
```

## Pre-activation checklist

Before turning this template into an active DEC, confirm:

```text
[ ] User gave explicit active-conversation execution authorization.
[ ] The DEC names only ABL-memory-0..8.
[ ] ABL-memory-9..11 remain excluded.
[ ] The implementation path is local and non-server.
[ ] No checkpoint, model run, training, or server import is needed.
[ ] Oracle bus fields are tagged in outputs.
[ ] Raw fixture labels are forbidden as variant inputs.
[ ] Required output files are named.
[ ] Stop gates G0-G5 are preserved or explicitly revised.
[ ] Evidence labels do not exceed P0 tensor-mechanics evidence.
```

## Future user decision options

```text
A. Approve P0 local static tensor prototype for ABL-memory-0..8.
B. Revise this template before execution.
C. Do not execute; return to research design.
```

## Version history

```text
v1  2026-05-08  cycle 030. Future P0 execution DEC template only.
                No implementation authorized.
```
