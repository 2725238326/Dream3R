# Dream3R 开题报告（内部稿 V1）

| 字段 | 取值 |
|---|---|
| 文件类型 | 开题报告内部稿 (Dream-vocabulary; 不外发) |
| 创建日期 | 2026-05-16 |
| 最后更新 | 2026-05-17 (expansion cycle: 双支柱扩展; §1-§9 累计正文 ~27000 字) |
| 状态 | v1.1 draft; §1-§9 + 支柱 B KYKT 平台内容扩展完成 |
| 授权根 | DEC-20260516-001 (cycle 036) + DEC-20260516-002 (cycle 037) + DEC-20260516-003 (cycle 038) + DEC-20260516-004 (cycle 039) + DEC-20260517-001 (cycle 040) + DEC-20260517-002 (cycle 041) + DEC-20260517-003 (cycle 042) |
| 配套文件 | OUTLINE_V1.md (章节结构) + STYLE_CONTRACT.md (双稿契约) + DRAFT_EXTERNAL_V1.md (外部稿) |
| 双稿关系 | 本稿是 master per STYLE_CONTRACT §3 规则 1; 外部稿是 internal 周期性快照 |
| 词汇 | 含 Dream / Dream3R / cycle / SPEC / DEC / CR / W-task / Track A / Track B / 服务器 path / agent 等 |

---

## §1 项目背景与研究问题

### 1.1 Track A 主线决策起源

Dream3R 项目 (内部代号 Dream, 架构产品 Dream3R) 的研究方向于 2026-05-06 经 DEC-20260506-001 user-locked 后定型为 architecture-first 主线: 设计新的 3R (前馈式三维重建) 架构作为 markdown spec + ablation plan + comparator map, 把架构本身作为 PRIMARY output; 论文写作降为 SUPPORT artifact。

这一决策的 5 个 in-force constraint 共同约束本开题报告:

- DEC-20260506-001 (architecture-first mainline) — 主线是架构而非论文
- DEC-20260504-002 (no-all-in) — 4 个 finalist 机制 (Critic / Memory / Permanence / Composer) 不收敛到任一单一 finalist
- DEC-20260501-011 (Dream3R thesis reframe; candidate-not-final) — Dream3R 是 candidate 架构, 非最终方案
- DEC-20260503-001 (research-code-discipline) — 5 条纪律 (尤其 rule 3 surgical edits + rule 5 honesty override) 约束本研究的所有 spec / code / cycle 操作
- F-002 (server-side discipline) — KYKT 3R 模型工作在 /hdd3/kykt26/code/dream3r/ 远端服务器执行; 本地 Windows 仅作 markdown + 编排

### 1.2 Dream3R v0.3 当前状态

Dream3R v0.3 主线截至 2026-05-16 处于以下状态:

- **架构定型 (markdown 层)**: SPEC-20260506-004 v0.2 完整定义 6 个核心模块 — C1 Perceiver (DINOv3-S frozen backbone; ViT-L → DINOv3-S 替换 per Delta 2, ~14x 参数减少 + ~5x 延迟加速) + C2 Memory (NSA three-branch 即 compressed/selected/sliding 三分支 + AnchorBank K=256 + StateToken; SPEC-20260508-001 v0.3 addendum) + C3 Permanence (Slot Attention + permanence_link) + C4 Critic (Sampson 几何 / depth 一致性 / 共视 conflict 三类信号 + repair actions 0/1/2 stub 3/4/5) + C5 Composer (7 expert pool: MASt3R + Fast3R + Spann3R + CUT3R + MoGe-2 + DepthAnything-V2 + Test3R; per Delta 5 + COMPOSER_CAPABILITY_DESCRIPTORS) + C6 Bus (CR-1..CR-6 cross-spec signal contract v2.1 per `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md`)
- **比较图谱定型**: SPEC-20260507-001 v0.2 把 19 个 comparator entry 重组为 5 tier (in-pool 7 / out-of-pool 3 / out-of-scope 1 / foundation 1 / orthogonal 8); 引入 Axis 9 NSA / Axis 10 DINOv3 / Axis 11 Composer pool 三个新轴
- **消融计划定型**: SPEC-20260506-005 v0.2 ABL-v02-1..9 + SPEC-20260508-002 ABL-memory-0..11 (后者 cycle 029 review 后 v1.1 修订)
- **代码实装 (服务器层)**: cycle 033 W1-W16 + cycle 034 W17-W18 完成。W1-W18 含 DINOv2 backbone (实际跑) + 3D-aware retrieval + active/stable state + Grassmannian 正则化 + 几何 Critic + ISA slot + 真实 MASt3R + Spann3R adapter + W17 Mamba-Transformer 混合循环 + W18 GaussianHead tensor 契约 (renderer-free)。代码部署在 /hdd3/kykt26/code/dream3r/
- **真实数据集成证据 (非质量证明)**: cycle 034 跑 evaluate_real_sequence.py on KITTI 真实序列 2 windows, pointmap L2 = 20.47。此数值作为系统集成证据 (端到端 pipeline 跑通), 非训练后质量。
- **ablation 现状**: ablate_recurrence.py 实装 4 变体 (baseline_cross_attention / mamba_hybrid / no_nsa / no_stable_memory), 在合成数据 windows=3 跑过。ABL-memory-0 通过 (cycle 031 local P0 scaffold)。其他 ABL 待启动。
- **现有 gated 项**: 真实数据训练 / 3DGS 渲染 / DTU 加载器 / Fast3R omegaconf 依赖 / 真实 CUT3R / MoGe-2 / DepthAnything-V2 / Test3R 加载 / TTT 路径 / W19-W30 等

### 1.3 Track B 综述四轴判断的反哺

Track B 3R-mix 中文综述于 2026-05-14 按 route C (arXiv-only) wound down, 18 A4 页 / 44 引文 / 6 图 5 表 / 0 编译错误。综述识别了 3R 研究方向的四轴判断:

- **轴 A: 六类典型几何失败模式** (综述 §10 首段) — 弱纹理 / 镜面玻璃 / 快速运动 / 长基线 / 尺度漂移 / 域外
- **轴 B: 长序列内存四类机制** (综述 §6) — 空间指针 (Point3R 类) / causal-autoregressive (CUT3R / STream3R 类) / hybrid memory (NSA-hybrid 类) / 预算治理与滤波 (LONG3R 类)
- **轴 C: 测试时机制三类区分** (综述 §7) — 一致性优化 (Test3R 类) / TTT 参数更新 (TTT3R 类) / 先验注入位置区分 (G-CUT3R / Pow3R / MASt3R-SfM 类)
- **轴 D: 输出资产三类** (综述 §8) — 4D pointmap / dynamic mask / 4DGS asset

cycle 035 (2026-05-15) 把这四轴判断映射到 Dream3R v0.3 架构上, 输出 4 个 markdown deliverables (planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md + SOTA_MATRIX_V2.md + CRITIC_CALIBRATION_PLAN_V1.md + LONG_SEQ_REAL_TABLE_PLAN.md) + WORK_RISK_REGISTER v1.1 (+4 行: R-OOD-1 / R-EXT-PRIOR-1 / R-4DGS-LIC-1 / R-INPUT-EXT-1)。

综述与 Dream3R 主线关系是单向反哺 (综述 → 主线), 综述 manuscript 在 2026-05-14 wound down 后未受到主线后续工作回流污染 (per Dream/3R-mix/deliverables/RELATION_TO_TRACK_A_2026-05-16.md)。

### 1.4 三个核心研究问题

基于综述四轴判断 + Dream3R v0.3 架构覆盖矩阵 (SOTA_MATRIX_V2 §6 + SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §3 显示 21 子类中 ✓ 6 / ⚠ 11 / ✗ 4), 本研究聚焦三个核心研究问题:

**Q1 验证机制的架构层落地 (Critic 路径; 轴 A + 轴 C)**: 综述 §7 区分 "一致性优化 (Test3R 风格, 无参数更新)" 与 "TTT 参数更新 (TTT3R 风格)" 两类测试时机制。Dream3R v0.3 当前 C4 Critic 是 "验证 + 修复" hybrid, 独立的一致性优化循环未拆出。本研究问: 把验证 (geometric_conflict scoring + repair suggestion) 与适应 (parameter update) 在架构层拆为两条路径, 是否优于 hybrid 配置? (对应 SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §5 B1 v0.4 spec delta 候选)

**Q2 长序列内存四类机制的架构层统一 (Memory 路径; 轴 B)**: 综述 §6 把长序列内存分为 4 类机制, 现有系统每个只占一档 (Point3R = 空间指针; CUT3R = causal-AR; NSA-hybrid 类 = hybrid memory; LONG3R = 预算治理)。Dream3R v0.3 C2 Memory 通过 NSA three-branch + AnchorBank K=256 + StateToken 已覆盖前 3 类 (✓ 空间指针 / ✓ causal-AR / ✓ hybrid memory), 第 4 类 (预算治理) ⚠ partial (帧预算约束接口存在但动态剪枝未对比)。本研究问: 在单一 C2 Memory 架构中同时实装 4 类机制是否可行? 4 类机制间的协同 / 冲突如何在 ablate_recurrence + LONG_SEQ_REAL_TABLE_PLAN V1 KITTI 长窗 (windows ≥ 10) 下显现?

**Q3 多专家组合是否优于单一 expert (Composer 路径; 轴 D + 综述 §3 best-of-N)**: Dream3R v0.3 C5 Composer 7-expert pool (per Delta 5) 是 architecture novelty 之一 (per SPEC-20260507-001 v0.2 pillar D heterogeneous best-of-N)。但综述 §3 + §6 显示这些 expert 各自在不同 regime 上有优势 (MASt3R 静态对 / Fast3R 多视图 / Spann3R 流式 / etc.), 组合是否真的优于单一 expert 是 ABL-v02-4 的 Tier 1 load-bearing 问题。本研究问: 在 KITTI 真实数据上, 多专家 best-of-N 路由是否在 pointmap L2 + route_regret 指标上显著超越单一 expert? 与 Test3R 内置 verifier 组合时, C4 Critic 的额外价值边际如何?

### 1.5 候选 vs 最终的边界

per DEC-20260501-011 (thesis reframe, candidate-not-final) + DEC-20260504-002 (no-all-in), Dream3R 是被评估的候选架构, 非项目收敛方案。本研究的成果不是论证 Dream3R 相对 SOTA 具有压倒性优势, 而是评估 Dream3R 在 Q1 / Q2 / Q3 三组维度上的表现, 为后续 v0.4 spec delta 演进或被替换提供实证依据。

### 1.6 Dream 项目工件引用

本节直接引用的工件:

- `Dream/decisions/DEC-20260506-001-mainline-architecture-first.md` (Track A 主线决策)
- `Dream/decisions/DEC-20260501-011-dream3r-thesis-reframe.md` (candidate-not-final)
- `Dream/decisions/DEC-20260504-002-no-all-in-on-single-finalist.md` (no-all-in)
- `Dream/decisions/DEC-20260503-001-research-code-discipline.md` (5 条纪律)
- `Dream/decisions/DEC-20260515-001-cycle-035-survey-driven-markdown-deliverables-launch.md` (综述反哺主线)
- `Dream/specs/SPEC-20260506-004-dream3r-architecture-v02.md` v0.2 (6 模块 + 6 Delta)
- `Dream/specs/SPEC-20260508-001-dream3r-c2-memory-v03-addendum.md` v0.3 (C2 NSA + AnchorBank)
- `Dream/specs/SPEC-20260507-001-dream3r-comparator-map-v02.md` v0.2 (Tier 1-5 + Axis 9-11)
- `Dream/3R-mix/deliverables/3r_survey_stage_final_2026-05-15_natural.pdf` (Track B 综述 deliverable)
- `Dream/planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md` (cycle 035 综述驱动优化提案)
- `Dream/planning/SOTA_MATRIX_V2.md` (综述四轴 + 输入扩展 axis re-label)
- `Dream/code/dream3r/RECENT_PROGRESS.md` (W1-W18 ledger)
- `Dream/cycles/CYCLE-20260511-001.md` (cycle 034 KITTI smoke 实证)

### 1.7 支柱 B: KYKT 聚合管理平台的研究必要性

随着前馌式三维重建从 DUSt3R 单一基准方法演化为 MASt3R / MonST3R / Spann3R / Fast3R / CUT3R / Align3R 等多模型并行演进的局面, 研究者面临日益尖锐的工程管理挑战: 每个模型拥有独立的 Python 环境 / CUDA 依赖 / 检查点路径 / 推理脚本 / 输出格式, 模型间的横向对比需要大量重复性工程労动。这一局面与 Dream3R v0.3 C5 Composer 7-expert pool 的架构设计直接相关: 消融实验的多专家对照、Critic 标定、长序列评测都需要一个统一的平台来调度执行、归集结果、组织对比。

KYKT 聚合管理平台 (Coding/4.06/vision_ui) 作为本项目的第二支柱, 为 Dream3R 架构研究提供工程基础设施:

- **统一模型注册与执行合同**: 通过 model_registry + runner 合同 + job.json / status.json / scene_meta.json 统一输出结构, 让 6+ 个 3R 模型共享同一套调度、结果归集、评估流水线
- **研究闭环支撑**: Dream3R 的消融实验 (ABL-v02-1..10 / ABL-memory-0..11) 、Critic 标定 (CRITIC_CALIBRATION_PLAN_V1) 、长序列评测 (LONG_SEQ_REAL_TABLE_PLAN) 均可通过 KYKT 平台的远端 SSH 调度执行, 本地桌面端实时跟踪状态与结果
- **应用对接层 (候选)**: 后续将模型推理封装为 REST/gRPC 接口, 对接三维重建下游应用 (点云编辑 / AR / 数字孪生 等), 形成研究→工程→应用的完整链路

两大支柱的关系: Dream3R 架构 (支柱 A) 提供算法创新, KYKT 平台 (支柱 B) 提供工程平台; Dream3R 的消融/评测需要 KYKT 平台调度执行, KYKT 平台的核心价值 = 为 Dream3R 等新架构提供标准化实验环境。本研究把支柱 B 作为项目主体问题之一 (§3 Q4), 而非仅仅工程贡献。

---

## §2 比较谱系与现状

本章在 Track B 3R-mix 中文综述 (Dream/3R-mix/main.tex §2-§9, 18 A4 页, 44 引文) 的基础上重新组织前馈式三维重建 (3R) 的比较谱系, 并在 §2.7 给出综述四轴覆盖矩阵下 Dream3R v0.3 的落点。综述文本本身已 wound down 至 route C arXiv-only 状态 (per cycle 034 + 2026-05-15 prose naturalization deliverable), 本章对其素材作 paraphrase + 结构重组, 不引入综述未触及的新引文。素材锚点逐子节给出。

### 2.1 基础谱系: DUSt3R / MASt3R / MASt3R-SfM 系

DUSt3R (2024) 作为 3R 范式起点提出了 pose-free 稠密点图回归 (per 综述 §3 + tab:foundation 第 1 行), 把图像对映射到稠密三维点图并以置信度反映可靠性, 多视角输入则通过成对预测 + 全局对齐组织。其能力来源于先前 CroCo 跨视角补全自监督预训练所学到的 cross-view 对应能力 (综述 §3 段 1)。新表示的代价是把长序列 / 动态物体 / 遮挡 / 尺度漂移 / 大规模多图等遗留问题推到了下游。

MASt3R (2024) 在 DUSt3R 基础上叠加 dense local feature head, 把描述子直接绑定到三维几何, 使匹配同时受 descriptor 局部判别性与 pointmap 全局几何约束 (综述 §3 段 2)。MASt3R-SfM 进一步把这一匹配能力接回经典 SfM 全局重建。这条支线提示: 3R 表示提供更强先验之后, 传统几何并未被取代而是以新接口回到系统 — 匹配 / 检索 / bundle adjustment 仍在, 输入条件与约束方式发生了变化。

Dream3R v0.3 C5 Composer 7-expert pool (per SPEC-20260506-004 v0.2 Delta 5 + COMPOSER_CAPABILITY_DESCRIPTORS) 显式接受 MASt3R 作为 in-pool 静态对几何专家 (per SPEC-20260507-001 v0.2 Tier 1 in-pool 7); MASt3R-SfM 进入 §2.5 测试时机制讨论。DUSt3R 本身在 SPEC-007 v0.2 中标注为 Tier 4 foundation (基础范式, 不直接进入 expert pool 比较)。

### 2.2 多视角规模化与统一视觉几何

把视角数推上去构成 DUSt3R 类方法的第一类工程压力 (综述 §4 + tab:foundation 后半)。Fast3R 走 many-view one-forward-pass 路线, 单 A100 上扩展至 1500 视角级别前馈重建; MV-DUSt3R+ 在稀疏视角 (12 / 20 视角) 上通过多视角 decoder 与 cross-reference fusion 完成单阶段重建。这两种规模压力方向相反, 都要在"多图汇聚"与"成对对齐"间重新分配计算预算。

VGGT (2025) 把 camera / depth / pointmap / tracks 放在同一视觉几何预测框架下, 把 3R 从"点图重建模型"扩展为"通用几何预测模型" (综述 §4 段 2)。MapAnything 在 metric feed-forward reconstruction 基础上允许内参 / 位姿 / 深度 / 部分重建等多种可选条件作为输入; Pow3R 直接把 camera 与 scene priors 当作可选模态进入前馈预测 (per 综述 §4 + §7)。约束变强了, 条件依赖与先验冲突也跟着进来。

Dream3R v0.3 在比较图谱 (SPEC-20260507-001 v0.2) 中把 Fast3R / MASt3R 列入 Tier 1 in-pool 7 expert; VGGT 列入 Tier 2 out-of-pool dropped (per Delta 5 + DEC-20260507-001 reasons: VGGT offline-batch 与 streaming budget 不兼容); MapAnything 列入 Tier 5 orthogonal (输入扩展 axis 与 v0.3 单图 + 序列输入接口正交)。Pow3R 列入 Tier 5 orthogonal 同时被 cycle 035 SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §3 + SOTA_MATRIX_V2 §6 标注为输入扩展 axis 候选 (R-INPUT-EXT-1 风险源头, 见 §9 风险章节)。

