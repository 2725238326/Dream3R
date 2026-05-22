# Dream3R v0.5 迭代测试与完成计划

date: 2026-05-22

status: execution planning, not axis closure

parent_artifacts:

- `ARCHITECTURE_V04_STATUS.md`
- `ARCHITECTURE_V04_AGENT_PROMPT.md`
- `specs/SPEC-20260522-001-dream3r-v05-axes.md`
- `code/dream3r/SOTA_FEATURE_MATRIX.md`
- `code/dream3r/RECENT_PROGRESS.md`
- `code/dream3r/NEXT_PHASE_ROADMAP.md`

## 研究判断

Dream3R 现在已经不处在“有没有架构骨架”的阶段。v0.4 已经把 typed contracts、RepairExecutor、V04Pipeline、composer dispatch、repair rerun、reroute、memory-to-critic 信号、permanence-to-memory 写入门控这些闭环补上，并用 24 个新测试和 130 个原有测试证明旧路径没有被破坏。

下一阶段的关键不是继续扩展概念图，而是把 v0.4 留下的 stub / fallback / proxy / contract-only 表面逐个推进到真实证据。换句话说，v0.5 的工作对象不是“再画一个更大的系统”，而是“给已经存在的系统补真实后端、真实数据日志、长序列行为和可复核的失败闭环”。

本计划把 v0.5 八轴拆成可执行、可测试、可停机检查的任务序列。它不批准 checkpoint 下载、不批准训练、不批准 heavy install、不批准修改 KYKT 前端，也不声称任何 v0.5 轴已经关闭。每个轴的关闭仍然需要独立 DEC，引用 `SPEC-20260522-001-dream3r-v05-axes.md` 中的 `closes_iff` 条件。

## 总目标

将 Dream3R 从 v0.4 架构闭环推进到 v0.5 证据闭环。

最低可接受结果：

1. 本地 v0.4 contract 更硬，不因 batch、空输入、多 tick、状态传递而脆弱。
2. 服务器上至少完成一次 KITTI 8 到 10 窗 smoke，输出长序列 memory / critic / composer 日志。
3. NSA 三分支权重得到长序列证据，尤其 sliding branch 是否长期为 0。
4. Composer 至少一个专家从 fallback 变成 real backend 证据，或者明确记录为什么不能做到。
5. repair / reroute 日志在真实窗口上可复核。
6. 每个仍未完成的 v0.5 轴都有明确 blocker、下一步和证据标签。

## 分层完成标准

### L0. Contract stability

目的：证明 v0.4 输出契约在小输入、缺失输入、多 tick 和边界情况下稳定。

本层只需要本地 CPU 和 mock / fallback，不需要服务器。

完成条件：

- `V04Pipeline.forward` 在 fake image sequence 上稳定返回 `ReconstructionOutput`。
- batch size 大于 1 时，输出字段存在且 batch 维度一致。
- raw images 缺失时，adapter fallback 路径能返回可标注结果，而不是静默失败。
- 多 tick 传递时，previous memory state / object slots / bus previous signals 不丢失。
- `repair_action_log` 对 action 0 / 1 / 2 / 3 都有确定结构。
- `contract_log` 记录 memory -> critic、permanence -> memory、critic -> composer 的关键读写。

推荐测试文件：

- `code/dream3r/tests/test_v04_edge_cases.py`
- `code/dream3r/tests/test_v04_multitick_state.py`

### L1. Long-sequence integration evidence

目的：证明空间记忆模块在真实数据长序列上有可观察行为。

本层需要服务器 `/hdd3/kykt26/`，但不需要下载新 checkpoint。

完成条件：

- KITTI 同一 drive 至少跑 8 窗，推荐 10 窗。
- 每个 tick 输出：
  - `nsa_branch_weights`
  - `latent_drift_proxy`
  - `bank_occupancy`
  - `selected_anchor_3d_distance`
  - `retrieval_diversity`
  - `repair_action_log`
  - `route_log`
  - `selected_expert`
  - `backend_status`
- 生成 JSONL 或 JSON summary。
- 明确判断 sliding branch 是否在任意窗口 weight > 0.05。
- 如果 sliding branch 仍为 0，记录是“观察结果”，不是马上认定为 bug。

对应 v0.5 轴：

- A6 NSA sliding branch utility verification

### L2. Real-backend evidence

目的：把 composer 从 fallback 证据推进到至少一个 real expert 证据。

本层需要服务器和已有 checkpoint 路径。不得在未授权时下载新 checkpoint。

