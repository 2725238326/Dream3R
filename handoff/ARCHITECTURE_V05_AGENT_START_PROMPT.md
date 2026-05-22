# Dream3R v0.5 execution agent start prompt

Use this prompt to start a focused architecture evidence-closure pass:

```text
You are working in E:\Dream3R. Read planning/DREAM3R_V05_ITERATION_TEST_PLAN.md first, then ARCHITECTURE_V04_STATUS.md, specs/SPEC-20260522-001-dream3r-v05-axes.md, TASK_SNAPSHOT.md, WORKFLOW_STATUS.md, and the v0.4 code under code/dream3r/contracts.py, repair.py, orchestrator.py, plus evaluate_real_sequence.py and ablate_real_sequence.py.

Your task is to begin the v0.5 evidence-closure program, starting with S0 local v0.4 edge tests and the server runbook for S1 A6 KITTI long-sequence memory verification.

Do not download checkpoints, train models, modify KYKT frontend, or claim any v0.5 axis closed. Make conservative additive edits, run available local tests, and update the relevant markdown status with exact test commands and remaining blockers.
```
