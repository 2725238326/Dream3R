# Dream3R 下一棒交接 — 2026-05-25

> 上一棒做了什么、你接下来做什么、不许做什么。读完就开干。

---

## 0. 你是谁、在哪

你是 Dream3R 项目的工程实施 agent。
工作目录：`E:\Dream3R`。
代码包：`E:\Dream3R\code\dream3r\`（本地编辑）/ `/hdd3/kykt26/code/dream3r/dream3r/`（服务器执行）。
服务器：`ssh BUAA-Server`，conda env `dream3r`（torch 2.5.1+cu121，4× TITAN RTX 24GB）。

**目标（用户原话）**：高强度推进第一版完全体模型 — 在 KITTI 上跑通端到端、输出真实 pointmap、完成一个核心创新的真实有效性对比。**不追求 SOTA，所有数字必须真实、可复现、可写入 closure 文档。**

---

## 1. 强制阅读顺序

1. `E:\Dream3R\CLAUDE.md` — 行为守则（Karpathy 4 原则）
2. `E:\Dream3R\mainwork.md` — 总图与 Stage 5 状态表（已更新到 2026-05-25）
3. `E:\Dream3R\mainwork\STAGE-4-CRITIC.md` — Stage 4 success criteria（你要让它真闭合）
4. `E:\Dream3R\cycles\CYCLE-20260525-stage4-router-regime-aware-gate.md` — **上一棒就做到这里**，详细写了为什么、改了什么、还差什么
5. `E:\Dream3R\specs\SPEC-20260522-001-dream3r-v05-axes.md` — v0.5 axis 边界（不要越线）
6. `E:\Dream3R\code\dream3r\RECENT_PROGRESS.md` — Tier 1/2/3 evidence 边界
7. 如果存在，读 `AGENTS.md` 与你将动到的子目录里的 `AGENTS.md`

---

## 2. 当前状态快照（2026-05-25）

| Stage | 状态 | 备注 |
|---|---|---|
| 1 MVR | ✅ done | DEC-20260523-004 |
| 2 Memory | ✅ done | DEC-20260523-005 |
| 3 Composer | ✅ done | DEC-20260523-006 |
| **4 Critic + Repair** | 🟡 **in_progress（你接手）** | 上一棒做完代码修复，未做服务器 retrain + ablation 复跑 |
| 5 Stretch | 🔲 optional | 看 `mainwork/STAGE-5-STRETCH.md` |

### Stage 4 卡在哪儿（上一棒发现并已定位）

旧 pipeline ablation 结果：

```text
full_pipeline_repair_on   = 0.2108669020
critic_on_repair_off      = 0.2253848203
both_off                  = 0.2253848203   <-- 与 critic_on_repair_off 一模一样
critic_changed_route_count = 0
t4_3                       = false
```

`critic_on_repair_off == both_off` 证明 critic 的 confidence 信号根本没让 routing 变化。Stage 4 不能这样闭合。

### 上一棒做了什么（仅本地、已通过 227 测试）

`ComposerRouter.confidence_gate` 从全局共享线性层升级为 regime-aware MLP，因为旧版的梯度在 per-regime 翻转监督下精确抵消，**架构上不可能学到 Stage 4 想要的行为**。修改三个文件：

- `code/dream3r/modules.py` — `confidence_gate = nn.Sequential(Linear(1+n_regimes, d_routing), GELU, Linear(d_routing, d_routing))`，forward 喂 `[critic_confidence, regime_probs]`，新增 `load_state_dict` 兼容旧 checkpoint
- `code/dream3r/scripts/train_router_only.py` — 联合训练 `loss_n + loss_h + loss_l`，删掉 conf-shift / 两阶段 / debug
- `code/dream3r/tests/test_router_only_training.py` — 新增测试断言 low-conf 翻转

本地直接证据（合成 4 序列）：

```text
pred no-conf:   [0, 0, 1, 1]   matches oracle y
pred conf-high: [0, 0, 1, 1]   matches oracle y
pred conf-low:  [1, 1, 0, 0]   per-regime flip 到 alt_y
```

详见 `cycles/CYCLE-20260525-stage4-router-regime-aware-gate.md`。

---

## 3. 第一阶段任务：把 Stage 4 真闭合（必须做完）

### Step A — 同步三个文件到服务器

```bash
scp E:\Dream3R\code\dream3r\modules.py                       BUAA-Server:/hdd3/kykt26/code/dream3r/dream3r/modules.py
scp E:\Dream3R\code\dream3r\scripts\train_router_only.py     BUAA-Server:/hdd3/kykt26/code/dream3r/dream3r/scripts/train_router_only.py
scp E:\Dream3R\code\dream3r\tests\test_router_only_training.py BUAA-Server:/hdd3/kykt26/code/dream3r/dream3r/tests/test_router_only_training.py
```

### Step B — 服务器先跑测试，确认同步无误

```bash
ssh BUAA-Server "cd /hdd3/kykt26/code/dream3r && conda run -n dream3r python -m pytest \
  dream3r/tests/test_router_only_training.py \
  dream3r/tests/test_router_ablation_eval.py \
  dream3r/tests/test_repair_pipeline_ablation_eval.py \
  dream3r/tests/test_repair_ablation_eval.py \
  dream3r/tests/test_spatial_memory.py -q"
