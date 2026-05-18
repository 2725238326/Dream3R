# Long-Seq Real-Data Table Plan: ablate_recurrence Extension to KITTI ≥10-Window

| 字段 | 取值 |
|---|---|
| 文件类型 | planning artifact (非 spec, 非决策, 非执行授权) |
| 创建日期 | 2026-05-15 |
| 状态 | v1, draft (plan-only; 执行需独立 DEC + F-002 server 授权) |
| 上游 | `planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md` §4 P0 + §5 A3 + 综述 §6 长序列内存四类 |
| 授权根 | DEC-20260515-001 (cycle 035 launch; 仅授权写本文件, 不授权执行) |
| 触及范围 | 仅本文件; 不动 `code/dream3r/ablate_recurrence.py`, 不动 `code/dream3r/config.py`, 不动 SPEC |

## 1. Goal

`code/dream3r/ablate_recurrence.py` 当前 4 个变体 (baseline_cross_attention / mamba_hybrid / no_nsa / no_stable_memory) 在合成数据 + windows=3 + seeds=[33,34,35] 上跑过 (per `code/dream3r/RECENT_PROGRESS.md` cycle 033 W14), 输出包含 `elapsed_ms_mean` + `state_delta_mean_abs` 等运行指标。

综述 §6 把长序列内存机制分为四类 (空间指针 / causal-autoregressive / hybrid memory / 预算治理与滤波), 并指出"长序列退化主要表现在尺度漂移 + 记忆衰减"两个症状。当前 ablate_recurrence:

1. 只跑 windows=3 (短序列), 无法暴露长序列退化
2. 用合成数据, 不接 KITTI 真实分布
3. 输出指标偏 runtime (elapsed_ms / state_delta), 缺尺度漂移 / 记忆衰减专用度量

本 plan 设计 KITTI ≥10 窗扩展的执行流程:

1. 把 4 个现有变体映射到综述 §6 四类机制 (做对应关系审计, 非实证)
2. 列出 KITTI 真实长窗 sub-sample 候选 + windows ∈ {10, 20, 50, 100} 的资源估算
3. 增加 4 个长序列专用度量 (scale_drift_proxy / memory_decay_proxy / anchor_fill_rate / retrieval_diversity)
4. 给出 expected behavior per variant (设计阶段假设, 非实证)
5. 给出 validation gate 让"扩展跑结果"与"合成数据 windows=3 baseline"在同一指标上对比, 避免回归

**本 plan 不做的事** (per DEC-20260515-001 §Not authorized):

- 不启动 ablate_recurrence on KITTI long windows (需独立 DEC + F-002)
- 不修改 `ablate_recurrence.py` 任何代码 (variant 列表 / argparse / measurement schema)
- 不下载 / 准备 KITTI long-sequence subset (server 数据准备需独立 DEC)
- 不修改 SPEC-20260506-005 v0.2 ABL-v02-N / SPEC-20260507-002 v0.3 / SPEC-20260508-002 (memory ablation addendum)
- 不下结论说"某变体在长窗上优于其他变体" — 这是 ABL 跑后的实证问题

## 2. 当前 ablate_recurrence 状态 (recap)

per `code/dream3r/ablate_recurrence.py` (cycle 033 W14 实装):

```text
4 variants 配置:
1. baseline_cross_attention
   state_recurrence_type = cross_attention
   memory_use_nsa        = True
   enable_stable_memory  = True

2. mamba_hybrid
   state_recurrence_type = mamba_hybrid
   memory_use_nsa        = True
   enable_stable_memory  = True

3. no_nsa
   state_recurrence_type = mamba_hybrid
   memory_use_nsa        = False
   enable_stable_memory  = True

4. no_stable_memory
   state_recurrence_type = mamba_hybrid
   memory_use_nsa        = True
   enable_stable_memory  = False

默认参数:
  windows = 3
  seeds   = [33, 34, 35]
  use_backbone = False    # 合成 latent 直接喂入 C2
  device  = cuda if available else cpu

当前度量 (_summarize 输出):
  backend / backend_error
  elapsed_ms_mean
  state_delta_mean_abs
  (其余度量未在 grep 切片内, 后续 calibration 启动 DEC 时 review)
```

## 3. 4 变体 → 综述 §6 四类机制映射

