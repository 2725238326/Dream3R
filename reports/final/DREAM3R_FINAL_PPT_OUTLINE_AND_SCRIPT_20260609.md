# Dream3R 结题答辩 PPT 页纲与讲稿

日期：2026-06-09

## 总体叙事

这套 PPT 面向结题答辩。主线是：研究问题来自前馈式三维重建模型分化；Dream3R 的当前可交付成果是 `v1.1.0` 状态条件化候选几何融合模型；模型有明确指标、状态对照、验证入口和局限边界；Qwen 与 Foundation3R 保留为诊断或后续研究，不进入当前正式模型。

推荐核心页数：14 页。

## Slide 1. 封面

标题：Dream3R：面向前馈式三维重建的状态条件化候选几何融合模型

副标题：结题报告 / Final defense

画面：左侧大标题，右侧三项结果：

```text
v1.1.0 official
KITTI / ETH3D: 0.1448 / 0.0570
state controls passed
```

讲稿：本次答辩汇报 Dream3R 的结题状态。当前正式交付是 `v1.1.0`，一个状态条件化候选几何融合模型。

## Slide 2. 研究问题

标题：前馈式 3R 模型变多后，关键问题变成如何使用候选几何。

要点：

```text
DUSt3R / MASt3R / Fast3R / VGGT / Spann3R 等模型各有优势
单一模型难以覆盖全部场景
候选之间需要可验证的融合协议
```

讲稿：前馈式 3R 已经从单一模型发展到模型族。Dream3R 关注的不是再堆一个孤立模型，而是如何把这些模型的候选几何放入统一、可验证的融合流程。

## Slide 3. 当前模型身份

标题：Dream3R v1.1.0 是状态条件化 proposal-fusion 模型。

画面：模型边界表。

| 是 | 不是 |
| --- | --- |
| 候选几何库上的状态条件化融合 | image-only proposal-free foundation model |
| 读取 teacher proposals、confidence、state、conflict | Qwen geometry model |
| 输出 pointmap、confidence、expert weights | universal SOTA claim |

讲稿：这个边界非常重要。结题模型有正式入口和指标，但它仍依赖候选几何库。无候选基础模型是后续研究线。

## Slide 4. 架构总览

标题：候选几何、状态和场景域共同决定最终点图。

画面：流程图。

```text
images
-> 3R proposal teachers
-> proposal bank + confidences
-> Dream state / memory context + conflict score
-> domain policy
-> final pointmap
```

讲稿：多个 teacher 先生成候选几何，Dream3R 在这些候选之上做状态条件化融合。状态对照是判断该设计是否成立的核心证据。

## Slide 5. v1.1.0 分支策略

标题：KITTI 保守稳定，ETH3D 使用 VGGT-Omega 分支。

| 数据域 | v1.1.0 分支 | 作用 |
| --- | --- | --- |
| KITTI | v1.0-rc1 bounded StatePrior + residual | 保持车载室外稳定性 |
| ETH3D | VGGT-Omega-expanded SCF | 利用室内/多视图强候选 |

讲稿：早期实验显示 VGGT-Omega 对 ETH3D 更有价值，但在 KITTI 上不适合作为通用替换。因此 v1.1.0 使用场景域条件策略。

## Slide 6. 主结果

标题：v1.1.0 保持 KITTI 稳定，并明显改善 ETH3D。

| 版本 | KITTI AbsRel | ETH3D AbsRel |
| --- | ---: | ---: |
| v1.0-rc1 fallback | 0.1448 | 0.1475 |
| v1.1.0 official | 0.1448 | 0.0570 |

讲稿：AbsRel 越低越好。v1.1 在 KITTI 上保持 fallback 结果，在 ETH3D 上通过 VGGT-Omega-expanded SCF 取得明显下降。

## Slide 7. 状态对照

标题：正常状态在两个数据域都优于无状态和乱序状态。

