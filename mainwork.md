# Dream3R Mainwork — Architecture Implementation Roadmap

**Version:** 1.0  
**Date:** 2026-05-23  
**Author:** Cascade (handoff to next agent)  
**Status:** Active

---

## 0. 假设与目标（请用户确认）

**默认目标：工作 demo（option 2）** — 在 KITTI 上跑通端到端，输出真实 pointmap，并对一个核心创新点（NSA memory 或 Composer routing）做有效性对比。**不追求 SOTA，追求每个数字真实**。

如目标变化：
- 选 option 1（顶会）：所有 stage 完成后还需加 ScanNet/ETH3D + 完整消融 + baseline 复现
- 选 option 3（PoC）：只做 Stage 1 + Stage 2 即可
- 选 option 4（提案级）：只做 Stage 1，定性结果即可

---

## 1. 当前现实诊断

**v0.5 架构是空壳。** 数据流：
```
随机 tensor → Linear projection → Memory/Critic/Composer (无意义) 
            → 8 个 Expert (全部 fallback) → 假 pointmap → 形状测试通过
```

**v0.5 已闭合的工程价值（不要丢弃）：**
- 模块接口定义清晰（contracts.py）
- Bus 跨模块通信机制 work
- 测试基础设施完备（195 tests pass）
- Critic、Memory、Permanence、ComposerRouter 的"骨架"代码逻辑正确（只是没有真数据）

**核心缺失：**
1. ❌ 没有真实 backbone（DINOv3）
2. ❌ 没有任何真实 expert（MASt3R 等都是 stub）
3. ❌ 没有真实数据 dataloader（只有合成数据）
4. ❌ 没有真实 evaluation metric

---

## 2. 实施路线图（5 个 Stage）

每个 Stage 一个独立 markdown，详见 `mainwork/STAGE-*.md`。

```
Stage 1 (MVR)        ──→ Stage 2 (Memory)    ──→ Stage 3 (Composer)
单 expert 端到端跑通     训练 Memory 证明价值     多 expert + 路由学习
1-2 周                  1 周                    1 周
                          │
                          ↓
                       Stage 4 (Critic+Repair)  ──→ Stage 5 (Stretch)
                       Critic 触发 repair       更多 expert / Permanence
                       1 周                     可选
```

**关键依赖：**
- Stage 1 是所有后续的前提
- Stage 2-4 顺序可调，但都依赖 Stage 1
- Stage 5 可选

---

## 3. Stage 索引

| Stage | 目标 | 时长 | 文档 |
|---|---|---|---|
| **0** | 当前空壳状态（已完成的脚手架） | done | — |
| **1** | DINOv3 + MASt3R + KITTI 真实端到端 smoke | 1-2 周 | `mainwork/STAGE-1-MVR.md` |
| **2** | 训练 Memory 模块证明长序列价值 | 1 周 | `mainwork/STAGE-2-MEMORY.md` |
| **3** | 加 Fast3R + 训练 Composer Router | 1 周 | `mainwork/STAGE-3-COMPOSER.md` |
| **4** | Critic + Repair 真实信号 | 1 周 | `mainwork/STAGE-4-CRITIC.md` |
| **5** | 可选拓展（CUT3R / Permanence / GS） | 可选 | `mainwork/STAGE-5-STRETCH.md` |

---

## 4. 全局规则

### 4.1 编码规范（强制）

**遵循 Karpathy 4 原则**（见根目录 `CLAUDE.md`）：

1. **Think Before Coding** — 不假设，不藏疑问，浮现 tradeoff
2. **Simplicity First** — 最小代码解决问题，不投机
3. **Surgical Changes** — 只动该动的，每行 diff 都能追到 user 请求
4. **Goal-Driven Execution** — 定义成功标准，循环直到通过

### 4.2 执行规则（强制）

