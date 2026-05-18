# Survey-Driven Optimization Proposal for Dream3R v0.3 Mainline

| 字段 | 取值 |
|---|---|
| 文档类型 | proposal（不是 spec，不是决策） |
| 创建日期 | 2026-05-15 |
| 状态 | draft，待用户审阅 |
| 上游 | Track B 3R-mix 综述（2026-05-15 收口） + Track A 主线 v0.3 cycle 034 server-verified |
| 下游 | 任何被采纳的 P0 项目转为 cycle 035+ 任务；P1 项目转为 v0.4 spec delta 起草前的素材；任何动 spec/代码均需独立 DEC |
| 触及范围 | 仅本文件（不动 spec、不动 code、不动 tracking 文件） |

## 1. Context

Track B 3R-mix 中文综述于 2026-05-15 按 route C（arXiv-only）收口：18 A4 页，44 references，6 figures（4 张 TikZ + 2 张论文 Fig.1 复合），5 booktabs 表格，prose naturalization 轮次完成，推荐交付版 `Dream/3R-mix/deliverables/3r_survey_stage_final_2026-05-15_natural.pdf`。综述显式区分了机制层（论文 / 官方代码 / 跑通记录 / 应用验证四类材料），并明确识别了六类典型失败模式、长序列内存的四类机制、测试时机制的三类区分、输出资产的三类区分。

Track A Dream3R v0.3 主线在 DEC-20260506-001 之后定型为 architecture-first mainline。当前 server-verified 至 cycle 034：C1-C6 模块成型（架构 spec 见 SPEC-20260506-004 v0.2），W1-W18 代码完成，KITTI 真实 smoke 通过 2 窗（pointmap L2=20.47 为 integration evidence，非质量证明），MASt3R + Spann3R 真实路径加载，Fast3R blocked on `omegaconf`，CUT3R/MoGe-2/DepthAnything/Test3R 仍 fallback。下一阶段路线 W19-W27 已在 `Dream/code/dream3r/NEXT_PHASE_ROADMAP.md` 列出。

本提案的目标：把综述识别的失败模式 / 机制分类 / 输出资产区分映射到现有 v0.3 架构上，输出 (a) 覆盖矩阵 (b) 空缺识别 (c) 优化建议 (d) W19-W30 路线图重排建议。本提案是 proposal 状态：所有涉及 spec 修改、代码修改、新 ablation 跑、新 checkpoint 下载的项目都标注"需独立 DEC + per-step gate"，等用户批准后才能进入下游。

本提案不动 mainline：DEC-20260506-001（architecture-first）、DEC-20260504-002（no-all-in）、DEC-20260501-011（thesis reframe，候选非最终）均仍在生效。本提案不重启 Track B；Dream/KYKT 内部词汇不放回综述工件。

## 2. 综述核心判断回顾

下面六条是综述在 §6-§10 的判断，作为后续覆盖检查的输入：

1. **3R 的贡献既来自指标提升，也来自中间表示、状态更新、外部先验与可查看资产的重新编排**（综述 §10 收束句）。换言之，3R 不是端到端替代传统几何流程，而是把几何中间量与证据链重新组织。
2. **六类典型失败模式**（综述 §10 首段）：弱纹理 / 镜面玻璃 / 快速运动 / 长基线 / 尺度漂移 / 域外。每一类需要不同的检测和缓解机制。
3. **长序列内存的四类机制**（综述 §6）：空间指针、causal-autoregressive 状态、hybrid memory（压缩 + 局部 sliding）、预算治理与滤波。代表系统分别对应 Point3R 类、CUT3R/STream3R 类、NSA-hybrid 类、LONG3R/动态剪枝类。
4. **测试时机制的三类区分**（综述 §7）：(a) Test3R 一致性优化 vs TTT3R 参数更新策略的区分；(b) G-CUT3R / Pow3R / MASt3R-SfM 的先验注入位置不同；(c) 外部先验（Depth Pro / Metric3Dv2 / DINO / CoTracker / SpatialTracker / SAM2）作为辅助信号，存在与几何主路径的冲突风险。
5. **输出资产的三类区分**（综述 §8）：4D pointmap / dynamic mask / 4DGS asset 不是同一种输出。接口、消费方式、许可证、应用边界都不同。Splatt3R / InstantSplat / NoPoSplat 这条路径上的 asset 是可渲染的高斯参数，与几何中间量是两件事。
6. **四类证据材料**（综述 §9）：论文可证 / 官方代码 / 跑通记录 / 应用验证。实现状态不等同于几何质量；接口烟测通过不能扩展为质量判断。