完成条件：

- 至少一个 adapter 返回 `backend_status["backend"] == "real"`。
- `composer.dispatch()` 的 `ExpertOutput` 进入 final `ReconstructionOutput.pointmap`。
- fallback / real 的状态可在测试和日志中区分。
- real expert 加载失败时不伪装成功，必须记录 `load_error`。

建议优先级：

1. MASt3R，已有 real loader path 和历史服务器证据。
2. Spann3R，如果服务器已有可用路径。
3. Fast3R，先解决 `omegaconf` blocker。
4. 其他 adapters 保持 fallback，直到有明确 checkpoint 和 repo path。

对应 v0.5 轴：

- A2 Composer adapter real-checkpoint loading

### L3. Critic slow-path evidence

目的：把几何校验从“触发内部 rerun / reroute”推进到“能触发一个外部验证路径”。

本层依赖 Test3R adapter 至少有可调用路径。没有 Test3R real backend 时，只允许做 contract 和 fallback 测试，不能声称 A5 关闭。

完成条件：

- 新增 action code 4，或明确复用 action 3 加 special target。
- 高冲突时触发 `dispatch("test3r", images)`。
- Test3R off-path 结果进入 `repair_action_log["offpath_verification"]`。
- 主输出和 off-path 验证输出分开记录，避免混淆。
- 至少一个真实窗口触发该路径并生成日志。

对应 v0.5 轴：

- A5 Test3R as Critic-triggered off-path

### L4. Asset promotion

目的：把 proxy / contract-only 输出推进为定义清楚的资产，但不提前承诺质量。

本层不是第一 sprint。必须先有 L1 / L2 的证据。

完成条件：

- dynamic mask 晋升标准写入 `SPEC-20260503-003` addendum。
- `PermanenceOutput` 同时保留 `dynamic_mask_proxy` 和新增 `dynamic_mask_final`。
- CR-2 优先消费 `dynamic_mask_final`，缺失时 fallback 到 proxy。
- 至少一个 real-data 窗口记录 final promotion 条件是否满足。
- GaussianHead / 4DGS 继续 deferred，除非用户单独批准 renderer DEC 和 license audit。

对应 v0.5 轴：

- A3 dynamic_mask_proxy -> final D2
- A7 GaussianHead conditional main-forward entry, likely deferred

## 推荐推进顺序

| Sprint | 目标 | 本地或服务器 | 轴 | 产物 | 为什么先做 |
|---|---|---|---|---|---|
| S0 | v0.4 edge hardening | 本地 | none | edge tests + multi-tick tests | 不依赖 checkpoint，先防止架构脆弱 |
| S1 | KITTI 8 到 10 窗 memory evidence | 服务器 | A6 | long-seq JSON + branch-weight table | 直接验证空间记忆图是否有实证行为 |
| S2 | MASt3R / Spann3R real dispatch | 服务器 | A2 partial | backend real test + route log | 让 composer 从 fallback 推进到真实证据 |
| S3 | Fast3R blocker fix | 服务器 | A2 partial | omegaconf fix note + integration test | 解开已有 real path 的依赖阻塞 |
| S4 | Test3R off-path contract | 本地 + 服务器 | A5 | action 4 + offpath log | 把 critic 图中的慢验证路径落地 |
| S5 | dynamic mask promotion design | 本地 + 服务器 | A3 | spec addendum + field + CR-2 update | 在有真实日志后再定义 D2 |
| S6 | DINOv3-S or replacement backbone decision | 本地调查 + 服务器 | A1 | SRC row + loader test | 先确认 release 和路径，不把名称当实现 |
| S7 | tttLRM A1 sub-action plan | markdown + later code | A8 | A1 enum + W25 plan | 依赖长序列证据，不应提前做 |
| S8 | 4DGS entry | deferred | A7 | separate DEC | renderer 和 license 风险高，暂不进主线 |

## 任务包 S0. 本地 v0.4 hardening

### S0.1 Edge-case contract tests

目标：补齐 v0.4 contract 的边界测试。

建议新增：

- `test_v04_forward_batch_two_keeps_contract_shape`
- `test_v04_forward_without_raw_images_marks_fallback_backend`
- `test_v04_output_contains_required_logs_under_no_repair`
- `test_v04_repair_log_schema_stable_for_all_actions`
- `test_v04_contract_log_records_required_signal_reads`
- `test_v04_backend_status_never_claims_real_without_loaded_adapter`

验收：

