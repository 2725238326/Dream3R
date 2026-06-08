# Dream3R Report And Midterm PPT Plan

Date: 2026-06-08
Status: execution plan

## Core Boundary

The opening report is a previous-stage artifact. Do not rewrite it as if it
already knew the current v1.1.0 result.

Use this boundary:

```text
Opening report:
  what the project proposed, why it was meaningful, what route was planned.

Midterm report:
  what was actually built and tested after opening, what passed, what failed,
  what the current honest model is, and what remains for final thesis work.

Midterm PPT:
  a compressed defense narrative: opening goal -> executed work -> current
  usable model -> evidence -> limits -> next plan.
```

## Existing Opening Materials

Use these as the previous-stage source of truth:

```text
planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md
planning/proposal_dream3r/DRAFT_INTERNAL_V1.md
planning/proposal_dream3r/OUTLINE_V1.md
planning/proposal_dream3r/PPT_MATERIAL_PLAN.md
planning/proposal_dream3r/deliverables/proposal_external_v1_2026-05-17.pdf
planning/proposal_dream3r/deliverables/ppt_work/proposal_dream3r_opening_report_final_text_only_cleaned.pptx
planning/proposal_dream3r/deliverables/ppt_work/proposal_dream3r_opening_report_final_script.md
```

Opening-report edits, if any, should be limited to formatting, typos, and
submission packaging. Do not insert v1.1 metrics, VGGT-Omega results, Qwen
negative gates, or Foundation3R failures into the opening report body.

## Midterm Report Positioning

The midterm report should be titled around current progress, not final success:

```text
面向前馈式三维重建的状态条件化多专家融合模型与验证平台中期报告
```

Safe one-sentence claim:

```text
本阶段围绕开题提出的长序列、校验、多模型组合和统一实验平台目标，
完成了从候选架构设计到可运行 Dream3R v1.1.0 状态条件化 proposal-fusion
模型包的阶段性实现，并形成了可复现的指标、对照、失败分支和后续路线。
```

Do not claim:

```text
proposal-free 3R foundation model already solved
Qwen improves geometry
VGGT-Omega is Dream3R itself
SOTA or full leaderboard result
```

## Midterm Report Structure

Recommended length: 20-30 pages.

```text
1. Introduction and opening-stage plan recap
2. Related work and opening-stage research basis
3. Architecture evolution after opening
4. Implemented Dream3R model line
5. Current official model package: v1.1.0
6. Experiments, controls, and evidence
7. Negative or non-promoted branches
8. Platform and engineering support
9. Current limitations
10. Next-stage plan toward final thesis
```

Section 1 should explicitly say the opening report belongs to the planning
stage. Section 3 should explain the evolution:

```text
opening candidate architecture
-> SCF / proposal-bank direction
-> v1.0-rc1 stable fallback
-> v1.1.0 domain-conditional proposal-fusion official package
-> v1.2-exp0 experimental core bridge, not official
```

## Evidence To Use

Current official model:

```text
release/OFFICIAL_VERSION.md
release/EFFECTIVE_ARCHITECTURE_V1_1.md
release/COMPLETE_MODEL_V1_1.md
release/MODEL_CARD_V1_1.md
release/ARCHITECTURE_DIAGRAM_V1_1.md
release/VERIFY_REPORT.md
release/ARTIFACTS.json
```

Metrics:

```text
Dream3R v1.1.0:
  KITTI / ETH3D AbsRel = 0.1448 / 0.0570
  metric direction = lower is better

Stable fallback v1.0-rc1:
  KITTI / ETH3D AbsRel = 0.1448 / 0.1475

State controls:
  KITTI state/no-state/shuffle = 0.1448 / 0.1553 / 0.1521
  ETH3D state/no-state/shuffle = 0.0570 / 0.0583 / 0.0598
```

Runtime evidence:

```text
runs/release/v11_demo/demo_kitti.json
runs/release/v11_demo/demo_eth3d.json
runs/release/v11_cache_demo/cache_demo_kitti.json
runs/release/v11_cache_demo/cache_demo_eth3d.json
```

Negative or bounded branches to report honestly:

```text
Qwen: diagnostic-only, no geometry promotion.
VGGT-Omega: real teacher, ETH3D-positive, not whole model.
Foundation3R/proposal-free: research lane, current gates not promotable.
v1.2-exp0: experimental core bridge, not v1.1 replacement.
```

## Midterm PPT Structure

Recommended length: 18-22 slides, 15-20 minutes.

```text
1. Cover
2. Opening-stage goal recap
3. Why 3R still needs state, verification, and multi-expert fusion
4. Work completed since opening
5. Architecture evolution roadmap
6. Current Dream3R v1.1.0 overview
7. v1.1 runtime architecture diagram
8. KITTI branch: v1.0-rc1 fallback path
9. ETH3D branch: VGGT-Omega-expanded SCF
10. Main result table
11. State/no-state/shuffle control table
12. Real proposal-cache runtime demo
13. What did not work: Qwen and proposal-free lanes
14. Platform / server / cache infrastructure
15. Code and reproducibility package
16. Current limitations
17. Next-stage plan
18. Summary
```

If time is tight, merge slides 8-9 and 14-15.

## PPT Visuals

Use these as primary visuals:

```text
release/ARCHITECTURE_DIAGRAM_V1_1.md
release/METHOD_FIGURE.md
release/RESULT_TABLE.md
release/VERIFY_REPORT.md
release/PRESENTATION_OUTLINE.md
```

Required figures/tables:

```text
1. Opening plan vs midterm status table
2. Architecture evolution timeline
3. v1.1 domain-conditional architecture diagram
4. KITTI/ETH3D result table
5. State/no-state/shuffle control table
6. Real-cache runtime evidence table
7. Negative-branch summary table
8. Next-stage Gantt or milestone table
```

## Writing Order

Do not start by polishing prose. Start with evidence selection.

```text
Step 1: Freeze the opening-stage material list.
Step 2: Draft the midterm report outline and evidence table.
Step 3: Fill sections 3-7 from release docs and verification artifacts.
Step 4: Fill platform/engineering section from existing opening platform text
        plus current server/cache/runtime chain.
Step 5: Draft the PPT from the report outline, not the other way around.
Step 6: Make one slide-by-slide speaker script.
Step 7: Render/preview PPT and remove overclaims.
```

## Immediate Execution Checklist

```text
1. Copy opening report deliverables into a "previous-stage reference" bundle.
2. Create midterm report markdown draft.
3. Create midterm PPT slide outline.
4. Convert release result tables into PPT-ready tables.
5. Generate or redraw the v1.1 architecture figure.
6. Write the first 18-slide PPT script.
7. Build PPTX only after the script is stable.
```

## Recommended Next Files To Create

```text
reports/midterm/DREAM3R_MIDTERM_REPORT_DRAFT.md
reports/midterm/DREAM3R_MIDTERM_PPT_OUTLINE.md
reports/midterm/DREAM3R_MIDTERM_PPT_SCRIPT.md
reports/midterm/assets/
```

Keep opening report deliverables under `planning/proposal_dream3r/`; do not
move or rewrite them into the midterm folder.
