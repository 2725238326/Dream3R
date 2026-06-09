# Dream3R Final-Stage Readiness Plan

Date: 2026-06-09

## Status

Dream3R is ready to move from closing-package preparation into final-stage
review, defense, and delivery polishing.

Update 2026-06-10: when the task is not just defense polish but active final
model improvement, hand off through:

```text
handoff/DREAM3R_FINAL_MODEL_IMPROVEMENT_HANDOFF_20260610.md
handoff/DREAM3R_FINAL_MODEL_IMPROVEMENT_START_PROMPT_20260610.md
```

That lane allows small, reversible v1.1 release-line improvements around
candidate-geometry fusion, provided the current metric and state-control gates
remain green.

The official deliverable remains:

```text
model: Dream3R v1.1.0
type: state-conditioned proposal-fusion 3R
api: dream3r.release_v11.build_dream3r_v11_release
KITTI / ETH3D AbsRel: 0.1448 / 0.0570
stable fallback: v1.0-rc1
```

The final-stage work is documentation, validation evidence, defense polish,
and packaging. It is not a new architecture-search phase.

## Locked Claims

The final report, PPT, README, release docs, and any future defense materials
should keep these claims stable:

- Dream3R v1.1.0 is the current official model package.
- The model is a state-conditioned proposal-fusion 3R system.
- KITTI uses the v1.0-rc1 bounded StatePrior + residual branch.
- ETH3D uses the VGGT-Omega-expanded SCF branch.
- State/no-state/shuffle controls are part of the core evidence:
  - KITTI: `0.1448 / 0.1553 / 0.1521`
  - ETH3D: `0.0570 / 0.0583 / 0.0598`
- v1.0-rc1 remains a stable fallback and regression gate.
- Qwen remains diagnostic-only.
- Foundation3R remains proposal-free future/research work, not the delivered
  model.

## Allowed Final-Stage Work

Allowed without reopening the research program:

1. Polish final report language, formatting, figure captions, and references.
2. Polish defense PPT ordering, slide density, speaker notes, and visual balance.
3. Refresh verification evidence after documentation edits.
4. Tighten artifact inventory and reproduction instructions.
5. Add small wording clarifications to limitations and non-claims.
6. Add tiny release-line fixes only if they are reversible and pass the current
   v1.1/v1.0 verification gates.

## Not Allowed Without A New Explicit Gate

Do not do these in the final-stage lane:

- Train a new model branch.
- Download or stage new checkpoints.
- Promote Qwen, Foundation3R, v1.2-exp0, or proposal-free decoding.
- Reopen broad architecture search.
- Rewrite the model story around VGGT-Omega as a universal replacement.
- Change the official metrics without rerunning and documenting state controls.
- Claim SOTA, universal generalization, image-only inference, or long-sequence
  deployment.

## Final-Stage Checklist

| ID | Item | Status | Evidence |
| --- | --- | --- | --- |
| FS-1 | Final report source and PDF exist | done | `reports/final/DREAM3R_FINAL_REPORT_20260609.md`; `reports/pdf/Dream3R_结题报告_20260609.pdf` |
| FS-2 | Final defense PPT source and PPTX exist | done | `reports/final/DREAM3R_FINAL_PPT_OUTLINE_AND_SCRIPT_20260609.md`; `reports/pptx/Dream3R_Final_Defense_20260609.pptx` |
| FS-3 | Deliverable inventory exists | done | `reports/final/DREAM3R_FINAL_DELIVERABLE_INVENTORY_20260609.md` |
| FS-4 | Release artifact manifest points to final deliverables | done | `release/ARTIFACTS.json` |
| FS-5 | Old RC materials are labeled historical/fallback | done | `release/METHOD_ONEPAGER.md`; `release/RESULT_TABLE.md`; `release/PRESENTATION_OUTLINE.md`; README/INDEX/WORKFLOW updates |
| FS-6 | Local release evidence is refreshed | done | v1.1 verifier pass; v1.1 smoke pass; KITTI/ETH3D demo pass; v1.0 fallback verifier pass; targeted release tests `18 passed` |
| FS-7 | Final-stage operating boundary is documented | done | this file |
| FS-8 | Final model improvement start handoff exists | done | `handoff/DREAM3R_FINAL_MODEL_IMPROVEMENT_HANDOFF_20260610.md`; `handoff/DREAM3R_FINAL_MODEL_IMPROVEMENT_START_PROMPT_20260610.md` |
| FS-9 | Final review pass before submission | pending | reread report/PPT, check institution formatting, rerun verifier/tests after edits |

## Verification Before Any Final Submission

After any final-stage edit, run the smallest evidence set that proves the
release story is still intact:

```powershell
python -B code\dream3r\scripts\verify_v11_release.py --root .
python -B code\dream3r\scripts\verify_release_candidate.py --root .
python -B -m pytest --assert=plain code\dream3r\tests\test_release_candidate_architecture.py code\dream3r\tests\test_release_candidate_verifier.py code\dream3r\tests\test_release_v11_architecture.py code\dream3r\tests\test_release_v11_verifier.py code\dream3r\tests\test_release_v11_smoke_model.py code\dream3r\tests\test_v11_demo_script.py -q
git diff --check
```

For PDF/PPTX changes, also visually inspect the first and last report pages and
a representative set of PPT slides.

## Next-Agent Resume Prompt

```text
Dream3R is in final-stage review/polish. Start from TASK_SNAPSHOT.md, then
planning/DREAM3R_FINAL_STAGE_READINESS_PLAN_20260609.md. Keep v1.1.0 official,
v1.0-rc1 as fallback, Qwen diagnostic-only, and Foundation3R future/research
only. Do not reopen architecture search. Polish report/PPT/release docs and
rerun v1.1/v1.0 verifiers plus targeted release tests after edits.
```
