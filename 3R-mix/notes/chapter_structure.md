# Chapter structure draft

Status: first-stage structure plan. This file guides `main.typ`; it is not final prose.

## 1. 引言：3R 方法的范式变化和综述范围

- 说明传统 SfM/MVS 与近期 feed-forward 3D reconstruction 的问题设置差异。
- 明确综述对象：以 DUSt3R 后的 3R / pointmap / visual geometry / streaming reconstruction 谱系为主。
- 限定 Dream 的位置：作为方法论和应用展望背景，不作为综述中心。
- 说明证据边界：论文声称、代码状态、本地流程、应用可行性分别标注。

## 2. 从传统几何流程到 pointmap 表示

- 传统流程：feature matching、pose estimation、triangulation、MVS/depth fusion、global optimization。
- DUSt3R 的重新组织：从图像直接预测稠密 3D pointmap 与 confidence，再派生下游几何量。
- pointmap 的优势：减少对显式相机先验的依赖，连接深度、匹配、位姿、点云。
- pointmap 的限制：尺度、全局一致性、多视角累积、动态干扰和长序列漂移仍需额外机制。

## 3. DUSt3R 及匹配增强分支

### 3.1 DUSt3R：pose-free pointmap reconstruction

- 介绍 DUSt3R 的输入输出、训练目标和全局对齐位置。
- 解释它为何成为后续模型的共同接口，而不是最终答案。

### 3.2 MASt3R：3D-grounded matching

- 写清 MASt3R 的贡献是 matching/descriptor grounding。
- 与 DUSt3R 的关系：增强匹配和 sparse global alignment，不是简单替代。

### 3.3 MASt3R-SfM：与传统 SfM 的接口

- 讨论 matching + retrieval + global SfM alignment。
- 放在验证/修正和工程桥接之间，避免把它写成纯 feed-forward 模型。

## 4. 多视角规模化与统一视觉几何模型

### 4.1 Fast3R 与 many-view forward pass

- 关注多图输入的规模化问题。
- 不把 “Fast” 简化为速度宣传，而是讨论 many-view regime fit。

### 4.2 MV-DUSt3R+ 与 sparse-view reconstruction

- 讨论 multi-view decoder、reference view selection、cross-reference fusion。
- 如写 NVS/Gaussian head，需要与 3DGS 输出章节互相引用。

### 4.3 VGGT 与统一 visual geometry prediction

- 介绍 camera、depth、pointmap、tracks 的统一输出。
- 与 DUSt3R/MASt3R/Fast3R 的比较必须基于论文或第三方评测，不写泛化结论。

### 4.4 MapAnything 与 metric feed-forward reconstruction

- 讨论可选几何输入和 metric scale 的重要性。
- 作为统一模型趋势，不替代逐模型比较。

### 4.5 Pow3R：利用 camera/scene priors

- 放在多视角与先验交界处。
- 说明先验输入提高约束，但也引入使用条件和先验冲突问题。

## 5. 视频深度、动态场景和 4D 重建

### 5.1 Align3R：单目深度和 3R 对齐

- 写 Depth Anything 类深度先验如何与跨帧几何一致性连接。
- 避免把深度估计结果直接等同于完整 3R。

### 5.2 MonST3R：motion-aware geometry

- 解释动态视频中静态点图假设的破裂。
- 说明 MonST3R 的 dynamic mask/confidence 用途和边界。

### 5.3 POMATO、D^2USt3R、Easi3R、RayMap3R

- POMATO：pointmap matching + temporal motion。
- D^2USt3R：4D pointmaps。
- Easi3R：training-free attention adaptation；需要在正文中单独说明它不是重新训练的动态 foundation model，而是从 DUSt3R 注意力中做 motion disentanglement。
- RayMap3R：RayMap static-scene bias and dynamic suppression。
- 本节重点是机制差异，不做未验证排行。
- 必备表：动态 3R 机制对照表，列出 MonST3R、POMATO、D^2USt3R、Easi3R、RayMap3R 的机制、输出和写作边界。

## 6. 长序列重建中的状态、记忆和缓存机制

### 6.1 CUT3R 与 recurrent persistent state

