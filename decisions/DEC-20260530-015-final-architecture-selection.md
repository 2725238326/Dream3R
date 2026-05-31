# DEC-20260530-015 — Select the final Dream3R architecture path

decision_id: DEC-20260530-015
date: 2026-05-30
scope: Dream3R final architecture selection
status: accepted as the final candidate architecture path; implementation remains staged and gated

## Context

The project has already falsified or demoted the unstable routes:

- hard expert selection is not the final Dream3R model;
- single-expert residual correction is negative;
- bounded SCF over real MASt3R / Fast3R / Spann3R proposals is positive;
- correct state beats no-state and shuffled-state on abs_rel and patch-oracle
  gap, but temporal / scale proxies are not solved;
- VGGT-Omega is now the first v2.2 admission target, with vanilla VGGT kept
  as baseline and OVGGT kept as a separate memory/cache comparator.

The remaining question is what can be defended as the final route rather than
another temporary patch.

## Decision

Select **Dream3R-PD** as the final architecture path:

```text
Dream3R-PD = Proposal-bank Distilled State-Conditioned 3R
```

The model is defined as:

```text
images
-> proposal encoders / teachers
-> Dream state encoder
-> state-conditioned proposal-set decoder
-> native Dream3R decoder distilled with proposal dropout
-> final pointmap + confidence + diagnostics
```

This is the final choice because it preserves the real evidence from SCF while
creating a route toward a standalone Dream3R model instead of a permanent
expert ensemble.

## Architecture layers

### Layer 0 — proposal teachers

Current core teachers:

```text
MASt3R / Fast3R / Spann3R
```

v2.2 admission order:

```text
VGGT-Omega -> CUT3R -> MonST3R
```

External methods are teachers / proposal encoders. They do not define the
Dream3R model identity.

### Layer 1 — Dream state encoder

Dream state remains the owned mechanism:

```text
Memory / AnchorBank / NSA / Permanence / Critic / Composer metadata
```

The next refinement is not larger routing. It is state reliability:

```text
state projection + critic calibration + temporal / scale objectives
```

### Layer 2 — proposal-set reconstruction decoder

SCFHead stays as Decoder v0. The final selected decoder family is a small
proposal-set decoder:

```text
proposal tokens:
  expert_id, backend, cost, pointmap patch, confidence, local scale

state tokens:
  memory context, anchor summary, NSA summary, permanence summary,
  critic reliability

decoder:
  cross-attend proposal tokens to state tokens
  predict bounded fusion weights, uncertainty, and diagnostics
```

This decoder must be trainable from cached proposals before any frozen-core
edit.

### Layer 3 — native decoder distillation

Once proposal-set decoding beats SCF, train the native Dream3R decoder:

```text
proposal-bank oracle / SCF weights / proposal-set decoder targets
+ proposal dropout
+ temporal / scale losses
-> native Dream3R decoder
```

The native decoder is the final product. The proposal bank is the teacher.

## Rejected final choices

| rejected route | reason |
| --- | --- |
| hard expert router | already demoted; selection alone cannot be the model |
| permanent full ensemble | expensive and weak as a thesis; does not create Dream3R-owned reconstruction |
| VGGT-Omega-only model | strong baseline, but it would make Dream3R a wrapper, not a new architecture |
| memory-only architecture | state is useful but not enough until temporal / scale metrics improve |
| direct native training now | premature before proposal-bank teacher targets and decoder gates are proven |
| broad expert search | too slow; breaks causality and deadline discipline |

## Minimal final claim

The defendable final claim is:

```text
Dream3R learns a state-conditioned reconstruction decoder from a small bank
of strong 3R proposal teachers, then distills that behavior toward a native
decoder with proposal dropout.
```

Do not claim:

```text
Dream3R is globally better than VGGT-Omega / CUT3R / MonST3R.
Dream3R has solved long-term memory.
Dream3R is native before proposal-set decoder and distillation gates pass.
```

## Acceptance gates

Dream3R-PD becomes the final implementation only if these gates pass:

1. **proposal admission gate**: VGGT-Omega real backend produces admissible
   proposal cache entries or is kept as comparator only;
2. **state gate**: correct-state remains better than no-state and
   shuffled-state after candidate admission;
3. **decoder gate**: proposal-set decoder beats SCFHead on abs_rel and
   patch-oracle gap;
4. **temporal / scale gate**: temporal_delta and scale_drift do not degrade;
5. **distillation gate**: native decoder with proposal dropout keeps most of
   proposal-set decoder quality while dropping at least one external teacher
   at inference.

If gate 1 fails, continue with the 3-expert bank. If gate 3 fails, keep SCF as
the honest final prototype and report native distillation as future work.

## Immediate execution plan

Use:

- `specs/SPEC-20260530-005-dream3r-pd-final-architecture.md`
- `planning/DREAM3R_PD_FINAL_ARCHITECTURE_PLAN.md`
- `handoff/ARCHITECTURE_V09_FINAL_SELECTION_AGENT_PROMPT.md`

No checkpoint download, server run, core edit, or training is authorized by
this DEC alone.