### 2.3 视频、动态场景与 4D 重建

静态场景假设是许多三维重建流程的隐含前提 (综述 §5 + tab:dynamic)。视频输入中一旦出现移动物体 / 非刚体 / 相机快速运动, 单一静态点图会把时间变化错误吸收进几何结构。Align3R 从动态视频单目深度对齐入手 (借 Depth Anything 等深度先验为跨帧一致性提供约束); MonST3R 在 DUSt3R 风格点图上微调, 输出 per-frame geometry + dynamic confidence/mask; POMATO 把 pointmap matching 与 temporal motion 结合; D²USt3R 把动态场景扩展到 4D pointmap; Easi3R 走推理时注意力调整路线, 从既有 DUSt3R 表征中分离运动 (training-free dynamic correction); RayMap3R 利用 RayMap 与图像双分支对比, 借静态偏置识别动态干扰。

注意 4D pointmap 与 dynamic mask 是几何中间量, 4DGS 是可渲染表示 — 两者落到下游做的事并不一样 (此区分在 §2.6 输出资产章节展开)。

Dream3R v0.3 C3 Permanence (Slot Attention + permanence_link, per SPEC-20260506-004 v0.2 §C3) 对应"动静分离"功能, 与 MonST3R / Easi3R 同属一类机制但实现路径不同; SPEC-007 v0.2 把 MonST3R 列入 Tier 5 orthogonal (动态主干路径与 v0.3 静态优先 + Permanence-辅助路径正交)。

### 2.4 长序列重建中的状态、记忆与缓存四类机制

长序列输入把 3R 模型推到第二类常见难题: 在有限算力下保留足够多的历史几何上下文, 又不能让错误状态被一直传下去 (综述 §6 + fig:memory + tab:memory)。综述 §6 把这一方向的近一年工作分为四类互不互斥的机制支线:

**B1 递推状态 (compressed)**: CUT3R 走 persistent recurrent state 的路线, 把连续 3D perception 组织成带状态的模型, 在输入流上递推更新; STream3R 在 causal transformer 框架下做可扩展的逐帧重建; LongStream 通过 gauge-decoupled 的关键帧位姿与正交尺度学习处理长在线序列。

**B2 空间 / 指针记忆 (selected)**: Spann3R 引入外部 spatial memory 用于全局 pointmap 重建; Point3R 在 Spann3R 思路上引入与三维场景结构相关联的指针记忆, 用于流式稠密重建。

**B3 混合记忆 (hybrid)**: LONG3R 用 memory gating 配合 dual-source decoder 维持长序列上下文; LoGeR 在 parametric TTT memory 上叠加滑动窗口注意力; Mem3R 把 tracking 与 mapping 的记忆显式解耦。

**B4 缓存治理与滤波 (budget governance)**: OVGGT 用自选择缓存与动态锚点保护维持固定计算预算; PAS3R 按位姿变化与图像频域线索调整状态更新; FILT3R 在递推状态之上加一层免训练的 Kalman 式潜变量滤波。

Dream3R v0.3 C2 Memory (per SPEC-20260508-001 v0.3 addendum) 通过 NSA three-branch (compressed / selected / sliding) + AnchorBank K=256 + StateToken + Mamba-Transformer 混合循环结构覆盖前 3 类: compressed 分支对应 B1 递推状态 (StateToken 实装); selected 分支 + AnchorBank 对应 B2 空间指针; sliding 分支 + Mamba hybrid 对应 B3 混合记忆。第 4 类 B4 预算治理 ⚠ partial — 帧预算约束接口存在但动态剪枝未对比 (per cycle 035 SOTA_MATRIX_V2 §6.4 + LONG_SEQ_REAL_TABLE_PLAN B4 coverage gap acknowledgement)。这一覆盖关系是 §3 Q2 (长序列内存机制统一) 的核心论据。

### 2.5 测试时验证、修正与先验输入三类机制

3R 模型一般同时输出 pointmap / depth / camera / tracks / confidence 等多个几何量, 它们之间天然存在一致性关系 (综述 §7 + tab:testtime)。综述 §7 把测试时阶段引入的机制分为三类:

**C1 一致性优化 (无参数更新)**: Test3R 用 image triplet 之间的几何一致性做测试时优化, 把推理过程组织为一致性最大化的轻量调整; 不更新模型参数。

**C2 测试时参数更新 (TTT)**: TTT3R 把递推 3R 模型的状态更新当成在线 test-time training, 按对齐置信度推导记忆更新速率; 实质是反向传播在推理阶段动态调整模型参数。

**C3 先验注入 (prior injection)**: G-CUT3R 在 CUT3R 上叠加一组模态特异的先验编码器 (深度 / 相机 / 位姿先验在合适时机进入); Pow3R 把先验当作可选输入直接进入前馈模型, 在训练时就纳入条件建模 (与 G-CUT3R 区别: G-CUT3R 推理时, Pow3R 训练时); MASt3R-SfM 通过经典 SfM 一致性循环对 MASt3R 的匹配结果做校验, 把测试时验证拉回 bundle adjustment 传统范式。综述 §7 段 3 还指出, 除模型自带先验通道外, 3R 系统经常借用外部先验 (Depth Pro / Metric3D v2 / DINOv2 / DINOv3 / CoTracker / SpatialTracker / SAM2), 在尺度 / 匹配 / 动态识别 / 失败检测上提供补充, 但每种先验自己也带偏置和失效区间 — 先验和模型预测对不上时需要在系统层 (而非模型层) 决定听谁的。

Dream3R v0.3 C4 Critic (per SPEC-20260506-004 v0.2 §C4: Sampson 几何 / depth 一致性 / 共视 conflict 三类信号 + repair actions 0/1/2 stub 3/4/5) 是"验证 + 修复"hybrid, 既包含 Test3R 风格的几何一致性验证 (无参数更新), 又包含 repair action 的输出修正 (无参数更新), 但不包含 TTT3R 风格的参数更新路径。这一未拆分的 hybrid 配置正是 §3 Q1 (验证机制路径) 的核心问题: 是否应在架构层把 C1 一致性优化与 C2 TTT 参数更新拆为两条独立路径? 此问题对应 cycle 035 SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §5 B1 候选 v0.4 spec delta (Critic path split: verification vs test-time adaptation), 仍 proposal-status, 未起草。

### 2.6 从几何预测到可查看输出三类资产

实际应用很少直接面向模型内部的 pointmap (综述 §8)。系统要把几何预测转化成可查看 / 可比较 / 可存档的结果, 这些输出在综述 §8 + tab:application 中归为三类:

**D1 4D pointmap (几何中间量)**: 由 D²USt3R / Dream3R v0.3 C1+C2+C3 输出的稠密时空点图; 适合下游几何一致性检查与跨视角对照, 但不直接渲染。

**D2 dynamic mask (几何中间量, 动静分离)**: MonST3R / Easi3R / RayMap3R / SAM2 输出的动态掩码; 与 D1 配合界定哪些像素属于动态。

**D3 4DGS asset (可渲染输出)**: 3D Gaussian Splatting 提供实时可渲染辐射场表示, 4DGS / 4D-Rotor Gaussian Splatting 把它扩展到动态场景; Splatt3R 在 MASt3R 风格几何上预测高斯属性, 把未标定图像对直接映射到 Gaussian; InstantSplat 借助稠密立体先验与 Gaussian Bundle Adjustment 处理稀疏视角; NoPoSplat 从稀疏无位姿图像直接预测规范坐标下的高斯。

Dream3R v0.3 W17-W18 (per code/dream3r/RECENT_PROGRESS.md, cycle 034 完成) 在 D1 + D2 已有实装 (W17 Mamba-Transformer 混合循环 + W18 GaussianHead tensor 契约 renderer-free); D3 (实际 Gaussian renderer) 仍 gated (W27 candidate per code/dream3r/NEXT_PHASE_ROADMAP.md), 受 R-4DGS-LIC-1 风险约束 (4DGS asset 渲染 license 链未文档化, 见 §9)。

### 2.7 综述四轴覆盖矩阵与 Dream3R v0.3 落点

把 §2.1-§2.6 的 6 大子方向按综述 §10 抽象出的四轴 (轴 A 六类失败模式 / 轴 B 长序列内存四类 / 轴 C 测试时三类 / 轴 D 输出资产三类) 重新汇总, 得到 21 子类的覆盖矩阵 (per cycle 035 SOTA_MATRIX_V2 §6 + SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §3 first-class support 21 子类)。Dream3R v0.3 在矩阵上的落点是: ✓ first-class 6 子类 / ⚠ partial 11 子类 / ✗ absent 4 子类。

**✓ first-class 6 子类**: 轴 A 弱纹理 + 长基线 (C4 Critic Sampson + 共视 conflict); 轴 B B1 递推状态 (C2 StateToken) + B2 空间指针 (C2 AnchorBank) + B3 混合记忆 (C2 NSA + Mamba); 轴 D D1 4D pointmap (C1+C2+C3 输出)。

**⚠ partial 11 子类**: 轴 A 镜面 + 快速运动 + 尺度漂移 (C4 Critic 信号通道存在但阈值未按失败模式标定 — cycle 035 CRITIC_CALIBRATION_PLAN_V1 plan-only 待执行); 轴 B B4 预算治理 (帧预算接口存在但动态剪枝未对比 — cycle 035 LONG_SEQ_REAL_TABLE_PLAN B4 coverage gap); 轴 C C1 一致性优化 + C3 先验注入 (C4 Critic hybrid 含一致性元素但未拆为独立路径); 轴 D D2 dynamic mask (W18 输出 tensor 契约存在但实际 Permanence link 训练未跑); 等等 (具体逐项见 SOTA_MATRIX_V2 §6 Tables A-E)。

**✗ absent 4 子类**: 轴 A OOD (R-OOD-1 风险, 见 §9; CRITIC_CALIBRATION_PLAN_V1 A6 mode 计划但未启动); 轴 C C2 TTT 参数更新 (R 不存在专用风险条目, 但属于 §3 Q1 候选 v0.4 spec delta B1 范围); 轴 D D3 4DGS asset 渲染 (R-4DGS-LIC-1 + W27 gated); 输入扩展 axis (R-INPUT-EXT-1; 综述驱动优化提案 §3 bonus axis; v0.4 spec delta B3 候选)。

Dream3R v0.3 在四轴上的整体定位: **不押注单一支线**, 而是在 C1 Perceiver (DINOv3-S frozen backbone, 综述 §7 段 3 视觉特征 backbone 类) + C2 Memory (NSA three-branch 同时实装 B1+B2+B3) + C3 Permanence (Slot Attention 对应轴 D D2) + C4 Critic (Sampson + depth + 共视 三类信号 + repair actions; 含 C1 一致性优化元素但未拆) + C5 Composer (7 expert pool 含轴 A / 轴 B / 轴 D 各支线代表) + C6 Bus (CR-1..CR-6 cross-spec signal contract v2.1) 六模块上同时维持多机制并置。这一 no-all-in 设计 (per DEC-20260504-002) 是 §3 Q3 (多专家组合是否优于单一 expert) 的架构前提, 也是 §6 预期成果中"在 Q1 / Q2 / Q3 三组维度上提供候选架构层方案的实证依据"的可行性基础。

落点判断的工件锚点: SOTA_MATRIX_V2.md 五张 Tables A-E (cycle 035 P0-2 deliverable) + SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md §3 21 子类覆盖矩阵 (cycle 035 上游 proposal) + WORK_RISK_REGISTER.md v1.2 17 行 (cycle 035 +4 cross-spec + cycle 036 +3 proposal-cycle)。这些工件本章不复制, 仅引用; §5 消融与评测 / §9 研究风险将进一步展开各子类的 falsification 路径与风险缓解机制。

### 2.8 现有 3R 工具链与平台综述

上述 §2.1-§2.7 的综述聚焦于算法与架构层面。然而, 多模型并行演进带来的不仅是算法挑战, 也是工程管理挑战。本节梳理现有 3R 方向的工具链与平台现状, 识别统一聚合管理平台的空白。

**学术平台 (NeRF 主导)**:

Nerfstudio (Tancik et al., 2023) 是当前最成熟的学术级 3D 重建平台, 提供统一的训练 / 评估 / 可视化流水线。但 Nerfstudio 的架构设计围绕 NeRF 范式 (per-scene optimization + volume rendering), 与前馌式 3R 的 feed-forward 范式存在根本差异: 3R 模型不需要每场景训练, 而是单次前向传播结合 streaming / batch 多模式输入。Nerfstudio 的 pipeline 抽象、数据解析器、viewer 均针对 NeRF 设计, 无法直接复用于 DUSt3R / MASt3R / Spann3R 等 3R 模型。

**商业产品 (封闭生态)**:

Polycam / Luma AI / RealityCapture 等商业产品将多视图重建包装为一键化工作流, 但均为闭源产品, 算法细节不可审计, 无法复现实验结果; 且其核心算法多属 SfM + MVS + 3DGS 等传统路线, 尚未全面集成前馌式 3R 模型。对于需要对照实验、消融分析、架构级对比的学术研究, 商业平台无法提供所需的可控性与可解释性。

**各模型官方 Demo (孤岛现状)**:

DUSt3R / MASt3R / MonST3R / Spann3R / Fast3R / CUT3R 等模型各自提供官方 demo.py 或 Gradio 界面, 但每个 demo 独立运行, 各自有不同的 Python 环境、输入格式、输出结构、评估指标。在同一场景上对比多个模型需要研究者手动编写开叱 / 解析 / 转换代码, 实验成本随模型数量线性增长。这一“孤岛现状”是 Dream3R C5 Composer 7-expert pool 实证评估的主要工程障碍。

**空白识别**: 缺乏一个面向前馌式 3R 的统一聚合对比管理平台。这一平台需要: (a) 统一的模型注册与执行合同, 让新模型接入的边际成本可控; (b) 统一的输出结构, 让跨模型对比不需要格式转换; (c) 远端 GPU 服务器调度, 让本地桌面端无需直接管理服务器环境; (d) 评估与对比框架, 让消融实验结果可组织、可复现。这一空白是本研究支柱 B (KYKT 聚合管理平台, per §1.7) 的研究动机, 也是 §3 Q4 (统一聚合管理与评估平台) 的学术依据。

Dream3R v0.3 的消融实验设计 (§5) 直接依赖这一平台: ABL-v02-4 Composer best-of-N vs single-expert 需要在同一平台上调度多模型运行; KITTI 长序列评测需要统一的结果归集与指标计算; Critic 标定需要跨模型的对比数据。KYKT 平台的设计将在 §4-B 展开。

---

## §3 候选研究问题

本章在 §1.4 提出的三个核心研究问题 (Q1 验证机制 / Q2 长序列内存 / Q3 多专家组合) 基础上, 把每个 Q 与 §2 综述谱系 + §4 Dream3R v0.3 架构两侧的素材对齐, 给出 (a) 该研究问题的 gap identification, (b) Dream3R v0.3 在当前迭代中的候选路径, (c) falsification 路径在 §5 评测设计中的入口, (d) candidate-not-final 边界声明。三个 Q 之后, §3.4 阐明四个 finalist 模块 (Critic / Memory / Permanence / Composer) 的独立性 (per DEC-20260504-002 no-all-in), §3.5 给出本研究的整体研究地位声明 (per DEC-20260501-011 candidate-not-final)。

### 3.1 Q1 验证机制的架构层落地 (Critic 路径)

**研究问题陈述**: 在前馈式 3R 架构中, 几何验证 (无参数更新的一致性检查 + 修复) 与测试时适应 (TTT 风格的参数更新) 在架构层应否拆为两条独立路径? 拆分后两条路径的边际贡献能否分离?

**Gap identification**: 综述 §7 (映射到 §2.5) 区分了测试时三类机制 — C1 一致性优化 (Test3R, 无参数更新)、C2 测试时参数更新 (TTT3R)、C3 先验注入 (G-CUT3R / Pow3R / MASt3R-SfM)。现有 3R 系统中, 这三类机制以独立工作发表, 缺乏在单一架构内的并置评估。具体而言: Test3R 走 image-triplet 一致性优化, 不更新模型参数; TTT3R 把递推 3R 模型的状态更新当成在线 test-time training, 通过反向传播在推理阶段动态调整记忆更新速率。两者在性质上不同 (一个是固定模型 + 输出修正, 另一个是动态模型 + 参数更新), 但在哪一个 + 在何种条件下 + 边际贡献多大, 现有文献无法回答。

**Dream3R v0.3 候选路径**: 当前 C4 Critic (per SPEC-20260506-004 v0.2 §C4) 是"验证 + 修复"hybrid — 含 Test3R 风格的几何一致性验证 (Sampson / depth / 共视 conflict 三类信号, 无参数更新) + repair action 0/1/2 (rerun_local_region / rerun_global / A5 reroute_model 切换专家, 无参数更新) + repair action 3/4/5 stub (未实装)。TTT3R 风格的测试时参数更新路径未拆出。这一 hybrid 配置使得"几何验证 vs 参数适应"两类机制的边际贡献在 Dream3R v0.3 当前实装下无法分离。

