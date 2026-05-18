# Dream3R 项目交接提示词

请将以下内容粘贴到新对话的第一条消息中：

---

我们在做一个叫 Dream3R 的 3D 重建（3R）研究项目。我需要先给你交代背景，然后重新描述我对几个核心模块的思路。请你先读完背景，等我说完再开始工作。

## 项目背景

Dream3R 是一个"控制图架构"（control-graph-as-architecture），核心思想是：3R 领域不缺更强的 backbone，缺的是一个控制层，决定什么时候验证、什么时候切换模型、什么时候拒绝写入静态地图。

### 架构设计（已完成，在 Dream/specs/ 下）

- **SPEC-20260506-001** — 架构 spec v0.1（1821 行），定义了 6 个计算核心：
  - C1 Perceiver：ViT backbone，复用 DUSt3R/MASt3R 的预训练权重
  - C2 Memory：SSM/Mamba 循环状态控制器，管理长序列记忆
  - C3 Permanence：Slot Attention，追踪物体身份，区分动态/静态
  - C4 Critic：小 transformer 头，验证几何一致性，决定修复动作
  - C5 Composer：参数为零的路由器，根据场景类型选模型
  - C6 Bus：跨模块信号总线 + CR-1..CR-6 冲突解决 gates
- **SPEC-20260506-002** — 消融计划（10 个实验，3 个优先级）
- **SPEC-20260506-003** — 对比模型地图（14+ 模型对比）
- **论文初稿** — literature/PAPER_DRAFT_V1.md

### 代码（已完成第一版，在 Dream/code/dream3r/ 下）

PyTorch 实现，已在服务器 GPU 上通过 smoke test 和 DTU 训练：
- bus.py — 总线 + CR gates
- modules.py — C1-C5 五个模块（v0.2，bus 承重版）
- model.py — 主模型，编排 bus tick 顺序
- losses.py — 多损失训练目标
- config.py — YAML 配置 + preset
- train.py — DDP 多卡训练（已验证 2 卡）
- data_dtu.py — DTU 数据集加载

### 服务器环境

- IP: 172.17.140.97, 用户: kykt26
- GPU: 4 x TITAN RTX 24GB（训练用 2-3 卡，给同学留空间）
- conda env: dream3r (torch 2.5.1+cu121, mamba-ssm 2.2.4)
- 数据: DTU (539MB, 22 scans) + KITTI (196GB)
- 已有模型代码: dust3r-main, mast3r, monst3r, spann3r, fast3r, cut3r, Test3R
- 已有权重: DUSt3R_ViTLarge, MASt3R_ViTLarge, spann3r.pth
- 代码和数据都在 /hdd3/kykt26/ 下，home 目录只放虚拟环境

### 发现的核心问题

代码结构上有 bus、CR gates、5 个模块，但实际上：
1. 所有模块输入都是随机特征，不是真实的 3R 输出
2. Critic 没有真正验证几何（没有真实的重投影误差）
3. Memory 在 4 帧 DTU 上学不到有意义的记忆策略
4. Permanence 在全静态场景上没有动态物体可分
5. Composer 用 uniform 表做路由，没有真正的模型选择
6. **创新点全在 spec 里写着，但代码里是空壳**

### 我接下来要做的

我要重新描述 Composer、Critic、Memory、Permanence 这几个模块应该怎么工作，以及它们和现有 3R 模型（DUSt3R/MASt3R/MonST3R/Spann3R）之间的关系。之前的思路可能需要大幅调整。

**请你先不要开始写代码或做设计。等我把新思路说完，我们再一起理清楚方向。**

### 关键文件路径（需要时再读）

- 架构 spec: Dream/specs/SPEC-20260506-001-dream3r-architecture.md
- 消融计划: Dream/specs/SPEC-20260506-002-dream3r-ablation-plan.md
- 代码: Dream/code/dream3r/
- 推进计划: Dream/code/dream3r/PLAN.md
- 任务快照: Dream/TASK_SNAPSHOT.md
- 服务器规则: 参见上面的服务器环境部分

---
