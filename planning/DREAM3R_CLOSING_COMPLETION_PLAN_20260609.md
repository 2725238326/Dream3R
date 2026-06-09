# Dream3R closing completion plan

Date: 2026-06-09
Status: active closing plan

## Goal

Bring Dream3R to a clean closing-state deliverable.

Closing work starts from the current architecture and allows small, reversible improvements when they can be verified quickly. The main output remains a coherent model package, evidence set, report, and presentation material for final submission or defense.

## Final model stance

Use this as the current baseline model statement:

```text
Dream3R v1.1.0 is a state-conditioned proposal-fusion model for feed-forward 3D reconstruction.
It uses existing 3R teacher outputs as proposal geometry, then applies state and domain-conditioned fusion.
KITTI uses the v1.0-rc1 stable branch.
ETH3D uses the VGGT-Omega-expanded state-conditioned fusion branch.
```

Do not describe it as a fully independent proposal-free 3R foundation model. If a small optimization is added before closing, document it as an incremental update over this baseline and keep the original v1.1.0 numbers visible.

## Closing checklist

### A. Model package

- Confirm `release/COMPLETE_MODEL_V1_1.md` still names `v1.1.0` as the official package.
- Confirm `release/EFFECTIVE_ARCHITECTURE_V1_1.md` contains the branch policy and metric table.
- Confirm `release/MODEL_CARD_V1_1.md` states model scope and limitations.
- Confirm `release/ARTIFACTS.json` lists the report, release, run, and verification artifacts.
- Confirm `release/RUNBOOK.md` contains reproduce commands.

### B. Verification

- Run local v1.1 verifier.
- Run local v1.1 smoke.
- Run local branch demo for KITTI and ETH3D.
- Run v1.0 fallback verifier.
- If server access is already available, run the GPU1 cache demo for one ETH3D entry.
- Record results in `release/VERIFY_REPORT.md` only if fresh runs were actually performed.

### C. Final report

Build the final report from the current opening and midterm documents:

- opening report: previous-stage motivation and planned route;
- midterm report: v1.1.0 model identity, completed work, metrics, controls, limitations;
- release docs: exact model package, scripts, evidence, artifacts.

Final report sections should be compact:

1. research problem;
2. related work and route selection;
3. Dream3R model design;
4. implementation and release package;
5. experiments and controls;
6. non-promoted branches;
7. limitations;
8. conclusion.

### D. Final PPT

Create a defense-ready deck around the model that actually exists.

Keep it to 12-16 core slides:

1. title and task;
2. problem;
3. why feed-forward 3R;
4. Dream3R model identity;
5. architecture diagram;
6. proposal bank and state;
7. domain policy;
8. metrics;
9. state controls;
10. VGGT-Omega branch;
11. Qwen and Foundation3R status;
12. deliverables;
13. limitations;
14. conclusion.

### E. Gaps and small optimizations to fill before closing

Fill these delivery gaps first:

- inconsistent names: proposal bank / candidate geometry / state-conditioned fusion;
- outdated metric values;
- missing limitation statements;
- missing reproduce command;
- missing artifact link;
- report/PPT language that sounds like promotion instead of student project writing;
- broken local verifier or smoke command.

Then allow small optimization work if it stays within the current release line:

- confidence or conflict-score cleanup in the existing fusion path;
- minor domain-policy cleanup that does not weaken current controls;
- release wrapper, verifier, smoke, cache-demo, or artifact-manifest hardening;
- report/PPT evidence cleanup tied to the current model;
- one small metric-affecting change only if normal/no-state/shuffle controls can be rerun.

Avoid these during closing unless the user explicitly asks:

- new Qwen routing;
- new proposal-free foundation training;
- new teacher-model admission;
- broad architecture refactor;
- new benchmark claim without fresh evaluation;
- checkpoint download.

## Recommended closing order

1. Refresh release artifact inventory.
2. Run or re-read verification evidence.
3. Identify at most one small optimization candidate.
4. If the candidate is low-risk, implement and verify it; otherwise record it as future work.
5. Draft final report.
6. Draft final PPT.
7. Render final PDF/PPT.
8. QA first/last pages and core tables.
9. Update `TASK_SNAPSHOT.md`, `WORKFLOW_STATUS.md`, `INDEX.md`, and `README.md`.

## Minimal success condition

Dream3R is ready for closing when:

- the official model is consistently named `v1.1.0`;
- the model boundary is clear;
- metrics and controls are consistent across docs;
- final report and PPT use the same story;
- verification evidence is linked;
- limitations are stated plainly.
- any small optimization is either verified or clearly marked non-promoted.
