# Dream3R v2.2 VGGT-Omega admission agent prompt

Use this prompt for the next agent that will research or execute v2.2 expert
admission.

```text
You are taking over Dream3R after the 2026-05-30 v2.2 admission correction.

Workspace: E:\Dream3R

Mandatory read order:
1. E:\Dream3R\TASK_SNAPSHOT.md
2. E:\Dream3R\decisions\DEC-20260530-014-v22-vggt-omega-admission.md
3. E:\Dream3R\specs\SPEC-20260530-004-dream3r-v22-expert-admission.md
4. E:\Dream3R\planning\DREAM3R_V22_ADMISSION_RUNBOOK.md
5. E:\Dream3R\decisions\DEC-20260530-013-milestone-reorg-proposal-bank-native-roadmap.md
6. E:\Dream3R\specs\SPEC-20260530-003-dream3r-reconstruction-decoder-roadmap.md
7. E:\Dream3R\planning\DREAM3R_MILESTONE_REORG_20260530.md
8. E:\Dream3R\decisions\DEC-20260530-011-scf-midterm.md
9. E:\Dream3R\decisions\DEC-20260530-012-ver21-state-training-metrics.md

Current model identity:
Dream3R = proposal encoders + Dream state + state-conditioned reconstruction decoder.

Do not describe Dream3R as a hard router or loose ensemble.

Current proven bank:
- MASt3R
- Fast3R
- Spann3R

Current v2.2 admission order:
1. VGGT-Omega / VGGT-Ω
2. CUT3R
3. MonST3R

Important deconfusion:
- VGGT-Omega is the upgraded VGGT-family proposal expert candidate.
- vanilla VGGT is now a baseline / schema ancestor, not the first integration target.
- OVGGT is a separate memory/cache comparator. Do not treat OVGGT as VGGT-Omega.

Recommended first task:
Research VGGT-Omega deployment without running it yet:
- official repo and project page;
- dependency and checkpoint policy;
- native output fields;
- minimal inference command;
- adapter normalization plan into ExpertProposal;
- exact G2 execution DEC draft for a one-window BUAA-Server smoke.

Hard constraints:
- Do not edit frozen core files without a new DEC:
  model.py, anchor_bank.py, nsa_attention.py, bus.py, orchestrator.py,
  repair.py, modules.py, contracts.py, config.py.
- Windows local is for docs/code edits and scp only; model execution goes
  through ssh BUAA-Server.
- Server GPU default: CUDA_VISIBLE_DEVICES=1.
- No checkpoint download, install mutation, or server run until a follow-up
  execution DEC names the path, checkpoint, command, and fallback exclusion.

Output requirement:
Update TASK_SNAPSHOT.md, WORKFLOW_STATUS.md, INDEX.md, registry entries, and
cycle log if you create a new decision/spec/plan.
```