- **本地 Windows = 编辑 + 同步 only**，不跑模型
- **服务器 = 训练 + 推理 + KITTI eval**，via `ssh BUAA-Server`
- **大文件下载流程**：先下到 `E:\Dream3R\downloads\` → 再 `scp` 到 server。**不直接在 server 上 wget/curl 大文件**（避免污染、便于本地审计）
- **代码同步流程**：本地编辑 → `scp` 到 `/hdd3/kykt26/code/dream3r/dream3r/<file>`
- **测试流程**：
  - 本地（schema/shape only）：`cd E:\Dream3R\code\dream3r && python -m pytest tests/ -q`
  - 服务器（完整）：`ssh BUAA-Server "cd /hdd3/kykt26/code/dream3r && conda run -n dream3r python -m pytest dream3r/tests/ -q"`
- **每个 Stage 闭合必须**：
  1. 通过该 Stage 的 success criteria
  2. 写一个 `cycles/CYCLE-YYYYMMDD-NNN.md`
  3. 写一个 `decisions/DEC-YYYYMMDD-NNN-stage-N-closure.md`
  4. 更新 `mainwork.md` 的 Stage 状态
- **不动核心**：除非修 bug，否则不要改 `anchor_bank.py / nsa_attention.py / model.py 主 forward`

### 4.3 数据与 checkpoint 管理

| 类型 | 本地路径 | 服务器路径 |
|---|---|---|
| 代码 | `E:\Dream3R\code\dream3r\` | `/hdd3/kykt26/code/dream3r/dream3r/` |
| 下载暂存 | `E:\Dream3R\downloads\` | （不存在，scp 后删除本地） |
| Checkpoints | （不存放） | `/hdd3/kykt26/checkpoints/` |
| 数据 | （不存放） | `/hdd3/kykt26/data/` |
| Runs/logs | （不存放） | `/hdd3/kykt26/code/dream3r/runs/` |

### 4.4 提问规则

遇到以下情况**必须停下来问用户**，不要自己决定：
- 需要下载 >500MB 的权重或数据
- 需要修改 v0.3 / v0.5 已闭合的核心模块
- 在两个合理设计方案之间犹豫
- 训练超过 4 小时不收敛
- 测试出现新的失败但与当前任务无关

---

## 5. 状态追踪

| Stage | 状态 | 开始 | 完成 | DEC |
|---|---|---|---|---|
| 0 | ✅ done | — | 2026-05-23 | DEC-20260523-001 (A6) |
| 1 | ✅ done | 2026-05-23 | 2026-05-23 | DEC-20260523-004 |
| 2 | ✅ done | 2026-05-23 | 2026-05-23 | DEC-20260523-005 |
| 3 | ✅ done | 2026-05-23 | 2026-05-23 | DEC-20260523-006 |
| 4 | ✅ done | 2026-05-25 | 2026-05-25 | DEC-20260525-001 |
| 5 | 🔶 S1 KITTI sealed, cross-dataset re-activated | 2026-05-25 | 2026-05-25 (S1 KITTI) | DEC-20260525-003 (S1 headline), DEC-20260525-004 (distill defer), DEC-20260525-005 (cross-dataset defer, trigger #2 fired 2026-05-25 evening) |

### Stage 4 闭合状态（2026-05-25）

Stage 4 已闭合，见 `cycles/CYCLE-20260525-stage4-closure.md` 和
`decisions/DEC-20260525-001-stage4-critic-closure.md`。

最终服务器证据：

- Critic summary: `conflict_abs_rel_corr = 0.8337993524`, `repair_action_accuracy = 0.9166666865`
- Router retrain: `final_accuracy = 1.0`, `augmented_with_critic_confidence = true`, `context_n_examples = 12`
- Pipeline ablation: `critic_changed_route_count = 1`, `repair_changed_output_count = 2`, `t4_3 = true`
- Metrics: `full_pipeline_repair_on = 0.2108669020`, `critic_on_repair_off = 0.2253848203`, `both_off = 0.2253848203`

Limit: this is real Stage 4 closure evidence, not a strict critic-only aggregate gain or SOTA claim.

### Stage 5 S1 闭合状态（2026-05-25）

Stage 5 S1（≥3 real expert Composer ablation）已闭合，见
`cycles/CYCLE-20260525-stage5-s1-three-expert.md` 和
`decisions/DEC-20260525-002-stage5-s1-three-expert-closure.md`。

最终服务器证据：

- Spann3R real integration: `2 passed, 8 warnings`
- Three-expert oracle: `expert_order = [fast3r, mast3r, spann3r]`, `oracle_counts = {mast3r: 8, fast3r: 2, spann3r: 2}`
- Strengthened router checkpoint: `/hdd3/kykt26/checkpoints/router_stage5_s1_regime_stats_v1/latest.pt`
- Strengthened router ablation: `/hdd3/kykt26/code/dream3r/runs/stage5_s1_router_ablation/results_regime_stats.json`
- Feature mode: `regime_stats`, using online regime-label `features` keys (`frame_count`, `depth_mean`, `valid_ratio`, `depth_temporal_change`, `oxts_available`, `mean_speed`, `speed_std`)
- Router ablation: `learned_router = 0.1636828103`, `oracle_router = 0.1636828103`, `best_single_expert = mast3r`, `always_mast3r = 0.1906146836`
- Improvement: `relative_improvement_vs_best_single = 0.1412896043`, `learned_uses_ge_3_experts = true`, `stage5_s1 = true`
- Regression check: Stage 4 repair pipeline remains `t4_3 = true`

Limit: this is still a 12-window KITTI closure ablation, not a SOTA or cross-dataset generalization claim. The earlier 6D regime-probability-only router did not select Spann3R; the current strengthened result depends on adding online regime-label `features` to the ablation router input.

LOO held-out check (2026-05-25):

- `learned_loo_mean = 0.1875902141`, `oracle_loo_mean = 0.1636828103`,
  `always_mast3r = 0.1906146836`
- `relative_improvement_vs_best_single = 0.0158669279` (1.59%, below the
  closure-set 5% threshold)
- `loo_route_accuracy_vs_oracle = 0.3333` (chance level on 3 classes)
- Held-out distribution drifts to `fast3r=3, mast3r=4, spann3r=5` vs oracle
  `fast3r=2, mast3r=8, spann3r=2`

Reading: the strengthened closure 14.13% gain reflects training-set
memorization on N=12, not a generalizable routing policy. Any future "router
learns" claim needs a larger window set or a second dataset.

Code hygiene fixes:

- `_feature_tensor` normalization stats are now frozen from the checkpoint at
  eval time (`feature_meta.stats_frozen=true`), eliminating silent drift on
  held-out subsets.
- `_load_router` raises on `feature_mode` mismatch between checkpoint and eval.
- Re-running the original strengthened ablation under the fix reproduces the
  closure number byte-identically.

### Stage 5 S1 expanded closure (2026-05-25, DEC-20260525-003)

Window count expanded from 12 to 59 via `--max-per-regime 25` against the same
246-sequence regime label pool. Three real experts unchanged. Server artifacts:

- `/hdd3/kykt26/code/dream3r/runs/stage5_s1_expand_oracle/oracle_expert_labels.json`
- `/hdd3/kykt26/checkpoints/router_stage5_s1_expand_v1/latest.pt`
- `/hdd3/kykt26/code/dream3r/runs/stage5_s1_expand_router_ablation/results.json`
- `/hdd3/kykt26/code/dream3r/runs/stage5_s1_expand_router_loo/results_loo.json`

59-window oracle distribution is far more balanced than 12-window snapshot:

```text
12-window: mast3r=8 (67%), fast3r=2 (17%), spann3r=2 (17%)
59-window: mast3r=31 (53%), spann3r=24 (41%), fast3r=4 (7%)
```

Closure ablation on 59 windows (passes 5% gate with margin):

```text
learned_router: 0.1485612884
oracle_router:  0.1481787252
always_mast3r:  0.1607782668  (best single)
relative_improvement_vs_best_single: 7.60%
learned_expert_counts: fast3r=4, mast3r=31, spann3r=24   (matches oracle exactly)
route_regime_cramers_v: 0.4718
stage5_s1: true
```

Held-out 59-fold LOO (strong route accuracy, modest abs_rel margin):

```text
learned_loo_mean: 0.1571985500
oracle_loo_mean:  0.1481787252
always_mast3r:    0.1607782668
relative_improvement_vs_best_single: 2.23%   (still below 5% gate held-out)
loo_route_accuracy_vs_oracle: 78%            (vs 33% chance for 3-class)
learned_loo_expert_counts: fast3r=6, mast3r=26, spann3r=27
```

Reading: at N=59, the router predicts the oracle expert on 78% of held-out
windows (well above chance), confirming it learns a generalizable in-domain
routing policy. The held-out abs_rel margin is small because MASt3R and
Spann3R are close on outdoor KITTI; full oracle headroom over best-single is
only 7.86%, and LOO captures 28% of that ceiling. The 12-window LOO 33%
chance-level result was an N-too-small artefact.

Honest claim: "router predicts oracle's expert on 78% of held-out KITTI
windows" + "closure-set abs_rel improvement of 7.60% over best single expert".
Not a SOTA claim, not a cross-dataset claim.

### Stage 5 S1 final seal (2026-05-25, DEC-20260525-005)

S1 closes at the 59-window KITTI expanded result above. Cross-dataset
validation (ETH3D Low-res many-view was the proposed target) is deferred:
the server cannot reach eth3d.net (TCP timeout, same symptom as ping
github.com 100% loss), and local-download-then-scp was declined due to
bandwidth constraints on both ends. See
`decisions/DEC-20260525-005-deferred-cross-dataset-validation.md` for the
preserved plan (target archives, upload path, dataloader/oracle/eval
sketches, trigger conditions). No code or checkpoint changes.

Also deferred at the same point: distilled-adapter architecture
(`decisions/DEC-20260525-004-deferred-distilled-adapter-architecture.md`).
Both deferrals leave the Router → full real model design as the
authoritative Stage 5 S1 closure architecture.

### Stage 5 cross-dataset re-activation (2026-05-25 evening)

DEC-20260525-005 trigger #2 (user bandwidth) fired on 2026-05-25 evening.
User downloaded ETH3D Low-res many-view Training set locally and scp'd 4
archives (~3.9 GB total) to `/hdd3/kykt26/data/eth3d/low_res_many_view/raw/`:

```text
multi_view_training_rig.7z              1.7G
multi_view_training_rig_undistorted.7z  1.5G
multi_view_training_rig_occlusion.7z    405M
multi_view_training_rig_scan_eval.7z    289M
```

DEC-005's preserved cross-dataset plan is now active. Stage 5 will close
fully via a forthcoming `DEC-20260525-006-cross-dataset-closure.md` once
the ETH3D oracle + transfer eval finishes. Handoff to the next agent:
`mainwork/HANDOFF-20260525-evening.md`.

---

## 6. 与现有文档的关系

- **不取代** `specs/SPEC-20260522-001-dream3r-v05-axes.md`（A1-A8 axis spec），而是**复用其轴定义**
- **不取代** `cycles/` 和 `decisions/` 目录，而是**统一调度它们**
- 取代 `HANDOFF_PROMPT_NEXT.md`（已过时）

---

## 7. 第一个动作

**下一个 agent 看完本文件后**：
1. 阅读 `CLAUDE.md`
2. 阅读 `mainwork/HANDOFF-20260525-evening.md`（本轮接续指南，自包含）
3. 阅读 Stage 5 S1 闭合链：`cycles/CYCLE-20260525-stage5-s1-three-expert.md` →
   `cycles/CYCLE-20260525-stage5-s1-kitti-expand.md` → `decisions/DEC-20260525-003-stage5-s1-expand-closure.md`
4. 阅读 cross-dataset 复活的依据：`decisions/DEC-20260525-005-deferred-cross-dataset-validation.md`
   （trigger #2 已在 2026-05-25 evening 触发，ETH3D 已上传到
   `/hdd3/kykt26/data/eth3d/low_res_many_view/raw/`）
5. 阅读仍在 defer 的决定：`decisions/DEC-20260525-004-deferred-distilled-adapter-architecture.md`，
   trigger 未满足，不要主动开这条线
6. 按 HANDOFF 推进：Track A (demo 打包) + Cross-dataset closure 双闭合；
   Track B (S5 tttLRM) 留到 cross-dataset 闭合后再说
