# Dream3R closing mainline agent prompt

Date: 2026-06-09
Purpose: hand off Dream3R final-stage work to another agent while keeping the mainline focused and still allowing small evidence-backed improvements.

## Role

You are taking over Dream3R at the closing stage. Your job is to turn the current usable model package into a clean final deliverable: final report material, final PPT material, verification evidence, artifact inventory, clear limitations, and any small low-risk model-package improvements that can be verified quickly.

The mainline starts from `v1.1.0`, but it is not frozen. You may make small, reversible improvements around the current release line when they improve delivery quality and can be verified with the existing v1.1/v1.0 gates. Do not present Qwen or Foundation3R as part of the official model unless new evidence actually passes the required controls. Do not claim Dream3R is a proposal-free 3R foundation model.

## Read first

Read these files in order:

1. `TASK_SNAPSHOT.md`
2. `WORKFLOW_STATUS.md`
3. `README.md`
4. `INDEX.md`
5. `release/COMPLETE_MODEL_V1_1.md`
6. `release/EFFECTIVE_ARCHITECTURE_V1_1.md`
7. `release/VERIFY_REPORT.md`
8. `reports/midterm/DREAM3R_MIDTERM_REPORT_DRAFT.md`
9. `reports/opening/DREAM3R_OPENING_REPORT_STUDENT_FINAL.md`

Use these as the source of truth. Older architecture prompts are background only.

## Current official model

The current official deliverable is Dream3R `v1.1.0`. Treat it as the baseline to improve from, not as a reason to stop all optimization.

```text
model type: state-conditioned proposal-fusion 3R model
KITTI branch: v1.0-rc1 bounded StatePrior + residual
ETH3D branch: VGGT-Omega-expanded state-conditioned fusion
metric: AbsRel, lower is better
KITTI / ETH3D: 0.1448 / 0.0570
state controls:
  KITTI normal/no-state/shuffle: 0.1448 / 0.1553 / 0.1521
  ETH3D normal/no-state/shuffle: 0.0570 / 0.0583 / 0.0598
fallback: v1.0-rc1
```

Allowed claim:

```text
Dream3R v1.1.0 is a runnable and verifiable state-conditioned proposal-fusion model for feed-forward 3D reconstruction. It organizes teacher-model geometry proposals into a proposal bank and uses state and domain information to choose or fuse geometry. It has metrics, state controls, release scripts, demo scripts, verification documents, and local/server evidence.
```

Disallowed claim:

```text
Dream3R is a complete proposal-free 3R foundation model trained from images.
```

## Main tasks

### 1. Finalize model delivery evidence

Check that the following are present and internally consistent:

- `release/COMPLETE_MODEL_V1_1.md`
- `release/EFFECTIVE_ARCHITECTURE_V1_1.md`
- `release/MODEL_CARD_V1_1.md`
- `release/ARCHITECTURE_DIAGRAM_V1_1.md`
- `release/VERIFY_REPORT.md`
- `release/ARTIFACTS.json`
- `release/RUNBOOK.md`
- `code/dream3r/scripts/verify_v11_release.py`
- `code/dream3r/scripts/smoke_v11_release_model.py`
- `code/dream3r/scripts/run_dream3r_v11_demo.py`
- `code/dream3r/scripts/run_dream3r_v11_cache_demo.py`

If a document contradicts the v1.1.0 identity, fix the document. If a script fails, fix only the smallest broken wrapper or test contract.

### 2. Prepare final report material

Use the existing opening and midterm reports as scaffolds. The final report should focus on:

- what problem Dream3R addresses;
- what the current model is;
- how the proposal bank, state, domain policy, and VGGT-Omega branch work;
- what metrics and controls support the claim;
- which branches failed or stayed diagnostic;
- what limitations remain.

Keep language direct. Avoid promotion-style phrasing. Do not over-explain research background.

### 3. Prepare final PPT material

The final PPT should be compact. Recommended flow:

1. problem and motivation;
2. current model identity;
3. architecture diagram;
4. v1.1.0 branch policy;
5. KITTI/ETH3D metrics;
6. state-control table;
7. VGGT-Omega evidence;
8. Qwen/Foundation3R status;
9. verification and deliverables;
10. limitations and conclusion.

### 4. Fill remaining weak points and allow small optimizations

First fill gaps that affect final delivery:

- missing artifact links;
- inconsistent metric tables;
- unclear model boundary;
- broken verifier or smoke command;
- missing limitation statement;
- missing final-report/PPT outline;
- missing short reproduce instructions.

Small model-package improvements are allowed if they stay close to the v1.1 line. Examples:

- confidence calibration inside the existing proposal-fusion path;
- clearer conflict-score handling if the current interfaces already expose it;
- small domain-policy cleanup that preserves KITTI and ETH3D controls;
- verifier, smoke, cache-demo, or artifact-manifest hardening;
- report/PPT updates that make the model boundary easier to defend.

Guardrails:

- keep `v1.1.0` as the baseline and compare against it;
- preserve `v1.0-rc1` fallback verification;
- require normal/no-state/shuffle controls for any metric-affecting change;
- avoid checkpoint download, large training, broad architecture refactor, or new model-family admission unless the user explicitly asks;
- if a small optimization does not beat or clarify the current package quickly, record it as non-promoted and return to closing work.

## Verification commands

Local verification:

```powershell
python -B code\dream3r\scripts\verify_v11_release.py --root .
python -B code\dream3r\scripts\smoke_v11_release_model.py --output runs\release\v11_smoke\smoke_v11_release_model.json
python -B code\dream3r\scripts\run_dream3r_v11_demo.py --domain kitti --output runs\release\v11_demo\demo_kitti.json
python -B code\dream3r\scripts\run_dream3r_v11_demo.py --domain eth3d --output runs\release\v11_demo\demo_eth3d.json
python -B code\dream3r\scripts\verify_release_candidate.py --root .
```

Server verification, if needed and already configured:

```text
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -B dream3r/scripts/verify_v11_release.py --root .
conda run -n dream3r python -B dream3r/scripts/smoke_v11_release_model.py --output runs/release/v11_smoke/smoke_v11_release_model.json
CUDA_VISIBLE_DEVICES=1 conda run -n dream3r python -B dream3r/scripts/run_dream3r_v11_cache_demo.py --domain eth3d --output runs/release/v11_cache_demo/cache_demo_eth3d.json --max-entries 1 --device cuda
```

Do not download weights or start training as part of closing work.

## Final answer format for the next agent

Report only:

- files changed;
- evidence checked;
- remaining risks;
- next concrete closing step.

Keep it short.