- recurrent state 是压缩状态，不是外部 memory store。

### 6.2 Spann3R 与 spatial memory

- 讨论 spatial memory 如何帮助全局 pointmap prediction。

### 6.3 Point3R、LONG3R、LoGeR、Mem3R

- Point3R：external spatial pointer memory。
- LONG3R：long-sequence memory gating/pruning。
- LoGeR：hybrid local/global memory。
- Mem3R：tracking 与 mapping memory 解耦。

### 6.4 STream3R、LongStream 与 causal/autoregressive route

- 区分 persistent state、session state、cache refresh。

### 6.5 OVGGT、PAS3R、FILT3R

- OVGGT：constant-budget cache compression and anchor protection。
- PAS3R：pose-adaptive update。
- FILT3R：latent-state Kalman filtering。
- 写作重点是“更新规则和预算管理”，不是泛泛“记忆增强”。

## 7. 测试时验证、修正和自适应

### 7.1 Test3R：test-time consistency learning

- 强调 Test3R 使用 triplet consistency / prompt tuning，和 TTT3R 的长序列 memory update 不同。

### 7.2 TTT3R：state update at test time

- 讨论测试时训练的计算代价和失败模式。

### 7.3 G-CUT3R 与 prior-guided reconstruction

- 讨论 camera/depth priors 如何进入 guided reconstruction。

### 7.4 MASt3R-SfM 与 classical consistency loop

- 与 Test3R/TTT3R 对比：SfM-stage consistency vs per-window consistency。

## 8. 面向应用的输出表示

### 8.1 Point cloud、depth、confidence 与 failure regions

- 说明最直接的可报告产物。

### 8.2 Mesh 与 Gaussian：从几何到可查看资产

- 3DGS/4DGS 是输出表示和渲染层，不是 3R 本身。

### 8.3 Splatt3R、InstantSplat、NoPoSplat

- pose-free/sparse-view Gaussian 路线。
- 应用段落要记录许可、依赖、权重和本地验证状态。

## 9. 方法比较表

表格列：

- model
- year
- input regime
- required camera/pose
- output representation
- dynamic support
- long-sequence support
- test-time verification/adaptation
- code/checkpoint/demo status
- application difficulty
- evidence label

## 10. 图示和应用路径

- Figure 1：3R 模型谱系图。必须是可读的路线图，而不是单列表格；DUSt3R 是根节点，Dream 不进入模型谱系。
- Figure 2：能力分类图。按 input regime、output representation、camera/prior、temporal handling、verification/adaptation 分层。
- Figure 3：应用落地图。从输入 regime 到几何预测、质量证据、输出资产和报告记录，明确“可运行不等于质量领先”。
- Figure 4：传统流程 vs pointmap 流程。服务引言，不使用论文截图，优先 Typst 原生绘制。
- Figure 5：长序列 memory primitive 区分图。区分 recurrent state、spatial/pointer memory、hybrid memory、cache/update policy。
- Figure 6：动态 3R 机制图。突出 MonST3R、POMATO、D^2USt3R、Easi3R、RayMap3R 的不同路径，避免把 Easi3R 淹没在列表里。

## 10.1 表格交付清单

- Table 1：文献相关性分层，支撑纳入/排除标准。
- Table 2：传统流程与 pointmap 路线对比。
- Table 3：支撑先验角色表，区分 depth、feature、tracking、segmentation。
- Table 4：动态 3R 机制对照表，必须包含 Easi3R。
- Table 5：长序列 memory primitive 对照表。
- Table 6：基础/多视角/统一几何模型比较。
- Table 7：视频/动态/长序列模型比较。
- Table 8：测试时验证、自适应与可视化输出比较。
- Table 9：应用证据矩阵，列出输出表示、质量证据、复现记录和许可证/依赖状态。

## 11. 经验总结与开放问题

- 从证据角度总结，而不是写口号。
- 开放问题：长序列漂移、动态/静态分离、先验冲突、测试时更新成本、Gaussian 输出质量、工程可复现性。
- Dream 经验只作为方法论：流程跑通不代表质量领先；模型选择需要 regime 与 evidence；结果要能转化为图、表、报告、失败样本。
