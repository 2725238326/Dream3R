# Dream3R 实现推进计划

日期：2026-05-10
状态：Cycle 033 架构推进中（W1-W10 主路径已大幅落地，W12/W14 已开始落地）

## 当前基线

- 代码：bus + 5 模块 + losses + smoke test 已通过 GPU 验证；Cycle 033 已补 temporal bus、SpatialMemory payload、NSA 几何稀疏、sequence training、loss/metrics/profiler、MASt3R + Spann3R real adapters、W12 3D-aware retrieval、W14 drift regularizer
- 环境：dream3r conda env，版本全部对齐 ✓
- 数据：服务器已有 DTU (539MB, 15 scenes) + KITTI (196GB)
- 硬件：4 x TITAN RTX 24GB，训练用 2-3 卡

### 服务器环境（已确认，干净）

```
conda env:      dream3r (Python 3.10)
torch:          2.5.1+cu121
causal-conv1d:  1.6.1
mamba-ssm:      2.2.4
transformers:   4.46.0
timm:           1.0.26
einops:         0.8.2
scipy:          1.15.3
tensorboardX:   2.6.5
GPU:            4 x NVIDIA TITAN RTX (24GB each)
CUDA (driver):  13.0
CUDA (PyTorch): 12.1
conda gcc:      12.4 (for CUDA extension compilation)
```

### 代码文件清单

```
Dream/code/dream3r/
├── __init__.py      — 包入口
├── bus.py           — C6 Memory Bus + CR-1..CR-6 gates (~130 行)
├── modules.py       — C1-C5 五个计算核心 (~280 行)
├── model.py         — Dream3R 主模型 + bus tick 编排 (~150 行)
├── losses.py        — 多损失训练目标 L_total (~90 行)
├── smoke_test.py    — 端到端验证脚本 (~100 行)
└── PLAN.md          — 本文件
```

---

## 阶段一：代码打磨（主线）

### 1.1 模块级代码审查和重构

- [x] Perceiver (C1)：接入 timm ViT-Base backbone（可开关）；pointmap/confidence/evidence 三个 head 改成多层 MLP
- [x] Memory (C2)：输入改为 concat(perception_summary, evidence_flat)；suppress_mask 维度修正；LayerNorm 加入
- [x] Memory (C2)：AnchorBank 支持 3D-aware retrieval；StateTokenRecurrence 接入 Grassmannian drift regularizer
- [x] Permanence (C3)：对照 Locatello 2020 重写 Slot Attention（q 来自 slots，k/v 来自 inputs，softmax over slots 竞争）；slot 初始化改为 mu+sigma 采样
- [x] Critic (C4)：改为 2-layer TransformerEncoder over 17 evidence tokens（不再 flatten 成单 token）
- [x] Bus (C6)：model.py 加入 read() 调用（Critic 读 capability_match 和 latent_drift_proxy），contract_log 非空
- [x] Composer (C5)：ExpertRegistry 能抽取 3R 方法 profile，MASt3R/Spann3R 真实 checkpoint path 接入，dispatch metadata 已记录
- [ ] Composer (C5)：regime classifier 接入真实输入 metadata（当前训练主路仍用传入 regime）
- [ ] Memory (C2)：GRU → Mamba SSM 替换（mamba-ssm 2.2.4 已装好，待代码层面切换）

### 1.2 训练基础设施

- [x] YAML config 系统（管理所有超参数；preset: small / small_vit / base）
- [x] DDP 多卡训练封装（2-3 卡，CUDA_VISIBLE_DEVICES 控制）
- [x] checkpoint 保存
- [x] tensorboard logging
- [x] 混合精度训练 (torch.amp)
- [x] gradient checkpointing 开关（长序列省显存）
- [ ] checkpoint resume 路径实测

### 1.3 代码质量

- [ ] 统一 tensor shape 注释（每个函数标清 [B, N, D] 的含义）
- [ ] 边界情况处理（第一个 window 没有 t-1 状态、空 anchor set 等）
- [x] 单元测试（bus / NSA / AnchorBank / Composer / SpatialMemory / sequence / permanence / critic / loss / eval / profiler / expert integration）

---

## 阶段二：数据准备

- [ ] DTU DataLoader（images + cams + pair.txt → frame pairs → ViT patches）
- [ ] GT pointmap 生成（从 cam 参数 + depth 计算）
- [ ] Critic 伪标签（DUSt3R 跑 DTU → reprojection error 阈值 → conflict label）
- [ ] KITTI DataLoader（连续帧 window-based 加载；后做）

## 阶段三：Backbone 接入

- [ ] 先 timm ViT-Base 跑通训练流程
- [ ] 后接 DUSt3R 预训练权重（/hdd3/kykt26/models/DUSt3R_ViTLarge_BaseDecoder_512_dpt.pth）
- [x] MASt3R adapter 真实 checkpoint 加载与 forward contract
- [x] Spann3R adapter 真实 checkpoint 加载、forward contract 与 Router dispatch
- [ ] Fast3R adapter 真实 forward：repo/checkpoint 已存在，当前 dream3r env 缺 `omegaconf`
- [ ] CUT3R adapter 真实 forward：repo/checkpoint 已存在，待接入

## 阶段四：第一轮训练（小规模验证）

- [ ] DTU 15 scenes, 2 卡 DDP, 只求跑通
- [ ] 验证 Loss 收敛 + Bus 信号流转 + CR gate 触发

## 阶段五：Tier 1 消融实验

- [ ] ABL-1: Bus 有没有用
- [ ] ABL-2: 混合基座对不对
- [ ] ABL-3: 梯度隔离

## 阶段六：扩大规模

- [ ] 加数据 + 换大 backbone + 出论文数字
