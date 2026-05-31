# Dream3R final architecture selection agent prompt

Use this prompt for the next agent that will execute the selected final
Dream3R architecture path.

```text
You are taking over Dream3R after the 2026-05-30 final architecture selection.

Workspace: E:\Dream3R

Mandatory read order:
1. E:\Dream3R\TASK_SNAPSHOT.md
2. E:\Dream3R\decisions\DEC-20260530-015-final-architecture-selection.md
3. E:\Dream3R\specs\SPEC-20260530-005-dream3r-pd-final-architecture.md
4. E:\Dream3R\planning\DREAM3R_PD_FINAL_ARCHITECTURE_PLAN.md
5. E:\Dream3R\decisions\DEC-20260530-014-v22-vggt-omega-admission.md
6. E:\Dream3R\specs\SPEC-20260530-004-dream3r-v22-expert-admission.md
7. E:\Dream3R\planning\DREAM3R_V22_ADMISSION_RUNBOOK.md
8. E:\Dream3R\decisions\DEC-20260530-011-scf-midterm.md
9. E:\Dream3R\decisions\DEC-20260530-012-ver21-state-training-metrics.md

Final selected architecture:
Dream3R-PD = Proposal-bank Distilled State-Conditioned 3R.

Do not reopen broad route search.
Do not present hard expert routing as the model.
Do not turn VGGT-Omega into the whole Dream3R model.

Current evidence:
- bounded SCF over MASt3R/Fast3R/Spann3R is the usable prototype;
- correct state beats no-state and shuffled-state on abs_rel and patch-oracle gap;
- temporal/scale metrics are not solved and must remain explicit gates;
- VGGT-Omega is the first v2.2 teacher candidate, execution gated.

Execution priority:
1. Write VGGT-Omega deployment inventory and G2 execution DEC draft.
2. Prototype ProposalSetDecoder over existing 3-expert caches.
3. Add trained-state projection / Critic calibration outside frozen core.
4. Admit VGGT-Omega only after real-backend smoke.
5. Attempt native decoder distillation only after proposal-set decoder wins.

Hard constraints:
- Do not edit frozen core files without a new DEC:
  model.py, anchor_bank.py, nsa_attention.py, bus.py, orchestrator.py,
  repair.py, modules.py, contracts.py, config.py.
- Windows local is for docs/code edits and scp only; model execution goes
  through ssh BUAA-Server.
- Server GPU default: CUDA_VISIBLE_DEVICES=1.
- No checkpoint download, install mutation, long run, or training campaign
  without a DEC naming the command, path, and expected output.

Output requirement:
If you create or promote artifacts, update TASK_SNAPSHOT.md, WORKFLOW_STATUS.md,
INDEX.md, README.md, RESEARCH_STATE.md, decision registry, and cycle log.
```