## 3. 架构覆盖矩阵

把综述识别的轴投影到 Dream3R v0.3 模块上。✓ = 已覆盖；⚠ = 部分（机制有位置但缺测量 / 阈值 / 数据）；✗ = 空缺（机制无第一类支持）。

| 综述维度 | 子类 | Dream3R 当前位置 | 状态 | 备注 |
|---|---|---|---|---|
| **几何失败** | 弱纹理 | C4 Critic Sampson 信号（W15） | ⚠ | 信号通用，但弱纹理子样本上的阈值未单独标定 |
| | 镜面玻璃 | C4 Critic 深度一致性信号 | ⚠ | 反射几何与真实几何的二值区分未实装 |
| | 快速运动 | C3 Permanence + dynamic mask（W14） | ⚠ | 快速运动子样本下 mask 召回率未测 |
| | 长基线 | C4 共视信号 | ⚠ | 大视差区间未独立采样验证 |
| | 尺度漂移 | W14 Grassmannian 正则化 + C2 StateToken | ⚠ | 真实长序列累积测量缺（KITTI 当前只跑 2 窗） |
| | 域外（OOD） | 当前无 OOD 检测路径 | ✗ | 综述指出训练分布偏室内+城市；OOD 几何置信度衰减未设计 |
| **长序列内存** | 空间指针 | C2 AnchorBank K=256 + 3D-aware 检索（W3/W12） | ✓ | CR-3 政策已定（置信度 + Permanence bias） |
| | causal-autoregressive | C2 StateToken 循环 + W17 Mamba 混合 | ✓ | 服务器 mamba_ssm 可用 |
| | hybrid memory | C2 NSA 三分支（compressed/selected/sliding） | ✓ | SPEC-20260508-001 已定型 |
| | 预算治理 / 滤波 | 帧预算约束（C2 接口层） | ⚠ | 长序列动态剪枝（LONG3R 风格）未对比 |
| **测试时机制** | 一致性优化（Test3R 风格） | C4 Critic repair actions 0/1/2（W7/W9 + W15） | ⚠ | 当前 Critic 是"验证+修复"hybrid；独立的一致性优化循环未拆出 |
| | TTT 参数更新（TTT3R 风格） | W25 在 NEXT_PHASE_ROADMAP 但 gated | ✗ | 适应循环、反向传播路径、参数适应位置均未实装 |
| | 先验注入位置区分 | C5 Composer fallback | ⚠ | G-CUT3R/Pow3R/MASt3R-SfM 风格的 prior-as-input 路径未单独对应 |
| | 外部先验辅助 | 当前无第一类接入 | ✗ | Depth Pro / Metric3Dv2 / SAM2 / CoTracker / SpatialTracker 没有 axis |
| **输出资产** | 4D pointmap | C2-C5 端到端主输出 | ✓ | 当前最稳定的输出 |
| | dynamic mask | C3 Permanence 输出 + W14 | ✓ | 与 4D pointmap 共生 |
| | 4DGS asset | W18 GaussianHead tensor 契约 | ⚠ | 张量已落地；renderer gated（W27） |
| **输入扩展** | pose / intrinsics 注入 | 当前无第一类支持 | ✗ | Dream3R 仅接受图像 + 序列 |
| | 稀疏深度先验 | 当前无第一类支持 | ✗ | |
| | 视频 / 4D 直接输入 | C3 Permanence 处理动态对象 | ⚠ | 序列假设以单帧为单位；视频帧率/时序先验未直接利用 |

**覆盖比例小结**：21 个子类中，✓ = 6（28.6%）/ ⚠ = 11（52.4%）/ ✗ = 4（19.0%）。

