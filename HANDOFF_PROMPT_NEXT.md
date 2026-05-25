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
3. `E:\Dream3R\cycles\CYCLE-20260525-stage4-closure.md` — Stage 4 闭合证据与限制
4. `E:\Dream3R\decisions\DEC-20260525-001-stage4-critic-closure.md` — Stage 4 closure decision
5. `E:\Dream3R\cycles\CYCLE-20260525-stage5-s1-three-expert.md` — Stage 5 S1 三专家 ablation 证据与限制
6. `E:\Dream3R\decisions\DEC-20260525-002-stage5-s1-three-expert-closure.md` — Stage 5 S1 closure decision
7. `E:\Dream3R\specs\SPEC-20260522-001-dream3r-v05-axes.md` — v0.5 axis 边界（不要越线）
8. `E:\Dream3R\code\dream3r\RECENT_PROGRESS.md` — Tier 1/2/3 evidence 边界
9. 如果存在，读 `AGENTS.md` 与你将动到的子目录里的 `AGENTS.md`

---

## 2. 当前状态快照（2026-05-25）

| Stage | 状态 | 备注 |
|---|---|---|
| 1 MVR | ✅ done | DEC-20260523-004 |
| 2 Memory | ✅ done | DEC-20260523-005 |
| 3 Composer | ✅ done | DEC-20260523-006 |
| **4 Critic + Repair** | ✅ done | DEC-20260525-001 |
| 5 Stretch | 🔶 partial (S1 strengthened) | DEC-20260525-002；看 `mainwork/STAGE-5-STRETCH.md` |

### Stage 4 已闭合

最终服务器证据：

```text
full_pipeline_repair_on   = 0.2108669020
critic_on_repair_off      = 0.2253848203
both_off                  = 0.2253848203
critic_changed_route_count = 1
repair_changed_output_count = 2
t4_3                       = true
```

重要限制：`critic_on_repair_off == both_off`，所以不要把 Stage 4 写成 strict critic-only aggregate gain。闭合依据是用户给定的核心门槛 `critic_changed_route_count > 0 && t4_3 == true`，以及 full pipeline 的真实 repair gain。

详见 `cycles/CYCLE-20260525-stage4-closure.md` 和 `decisions/DEC-20260525-001-stage4-critic-closure.md`。

---

## 3. Stage 5 S1 已强化闭合

S1 把 learned router 从两专家（MASt3R + Fast3R）推进到了三候选真实专家（Fast3R + MASt3R + Spann3R），并完成真实 KITTI ablation。随后补上 `regime_stats/features` router ablation，使 learned router 实际选择三专家并匹配 oracle routes。

基础三专家证据：

```text
expert_order: [fast3r, mast3r, spann3r]
oracle_counts: mast3r=8, fast3r=2, spann3r=2
learned_router: 0.1722621613
best_single_expert: mast3r
always_mast3r: 0.1906146836
relative_improvement_vs_best_single: 0.0962807369
stage5_s1: true
```

基础 6D-router 限制（保留为诊断，不是最终强化结果）：

```text
learned_expert_counts: fast3r=3, mast3r=9, spann3r=0
oracle_expert_counts: fast3r=2, mast3r=8, spann3r=2
learned_uses_ge_3_experts: false
```

强化服务器证据：

```text
router checkpoint: /hdd3/kykt26/checkpoints/router_stage5_s1_regime_stats_v1/latest.pt
router ablation: /hdd3/kykt26/code/dream3r/runs/stage5_s1_router_ablation/results_regime_stats.json
feature_mode: regime_stats
stat_source: features
learned_router: 0.1636828103
oracle_router: 0.1636828103
always_mast3r: 0.1906146836
relative_improvement_vs_best_single: 0.1412896043
learned_expert_counts: fast3r=2, mast3r=8, spann3r=2
oracle_expert_counts: fast3r=2, mast3r=8, spann3r=2
learned_uses_ge_3_experts: true
stage5_s1: true
```

准确说法：三真实专家候选、三专家 oracle、feature-augmented learned router 三者都成立；在 12-window KITTI closure set 上 learned router 与 oracle route 一致，相对 best single expert 改善 14.13%。不要把它写成 SOTA、跨数据集泛化或 held-out result。

## 3. 下一阶段任务：审阅强化闭合，再开 Stage 5 剩余项

第一优先级：审阅 `regime_stats/features` 这次强化闭合是否符合真实证据边界。

执行顺序：

1. 读 `cycles/CYCLE-20260525-stage5-s1-three-expert.md` 的 Richer Router Feature Addendum。
2. 核验 server artifact：`results_regime_stats.json` 与 `router_stage5_s1_regime_stats_v1/summary.json`。
3. 确认 feature source 是 `stage3_regime_labels/regime_labels.json` 的 `features`，不是 oracle metrics。
4. 如果审阅通过，再推进下一个 Stage 5 stretch：real-data ablation table、second-dataset plan，或 CUT3R/VGGT real-checkpoint authorization path。

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
4. 重跑 repair pipeline ablation

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
| Stage 4 closure | `E:\Dream3R\cycles\CYCLE-20260525-stage4-closure.md` |
| Stage 4 诊断记录 | `E:\Dream3R\cycles\CYCLE-20260525-stage4-router-regime-aware-gate.md` |
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

**Stage 4 与 Stage 5 S1 strengthened closure 已闭合；下一棒先审阅 `regime_stats/features` 证据边界，再推进 Stage 5 剩余 stretch。**
