# CYCLE-20260527 — State-conditioned reconstruction pivot

cycle_id: CYCLE-20260527-state-conditioned-reconstruction
date: 2026-05-27
cycle_name: routing ceiling to state-conditioned reconstruction

## Goal

Optimize the original Dream3R architecture design after the user identified
hard expert selection as an insufficient mainline.

## User Direction

The user explicitly challenged the router-first framing:

```text
"选专家这个思路很烂吧其实"
"那我们该怎么做啊，我觉得要改改路线"
"我们调整架构吧，我认为这是必要的"
"可以开始推进，我们最初的架构设计你优化一下吧"
```

## Sources Reviewed

- `mainwork/HANDOFF-20260527-stage6.md`
- `mainwork/midterm/MIDTERM-20260530.md`
- `specs/SPEC-20260506-001-dream3r-architecture.md`
- `specs/SPEC-20260506-004-dream3r-architecture-v02.md`
- `specs/SPEC-20260522-001-dream3r-v05-axes.md`
- `mainwork.md`
- DEC-007 / DEC-008 summaries already reflected in `mainwork.md`

## Mechanisms Extracted

- Hard expert selection is a control-plane mechanism.
- State-conditioned fusion/correction is the missing reconstruction-plane
  mechanism.
- Composer remains useful as proposal prior, regime probe, and cost-aware
  proposal scheduler.
- Stage 6 should be interpreted as the first state-to-depth wire probe.

## Research Units Created Or Updated

No separate RU file created in this pass. The architectural unit is
captured as `SPEC-20260527-001`.

## Scoring Changes

No scoreboard update in this pass. The qualitative score of hard routing as
headline contribution is downgraded; the state-conditioned reconstruction
direction is promoted for post-midterm work.

## Decisions

Created:

- `decisions/DEC-20260527-009-state-conditioned-reconstruction-pivot.md`

Created architecture addendum:

- `specs/SPEC-20260527-001-dream3r-state-conditioned-reconstruction.md`

## Deferred Items

- Core code edits remain blocked by CLAUDE.md unless a separate DEC grants
  an exemption.
- Multi-expert proposal-bank cache is the next implementation design after
  the Stage 6 real-backend rerun.
- Long-sequence coherence metrics need a concrete post-midterm plan.

## Next Action

1. Finish the Stage 6 real-backend rerun path if feasible.
2. Finalize `mainwork/midterm/MIDTERM-20260530.md` with the new narrative:
   routing-side validated, reconstruction-plane missing, post-midterm
   pivot to state-conditioned reconstruction.