- 本地 `python -m pytest dream3r/tests/test_v04_edge_cases.py -q` 通过。
- 不改 v0.3 主路径，除非测试暴露真实 contract bug。

### S0.2 Multi-tick state tests

目标：证明 V04Pipeline 不是单 tick toy wrapper。

建议新增：

- `test_v04_pipeline_carries_memory_state_across_ticks`
- `test_v04_pipeline_carries_object_slots_across_ticks`
- `test_v04_pipeline_previous_bus_signals_affect_next_tick`
- `test_v04_repair_cap_resets_per_forward_not_globally`

验收：

- 连续 3 ticks fake sequence 不丢状态。
- `bank_occupancy` 或 retrieval log 至少随 tick 有可观察变化。
- repair cap 不跨 forward 错误污染下一轮。

### S0.3 Runbook generator

目标：为服务器执行生成稳定命令清单，避免临场拼命令。

建议新增：

- `code/dream3r/scripts/run_v05_longseq_kitti.ps1`，本地生成/记录命令即可，不直接执行服务器动作。
- 或 `code/dream3r/V05_SERVER_RUNBOOK.md`，列出 SSH、SFTP、pytest、KITTI run、JSON export 的命令。

验收：

- runbook 能让用户 SSH 到 `/hdd3/kykt26/` 后逐条执行。
- 明确哪些命令是本地执行，哪些命令是服务器执行。

## 任务包 S1. A6 长序列空间记忆验证

### 研究问题

KITTI 两窗 smoke 中 NSA branch weights 为 compressed 0.3927 / selected 0.6073 / sliding 0.000。这个 0.000 可能有三种解释：

1. 短序列下 sliding branch 确实不需要参与。
2. training-free routing 有偏置，压制 sliding branch。
3. 当前日志或分支权重统计没有覆盖真实 sliding 贡献。

S1 的目标不是让 sliding branch 必须变大，而是判断哪种解释更可信。

### 实验设计

输入：

- KITTI `2011_09_26_drive_0001_sync_02`
- window count: 8 和 10，优先 10
- architecture: v0.4 pipeline
- backend: 当前可用 backend，允许 fallback，但必须标注

输出：

- `demo_artifacts/real_sequence/v05_longseq_kitti_10.json`
- `demo_artifacts/real_sequence/v05_longseq_kitti_10_summary.md`

每 tick 记录：

| 字段 | 用途 |
|---|---|
| `tick_id` | 对齐窗口 |
| `selected_expert` | 检查 routing |
| `backend_status` | 防止 fallback 被误读 |
| `nsa_branch_weights.compressed` | 压缩远程状态权重 |
| `nsa_branch_weights.selected` | AnchorBank 检索权重 |
| `nsa_branch_weights.sliding` | 局部窗口权重 |
| `latent_drift_proxy` | 长序列漂移代理 |
| `bank_occupancy` | AnchorBank 填充 |
| `selected_anchor_3d_distance` | 空间锚点质量代理 |
| `repair_action` | 是否触发校验修复 |
| `repair_action_log.n_attempts` | 是否受控 |
| `route_log.reroute_applied` | 是否模型切换 |
| `pointmap_l2` | 集成稳定性，不是 SOTA 质量 |

### 判读规则

| 观察 | 判断 | 下一步 |
|---|---|---|
| sliding > 0.05 至少一次 | sliding branch 在长序列有参与 | A6 可推进到 evidence-observed |
| sliding 始终 0，但 bank_occupancy 和 selected 稳定增长 | 可能是 selected branch 足够强 | 记录为 design observation，不急改 |
| sliding 始终 0，latent_drift_proxy 上升 | 可能存在 routing starvation | 本地查 nsa gate bias |
| repair action 频繁触发 | Critic 可能过敏或 pointmap 不稳定 | 进入 calibration task |
| reroute 从不触发 | 可能 conflict 不够高，也可能 route threshold 太保守 | 构造高冲突 fixture |

### A6 closure boundary

S1 可以给 A6 提供 evidence，但不自动关闭 A6。关闭 A6 需要 cycle log 明确写入：

- longer KITTI window count
- sliding branch 是否触发
- 如果未触发，是否调查 routing bias
- SOTA matrix NSA row 是否更新

## 任务包 S2. A2 adapter real-backend staged closure

### 研究问题

Composer 的结构价值只有在至少部分 expert 真正接入后才有说服力。现在 v0.4 已证明 dispatch 路径存在，但多数 adapter 还是 fallback。S2 的目标是先关闭最容易关闭的 adapter 子集，而不是七个一起赌。

### 分阶段 adapter 顺序