```

期望：全过。任何 fail 都先停下来报告，不要硬冲。

### Step C — 重训 router_only_v1（新 gate 第一次拿到真梯度）

服务器侧的 `oracle_expert_labels.json` 已包含 `metrics` 字段，所以 `train_router_only.py` 会自动走 augmented 路径。

```bash
ssh BUAA-Server "cd /hdd3/kykt26/code/dream3r && conda run -n dream3r python -m dream3r.scripts.train_router_only \
  --preset router_only \
  --epochs 500 \
  --lr 0.05 \
  --batch-size 16 \
  --output-dir /hdd3/kykt26/checkpoints/router_only_v1"
```

读回 summary 检查：

```bash
ssh BUAA-Server "cat /hdd3/kykt26/checkpoints/router_only_v1/summary.json"
```

健康判据（必须全满足才往下走）：

- `augmented_with_critic_confidence == true`
- `final_accuracy >= 0.75`
- `high_conf_accuracy_vs_best >= 0.75`
- `low_conf_flip_rate_vs_no_conf > 0.0`

如果 `low_conf_flip_rate_vs_no_conf == 0.0`：
不要硬调 epochs/lr。先 `cat` checkpoint 验证 `confidence_gate.0.weight` 和 `confidence_gate.2.weight` 都存在（说明 regime-aware MLP 真的就位）。如果 key 是 `confidence_gate.weight`，说明同步没生效，回 Step A。

### Step D — 重跑 pipeline ablation

```bash
ssh BUAA-Server "cd /hdd3/kykt26/code/dream3r && conda run -n dream3r python -m dream3r.scripts.eval_repair_pipeline_ablation \
  --router-checkpoint /hdd3/kykt26/checkpoints/router_only_v1/latest.pt \
  --critic-checkpoint /hdd3/kykt26/checkpoints/critic_only_v1/latest.pt \
  --output /hdd3/kykt26/code/dream3r/runs/stage4_repair_pipeline_ablation/results.json"

