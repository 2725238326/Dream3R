# CYCLE-20260530 — Dream3R ver2.0 SCF midterm closure

date: 2026-05-30
status: closed for midterm documentation; further training deferred
linked_decision: `decisions/DEC-20260530-011-scf-midterm.md`
linked_spec: `specs/SPEC-20260530-001-dream3r-ver2-scf-architecture.md`

## Objective

Turn the 2026-05-27 route correction into a two-day midterm deliverable:
an honest usable Dream3R-ver2.0 model target, real-backend baselines,
negative-result accounting, positive SCF result, and a next-agent prompt that
keeps future work focused.

## Actions completed

- Diagnosed and fixed the Stage 6 baseline pathology with an L0 real-backend
  guardrail in non-core scripts.
- Re-ran the single-expert residual head on real adapters and rejected it as
  L1 negative.
- Built the all-expert proposal-bank SCF path:
  `code/dream3r/scf_head.py`,
  `code/dream3r/scripts/build_scf_cache.py`,
  `code/dream3r/scripts/train_scf_head.py`.
- Evaluated SCF across 4 seeds on KITTI and ETH3D held-out splits.
- Recorded the accepted decision in `DEC-20260530-011`.
- Promoted the result into the ver2.0 architecture spec.

## Result

Dream3R-ver2.0 is now defined as bounded state-conditioned multi-expert
fusion, not hard expert selection. Composer is a proposal prior / scheduler,
not the thesis centerpiece.

Evidence:

| test | verdict |
| --- | --- |
| L0 real-backend guardrail | pass; real fast3r baseline ~0.232 KITTI / ~0.213 ETH3D, not ~0.93 stub |
| L1 single-expert residual | negative; KITTI -47.1pp, ETH3D -91.9pp |
| L2 SCF | positive; KITTI +9.8% +/- 2.7% vs best single, ETH3D +2.4% +/- 3.0% |
| no-state ablation | state is load-bearing in seed 7; fusion-only weakens KITTI and flips ETH3D negative |
| residual ablation | rejected; diverges |

## Honest boundaries

- The state signal is `memory.fused_context` from the current untrained
  memory path; this validates state-conditioned fusion, not trained memory
  quality.
- ETH3D is small and noisy.
- No temporal metric, scale-drift metric, or leave-one-scene-out split has
  been run.
- No frozen v0.3/v0.5 core files were modified.

## Follow-up prompt

Future agents should start from:

```text
handoff/ARCHITECTURE_V06_SCF_AGENT_START_PROMPT.md
```

They should continue SCF/ver2.0 consolidation and L4 state retraining
planning, not reopen broad architecture search.
