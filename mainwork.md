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
| 5 | 🔶 closed; cross-domain follow-up + addenda complete; critic↔router loop attempted | 2026-05-25 | 2026-05-27 | DEC-20260525-003 (S1 KITTI), DEC-20260525-004 (distill defer), DEC-20260525-005 (cross-dataset defer → trigger #2 fired), DEC-20260525-006 (cross-dataset closure), DEC-20260526-007 (cross-domain follow-up, addenda 1/2/3), DEC-20260527-008 (critic↔router closed loop, NEGATIVE); no active handoff |

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

### Stage 5 cross-dataset closure (2026-05-26, DEC-20260525-006)

DEC-005 trigger #2 (user bandwidth) fired 2026-05-25 evening; ETH3D
Low-res many-view Training archives (4 × .7z, ~3.9 GB) were uploaded to
`/hdd3/kykt26/data/eth3d/low_res_many_view/raw/` and extracted to
`/hdd3/kykt26/data/eth3d/low_res_many_view/training/{5 scenes}`.

Four new code paths (no v0.3/v0.5 core edits):

- `code/dream3r/data/eth3d_long.py`
- `code/dream3r/scripts/generate_eth3d_regime_labels.py`
- `code/dream3r/scripts/build_oracle_expert_labels_eth3d.py`
- `code/dream3r/scripts/eval_cross_domain_router.py`

ETH3D 50-window oracle (10 per scene, cam5, sparse SfM points3D as GT,
align_scale=True):

```text
oracle_counts: spann3r=23 (46%), mast3r=16 (32%), fast3r=11 (22%)
metric:        scale_aligned_abs_rel
```

Best-single shifts across domains: MASt3R on KITTI -> Spann3R on ETH3D.
Fast3R triples its oracle share (7% -> 22%).

Cross-dataset transfer eval (Stage 5 S1 router on ETH3D, zero-shot):

```text
learned_router: 0.2712   <- collapses to always_fast3r
oracle_router:  0.2075
always_fast3r:  0.2712
always_mast3r:  0.2583
always_spann3r: 0.2324   (best single on ETH3D)
relative_improvement_vs_best_single: -16.7%      # router worse than best single
eth3d_route_accuracy_vs_oracle: 22%              # below 33% chance
learned_expert_counts: fast3r=50, mast3r=0, spann3r=0
oracle_expert_counts:  fast3r=11, mast3r=16, spann3r=23
best_single_shifted_kitti_to_eth3d: true
```

Reading: the KITTI-trained router does NOT transfer zero-shot to ETH3D.
Root cause is KITTI-specific stat features (`oxts_available`,
`mean_speed`, `speed_std`) being out-of-distribution for ETH3D's static
rig; frozen KITTI normalization pushes ETH3D inputs into a corner of the
router's input manifold where it deterministically picks Fast3R.

Honest claim: cross-dataset routing is domain-specific. The current
KITTI router does not transfer. Best single expert and oracle
distribution both shift by domain — itself a real cross-dataset signal.

### Stage 5 S1 demo packaging (2026-05-26)

Track A from `HANDOFF-20260525-evening.md`: end-to-end runnable demo of
the Stage 5 S1 expanded router + three real experts on KITTI long
windows. Live forward, two contrast windows (best MASt3R-winning + best
Spann3R-winning), three matplotlib PNGs + ASCII PLY pointmap per window,
top-level + per-window summary JSON.

New files:

- `code/dream3r/scripts/demo.py`
- `code/dream3r/DEMO.md`
- `cycles/CYCLE-20260525-demo-package.md`

Server output `/hdd3/kykt26/code/dream3r/runs/demo_stage5_s1/`:

```text
window_00_2011_09_26_drive_0015_sync_03_oracle_mast3r/
  router=mast3r (MATCH), per_expert_abs_rel: fast3r=0.2466, mast3r=0.0745, spann3r=0.1808
  ply: 232 vertices
window_01_2011_09_28_drive_0165_sync_03_oracle_spann3r/
  router=spann3r (MATCH), per_expert_abs_rel: fast3r=0.2818, mast3r=0.1448, spann3r=0.0951
  ply: 264 vertices
```

Both windows: router's choice matches oracle's choice; chosen expert's
abs_rel is the lowest among the three on each window.

### Stage 5 follow-up: cross-domain routing experiments (2026-05-26, DEC-20260526-007)

HANDOFF-20260526-evening recipe of three retrains executed on server,
no v0.3/v0.5 core edits. See
`cycles/CYCLE-20260526-cross-domain-router-retrain.md` and
`decisions/DEC-20260526-007-cross-domain-routing.md`.

Held-out LOO route accuracy (vs 33% chance):

```text
                            KITTI LOO    ETH3D LOO/transfer
DEC-006 baseline (S5 S1):   78%          22%   (collapse to fast3r)
(a) Robust KITTI router:    77.97%       32%   (collapse to mast3r)
(b) ETH3D-only router:      —            54%   ✓
(c) Joint router v1:        72.88%  ✓    42%   ✓
(c) Joint router v2 (per-domain norm):  71.19% ✓   48%   ✓
```

Held-out rel_imp vs best-single:

```text
                            KITTI         ETH3D
(a) Robust KITTI router:    +4.19%        -11.14%
(b) ETH3D-only router:      —             +6.39%
(c) Joint router v1:        +2.81%        +4.70%
(c) Joint router v2:        +1.35%        +5.78%
```

Honest claim (DEC-007, revised after v2): single-domain routing on
KITTI and ETH3D is learnable in isolation; KITTI's specialized router
does NOT transfer zero-shot to ETH3D even after dropping the 3
KITTI-specific stats; a single 12D-input joint router with explicit
2D domain-id + **per-domain stat normalization** simultaneously beats
each domain's best single expert on held-out LOO. Per-domain norm
(v2) closes ~half the ETH3D-side gap to the specialist that v1's
joint norm incurred, at ~1.5pp cost on KITTI LOO route accuracy. v2
is the recommended cross-domain router going forward.

New server artifacts: `router_kitti_robust_v1`, `router_eth3d_v1`,
`router_joint_v1`, `router_joint_v2` checkpoints + 8 results JSONs
(see CYCLE doc for authoritative paths). No active handoff after this
closure.

### Stage 5 follow-up addendum 3 (2026-05-27, DEC-007 addendum 3)

Two overnight validations executed via
`scripts/tonight_overnight.sh` (32/32 OK):

(A) **Dense GT oracle** — ETH3D 50w oracle rebuilt with
`rig_scan_eval/*.ply` laser-scan depth instead of SfM-sparse
`points3D.txt`. New `data/eth3d_dense_oracle.py` provides MLP/PLY
parsers + vectorized world→camera projection. Joint v3 (per-domain
norm, dense ETH3D + sparse KITTI) retrained + 109-fold LOO.

Held-out LOO route accuracy (vs 33% chance):

```text
                           KITTI LOO    ETH3D LOO/transfer
v2 (sparse oracle):        71.19%       48.00%
v3 (dense oracle):         72.88%       66.00%   (+18pp)
(b) ETH3D-only v2 dense:   —            68.00%
KITTI router → ETH3D dense (zero-shot): 42% route_acc, rel_imp -22.59%
```

Held-out rel_imp vs best-single:

```text
                           KITTI         ETH3D
v2 (sparse oracle):        +1.35%        +5.78%
v3 (dense oracle):         -0.09%        +8.03%
(b) ETH3D-only v2 dense:   —             +7.63%
```

Reading: dense GT is a stronger oracle signal. Joint v3 ETH3D LOO
route accuracy jumps 18pp (48% → 66%) without losing KITTI LOO
route accuracy. KITTI router still does not transfer (dense rel_imp
-22.59%, worse than sparse -11.14% because dense oracle widens the
always_mast3r vs always_spann3r gap). Joint v3 (dense) is the new
canonical cross-domain router; v2 (sparse) preserved as a more
conservative oracle baseline.

(C) **Seed sweep** — discovered both LOO scripts hardcoded
`torch.manual_seed(7)` without `--seed` CLI; original overnight
sweep produced 5× byte-identical results. Fix: `--seed` added to
`eval_router_loo.py` + `eval_router_joint_loo.py`, threaded through
to per-fold training. Re-run via `scripts/rerun_seed_sweep.sh`
(5 seeds × 3 LOO = 15 runs, 1h06m, all OK).

Seed-variance summary (mean ± std across seeds {7, 11, 13, 17, 19}):

```text
                            route_acc           rel_imp
(a) KITTI-robust LOO:       73.56% ± 3.51pp     +3.02% ± 1.35pp
(b) ETH3D-only LOO:         48.80% ± 3.90pp     +5.68% ± 1.03pp
(c) Joint v2 KITTI LOO:     70.85% ± 3.87pp     +0.87% ± 1.62pp
(c) Joint v2 ETH3D LOO:     51.20% ± 4.15pp     +6.15% ± 0.65pp
```

Reading: route accuracy is seed-robust (all std < 5pp gate; all 15
runs stay above 33% chance). ETH3D rel_imp is seed-robust (5/5
joint, 4/5 ETH3D-only above 5% gate). **KITTI rel_imp on joint
router is NOT seed-robust** (mean +0.87%, seed=19 actually
negative). The DEC-007 evening "+1.35% KITTI joint rel_imp" was a
single-seed point sample; revised honest claim downgrades it to
"essentially zero on average, sign-unstable". Both-domains-above-
chance claim and ETH3D-side beat-best-single claim both remain
robust.

No v0.3/v0.5 core touched. No new datasets, no new experts.

### Stage 5 follow-up addendum 4: Critic↔Router closed loop (2026-05-27, DEC-008)

Attempt to wire Stage 4 (Critic + Repair) into Stage 5 (Composer
Router) as a closed-loop reroute. Approved plan
`.claude/plans/cheerful-snuggling-puppy.md`.

Two key findings before reroute eval even ran:

1. **Trained Critic does NOT transfer.** On 327 per-(window, expert)
   entries (KITTI 59w + ETH3D 50w × 3 experts), the trained Critic's
   `conflict_score_sigmoid` has std=0.017 (failing the >0.1 plan
   gate) and picks the best expert on only 25.4% of KITTI windows
   (below 33% chance). Never recommends action=3 (reroute) on any
   of the 327 entries.
2. **Critic's deterministic geometric features ARE informative** —
   sampson_distance picks best expert on 52.5% (KITTI) / 42% (ETH3D),
   both above chance. Used as inference-time reroute heuristic
   (margin=0.10) on joint v3 dense router.

Phase C 5-seed LOO sweep result:

```text
                        router-only          with reroute         delta
KITTI rel_imp:          +2.16% ± 1.33pp      +1.41% ± 1.01pp      -0.75pp
ETH3D rel_imp:          +9.11% ± 1.64pp      +6.99% ± 2.15pp      -2.12pp
```

KITTI: 1/5 seeds gain (+0.12 to +0.29pp), 4/5 lose (-0.77 to -2.55pp).
ETH3D: 1/5 seeds marginally gain (+0.41pp on seed=19), 4/5 lose
(-1.50 to -3.90pp). Plan criterion 4 ("at least 1pp improvement on
at least one domain") FAILS.

Reading: at the current data scale (109 windows, 3 experts), the
joint v3 dense router on regime+stat features already extracts the
available routable signal. Geometric features carry partial signal
but are redundant with regime+stat input. Reroute overrides correct
router picks more often than it fixes incorrect ones.

This is a **negative outcome** — Stage 4 Critic does not add value
to Stage 5 routing at this scale. The wiring infrastructure works
without v0.3/v0.5 core edits; the signal does not transfer. See
DEC-008 §Out of Scope for trigger conditions to revisit (Critic
retrain on 109w, geometry as router input).

---

## 6. 与现有文档的关系

- **不取代** `specs/SPEC-20260522-001-dream3r-v05-axes.md`（A1-A8 axis spec），而是**复用其轴定义**
- **不取代** `cycles/` 和 `decisions/` 目录，而是**统一调度它们**
- 取代 `HANDOFF_PROMPT_NEXT.md`（已过时）

---

## 7. 第一个动作

Stage 5 已闭合（DEC-20260525-006）+ cross-domain follow-up first-pass
已闭合（DEC-20260526-007，含 addendum 1/2/3）+ Critic↔Router closed
loop 已尝试并闭合为 NEGATIVE（DEC-20260527-008）。**当前无 active
handoff**。

阅读顺序（下一 agent）：

1. `CLAUDE.md`
2. `mainwork.md` §5 + §7
3. `decisions/DEC-20260526-007-cross-domain-routing.md`（含 addendum 1/2/3）
4. `cycles/CYCLE-20260526-cross-domain-router-retrain.md`（含 addendum 1/2/3）
5. `decisions/DEC-20260527-008-critic-router-loop.md`（NEGATIVE，含 wiring 教训）
6. `cycles/CYCLE-20260527-critic-router-loop.md`

如需推进下一方向，待选线（trigger 未满足）：

- DEC-008 follow-up #1：Critic retrain on Stage 5 windows
  （327 examples × 3 experts，~1.5d，可能改善 conflict head 泛化）
- DEC-008 follow-up #2：把 geometric features 作为 router 训练
  INPUT（非 reroute heuristic），架构改动较大
- Track B - S5 tttLRM（独立 handoff，DEC-006/007/008 已完成，可以排）
- DEC-20260525-004（distilled adapter，trigger 仍未满足）
- 第三 domain 测试（DEC-007 follow-up #1）
- S3 GaussianHead / S2 Permanence（仍 deferred，需要 trigger 满足）
- 决定方向后再开新 cycle / HANDOFF。