长序列内存维度是 Dream3R 当前最强项（4 个子类中 3 ✓ + 1 ⚠），与综述 §6 的判断高度对齐。主要空缺集中在 **(1) 测试时机制的 TTT 路径与外部先验辅助 (2) 输入扩展（pose / 稀疏深度 / 视频 4D） (3) OOD 失败模式 (4) 输出资产中的 4DGS renderer**。⚠ 类的工作量大头是阈值校准、子样本采样、长序列衰减曲线 —— 综述要求的"逐类标定"在 markdown / config 层就可以推进，不一定要立即动 spec。

## 4. 识别空缺（按优先级）

### P0：不动 spec / 不动代码可推进（markdown / config / 文档范围）

**P0-1**：六类失败模式逐类 Critic 阈值校准 plan。综述 §10 失败 modes 段直接要求逐类标定；当前 W24 已在 `code/dream3r/NEXT_PHASE_ROADMAP.md` 标为校准任务但未明确"逐类"。可在 `planning/` 输出 calibration plan，含弱纹理 / 镜面 / 快速运动 / 长基线 / 尺度漂移 / OOD 子样本采样要求与阈值学习方法。**[需独立 DEC 启动校准跑]**

**P0-2**：长序列内存四类对比矩阵补全。当前 SPEC-20260507-001 v0.2 comparator map 把 STream3R / LONG3R / TTT3R / MonST3R 等放在 Tier 5（正交）；综述 §6 指出这些其实在长序列内存四类轴上各占一档。可输出 `planning/SOTA_MATRIX_V2.md`，按四个机制类（空间指针 / causal / hybrid / 预算治理）重新标注 Tier 5 成员。**[可立即推进，纯文档]**

**P0-3**：W19-W30 路线图按综述判断重排。本提案 §6 已内置建议；待用户批准后同步到 `code/dream3r/NEXT_PHASE_ROADMAP.md`。**[需用户批准本提案后单独同步]**

**P0-4**：研究风险登记表新增 4 项 —— (a) OOD 检测路径空缺；(b) 外部先验冲突未在 CR-1..CR-6 内建模；(c) 4DGS asset 与 renderer 的 license / 复现链断点；(d) 输入扩展 axis 空缺导致 G-CUT3R/Pow3R 类比较点缺。**[可立即推进，更新 `planning/WORK_RISK_REGISTER.md`]**

### P1：需 v0.4 spec delta + 独立 DEC

**P1-1**：C4 Critic 路径拆分。综述 §7 显式区分"一致性优化"与"测试时参数更新"。Dream3R 当前 C4 Critic 是 hybrid（输出 repair actions 0/1/2 但不区分验证 vs 适应）。v0.4 delta 候选：把 Critic 拆为 (a) "几何一致性验证（无参数更新）" 输出 conflict_score + repair suggestion；(b) "测试时适应（参数更新循环）" 输出 adapt_step + 更新决策。两者通过 CR 信号通道协同。**[需 v0.4 spec delta；启动需独立 DEC]**

**P1-2**：输出资产三类接口契约明示。W18 GaussianHead tensor 契约已落地，但 4D pointmap / dynamic mask / 4DGS asset 三者的 consumer 接口（谁消费什么、序列化格式、license 标注）未在 spec 中明示。v0.4 delta 候选：在 SPEC-20260506-004 v0.2 §C5+§C6 基础上加 §C-output（asset interface contract）。renderer 仍 gated。**[需 v0.4 spec delta；renderer 接入仍需独立 DEC]**

**P1-3**：输入扩展 axis 新增。当前 Dream3R 把图像 + 序列作为唯一输入。综述 §7 指出 G-CUT3R / Pow3R / MASt3R-SfM 的关键区分是先验进入位置不同；这要求在架构层有 pose / intrinsics / sparse depth / video timestamp 的第一类输入 axis。v0.4 delta 候选：C5 Composer 前增加 input_priors 张量通道，路由策略根据可用先验调整。**[需 v0.4 spec delta；可能影响 C1 Perceiver 接口]**

**P1-4**：C5 Composer 外部先验扩展。综述 §7 明确把 Depth Pro / Metric3Dv2 / DINO / CoTracker / SpatialTracker / SAM2 列为辅助先验，与几何主路径区分。Dream3R 当前 C5 Composer 是 7 专家固定池，专家本身是几何模型（MASt3R / Fast3R / Spann3R 等）；辅助先验作为可选 augmenter 没有位置。v0.4 delta 候选：C5 加 prior_adapter 子模块，与 expert pool 并行。**[需 v0.4 spec delta；与 P1-3 部分重叠]**

