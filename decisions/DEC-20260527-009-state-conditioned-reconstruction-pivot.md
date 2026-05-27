# DEC-20260527-009 — Pivot Dream3R from hard expert selection to state-conditioned reconstruction

decision_id: DEC-20260527-009
date: 2026-05-27
scope: Dream3R architecture direction and midterm narrative
decision: Demote hard expert selection from the headline architecture claim and promote state-conditioned reconstruction as the post-midterm Dream3R direction.
status: accepted for architecture planning; implementation remains gated

## Context

The original v0.2 architecture narrowed the main claim to
Verification-as-architecture plus Heterogeneous best-of-N Composer. The
last three closures show that this is not strong enough as the primary
research direction:

- DEC-007: routing is learnable, especially on ETH3D, but it is bounded
  by the expert pool and domain-specific.
- DEC-008: Critic -> Router reroute is wired but negative at the current
  data scale.
- MIDTERM §3: final `pointmap` in V04Pipeline equals the selected expert's
  standalone output; Memory / Anchor / NSA / Permanence / Critic state is
  emitted but not used by the depth-producing path.
- Stage 6: the right missing wire is a state-to-depth wire, but its first
  cache also surfaced a real-backend loading pathology.

## Evidence

Evidence labels:

- `code-observed`: `ReconstructionOutput.pointmap = expert.pointmap` in
  the v0.4 pipeline.
- `server-observed`: DEC-007 and DEC-008 routing / reroute sweeps.
- `inferred`: hard routing is better framed as a diagnostic baseline than
  as the final Dream3R architecture.

The core architectural weakness is not that Composer is useless. It is
that Composer is currently the only depth-affecting architectural lever.
Everything upstream becomes control-plane state unless a fusion/correction
module consumes it.

## Options

### Option A — Keep best-of-N Composer as the main claim

Rejected. It is experimentally bounded, easy to frame as an ensemble
baseline, and does not make Memory/Anchor/NSA load-bearing for final
geometry.

### Option B — Discard Composer and make Memory the only claim

Rejected. Composer produced real evidence and remains useful as a regime
probe and proposal prior. Discarding it would lose a validated diagnostic
surface.

### Option C — Reframe Dream3R as state-conditioned reconstruction

Accepted. Composer remains as proposal prior / diagnostic baseline, while
the new load-bearing claim becomes:

```text
persistent state + reliability signals directly condition final pointmap
```

## Decision

Adopt `SPEC-20260527-001-dream3r-state-conditioned-reconstruction.md` as
the architecture addendum for post-midterm work.

This decision partially supersedes SPEC-20260506-004 Delta 6:

```text
old headline D: Heterogeneous best-of-N Composer
new role for D: proposal prior / diagnostic baseline / cost-aware runner
```

The new headline mechanism is:

```text
state-conditioned fusion and correction
```

## Risks

- A simple residual head may show null or negative gain on real expert
  baselines. That does not invalidate the pivot; it means current state is
  not yet depth-informative enough.
- Multi-expert fusion increases compute cost. Composer should remain as a
  cost-aware proposal scheduler.
- Long-sequence metrics may be harder to explain than abs_rel. The midterm
  report should keep abs_rel as a sanity metric but not as the sole claim.

## User Approval Required

Already provided in active conversation for architecture route adjustment:

```text
"我们调整架构吧，我认为这是必要的"
"可以开始推进，我们最初的架构设计你优化一下吧"
```

Still requires separate approval:

- core v0.3/v0.5 code edits
- new checkpoint download
- long training outside the approved Stage 6 path
- final thesis declaration

## Next Action

1. Keep the Stage 6 real-backend rerun, but interpret it as L1
   state-to-depth evidence, not as a router upgrade.
2. Update the midterm report to say routing-side control plane is
   validated but not sufficient.
3. After midterm, build L2 multi-expert proposal-bank cache and
   soft-fusion/correction head.

