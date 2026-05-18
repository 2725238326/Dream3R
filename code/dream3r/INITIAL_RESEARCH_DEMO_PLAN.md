# Dream3R Initial Research Closure and Demo Plan

Status: formalized closure and presentation plan.

Date: 2026-05-10

## Research thesis

Dream3R 当前阶段的研究目标，是在长序列三维重建场景中，把感知、空间记忆、几何检查、多模型接口和结果输出组织成一个可以持续实验的原型系统。它不是为了替代所有现有 3R 方法，而是为后续比较、消融和应用展示提供一个统一的工作基础。

- 视觉特征提取为重建提供基础输入。
- 多模型接口保留 MASt3R、Spann3R、Fast3R 等方法的接入空间。
- 稀疏记忆检索用于组织长序列上下文。
- active/stable memory 区分短期状态更新和长期空间保留。
- AnchorBank 负责保存可召回的稳定空间信息。
- 几何自检模块根据一致性信号给出冲突和修正建议。
- 对象状态模块用于维护动态对象和静态场景之间的关系。
- Mamba hybrid recurrence 提供另一种时序状态更新路径。
- GaussianHead 为后续三维可视化输出保留张量接口。

当前目标：证明这些模块已经形成可运行、可测试的原型，并为后续真实数据消融和应用展示打基础。

## Tonight Definition of Done

今晚结束时必须满足：

1. `dream3r.demo_mamba_path` 能在服务器跑通并输出可讲的 JSON。
2. Smoke test 通过。
3. Full `dream3r.tests.test_*` suite 通过。
4. 展示文档能解释：
   - 我们解决什么问题。
   - 从 3R 家族吸收了什么优点。
   - Dream3R 架构如何综合这些优点。
   - 当前代码已经真实做到哪些。
   - 下一阶段还缺什么。
5. 不再临时开新技术方向；今晚只收束、验证、展示。

## Demo Storyline

### 1. Problem

现有 3R 方法各有强项，但很难同时满足：

- 高质量视觉先验
- 长序列 streaming
- bounded memory
- 几何一致性自检
- 多专家路由
- 对象级连续性
- 面向未来 3DGS 输出

Dream3R 的切入点是把重建流程拆成可观察、可记录的环节，而不是只依赖一次黑盒前向计算。这样后续才能分析每个环节是否真的带来收益。

### 2. What We Borrowed From Existing 3R

- MASt3R / Spann3R：成熟 3R expert 能力与 pointmap-style 几何输出。
- CUT3R：state-token recurrence 的 streaming 思路。
- Point3R / Mem3R / LONG3R 方向：长期空间记忆与遗忘问题意识。
- VGGT / foundation model trend：统一视觉先验的重要性。
- NSA sparse attention：compressed / selected / sliding 三路上下文融合。
- Mamba trend：用 state-space path 改进长序列时序演化。

### 3. What Dream3R adds

- 模块间信息传递机制：记录不同模块之间的读写和控制信号。
- 长期空间记忆库：保存可召回的稳定空间信息。
- 短期/长期状态分离：短期状态负责当前窗口更新，长期记忆负责跨窗口保留。
- 几何自检：将几何一致性信号转化为冲突分数和修正建议。
- 对象状态维护：用对象级状态辅助跨窗口匹配。
- 多模型调度接口：为不同 3R 方法保留统一调用入口。
- 时序状态更新：`state_recurrence_type="mamba_hybrid"` 已接入可运行路径。
- 三维可视化接口：为后续 3DGS 输出保留明确张量格式。

## Live Demo Commands

Run on server:

```bash
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -m dream3r.demo_mamba_path
```

Expected talking points from JSON:

- `device: cuda`
- `cross_attention` and `mamba_hybrid` both run for 3 streaming windows.
- `mamba_hybrid.backend` should be `mamba_ssm`.
- `latent_state_tokens` remains `[1, 32, 128]`.
- `state_delta_mean_abs` shows state is evolving.
- `stable_promotion_rate` shows active state can promote into stable memory.
- `nsa_branch_mean` shows compressed / selected / sliding branches are active.
- `recommended_action` shows Critic repair loop is producing downstream actions.

Validation:

```bash
powershell -NoProfile -ExecutionPolicy Bypass -File E:\kykt\Dream\code\dream3r\scripts\sync_verify_server.ps1 -Mode test
powershell -NoProfile -ExecutionPolicy Bypass -File E:\kykt\Dream\code\dream3r\scripts\sync_verify_server.ps1 -Mode test -FullTests
```

## Tonight Execution Plan

### Phase A: Freeze Scope

Do:

- Keep W1-W18 as the initial research boundary.
- Treat W17 Mamba demo path as the headline new result.
- Treat W18 GaussianHead as future-output contract, not renderer completion.

Do not:

- Start new renderer work.
- Install packages.
- Download checkpoints.
- Rewrite core modules unless a test fails.

### Phase B: Evidence Pack

Prepare these artifacts:

- `CYCLE_033_PLAN.md`: full architecture advancement record.
- `CYCLE_034_PLAN.md`: stabilization and Mamba path status.
- `DEMO_2026_05_11.md`: short demo brief.
- `INITIAL_RESEARCH_DEMO_PLAN.md`: this closure plan.
- Test output summary: smoke + full suite pass.
- Demo output JSON.

### Phase C: Demo Flow

Suggested 8-minute version:

1. 60s: Current 3R gap and Dream3R thesis.
2. 90s: Architecture graph: Perceiver, SpatialMemory, Permanence, Critic, Composer, Bus.
3. 90s: What was integrated from 3R family and why it matters.
4. 90s: Mamba path live run.
5. 60s: Tests and verification.
6. 90s: Next stage: real data, calibration, renderer/3DGS, ablation.

### Phase D: Final Stop Criteria

Stop tonight when:

- Demo command output is captured.
- Full tests pass after latest sync.
- Docs are synced to server.
- The remaining work is clearly labeled as next phase, not unfinished current phase.

## Next Phase After Demo

Priority order:

1. Real-data loader and real sequence evaluation.
2. Ablation table: cross-attention vs Mamba hybrid, with NSA on/off and active/stable on/off.
3. Critic calibration on real geometric consistency distributions.
4. Fast3R dependency cleanup if approved.
5. 3DGS renderer backend only after `gsplat` or equivalent is approved.

## One-sentence summary

Dream3R 当前阶段已经从方案设计推进到可运行原型；下一步需要用真实数据消融、质量评估和可视化结果来支撑更强的研究结论。