| 数据域 | 正常状态 | 无状态 | 乱序状态 |
| --- | ---: | ---: | ---: |
| KITTI | 0.1448 | 0.1553 | 0.1521 |
| ETH3D | 0.0570 | 0.0583 | 0.0598 |

讲稿：这是当前模型最关键的证据。若正常状态不优于控制组，状态模块就不能作为有效贡献。当前两个数据域都通过。

## Slide 8. VGGT-Omega 的角色

标题：VGGT-Omega 是 ETH3D 分支教师，不是 Dream3R 的全部。

要点：

```text
KITTI oracle gain: +1.18%, VGGT wins 2/50
ETH3D oracle gain: +18.35%, VGGT wins 35/50
v1.1.0 只在 ETH3D 分支正式使用 VGGT-Omega-expanded SCF
```

讲稿：VGGT-Omega 对 ETH3D 很有帮助，但 KITTI 证据不足。当前模型采用有边界的接入方式。

## Slide 9. 验证链路

标题：结题模型有固定入口、脚本和产物。

画面：验证命令表。

| 验证项 | 当前状态 |
| --- | --- |
| v1.1 verifier | pass |
| v1.1 smoke | pass |
| KITTI demo | pass |
| ETH3D demo | pass |
| v1.0 fallback verifier | pass |

讲稿：结题阶段重新跑了本地基础验证。真实候选缓存 demo 也已有服务器侧记录，用于证明 release API 能消费真实缓存。

## Slide 10. 没有纳入官方模型的分支

标题：负结果保留为边界证据，避免过度声明。

| 分支 | 当前结论 |
| --- | --- |
| Qwen semantic controller | diagnostic-only，当前无稳定几何增益 |
| Foundation3R proposal-free | 有训练入口，当前指标和状态因果性不足 |
| v1.2-exp0 core bridge | scaffold only，未通过正式指标门槛 |

讲稿：这些分支不是失败后删除，而是作为结题边界保留。它们说明为什么当前正式模型仍选择 proposal-fusion 路线。

## Slide 11. 产物清单

标题：交付物覆盖模型、验证、报告和答辩材料。

要点：

```text
release/OFFICIAL_VERSION.md
release/COMPLETE_MODEL_V1_1.md
release/VERIFY_REPORT.md
release/ARTIFACTS.json
reports/final/DREAM3R_FINAL_REPORT_20260609.md
reports/pptx/Dream3R_Final_Defense_20260609.pptx
```

讲稿：最终交付不是单个模型文件，而是一组可复查产物，包括版本说明、验证报告、运行脚本、报告和 PPT。

## Slide 12. 局限

标题：当前结果是清晰可交付模型，不是终点。

要点：

```text
仍依赖 teacher proposals 和缓存
只在 KITTI/ETH3D 形成正式结论
真实缓存 demo 不是完整 benchmark rerun
长序列、动态场景、跨域迁移仍需验证
```

讲稿：主动说明局限比扩大结论更重要。当前模型可交付，但还不是无候选几何基础模型。

## Slide 13. 后续工作

标题：下一步先扩充 v1.1 证据，再重启更难的无候选路线。

要点：

```text
更多窗口、数据域和随机种子
教师贡献消融与置信度/冲突校准
运行时间、显存和失败案例统计
Foundation3R 需要新目标、新数据或新结构
```

讲稿：短期重点是把 v1.1 从可交付模型包推进到论文级实验系统。Foundation3R 需要重新设计，而不是继续小改浅层 head。

## Slide 14. 结论

标题：Dream3R 已形成边界清楚、可运行、可验证的 v1.1.0 结题模型。

结论：

```text
1. 当前模型是 state-conditioned proposal-fusion 3R。
2. KITTI / ETH3D 指标为 0.1448 / 0.0570。
3. 状态对照在两个数据域通过。
4. Qwen 和 Foundation3R 保留为诊断/后续研究。
```

讲稿：本课题的阶段成果是把一个开放的架构探索收束成可交付模型包。它有明确边界、指标、对照和复现入口，可以作为后续论文实验和无候选模型研究的基础。
