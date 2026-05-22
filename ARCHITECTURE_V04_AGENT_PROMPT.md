# Dream3R v0.4 架构闭环 Agent 提示词

## 主提示词

你现在接手 `E:\Dream3R` 项目，目标是把当前 Dream3R 架构从“模块骨架原型”推进到“可运行、可测试、可验收的 v0.4 闭环架构”。

重要边界：

- 不处理开题报告、论文包装、PPT 美化。
- 不做空泛架构描述，必须落到代码、测试和 markdown 任务状态。
- 不虚假声明未实现能力。所有 stub / fallback / proxy 必须显式标注。
- 优先完成架构闭环，而不是追求最终重建性能。

你需要先阅读项目 markdown，确认当前进度、任务清单和被勾选/待完成事项。重点读取：

- `E:\Dream3R\TASK_SNAPSHOT.md`
- `E:\Dream3R\INDEX.md`
- `E:\Dream3R\WORKFLOW_STATUS.md`
- `E:\Dream3R\RESEARCH_STATE.md`
- `E:\Dream3R\README.md`
- `E:\Dream3R\ARCHITECTURE_V04_AGENT_PROMPT.md`
- `E:\Dream3R\ARCHITECTURE_V04_STATUS.md`，如果存在
- `E:\Dream3R\code\dream3r` 下的核心代码

你的核心目标：

基于现有代码，完成 Dream3R v0.4 架构闭环建设，使系统至少具备以下真实可测试行为。

### 1. Perception 感知模块

输入 `image sequence` / `image pair` / `single image`。

输出统一 `PerceptionOutput`：

- `feature_tokens`
- `pointmap_proposal`
- `confidence`
- `evidence_signals`
- `backbone_status`

如果当前没有真实 DINOv3-S，不要写成已实现。保留 adapter / fallback，并在输出日志中标注真实 backend。

### 2. SpatialMemory 空间记忆模块

保留并强化 compressed / selected / sliding 三分支。

要求：

- AnchorBank 默认 `K=256`。
- 支持 `cross_attention` / `mamba_hybrid` recurrence。
- 输出统一 `MemoryOutput`：
  - `fused_context`
  - `latent_drift_proxy`
  - `bank_occupancy`
  - `selected_anchor_stats`
  - `retrieval_log`
  - `memory_backend_status`

### 3. Permanence 永久性模块

负责动态/静态分离、slot / object tracking、stable memory 写入门控。

输出统一 `PermanenceOutput`：

- `dynamic_logits` 或 `dynamic_mask_proxy`
- `dynamic_ratio`
- `suppress_static_write`
- `object_track_set`
- `stable_promotion_log`

如果 dynamic mask 还不是最终 D2 资产，必须明确写成 proxy / intermediate output。

### 4. GeometryCritic 几何校验模块

聚合以下信号：

- Sampson / epipolar consistency
- depth consistency
- covisibility conflict
- confidence
- `latent_drift_proxy`
- `selected_anchor_3d_distance`
- `bank_occupancy`

输出统一 `CriticDecision`：

- `conflict_score`
- `repair_action`
- `reroute_hint`
- `reason_codes`
- `local_window_ids`
- `critic_log`

`repair_action` 至少支持：

- `0`: no repair
- `1`: local rerun
- `2`: full window rerun
- `3`: reroute model

### 5. RepairExecutor 修复执行器

当前架构最大缺陷是 critic 只给信号，没有真正闭环执行。你必须新增或完善 `RepairExecutor`，使 critic decision 能真实影响当前 pipeline。

最低要求：

- `action=1` 时触发局部 rerun 或局部子链路 rerun。
- `action=2` 时触发当前 window rerun，必须有 `max_repair_attempts`，默认 `1`。
- `action=3` 或 `reroute_hint=True` 时触发 composer reroute。
- `repair_action_log` 必须记录每次触发、原因、执行结果和是否达到 max attempts。
- 防止无限递归和重复修复。

### 6. Composer 多模型编排模块

维护七个候选专家：

- MASt3R
- Fast3R
- Spann3R
- CUT3R
- MoGe-2
- DepthAnything
- Test3R

Router 根据以下条件选择专家：

- input mode
- memory state
- critic decision
- backend availability
- cost budget
- previous failure / route regret

必须区分：

- real backend
- fallback backend
- stub backend

主 forward 里必须存在 dispatch 路径。不能只输出 routing logits 而不执行 dispatch。

如果真实 expert 不可用，fallback 也必须返回统一 `ExpertOutput`，并在 evidence / route_log 中标注 `backend_status`。

### 7. Final ReconstructionOutput

最终输出必须统一包含：

- `pointmap`
- `confidence`
- `dynamic_logits` 或 `dynamic_mask_proxy`
- `evidence`
- `selected_expert`
- `backend_status`
- `conflict_score`
- `memory_log`
- `route_log`
- `repair_action_log`
- `contract_log`

## 强制闭环要求

你必须让以下跨模块信号变成真实行为，而不只是日志字段：

