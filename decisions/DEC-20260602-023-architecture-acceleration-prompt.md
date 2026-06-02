# DEC-20260602-023: Accelerated architecture convergence prompt

Date: 2026-06-02
Status: accepted
Scope: Dream3R architecture execution mode

## Decision

Adopt an accelerated architecture-convergence handoff for the next Dream3R
agent. The next agent must stop treating tiny residual gains as the main
research lane and must instead drive Dream3R toward a usable architecture
milestone:

```text
proposal teachers + Dream state
-> frozen trained StatePrior
-> bounded fusion/refinement baseline
-> native student decoder/distillation candidate
```

The current bounded residual result remains the best verified baseline, but it
is not the final ambition. Future work should use it as a control and move to
high-impact gates: native distillation, state-objective training, and tightly
gated teacher-bank admission.

## Why

The 2026-05-31 to 2026-06-01 runs established a clear pattern:

- `StatePriorHead` proves Dream state contains usable expert-prior signal.
- joint `ProposalSetDecoder` training collapses or overrides that signal.
- frozen StatePrior preserves state causality.
- bounded residual refinement gives only a small positive gain.

That is enough evidence to stop cycling on small head variants. The architecture
problem is now how to make Dream3R own the reconstruction path, not how to tune
another shallow mixer.

## Accepted execution posture

The next agent should:

1. Lock the current bounded frozen-prior model as the baseline.
2. Draft and execute only gates that can materially change the model class.
3. Prefer native student decoder/distillation over more residual-head variants.
4. Admit new teachers only if they improve proposal diversity or oracle bounds.
5. Keep state causality controls mandatory: correct-state must beat shuffle/no-state.

## Rejected

| Option | Reason |
| --- | --- |
| Continue residual-head micro-variants | Low ceiling; likely consumes time without changing the architecture claim. |
| Reopen broad expert search | The project already narrowed the bank; blind search loses causality and time. |
| Promote VGGT-Omega as Dream3R itself | External model wrapper is not a Dream3R-owned architecture. |
| Train joint decoder without frozen-prior guardrails | DEC-020 showed collapse/override of the state prior. |

## Artifacts

- `planning/DREAM3R_ARCHITECTURE_ACCELERATION_PLAN_20260602.md`
- `handoff/ARCHITECTURE_V10_ACCELERATED_CONVERGENCE_AGENT_PROMPT.md`
- `cycles/CYCLE-20260602-architecture-acceleration-prompt.md`

## Boundaries

- No frozen core edits are authorized by this decision.
- No checkpoint download, environment mutation, server training campaign, or
  long run is authorized by this decision alone.
- Existing server path remains `/hdd3/kykt26/code/dream3r`.
- GPU default remains `CUDA_VISIBLE_DEVICES=1`.