| 变体 | state_recurrence | memory_use_nsa | enable_stable_memory | 综述 §6 对应机制 |
|---|---|---|---|---|
| baseline_cross_attention | cross_attention | True | True | hybrid memory (B3) — cross-attention + NSA 三分支 + AnchorBank |
| mamba_hybrid | mamba_hybrid | True | True | causal-autoregressive (B2) + hybrid memory (B3) — Mamba 循环 + NSA 三分支 + AnchorBank |
| no_nsa | mamba_hybrid | False | True | causal-autoregressive (B2) — Mamba 循环 + AnchorBank (无 hybrid) |
| no_stable_memory | mamba_hybrid | True | False | causal-autoregressive (B2) + hybrid (B3) 一部分 — Mamba 循环 + NSA, 无 spatial pointer |

**对应关系审计**:

- B1 空间指针 (Point3R 类): 由 `enable_stable_memory=True` 启用的 AnchorBank K=256 + 3D-aware retrieval 实现。`no_stable_memory` 是这一类的 ablation。
- B2 causal-autoregressive (CUT3R/STream3R 类): 由 `state_recurrence_type=mamba_hybrid` 启用的 Mamba 循环 + StateToken 实现。`baseline_cross_attention` 是这一类的 ablation (用 cross-attention 替代 SSM 循环)。
- B3 hybrid memory (NSA-hybrid): 由 `memory_use_nsa=True` 启用的 NSA 三分支 (compressed + selected + sliding) 实现。`no_nsa` 是这一类的 ablation。
- B4 预算治理 / 滤波 (LONG3R 类): **无对应 ablation 变体**。`ablate_recurrence.py` 4 变体不覆盖 B4 子类。这是一个空缺, 与 `planning/SOTA_MATRIX_V2.md` Table B 的 B4 ⚠ 标注一致。

**B4 空缺的影响**: 在 windows ≥ 50 / 100 时, 没有动态剪枝的变体可能因 anchor budget 用尽而退化。本 plan 不新增 B4 变体 (新增变体需独立 spec delta + DEC; per SPEC-20260508-001 v0.3 + SPEC-20260508-002 memory ablation addendum); 仅在 §6 validation gate 里把 B4 列为"已知未覆盖"以避免误读结果。

## 4. KITTI long-window sub-sample 候选

| Sub-sample 标签 | KITTI 来源 | windows | 估计帧数 (per window=4 frames) | 候选场景 |
|---|---|---|---|---|
| KITTI-LONG-10 | KITTI raw / odometry | 10 | 40 frames | seq 00 部分段 |
| KITTI-LONG-20 | KITTI raw / odometry | 20 | 80 frames | seq 00 / 02 部分段 |
| KITTI-LONG-50 | KITTI odometry full | 50 | 200 frames | seq 04 / 06 |
| KITTI-LONG-100 | KITTI odometry full | 100 | 400 frames | seq 00 / 05 / 07 完整 |

**注**:
- 上表 windows 数是 plan-level, 实际帧数需根据 `evaluate_real_sequence.py` 的 window stride 配置 (cycle 034 KITTI smoke 用了 window=4 frames + stride=1, 2 windows = 8 frames)。
- 任何 KITTI sequence 下载 / preprocessing 需独立 DEC (per F-002); 当前 cycle 034 只覆盖 2 windows 的最小 smoke。
- 候选场景仅做 server-side review reference, 不在本 cycle 实际选取。
- KITTI license 已在 cycle 034 KITTI smoke 时 review (per cycle 034 cycle log), 不需重新 review; 但实际 sequence 选取需在启动 DEC 中固定。

## 5. 4 个长序列专用度量 (推荐新增)

当前 `_summarize()` 输出 `elapsed_ms_mean` + `state_delta_mean_abs` 不足以暴露长序列退化。推荐在 plan 阶段定义以下 4 个 plan-level 度量, 由 calibration 启动 DEC 在 ablate_recurrence.py 代码层落地:

### 度量 D1: scale_drift_proxy

```text
定义: 在 window i 和 window 0 上, 同一物理点 (如果有跨窗共视) 的 pointmap 输出 L2 距离 ratio
公式: D1[i] = mean_per_point(|p_i - p_0| / |p_0|)
诊断: D1 单调上升 → 尺度漂移; D1 在 window i_critical 突然跳变 → memory reset
来源信号: pointmap_conflict (per CROSS_SPEC_SIGNAL_CONTRACT v2.1)
对应综述: §6 + §10 A5 尺度漂移
```

### 度量 D2: memory_decay_proxy

