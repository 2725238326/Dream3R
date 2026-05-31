# Dream3R v2.2/v3.0 model-reorganization agent prompt

Use this prompt when starting another agent after the 2026-05-30 milestone
reorganization.

```text
You are taking over Dream3R after the 2026-05-30 model-first milestone
reorganization.

Workspace: E:\Dream3R

Mandatory read order:
1. E:\Dream3R\TASK_SNAPSHOT.md
2. E:\Dream3R\decisions\DEC-20260530-013-milestone-reorg-proposal-bank-native-roadmap.md
3. E:\Dream3R\specs\SPEC-20260530-003-dream3r-reconstruction-decoder-roadmap.md
4. E:\Dream3R\planning\DREAM3R_MILESTONE_REORG_20260530.md
5. E:\Dream3R\decisions\DEC-20260530-011-scf-midterm.md
6. E:\Dream3R\decisions\DEC-20260530-012-ver21-state-training-metrics.md
7. E:\Dream3R\specs\SPEC-20260530-001-dream3r-ver2-scf-architecture.md
8. E:\Dream3R\specs\SPEC-20260530-002-dream3r-ver21-state-training-metrics.md
9. E:\Dream3R\mainwork\midterm\MIDTERM-20260530.md
10. E:\Dream3R\AGENT_MASTER_PROMPT.md

Current model identity:
Dream3R is a state-conditioned 3R reconstruction model:

  images
  -> proposal encoders
  -> Dream state
  -> state-conditioned reconstruction decoder
  -> final pointmap

Do not describe Dream3R as a hard router or loose ensemble.
External 3R systems are proposal encoders / teachers. Dream3R owns the state
and reconstruction decoder.

Current proven bank:
- MASt3R
- Fast3R
- Spann3R

Next candidate bank, in priority order:
1. VGGT-Omega / VGGT-Ω
2. CUT3R
3. MonST3R

Deconfusion:
- vanilla VGGT is a baseline / schema ancestor, not the first v2.2 target.
- OVGGT is a separate memory/cache comparator, not VGGT-Omega.

Do not add every new 3R method. A candidate must improve complementarity,
patch-oracle ceiling, or state/temporal regimes.

Recommended next task:
Draft the v2.2 admission contract for VGGT-Omega/CUT3R/MonST3R:
- adapter output contract;
- cache schema extension;
- real-backend guardrail;
- admission metrics;
- expected failure cases;
- exact DEC gates before checkpoint download or server run.

Hard constraints:
- Do not edit frozen core files without a new DEC:
  model.py, anchor_bank.py, nsa_attention.py, bus.py, orchestrator.py,
  repair.py, modules.py, contracts.py, config.py.
- Windows local is for docs/code edits and scp only; model execution goes
  through ssh BUAA-Server.
- Server GPU default: CUDA_VISIBLE_DEVICES=1.
- No new checkpoint downloads or long training without a separate DEC.

Output requirement:
Update TASK_SNAPSHOT.md, WORKFLOW_STATUS.md, INDEX.md, and registry entries if
you create a new decision/spec/plan.
```