| Adapter | 当前状态 | 优先级 | 原因 | 完成条件 |
|---|---|---|---|---|
| MASt3R | loader wired, local no ckpt | P0 | 历史服务器证据最强 | server tick backend real |
| Spann3R | fallback / server可能已有 | P0 | 与 memory 主题最相关 | server tick backend real |
| Fast3R | loader wired, omegaconf blocker | P1 | many-view baseline 关键 | blocker fix + backend real |
| DepthAnything | fallback | P2 | depth prior 支持 critic / mask | checkpoint path + ExpertOutput |
| MoGe-2 | fallback and missing SRC row | P2 | 单目几何 prior | 先补 SRC row |
| CUT3R | fallback | P3 | dynamic tolerance 相关 | repo path clear |
| Test3R | fallback | P1 for A5 | critic slow path 依赖 | off-path callable |

### 每个 adapter 的 closure checklist

每个 adapter 单独关闭，不要要求一次全关。

- [ ] `load_checkpoint(path)` 实际实现。
- [ ] 服务器上 path 存在，且加载日志记录 path。
- [ ] `adapter.is_loaded == True`。
- [ ] `backend_status["backend"] == "real"`。
- [ ] 一次 `composer.dispatch(adapter_id, images)` 返回 `ExpertOutput`。
- [ ] `ExpertOutput.evidence["backend_status"]` 标注 real。
- [ ] fallback path 仍然存在，加载失败时不会 crash 整个 pipeline。
- [ ] 新增或更新 integration test，服务器专用可跳过本地。
- [ ] `ARCHITECTURE_V04_STATUS.md` 和 `SOTA_FEATURE_MATRIX.md` 同步。

### 失败处理

| 失败 | 处理 |
|---|---|
| checkpoint 缺失 | 不下载，记录需要用户批准 |
| repo 缺失 | 不自动 clone，记录 path requirement |
| dependency 缺失 | 如果是轻量依赖，写 server runbook 让用户确认 |
| 输出 shape 不匹配 | adapter 层做 shape normalization，不改 final contract |
| real 输出比 fallback 差 | 不回滚 real，标注 quality not proven |

## 任务包 S3. A5 Test3R off-path

### 研究问题

当前 Critic 的 repair action 已能触发 internal rerun 和 reroute，但图里的“校验模块源自 Test3R，支持在线修复”还没有真正体现在 off-path 验证上。A5 要做的是把 Test3R 从普通 composer expert 变成 critic-triggered slow path。

### 合理设计

不要让 Test3R off-path 直接替换主输出。先作为验证证据进入 repair log。

推荐 contract：

```text
action 4: test3r_offpath_verify
trigger: conflict_score high OR reroute_hint true AND selected_expert not test3r
effect: dispatch("test3r", images) once
output: repair_action_log.offpath_verification
```

推荐日志：

```text
offpath_verification:
  expert_id: test3r
  backend: real | fallback | stub
  triggered_by: conflict_score | reroute_hint | reason_code
  pointmap_shape: ...
  confidence_mean: ...
  accepted_as_main_output: false
```

验收：

- 本地 fallback test 证明 action 4 能 dispatch Test3R。
- 服务器 test 证明如果 Test3R real backend 可用，backend 变成 real。
- 主输出和 off-path 输出分开。
- `max_repair_attempts` 仍然生效，不进入循环。

## 任务包 S4. A3 dynamic mask promotion

### 研究问题

`dynamic_mask_proxy` 现在只是中间代理。要变成 D2，必须有 promotion criterion。否则命名上升级，科学上没有升级。

### 推荐 promotion criterion

一个像样的 D2 final mask 至少满足三类证据中的两类：

1. Temporal consistency: 同一 region / slot 在连续 N 窗保持稳定，建议 N >= 3。
2. Geometry consistency: 该区域在 depth / epipolar / covisibility conflict 上有可解释变化。
3. External prior agreement: 与 SAM 2 / tracker / depth prior 中至少一种外部先验有一致性。

短期不必引入外部大模型。可以先定义 criterion，并用 proxy-only evidence 标注“未满足 external prior”。

### 字段迁移

建议新增：

```text
PermanenceOutput.dynamic_mask_final: Optional[tensor]
PermanenceOutput.dynamic_mask_status:
  proxy_only | promoted_final | unavailable
PermanenceOutput.dynamic_mask_promotion_log:
  temporal_consistency
  geometry_consistency
  external_prior_agreement
  promoted
```

CR-2 规则：