```text
定义: NSA selected branch 在 window 0 写入的 anchor, 在 window i 被检索的概率
公式: D2[i] = P(selected_indices_at_window_i ∩ written_at_window_0)
诊断: D2 单调下降 → 早期 anchor 被遗忘; D2 在所有 window 上接近 0 → memory 完全被新帧覆盖
来源信号: 从 NSA selected branch 的 attention scores 提取 (需 code 层 instrumentation)
对应综述: §6 hybrid memory B3 子类
```

### 度量 D3: anchor_fill_rate

```text
定义: AnchorBank 在 window i 的填充比例
公式: D3[i] = nonzero_anchors_at_window_i / K (K=256)
诊断: D3 在 windows < K/4 时线性上升 → 正常; D3 饱和 → budget 触发, 需要 LRU/置换策略; D3 触发置换但不区分 high/low confidence anchor → 政策缺陷
来源信号: AnchorBank state (per SPEC-20260508-001 v0.3 C2 §AnchorBank)
对应综述: §6 空间指针 B1 子类 + §6 B4 预算治理 (空缺信号)
```

### 度量 D4: retrieval_diversity

```text
定义: 跨 windows 的 NSA selected branch 检索到的 anchor index 多样性
公式: D4 = unique_indices_across_all_windows / sum_indices_across_all_windows
诊断: D4 接近 1 → 每次检索都用不同 anchor (健康); D4 接近 0 → 几个 hot anchor 被反复检索, 其余 anchor "死"
来源信号: NSA selected branch indices 时序累积
对应综述: §6 hybrid memory B3 子类 + Memory 政策审计
```

**注**: 4 个度量中 D1 + D3 当前已经可以从 Critic 已发布信号 (pointmap_conflict / AnchorBank state) 中提取, 度量层只需要 aggregation logic; D2 + D4 需要 ablate_recurrence.py 在 NSA branch 加 instrumentation hook (非破坏性), 这是 calibration 启动 DEC 的代码工作量评估项。

## 6. Expected behavior per variant (design assumption, non-empirical)

下表是基于综述 §6 判断 + Dream3R 架构知识的 design assumption, 不是实证结论。实际跑结果可能反驳任何一行 (这是 ablation 的核心价值)。

| 变体 | windows=3 (current) | windows=10 (KITTI-LONG-10) | windows=50 (KITTI-LONG-50) | windows=100 (KITTI-LONG-100) |
|---|---|---|---|---|
| baseline_cross_attention | ✓ runtime baseline | D1 / D2 偏高 (无 SSM 长程压缩) | D1 / D2 显著退化 | 预期失败或 OOM (cross-attention O(N²)) |
| mamba_hybrid | ✓ runtime baseline | D1 / D2 较低 (Mamba 长程 + NSA 选择 + AnchorBank) | D1 / D2 仍较低, D3 接近饱和 | D3 饱和触发置换政策 (政策本身的 B4 子类未实装是已知风险) |
| no_nsa | ✓ runtime baseline | D2 显著退化 (无 NSA selected branch) | D2 高, D4 低 | 预期严重退化 (mamba 一个 path 不足以选择) |
| no_stable_memory | ✓ runtime baseline | D1 退化 (无 spatial anchor → 无尺度锚点) | D1 显著漂移 | 预期失败 — spatial anchor 是长序列尺度稳定的关键 |

**设计假设的可证伪性**:
- 若 mamba_hybrid 在 windows=50 上 D1 / D2 也显著退化, 综述 §6 NSA-hybrid 假设受质疑 → 触发 v0.4 spec delta 重新设计 C2
- 若 no_nsa 反而 D1 / D2 比 mamba_hybrid 更稳定, NSA 必要性受质疑 → 触发 NSA 移除考虑
- 若 baseline_cross_attention 在 windows=50 上 OOM 没发生, cross-attention 在 KITTI 真实分布下也能撑住, 综述 §6 NSA 优势变成"非必要优化"而非"载荷设计"

这 3 个 falsifier 是 ablate_recurrence KITTI 长窗扩展的真实价值; 不是为了"证实 NSA-hybrid 优"。

## 7. Validation gate (calibration 启动 DEC 必须满足)

ablate_recurrence KITTI 长窗扩展跑 (如果未来获得独立 DEC 授权) 必须报告以下 6 个 metric 才能 close cycle:

1. **windows=3 baseline 回归**: 用同一 commit + 同一 ablate_recurrence.py + KITTI windows=3 子集跑一遍, 与 cycle 033 W14 合成 windows=3 baseline 在 elapsed_ms_mean 上误差 < 20%。如果显著偏离, code 层有 regression, 不接长窗结果。
2. **D1-D4 度量定义稳定**: 4 个度量在 fixed seed 下重跑两次, 数值差异 < 5%。
3. **B4 子类未覆盖警告**: cycle 输出必须明示"4 变体不覆盖综述 §6 B4 预算治理子类", 避免读者误读 mamba_hybrid 在 windows=100 失败为"NSA-hybrid 整体失败"。
4. **windows 升级单调**: windows=10 跑前必须 windows=3 通过; windows=50 跑前必须 windows=10 通过; windows=100 跑前必须 windows=50 通过 (避免 OOM 浪费 GPU)。
5. **每个变体每个 windows level 至少 3 seeds**: 单 seed 不接受, 避免 seed 敏感导致假信号。
6. **KITTI sequence 选取固定**: calibration 启动 DEC 必须列出具体使用的 KITTI sequence ID, 不允许"运行时挑选"。

不满足任何一项, 该 windows level 结果不接受。

## 8. 资源估算 (engineering-judgment; 非承诺值)

| Windows level | 变体 × seeds | 单跑帧数 | GPU 估时 (per variant per seed) | Total GPU 估时 |
|---|---|---|---|---|
| windows=3 (baseline 回归) | 4 × 3 = 12 | 12 | <1 min | <12 min |
| windows=10 (KITTI-LONG-10) | 4 × 3 = 12 | 40 | ~3 min | ~36 min |
| windows=20 (KITTI-LONG-20) | 4 × 3 = 12 | 80 | ~6 min | ~72 min |
| windows=50 (KITTI-LONG-50) | 4 × 3 = 12 | 200 | ~15 min | ~3 hr |
| windows=100 (KITTI-LONG-100) | 4 × 3 = 12 | 400 | ~30 min (assuming linear; potentially OOM 前要 abort) | ~6 hr |

**Total GPU 估时 (4 windows level 全跑)**: ~10 hours single GPU。

