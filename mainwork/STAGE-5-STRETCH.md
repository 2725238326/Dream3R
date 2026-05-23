# STAGE 5 — Stretch Goals (Optional)

**Goal:** 在 Stage 1-4 闭合的真实 demo 基础上，按需扩展。每个子项独立可选，不强制全做。

**Prerequisite:** Stage 1-4 闭合。

**目的：** 朝向论文级别的完整性靠近。如果用户目标是 option 2（demo），到 Stage 4 就够了。

---

## 可选子任务（按价值排序）

### S1. 加更多 expert（CUT3R / Spann3R / VGGT）

**为什么：** 让 Composer 的"多 expert 路由"更有说服力（≥3 expert 才显得不像 toy）。

**Spec:**
- 每个 expert 一个独立 sub-task：CUT3R, Spann3R, VGGT
- 每个：下载 checkpoint → real adapter forward → smoke test
- 重新跑 Stage 3 的 router ablation（更多 expert）

**Estimated:** 2-3 天 / expert

---

### S2. Permanence 在动态场景的真实信号

**为什么：** 当前 Permanence 是 stub，KITTI 主要是静态场景。需要 KITTI tracking 子集或 Waymo 才有动态。

**Spec:**
- 用 KITTI tracking 数据（含 dynamic object bbox）
- 训练 Permanence：`dynamic_mask` 与真实 dynamic bbox 的 IoU
- 触发 CR-2: suppress static write of dynamic regions
- 评估：with-Permanence vs without 在动态 sequence 上的 drift

---

### S3. GaussianHead 主前向

**为什么：** v0.5 的 A7 axis。让最终输出是 3D Gaussian 而不只是 pointmap，朝 4DGS 方向迈一步。

**Spec:**
- Reference: Splatter-Image, MV-Splat
- 训练：用 KITTI image pair → 预测 3D Gaussians → render novel view → photometric loss
- 复杂度高，需要单独 1 周

**注意：** 这是主前向重构，不要直接合并，先做 branch。

---

### S4. ScanNet / ETH3D 评估

**为什么：** 论文级别需要至少 2 个 benchmark。ScanNet（室内）+ ETH3D（多视角立体）。

**Spec:**
- 下载数据集（先和用户确认下载位置 + 申请权限）
- 复用 Stage 1-4 的 dataloader 模板
- 跑同样的 ablation 表

---

### S5. tttLRM 真实 TTT 训练

**为什么：** A8 已 scaffold，但 `TTTStateUpdater` 是占位符。

**Spec:** 见 `planning/TTT_PLAN.md`
- 实现真 gradient step（self-supervised consistency loss）
- 训练 `StateUpdatePolicy` 做 sub-action 选择
- 长 sequence eval

---

## 闭合标准

每个子项独立闭合，独立写 cycle log + DEC：
- `cycles/CYCLE-YYYYMMDD-stage5-Sx.md`
- `decisions/DEC-YYYYMMDD-NNN-stage5-Sx-closure.md`

---

## 推荐组合（如果做论文）

- **最小论文配置：** Stage 1-4 + S1（≥3 expert）+ S4（ScanNet）
- **完整论文配置：** + S2（Permanence）+ S5（TTT）

S3（GaussianHead）建议作为单独 follow-up paper。
