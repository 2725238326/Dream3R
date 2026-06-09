# 面向前馈式三维重建的状态条件化候选几何融合模型结题报告

日期：2026-06-09

## 摘要

本课题围绕前馈式三维重建中的多模型候选几何融合问题展开。现有 DUSt3R、MASt3R、Fast3R、VGGT、Spann3R 等模型能够从图像中直接预测三维几何或相关中间结果，但不同模型在室外车载、室内多视图、长序列和动态场景上的优势并不一致。Dream3R 的研究目标是在多个三维重建教师模型输出的候选几何之上，引入状态向量、记忆上下文、候选置信度和冲突分数，形成可验证的状态条件化融合模型。

结题阶段的当前交付模型为 Dream3R `v1.1.0`。它是一个状态条件化候选几何融合模型，而不是从图像直接输出完整三维几何的无候选基础模型。`v1.1.0` 采用场景域条件策略：KITTI 分支使用 `v1.0-rc1` 中已经稳定的有界 StatePrior 与残差修正路径，ETH3D 分支使用引入 VGGT-Omega 的状态条件融合路径。官方主指标为 KITTI / ETH3D 绝对相对误差 `0.1448 / 0.0570`，数值越小表示误差越低。

为了避免把教师模型优势误写成状态模块贡献，项目保留了正常状态、无状态和乱序状态三组对照。当前结果为：KITTI `0.1448 / 0.1553 / 0.1521`，ETH3D `0.0570 / 0.0583 / 0.0598`。两个数据域中正常状态均取得最低误差。项目同时记录了 Qwen 语义控制和 Foundation3R 无候选几何分支的负结果，二者均不进入当前正式模型。结题产物包括模型入口、验证脚本、演示脚本、真实候选缓存演示、发布说明、验证报告、产物清单、最终报告和答辩 PPT。

## 1. 研究问题

前馈式三维重建把传统多阶段三维视觉流程压缩到单次或少量前向推理中，降低了几何重建的系统复杂度。随着模型族增多，一个新的问题变得突出：不同模型生成的几何候选在不同场景中表现差异明显，单一模型很难稳定覆盖全部输入条件。一个模型可能在车载室外场景更稳，另一个模型可能在室内多视图场景更强。如果只报告最好的单一模型，系统无法解释不同候选之间的关系，也无法说明额外状态信息是否真正参与了有效决策。

Dream3R 把这个问题收束为候选几何库上的状态条件化融合。输入不再是一条孤立的模型输出，而是一组来自不同前馈式三维重建教师模型的点图、置信度和相关质量信号。模型同时读取 Dream state 或记忆上下文，并结合候选之间的冲突分数和场景域信息，输出最终点图、置信度和专家权重。

本课题重点回答三个问题：

1. 多个三维重建教师模型的输出能否整理成统一候选几何库。
2. 状态向量能否在候选选择或融合中产生可测量作用。
3. 当前系统的收益来自哪条证据链，哪些分支还不能作为正式模型结论。

## 2. 方法设计

Dream3R `v1.1.0` 的正式模型形态可以概括为：

```text
输入图像
-> 前馈式三维重建教师模型
-> 候选几何库 + 置信度
-> Dream state / memory context + conflict score
-> 场景域条件策略
   -> KITTI: v1.0-rc1 bounded StatePrior + residual
   -> ETH3D: VGGT-Omega-expanded state-conditioned fusion
-> final pointmap + confidence + expert weights
```

其中，候选几何库负责统一不同教师模型的输出；状态向量或记忆上下文提供跨帧、跨视图或跨候选的历史信息；冲突分数描述不同候选之间的分歧；场景域条件策略决定使用已经通过对照的分支。

### 2.1 KITTI 分支

KITTI 分支保留 `v1.0-rc1` 的稳定路径。该路径由有界 StatePrior 与残差修正构成，目标是在车载室外数据上保持稳定结果，避免把对 ETH3D 有利的 VGGT-Omega 分支强行用于全部场景。`v1.0-rc1` 同时作为 `v1.1.0` 的稳定回退版本保留。