- critic -> repair executor -> rerun
- critic -> composer -> reroute
- permanence -> memory 写入门控
- memory -> critic 冲突判断
- composer -> final output

## 工程实施建议

优先在现有代码上做保守增量，不做无关大重构。

如需新增文件，优先考虑：

- `E:\Dream3R\code\dream3r\contracts.py`
- `E:\Dream3R\code\dream3r\repair.py`
- `E:\Dream3R\code\dream3r\orchestrator.py` 或 `pipeline.py`
- `E:\Dream3R\code\dream3r\tests\test_v04_architecture_contract.py`
- `E:\Dream3R\code\dream3r\tests\test_repair_executor_contract.py`
- `E:\Dream3R\code\dream3r\tests\test_composer_dispatch_contract.py`
- `E:\Dream3R\ARCHITECTURE_V04_STATUS.md`

建议使用 dataclass 或 TypedDict 固化模块间 contract，减少裸 dict 传递。

保留现有 v0.3 路径，新增 `architecture_version="v0.4"` 或等价配置开关。

测试必须能在没有 GPU、没有 checkpoint 的情况下用 tiny tensor / mock backend 跑通。

## 自主决策规则

除非遇到以下问题，否则不要停下来问用户，直接做保守工程决策并完成任务：

1. 是否要下载大型 checkpoint 或联网获取模型权重。
2. 是否要删除/重写大量已有代码。
3. 是否要改变项目的核心研究目标。
4. 是否要把 4DGS 纳入本轮主线。
5. 是否要把 dynamic mask 宣称为最终 D2 成品。

默认决策：

- 优先完成 fallback 闭环，再接真实专家。
- dynamic mask 先作为 `dynamic_logits` / `dynamic_mask_proxy`。
- `repair action=2` 默认只允许当前 window 重跑一次。
- 4DGS 本轮只保留 contract，不纳入主 forward 主线。
- 外部专家真实 backend 不可用时，必须 fallback，但不能伪装成 real backend。

## Markdown 任务要求

阅读项目 markdown 中的 checklist / TODO / progress table。

把和 v0.4 架构闭环相关的任务整理为执行清单。

完成代码和测试后，更新对应 markdown：

- 已真实完成并验证的任务才勾选为 `[x]`。
- 只完成 scaffold 的任务必须标注 scaffold / proxy / fallback。
- 未完成项保留 `[ ]`，并写清阻塞原因或下一步。
- 新增或更新 `ARCHITECTURE_V04_STATUS.md`，记录：
  - 本轮完成了什么
  - 哪些闭环已经成立
  - 哪些还是 stub / fallback / proxy
  - 测试结果
  - 下一步最小实验

## 验收标准

完成后必须能证明：

1. fake image sequence 可以走完整 v0.4 forward。
2. critic `action=1` 会触发 local rerun，并进入 `repair_action_log`。
3. critic `action=2` 会触发受控 full window rerun，不会无限循环。
4. `reroute_hint=True` 或 `action=3` 会让 Composer 选择不同 expert。
5. `suppress_static_write=True` 会真实影响 AnchorBank / stable memory 写入。
6. Memory 的 `latent_drift_proxy` / `bank_occupancy` 等信号进入 Critic。
7. Composer dispatch 的 `ExpertOutput` 进入 final output。
8. 输出包含 `pointmap`、`confidence`、`evidence`、`memory_log`、`route_log`、`repair_action_log`、`contract_log`。
9. 相关单元测试或 contract 测试通过；如因缺少 torch / checkpoint 不能跑，必须说明原因，并至少完成语法 / 静态检查。

## 执行流程

1. 只读审查当前 markdown 和核心代码。
2. 给出极短实施计划。
3. 直接实现 v0.4 闭环骨架。
4. 编写 / 更新测试。
5. 运行可用测试。
6. 更新 markdown checklist 和 `ARCHITECTURE_V04_STATUS.md`。
7. 最终汇报修改文件、测试结果、完成度和剩余风险。

最终回答必须包含：

- 修改文件列表
- 架构闭环完成情况
- 仍为 stub / fallback / proxy 的部分
- 测试命令和结果
- markdown 中哪些任务被勾选或更新
- 下一步建议

## 短启动提示词

请优先以 `E:\Dream3R\ARCHITECTURE_V04_AGENT_PROMPT.md` 为最高任务说明，在它的基础上工作。随后读取 `E:\Dream3R\TASK_SNAPSHOT.md`、`INDEX.md`、`WORKFLOW_STATUS.md`、`RESEARCH_STATE.md`、`README.md`，以及 `code/dream3r` 下的 `model.py`、`modules.py`、`bus.py`、`anchor_bank.py`、`nsa_attention.py`、`composer_experts/*`。目标是自主完成 v0.4 架构闭环实现、测试和 markdown checklist 更新；除非涉及大规模删除、下载 checkpoint、改变研究目标或纳入 4DGS 主线，否则不要停下来问用户，直接做保守工程决策并完成。