ssh BUAA-Server "cat /hdd3/kykt26/code/dream3r/runs/stage4_repair_pipeline_ablation/results.json"
```

**Stage 4 闭合判据**（按 `mainwork/STAGE-4-CRITIC.md` T4.3 + `cycles/CYCLE-20260525-stage4-router-regime-aware-gate.md`）：

- `critic_changed_route_count > 0`
- `critic_on_repair_off != both_off`（数值不同，证明 critic 信号真的进了路由）
- `full_pipeline_repair_on <= critic_on_repair_off <= both_off`（abs-rel 越小越好；at least 一个不等号要严格成立）
- `t4_3 == true`

任意一条不满足，**停下来汇报**，不要造数字也不要降标准。常见不满足的原因和处理方式：

- `critic_changed_route_count == 0` 但 router summary 显示新 gate 学到了：说明真实 KITTI 上 critic 的 conf 落点不在训练时的 [low, high] 带内。先 `cat` 一段 ablation 中间日志看实际 conf 直方图。可能要扩大训练 conf 区间或换 conf 采样策略。
- `full_pipeline_repair_on > critic_on_repair_off`：repair 反而变差。先看是哪个 sequence 的哪个 action 拖累，不要直接把 repair 关掉敷衍。

### Step E — 写闭合文档

闭合判据全过后，必须写两份文档（参照 `cycles/CYCLE-20260523-stage3.md` 和 `decisions/DEC-20260523-006-stage3-composer-closure.md` 的格式）：

1. `cycles/CYCLE-YYYYMMDD-stage4-closure.md`：列同步、retrain summary 的具体数字、ablation 的具体数字、跑过哪些 test
2. `decisions/DEC-YYYYMMDD-NNN-stage4-critic-closure.md`：明确说"Close Stage 4 as complete"，列指标，列 implementation boundary（没改 model.py 主 forward / anchor_bank.py / nsa_attention.py），列 follow-up

然后更新 `E:\Dream3R\mainwork.md` 第 5 节状态表 Stage 4 改为 ✅ done。

---

## 4. Stage 4 闭合后：朝"完全体架构"推进

用户的"完全体"对照 `mainwork/STAGE-5-STRETCH.md` 的可选子任务。**不是全做**，按价值/可证伪性挑。建议执行序：

### S1（强烈推荐先做）— 把 Composer 撑满到 ≥3 个真实 expert

理由：Stage 3 闭合用的是 MASt3R + Fast3R 两人。一个"多 expert 路由"只有 2 个候选，论文/汇报上立不住。再加一个真实 expert 直接让"完全体"那一栏可信度起来。

候选优先级（基于 `code/dream3r/SOTA_FEATURE_MATRIX.md` 当前状态）：

1. **Spann3R**（已有 `spann3r_adapter` real-wired，server 上有 checkpoint，是已注册八专家之一）
2. **CUT3R**（adapter 是 `deterministic fallback`，需要 `load_checkpoint`）
3. **VGGT**（capability_card v2.2 已就绪；checkpoint 下载需用户授权）

每个 expert 的步骤：

1. 服务器上跑 `dream3r/tests/test_<expert>_integration.py`（如果 server-only 标志要打开看 README）
2. 用现有 `dream3r.scripts.build_oracle_expert_labels.py` 给 KITTI 的 8 个 sample sequence 算 abs-rel oracle（注意会改写 `oracle_expert_labels.json` 里的 `expert_order` 和 `metrics`，先 backup 旧的）
3. 用更多 expert 重跑 `dream3r.scripts.train_router_only` 与 `dream3r.scripts.eval_router_ablation`
4. 重新跑 Step D pipeline ablation

闭合判据：≥3 expert 路由表里 learned_router 仍优于 best single-expert baseline ≥ 5%。

### S4（次推荐）— ScanNet 或 ETH3D 二号数据集

理由：单 KITTI 论文撑不住。ScanNet 室内 + ETH3D 多视立体能让 Stage 1-4 的 pipeline 覆盖到 dense static 之外。

**前置**：必须先问用户是否同意下载（`mainwork.md` §4.4 触发条件）。

### S2（可选，非主线）— Permanence 真实信号

理由：当前 KITTI 几乎没有 dynamic object，Permanence 模块拿不到真信号，路径上是 stub。要做需要 KITTI tracking 子集或 Waymo。同样前置：先问用户。

### 其他子任务

- **S3 GaussianHead 主前向**：是分支级 refactor，不要直接合到 main forward。先写设计文档（`STREAM3R_RELATION.md` 或类似），再问用户是否开 branch。
- **S5 tttLRM 真 TTT 训练**：见 `planning/TTT_PLAN.md`，A8 已 scaffold，但实际 gradient step 没写。可以做，但优先级低于 S1。

---

## 5. 硬规则（违反就停下来问，不要自己决定）

来自 `E:\Dream3R\mainwork.md` §4 + `CLAUDE.md`：

1. **本地 Windows 不跑模型**。所有训练 / KITTI eval / pytest（除 schema-only）在 server。
2. **不下载 >500MB 文件**，先问用户。下载流程是：本地 `E:\Dream3R\downloads\` 暂存 → `scp` 到 server → 删本地。
3. **不动 `model.py` 主 forward / `anchor_bank.py` / `nsa_attention.py` / `bus.py`**（除非修 bug，且必须在 cycle log 里说明）。
4. **不为闭合 stage 造数字**。指标不达标就停下来汇报，列出失败原因和你的诊断。
5. **不回退已修 bug**：
    - `bus.hard_reset()` + `model.forward timestep==0` 跨 batch 修复
    - `n_regimes=6`（老 checkpoint n_regimes=5 不能直接 resume）
    - ComposerRouter `confidence_gate` 升级为 regime-aware MLP（**这是上一棒的修复，不要回退**）
6. **遇到模糊立刻问，不要瞎猜**。歧义触发：要在两个合理设计之间选、训练超 4 小时不收敛、新 fail 与当前任务无关。

---

## 6. 关键文件 / 路径速查

| 项 | 路径 |
|---|---|
| 总图 | `E:\Dream3R\mainwork.md` |
| Stage 4 spec | `E:\Dream3R\mainwork\STAGE-4-CRITIC.md` |
| Stage 5 stretch | `E:\Dream3R\mainwork\STAGE-5-STRETCH.md` |
| 上一棒工作记录 | `E:\Dream3R\cycles\CYCLE-20260525-stage4-router-regime-aware-gate.md` |
| v0.5 axes spec | `E:\Dream3R\specs\SPEC-20260522-001-dream3r-v05-axes.md` |
| Tier 1/2/3 evidence | `E:\Dream3R\code\dream3r\RECENT_PROGRESS.md` |
| 外部方法到 Dream3R 模块映射 | `E:\Dream3R\code\dream3r\SOTA_FEATURE_MATRIX.md` |
| 行为守则 | `E:\Dream3R\CLAUDE.md` |
| 训练入口 | `code/dream3r/train.py` |
| Router 训练 | `code/dream3r/scripts/train_router_only.py` |
| Router ablation | `code/dream3r/scripts/eval_router_ablation.py` |
| Repair pipeline ablation | `code/dream3r/scripts/eval_repair_pipeline_ablation.py` |
| Critic 训练 | `code/dream3r/scripts/train_critic_only.py` |
| KITTI eval | `code/dream3r/evaluate_real_sequence.py` |
| 服务器 KITTI 数据 | `/hdd3/kykt26/data/kitti/rectified` |
| 服务器 checkpoints | `/hdd3/kykt26/checkpoints/` |
| 服务器 runs | `/hdd3/kykt26/code/dream3r/runs/` |

---

## 7. 一句话总结

**先把 Stage 4 真闭合（同步 + retrain + ablation + 写两份闭合 doc），然后挑 S1（≥3 真 expert）继续推完全体。除此之外的事都先问用户。**