### 2.2 ETH3D 分支

ETH3D 分支引入 VGGT-Omega 作为候选教师模型之一。前期 50 个 KITTI 窗口和 50 个 ETH3D 窗口的候选上限分析显示，VGGT-Omega 对 ETH3D 相近场景更有价值，因此 `v1.1.0` 只在 ETH3D 分支中使用 VGGT-Omega-expanded 状态条件融合路径。该策略保留了 KITTI 的稳定性，同时利用了 VGGT-Omega 在 ETH3D 上的候选几何优势。

### 2.3 状态对照

状态对照是当前模型成立的关键约束。若正常状态、无状态、乱序状态三组结果没有稳定差距，状态模块就只能作为结构设计存在，不能作为有效机制结论。因此，`v1.1.0` 的正式结果必须同时报告三组对照。只有正常状态优于无状态和乱序状态时，状态条件化融合才有足够证据进入正式模型口径。

## 3. 实现与发布包

当前正式入口为：

```text
dream3r.release_v11.build_dream3r_v11_release
```

主要脚本包括：

```text
code/dream3r/scripts/verify_v11_release.py
code/dream3r/scripts/smoke_v11_release_model.py
code/dream3r/scripts/run_dream3r_v11_demo.py
code/dream3r/scripts/run_dream3r_v11_cache_demo.py
code/dream3r/scripts/verify_release_candidate.py
```

发布文档包括：

```text
release/OFFICIAL_VERSION.md
release/COMPLETE_MODEL_V1_1.md
release/EFFECTIVE_ARCHITECTURE_V1_1.md
release/MODEL_CARD_V1_1.md
release/ARCHITECTURE_DIAGRAM_V1_1.md
release/VERIFY_REPORT.md
release/RUNBOOK.md
release/ARTIFACTS.json
release/STABLE_FALLBACK_V1_0_RC.md
```

轻量 demo 使用合成候选几何张量验证可调用运行契约。真实候选缓存 demo 在 BUAA-Server GPU1 上读取已有 SCF/VGGT-Omega 缓存，验证分支专家顺序、缓存字段适配和 JSON 输出。该 demo 是运行契约证据，不是新的 benchmark 结果。

## 4. 实验结果

本报告使用绝对相对误差作为主指标。数值越低，预测深度与真实深度的相对误差越低。

### 4.1 官方模型指标

| 模型版本 | KITTI AbsRel | ETH3D AbsRel | 说明 |
| --- | ---: | ---: | --- |
| `v1.0-rc1` stable fallback | 0.1448 | 0.1475 | 有界 StatePrior + residual |
| `v1.1.0` official | 0.1448 | 0.0570 | KITTI 使用 fallback，ETH3D 使用 VGGT-Omega-expanded SCF |

`v1.1.0` 在 KITTI 上保持 `v1.0-rc1` 的稳定结果，在 ETH3D 上取得明显下降。该结果支持场景域条件策略：不同场景使用已经通过状态对照的分支，而不是把同一教师模型或同一融合策略套到全部场景。

### 4.2 状态因果性对照

| 数据域 | 正常状态 | 无状态 | 乱序状态 |
| --- | ---: | ---: | ---: |
| KITTI | 0.1448 | 0.1553 | 0.1521 |
| ETH3D | 0.0570 | 0.0583 | 0.0598 |

两个数据域中，正常状态均取得最低误差。这说明状态信息在当前候选融合或分支选择中具有可观测贡献。该结论仍限于当前数据域、缓存规模和评估协议，不能外推为通用 SOTA 或长序列部署结论。

### 4.3 本地验证刷新

结题 pass 中重新运行了本地基础验证：

| 命令 | 结果 |
| --- | --- |
| `python -B code\dream3r\scripts\verify_v11_release.py --root .` | pass |
| `python -B code\dream3r\scripts\smoke_v11_release_model.py --output runs\release\v11_smoke\smoke_v11_release_model.json` | pass |
| `python -B code\dream3r\scripts\run_dream3r_v11_demo.py --domain kitti --output runs\release\v11_demo\demo_kitti.json` | pass |
| `python -B code\dream3r\scripts\run_dream3r_v11_demo.py --domain eth3d --output runs\release\v11_demo\demo_eth3d.json` | pass |
| `python -B code\dream3r\scripts\verify_release_candidate.py --root .` | pass |

