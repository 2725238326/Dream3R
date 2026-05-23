# STAGE 3 — Composer Router Real Routing

**Goal:** 加入第 2 个真实 expert (Fast3R)，训练 Composer 学习根据 regime / capability 路由，证明多 expert + 路由优于单 expert。

**Prerequisite:** Stage 1, Stage 2 闭合。

**Success criteria:**
- 至少 2 个真实 expert 可用：MASt3R + Fast3R
- 在 KITTI 不同特征 sequence 上：
  - **with-router**：综合指标（depth abs-rel 平均）优于
  - **single-expert baseline**（永远用 MASt3R）和 **single-expert baseline**（永远用 Fast3R）
- 路由分布与 regime 类型有合理相关性（例如 sparse_view → MASt3R，feed_forward_manyview → Fast3R）

**Estimated time:** 1 周

---

## Tasks

### T3.1 — Fast3R real adapter

**Spec:**
- 下载 Fast3R checkpoint（HuggingFace `naver/Fast3R` 或论文官方 release）
  - `E:\Dream3R\downloads\fast3r/` → scp 到 `/hdd3/kykt26/checkpoints/fast3r/`
- 改 `composer_experts/fast3r_adapter.py` 为真实推理（参考 Stage 1 T1.3 的 MASt3R 模式）

**Verify:**
- `tests/test_fast3r_real.py` (server, gpu mark)
- 1 个 image pair smoke OK

---

### T3.2 — Regime ground truth labeling

**Spec:**
- 给 KITTI sequence 按特征自动打 regime 标签：
  - `outdoor_static`: 城市街道无大动态
  - `dynamic_scene`: KITTI tracking 中有车/人
  - `dense_sequential`: 长 sequence
  - `sparse_view`: 抽稀帧的子集
- 输出 `regime_labels.json` 每个 sequence 一组 6 维概率

**Verify:**
- 抽 10 个 sequence 人工 sanity check 标签合理

---

### T3.3 — Composer router supervised training

**Spec:**
- 监督信号：oracle expert（每个 sequence 离线计算每个 expert 的真实 metric，最优者作为 router 标签）
- 训练 `ComposerRouter`：
  - frozen backbone, frozen experts, frozen memory
  - 只训练 router 参数
  - cross-entropy loss against oracle labels
- preset `router_only`

**Verify:**
- TensorBoard：router accuracy 上升
- Checkpoint 保存

---

### T3.4 — Multi-expert ablation

**Spec:**
- `code/dream3r/scripts/eval_router_ablation.py`：
  - (a) router learned
  - (b) always MASt3R
  - (c) always Fast3R
  - (d) random routing
- 在多个 KITTI sequence 上跑，对比 metrics

**Verify (Stage 3 闭合):**
- (a) 综合指标优于 (b) 和 (c)
- 路由分布与 regime 标签相关性 > 0.3

**Closure:**
- `cycles/CYCLE-YYYYMMDD-stage3.md`
- `decisions/DEC-YYYYMMDD-NNN-stage3-composer-closure.md`

---

## 不做什么

- ❌ 不训练 backbone / experts / memory
- ❌ 不加超过 2 个 expert（其他 expert 推迟到 Stage 5）
- ❌ 不做 RL routing（用 supervised oracle）
