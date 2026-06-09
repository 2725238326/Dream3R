# Short Prompt: Start Dream3R Final Model Improvement

You are working in `E:\Dream3R`.

Read first:

```text
TASK_SNAPSHOT.md
handoff/DREAM3R_FINAL_MODEL_IMPROVEMENT_HANDOFF_20260610.md
handoff/CONTEXT_COMPACTION_20260608_V11_USABLE_MODEL.md
```

Task: improve the final Dream3R model without reopening architecture search.

Baseline:

```text
official model: Dream3R v1.1.0
stable fallback: v1.0-rc1
KITTI / ETH3D AbsRel: 0.1448 / 0.0570
controls:
  KITTI normal/no-state/shuffle: 0.1448 / 0.1553 / 0.1521
  ETH3D normal/no-state/shuffle: 0.0570 / 0.0583 / 0.0598
```

Execute:

1. Run baseline v1.1/v1.0 verifiers and targeted release tests.
2. Build a final evaluation pack under `runs/release/v11_final_eval/` and a
   compact table under `release/FINAL_EVAL_TABLE_V1_1.md`.
3. Try one small, reversible v1.1 fusion improvement: confidence calibration or
   conflict-aware residual/dampening. Keep output contracts stable.
4. Promote only if KITTI <= `0.1448`, ETH3D <= `0.0570`, both domains still
   beat no-state and shuffle controls, v1.0 fallback remains green, and tests
   pass. Otherwise keep `v1.1.0` official and record the attempt as neutral or
   negative.
5. Sync `TASK_SNAPSHOT.md`, `WORKFLOW_STATUS.md`, `release/VERIFY_REPORT.md`,
   and `release/ARTIFACTS.json`.

Do not promote Qwen, Foundation3R, proposal-free decoding, or `v1.2-exp0`.
Do not download checkpoints or start broad architecture exploration.
