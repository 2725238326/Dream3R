# Dream3R 研究接力提示词 — 方向 3.1: CUT3R + Spann3R Memory 机制研究

## 你是谁、你在做什么

你接手一个名为 Dream3R 的 3D 重建研究项目。Dream3R 的核心思想是：不做又一个新 backbone，而是设计一个**控制图架构（control-graph-as-architecture）**，把多个已有 3R 模型的优点融合到一起。

项目已经完成了：
- 架构设计文档（v0.2，6 个 delta）
- 服务器上的代码框架（21 个 Python 文件，能在 GPU 上跑通）
- 3 个 expert 真实推理（DepthAnything-V2 24.3ms / MASt3R 342ms / Test3R 341ms）
- 论文草稿 v1.3

**但用户指出了核心问题**：之前的工作太偏"搭框架调接口"，核心机制没有深入研究。现在需要转向**真正的研究探索**。

## 你现在的任务

**方向 3.1：研究 CUT3R 和 Spann3R 的 memory/state 机制，设计 Dream3R 的 C2 Memory 改进方案。**

### 为什么这是最优先

Dream3R 的 C2 Memory 模块当前实现（modules.py 的 MemorySSM）用 GRU + AnchorBank + NSA 三分支。但这个设计有两个问题：
1. GRU 作为 memory 核心太简单了，CUT3R 已经证明 **state token 与 frame token 的 cross-attention** 是更好的 memory 机制
2. AnchorBank + cosine top-k 太朴素了，Spann3R 的 **spatial memory + query-based retrieval** 更贴合 3R 场景

### 具体要做什么

**第一步：读代码（不改任何文件）**

1. 读 CUT3R 代码（服务器 `/hdd3/kykt26/code/cut3r/`）：
   - 找到 state token 的定义和初始化
   - 理解 state token 和 frame token 怎么做 cross-attention
   - state 怎么在帧之间持续更新（不丢失也不爆炸）
   - 输出什么（pointmap? state vector? 两者都有?）

2. 读 Spann3R 代码（服务器 `/hdd3/kykt26/code/spann3r/`）：
   - 找到 spatial memory 的数据结构
   - 理解 query feature 怎么生成（上一帧生成下一帧的 query?）
   - memory 怎么检索（attention? cosine? learned?）
   - 和 DUSt3R 的 decoder 怎么结合

3. 对比两者：
   - CUT3R 的 state 是隐式的（learned state tokens），Spann3R 的 memory 是显式的（3D points + features）
   - 两者能否结合？比如 state tokens 做隐式 memory + spatial points 做显式 anchor bank
   - 和 NSA 三分支的关系是什么（compressed branch ≈ CUT3R state? selected branch ≈ Spann3R retrieval?）

**第二步：写一份设计文档**

基于读码发现，写一份 `Dream/planning/MEMORY_V03_DESIGN_STUDY.md`，内容包括：
- CUT3R memory 机制的技术细节摘要
- Spann3R memory 机制的技术细节摘要
- 两者对比分析（隐式 vs 显式，优缺点）
- Dream3R C2 Memory v0.3 改进提案：怎么融合两者的优点
- 和 NSA 三分支的对接方案
- 风险和开放问题

**不要做什么**：
- 不改任何现有代码
- 不搭新框架
- 不做空壳 wrapper
- 不写论文——这阶段是研究探索

## 关键文件位置

```
本地（Windows E:\kykt\）：
  Dream/TASK_SNAPSHOT.md          — 最高权限入口，先读这个
  Dream/RESEARCH_STATE.md        — 研究状态
  Dream/specs/SPEC-20260506-004* — v0.2 架构 spec（Delta 3 = C2 Memory）
  Dream/planning/DREAM3R_V02_CODE_STRUCTURE.md — 代码结构规划

服务器（172.17.140.97, 用户 kykt26, SSH 别名 BUAA-Server）：
  /hdd3/kykt26/code/cut3r/       — CUT3R 代码（重点读 src/ 下的模型文件）
  /hdd3/kykt26/code/spann3r/     — Spann3R 代码（重点读 spann3r/model.py）
  /hdd3/kykt26/code/dream3r/     — Dream3R 当前代码（参考但不改）
  
  SSH 连接：ssh BUAA-Server（已配置密钥）
  conda env: dream3r / cut3r / spann3r（各自的环境）
```

## 工作规范

- 数据和模型放 /hdd3/，不放 home
- 不要同时占满所有 GPU
- 已有虚拟环境 kykt（Python 3.10），也有各 3R 模型自己的环境
- 这阶段是**研究探索**，不是工程交付。重要的是理解机制、提出融合方案，不是写跑通的代码

## 用户背景

用户是研究生，做 3R（3D Reconstruction）方向。项目目标是在 post-DUSt3R 时代提出一个新的架构级创新。用户关心的是**真正的技术深度**，不是框架搭建。之前的 agent 太注重"搭好跑通"而忽略了"为什么这么设计"。这次你要补上这个缺口。