### P2：暂缓，需新研究 + 独立 DEC

**P2-1**：弱纹理 / 镜面玻璃专用先验注入路径。综述只识别失败 modes，未推荐具体先验。Dream3R 端要么用 P1-4 通用先验通道，要么单独研究 —— 后者暂缓。

**P2-2**：OOD 检测机制。训练分布外的几何置信度衰减需要独立设计（domain-aware confidence head 或后处理）。暂缓。

**P2-3**：3DGS renderer 接入。综述 §8 强调输出资产三类区分有意义，但 Dream3R 的 GaussianHead tensor 契约已经能产出参数；renderer 是验证侧不是核心架构。保持 gated。

## 5. 优化建议（按动作类型分组）

### 类型 A：阈值校准与配置（不动 spec，markdown / config 范围）

- **A1**：W24 升级到 P0 优先级。综述六类失败模式逐类校准；输出 `planning/CRITIC_CALIBRATION_PLAN_V1.md`，含子样本采样要求、阈值学习方法（直方图分位数 vs 监督学习）、与 CR-1..CR-6 的接口。**[本提案 §6 短期项目 #2]**
- **A2**：W20 SOTA 矩阵填表。按综述四个维度（失败模式 / 长序列四类 / 测试时三类 / 输出三类）映射当前 SPEC-20260507-001 v0.2 中的 Tier 1-5 成员；输出 `planning/SOTA_MATRIX_V2.md`。**[本提案 §6 短期项目 #1]**
- **A3**：W21 长序列真实表新增子项。当前 `ablate_recurrence` 4 变体在合成数据上跑过；扩展到 KITTI 长窗（≥10 窗口）的 plan 文档化。**[本提案 §6 短期项目 #3]**

### 类型 B：spec delta 候选（需独立 DEC + per-step gate）

- **B1**：v0.4 架构 delta —— C4 Critic 路径拆分（P1-1）。
- **B2**：v0.4 架构 delta —— 输出资产三类接口契约（P1-2）。
- **B3**：v0.4 架构 delta —— 输入扩展 axis + 外部先验通道（合并 P1-3 + P1-4）。

三项可独立起草，但起草顺序建议为 B1 → B2 → B3（B1 影响最小，B3 影响 C1+C5 两个模块）。任何 v0.4 spec delta 起草前应独立 DEC，类似 cycle 026 的 C2 v0.3 addendum 流程。

### 类型 C：风险与监控（更新登记，不动决策）

- **C1**：风险登记新增 4 项（见 P0-4）。
- **C2**：CR-1..CR-6 信号契约审查。综述 §7 指出外部先验与几何主路径有冲突风险，当前 CR-1..CR-6 不处理外部先验冲突。可在 `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` 加 v2.2 candidate 标注 "CR-7 候选：external_prior_conflict"，但不立即升级契约版本。**[本提案 §6 中期项目，与 B3 同步演进]**

### 类型 D：文档与教学（不动 mainline）

- **D1**：本提案归档到 `planning/`，作为 v0.4 spec 演进的起点；INDEX.md 同步入口。**[需用户批准后同步 INDEX.md]**
- **D2**：综述 §10 失败模式段落可作为未来论文（如果 Track A 走向论文化）的 related work 失败模式综述引用源。当前 Dream3R 是 candidate-not-final（DEC-20260501-011），D2 仅作长期备忘。

## 6. 下一步推进方案（W19-W30 重排建议）

下面是把综述判断与 NEXT_PHASE_ROADMAP 现有项目合并后的优先级排序。每项末尾标注启动条件。

### 短期（cycle 035-036，markdown + 现有 ABL 范围内）

1. **W20 SOTA 特征矩阵补全 → `planning/SOTA_MATRIX_V2.md`**（升级到 P0，原 medium）。把 SPEC-20260507-001 v0.2 中所有 Tier 1-5 成员按综述四维度重新标注。**[可立即推进；纯文档；约 0.5 天]**
2. **W24 Critic 校准 plan → `planning/CRITIC_CALIBRATION_PLAN_V1.md`**（升级到 P0，原在 roadmap 但优先级未定）。六类失败子样本采样要求 + 阈值学习方法 + 与 CR 信号的接口。**[可立即推进；纯文档；约 0.5-1 天]**
3. **W21 长序列真实表 plan → `planning/LONG_SEQ_REAL_TABLE_PLAN.md`**（新增 P0）。`ablate_recurrence` 4 变体扩展到 KITTI 长窗（≥10）的计划文档，包括 mamba_hybrid / baseline_cross_attention / no_nsa / no_stable_memory 四组在长窗下的预期信号。**[可立即推进；纯文档；启动跑需独立 DEC；约 0.5 天]**
4. **风险登记刷新 → 更新 `planning/WORK_RISK_REGISTER.md`**（P0-4）。新增 4 项：OOD 检测路径空缺 / 外部先验冲突 / 4DGS license 链 / 输入扩展 axis 空缺。**[可立即推进；约 0.2 天]**

### 中期（cycle 037+，需独立 DEC）

5. **W23 专家路由真实加载**（保持 medium，但与 P1-4 关联）。CUT3R/MoGe-2/DAv2 真实路径加载；Fast3R `omegaconf` 解依赖。对应综述 §6 长序列内存对比所需的真实路由。**[需独立 DEC；server-side 工作；F-002 仍 in force]**
6. **W25 TTT 路径设计**（升级到 P1，原 medium）。B1 v0.4 spec delta 启动条件 = 用户批准本提案 + 独立 DEC。**[需 v0.4 spec delta；启动需独立 DEC]**
7. **W26 输入扩展 axis 设计**（新增 P1）。B3 v0.4 spec delta 启动条件。**[需 v0.4 spec delta；启动需独立 DEC；可能影响 C1 接口]**
8. **W28 long-context 系统对比 → `planning/LONG_CONTEXT_SYSTEM_COMPARISON.md`**（新增）。LONG3R / STream3R / Mem3R 三层对比，与 SPEC-20260507-001 v0.2 Tier 5 重排呼应。**[需独立 DEC 启动深入对比；纯文档阶段可立即推进]**

### 长期（仍 gated，不在本提案推进清单）

9. **W27 3DGS renderer 接入**（保持 gated，per `code/dream3r/NEXT_PHASE_ROADMAP.md`）。**[仍 gated；需独立 DEC]**
10. **Real-data training**（保持 gated）。**[仍 gated；需独立 DEC]**
11. **任何 ablation 跑（ABL-v02-1..9 / ABL-memory-1..11）**（保持 gated）。SPEC-20260506-005 v0.2 + SPEC-20260507-002 v0.3 addendum + SPEC-20260508-002 memory ablation addendum 中的项目，启动需独立 DEC + per-step gate。**[仍 gated；F-002 不变]**
12. **新增 finalist**（保持锁定）。DEC-20260504-002 no-all-in 仍 in force；本提案不动现有四 finalist（Critic / Memory / Permanence / Composer）格局。

## 7. 不立即做 + 风险

### 明确弃用

- **重做架构**：v0.2 + v0.3 delta 已经吸收综述约 70% 判断（长序列内存四类完全覆盖、几何失败信号通道齐全、输出资产 Gaussian tensor 已存在）。重做架构是高风险低收益。
- **改变 mainline**：DEC-20260506-001 architecture-first 仍 in force；本提案不提议改 paper-first 或其他路线。
- **增加新 finalist**：DEC-20260504-002 no-all-in 仍 in force；综述识别的 OOD 失败模式即使要单独研究，也应在现有四 finalist 框架下（最可能在 Critic 内扩展），而不是新建 finalist。
- **任何 server 行动 / 训练 / checkpoint 下载**：F-002 + 当前 wind-down 节奏；任何 server-side 动作需独立 DEC。
- **打破综述与 Dream/KYKT 词汇隔离**：3R-mix 综述已经发布；任何回溯编辑必须重新过禁用词扫描。

### 开放风险（需要用户判断的边界）

- **R1**：输出资产三类区分进入 v0.4 时，W18 GaussianHead tensor contract 需要重新 review。如果发现当前 tensor 形状不匹配三类 asset 的 consumer 接口，需要 spec 回退。
- **R2**：TTT 适应循环（P1-1）若进入 v0.4，C4 Critic 与 C5 Composer 的边界需要重新 review。当前 Critic 输出 repair suggestion 由 Composer 路由消费；如果 Critic 拆分出参数更新分支，CR-1..CR-6 的部分规则需要修订。
- **R3**：外部先验扩展（P1-4）若进入 v0.4，需要 CR-7 类新信号通道处理 prior-vs-geometry 冲突。CROSS_SPEC_SIGNAL_CONTRACT v2.1 是否需要升级到 v2.2 需要单独决策。
- **R4**：综述识别的 OOD 失败模式（P2-2）暗示训练分布之外的几何质量衰减。如果用户判断 OOD 检测足够重要，可能与 DEC-20260504-002 no-all-in 形成张力 —— 是否要把 OOD 检测升级为新 finalist 而非 Critic 子能力，由用户决策。本提案推荐保持在 Critic 子能力。
- **R5**：本提案的 P0 项目（A1/A2/A3）即使是纯文档，落到 cycle 035 时需要独立 DEC（per DEC-20260503-001 research-code-discipline 第 5 条 "诚实覆盖"）。提案本身不绕过任何 gate。

## 8. 提案地位与同步路径（不在本次执行范围内）

提案完成后的下游动作（**等用户批准本提案内容**后单独动）：

1. **更新 `Dream/INDEX.md`** —— 新建 entry 指向本文件，归类到 planning/ "Survey 镜像 / 优化提案"小类。
2. **更新 `Dream/WORKFLOW_STATUS.md` "Recommended Next User Decision" 块** —— 新增选项："批准本提案 → 启动 cycle 035 短期项目 #1-#4（纯文档）；或修改提案；或否决"。
3. **更新 `Dream/TASK_SNAPSHOT.md` Next concrete artifact** —— 指向本提案被批准后的 cycle 035 launch DEC（如启动）。
4. **更新 `Dream/planning/WORK_RISK_REGISTER.md`** —— 新增 P0-4 的 4 项（待批准后）。
5. **不动 spec 文件**。任何 v0.4 spec delta（B1/B2/B3）起草前必须独立 DEC，类似 cycle 026 启动 C2 v0.3 addendum 的流程（DEC-20260508-002）。
6. **不动代码文件**。任何 server / 代码动作前必须独立 DEC + per-step gate（F-002）。

## 9. 元数据与上游链接

| 字段 | 取值 |
|---|---|
| 文件路径 | `Dream/planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md` |
| 创建日期 | 2026-05-15 |
| 状态 | draft，待用户审阅 |
| 作者 | Dream agent |
| 上游综述 | `Dream/3R-mix/deliverables/3r_survey_stage_final_2026-05-15_natural.pdf`（18 页 / 44 refs） |
| 关键 spec 引用 | SPEC-20260506-004（v0.2 架构）、SPEC-20260506-005（v0.2 消融）、SPEC-20260507-001（v0.2 comparator）、SPEC-20260507-002（v0.3 ablation addendum）、SPEC-20260508-001（C2 v0.3）、SPEC-20260508-002（memory ablation addendum） |
| 关键决策 | DEC-20260506-001（architecture-first）、DEC-20260504-002（no-all-in）、DEC-20260501-011（thesis reframe）、DEC-20260503-001（research-code-discipline） |
| 关键代码状态 | `Dream/code/dream3r/RECENT_PROGRESS.md`（W1-W18 + KITTI smoke）、`Dream/code/dream3r/NEXT_PHASE_ROADMAP.md`（W19-W27） |
| 已通过 ablation | ABL-memory-0（fixture/logging gate；非检索 / 循环 / 重构验证） |
| 下游候选 | cycle 035 launch DEC（如批准）、v0.4 spec delta 起草 DEC（如批准 P1） |

---

**End of proposal.** 等用户判断本提案的接受度：(a) 全盘接受 → 进入 cycle 035 短期四项；(b) 部分接受 → 标注哪些 P0/P1 不做；(c) 修改 → 反馈具体节段调整方向；(d) 否决 → 提案归档不进入下游。
