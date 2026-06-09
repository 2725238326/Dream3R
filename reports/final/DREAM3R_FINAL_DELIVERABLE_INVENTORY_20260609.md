# Dream3R 结题产物清单

日期：2026-06-09

## 当前模型

```text
official model: Dream3R v1.1.0
model type: state-conditioned proposal-fusion 3R
stable fallback: v1.0-rc1
KITTI / ETH3D AbsRel: 0.1448 / 0.0570
state controls:
  KITTI normal/no-state/shuffle: 0.1448 / 0.1553 / 0.1521
  ETH3D normal/no-state/shuffle: 0.0570 / 0.0583 / 0.0598
```

## 模型与验证入口

| 产物 | 路径 | 状态 |
| --- | --- | --- |
| 官方版本说明 | `release/OFFICIAL_VERSION.md` | ready |
| 完整模型包说明 | `release/COMPLETE_MODEL_V1_1.md` | ready |
| 有效架构说明 | `release/EFFECTIVE_ARCHITECTURE_V1_1.md` | ready |
| 模型说明卡 | `release/MODEL_CARD_V1_1.md` | ready |
| 架构图说明 | `release/ARCHITECTURE_DIAGRAM_V1_1.md` | ready |
| 验证报告 | `release/VERIFY_REPORT.md` | refreshed evidence referenced |
| 运行手册 | `release/RUNBOOK.md` | ready |
| 产物 JSON 清单 | `release/ARTIFACTS.json` | updated in closing pass |
| v1.1 verifier | `code/dream3r/scripts/verify_v11_release.py` | local pass |
| v1.1 smoke | `code/dream3r/scripts/smoke_v11_release_model.py` | local pass |
| v1.1 branch demo | `code/dream3r/scripts/run_dream3r_v11_demo.py` | local pass |
| real cache demo | `code/dream3r/scripts/run_dream3r_v11_cache_demo.py` | server evidence exists |
| v1.0 fallback verifier | `code/dream3r/scripts/verify_release_candidate.py` | local pass |

## 报告与答辩材料

| 产物 | 路径 | 状态 |
| --- | --- | --- |
| 最终模型完善交接 | `handoff/DREAM3R_FINAL_MODEL_IMPROVEMENT_HANDOFF_20260610.md` | active next-agent handoff |
| 最终模型完善短提示词 | `handoff/DREAM3R_FINAL_MODEL_IMPROVEMENT_START_PROMPT_20260610.md` | active start prompt |
| 最后阶段推进计划 | `planning/DREAM3R_FINAL_STAGE_READINESS_PLAN_20260609.md` | final-stage boundary |
| 开题报告源稿 | `reports/opening/DREAM3R_OPENING_REPORT_STUDENT_FINAL.md` | historical source |
| 开题报告 PDF | `reports/pdf/Dream3R_开题报告_20260608.pdf` | rendered |
| 中期报告源稿 | `reports/midterm/DREAM3R_MIDTERM_REPORT_DRAFT.md` | historical source |
| 中期报告 PDF | `reports/pdf/Dream3R_中期报告_20260608.pdf` | rendered |
| 结题报告源稿 | `reports/final/DREAM3R_FINAL_REPORT_20260609.md` | final source |
| 结题报告 PDF | `reports/pdf/Dream3R_结题报告_20260609.pdf` | generated in closing pass |
| 结题 PPT 页纲与讲稿 | `reports/final/DREAM3R_FINAL_PPT_OUTLINE_AND_SCRIPT_20260609.md` | final source |
| 结题答辩 PPTX | `reports/pptx/Dream3R_Final_Defense_20260609.pptx` | generated in closing pass |
| 结题产物清单 | `reports/final/DREAM3R_FINAL_DELIVERABLE_INVENTORY_20260609.md` | final source |

## 本地验证刷新

| 命令 | 结果 |
| --- | --- |
| `python -B code\dream3r\scripts\verify_v11_release.py --root .` | pass |
| `python -B code\dream3r\scripts\smoke_v11_release_model.py --output runs\release\v11_smoke\smoke_v11_release_model.json` | pass |
| `python -B code\dream3r\scripts\run_dream3r_v11_demo.py --domain kitti --output runs\release\v11_demo\demo_kitti.json` | pass |
| `python -B code\dream3r\scripts\run_dream3r_v11_demo.py --domain eth3d --output runs\release\v11_demo\demo_eth3d.json` | pass |
| `python -B code\dream3r\scripts\verify_release_candidate.py --root .` | pass |

## 局限与非声明

当前交付不声明：

```text
proposal-free foundation 3R
image-only inference
Qwen geometry improvement
Foundation3R promotion
universal SOTA
full long-sequence streaming deployment
```

当前交付可以声明：

```text
Dream3R v1.1.0 is a runnable and verifiable state-conditioned proposal-fusion
3R model package with KITTI/ETH3D branch metrics, state controls, release
scripts, demo scripts, verification docs, and local/server evidence.
```
