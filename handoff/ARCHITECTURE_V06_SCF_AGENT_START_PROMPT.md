# Dream3R-ver2.0 SCF next-agent prompt

Use this prompt to start another agent after the 2026-05-30 midterm SCF
closure. It is intentionally short so the agent starts from the documented
state instead of re-planning the whole project.

```text
You are taking over Dream3R after the 2026-05-30 midterm closure.

Workspace: E:\Dream3R.
Time budget: this is a two-day midterm recovery/ship window, not a 4-week
architecture exploration.

Mandatory read order:
1. E:\Dream3R\TASK_SNAPSHOT.md
2. E:\Dream3R\decisions\DEC-20260530-011-scf-midterm.md
3. E:\Dream3R\specs\SPEC-20260530-001-dream3r-ver2-scf-architecture.md
4. E:\Dream3R\decisions\DEC-20260530-012-ver21-state-training-metrics.md
5. E:\Dream3R\specs\SPEC-20260530-002-dream3r-ver21-state-training-metrics.md
6. E:\Dream3R\planning\DREAM3R_VER21_STATE_TRAINING_PLAN.md
7. E:\Dream3R\mainwork\midterm\MIDTERM-20260530.md
8. E:\Dream3R\mainwork.md
9. E:\Dream3R\AGENT_MASTER_PROMPT.md

Current conclusion:
- Dream3R-ver2.0 is bounded state-conditioned multi-expert fusion (SCF).
- Hard expert selection / Composer routing is NOT the headline architecture;
  Composer is only a proposal prior, scheduler, and diagnostic baseline.
- L0 real-backend guardrail fixed the fallback-stub pathology.
- L1 single-expert residual is NEGATIVE.
- L2 SCF is POSITIVE: KITTI +9.8% +/- 2.7% vs best single, ETH3D +2.4% +/-
  3.0%, near-oracle gaps ~1-2%.
- Ver2.1 direction is trained-state SCF: patch-oracle / temporal-delta /
  scale-drift metrics are now implemented, and the first 4-seed control has
  completed.
- 4-seed refresh summary:
  correct state = KITTI +9.79%, ETH3D +2.44%;
  no-state = KITTI +5.04%, ETH3D -6.47%;
  shuffled-state = KITTI +3.27%, ETH3D -10.09%.
  Correct state also has the lowest patch-oracle gap on both domains. This
  supports window-aligned state usefulness, while temporal/scale proxies
  remain open.

Do not reopen broad architecture search. Do not make VGGT, GaussianHead,
tttLRM, Test3R off-path, Critic reroute, or more router sweeps the main
route unless DEC-011 says they are needed as a bounded follow-up.

Hard constraints:
- Do not edit frozen v0.3/v0.5 core without a new DEC:
  model.py, anchor_bank.py, nsa_attention.py, bus.py, orchestrator.py,
  repair.py, modules.py, contracts.py, config.py.
- Windows local is for docs/code edits and scp only; model execution goes
  through ssh BUAA-Server.
- Server GPU default: CUDA_VISIBLE_DEVICES=1.
- No new checkpoint downloads or long training unless explicitly approved.

Your next task:
Plan and start the smallest post-midterm L4 step that makes SCF more
credible:
1. draft/run the frozen-state projection experiment, or
2. package the SCF + ver2.1 result for midterm presentation, or
3. draft the DEC for explicit temporal/scale state training.

The first option now has a local implementation surface in
`code/dream3r/scripts/train_scf_head.py`; server execution remains gated.

Output requirements:
- State which of the three L4 paths you chose and why.
- Keep the plan under the SCF/ver2.0 architecture.
- Mark any core edit, server training, checkpoint download, or long run as
  DEC/user-gated.
- If you edit files, update TASK_SNAPSHOT.md, WORKFLOW_STATUS.md, and the
  relevant cycle/decision/spec index.
```