```text
if dynamic_mask_final is available:
    use final for suppress_static_write
else:
    use dynamic_mask_proxy
```

验收：

- `dynamic_mask_proxy` 仍存在。
- `dynamic_mask_final` 不满足条件时为 None。
- CR-2 消费路径可测试。
- 文档明确 D2 final 是否关闭。

## 任务包 S5. A1 backbone integration decision

### 研究问题

图里写 DINOv3-S，但代码当前没有真实 DINOv3-S release pin。A1 的第一步不是写 loader，而是确认“DINOv3-S”是否是可复现对象。

### 决策路径

| 结果 | 决策 |
|---|---|
| DINOv3-S 有明确 release + checkpoint | 走 A1 原计划 |
| 只有 DINOv3 family 没有 S release | 改名为 modern self-supervised backbone real integration |
| 服务器已有 DINOv2 稳定路径 | 短期用 DINOv2 作为 real baseline |
| timm / hub 无法稳定加载 | 用 manual checkpoint path，不依赖在线 hub |

### 完成条件

- 新增 `SRC-*` row，记录具体 backbone release。
- `Perceiver._try_load_backbone` 可 deterministic resolve。
- `backend_status["backend"] == "real"` 在服务器至少一次。
- 本地无 backbone 时仍 fallback，不影响 tests。

## 任务包 S6. A8 tttLRM-style A1 sub-action

### 研究问题

v0.4 RepairExecutor 只有窗口级 action。长序列记忆需要更细粒度的 state update policy。A8 的价值在于把“更新状态”从隐式行为变成可记录的 action vocabulary。

### 建议先做设计，不急写复杂算法

新增 enum：

```text
A1SubAction:
  full_update
  pose_adaptive_update
  kalman_update
  skip_update
  reset_state
  ttt_lrm_update
```

策略输入：

- `latent_drift_proxy`
- `bank_occupancy`
- `conflict_score`
- `confidence_mean`
- `nsa_branch_weights`
- `repair_action`

短期默认：

```text
if conflict_score high and latent_drift high:
    reset_state or ttt_lrm_update
elif confidence low:
    skip_update
elif pose novelty high:
    pose_adaptive_update
else:
    full_update
```

验收：

- 不需要训练 tttLRM。
- 先让 policy 产生日志和可测试选择。
- W25 `TTT_PLAN.md` 再决定是否实现真正 test-time update。

## Server runbook outline

此处只给执行清单。真正执行需要用户服务器操作或显式授权。

```bash
# 1. SSH to server
ssh <user>@<server>

# 2. Enter project
cd /hdd3/kykt26/code/dream3r

# 3. Check environment
python -c "import torch; print(torch.__version__)"
python -c "import dream3r; print('dream3r import ok')"

# 4. Run v0.4 contract tests
python -m pytest dream3r/tests/test_v04_architecture_contract.py \
                 dream3r/tests/test_repair_executor_contract.py \
                 dream3r/tests/test_composer_dispatch_contract.py -q

# 5. Run proposed edge tests when added
python -m pytest dream3r/tests/test_v04_edge_cases.py \
                 dream3r/tests/test_v04_multitick_state.py -q

# 6. Run KITTI long sequence smoke
python -m dream3r.evaluate_real_sequence \
  --sequence-root <kitti_sequence_path> \
  --max-windows 10 \
  --architecture-version v0.4 \
  --output-json demo_artifacts/real_sequence/v05_longseq_kitti_10.json

# 7. If ablation runner supports it
python -m dream3r.ablate_real_sequence \
  --sequence-root <kitti_sequence_path> \
  --max-windows 10 \
  --output-json demo_artifacts/real_sequence/v05_real_ablation_10.json
```

如果当前 CLI 参数不完全一致，执行 agent 应先读取 `evaluate_real_sequence.py` 和 `ablate_real_sequence.py`，不要臆造参数。runbook 可以调整，但必须把最终实际命令写入 cycle log。

## Evidence table template

每次服务器 run 后都应填表。

| Run id | Date | Code commit or status | Data | Windows | Backbone | Expert backends | Mean pointmap L2 | Sliding fired | Repair fired | Reroute fired | Evidence label |
|---|---|---|---|---:|---|---|---:|---|---|---|---|
| v05-a6-kitti10-001 | TBD | dirty or hash | KITTI drive | 10 | fallback / real | fallback / real | TBD | yes / no | yes / no | yes / no | integration evidence |

## JSON summary schema

建议每次实验导出同一 schema，方便后续画图。