此外，发布报告中保留了历史完整测试记录：本地 full suite `300 passed, 2 skipped`，服务器侧 v1.1/v1.0 验证、demo、release tests 和真实缓存 demo 均通过。

## 5. 未纳入官方模型的分支

### 5.1 Qwen 语义控制

Qwen3-VL-2B-Instruct 被测试为离线语义控制信号，目标是辅助路由、风险提示或教师模型调度。当前实验结果显示，它能生成稳定语义标签，但没有形成可靠几何收益。50 窗口 controller、留出组校准和 semantic Critic-prior gate 均没有通过几何控制门槛。因此，Qwen 在结题模型中只作为诊断记录保留，不进入 `v1.1.0` 正式推理图。

### 5.2 Foundation3R 与无候选几何分支

Foundation3R 是更接近无候选几何基础模型的研究尝试。当前代码已经具备前向契约、稠密教师缓存、训练入口、VGGT feature student 和状态调制实验，但多次 gate 显示几何精度和状态因果性不足。2026-06-08 的状态调制 gate 在 KITTI 有一定改善，但 ETH3D 上乱序状态更好，不能推广为正式模型。该分支保留为后续研究路线，下一步必须改变目标、数据规模或模型结构，而不是重复浅层解码器微调。

### 5.3 `v1.2-exp0`

`v1.2-exp0` 是受控 core bridge scaffold，用于测试把状态条件化候选融合更深入接入 core forward 的可能性。它通过了架构层测试，但没有通过真实缓存指标和状态对照，因此不替代 `v1.1.0`。

## 6. 局限性

当前结题交付有明确边界：

1. `v1.1.0` 仍依赖教师模型与候选缓存，不是 image-only proposal-free 3R foundation model。
2. 正式指标集中在 KITTI 和 ETH3D 两个数据域，尚未覆盖更大规模、多数据集、重复种子统计和公开排行榜协议。
3. 真实缓存 demo 证明运行契约，不等同于新的完整 benchmark rerun。
4. 状态信号在当前对照中有效，但更长序列、动态场景和跨域迁移仍需继续验证。
5. Qwen 语义信号尚未证明能改善几何，不能写成当前模型贡献。
6. Foundation3R 无候选几何路线仍处于研究阶段，不能作为正式结题模型。

这些局限不影响当前结题结论：Dream3R 已经形成一个可运行、可验证、边界清晰的状态条件化候选几何融合模型包。

## 7. 结论

截至结题阶段，Dream3R 已经从早期架构设想推进到 `v1.1.0` 官方模型包。当前模型的核心贡献是把多个前馈式三维重建教师模型的输出组织成候选几何库，并在此基础上用 Dream state、候选置信度、冲突分数和场景域信息进行状态条件化融合。`v1.1.0` 在 KITTI / ETH3D 上达到 `0.1448 / 0.0570`，并通过正常状态、无状态、乱序状态对照。

结题交付的重点不是宣称通用最优模型，而是形成一条可检查的研究链路：模型身份清楚，指标和对照可追溯，失败分支被诚实记录，验证入口和产物清单完整。后续工作应优先扩大 `v1.1.0` 的正式评测和消融，再在新的目标、数据和模型结构下重启 Foundation3R 无候选几何路线。

## 参考材料

[1] `release/OFFICIAL_VERSION.md`  
[2] `release/COMPLETE_MODEL_V1_1.md`  
[3] `release/EFFECTIVE_ARCHITECTURE_V1_1.md`  
[4] `release/MODEL_CARD_V1_1.md`  
[5] `release/VERIFY_REPORT.md`  
[6] `release/RUNBOOK.md`  
[7] `reports/opening/DREAM3R_OPENING_REPORT_STUDENT_FINAL.md`  
[8] `reports/midterm/DREAM3R_MIDTERM_REPORT_DRAFT.md`
