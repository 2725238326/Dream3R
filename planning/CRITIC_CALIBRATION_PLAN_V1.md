# Critic Calibration Plan V1: Per-Failure-Mode Threshold Standardization

| 字段 | 取值 |
|---|---|
| 文件类型 | planning artifact (非 spec, 非决策, 非执行授权) |
| 创建日期 | 2026-05-15 |
| 状态 | v1, draft (plan-only; 执行需独立 DEC) |
| 上游 | `planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md` §4 P0-1 + 综述 §10 六类失败模式段 |
| 授权根 | DEC-20260515-001 (cycle 035 launch; 仅授权写本文件, 不授权执行) |
| 触及范围 | 仅本文件; 不动 `code/dream3r/config.py`, 不动 SPEC, 不动 paradigm/CROSS_SPEC_SIGNAL_CONTRACT |

## 1. Goal

Dream3R v0.3 C4 Critic (per SPEC-20260506-004 v0.2 §C4) 当前发布单一标量 `conflict_score(t)`, threshold `theta_conflict` 标注为 `inferred`, 没有 per-failure-mode 分层 (per `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v2.1 §Critic-publishes)。综述 §10 首段指出 3R 系统在六类几何条件下失败原因不同, 单一阈值无法捕捉子类差异。

本 plan 设计一套 per-failure-mode threshold standardization 流程:

1. 把综述六类失败模式 (弱纹理 / 镜面玻璃 / 快速运动 / 长基线 / 尺度漂移 / 域外) 映射到 C4 Critic 的现有信号通道 (Sampson / depth consistency / 共视 / reprojection / confidence)
2. 为每个失败模式定义 sub-sample 采样规则 (在哪些数据集 / 哪些场景 / 用什么标签选取代表性子集)
3. 描述两种 threshold 学习方法 (distribution-quantile vs supervised) 的适用边界 + 选型依据
4. 给出 calibrated threshold 表的 schema + 如何被 C4 Critic 在 inference 时读取
5. 给出 validation gate 让"标定过的 threshold" 与"v0.3 默认 threshold" 在同一个 KITTI smoke 上对比, 避免回归

**本 plan 不做的事** (per DEC-20260515-001 §Required Boundary):

- 不修改 `code/dream3r/config.py` 中任何 threshold 默认值
- 不启动 calibration data collection 跑 (需独立 DEC + F-002 server 授权)
- 不修改 SPEC-20260506-004 v0.2 §C4 Critic 任何 contract
- 不修改 `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v2.1 (即不引入 CR-7 / CR-8)
- 不下结论说"per-mode threshold 优于 single threshold" — 这是 A4 验证质量的实证问题, 本 plan 只设计验证流程

## 2. C4 Critic 当前 threshold 状态 (recap from spec)

per SPEC-20260506-004 v0.2 §C4 + CROSS_SPEC_SIGNAL_CONTRACT v2.1:

```text
Critic 发布 conflict_score(t) = scalar, 由以下 5 个子信号聚合 (weights inferred):
  - pose_novelty
  - view_overlap (共视)
  - reprojection_residual (Sampson 类)
  - pointmap_conflict (depth consistency)
  - confidence_drop

Critic threshold theta_conflict 当前:
  - 单一标量
  - 标注 inferred (不从训练数据学得, 不来自 cross-validation)
  - 在 v0.3 默认 config 中以一个 magic number 出现

Critic 输出 recommended_action ∈ {accept, rerun_local_region, reroute_model,
                                    open_anchor_budget, request_prior,
                                    conflict_unresolved}
```

**关键缺陷** (per 综述 §10): 5 个子信号在 6 类失败模式下的分布完全不同。例如 reprojection_residual 在"长基线"场景下天然偏高 (大视差正常现象), 但在"弱纹理"场景下偏低 (匹配点稀疏导致 residual 失真); 单一 theta_conflict 必然在某些子类过严, 某些子类过松。

## 3. 六类失败模式 → 信号通道映射

| 失败模式 | 主信号通道 | 次信号通道 | 子类特征 (per 综述 §10) |
|---|---|---|---|
| A1 弱纹理 | confidence_drop | reprojection_residual (反向) | 匹配点稀疏; reprojection 失真; confidence head 低 |
| A2 镜面玻璃 | pointmap_conflict | depth-RGB 不一致 (proposed CR-7 if 引入) | 反射几何与真实几何二值区分; pointmap depth ≠ visual depth |
| A3 快速运动 | pose_novelty | dynamic_ratio (来自 Permanence) | 帧间 pose 变化大; dynamic_ratio 高 |
| A4 长基线 | view_overlap (反向, 低) | reprojection_residual (基线放大效应) | 共视区域小; 大视差 |
| A5 尺度漂移 | latent_drift_proxy (Memory 发布) | confidence_drop (累积) | 长序列累积; drift proxy 单调上升 |
| A6 域外 (OOD) | confidence_drop (全局低) | route_regret_estimate (Composer 发布; 高 = 池中无适配 expert) | 训练分布外; capability_match 全局低 |

**注**: A2 (镜面玻璃) 主信号是 pointmap_conflict, 次信号需要 visual-depth-vs-pointmap-depth 一致性检查, 这个 channel 当前不存在 (是 proposal §5 C2 "CR-7 候选" 的内容)。本 plan 在 A2 上只用现有通道 (pointmap_conflict 单通道), 不假设 CR-7 存在。

## 4. Sub-sample 采样规则

每个失败模式需要 1 个独立的 sub-sample set 用于 threshold 标定。

| 失败模式 | 候选数据源 | 标签规则 | 目标 sample 数 |
|---|---|---|---|
| A1 弱纹理 | ScanNet / 7-Scenes / 室内 KITTI | 选取 texture variance < 阈值 的窗 (光度方差低) | ≥ 200 窗口 |
| A2 镜面玻璃 | GlassRGBD / Trans10K / 用户挑选的特定 KITTI 场景 | 镜面 / 玻璃 manual mask 或语义分割 mask 标签 | ≥ 100 窗口 |
| A3 快速运动 | TUM Dynamic / KITTI 加速段 | inter-frame translation > 阈值 或 motion blur 标签 | ≥ 200 窗口 |
| A4 长基线 | MegaDepth / KITTI 大转角段 | 帧间 baseline > 阈值 (相对场景尺度) | ≥ 200 窗口 |
| A5 尺度漂移 | KITTI 全序列 / TUM 长录制 | 窗 ≥ 10 (long-sequence) + 已知 ground-truth scale drift | ≥ 50 序列 |
| A6 域外 (OOD) | Co3D / DyCheck / aerial 数据集 (训练分布外) | 训练集 (KITTI + ScanNet) 之外的几何域 | ≥ 100 窗口 |

**注**:
- 上表的"候选数据源"全部是 server-side 数据 (per F-002, 任何下载需独立 DEC)
- 上表的 sample 数是 plan-level estimation, 不是承诺值
- 任何"用户挑选的特定 KITTI 场景" 需独立 DEC 授权 manual labeling 工作量
- 本 plan 不规定 dataset license 处理, license 检查在 calibration 启动 DEC 时单独 review

## 5. Threshold 学习方法

### 方法 A: Distribution-quantile (无监督, 推荐 P0 起步)

**步骤**:
1. 对每个失败模式 sub-sample, 跑现有 C4 Critic, 收集每个窗的 5 个子信号值 (pose_novelty / view_overlap / reprojection_residual / pointmap_conflict / confidence_drop)
2. 对每个子信号在 sub-sample 上画分位数直方图
3. 选 P95 (或 P90) 作为该子类 "conflict" 阈值
4. 输出 per-mode-per-signal threshold 表 (5 signals × 6 modes = 30 个 scalar)

**优点**: 不需要 ground-truth 几何错误标签, 只需 sub-sample 划分; 工作量低。
**缺点**: P95 是经验值, 不一定是最优分界点; 假设"该子类大部分样本是 conflict 状态", 不一定成立 (例如 A1 弱纹理子样本中大部分窗可能仍是正常重建)。

### 方法 B: Supervised (per-mode binary classifier; 推荐 P1 升级)

**步骤**:
1. 对每个失败模式 sub-sample, 跑 C4 Critic 收集 5 个子信号
2. 同时获取 ground-truth 几何错误标签 (per-pixel L2 > 阈值 或 manual mark)
3. 训练一个 6-way (or 7-way 包含 "正常") classifier, 输入 5 子信号, 输出失败模式概率分布
4. 部署: classifier 概率 → 6 个 mode-specific conflict score (代替 single conflict_score), C4 Critic 用 per-mode threshold 触发 repair action

**优点**: 可以处理 mode-mixing (一个窗同时有弱纹理 + 长基线); 输出更精确的 conflict reason。
**缺点**: 需要 ground-truth 几何错误标签 (P0 阶段不一定有); classifier 本身需要训练; 推理时增加额外 forward pass (虽然轻量)。

### 方法选型决策树

```text
是否有 ground-truth per-pixel L2 标签?
├── 否 -> 起步用方法 A (P0)
│         如果 A 的 P95 阈值在 KITTI smoke 上比 single theta_conflict 改进 < 10%
│         (per 6.4 validation gate), 不强行升级到方法 B; 保留 single threshold
└── 是 -> 直接用方法 B (P1)
         需要 v0.4 spec delta 在 C4 Critic 输出契约中加 mode-distribution
         (per proposal §5 B1 v0.4 spec delta)
```

P0 cycle (此 plan 范围) 只设计方法 A 的执行流程, 方法 B 的训练流程 outline-only。

## 6. Per-mode threshold 表 schema

calibration 跑完后输出的 YAML / JSON 表 schema:

```yaml
schema_version: v1
created: <date>
calibration_method: distribution_quantile_P95   # or supervised_binary
upstream_subsamples:
  - mode: A1_weak_texture
    dataset: <source>
    n_windows: <int>
    label_rule: <description>
  ...
per_mode_thresholds:
  A1_weak_texture:
    pose_novelty: <float>
    view_overlap: <float>
    reprojection_residual: <float>
    pointmap_conflict: <float>
    confidence_drop: <float>
    aggregate_conflict_threshold: <float>   # if scalar aggregation kept
  A2_specular: ...
  A3_fast_motion: ...
  A4_long_baseline: ...
  A5_scale_drift: ...
  A6_ood: ...
default_fallback:   # for samples not classified into any of A1-A6
  conflict_threshold: <float>   # = current v0.3 default
provenance:
  calibration_run_id: <uuid>
  calibration_dec_id: <DEC-YYYYMMDD-NNN>
  server_session: <session_id>
```

**注**: 此 schema 是 plan-level; 落地为 YAML 需 calibration 跑后, 跑前后的 schema 评审是独立 DEC 的事。

## 7. C4 Critic inference-time 读取流程

calibrated threshold 表如何被 C4 Critic 在 inference 时使用 (设计 outline, 不实装):

```text
1. C4 Critic 接受当前窗 t 的 5 个子信号 + 当前窗的 mode_estimate
   (mode_estimate 来自方法 A 的 P95 trigger 或方法 B 的 classifier)
2. C4 Critic 用 per_mode_thresholds[mode_estimate] 替代单一 theta_conflict
3. conflict_score 计算保留现有 v0.3 公式 (5 子信号 inferred weights), threshold 应用层 swap
4. recommended_action 路径:
   - if 任意子信号超过 per_mode_thresholds[mode_estimate]: 触发对应 mode 的 repair action
     (e.g., A1 触发 request_prior; A4 触发 reroute_model; A5 触发 open_anchor_budget)
   - if 无 mode 匹配 (route_regret_estimate 高): fallback 到 conflict_unresolved
```

**注**:
- mode_estimate 的精度直接决定 per-mode threshold 是否有效。若 mode_estimate 错分 (e.g., 把 A4 长基线错分为 A1 弱纹理), per-mode threshold 反而不如 single threshold。validation gate (§6.4) 必须覆盖 mode_estimate 错分率。
- repair action 的 mode → action 映射是 design hypothesis, 需要 v0.4 spec delta 落实 (per proposal §5 B1)。本 plan 把映射列为 design candidate, 不固化。

## 8. Validation gate (calibration 启动 DEC 必须满足的条件)

calibration 跑 (如果未来获得独立 DEC 授权) 必须报告以下 5 个 metric 才能 close cycle:

1. **mode_estimate 准确率**: 在 6 个 sub-sample 上, mode_estimate 应该把样本归到对应 mode 至少 80%(P0 起步) / 95%(P1 升级) 的窗。
2. **per-mode P95 与 single theta_conflict 在 KITTI 2 窗 smoke 上的对比**: 若 per-mode 比 single 在 pointmap L2 上没有改进 (KITTI cycle 034 baseline L2=20.47), 不升级到 calibrated config。
3. **重复实验**: 在 fixed seed 下重跑两次 calibration, P95 阈值差异 < 5% (避免 seed 敏感)。
4. **dataset license 链清**: 每个数据集的 license 必须在 calibration 启动 DEC 中单独标注。
5. **fallback 路径完整**: 如果 mode_estimate 无法把窗归到任何 mode, default_fallback 必须使用 v0.3 默认 single threshold, 不能 silently 触发未知 repair action。

不满足任何一项, calibration 跑应该被回滚, calibrated config 不被 commit 到 `config.py`。

## 9. 与 CROSS_SPEC_SIGNAL_CONTRACT v2.1 的关系

本 plan 不引入新的 CR signal channel。所有 calibration 工作发生在 C4 Critic 内部 (subsignal 收集 + threshold table + mode_estimate 计算), Critic 对外发布的接口仍是 conflict_score + recommended_action (per CROSS_SPEC_SIGNAL_CONTRACT v2.1 §Critic-publishes 不变)。

唯一对接 contract 的可能扩展: 若方法 B (supervised) 部署 mode-distribution 输出 (per proposal §5 B1 v0.4 spec delta), 需 CROSS_SPEC_SIGNAL_CONTRACT 升级到 v2.2 加 `mode_distribution` 新 signal。但这是 v0.4 spec delta 范围, 不在本 plan 内。

## 10. 不立即做 + 风险

### 10.1 不立即做

- **不启动 calibration 跑**: 任何 server-side 数据收集 / threshold 训练需独立 DEC + F-002 server 授权。本 plan 是 markdown deliverable。
- **不修改 config.py**: per DEC-20260515-001 §Not authorized 明确禁止。
- **不假设 CR-7 (mode-distribution) 已经存在**: 本 plan 在现有 5 子信号 + 单 conflict_score 的 contract 上设计。
- **不下结论说 single threshold 应该被替换**: 替换决策需要 calibration 跑后的 validation gate 通过。

### 10.2 开放风险

- **R1 (mode 错分级联)**: mode_estimate 错分会让 per-mode threshold 反而退化 (e.g., A4 错分为 A1 触发错误 repair)。validation gate §6.4 metric 1 + 2 共同约束。
- **R2 (sub-sample bias)**: ScanNet/7-Scenes 室内, KITTI 城市, Co3D 物体级 — 任何一个 sub-sample 都可能不代表实际 OOD 分布。calibration 跑应使用 cross-dataset hold-out 验证 (不是简单 train/test split 在同一 dataset 内)。
- **R3 (label 工作量)**: A2 镜面玻璃 + A5 尺度漂移 + A6 OOD 三个 mode 的 ground-truth label 需要 manual annotation 或来自有限的标注数据集 (GlassRGBD / DyCheck), 工作量级别在 calibration 启动 DEC 时单独评估。
- **R4 (与 SPEC-20260507-002 v0.3 ablation addendum 的关系)**: 若 ABL-v02-N 中已经有针对 single theta_conflict 的 ablation (ABL-v02-1 NSA-removal 是相关的), calibration 跑不应与 ABL 跑同时启动 (避免变量混淆)。calibration 启动 DEC 应说明与 ABL 时序关系。
- **R5 (与 proposal §5 B1 v0.4 spec delta 的关系)**: 本 plan 设计方法 A 起步, 不预设方法 B。若用户后续批准 B1 v0.4 spec delta (C4 Critic 拆分为验证 + TTT), 本 plan 的方法 A 输出可作为方法 B classifier 的初始训练数据。

## 11. 下一步 (per DEC-20260515-001 §Next Direction If Passed)

A. 启动独立 DEC 授权 calibration data collection on KITTI / ScanNet / 选定子集 -> 此 plan 进入执行
B. 暂不启动 calibration, 优先 LONG_SEQ_REAL_TABLE_PLAN 执行 -> 此 plan 进入 hold
C. 启动 v0.4 spec delta B1 (C4 Critic 拆分 + mode_distribution) -> 此 plan 的方法 A 流程为 B 的训练数据准备阶段
D. 暂停 + 修订本 plan
E. 回到 architecture-first mainline 非 survey 工作

DEC-20260506-001 architecture-first mainline + DEC-20260504-002 no-all-in + DEC-20260501-011 thesis reframe + DEC-20260503-001 research-code-discipline 全部仍在 force; 本 plan 不动。

## 12. Metadata

| 字段 | 取值 |
|---|---|
| 文件路径 | `Dream/planning/CRITIC_CALIBRATION_PLAN_V1.md` |
| 创建日期 | 2026-05-15 |
| 状态 | v1, draft (plan-only; 执行需独立 DEC) |
| 作者 | Dream agent |
| 上游 | SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §4 P0-1 + 综述 §10 |
| 授权根 | DEC-20260515-001 (cycle 035 launch; 仅授权写本文件, 不授权执行) |
| 引用 spec (不修改) | SPEC-20260506-004 v0.2 §C4 Critic / SPEC-20260506-005 v0.2 (ABL-v02-1) / SPEC-20260507-002 v0.3 ablation addendum |
| 引用 paradigm (不修改) | CROSS_SPEC_SIGNAL_CONTRACT v2.1 §Critic-publishes / RESEARCH_CODE_DISCIPLINE rule 3 (Surgical Edits) + rule 5 (Honesty Override) |
| 引用代码状态 (不修改) | `code/dream3r/config.py` 中 conflict_threshold 默认值 / `code/dream3r/RECENT_PROGRESS.md` W15 |
| 下游候选 | calibration 启动 DEC (如批准) -> calibrated config -> v0.4 B1 spec delta 起草素材 |
| 不下游 | 任何 server 跑 / config commit / spec change 在本 cycle 035 |

---

**End of Critic Calibration Plan V1.** 本文件是 cycle 035 P0-1 deliverable; 任何 calibration 启动需独立 DEC + per-step gate + F-002 server 授权。