```json
{
  "run_id": "v05-a6-kitti10-001",
  "architecture_version": "v0.4",
  "axis_targets": ["A6"],
  "data": {
    "dataset": "KITTI",
    "sequence": "2011_09_26_drive_0001_sync_02",
    "window_count": 10
  },
  "backend_status": {
    "perception": "stub_or_real",
    "composer": {
      "mast3r": "fallback_or_real"
    }
  },
  "ticks": [
    {
      "tick_id": 0,
      "nsa_branch_weights": {
        "compressed": 0.0,
        "selected": 0.0,
        "sliding": 0.0
      },
      "latent_drift_proxy": 0.0,
      "bank_occupancy": 0.0,
      "selected_expert": "mast3r",
      "repair_action": 0,
      "reroute_applied": false,
      "pointmap_l2": 0.0
    }
  ],
  "summary": {
    "sliding_fired": false,
    "repair_fired": false,
    "reroute_fired": false,
    "real_backend_seen": false,
    "evidence_boundary": "integration evidence, not trained reconstruction quality"
  }
}
```

## Decision gates

### Gate G0. Local stability

Pass if all S0 tests pass.

Fail if V04Pipeline contract is unstable under fake inputs. If fail, fix contract before server work.

### Gate G1. Long-sequence observability

Pass if KITTI 8 到 10 窗 produces complete memory / critic / route logs.

Fail if run crashes, logs missing, or output cannot be tied to ticks.

### Gate G2. Sliding branch diagnosis

Pass if sliding branch either fires or its non-firing is explicitly diagnosed.

Fail if we still only know “2-window smoke had 0.000”。

### Gate G3. Real backend evidence

Pass if at least one adapter returns backend real on server.

Fail if all remain fallback due to checkpoint / dependency / path blockers. This is not a research failure, but it blocks A2 closure.

### Gate G4. Critic slow-path readiness

Pass if Test3R can be dispatched as off-path verification in fallback or real mode.

Fail if action vocabulary or dispatcher cannot target Test3R specifically.

## Risk register for this plan

| Risk | Likelihood | Impact | Mitigation |
|---|---:|---:|---|
| DINOv3-S release ambiguity | high | medium | Treat A1 as release survey first |
| Checkpoint path missing | high | high | Do not download by default, record blocker |
| Fast3R dependency blocker | medium | medium | Isolate `omegaconf` fix in server runbook |
| Sliding branch remains 0 | medium | medium | Diagnose before changing routing |
| Dynamic mask overclaim | high | high | Keep proxy and final fields separate |
| Repair loop runaway | low | high | Preserve `max_repair_attempts` tests |
| Real backend slower than fallback | medium | low | Log cost and quality separately |
| 4DGS scope creep | high | high | Keep A7 deferred unless DEC approved |

## What not to do

- Do not claim DINOv3-S is integrated until `backend_status["backend"] == "real"` is observed.
- Do not promote `dynamic_mask_proxy` to D2 by renaming alone.
- Do not merge 4DGS into main forward in this sprint.
- Do not download checkpoints without explicit approval.
- Do not treat KITTI pointmap L2 as SOTA quality.
- Do not rewrite v0.3 modules unless an axis closure DEC explicitly requires it.
- Do not collapse all adapters into one sprint.
- Do not hide fallback status in pretty summaries.

## Short prompt for another agent

Use the following prompt to start a focused execution pass:

```text
You are working in E:\Dream3R. Read planning/DREAM3R_V05_ITERATION_TEST_PLAN.md first, then ARCHITECTURE_V04_STATUS.md, specs/SPEC-20260522-001-dream3r-v05-axes.md, TASK_SNAPSHOT.md, WORKFLOW_STATUS.md, and the v0.4 code under code/dream3r/contracts.py, repair.py, orchestrator.py, plus evaluate_real_sequence.py and ablate_real_sequence.py. Your task is to begin the v0.5 evidence-closure program, starting with S0 local v0.4 edge tests and the server runbook for S1 A6 KITTI long-sequence memory verification. Do not download checkpoints, train models, modify KYKT frontend, or claim any v0.5 axis closed. Make conservative additive edits, run available local tests, and update the relevant markdown status with exact test commands and remaining blockers.
```

## Expected final report from execution agent

The execution agent should end with:

- Files changed.
- Tests added.
- Commands run.
- Test results.
- Whether S0 passed.
- Whether a server runbook was produced.
- Whether any v0.5 axis evidence changed.
- Which blockers remain.
- Exact next command for the human to run on server, if server execution is still needed.
