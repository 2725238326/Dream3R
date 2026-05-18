# Memory v0.3 ablation addendum review

Last updated: 2026-05-08

Status: review complete, corrections applied.

Review target:

```text
specs/SPEC-20260508-002-dream3r-memory-v03-ablation-addendum.md
```

Decision:

```text
decisions/DEC-20260508-005-cycle-029-memory-ablation-review.md
```

## Verdict

```text
APPROVED FOR PLANNING USE, WITH CYCLE 029 CORRECTIONS APPLIED.
NOT APPROVED FOR EXECUTION.
```

The addendum is good enough to govern a future P0 execution DEC after
the corrections below. It preserves the key research boundary: C2 Memory
v0.3 remains an engineering plan, not a validated mechanism.

## Review scope

This review checked:

- claim coverage
- Tier 1 stop conditions
- P0 tensor-only versus future module/integration separation
- oracle-bus and fixture-label boundaries
- execution gates
- paper evidence boundaries

This review did not run code, models, training, checkpoints, or server
experiments.

## Findings and disposition

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| R-029-1 | high | `ABL-memory-0` forbids fixture labels as hidden model inputs, but P0 variants also read synthetic bus fields such as `dynamic_ratio` and `conflict_score`. Without an oracle-bus rule, a future executor could accidentally let labels leak into the mechanism. | Fixed in SPEC-20260508-002 by adding an oracle-bus boundary section. |
| R-029-2 | medium | `ABL-memory-3` allowed "continuity or responsiveness" as a pass. Smoothness alone can hide stale state. | Fixed by requiring continuity plus drift responsiveness, or an explicit stale-smooth fail. |
| R-029-3 | medium | `C2M-C8` and `ABL-memory-8` used streaming-envelope language, but P0 records op proxy only. | Fixed by narrowing the claim to cost decomposition and fallback selection until module benchmark. |
| R-029-4 | medium | The phrase "fails strongly" was useful but undefined. | Fixed by adding hard-fail and soft-fail decision rules before Tier 1 interpretation. |
| R-029-5 | low | `C2M-C1` mentioned loop and overlap retrieval, while P0 fixtures currently prove only controlled revisit/loop retrieval. | Fixed by narrowing the P0 claim and reserving overlap for a later fixture or recorded trace. |

## Claim coverage assessment

The post-correction map covers all current C2 Memory v0.3 planning claims:

```text
C2M-C1 -> ABL-memory-1
C2M-C2 -> ABL-memory-2
C2M-C3 -> ABL-memory-3
C2M-C4 -> ABL-memory-4
C2M-C5 -> ABL-memory-5
C2M-C6 -> ABL-memory-6
C2M-C7 -> ABL-memory-7
C2M-C8 -> ABL-memory-8
C2M-C9 -> ABL-memory-9
C2M-C10 -> ABL-memory-10
C2M-C11 -> ABL-memory-11
```

No claim is currently unmapped.

## Tier 1 stop-condition assessment

Tier 1 is appropriate:

```text
ABL-memory-1: spatial retrieval
ABL-memory-3: state-token continuity
ABL-memory-4: dynamic write suppression
ABL-memory-5: conflict quarantine
ABL-memory-6: utility pruning
```

The important global stop rule is retained:

```text
If ABL-memory-1 and ABL-memory-3 both hard-fail, C2 v0.3 should stop
before server model integration.
```

Cycle 029 adds the missing hard/soft fail definitions so this rule is
not left to interpretation.

## Stage-separation assessment

Stage separation is sound after correction:

- `ABL-memory-0..8` remain P0 tensor-only and checkpoint-free.
- `ABL-memory-9` is future-gated because payload source quality needs
  recorded or real model tensors.
- `ABL-memory-10` is future-gated because reconstruction quality is not
  measurable in P0.
- `ABL-memory-11` is future-gated because NSA should be evaluated only
  after payload semantics are fixed.

## Execution-gate assessment

The addendum correctly requires a separate DEC before any execution.

Future execution should be limited to:

```text
Dream/experiments/prototypes/memory_v03_p0/
```

until the user explicitly authorizes server integration.

## Remaining risks

1. P0 can still overfit synthetic fixture structure. This is acceptable
   only if the result stays labeled `engineering-demonstrated` for
   tensor mechanics, not for reconstruction quality.
2. Payload-source selection remains unresolved until `ABL-memory-9`.
3. Decoder-coupling remains unvalidated until `ABL-memory-10`.
4. NSA remains non-load-bearing until `ABL-memory-11`.

## Recommended next action

Default next action:

```text
Prepare a P0 execution DEC template, still markdown-only, so the user
can later authorize or reject implementation with exact scope.
```

Alternative if the user explicitly authorizes execution:

```text
Open a new DEC for implementing P0 ABL-memory-0..8 under:
  Dream/experiments/prototypes/memory_v03_p0/
```

## Version history

```text
v1  2026-05-08  cycle 029 review report. Approved SPEC-20260508-002
                for planning use after surgical corrections.
```
