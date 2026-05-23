# STAGE 4 — Critic + Repair Real Signal

**Goal:** 让 Critic 在真实输出上检测几何不一致，触发 RepairExecutor 真正改善输出。

**Prerequisite:** Stage 1-3 闭合。

**Success criteria:**
- Critic 在 KITTI 上能识别"坏"的 expert 输出（confidence-weighted Sampson distance > threshold）
- Repair action 真实触发（不只是 logged）：
  - `local_rerun`: 实际重跑某 frame
  - `reroute_model`: 实际换 expert
  - `test3r_offpath_verify`: 实际跑 Test3R off-path 检查
- 在 hard sequence（高动态、低纹理、稀疏视角）上，with-repair 比 without-repair 在 abs-rel 上有改善

**Estimated time:** 1 周

---

## Tasks

### T4.1 — Critic supervised training

**Spec:**
- Ground truth: 用 KITTI velodyne 算 oracle abs-rel，per-window
  - 高 abs-rel → label = "conflict"
  - 低 abs-rel → label = "clean"
- 训练 `Critic`：
  - frozen 一切其他模块
  - 输入：evidence tokens + pointmap pair
  - 输出：conflict_score（regression to abs-rel） + repair_action（classification）

**Verify:**
- Critic conflict_score 与 oracle abs-rel 相关性 > 0.5
- Repair action accuracy > 50%（baseline = always action 0）

---

### T4.2 — Repair action 真实接通

**Spec:** 当前 `RepairExecutor` 已有 5 个 action 但都是 stub。改成真实执行：
- **Action 0 (no_repair)**: 已 OK
- **Action 1 (local_rerun)**: 实际把"坏" frame 用同一 expert 重跑（可能加 dropout/augmentation）
- **Action 2 (window_rerun)**: 整个 window 重跑
- **Action 3 (reroute_model)**: 真实换到另一个 expert（需要 Stage 3 多 expert 就绪）
- **Action 4 (test3r_offpath_verify)**: 已存在 stub，需接 Test3R real
- 修改 `code/dream3r/repair.py`

**Verify:**
- 各 action 单元测试：action 触发后输出与 baseline 不同（diff 非零）
- log 中能看到 action 真实生效的痕迹

---

### T4.3 — Hard sequence ablation

**Spec:**
- 选 5 个 hard KITTI sequence（高动态 / 低纹理）
- 对比：
  - (a) full pipeline（critic + repair on）
  - (b) critic on but repair off
  - (c) both off
- 计算 abs-rel, mean conflict_score

**Verify (Stage 4 闭合):**
- (a) > (b) > (c) 在 abs-rel 改善上
- 至少在 1 个 sequence 上 (a) 比 (c) 改善 > 5%

**Closure:**
- `cycles/CYCLE-YYYYMMDD-stage4.md`
- `decisions/DEC-YYYYMMDD-NNN-stage4-critic-closure.md`

---

## 不做什么

- ❌ 不训练 backbone / experts / memory（已 frozen）
- ❌ 不重写 ComposerRouter（Stage 3 已稳定）
- ❌ 不引入 RL，用 supervised oracle
