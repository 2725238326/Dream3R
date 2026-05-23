# STAGE 2 — Memory Module Real Training

**Goal:** 训练 `SpatialMemory` (NSA + AnchorBank) 模块，证明它在长序列上比"无 memory baseline"有定量优势。

**Prerequisite:** Stage 1 已闭合（DINOv3 + MASt3R + KITTI 端到端 work）。

**Success criteria:**
- 在 KITTI 长序列（≥50 windows）上：
  - **with-memory**：drift（accumulated pose error 或 cross-window pointmap consistency）显著低于
  - **without-memory baseline**（直接每个 window 独立调用 MASt3R）
- 训练曲线收敛（loss 下降，evaluation metric 提升）
- 195+ tests 仍然通过

**Estimated time:** 1 周

---

## Tasks

### T2.1 — Memory training data preparation

**Spec:**
- 从 KITTI 取长 sequence（每 sequence 50-100 帧）
- 滑窗切成 `sequence_length=8` 的训练样本（overlap 4）
- Ground truth: 用 LiDAR 投影 depth + GT pose 作为监督信号
- 新建 `code/dream3r/data/kitti_long.py`：`KITTILongSequenceDataset`

**Verify:**
- 单元测试：长 sequence 加载，shape 正确
- Server smoke：迭代 10 个 batch 不报错

---

### T2.2 — Memory loss design

**Spec:** 在已有 loss 之上加（或替换）：
- **Memory consistency loss**: `||state_t - encode(state_{t-1}, frame_t)||` 重构损失
- **Cross-window pointmap consistency**: 同一 3D 点在重叠 window 中应有相似坐标
- **Anchor reuse reward**: 鼓励高 confidence 帧的 anchor 被后续 retrieval 命中

修改 `code/dream3r/losses.py`（surgical change，不动现有 loss 接口）。

**Verify:**
- `tests/test_memory_loss.py`: 各 loss 项数值合理（>0, finite, gradient flows）

---

### T2.3 — Memory-only training run

**Spec:**
- Backbone (DINOv3) frozen
- MASt3R adapter frozen（只用它做 pointmap supervision target）
- Critic / Composer / Permanence frozen 或绕过
- **只训练 SpatialMemory + AnchorBank** 的参数
- 用 `train.py` 现有的训练循环，配置新 preset `memory_only`：
  - `freeze_backbone: True, freeze_experts: True, train_modules: ['memory']`
- 在 server GPU 0 跑 20 epoch，bs=4（长序列显存大）

**Verify:**
- TensorBoard：memory loss 单调下降
- Checkpoint 保存到 `/hdd3/kykt26/checkpoints/memory_only_v1/`

---

### T2.4 — Long-sequence evaluation: with-memory vs no-memory

**Spec:**
- 新建 `code/dream3r/scripts/eval_memory_ablation.py`：
  - 加载训好的 memory checkpoint
  - 在 KITTI 长 sequence（≥50 windows）上跑两次：
    - (a) memory ON
    - (b) memory bypass（state 不传递）
  - 计算 metrics: pointmap drift, depth abs-rel per window, ATE
  - 输出对比表 + plot

**Verify (Stage 2 闭合):**
- (a) 比 (b) 在 drift / abs-rel 上有可观察差距（至少 5% 改善）
- 实验记录到 `experiments/EXP-YYYYMMDD-stage2-memory-ablation.md`

**Closure artifacts:**
- `cycles/CYCLE-YYYYMMDD-stage2.md`
- `decisions/DEC-YYYYMMDD-NNN-stage2-memory-closure.md`
- `mainwork.md` Stage 2 → ✅

---

## 不做什么

- ❌ 不训练 backbone（保持 DINOv3 frozen）
- ❌ 不训练 expert（MASt3R frozen，只作为 oracle）
- ❌ 不训练 router / critic / permanence（这是 Stage 3-4 的任务）
- ❌ 不追求 SOTA，只追求 with-memory > without-memory