为分离这两类机制, cycle 035 SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §5 B1 提出 v0.4 spec delta 候选: 在架构层把 C1 一致性优化与 C2 TTT 参数更新拆为两条独立路径, 让 C4 Critic 专注于 verification + repair, 另起一个 TTT 路径模块 (暂记 C4', 命名候选) 负责测试时参数更新。该 v0.4 spec delta 当前仍 proposal-status, 未在 cycle 039 起草; §3.1 在开题报告语义层把它作为本研究的明确实证缺口与候选设计方向。

**Falsification 路径**: 在 §5 实验设计中, ABL-v02-1..9 (SPEC-005 v0.2) 主要消融 v0.3 架构层 deltas, 不直接评估 C4 Critic 拆分前后的边际贡献。cycle 035 CRITIC_CALIBRATION_PLAN_V1 把六类失败模式 → C4 五个 sub-signal 的标定方案 ready, 但执行 gated on F-002 server authorization。Q1 的正面 evaluation 需要 (a) v0.4 spec delta B1 起草并实装 (post-开题报告 work), 然后 (b) 在 KITTI 长序列上对照"hybrid C4 v0.3" vs "拆分后 v0.4 (C4 + C4')"两组配置, 度量 route_regret + 修复后 pointmap L2 + 测试时算力开销。在开题报告时间窗口内 (M1-M5), Q1 的 evaluation 边界停留在 plan + spec-delta-drafted 阶段, 不承诺实证拆分对比。

**candidate-not-final 边界**: Q1 不主张 Critic 拆分路径优于 hybrid 路径; 也不主张 hybrid 路径优于 TTT3R 风格独立适应路径。Q1 是 "评估两条路径的边际差异是否在标准 3R 评测下显著存在" 的研究问题, 不是 "证明哪条路径更优" 的结论性命题。

### 3.2 Q2 长序列内存四类机制的架构层统一 (Memory 路径)

**研究问题陈述**: 在单一 3R 架构的 C2 Memory 模块内, 同时实装综述 §6 抽象出的长序列内存四类机制 (B1 递推状态 / B2 空间指针 / B3 混合记忆 / B4 缓存治理) 是否可行? 四类机制间的协同 / 冲突如何在长序列真实评测下显现?

**Gap identification**: 综述 §6 (映射到 §2.4) 把长序列 3R 工作分为四类互不互斥的内存机制支线。现有系统每个只占四类机制中的一档: CUT3R / STream3R / LongStream 走 B1 递推状态; Spann3R / Point3R 走 B2 空间指针; LONG3R / LoGeR / Mem3R 走 B3 混合记忆; OVGGT / PAS3R / FILT3R 走 B4 缓存治理。换言之, 四类机制在文献里是 disjoint 的; 一个系统选定一档之后, 其他三档在架构层缺席。这导致两个未回答的问题: (a) 单一架构能否同时实装四档而仍维持单帧 30-50 ms 帧预算 (per §4.1 Delta 1)? (b) 四类机制 jointly 实装时, 是否出现协同 (e.g., 空间指针 + 递推状态 的双通道写入提升长序列稳定性) 或冲突 (e.g., 缓存治理的剪枝策略 与混合记忆的注意力 weight 出现 contention)?

**Dream3R v0.3 候选路径**: C2 Memory (per SPEC-20260508-001 v0.3 addendum, supersedes Delta 3) 通过 NSA three-branch (compressed / selected / sliding) + AnchorBank K=256 + StateToken + Mamba-Transformer 混合循环结构覆盖前三档:

- B1 递推状态 ← StateToken (compressed branch, per NSA_MEMORY_INTEGRATION_MEMO §Compressed)
- B2 空间指针 ← AnchorBank K=256 (selected branch + selection gate)
- B3 混合记忆 ← Mamba hybrid + NSA three-branch (sliding branch 局部 + 全局)

B4 缓存治理 ⚠ partial: 帧预算约束接口存在 (per §4.1 Delta 1 latency budget 30-50 ms), 但动态剪枝策略未与基线对照 (per cycle 035 LONG_SEQ_REAL_TABLE_PLAN §B4 explicit coverage gap)。Q2 的核心是验证这一同时覆盖关系在 KITTI windows ≥ 10 长序列上是否 (a) 维持帧预算, (b) 在四类机制 jointly 实装时显现协同或冲突。

**Falsification 路径**: §5 实验设计将通过 ablate_recurrence.py 4 variants (baseline_cross_attention / mamba_hybrid / no_nsa / no_stable_memory) + cycle 035 LONG_SEQ_REAL_TABLE_PLAN 4 度量 (scale_drift_proxy / memory_decay_proxy / anchor_fill_rate / retrieval_diversity) 在 windows ∈ {10, 20, 50, 100} 上展开。Q2 的正面 evaluation 需要 F-002 server authorization 启动 KITTI 长序列 evaluation 跑; 在开题报告时间窗口内, Q2 的 evaluation 边界停留在 plan-ready + W17 实装完成阶段, 不承诺 KITTI 长序列实证数值。

B4 缓存治理子问题需要 v0.4 spec delta 候选 (动态剪枝接口) 或 v0.4 evaluation extension (现有帧预算接口的剪枝策略评估), 在开题报告时间窗口内不要求 closure。

**candidate-not-final 边界**: Q2 不主张 Dream3R v0.3 C2 Memory 是长序列内存机制统一的最终方案; 也不主张四类机制同时实装必然优于专一档。Q2 是 "评估单一架构同时实装多机制的可行性 + 协同/冲突显现" 的研究问题。

### 3.3 Q3 多专家组合是否优于单一 expert (Composer 路径)

**研究问题陈述**: 在前馈式 3R 架构中, 多专家组合 (best-of-N routing) 相对单一 expert 是否在标准评测下显现显著实证优势? 与 Test3R 内置 verifier 组合时, C4 Critic 的额外边际价值如何?

**Gap identification**: 综述 §3 + §6 + §7 + §8 (映射到 §2.2 / §2.4 / §2.5 / §2.6) 显示, 现有 3R 系统在不同 regime 上各有优势: MASt3R 在静态对几何上精度高, Fast3R 在多视图密集场景下高效, Spann3R 在流式场景下具备内置内存, CUT3R 在动态容忍场景下表现稳健, MoGe-2 在单目 pointmap 上 fail-safe, DepthAnything-V2 在单目 depth foundation 上 license-clear, Test3R 在测试时一致性验证上自带 verifier。多专家组合作为架构层方案 (per SPEC-20260506-004 v0.2 Delta 5 + COMPOSER_CAPABILITY_DESCRIPTORS 7-expert pool + DEC-20260507-001 Tier 1 in-pool) 在工程上具备直接合理性, 但其相对单一专家的实证优势是否在标准评测下显著存在, 现有文献缺乏对照实验。

**Dream3R v0.3 候选路径**: C5 Composer (per §4.6) 通过 7-expert pool + capability descriptor + 路由策略 (capability_match spread > 0 → cost_adjusted_match 解析 ties; spread = 0 → fail_fast 触发) 显式实装 best-of-N 路由。CR-1 与 C4 Critic 协作 (Critic A5 reroute 须有 Composer capability_match spread 支持); CR-4 处理 tied capability (Composer 不强制选择, Critic 在 epsilon_tie 窗口内决断)。

Q3 涉及两个子问题:

- **Q3-a**: best-of-N (7-expert pool) vs single-expert (e.g., MASt3R-only) 在 KITTI 真实数据上, pointmap L2 + route_regret + scale_drift_proxy 哪一组显著占优?
- **Q3-b**: 加入 Test3R 后, 7-expert pool + Test3R verifier 组合是否相对 6-expert pool + 外部 C4 Critic 显现额外边际价值? (per SPEC-20260507-002 v0.3 ABL-v02-10 Test3R-alone candidate)

**Falsification 路径**: §5 实验设计将通过 ABL-v02-4 (Composer best-of-N vs single-expert) + ABL-v02-6 (capability_match 测量) + ABL-v02-10 (Test3R-alone vs Test3R-in-pool) 三组消融在 KITTI / DTU 评测协议下展开。Q3 的正面 evaluation 需要 F-002 server authorization 启动多专家真实加载 + 多 regime workload 评测; 在开题报告时间窗口内 (W19-W23 期间), Q3 的 evaluation 边界停留在 ABL 实验组 ready + 评测协议 ready 阶段, 不承诺多专家路由 best practice 的最终判定。

**candidate-not-final 边界**: Q3 不主张 Dream3R v0.3 C5 Composer 7-expert pool 是多专家组合的最终方案; 也不主张 best-of-N 路由必然优于单一 expert。Q3 是 "提供 best-of-N vs single-expert 的对照实验证据" 的研究问题, 不是 "证明 best-of-N 普遍占优" 的结论性命题。

### 3.4 四个 finalist 模块的独立性 (no-all-in 设计)

per DEC-20260504-002 (no-all-in on single finalist), Dream3R v0.3 的 4 个 finalist 模块 (C4 Critic / C2 Memory / C3 Permanence / C5 Composer) 设计上保持独立性: 任一模块的实证表现不达标均不影响其他三模块的独立评估。这一独立性体现在三个层面:

- **架构层独立**: C4 / C2 / C3 / C5 各自有 standalone SPEC (SPEC-20260503-001 Critic / SPEC-20260503-002 Memory / SPEC-20260503-003 Permanence / SPEC-20260504-001 Composer); 跨模块通过 C6 Bus + CR-1..CR-6 cross-spec signal contract (per §4.7) 协同, 不通过 shared parameter 耦合。
- **评测层独立**: §5 实验设计中, ABL-v02-1..9 + ABL-memory-0..11 + CRITIC_CALIBRATION_PLAN_V1 + LONG_SEQ_REAL_TABLE_PLAN 各自针对单一模块设计消融组与度量, 不要求多模块 jointly 达标。
- **研究问题独立**: §3.1 Q1 (Critic 验证) / §3.2 Q2 (Memory 长序列) / §3.3 Q3 (Composer 路由) 各自挂在不同 finalist 模块上; Q1 失败不否决 Q2 / Q3, 反之亦然。

值得注意: §3.1-§3.3 的三个 Q 直接挂在 C4 / C2 / C5 三个 finalist 模块上, C3 Permanence (动静分离) 不构成本研究三个 Q 的核心命题, 但作为 4 finalist 之一仍在 §4.4 + §5 + §7 实证轨道内独立评估 (per DEC-20260504-002 no-all-in 不允许 silent retiring of any non-finalist track)。

这一独立性是 candidate-not-final 框架的工程支撑: 任一模块若被后续工作替换或修订, 其他模块仍可独立留存; 任一 Q 若被实证证伪, 其他两 Q 仍可独立评估。

### 3.5 候选 vs 最终的研究地位声明

per DEC-20260501-011 (Dream3R thesis reframe; candidate-not-final), Dream3R 是被评估的候选架构, 非项目收敛方案。这一研究地位声明对本研究三个 Q 与三个创新点 (§6.2) 的措辞构成硬约束:

- 本研究 **不** 论证 Dream3R 相对 SOTA 在任一单一指标上具有压倒性优势 (per §4.8 整体定位)
- 本研究 **不** 主张 Dream3R 是最终方案; v0.4 spec delta 候选 (B1 Critic 路径拆分 / B2 输出资产契约 / B3 输入扩展 axis, per cycle 035 SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §5) 表明后续版本明确可能修订或替换 v0.3 架构
- 本研究 **不** 把 C2 Memory v0.3 (NSA + AnchorBank + StateToken + Mamba hybrid) 等同于长序列内存机制的最优方案; SPEC-20260508-001 v0.3 addendum 自身的 "未实装的 candidate" 与 "engineering-judgment 标记" 是 candidate 框架的实证体现

研究地位的正面表述: 本研究的成果是 (a) 一个具体的 3R 候选架构 (Dream3R v0.3) 的设计文档 + 实证评测, (b) 综述四轴判断与候选架构 X 路径的覆盖矩阵 (per §2.7 + cycle 035 SOTA_MATRIX_V2), (c) 多机制并置评估的 best practice 实证数据, (d) v0.4 spec delta 演进路径的明确候选清单。这些成果都不是 "Dream3R 是 3R 方向的最终解" 的结论性主张, 而是 "Dream3R v0.3 提供了一个具体且可证伪的候选架构 + 实证轨道" 的研究地位声明。

候选架构演化路径在 §8 时间安排 + §9 风险章节进一步展开, 包括 v0.4 spec delta 候选清单 + 候选架构被修订/替换的风险条目 (R-PROP-CLAIM-1 in WORK_RISK_REGISTER v1.2)。

### 3.6 Q4 统一聚合管理与评估平台 (平台路径)

**研究问题陈述**: 如何设计一个面向多模型前馌式 3R 研究的统一聚合管理与评估平台, 使其具备: (a) 新模型接入的低边际成本, (b) 跨模型横向对比的统一输出结构, (c) 远端 GPU 服务器的透明调度, (d) 下游应用对接的 API 封装候选方案?

**Gap identification**: §2.8 识别的三类现状 — Nerfstudio 为 NeRF 设计 (范式不兼容), 商业产品闭源 (不可审计), 官方 demo 孤岛 (边际成本线性增长) — 共同指向同一空白: 前馌式 3R 方向缺乏统一平台。这一空白导致 Dream3R v0.3 的 C5 Composer 7-expert pool 实证评估 (§3 Q3) 的工程成本过高, 也制约了 ABL-v02-4 / CRITIC_CALIBRATION_PLAN_V1 / LONG_SEQ_REAL_TABLE_PLAN 的执行效率。

**KYKT 平台候选路径**: KYKT 聚合管理平台 (Coding/4.06/vision_ui) 通过 Tauri 2 + React + TypeScript + FastAPI + SSH/SCP 技术栈, 在本地桌面端与远端 GPU 服务器之间建立统一调度层。当前已接入 6 个 3R 模型 (DUSt3R / MASt3R / MonST3R / Spann3R / Fast3R / CUT3R), 其中 4 个已通过 smoke test。平台架构设计将在 §4-B 展开。

**Q4 子问题分解**:

- **Q4-a 模型注册与执行合同**: 如何定义统一的 model_registry + runner contract, 使新模型接入仅需“注册模型 → 添加 runner → 添加 SSH dispatch 分支”三步? 当前 6 模型接入之后, 新模型接入的平均耗时如何?
- **Q4-b 统一评估框架**: 如何设计跨模型对比矩阵 (per sample_manifest.json + job output + evaluation.json), 使 Dream3R 的消融实验结果可组织、可复现?
- **Q4-c 应用对接层**: 平台层推理能力如何封装为 REST/gRPC 接口, 供下游应用调用? (本阶段仅概念设计, 不吸取实装)

**与 Q1-Q3 的关系**: Q4 为 Q1-Q3 提供工程基础设施。Q3 (best-of-N vs single-expert) 的实证评估直接依赖 Q4-a (多模型统一调度); Q1 (Critic 标定) 依赖 Q4-b (跨模型对比数据); Q2 (长序列评测) 依赖 Q4-a (远端执行调度)。Q4 是工程级研究问题, 其评估标准见 §5.8。

**candidate-not-final 边界**: Q4 不主张 KYKT 平台是唯一可行的 3R 统一平台方案; 也不主张当前架构设计已完备。Q4 是“评估统一平台在多模型 3R 研究中的工程效率与可复现性提升”的研究问题。

---

## §4 Dream3R v0.3 架构与 KYKT 平台架构

本章分两大部分: §4-A 描述 Dream3R v0.3 候选架构 (支柱 A), §4-B 描述 KYKT 聚合管理平台 (支柱 B)。两大支柱独立设计、并行评估, 通过平台层调度与评测框架协同。

### §4-A Dream3R v0.3 候选架构

本节在 SPEC-20260506-004 v0.2 (架构 v0.2 delta, 六 Delta 设计) + SPEC-20260508-001 v0.3 (C2 Memory v0.3 addendum) + paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md v2.1 (CR-1..CR-6 cross-spec 信号契约) 的基础上, 按 8 个子节描述 Dream3R v0.3 的整体设计与 C1-C6 六模块。本节为开题报告层的架构描述, 不复述 SPEC 工程细节; SPEC 由 section / Delta / line anchor 引用, 不修改。

### 4.1 整体设计与帧预算

Dream3R v0.3 是按 architecture-first 主线 (per DEC-20260506-001) 设计的前馈式 3R 候选架构。整体框架由六个模块 (C1 Perceiver / C2 Memory / C3 Permanence / C4 Critic / C5 Composer / C6 Bus) 通过 cross-spec 信号契约 (CR-1..CR-6, v2.1) 串接, 接受图像序列 (或单图 / 图像对) 作为输入, 输出 4D pointmap (D1) + dynamic mask (D2) 张量契约 (W17-W18 cycle 034 完成); 可渲染 4DGS asset (D3) 由 W27 candidate gated。

per SPEC-20260506-004 v0.2 Delta 1, 整体设计采用 speed priority 与 frame budget 约束: 单帧目标延迟 30-50 ms (paper-derived from DINOv3 family throughput; engineering-judgment for 实际剩余 budget 分配到 C2-C6)。该约束是 §4.2 C1 backbone tier 选择 (Delta 2: DINOv3-S 取代 ViT-L) 与 §4.6 C5 Composer pool 7-expert 准入标准 (Delta 5: 排除 VGGT ~1.2B + MapAnything 因超 budget) 的源头驱动条件。

Dream3R v0.3 的 architecture novelty 集中在两条 pillar (per SPEC-004 v0.2 Delta 6 main claim narrowing):

- **Pillar A: Verification-as-architecture** — C4 Critic 把几何冲突检测与修复显式作为架构组件 (而非测试时附加路径), 通过 Sampson / depth / 共视三类信号 + repair actions 0-5 在每个窗口提供 falsifiability 与可观察的修复行为。
- **Pillar D: Heterogeneous best-of-N Composer** — C5 Composer 通过 7-expert pool + capability descriptor 显式路由, 每个 expert 在不同 regime (静态对 / 多视图 / 流式 / 单目 / 测试时一致性) 有差异化 capability_match。

其他模块 (C1 / C2 / C3 / C6) 是 enabling layer, 为 pillar A + D 提供输入特征、长序列上下文、动静分离、与跨模块信号路径; 它们各自的设计不构成 main claim。

### 4.2 C1 Perceiver (DINOv3-S frozen backbone)

C1 Perceiver 负责从输入图像 (或图像序列) 提取视觉特征, 供下游 C2-C5 消费。per SPEC-004 v0.2 Delta 2, C1 backbone 从 v0.1 的 ViT-L 替换为 DINOv3-S (S = Small tier, 自监督预训练 + frozen)。这一替换的依据是 DINOV3_C1_INTEGRATION_MEMO 中记录的两项 paper-derived metric: 参数量减少 ~14× (ViT-L ~300M → DINOv3-S ~21M), 推理延迟加速 ~5× (在标准 image-pair 输入下)。

frozen-backbone 决策 (而非 fine-tune) 的依据: (a) DINOv3 自监督训练已在大规模图像上学到通用 cross-view 对应能力 (类似综述 §3 提到的 CroCo → DUSt3R 迁移路径); (b) frozen 路径降低训练 cost 并避免 backbone-drift 风险; (c) 头部 (heads) 从头训, 在小型架构上更灵活。-B (Base) tier 作为 fallback 记录在 memo, 但 v0.3 默认不切换。

C1 输出特征 token 序列, 直接进入 C2 Memory 的三分支稀疏注意力 + C5 Composer 的路由层 + C4 Critic 的几何信号通道; 这些下游消费由 C6 Bus 的 cross-spec 信号契约 (per §4.7) 规约。

### 4.3 C2 Memory (NSA three-branch + AnchorBank + StateToken + Mamba hybrid)

C2 Memory 是 Dream3R v0.3 在长序列轴上覆盖综述 §6 四类机制 (B1 递推状态 / B2 空间指针 / B3 混合记忆 / B4 缓存治理) 的核心模块。per SPEC-20260508-001 v0.3 addendum (supersedes v0.2 Delta 3), C2 现行设计是 NSA-style three-branch sparse attention 与显式 AnchorBank + StateToken 的组合:

- **Compressed branch**: 把历史窗口的 token 流压缩为 fixed-size latent (对应综述 B1 递推状态; 实装由 StateToken 承载, 在每个窗口 incremental 更新; per NSA_MEMORY_INTEGRATION_MEMO §Compressed)。
- **Selected branch**: 通过 attention selection 从 AnchorBank (K=256 capacity) 中按 query relevance 抽取 top-k 三维空间锚点 (对应综述 B2 空间 / 指针记忆; 类似 Spann3R 的可寻址空间存储; per NSA_MEMORY_INTEGRATION_MEMO §Selected)。
- **Sliding branch**: 局部窗口的 frame-value tokens 直接保留 (对应综述 B3 混合记忆的局部窗口分量); 与 compressed + selected 通过 attention 共同消费 (per NSA_MEMORY_INTEGRATION_MEMO §Sliding)。

W17 Mamba-Transformer 混合循环结构 (cycle 034) 把上述三分支封装为可选择 recurrence backbone, 与 baseline cross-attention 在 ablate_recurrence 的 4 variants (baseline_cross_attention / mamba_hybrid / no_nsa / no_stable_memory) 中并置。B4 缓存治理 (动态剪枝 / 帧预算约束下的 anchor 替换) 是 partial coverage: 帧预算约束接口存在但动态剪枝策略未与基线对照 (per cycle 035 LONG_SEQ_REAL_TABLE_PLAN §B4 explicit coverage gap; 该 gap 是 §5 消融评测的 falsification 目标之一)。

C2 模块向 C6 Bus 发布的关键信号包括 `latent_drift_proxy` (per CR-3, 信息性, 不直接 gate C4 Critic 的 A5 reroute), 以及 `write_value_estimate` (per CR-2, 被 C3 Permanence 的 suppress_static_write 约束)。

### 4.4 C3 Permanence (Slot Attention + permanence_link)

C3 Permanence 负责动静分离与长序列上的 object identity 维护, 对应综述 §5 + §8 的 D2 dynamic mask 资产。模块以 Slot Attention 为骨架, 每个 slot 绑定一个 (类) 三维对象的 latent 表示; 通过 permanence_link (跨窗口的 slot 关联) 维持 identity 持续性。

C3 向 C2 Memory 发布 `suppress_static_write(r)` 信号: 当 Permanence 判定区域 r 为动态时, Memory 的 A2 (static map update) 必须遵守该 suppression (per CR-2)。这条 binding 是 Permanence-Memory 边界的关键 contract; Memory 若因结构限制无法遵守, 须显式 log `cross_spec_refusal` 并 surface 到 Advisor, 不允许 silent override。

C3 的设计与 MonST3R / Easi3R / RayMap3R 等动态主干路径 (per §2.3) 同属"动静分离"类机制, 但实现路径不同: MonST3R 类是动态主干 + 动态置信度回归, Dream3R v0.3 是静态优先 + Permanence-辅助。这两类方向在系统层互补而非互替, 是 §3 Q3 多专家组合的设计前提之一。

### 4.5 C4 Critic (Sampson + depth + 共视 conflict + repair actions)

C4 Critic 是 Pillar A (Verification-as-architecture) 的载体, 也是 §3 Q1 (验证机制路径) 的核心架构组件。per SPEC-20260506-004 v0.2 §C4, C4 通过三类几何信号检测当前窗口的几何冲突:

- **Sampson 几何**: 跨视图几何 epipolar 残差 (检测 pose / 内参与匹配 不一致)。
- **Depth 一致性**: 跨视图 depth 重投影残差 (检测 scale / depth 漂移)。
- **共视 conflict**: 多视图共视区域的 pointmap 一致性 (检测局部 mismatch)。

三类信号聚合为 `conflict_score(t)`, 通过 threshold `theta_conflict` 触发 repair actions:

- Action 0: no_action (conflict_score 低于 threshold)
- Action 1: rerun_local_region (局部 region 重跑 C1 + C2)
- Action 2: rerun_global (全窗口重跑)
- Action 3-5: stub (predicted / 未实装; per spec v0.3 行动空间扩展候选)

A5 reroute_model 是与 C5 Composer 协作的特殊 action: 当 conflict_score 高且 capability_match spread > 0, Critic 触发 reroute 切换到 Composer pool 的另一 expert (per CR-1 binding: Critic A5 requires Composer agreement on capability_match spread)。

C4 当前是"验证 + 修复"hybrid: 含 Test3R 风格的几何一致性验证 (无参数更新) + repair action 的输出修正 (无参数更新), 但不含 TTT3R 风格的测试时参数更新 (per cycle 035 SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §5 B1: 在架构层把 C1 一致性优化与 C2 TTT 参数更新拆为两条独立路径, 是 v0.4 spec delta 候选, 当前仍 proposal-status)。

per cycle 035 CRITIC_CALIBRATION_PLAN_V1, 三类信号的 threshold 阈值目前是统一 default, 未按六类失败模式 (弱纹理 / 镜面 / 快速运动 / 长基线 / 尺度漂移 / OOD) 逐类标定; 标定 plan 已 ready, 执行 gated on F-002 server authorization。

### 4.6 C5 Composer (7 expert pool + capability descriptor)

C5 Composer 是 Pillar D (Heterogeneous best-of-N) 的载体, 也是 §3 Q3 (多专家组合) 的核心架构组件。per SPEC-20260506-004 v0.2 Delta 5 + COMPOSER_CAPABILITY_DESCRIPTORS, 当前 expert pool 含 7 个 admitted lightweight expert:

| Expert ID | Model | innovation point | 规模 | attention regime |
|---|---|---|---|---|
| EXPERT-01 | MASt3R | pair / matching head | ~300M | full attn |
| EXPERT-02 | Fast3R | many-view single fwd | ~580M | full attn |
| EXPERT-03 | Spann3R | streaming spatial anchor | ~250M | (spatial) |
| EXPERT-04 | CUT3R | online persistent state | ~300M | (recurrent) |
| EXPERT-05 | MoGe-2 | mono pointmap | ~200M | full attn |
| EXPERT-06 | DepthAnything-V2 | mono depth foundation | ~25M Small | (depth prior) |
| EXPERT-07 | Test3R | test-time consistency verification | (lazy off-path; backbone + iteration) | full attn |

排除依据 (per Delta 5 engineering-judgment): VGGT (~1.2B; 超 frame budget) / MapAnything (multi-modal foundation, 太重) / PE Perception Encoder (太重) / Kimi Linear KDA (LM-to-3R transfer 不追求, RU-007 历史保留)。

Composer 的路由策略基于 capability descriptor: 每个 expert 在 (输入 regime, 输出 schema, infrastructure cost, attention regime, capability_match, failure modes) 9 axes 上携带 paper-derived / engineering-derived 标签; 路由层按当前输入 regime 与 capability_match 计算 spread, 当 spread > 0 时由 cost_adjusted_match (per v2 contract upgrade, DEC-20260504-004) 解析 ties; 当 spread = 0 时 fail_fast 触发 (per SPEC-20260504-001 §fail_fast_threshold)。

C5 与 C4 Critic 通过 CR-1 协作 (Critic A5 reroute 须有 Composer capability_match spread 支持); 通过 CR-4 处理 tied capability (Composer 不强制选择 top-1, 由 Critic 在 epsilon_tie window 内按 Critic-internal preference 决断)。

### 4.7 C6 Bus (CR-1..CR-6 cross-spec signal contract v2.1)

C6 Bus 是 Dream3R v0.3 跨模块协同的信号契约层, 不是 trainable 模块。per paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md v2.1 §Conflict Resolution Rules, 六条规则规约模块间的争议解决与信号 binding:

- **CR-1**: Critic A5 reroute_model 要求 Composer capability_match spread > 0; Critic 不发明 Composer 未刻画的模型。
- **CR-2**: Permanence suppress_static_write(r) 对 Memory 的 A2 是 binding; 不能 silent override; 若结构限制无法 honor, 须 log cross_spec_refusal + surface Advisor。
- **CR-3**: Memory latent_drift_proxy 是 Critic 验证的信息性输入, 不直接 gate A5; drift 单独不构成 Critic reroute 条件 (Critic 与 Memory falsification 独立)。
- **CR-4**: Composer top-1 / top-2 capability_match 在 epsilon_tie (default 0.05; inferred) 窗口内时, Composer 不强制选择, 由 Critic 按 Critic-internal preference 决断 (v2 起以 cost_adjusted_match 为 canonical, 处理 cost 不对称 tie)。
- **CR-5**: 所有 cross-spec 信号携带 producer 的 evidence label, 沿信号路径传播; Critic 不能 silently 把 inferred 信号升级为 paper-proven (per RESEARCH_CODE_DISCIPLINE.md rule 5 Honesty Override)。
- **CR-6**: 每个 cycle 009 case card 必须记录消费的 cross-spec 信号 + producer evidence label at consumption time; unknown 信号须 caveat。

v2.1 的 additive 变化 (per DEC-20260505-001) 是新增 "Forward-reference null protocol" 子节, 把 cycle 009 + cycle 010 case card 中已使用的"signal 在被消费时还未发布, 消费方回 null + 留 forward reference"模式正式化, 不修改 v2 substance。CR-7 (external_prior_conflict) 作为 v2.2 候选已记录在 cycle 035 SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §5 C2, 仍 proposal-status。

### 4.8 与现有 3R 系统的结构差异

把 Dream3R v0.3 的六模块设计与 §2 综述谱系对比, 主要结构差异在三点:

**结构差异 1 (轴 B 长序列内存): 单一架构同时覆盖多类机制**。综述 §6 中 CUT3R / Spann3R / LONG3R / Point3R 等系统各自占四类机制 (B1-B4) 的一档; Dream3R v0.3 的 C2 Memory (NSA three-branch + AnchorBank + StateToken + Mamba hybrid) 在单一架构内同时实装 B1 + B2 + B3, B4 partial。这一同时覆盖关系是 §3 Q2 (长序列内存机制统一) 的实证目标。

**结构差异 2 (轴 C 测试时机制): 显式区分"验证"与"路由切换", 暂未区分"参数更新"**。综述 §7 中 Test3R / TTT3R / G-CUT3R / Pow3R 等系统在测试时三类机制中分散存在; Dream3R v0.3 通过 C4 Critic 显式实装一致性验证 + repair action, 通过 C5 Composer 显式实装 expert reroute, 通过 CR-1 显式协调两者; 但当前 C4 是 verification-only (无参数更新), TTT 类参数更新路径未拆出 (B1 v0.4 spec delta 候选)。这一未拆分构成 §3 Q1 (验证机制路径) 的研究问题。

**结构差异 3 (轴 D + 多专家组合): 显式 best-of-N expert pool**。综述 §3-§7 中各 3R 系统在不同 regime 上分别擅长 (MASt3R 静态对 / Fast3R 多视图 / Spann3R 流式 / CUT3R 动态容忍 等); Dream3R v0.3 的 C5 Composer 通过 7-expert pool + capability descriptor 显式 best-of-N 路由, 把这一 regime 分化变成架构层显式选择。这一设计是 §3 Q3 (多专家组合实证评估) 的架构前提, 也是 cycle 029 review (per MEMORY_V03_ABLATION_REVIEW.md R-029-1..5) 之后保留的 cycle 035 SOTA_MATRIX_V2 §6 first-class support 6 子类的来源之一。

整体定位: Dream3R v0.3 不主张相对现有 SOTA 在任一单一指标上压倒性领先, 而是评估"在统一架构内同时实装多机制 + 显式路由"这一架构层 best practice 在 Q1 / Q2 / Q3 三组维度上的实证表现 (per DEC-20260501-011 candidate-not-final + DEC-20260504-002 no-all-in)。架构与单一支线方法的实证对照将在 §5 消融与评测设计中按 ABL-v02-1..9 + ABL-memory-0..11 + 综述驱动新增 calibration / long-seq 评测展开。

### §4-B KYKT 聚合管理平台架构

本节描述 KYKT 聚合管理平台 (支柱 B) 的架构设计。平台代码位于 Coding/4.06/vision_ui, 当前处于功能原型阶段 (6 模型接入 / 4 smoke 通过 / 桌面端可用 / AI 评估层存在)。本节按概念设计层描述, 不涉及实装细节。

#### 4-B.1 总体架构与技术栈

KYKT 平台采用桌面优先 (desktop-first) 架构:

```text
Tauri 2 桌面外壳
  → React + TypeScript 前端
  → 本地 FastAPI 后端 (127.0.0.1:8765)
  → 系统 SSH / SCP 远端调度
  → GPU 服务器模型执行 (/hdd3/kykt26)
```

这一架构的设计考量:

- **桌面优先 vs Web SaaS**: 研究场景下 GPU 服务器通常位于校园网或 VPN 内网, 不适合暴露为公网 Web 服务; Tauri 桌面外壳提供本地文件系统访问 + 系统 SSH 调用, 满足研究者日常工作流
- **本地后端为程**: FastAPI 在本地运行, 管理 job 生命周期 / SSH 连接 / 结果缓存, 避免对远端服务器部署 Web 服务的依赖
- **透明 SSH 调度**: 模型执行通过系统 SSH + SCP 完成, 不依赖特定远端服务, 兼容各类服务器配置
- **可移植包装**: 通过内嵌 Python 分发 + React 构建 + Tauri 单文件分发, 实现一键部署 (per PORTABLE_BUNDLE.md)

#### 4-B.2 模型注册与执行合同

KYKT 平台定义统一的模型注册与执行合同:

- **模型注册 (model_registry.py)**: 每个模型携带 ID / 名称 / 族 (DUSt3R 族 / MonST3R 族) / 运行状态 / 参数族 / 输出合同 / 服务器环境信息; 新模型接入仅需: 注册模型 → 添加 runner → 添加 SSH dispatch 分支
- **Runner 合同**: 每个模型的 runner (e.g., dust3r_runner.py / monst3r_runner.py / spann3r_runner.py) 遵守相同的 I/O 合同: 读取 job.json → 执行推理 → 输出 scene_meta.json + 标准 output/ 目录结构
- **Job 生命周期**: 创建 → 准备远端目录 → 上传输入 → 上传 runner → 远端执行 → 下载结果 → 完成/失败; 状态转移通过 status.json 跟踪
- **当前覆盖**: DUSt3R (smoke ✓) / MASt3R (smoke ✓) / MonST3R (smoke ✓) / Spann3R (smoke ✓) / Fast3R (前向通过) / CUT3R (环境就绪, runner 待写)

这一合同设计保证新模型接入时无需修改前端 / 调度层 / 评估层, 仅需实现 runner + 注册元数据, 边际成本可控。这是 Q4-a (新模型接入低边际成本) 的架构基础。

#### 4-B.3 统一评估框架

KYKT 平台提供三层评估机制:

- **自动指标层**: 每个 job 完成后自动生成 result_summary.json + result_summary.md, 包含运行时、内存占用、输出完整性 (artifact count / expected vs actual)
- **手动评分层**: evaluation.json 支持人工评分 (quality / completeness / notes), 保存在 local_jobs/<job_id>/ 下, 在前端可视化展示
- **AI 评估层**: advisor.py 接入 OpenAI-compatible API, 可对已完成 job 进行自动诊断 / 建议 / 报告生成 (per settings/advisor.json 配置)
- **样本矩阵 (Sample Matrix)**: samples_manifest.json 定义跨模型对比样本集, 前端提供排序 / 筛选 / 批量操作 / 报告导出 / locate-job 联动

该评估框架为 Dream3R ABL-v02-4 (best-of-N vs single-expert) 提供横向对比基础设施, 也为 Q4-b (跨模型对比矩阵) 提供工程实现。

#### 4-B.4 应用对接层 (概念设计)

本阶段 KYKT 平台以研究工具为主; 后续计划将推理能力封装为应用对接层, 概念设计包括:

- **REST API 封装**: 将已经准备好的 model_registry + runner 合同包装为 HTTP 接口, 提供 /infer (单次推理) + /batch (批量推理) + /compare (多模型对比) 端点
- **gRPC streaming (候选)**: 对于 Spann3R / CUT3R 等流式模型, streaming 接口更自然; gRPC 作为候选传输协议
- **下游应用场景 (概念)**: 点云编辑 / AR 场景重建 / 数字孪生 / 自动驾驶感知 等需要三维重建能力的场景, 通过 API 层获取 KYKT 平台的多模型推理服务

本节仅为概念设计, 不吸取实装承诺; 实装时序见 §8 P-6 里程碑。

#### 4-B.5 与 Dream3R 架构的协同关系

KYKT 平台 (支柱 B) 与 Dream3R 架构 (支柱 A) 的协同关系体现在三个层面:

- **执行层**: Dream3R 的 ABL-v02-1..10 / ABL-memory-0..11 / Critic 标定 / 长序列评测均可通过 KYKT 平台的 SSH 调度执行, 本地桌面端实时跟踪状态与结果
- **对比层**: Dream3R C5 Composer 7-expert pool 的实证评估通过 KYKT 平台的 Sample Matrix 与评估框架组织多模型对比数据
- **演进层**: Dream3R 未来版本 (v0.4+) 可作为 KYKT 平台上的新模型接入, 与现有 3R 模型在同一评测框架下对比

这一协同关系保证: (a) 支柱 A 的研究问题 (Q1-Q3) 有可执行的工程基础, (b) 支柱 B 的研究问题 (Q4) 有明确的上层应用场景 (= Dream3R 消融评估), (c) 两支柱可独立评估且互相增强。

---

## §5 消融与评测设计

本章在三个 SPEC + 两个 cycle 035 plan + 一份服务器端 progress ledger 的基础上, 描述 Dream3R v0.3 的评测协议: §5.1 给出三层证据阶梯, §5.2-§5.5 展开四组消融 / 标定 / 长序列评测, §5.6 列出评测数据集, §5.7 列出主要评测指标。本章为 plan-level, 所有 ABL-v02-N / ABL-memory-N / Critic 校准 / 长序列评测的执行 gated on F-002 server authorization 与 per-step DEC, 不在 cycle 040 启动。

### 5.1 三层证据阶梯

per DEC-20260503-001 (research-code-discipline) rule 5 Honesty Override + cycle 008.5 evidence ladder, Dream3R 评测证据按三层逐层升级, 每层都有独立的 falsification 标准:

- **L1 论文层证据 (paper-derived)**: 综述 §1-§10 涵盖的 44 引文 + cycle 013 SPINE_* 4 个 finalist 文献骨干 + cycle 008.5 finalist mechanism spec 引述。本层证据反映"该机制在论文中报告了如此表现", 不构成本研究的实证主张。
- **L2 代理用例层证据 (case-derived)**: cycle 009-012 的 13 张 case card (CRITIC-01..03 / MEMORY-01..03 / PERMANENCE-01..03 / COMPOSER-01..05) 在 paper-derived 与 KYKT-metadata-derived 数据上验证 cross-spec signal contract v2.1 (CR-1..CR-6) 的可行性。本层证据反映"按现有论文 + 内部 metadata 可以 instantiate 信号契约", 不构成 v0.3 架构层 best practice 的最终实证。
- **L3 原型实现层证据 (code-observed)**: code/dream3r/ 的 W1-W18 实装 + cycle 034 KITTI smoke (pointmap L2 = 20.4747 on 2011_09_26_drive_0001_sync_02, windows=2; per RECENT_PROGRESS.md line 56-78: integration evidence, not trained reconstruction quality) + cycle 031 local ABL-memory-0 fixture/logging gate pass (22/22 validity checks)。本层证据反映"v0.3 架构端到端 pipeline 跑通, fixture/logging 基底通过 validity gate", 不构成模型质量 / 训练后表现 / 论文-级别 claim 的实证。

三层证据互不替代: L1 是上游 framing, L2 是 cross-spec 信号契约的 cycle-级 stress test, L3 是 W-task 级实装。§5.2-§5.5 列出的所有 ABL / 标定 / 长序列评测均 L3 级活动, 执行后才能升级该 ABL 的 evidence label 至 code-observed; 执行前仍为 plan-only。

### 5.2 架构层消融实验组 (ABL-v02-1..10)

per SPEC-20260506-005 v0.2 + SPEC-20260507-002 v0.3 addendum, 架构层消融组覆盖 v0.2 六个 Delta + v0.3 ABL-v02-10 addendum, 共 10 项 ABL 分三个 tier:

**Tier 1 (load-bearing 4 项)**:

- ABL-v02-1 NSA-removal: 把 C2 Memory 的 NSA selected branch 退化为 cosine top-k, 检验 Delta 3 (NSA 三分支) + Delta 4 (Sparse Attention as architectural optimization) 的边际贡献。Pillar A + Pillar E 双向 falsification 入口。
- ABL-v02-4 Composer best-of-N: 7-expert pool vs single-expert isolation, 检验 Delta 5 (7 admitted experts) + Delta 6 (A+D pillar narrowing) 的实证基础。Pillar D 主 falsification 入口; §3.3 Q3 核心证据来源。
- ABL-v02-6 selection-gate signal subsetting: Critic-only / Permanence-only / Both / Neither 四 variants, 检验 Delta 3 verification coupling 与 C4 Critic 信号通道的边际贡献。Pillar A + E 共同 falsification 入口; §3.1 Q1 核心证据来源。
- ABL-v02-10 Test3R-alone comparator (cycle 023 v0.3 addendum 新增): full Critic + bus gates + Test3R lazy vs Test3R built-in verifier only, 同 trigger frequency, 检验 Pillar A robustness — 若 Test3R-alone 匹配或超过 Dream3R Critic-gate pipeline, Pillar A 弱化或证伪。§3.1 Q1 + §3.3 Q3-b (Test3R 内置 verifier 边际) 双向证据。

**Tier 2 (training 维护 4 项)**:

- ABL-v02-2 DINOv3 backbone tier: -S vs -B vs -L 三 variants, 检验 Delta 2 backbone 替换的 weight-class regression vs ViT-L baseline 的 robustness。
- ABL-v02-3 frozen vs partial-unfreeze: top-2/4 blocks 解冻 vs 全微调, 检验 frozen-backbone 决策的 training cost / quality tradeoff。
- ABL-v02-7 head training schedule: head-only vs multi-stage warmup vs full joint, 检验 v0.3 训练 stability + 收敛。
- ABL-v02-8 frame-budget benchmark: per-component + end-to-end + lazy-path latency on TITAN RTX 24GB, 检验 Delta 1 30-50 ms/frame budget + 30 FPS compliance。

**Tier 3 (longer-tail 2 项)**: ABL-v02-5 capability_match measurement (per-expert per-regime 度量); ABL-v02-9 NSA kernel benefit decomposition (hardware-aware vs algorithmic-only vs plain dense+top-k; cu121 portability)。

ABL-v02-4 内附 **VGGT offline-batch baseline** (per SPEC-20260507-002 v0.3 addendum Variant X): VGGT (~1.2B) 在同 benchmark 上以 offline-batch 模式运行, 与 Dream3R streaming-first Composer 在 B1+B2+B4 三类 benchmark 上对比。Honest framing: Dream3R 的 streaming-first 优势是 streaming-specific, 非 universal-on-batch; 该 baseline 是 Pillar D threat (per cycle 022 paper §6 v0.2 comparator positioning) 的实证回应。

整体合规预算约 1377 GPU-hours (per cycle 023 v0.3 addendum), 含 Tier 1 + Tier 2 + Tier 3 + ABL-v02-10 + VGGT baseline; 实际执行按 per-ABL 单独 DEC + F-002 服务器授权逐步推进, 不在 cycle 040 启动。

### 5.3 记忆机制消融实验组 (ABL-memory-0..11)

per SPEC-20260508-002 (v1.1 cycle 029 reviewed and corrected), 记忆机制消融组针对 SPEC-008 v0.3 提出的 C2 Memory v0.3 变体 (V0 vector AnchorBank / V1 spatial key-value bank / V2 state-token recurrence / V3 hybrid bus-gated writes) 在 P0 静态 tensor fixture (R1 loop / R2 drift / R3 dynamic / R4 conflict / R5 budget 五类 regime) 上展开 12 项 ABL:

- **Tier 0 验证 fixture/logging 基底**: ABL-memory-0 (cycle 031 已执行通过 22/22 validity checks; 该通过仅 = fixture + logging substrate 通过, 不 = C2 memory 质量验证)
- **Tier 1 load-bearing memory 主张 5 项**: ABL-memory-1 spatial vs vector bank (V0 vs V1 vs V3 in R1) / ABL-memory-3 state-token recurrence (V0 vs V2 vs V3 in R2 continuity + drift) / ABL-memory-4 bus-gated dynamic suppression (V1 ungated vs V3 gated in R3) / ABL-memory-5 conflict quarantine (V1 vs V3 in R4) / ABL-memory-6 utility pruning vs LRU (V1/V3 in R5 future-use survival)
- **Tier 2 训练维护 + uncertainty 3 项**: ABL-memory-2 duplicate filtering / ABL-memory-7 entropy as uncertainty signal / ABL-memory-8 operation proxy + latency envelope
- **Tier 3 未来 P1/P3/P4 集成 3 项**: ABL-memory-9 value payload source / ABL-memory-10 memory before vs after decoder / ABL-memory-11 NSA gate after payload semantics

cycle 029 v1.1 review 后 5 项关键 correction 已入册 (per MEMORY_V03_ABLATION_REVIEW.md R-029-1..5):

- **R-029-1 Oracle-bus boundary**: P0 fixture 允许 synthesize 5 个 bus oracle 字段 (`dynamic_ratio` / `suppress_static_write` / `conflict_score` / `permanence_link` / `capability_match`) 作为 cross-spec 信号; **禁止** V0/V1/V2/V3 直接 read 3 个 ground-truth 字段 (`group_id` / `is_dynamic` / `is_corrupt`), 否则 oracle 泄漏导致评测无效
- **R-029-2 Hard/soft fail rule**: hard_fail = metric fails condition + logs valid (本研究记录 go/no-go); soft_fail = inconclusive / weak denominator / repairable interface issue (本研究 escalate, 不直接 no-go)
- **R-029-3 State-token stale-smooth fail**: 状态记忆向量 V2 在 R2 drift 上 stale-smooth 模式 (写后立即读, 无 recurrence) 必须 fail; 不允许 V2 silently 用同窗口 zero-recurrence 形态过 ABL-memory-3
- **R-029-4 Op proxy-only cost claim**: ABL-memory-8 cost label 只能用 operation proxy (multiply-adds + memory ops), 不能用 wall-time (因 P0 静态 fixture 与 server 真实 GPU latency 不可比)
- **R-029-5 Controlled loop/revisit narrowed**: ABL-memory-1 / 6 的 "revisit accuracy" 主张限定在 fixture-controlled loop, 不延伸至真实序列

执行后才能升级该 ABL 的 evidence label, cycle 040 仅 plan-level 引用; cycle 031 已执行的 ABL-memory-0 通过仅适用于 Tier 0 验证, 不构成 Tier 1-3 主张证据。

### 5.4 校验阈值标定方案 (CRITIC_CALIBRATION_PLAN_V1)

per cycle 035 P0-1 deliverable CRITIC_CALIBRATION_PLAN_V1.md, C4 Critic 当前的 unified `theta_conflict` 单阈值替换为按六类失败模式 × 5 sub-signal 的 30-scalar 阈值表。5 sub-signal 命名: `pose_novelty` / `view_overlap` / `reprojection_residual` (Sampson 类) / `pointmap_conflict` (depth 一致性) / `confidence_drop`。

六类失败模式 → primary + secondary signal 映射 (per CRITIC_CALIBRATION_PLAN_V1.md §3 表):

- A1 弱纹理: primary confidence_drop + secondary reprojection_residual (反向); 子类特征 = 稀疏匹配 + 残差分布偏移
- A2 镜面玻璃: primary pointmap_conflict + secondary depth-RGB inconsistency; 反射 vs 真实几何二元
- A3 快速运动: primary pose_novelty + secondary dynamic_ratio (来自 Permanence); 大帧间位姿变化
- A4 长基线: primary view_overlap (低/反向) + secondary reprojection_residual (基线放大); 共视区小 + 大视差
- A5 尺度漂移: primary latent_drift_proxy (来自 Memory) + secondary confidence_drop (累积); 长序列累积
- A6 域外 (OOD): primary confidence_drop (全局低) + secondary route_regret_estimate (Composer; 高 = 无适配 expert); 训练分布外

标定 method 选择 decision tree:

- **Method A (distribution-quantile, P0)**: 在 sub-sample histogram 上取 P95 quantile; 无需 ground-truth labels; 是 cycle 040 - cycle 041 时间窗口内的默认起点
- **Method B (supervised binary classifier, P1)**: 需要 per-pixel L2 ground-truth; 输出 mode-distribution probabilities; 需 v0.4 spec delta 起草作为入口

5-metric validation gate (per §6 of CRITIC_CALIBRATION_PLAN_V1.md):

1. mode_estimate accuracy ≥ 80% (P0) / ≥ 95% (P1) per sub-sample
2. per-mode P95 vs single theta_conflict 在 KITTI 2-window smoke 上不回归 (baseline L2 = 20.47 不变差)
3. fixed seed 下重复 calibration: P95 阈值 variance < 5%
4. dataset license 链 clear 一项独立 calibration DEC
5. fallback path 完整: 若 mode_estimate 失败, 退回 v0.3 single threshold, 不 silent unknown repair

整体规模 ~30 scalar threshold + sub-sample 分组采样规则; 执行 gated on F-002 server authorization + 独立 DEC, 不在 cycle 040 启动。

### 5.5 长序列真实数据评测 (LONG_SEQ_REAL_TABLE_PLAN)

per cycle 035 P0-3 deliverable LONG_SEQ_REAL_TABLE_PLAN.md, 在 KITTI long windows ∈ {10, 20, 50, 100} 上展开 4 ablate_recurrence variants × 4 long-sequence metrics 的对照评测:

**4 ablate_recurrence variants** (现有 ablate_recurrence.py 实装):

1. baseline_cross_attention: cross_attention recurrence + NSA + stable_memory (对照 baseline; 综述 §6 B1 递推状态)
2. mamba_hybrid: mamba SSM recurrence + NSA + stable_memory (Dream3R v0.3 默认; 综述 §6 B3 混合记忆)
3. no_nsa: mamba SSM + 移除 NSA + stable_memory (检验 NSA 三分支边际)
4. no_stable_memory: mamba SSM + NSA + 移除 stable_memory (检验 active/stable 分离边际)

**4 long-sequence metrics** (新增, 区别于 §5.7 一般 pointmap 指标):

- D1 scale_drift_proxy: pointmap L2 ratio per physical point across windows; 单调上升 → drift
- D2 memory_decay_proxy: P(selected_indices_window_i ∩ written_window_0); 衰减 → anchor forgetting
- D3 anchor_fill_rate: nonzero_anchors / K (K=256); 饱和 → budget triggered
- D4 retrieval_diversity: unique_indices / sum_indices; 高 = 健康 / 低 = "hot anchor" 重复

**Windows staging** (monotone upgrade gate, per LONG_SEQ_REAL_TABLE_PLAN §3): KITTI-LONG-10 (40 frames, seq 00 partial) → KITTI-LONG-20 (80 frames, seq 00/02 partial) → KITTI-LONG-50 (200 frames, seq 04/06) → KITTI-LONG-100 (400 frames, seq 00/05/07 complete)。每一档跑 ≥ 3 seeds; 高档需先通过低档的 elapsed_ms_mean + D1-D4 stability gate 才推进。

**B4 缓存治理 coverage gap (per §3 plan)**: 4 variants 覆盖综述 §6 B1 递推状态 + B2 空间指针 + B3 混合记忆三档, **不覆盖** B4 预算治理 (LONG3R-style dynamic pruning)。cycle output 须在 §B4 子节明示 "4 variants 不覆盖 §6 B4 子类, 避免读者误读"。B4 closure 需 v0.4 spec delta 候选 (动态剪枝接口) 或 v0.4 evaluation extension。

6-metric validation gate (per §6 of LONG_SEQ_REAL_TABLE_PLAN.md): windows=3 baseline 不回归 cycle 033 synthetic / D1-D4 stability < 5% / B4 sub-class 明示 uncovered warning / windows upgrade monotone / ≥ 3 seeds per variant / KITTI sequence selection 在 startup DEC 中 fix 不 runtime cherry-pick。

预计资源约 10 GPU-hours single-GPU for full sweep; 执行 gated on F-002 server authorization + 独立 DEC, 不在 cycle 040 启动。

### 5.6 评测数据集

Dream3R v0.3 的评测数据集分三层:

- **静态 fixture (R1-R5, cycle 031 已实装)**: 确定性 tensor fixture, 不依赖外部数据集 license; 用于 ABL-memory-0..8 在 fixture-controlled regime 下的对照 (R1 loop / R2 drift / R3 dynamic / R4 conflict / R5 budget)。优势: 完全可重现; 劣势: 不反映真实 dataset distribution
- **KITTI 真实数据 (cycle 034 已通过 smoke)**: 已实装 data/kitti_real.py + evaluate_real_sequence.py + KITTI rectified RGB/depth 加载链; cycle 034 smoke 在 2011_09_26_drive_0001_sync_02 的 2 windows 上跑通, pointmap L2 = 20.4747 + depth RMSE = 21.8658 (integration evidence, 非训练后质量, per §7.3)。开题报告期间 KITTI 是主评测集合 (KITTI-LONG-10 / 20 / 50 / 100 staged)
- **DTU 拟扩展 (W19 unblocked task)**: data/dtu.py loader stub 已起草, 但 DTU license 链 + multi-view registration loader 仍 W19 任务; cycle 040 引用为 plan, 不在 cycle 040 启动

per cycle 034 经验, KITTI 的 rectified + GPS 同步窗口对作为 streaming 输入比较友好; DTU 的多视图 + 稀疏 calibration 更接近 SPEC-007 v0.2 Tier 1 in-pool 7 expert 中 MASt3R / Spann3R 的原 paper 评测协议, 是 §5.2 ABL-v02-4 Composer best-of-N 实证需要扩展的数据集。后续 W19 + DTU loader 接入 + 评测协议补充 stays gated on 独立 DEC + F-002 server authorization。

### 5.7 主要评测指标

Dream3R v0.3 在三层证据阶梯上使用的主要评测指标分四组:

- **pointmap / depth 几何指标**: pointmap L2 (per-pixel 三维点 L2 误差) + depth RMSE + per-mode pointmap quality decomposition (按六类失败模式分子样本); 适用 §5.2 ABL-v02 全部 + §5.4 Critic 标定 + §5.5 长序列评测
- **路由指标**: route_regret (cost-typed per v2 contract, DEC-20260504-004) + capability_match spread + epsilon_tie window hit rate + fail_fast trigger rate; 适用 §5.2 ABL-v02-4/5/6 + §3.3 Q3 best-of-N vs single-expert 对照
- **记忆指标**: scale_drift_proxy / memory_decay_proxy / anchor_fill_rate / retrieval_diversity (4 项 per §5.5) + latent_drift_proxy (CR-3 信号路径) + write_value_estimate (CR-2 信号路径); 适用 §5.3 ABL-memory 全部 + §5.5 长序列评测
- **校验指标**: conflict_score / theta_conflict trigger rate + per-mode mode_estimate accuracy + repair action success rate + Critic-Composer reroute (A5) hit rate (per CR-1); 适用 §5.4 Critic 标定 + §5.2 ABL-v02-6/10

cross-spec consistency 指标 (per CR-1..CR-6 v2.1): cross_spec_refusal log count + forward-reference null occurrence + evidence label preservation rate at consumption (per CR-5); 适用所有 ABL 的 cross-spec 信号路径审计。

所有指标在 cycle 040 仅 plan-level 引用, 执行 gated; cycle 034 KITTI smoke 的 pointmap L2 = 20.4747 + depth RMSE = 21.8658 是唯一已有的 L3 真实数据数值 (集成证据, 非训练后质量)。

### 5.8 平台层评测标准 (支柱 B)

支柱 B (KYKT 聚合管理平台) 的评测标准与支柱 A (架构层算法指标) 不同, 采用工程效率与可复现性指标:

- **新模型接入耗时 (Q4-a)**: 衡量新模型从“环境就绪”到“首次 smoke 通过”的平均工时 (person-hours); 目标: 在 6 模型接入经验基础上, 后续新模型接入≤ 8h 工时 (runner 写作 + smoke + 注册)
- **统一合同覆盖率 (Q4-a)**: 已接入模型中, 完整遵守 runner I/O 合同 (job.json → scene_meta.json + output/) 的比例; 目标: ≥ 80% (5/6 模型完整合同)
- **跨模型对比矩阵完整性 (Q4-b)**: samples_manifest.json 中定义的对比样本集上, 实际产出有效结果的 (model × sample) 单元格占比; 目标: ≥ 60% (4/6 模型 × 全部对比样本)
- **API 对接能力 (Q4-c)**: REST API 层是否能够成功提供单次推理 / 批量推理 / 多模型对比三类端点 (候选指标, 仅概念验证)

评测方式: 平台层评测不依赖 F-002 server authorization, 可在本地环境 + 现有服务器上执行; 评测时序见 §8 P-1..P-7 里程碑。

---

## §6 预期成果

本章按三个子节给出本研究的预期成果与创新点。§6.1 列出本研究的预期交付物 (架构设计文档 + 原型实现 + 评测结果 + 综述与方法学副产物 + KYKT 平台); §6.2 把 §3 四个 Q (Q1 验证 / Q2 长序列内存 / Q3 多专家组合 / Q4 统一平台) 对应的四个创新点 (IP1 verification-as-architecture / IP2 heterogeneous best-of-N Composer / IP3 NSA-hybrid memory / IP4 统一聚合管理平台) 显式声明; §6.3 阐明本研究与现有工作的实证差异 — 本研究 **不** 主张 Dream3R 相对 SOTA 压倒性领先, 主张提供多机制并置的对照实验证据。三个子节都受 STYLE_CONTRACT §5 candidate-not-final 句式表硬约束。

### 6.1 预期交付物

本研究的预期交付物分四类:

**架构设计文档**: Dream3R v0.3 的完整 SPEC 系列 (已有 SPEC-20260506-004 v0.2 + SPEC-20260508-001 v0.3 + SPEC-20260507-001 v0.2 + SPEC-20260507-002 v0.3 + SPEC-20260506-005 v0.2 + SPEC-20260508-002 + paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md v2.1 七份), 加上 cycle 035 SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §5 提出的 v0.4 spec delta 候选 (B1 Critic 路径拆分 / B2 输出资产契约 / B3 输入扩展 axis), 在开题报告时间窗口结束 (M5 节点) 之前形成 v0.3 完整稿 + v0.4 spec delta 候选清单。

**原型实现**: code/dream3r/ (服务器部署 /hdd3/kykt26/code/dream3r/), 当前 W1-W18 完成 (per RECENT_PROGRESS.md), 包括 DINOv2 backbone 实际跑通 + 3D-aware retrieval + active/stable state + Grassmannian 正则化 + 几何 Critic + ISA slot + 真实 MASt3R + Spann3R adapter + W17 Mamba-Transformer 混合循环 + W18 GaussianHead tensor 契约 (renderer-free)。开题报告时间窗口内的预期延伸: W19 多专家真实加载 + W20 路由层实装 + W21-W22 ablate_recurrence + critic_calibration 真实数据扩展。W23-W30 (DTU loader / TTT / 4DGS renderer / 真实数据训练) 作为 post-开题报告 work, 不在预期交付物声明范围内。

**评测结果**: ABL-v02-1..9 + ABL-memory-0..11 + cycle 035 CRITIC_CALIBRATION_PLAN_V1 + LONG_SEQ_REAL_TABLE_PLAN 在 KITTI 真实数据上的对照实验数据集合, 包括 (a) §3.1 Q1 verification 路径的 evaluation gating data (拆分前 hybrid v0.3 实证基线), (b) §3.2 Q2 长序列内存四类机制在 windows ∈ {10, 20, 50, 100} 上的协同/冲突显现数据, (c) §3.3 Q3 best-of-N vs single-expert 的 pointmap L2 + route_regret + scale_drift_proxy 对照数据, (d) Test3R-alone 在 pillar A 上与 Dream3R Critic-gate pipeline 的对照数据 (per ABL-v02-10)。所有评测结果都以"评估候选架构 X 是否在 ... 维度上呈现优势"的句式呈现, 不以"宣称 X 优于 SOTA"的句式呈现。

**综述与方法学副产物**: Track B 3R-mix 中文综述 (18 A4 页 / 44 引文 / 6 图 5 表 / 2026-05-15 prose naturalization deliverable, arXiv 自存档路线) 是本研究的方向定调副产物, 已在 cycle 036 packaging 完成 SHA256 pre-fill。Track A 与 Track B 共享 references.bib 但不互相引用 (sibling artifacts; 词汇隔离声明 in RELATION_TO_TRACK_A_2026-05-16.md)。cycle 035 SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL + SOTA_MATRIX_V2 + CRITIC_CALIBRATION_PLAN_V1 + LONG_SEQ_REAL_TABLE_PLAN 4 markdown deliverables 是综述反哺 Track A 主线的实证副产物。

### 6.2 创新点声明

per §3.1-§3.3 三个 Q 与 §4 六模块设计, 本研究的三个创新点 (Innovation Points, IP) 如下:

**IP1: Verification-as-architecture (校验作为架构组件; 对应 Q1 + §4.5 + Pillar A)**

把几何验证 (一致性检查 + 修复) 显式作为 3R 架构层组件, 而非测试时附加路径或后处理步骤。Dream3R v0.3 通过 C4 Critic (Sampson / depth / 共视 conflict 三类信号 + repair actions 0/1/2 stub 3/4/5) 实现这一架构组件化。creation novelty 不在于"几何验证本身是新概念"(经典 BA / SfM 也含验证元素), 而在于"把验证 + 修复在前馈式 3R 架构内显式作为模块 + 信号契约的一部分"。本研究的对照实验将提供 C4 Critic 在 Dream3R v0.3 内的 (a) 失败模式检出率, (b) 修复动作有效性, (c) 与 Test3R 内置 verifier 在测试时一致性优化上的对照数据。

句式约束: 不说 "Dream3R 已完全解决几何验证问题"; 说 "Dream3R 在架构层提供了几何验证的候选模块设计 + 对照实验证据"。

**IP2: Heterogeneous best-of-N Composer (异构多专家组合; 对应 Q3 + §4.6 + Pillar D)**

把多个不同 regime 优势的 3R expert (MASt3R / Fast3R / Spann3R / CUT3R / MoGe-2 / DepthAnything-V2 / Test3R) 通过 capability descriptor + 路由策略组合, 在架构层显式实装 best-of-N 选择。creation novelty 不在于 "best-of-N 路由本身" (经典 ensemble 也含 best-of-N 元素), 而在于 (a) capability descriptor 把每个 expert 在 9 axes 上携带 paper-derived / engineering-derived 标签, (b) 路由由 capability_match spread + cost_adjusted_match + epsilon_tie 决定 (per v2 contract upgrade, DEC-20260504-004), (c) 与 C4 Critic 通过 CR-1 协作路由切换。本研究将提供 best-of-N (7-expert pool) vs single-expert 在 KITTI 真实数据上的 pointmap L2 + route_regret 对照数据。

句式约束: 不说 "best-of-N 路由必然优于单一 expert"; 说 "本研究提供 best-of-N vs single-expert 的对照实验数据"。

**IP3: NSA-hybrid memory (统一覆盖长序列内存四类机制; 对应 Q2 + §4.3 + 综述 §6 四类)**

把综述 §6 抽象出的长序列内存四类机制 (B1 递推状态 / B2 空间指针 / B3 混合记忆 / B4 缓存治理) 在单一 C2 Memory 模块内通过 NSA three-branch + AnchorBank K=256 + StateToken + Mamba-Transformer 混合循环结构 jointly 实装。creation novelty 不在于"NSA 三分支机制本身" (NSA 类机制在文献中已有), 而在于 (a) 把 NSA 三分支映射到长序列内存四类机制的前三档 (compressed ↔ B1, selected ↔ B2, sliding ↔ B3), (b) 同时维持单帧 30-50 ms 帧预算 (per Delta 1), (c) B4 缓存治理 partial coverage 与实证缺口的显式承认 (per cycle 035 LONG_SEQ_REAL_TABLE_PLAN §B4 coverage gap)。本研究将提供 ablate_recurrence 4 variants 在 KITTI windows ∈ {10, 20, 50, 100} 上的 scale_drift_proxy + memory_decay_proxy + anchor_fill_rate + retrieval_diversity 数据。

句式约束: 不说 "Dream3R 已完全解决长序列内存问题"; 说 "Dream3R 在单一架构内同时实装四类机制中的前三档, 为长序列内存机制统一提供候选实证"。

三个 IP 与 §3.1-§3.3 三个 Q 一一对应 (Q1 ↔ IP1; Q2 ↔ IP3; Q3 ↔ IP2)。三个 IP 的 candidate-not-final 共同体现在 "提供 ... 候选 ... + 对照实验证据" 的句式模式, 而非 "宣称 X 优于 Y" 的结论性命题。

**IP4: 面向前馌式 3R 的统一聚合管理平台 (工程创新点; 对应 Q4 + §4-B + Pillar B)**

设计并实现一个面向多模型前馌式 3R 研究的统一聚合管理平台 (KYKT), 通过统一模型注册 / 执行合同 / 评估框架 / 应用对接层四层设计, 为 Dream3R 等新架构的消融实验与跨模型对比提供标准化工程基础设施。creation novelty 不在于“平台概念本身”(工具链平台在 ML 研究中已有 MLflow / Nerfstudio 等), 而在于 (a) 针对前馌式 3R 范式的统一 runner 合同设计 (区别于 NeRF per-scene 工作流), (b) 6 个异构 3R 模型在同一平台上的实际接入与对比, (c) 与 Dream3R 架构研究 (Q1-Q3) 的直接协同。

句式约束: 不说 "KYKT 是唯一可行的 3R 统一平台"; 说 "KYKT 平台为多模型 3R 研究提供了一个统一聚合管理的候选方案 + 工程实证".

四个 IP 与 §3.1-§3.6 四个 Q 对应 (Q1 ↔ IP1; Q2 ↔ IP3; Q3 ↔ IP2; Q4 ↔ IP4)。其中 IP1-IP3 属支柱 A (算法创新), IP4 属支柱 B (工程创新); 四个 IP 的 candidate-not-final 共同体现在 "提供 ... 候选 ... + 实证证据" 的句式模式。

### 6.3 与现有工作的实证差异

本研究与现有 3R 工作的实证差异不在 "Dream3R 相对 SOTA 在某单一指标上压倒性领先" — 这一论断超出本研究的 candidate-not-final 边界, 也与 §4.8 整体定位 + DEC-20260501-011 + DEC-20260504-002 三项决策矛盾。

本研究与现有 3R 工作的实证差异在三个层面:

- **方法学差异**: 现有 3R 工作以 "单一论文一个方法" 的离散发表模式为主; 本研究以 "在统一架构内多机制并置评估" 的对照实验模式为主。前者擅长在某一档 (e.g., B1 递推状态 或 B2 空间指针) 上 push SOTA; 后者擅长在多档之间提供协同 / 冲突 / 边际贡献的对照数据。两者不互替, 是研究方向上的互补关系。
- **失败模式系统化差异**: 现有 3R 工作 (per 综述 §10) 多数把六类典型失败模式作为 "limitations" 章节简要提及; 本研究通过 C4 Critic + cycle 035 CRITIC_CALIBRATION_PLAN_V1 把六类失败模式映射到 5 个 sub-signal 的逐类阈值标定, 提供失败模式系统化的对照实验证据。这一差异是 IP1 的方法学体现。
- **架构组合差异**: 现有 3R 工作以 "single best architecture" 为主; 本研究通过 C5 Composer + COMPOSER_CAPABILITY_DESCRIPTORS 7-expert pool 显式实装 "heterogeneous best-of-N"。这一差异是 IP2 的架构体现。

本研究的实证目标不是把 Dream3R 推上 KITTI / DTU / ScanNet 等单一 leaderboard 的 top-N; 而是在 §5 实验设计指定的 evaluation 协议下, 提供三个 Q 与三个 IP 对应的对照实验数据, 让后续工作 (无论是 Dream3R v0.4 演进, 还是其他 3R 架构) 可以基于这些数据判断: (a) 当前 Dream3R v0.3 在三个 Q 上的覆盖与缺口, (b) v0.4 spec delta 候选 (B1 / B2 / B3) 应优先推进哪一个, (c) 是否有 v0.5 候选架构 需要替换 v0.3 整体设计。这一对照实验数据 + 候选演化路径是本研究的核心实证差异, 也是 candidate-not-final 框架的工程落点。

支柱 B 的实证差异体现在: 现有 3R 研究以“每篇论文一个独立 demo”的离散工作流为主; 本研究通过 KYKT 平台提供“多模型统一调度 + 横向对比 + 研究闭环”的工程实证。这一差异是 IP4 的工程体现, 也是支柱 B 独立于支柱 A 的实证贡献。

---

## §7 已完成工作

本章按六个子节给出 Dream3R 项目截至 2026-05-17 的已完成工作: §7.1 架构设计文档系列, §7.2 实现里程碑 W1-W18, §7.3 KITTI 真实数据集成证据, §7.4 综述 (Track B) 发布, §7.5 综述反哺主线 (cycle 035 4 deliverables), §7.6 cycle 历史。本章 evidence label 严格遵守 RESEARCH_CODE_DISCIPLINE rule 5 Honesty Override: paper-derived / code-observed / engineering-demonstrated / inferred / speculative / unknown 分级标注; pointmap L2 = 20.4747 数值明示为"集成证据, 非训练后质量"。

### 7.1 架构设计文档系列

Dream3R 截至 2026-05-17 的架构设计 corpus 包含 7 份正式 SPEC + 1 份 paradigm 跨 spec 契约 + 若干 planning artifact:

- **SPEC-20260506-001 v0.1 Dream3R 架构 (cycle 016 S2; 1821 行)**: control-graph-as-architecture; hybrid substrate (transformer + SSM + slot + bus); 4 finalist 综合为 C1-C5 + C6 bus; CR-1..CR-6 作为 gates; A1-A8 映射到具体 layer
- **SPEC-20260506-002 v0.1 ablation plan (cycle 016 S3)**: 10 ablations 3 tier; falsification table per architectural claim; B1-B6 benchmark categories
- **SPEC-20260506-003 v0.1 comparator map (cycle 016 S4)**: 14+ models across 7 groups; 8 comparison axes; threat ranking
- **SPEC-20260506-004 v0.2 架构 delta (cycle 018 S4; 6 deltas)**: 帧预算 30-50 ms (Delta 1) / DINOv3-S 替换 ViT-L (Delta 2) / bounded anchor bank + NSA retrieval (Delta 3) / Sparse Attention as engineering optimization (Delta 4) / 7-expert Composer pool (Delta 5) / 主张窄化为 Pillar A + Pillar D (Delta 6); v0.1 body 不动 per DEC-002
- **SPEC-20260506-005 v0.2 ablation v0.2 (cycle 019 S2)**: 9 ABL-v02 + per-ABL review checklist for other-agent handoff; 主张映射 v0.2 Deltas 1-6
- **SPEC-20260507-001 v0.2 comparator v0.2 (cycle 021 S3; 880 行)**: 5-tier 重组 (in-pool 7 / out-of-pool 3 / out-of-scope 1 / foundation 1 / orthogonal 8) + 3 NEW axes 9-11 (NSA / DINOv3 / Composer pool) + Pillar A/D 威胁重排
- **SPEC-20260507-002 v0.3 addendum (cycle 023 S3)**: 增 ABL-v02-10 Test3R-alone Tier 1 comparator + VGGT offline-batch baseline annotation + Pillar A 4 sub-claim × primary ABL falsification map + 更新 compute budget ~1377 GPU-hours
- **SPEC-20260508-001 v0.3 C2 Memory addendum (cycle 026 S3)**: supersedes Delta 3; vector GRU + vector AnchorBank + NSA-label 升级为 latent state-token recurrence + explicit spatial key/value memory + geometry-aware bus-gated writes; CUT3R-like state tokens / Spann3R-like spatial bank / recent frame-value tokens
- **SPEC-20260508-002 v1.1 Memory ablation addendum (cycle 028 + cycle 029 review)**: ABL-memory-0..11 + cycle 029 R-029-1..5 corrections (oracle-bus boundary, hard/soft fail rule, state-token stale-smooth fail, op proxy cost, controlled loop narrowed)
- **paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md v2.1 (cycle 011 + cycle 011 v2.1 additive)**: CR-1..CR-6 跨 spec 信号契约 + forward-reference null protocol 子协议 (v2.1 additive per DEC-20260505-001)
- **planning 配套**: COMPOSER_CAPABILITY_DESCRIPTORS (cycle 018 S2) / NSA_MEMORY_INTEGRATION_MEMO (cycle 018 S3) / DINOV3_C1_INTEGRATION_MEMO (cycle 018 S3) / MEMORY_V03_DESIGN_STUDY (cycle 025) / MEMORY_V03_P0_PROTOTYPE_PLAN (cycle 027) / MEMORY_V03_ABLATION_REVIEW (cycle 029) / SOTA_MATRIX_V2 (cycle 035 P0-2) / CRITIC_CALIBRATION_PLAN_V1 (cycle 035 P0-1) / LONG_SEQ_REAL_TABLE_PLAN (cycle 035 P0-3) / WORK_RISK_REGISTER v1.2 (cycle 036 +3 proposal-cycle 行)

所有 SPEC 在 git 历史 + cycle log 中可回溯; v0.1 body 在 v0.2 / v0.3 addendum 中保留不动 (per RESEARCH_CODE_DISCIPLINE rule 3 surgical edits + rule 5 honesty override)。

### 7.2 实现里程碑 W1-W18

per code/dream3r/RECENT_PROGRESS.md (服务器部署 /hdd3/kykt26/code/dream3r/), 截至 cycle 034 (2026-05-11) Dream3R v0.3 在服务器端通过两层验证:

**Tier 1 集成验证 (11 项, code-observed)**:

- v0.3 forward / backward 整 pipeline 跑通
- multi-window streaming state 更新
- NSA 三分支 (compressed / selected / sliding) mixing
- active → stable memory promote / recall
- 3D-aware AnchorBank retrieval
- C4 Critic repair action handoff (A5 reroute → C5 Composer)
- C3 Permanence slot pose tracking
- Mamba recurrence factory & demo
- W18 GaussianHead tensor 契约 (no renderer, renderer-free)
- 合成 ablate_recurrence & visualization
- KITTI rectified RGB/depth loader + evaluate_real_sequence.py

**Tier 2 真实数据 smoke (code-observed; cycle 034)**:

- KITTI rectified RGB/depth windows 加载链跑通
- 两 windows 真实序列通过 Dream3R 完整 pipeline 前向
- evaluation JSON 产出
- 实测: pointmap L2 = 20.4747, depth RMSE = 21.8658

**主要实装文件清单** (code/dream3r/):

- `bus.py`: C6 Memory Bus typed signal 命名空间 + CR-1..CR-6 gates (零参数)
- `modules.py`: C1 Perceiver (ViT backbone + heads) / C2 Memory (GRU + Mamba) / C3 Permanence (Slot Attention) / C4 Critic (TransformerEncoder) / C5 Composer (table join)
- `mamba_block.py`: Mamba-Transformer hybrid recurrence backbone (W17)
- `gaussian_head.py`: GaussianHead tensor 契约 (W18, renderer-free)
- `memory_anchor_bank.py` + `nsa_attention.py`: NSA three-branch + AnchorBank K=256
- `composer_experts/`: 7-expert adapter 子目录 (MASt3R / Fast3R real loaded; CUT3R / MoGe-2 / DepthAnything-V2 / Test3R stub)
- `data/kitti_real.py` + `evaluate_real_sequence.py`: KITTI 真实数据 loader + evaluation entry
- `ablate_recurrence.py` + `export_demo_artifacts.py`: 4 variants 合成 ablation + demo artifact export
- `tests/test_isa_slots.py`: W16 ISA pose stress tests

ABL-memory-0 在本地 P0 scaffold (cycle 031, experiments/prototypes/memory_v03_p0/) 通过 22/22 fixture / logging validity checks; 该 pass 仅 = Tier 0 fixture/logging substrate 验证, **不** = C2 memory 质量 / retrieval 质量 / recurrence 质量 / reconstruction 质量 / 模型行为 / 论文 claim 验证。

### 7.3 KITTI 真实数据集成证据

per cycle 034 + RECENT_PROGRESS.md line 56-78, Dream3R v0.3 在 KITTI 真实序列上的首次真实数据 smoke:

```text
dataset    : kitti_rectified
sequence   : 2011_09_26_drive_0001_sync_02
windows    : 2 (相邻 frame pair)
device     : cuda
backend    : mamba_ssm
pointmap L2: 20.4747
depth RMSE : 21.8658
```

**evidence label 边界声明 (per RECENT_PROGRESS.md line 78)**:

```text
This is real-data integration evidence, not SOTA reconstruction
accuracy. The numbers reflect that the entire pipeline (data load
→ C1 Perceiver → C2 Memory → C3 Permanence → C4 Critic → C5
Composer → C6 Bus → 输出 4D pointmap + dynamic mask) runs end-to-
end on real KITTI rectified frames without crashing or silent
NaN. The numbers do NOT reflect trained reconstruction quality,
do NOT support any SOTA-comparable claim, and do NOT close any
of the §3 Q1/Q2/Q3 research questions.
```

L2 = 20.47 / RMSE = 21.87 在 KITTI rectified 上的数量级位于"集成跑通 + 输出 shape 正确 + 数值在合理范围"区间; 训练前 baseline 数值, 未经过 v0.3 端到端训练。任何后续 Q1/Q2/Q3 实证主张 (per §3 + §6) 都需要 W19-W30 训练 + 真实数据 ABL + KITTI long-window evaluation, 这些仍 gated on F-002 server authorization + 独立 DEC。

### 7.4 综述发布 (Track B 3R-mix)

Track B 中文 3R 综述于 2026-05-06 启动 (cycle 034 S8 + 0513 series), 2026-05-14 wound down 至 route C arXiv-only (per RELATION_TO_TRACK_A_2026-05-16.md):

- **形态**: 18 A4 页 LaTeX (ctexart + xelatex + unsrtnat); 10 sections; 6 figures (4 TikZ + 2 paper-Fig.1 composites); 5 booktabs tables; 0 LaTeX errors / 0 warnings
- **引文**: 44 BibTeX entries, 全部 cite (无 \nocite{*}); CroCo + MASt3R 机制 段补充 2026-05-14
- **figures**: dust3r / vggt / monst3r / cut3r 4 paper Fig.1 crop 嵌入 (per 2026-05-13 user-confirmed reuse license; 仅 4 篇)
- **deliverables**:
  - `deliverables/3r_survey_stage_final_2026-05-13.pdf` (基线 polish)
  - `deliverables/3r_survey_stage_final_2026-05-13_refined.pdf` (cycle 034 三轮 polish)
  - `deliverables/3r_survey_stage_final_2026-05-14_quality.pdf` (CroCo + §10 失败模式 + fig:timeline 修订)
  - `deliverables/3r_survey_stage_final_2026-05-15_natural.pdf` (2026-05-15 prose naturalization deliverable; **当前推荐提交 PDF**)

**词汇隔离 (per cycle 034 G2 grep verified)**: main.tex / references.bib / notes/* 均 0 hit on `Dream\|Dream3R\|KYKT\|agent\|skill\|workflow\|本地项目\|cycle\|SPEC-\|DEC-\|CR-`。综述 manuscript surface 不出现 Dream / KYKT 内部 vocabulary, 是 sibling artifact (per Dream/3R-mix/deliverables/RELATION_TO_TRACK_A_2026-05-16.md)。

**提交 packaging (cycle 036 + cycle 037)**: `deliverables/SUBMISSION_PACKAGE_ADVISOR_2026-05-16.md` (~600 字 中文 cover note, G2 vocab-clean) + `deliverables/SUBMISSION_RECORD_2026-05-16.md` (含 recipient / channel / submitted_at slot + pdf_sha256 = A0763DB7AB7A1E8E1427D4DCC8CB62BC15F94F3F2D915AD0BFBB235CC99C64B0 pre-filled 2026-05-16) + `deliverables/RELATION_TO_TRACK_A_2026-05-16.md` (~600 字 internal meta, 不与 PDF 同包提交)。实际提交动作 (email / IM / portal / offline) 是用户 cycle 外人工动作; packaging stands ready。

### 7.5 综述反哺主线 (cycle 035)

per cycle 035 (2026-05-15), 综述四轴判断 (六类失败模式 / 长序列内存四类 / 测试时三类 / 输出资产三类) 反哺 Track A Dream3R 主线, 输出 4 markdown deliverables + WORK_RISK_REGISTER 4 新行:

- **SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md (cycle 035 上游 proposal; status: draft awaiting user review)**: 21 子类覆盖矩阵 (✓ 6 first-class / ⚠ 11 partial / ✗ 4 absent); P0/P1/P2 gap 识别; 类型 A/B/C/D 优化建议; W19-W30 roadmap 重排建议
- **SOTA_MATRIX_V2.md (cycle 035 P0-2)**: 五张 Tables A-E 重新标注 SPEC-007 v0.2 19 comparator entries 与 5 axes (失败模式 / 长序列内存 / 测试时 / 输出资产 / 输入扩展 bonus); 4 first-class-support gap (OOD / external prior / 4DGS license / 输入扩展 axis) 反哺 WORK_RISK_REGISTER
- **CRITIC_CALIBRATION_PLAN_V1.md (cycle 035 P0-1)**: 六类失败模式 → C4 Critic 5 sub-signal 映射; method A vs B selection decision tree; 5-metric validation gate (plan-only, 执行 gated)
- **LONG_SEQ_REAL_TABLE_PLAN.md (cycle 035 P0-3)**: 4 ablate_recurrence variants × 4 long-seq metrics × windows ∈ {10, 20, 50, 100} 分级执行; B4 缓存治理 explicit coverage gap; 6-metric validation gate (plan-only, 执行 gated)
- **WORK_RISK_REGISTER.md v1.1 (cycle 035 +4 行)**: R-OOD-1 (域外检测缺口) + R-EXT-PRIOR-1 (外部先验冲突) + R-4DGS-LIC-1 (4DGS license 链) + R-INPUT-EXT-1 (输入扩展 axis)。cycle 036 v1.2 再加 R-PROP-VOCAB-1 / R-PROP-CLAIM-1 / R-PROP-SYNC-1 三 proposal-cycle 行, 共 20 行

cycle 035 4 markdown deliverables 是 Track B → Track A 单向反哺; 综述 manuscript 在 2026-05-14 wound down 后未受到主线后续工作回流污染。

### 7.6 cycle 历史

cycle 015 (2026-05-05) 起 Dream 主线进入架构-first 轨道 (per DEC-20260506-001); cycle 016-021 完成 v0.2 markdown trio (SPEC-004 + SPEC-005 + SPEC-007); cycle 022 paper v1.2 (PAPER_DRAFT_V1.md 含 v0.2 deltas 与 comparator); cycle 023 v0.3 ablation addendum (ABL-v02-10 + VGGT baseline); cycle 024 服务器 v0.2 scaffold; cycle 025-027 C2 Memory v0.3 设计与 P0 plan; cycle 028-031 ablation addendum review + local P0 scaffold + ABL-memory-0 fixture pass; cycle 032 v0.3 codebase 服务器端验证 (synthetic 训练 10 epochs 收敛, 8.4ms p95 profiling, 9/9 smoke tests, 4/4 unit tests, 通过 REVIEW_PROMPT.md onboarding); cycle 033-034 W1-W18 实装完成 + KITTI smoke; cycle 035 综述反哺 4 deliverables; cycle 036-039 开题报告双稿 § 1 + § 2 + § 3 + § 4 + § 6 起草; cycle 040 (本 cycle) § 5 + § 7 + § 8 起草。

cycle 015 Critic L3 pilot scope (DEC-20260505-005 authorized 但 per-step micro gates 仍 required) 在 cycle 016 主线 redirect 后保持 paused at S9 done, 不 abandon — L3 infrastructure (test3r conda env on server + launch.py patch + 4 local shallow clones) 留作 future Critic A4 evidence anchor (per DEC-20260506-001 §S2/D6')。

整体 cycle 历史的 evidence label: cycle 032 服务器端验证 + cycle 034 KITTI smoke 为 code-observed; 其他 cycle 输出 (markdown SPEC / planning / cycle log) 为 engineering-demonstrated 或 paper-derived; 任一 cycle 输出均未 promote 至 paper-proven。

### 7.7 KYKT 平台开发进展 (支柱 B)

KYKT 聚合管理平台 (Coding/4.06/vision_ui) 截至 2026-05-17 的开发进展:

**模型接入与 smoke test**:

| 模型 | 服务器环境 | Runner | Smoke | 备注 |
|---|---|---|---|---|
| DUSt3R | ✓ 环境 + 权重 | ✓ dust3r_runner.py | ✓ 通过 | 静态对 / 多视图 |
| MASt3R | ✓ 环境 + 权重 | ✓ mast3r_runner.py | ✓ 通过 | 静态多图匹配 |
| MonST3R | ✓ 环境 + 权重 + 第三方 | ✓ monst3r_runner.py | ✓ 通过 | 视频/动态重建 |
| Spann3R | ✓ 环境 + 权重 | ✓ spann3r_runner.py | ✓ 通过 | 流式重建 |
| Fast3R | ✓ 环境 + 权重 | ✓ fast3r_runner.py | ○ 前向通过 | 长序列多视图 |
| CUT3R | ✓ 环境 (curope 重建) | ○ 待写 | ○ 待测 | 在线/持久状态 |

**桌面端产品 surface**:

- 命令中心 (focus job + 运行健康 + 快速导航)
- 工作台 (job 列表 / 筛选 / 批量操作 / 键盘导航 / inspector)
- 创建工作区 (模型目录驱动 / 参数路由 / 输入分组)
- 样本矩阵 (samples_manifest.json / 排序 / 筛选 / 报告导出)
- 部署控制台 (远端状态查询 / 模型部署状态)
- AI 顾问 (OpenAI-compatible / 评估 / 建议 / 报告生成)

**关键工程成果**:

- Tauri 2 桌面外壳: 自动管理 FastAPI 后端启动 / 健康检查 / 日志写入
- FastAPI JSON API: /api/bootstrap, /api/jobs, /api/samples, /api/deployment/status, /api/advisor 等完整端点
- SSH/SCP 远端调度: SIGTERM → grace → SIGKILL 的安全取消流 + 孤立任务恢复
- 可移植包装: NSIS / MSI 安装程序 + 单文件 exe; 内嵌 Python 分发方案已设计
- curope CUDA 扩展重建: Align3R + CUT3R 环境均已经解除阻塞 (2026-05-03)

**evidence label**: 平台开发进展全部为 code-observed 或 engineering-demonstrated; DUSt3R / MASt3R / MonST3R / Spann3R 四个 smoke test 产出了实际 job artifact (matches.png / pointcloud.ply / scene.glb 等), 存储在 local_jobs/ 下。

## §8 时间安排

本章按三个时间段给出 Dream3R 后续研究计划: §8.1 短期 (M1-M2, cycle 040-042 开题报告完稿 + 提交 + 启动后续 ABL plan)、§8.2 中期 (M3-M5, W19-W23 真实路由 + W24-W26 v0.4 spec delta + B1/B2/B3 候选)、§8.3 长期 (M6-M8, W27 3DGS renderer + 真实数据训练 + 论文撰写 + 综合评测)。时间表为 candidate timeline, 非 committed schedule, 受 F-002 server authorization + per-step DEC + advisor 反馈影响。

### 8.1 短期 (M1-M2)

短期目标 = 开题报告完稿 + 提交 + 已 plan 的 P0/P1 deliverable 执行入口。

- **cycle 040 (2026-05-17, 已完成)**: § 5 + § 7 + § 8 dual-draft 完稿 (~11000 字); STYLE_CONTRACT 43→48 rows
- **cycle 041 (2026-05-17, 已完成)**: § 9 风险分析 起草 (~1500 字 内 + ~1000 字 外) + 通稿审查 (G3a/G3b/G4 all 0 hits; no § 1-§ 8 surgical edits needed) + STYLE_CONTRACT 48→50 rows final sync
- **cycle 042 (本 cycle, 2026-05-17)**: 最终修订 + PDF 编译 (pandoc + xelatex) + 提交 packaging (复用 cycle 036 Part A pattern)
- **Track B 实际提交动作 (用户 cycle 外人工动作)**: 综述 deliverables/3r_survey_stage_final_2026-05-15_natural.pdf + cover note + SUBMISSION_RECORD slot 填写 (recipient / channel / submitted_at), 与 cycle 040 + 041 + 042 并行可执行

短期 cycle 040-042 evidence label: 全部 markdown-only + plan-level; 不启动 server 行动 / 训练 / checkpoint / 任何 ABL 执行。

### 8.2 中期 (M3-M5)

中期目标 = W19-W26 实装 + B1/B2/B3 v0.4 spec delta 候选 + cycle 035 P0/P1 plan 执行入口。每项 milestone 需独立 DEC + F-002 server authorization。

按 cycle 035 SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §6 W-task reorder 推荐 (recommendation-status, 非 committed):

- **W20 SOTA matrix (P0 已升级, cycle 035 已完成)**: planning/SOTA_MATRIX_V2.md 已 land
- **W24 Critic calibration plan (P0 已升级, cycle 035 已完成 plan)**: 执行 gated; 中期入口
- **W21 ablate_recurrence long-seq table plan (P0 已升级, cycle 035 已完成 plan)**: 执行 gated; 中期入口
- **W19 真实数据路径 (DTU + KITTI loader, real evaluation entry)**: cycle 040 cycle 后第一个 unblocked task (per NEXT_PHASE_ROADMAP); DTU license 链 + multi-view registration loader 是主要工作量
- **W22 visualization pack (NSA weights / AnchorBank occupancy / Critic timeline / state drift curves)**: unblocked (post-demo, medium-high priority); 中期独立 DEC
- **W23 expert routing 真实加载 (CUT3R / MoGe-2 / DepthAnything-V2 真实 adapter; Fast3R omegaconf depfix)**: 中期高优 unblocked; 与 W19 + W22 并行可推进
- **W24 Critic calibration 执行 (cycle 035 plan 升级到 W24 实装)**: F-002 + 独立 DEC; 30 scalar threshold 表 + sub-sample 分组采样的具体执行
- **W25 测试时适应 (TTT3R 风格参数更新路径)**: Gated (post 真实数据); 与 B1 v0.4 spec delta (Critic 路径拆分) 协同
- **W26 输入扩展 axis 设计 (输入扩展 axis: pose / sparse depth / video; 与 Pow3R / MapAnything 路径对接)**: Gated (design first); 与 B3 v0.4 spec delta (输入扩展 axis) 协同

**v0.4 spec delta 候选 (proposal-status; per cycle 035 SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §5)**:

- **B1 Critic 路径拆分**: 把 C4 Critic 一致性优化 vs C2 TTT 参数更新拆为两路径 (per §3.1 Q1); 与 W25 协同
- **B2 输出资产契约**: D1 / D2 / D3 (含 4DGS) 输出资产 explicit contract; 与 W27 协同; 受 R-4DGS-LIC-1 风险约束
- **B3 输入扩展 axis**: 引入 pose / sparse depth / video 作为 first-class 输入接口 (per Pow3R / MapAnything 谱系); 与 W26 协同; 关联 R-INPUT-EXT-1 风险

每 v0.4 spec delta 候选需独立 DEC 起草 (类似 SPEC-008 v0.3 addendum 流程)。

### 8.3 长期 (M6-M8)

长期目标 = W27 4DGS renderer 接入 + 真实数据训练 + 论文撰写 + 综合评测。这一段时间窗 (estimated 6-8 月后) 远 outside 开题报告时间窗口, 时间表 candidate 性更强。

- **W27 4DGS renderer (gsplat / gaussian-splatting 路径)**: 把 W18 GaussianHead tensor 契约接入实际可渲染 4DGS asset; 受 R-4DGS-LIC-1 风险约束 (renderer license 链未文档化); 与 B2 v0.4 spec delta 协同; 独立 DEC + F-002 + license check 三 gate
- **W28 训练基础设施 (checkpoint resume / 确定性 seed / run metadata / config snapshot)**: 真实数据训练的工程支撑; F-002 + 独立 DEC
- **真实数据训练**: 在 W19 (DTU loader) + W21 (long-seq) + W23 (expert 真实加载) + W24 (Critic 标定) + W28 (训练基础设施) 都通过后, 启动 v0.3 端到端真实数据训练; 这是 Q1/Q2/Q3 实证 evaluation 的 prerequisite
- **W29 文档 pack (架构图 / method matrix / ablation 表 / limitations / claim tracking)**: 持续维护, 不单独 milestone
- **论文撰写 (Phase 2)**: PAPER_DRAFT_V1.md v1.2 → v2 升级, 含 ABL-v02-1..10 + ABL-memory-0..11 实证数值, 候选目标会议 (per DEC-20260506-001 paper-as-support; 具体会议 + 篇幅 + scope gated on 用户方向)
- **综合评测**: KITTI / DTU / 可能扩展 ScanNet / 7-Scenes 等; 与 §3 Q1/Q2/Q3 三组研究问题对照; 与 B1/B2/B3 v0.4 spec delta 协同

长期阶段 evidence label 待 Tier 1 + Tier 2 ABL 跑出后才能从 plan-only 升级至 code-observed / engineering-demonstrated; 任何 paper-proven claim 仍需会议接收。

### 8.4 KYKT 平台里程碑 P-1..P-7 (支柱 B)

支柱 B (KYKT 平台) 的开发里程碑嵌入 M1-M8 时间框架:

| 里程碑 | 内容 | 时间段 | 依赖 |
|---|---|---|---|
| P-1 | CUT3R runner 写作 + smoke test | M1-M2 | curope 环境已就绪 |
| P-2 | Align3R runner 写作 + smoke test | M1-M2 | curope 环境已就绪 |
| P-3 | 跨模型对比视图 + 报告导出 | M2-M3 | P-1 + P-2 完成 |
| P-4 | 统一评估框架 v2 (自动指标 + AI 评估升级) | M3-M4 | P-3 对比数据积累 |
| P-5 | Dream3R 作为新模型接入 KYKT 平台 | M5-M6 | Dream3R 训练后检查点可用 |
| P-6 | REST API 封装层 (概念验证) | M6-M7 | P-4 评估框架稳定 |
| P-7 | 平台整体评测报告 (对应 §5.8 指标) | M7-M8 | P-1..P-6 全部完成 |

P-1 / P-2 为短期优先 (环境已就绪, 只需 runner 写作); P-3..P-4 为中期 (依赖对比数据积累); P-5..P-7 为长期 (依赖 Dream3R 架构进展)。所有里程碑为 candidate timeline, 与支柱 A 的 W-task 同样受 per-step DEC + 服务器可用性约束。

整体时间表 candidate-not-final 性 (per DEC-20260501-011): M1-M8 各阶段都可能因为 (a) 服务器算力 / GPU 可用性 (per F-002), (b) 实证结果反馈 (e.g., ABL-v02-4 best-of-N 不显著 → 重新 prioritize Pillar D 路径), (c) v0.4 spec delta 候选选择 (B1 vs B2 vs B3 优先级), (d) advisor 反馈 (开题报告 feedback 可能 reshape M1-M2), (e) Track B 综述提交后是否引发新方向 等因素调整。每次调整在对应 cycle log 记录, 不 silent 改时间表。

---

## §9 研究风险

本章汇总开题阶段识别的主要研究风险, 按架构层 / 跨模块 / 实证执行 / 工程时序 / 平台层 (支柱 B) / 开题报告 process 六个层面分组, 并在 §9.7 给出整体应对策略。风险条目引用 WORK_RISK_REGISTER v1.2 (17 行 per-spec + cross-spec 风险 + cycle 035 v1.1 +4 行 + cycle 036 v1.2 +3 行 + expansion cycle +4 行平台风险 = 24 行总计)。所有缓解措施均为 plan-level 或 partial-mitigated, 没有任何风险在开题阶段被完全消除。

### 9.1 架构层风险

架构层风险来自 WORK_RISK_REGISTER 中各 finalist SPEC 的 per-spec risk 指针:

- **Critic 标定缺口**: C4 Critic 依赖 Sampson / depth / 共视 三路几何信号的阈值配置 (theta_conflict 等); CRITIC_CALIBRATION_PLAN_V1 提出了 method A (分布分位数 P95) 与 method B (监督分类器 + 单调升级门) 两条路径, 但均处于 plan-only 状态, 执行 gated on F-002。阈值未经真实数据标定前, Critic 的 repair action 分派可能偏保守或偏激进, 直接影响 §3 Q1 的实证评估。
- **Memory 校准精度**: C2 Memory v0.3 的 NSA 三分支稀疏注意力 + AnchorBank K=256 + StateToken + Mamba-Transformer 混合循环在 ABL-memory-0 fixture/logging gate 通过 (cycle 031, 集成证据), 但 ABL-memory-1..11 全部 plan-only; Memory 的 long-seq 校准精度 (scale_drift_proxy / memory_decay_proxy / anchor_fill_rate / retrieval_diversity 四指标) 尚未在真实数据 windows ∈ {10, 20, 50, 100} 上验证。
- **Permanence 静态写入覆盖**: C3 Permanence 通过 CR-2 binding 向 Memory 发送 suppress_static_write 信号; Memory 若部分忽略该信号, 动态物体的永久性 link 可能被静态背景覆盖 (per WORK_RISK_REGISTER "Memory honor of Permanence suppress_static_write fails")。缓解依赖 CR-2 logged-refusal rule, 但 refusal 路径在 v0.3 仅 stub 级别。
- **Composer 零 spread fail-fast**: C5 Composer 的 7-expert pool 依赖 capability_match (spread) 作为路由信号; 当所有 expert 在某 failure mode 下的 spread → 0, Composer 触发 fail_fast (per SPEC-20260504-001 fail_fast_threshold); 这一退化场景在开题阶段仅有文档级缓解 (retire-to-support 路径记录在 WORK_RISK_REGISTER), 未经实证触发。
- **信号契约漂移**: C6 Bus 的 CR-1..CR-6 cross-spec 信号契约 v2.1 在 v0.3 下未经全路径端到端验证; 任何 case card 对同一信号的语义理解偏差可能导致契约漂移 (per WORK_RISK_REGISTER "Cross-spec signal contract drift")。

### 9.2 跨模块风险

跨模块风险在 cycle 035 综述反哺后浮出, 记录为 WORK_RISK_REGISTER v1.1 +4 行:

- **R-OOD-1 域外检测缺口**: C4 Critic 当前不含显式域外检测路径; 训练分布外 (indoor + urban KITTI/ScanNet 之外) 的窗口可能 silently 通过 Critic acceptance, 使 Composer 路由到错误 expert。缓解: CRITIC_CALIBRATION_PLAN_V1 A6 mode (plan-only); 不可 promote 为 v0.4 finalist without 独立 DEC (per DEC-20260504-002)。
- **R-EXT-PRIOR-1 外部先验冲突**: 未来 C5 Composer prior-adapter (Depth Pro / Metric3Dv2 / SAM2 / CoTracker 等) 可能输出与 C2 Memory pointmap 或 C4 Critic conflict_score 矛盾的先验; CR-1..CR-6 v2.1 无 resolution priority 定义。缓解: v0.4 spec delta B3 (输入扩展 axis) 可引入 CR-7 candidate external_prior_conflict v2.2, 但需独立 DEC + contract version bump。
- **R-4DGS-LIC-1 4DGS 许可链**: W18 GaussianHead tensor 契约仅定义张量输出格式, 不含 license metadata; W27 renderer (gsplat / gaussian-splatting 路径) 接入时可能继承 viral / restricted license 的 Gaussian splatting 库。缓解: W27 保持 gated (per NEXT_PHASE_ROADMAP); 实际接入需 per-renderer license review DEC + 用户 gate。
- **R-INPUT-EXT-1 输入扩展 axis 空缺**: Dream3R v0.3 仅接受 images + sequence 作为输入; Pow3R / MapAnything / MASt3R-SfM 等系统已支持 pose / sparse depth / video timestamp 作为 first-class 输入, 形成 benchmark 准入门槛。缓解: v0.4 spec delta B3 (input_priors tensor channel) 为候选方案; 实装需独立 DEC + C1 + C5 + CR contract 三方联动。

### 9.3 实证执行风险

- **集成证据 vs 训练后质量边界**: §7.3 报告的 KITTI pointmap L2 = 20.4747 是集成证据 (integration evidence), 非训练后重建质量; 数值本身不应被读作 SOTA-comparable。风险: 导师或外部 reviewer 可能将该数值解读为训练后精度。缓解: §7.3 + §5.1 双处 caveat 显式并置; 后续 C2 quality 需要端到端训练 (W19-W28 gated)。
- **ABL 计划 plan-only 边界**: §5.2 ABL-v02-1..10 + §5.3 ABL-memory-0..11 + §5.4 Critic 标定 + §5.5 长序列评测 均为 plan-only, 执行 gated on F-002 server authorization。风险: 评测协议章节的表格化呈现可能给读者 "已跑" 的视觉暗示。缓解: 每子节末尾重复 "plan-only; 执行 gated" caveat。
- **数据集 license**: KITTI 主 (CC BY-NC-SA 3.0) 允许学术用途; DTU 拟扩展需确认 license 兼容; 合成 fixture 自建无 license 问题。

### 9.4 工程时序风险

- **W19-W30 时间表候选性**: §8 M3-M8 timeline 是 candidate schedule, 不是 committed schedule; 各 W-task 需独立 DEC + F-002 server authorization, 实际推进节奏受 GPU 可用性 / 实证反馈 / 导师意见三重约束。
- **v0.4 spec delta 候选优先级**: B1 (Critic 路径拆分) / B2 (输出资产契约) / B3 (输入扩展 axis) 三项 v0.4 spec delta 均为 proposal-status, 不是 locked architecture; 优先级选择 (B1 vs B2 vs B3) 取决于 M3-M5 实证反馈, 开题阶段不可 pre-commit。
- **3DGS renderer license**: W27 4DGS renderer 接入时序依赖 R-4DGS-LIC-1 清除 + B2 spec delta landing; 长期目标 M6-M8 的 4DGS asset 输出功能路径最长, 风险最集中。

### 9.5 平台层风险 (支柱 B)

支柱 B (KYKT 聚合管理平台) 的特有风险:

- **R-PLAT-ENV-1 多模型环境冲突**: 6 个 3R 模型各自依赖不同的 Python 环境 / CUDA 版本 / 第三方库; 服务器端 conda 环境隔离可避免直接冲突, 但磁盘空间 / 共享 CUDA driver 版本约束仍可能导致特定模型运行失败 (如 CUT3R 依赖 curope CUDA 扩展重建)。缓解: per-model conda env + curope 重建脆本已有 (2026-05-03); 残余风险: 未来新模型可能引入新 CUDA 版本要求
- **R-PLAT-SERVER-1 服务器可用性**: KYKT 平台的远端执行依赖 GPU 服务器 SSH 可达性; 校园网 / VPN 断连、服务器维护、GPU 占用等均可能导致 job 执行失败。缓解: 孤立任务恢复机制 (orphan recovery) + SSH 重连 + SIGTERM/grace/SIGKILL 安全取消流已实现; 残余风险: 多服务器负载均衡未实现 (when 可用)
- **R-PLAT-TAURI-1 Tauri 兼容性**: Tauri 2 桌面外壳依赖系统 WebView2 (Windows) / WebKit (macOS/Linux); 不同操作系统版本的 WebView 行为差异可能影响前端渲染。缓解: 当前主要针对 Windows 开发测试, 跨平台支持作为后续目标; 残余风险: macOS/Linux 兼容性未验证
- **R-PLAT-API-1 API 安全性**: REST API 封装层 (§4-B.4 概念设计) 将模型推理能力暴露为 HTTP 接口; 在校园网内网环境下安全风险可控, 但若扩展至公网环境需追加认证 / 限流 / 访问控制。缓解: 本阶段 API 仅概念设计, 不实装; 实装时需安全审查 DEC

### 9.6 开题报告 process 风险

cycle 036 v1.2 新增 3 行 proposal-cycle 风险:

- **R-PROP-VOCAB-1 vocab 泄漏**: 外部稿 grep 在每 cycle close 时验证 Dream-vocabulary 零泄漏; cycle 036-040 共 surface 10+ hits, 均通过 corrective edits 清除。残余风险: 通稿审查可能在 §1-§8 已关闭章节中 surface 此前未检测的边缘情况 (e.g., 信号名英文 + 上下文暗示内部编号)。
- **R-PROP-CLAIM-1 over-claim**: 候选架构 X 的 candidate-not-final 定位 (per DEC-20260501-011) 要求所有 claim 句式避免 over-claim 表述 (宣称优越性 / 宣称为最终设计 等); cycle 039 G4 surface 7 hits/side 在 negation-context 句式中, 通过 corrective rephrasing 清除。残余风险: §9 风险描述中 mitigation 措辞可能 inadvertently 暗示风险已完全解决。
- **R-PROP-SYNC-1 双稿语义漂移**: internal-is-master + 周期性 external 快照规则 (STYLE_CONTRACT §3) 保证双稿语义一致; 但随 §1-§9 全部落地, 累计 ~19000 内 + ~15000 外 字的大规模双稿可能在 §X 间交叉引用点产生微漂移。通稿审查 (本 cycle) 是最终同步窗口。

### 9.7 风险应对策略

本研究采用 "层级化缓解 + 残余风险显式声明" 的整体应对策略:

| 优先级 | 风险层面 | 核心缓解路径 | 残余风险 |
|---|---|---|---|
| P0 | 实证执行 | F-002 server gate + plan-only caveat + 集成证据 vs 质量 caveat | ABL 全部未跑; 训练后质量未知 |
| P0 | over-claim | STYLE_CONTRACT §5 句式表 + per-cycle G4 grep | negation-context 边缘情况 |
| P1 | 跨模块 (R-OOD-1 / R-EXT-PRIOR-1) | CRITIC_CALIBRATION_PLAN_V1 A6 + v0.4 B3 spec delta 候选 | 均为 plan-only; 执行需独立 DEC |
| P1 | 4DGS license (R-4DGS-LIC-1) | W27 gated + per-renderer license review | renderer 选型未定 |
| P2 | 架构层 per-spec | fixture/logging gate + CR logged-refusal + fail_fast threshold | 真实数据端到端验证待 W19+ |
| P2 | 工程时序 | candidate timeline + 独立 DEC per W-task | GPU 可用性 / 导师反馈 不可控 |
| P2 | vocab 泄漏 / 双稿漂移 | STYLE_CONTRACT §2 替换表 48+ 行 + §3 sync rule + per-cycle grep | 边缘情况累积 |
| P2 | 平台层 (支柱 B) | per-model conda env + orphan recovery + Tauri Windows 主测 + API 概念设计不实装 | 多服务器、跨平台、公网 API 均未验证 |

**整体判断**: 所有已识别风险均有 plan-level 或 partial 缓解路径, 但无一风险在开题阶段被完全消除。这一状态与 candidate-not-final 研究定位 (per DEC-20260501-011) 一致 — Dream3R 是被评估的候选架构, 其风险是研究对象的一部分, 而非需要在开题前清除的工程障碍。后续 cycle 042+ 的每一步推进都将缩小特定风险的残余窗口, 但新风险也可能随实证数据浮出。

---

## 元数据

| 字段 | 取值 |
|---|---|
| 文件路径 | `Dream/planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` |
| 创建日期 | 2026-05-16 |
| 状态 | v1.1 draft; §1-§9 + 支柱 B KYKT 平台内容扩展完成; expansion cycle |
| 作者 | Dream agent (cycle 036-042) |
| 上游决策 | DEC-20260516-001 (cycle 036) → DEC-20260517-003 (cycle 042) |
| 双稿关系 | master per STYLE_CONTRACT §3 规则 1 |
| 当前字数 | §1-§9 累计正文 ~27000 字 (含支柱 B 扩展 ~7700 字; ≈ 93% of OUTLINE §2 内稿估算 ~29400 字) |
| 起草历史 | cycle 036 §1 → 037 §2 → 038 §4 → 039 §3+§6 → 040 §5+§7+§8 → 041 §9+通稿审查 → 042 最终修订 → expansion cycle 双支柱扩展 |
| Sync log | 见 STYLE_CONTRACT.md §6 (append-only; cycle 036-042 全部条目) |