**注**:
- 上表估时基于 KITTI smoke cycle 034 的 2-window 时延外推, 非实测
- 若 baseline_cross_attention 在 windows=100 OOM, 该 cell 实际时长会比估算短 (因 abort)
- 若加入 D2 + D4 instrumentation hook, 单跑时延会增加 5-15% (instrumentation overhead)
- F-002 server 资源使用必须遵循 reference_server_lab_rules.md (don't hog all GPUs); 推荐 single GPU 而非 multi-GPU

## 9. 与 SPEC-20260508-002 memory ablation addendum 的关系

`code/dream3r/ablate_recurrence.py` 4 变体当前对应 SPEC-20260508-002 v0.3 memory ablation addendum 的一个子集 (ABL-memory-1..N 中的 baseline / state recurrence / NSA / stable memory ablation)。本 plan 扩展的是同一组变体在 KITTI 长窗上的真实数据应用; 不引入新的 ablation ID; 不修改 SPEC-20260508-002。

任何 SPEC-20260508-002 范围内的 ABL ID 升级 (从 spec-listed 到 spec-listed + KITTI-verified) 是 calibration 启动 DEC 的输出物, 不是本 plan 的输出。

## 10. 与 cycle 034 KITTI smoke 的关系

cycle 034 KITTI smoke 跑了 `evaluate_real_sequence.py` 在 2 windows 上, 输出 pointmap L2 = 20.47 作为 integration evidence (非质量证明; per CYCLE-20260511-001 cycle log)。本 plan 扩展跑的是 `ablate_recurrence.py` 而非 `evaluate_real_sequence.py`, 焦点是 4 变体对比 (内部 ablation), 不是 Dream3R 整体管线验证 (cycle 034 任务)。

两者不冲突: cycle 034 验证整体 pipeline integration; 本 plan 扩展跑验证 C2 内部记忆机制在长窗下的退化模式。同一启动 DEC 可以同时授权两者, 但 metric 分开报告。

## 11. 不立即做 + 风险

### 11.1 不立即做

- **不启动任何 KITTI 长窗跑** (per F-002 + DEC-20260515-001 §Not authorized)
- **不修改 ablate_recurrence.py / config.py / evaluate_real_sequence.py 任何代码**
- **不新增 B4 预算治理子类变体** (需 spec delta + DEC)
- **不下载 / 预处理 KITTI long sequence subset** (需独立 server DEC)
- **不下结论说哪个变体长窗下最优** — 实证问题, 本 plan 范围外

### 11.2 开放风险

- **R1 (instrumentation overhead)**: D2 / D4 度量需要 NSA branch instrumentation hook, 改动 modules.py 是非小动作 (per RESEARCH_CODE_DISCIPLINE rule 3 Surgical Edits); 启动 DEC 需明示 hook 改动范围。
- **R2 (KITTI long sequence license + storage)**: KITTI raw 数据 + odometry 数据合计在 server-side 已有 /hdd3 存储 (per cycle 034 KITTI smoke), 但 long sequence 跑可能需要更大 cache; 启动 DEC 需 server storage review。
- **R3 (B4 子类空缺误读)**: 若读者把 mamba_hybrid 在 windows=100 退化误读为"NSA-hybrid 整体失败", 而忽略 B4 预算治理子类未覆盖, 会得出错误结论。validation gate §7 metric 3 防御此误读。
- **R4 (设计假设过强)**: §6 expected behavior 表是 design assumption, 实际跑可能反驳全部 4 行。这是 ablation 价值, 不是 plan 缺陷; 但启动 DEC 时需明确"实证结果优先, 不强求与 expected 一致"。
- **R5 (与 SPEC-20260507-002 v0.3 ablation addendum 协调)**: 该 spec 列出 ABL-v02-N 中部分项目与本 plan 重叠 (e.g., NSA ablation = ABL-v02-1); 启动 DEC 应明示与 ABL-v02-N 命名 / 跑序对应关系。

## 12. 下一步 (per DEC-20260515-001 §Next Direction If Passed)

A. 启动独立 DEC 授权 ablate_recurrence KITTI windows=10 → 20 → 50 → 100 阶梯跑
B. 仅授权 windows=10 (最小代价), 看通过后再升级
C. 暂不启动, 优先 CRITIC_CALIBRATION_PLAN_V1 执行
D. 启动 v0.4 spec delta 加入 B4 预算治理子类变体 (LONG3R 风格动态剪枝) 后再扩展跑
E. 修订本 plan
F. 回到 architecture-first mainline 非 survey 工作

DEC-20260506-001 architecture-first mainline + DEC-20260504-002 no-all-in + DEC-20260501-011 thesis reframe + DEC-20260503-001 research-code-discipline + F-002 全部仍在 force; 本 plan 不动。

## 13. Metadata

| 字段 | 取值 |
|---|---|
| 文件路径 | `Dream/planning/LONG_SEQ_REAL_TABLE_PLAN.md` |
| 创建日期 | 2026-05-15 |
| 状态 | v1, draft (plan-only; 执行需独立 DEC + F-002 server 授权) |
| 作者 | Dream agent |
| 上游 | SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §4 P0 + §5 A3 + 综述 §6 长序列内存四类 |
| 授权根 | DEC-20260515-001 (cycle 035 launch; 仅授权写本文件, 不授权执行) |
| 引用 spec (不修改) | SPEC-20260506-005 v0.2 ABL-v02-N / SPEC-20260507-002 v0.3 ablation addendum / SPEC-20260508-001 v0.3 C2 memory / SPEC-20260508-002 memory ablation addendum |
| 引用 paradigm (不修改) | CROSS_SPEC_SIGNAL_CONTRACT v2.1 / RESEARCH_CODE_DISCIPLINE rule 3 (Surgical Edits) + rule 5 (Honesty Override) |
| 引用代码状态 (不修改) | `code/dream3r/ablate_recurrence.py` (4 variants) / `code/dream3r/RECENT_PROGRESS.md` W14 / `code/dream3r/NEXT_PHASE_ROADMAP.md` W21 |
| 引用 cycle | CYCLE-20260510-001 (cycle 033 W14) / CYCLE-20260511-001 (cycle 034 KITTI smoke 2 windows) |
| 下游候选 | KITTI 长窗跑启动 DEC (如批准) → ablate_recurrence KITTI verified extension → B4 子类变体 v0.4 spec delta 起草素材 |
| 不下游 | 任何 server 跑 / code change / spec change 在本 cycle 035 |

---

**End of Long-Seq Real-Data Table Plan.** 本文件是 cycle 035 P0-3 deliverable; 任何 KITTI 长窗跑启动需独立 DEC + per-step gate + F-002 server 授权。
