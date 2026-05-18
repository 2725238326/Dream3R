# Dream3R 开题报告双稿 Outline V1

| 字段 | 取值 |
|---|---|
| 文件类型 | planning artifact (9-section dual outline + chapter mapping + 字数估算 + cycle 037+ 起草顺序) |
| 创建日期 | 2026-05-16 |
| 状态 | v1.1 (cycle 036 启动 → cycle 042 close → expansion cycle: 双支柱扩展, 增加支柱 B KYKT 平台内容) |
| 授权根 | DEC-20260516-001 (cycle 036 launch) |
| 上游 | Dream/3R-mix/main.tex 综述 §1-§10 + Dream/planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md + Dream/planning/SOTA_MATRIX_V2.md + Dream/specs/SPEC-* + Dream/decisions/DEC-* + Dream/code/dream3r/RECENT_PROGRESS.md |
| 触及范围 | 仅本文件; 不动 spec / code / paradigm |

## 1. 双稿基本约定 (per STYLE_CONTRACT.md)

| 维度 | 内部稿 DRAFT_INTERNAL_V1.md | 外部稿 DRAFT_EXTERNAL_V1.md |
|---|---|---|
| 受众 | 项目内部审计 / 后续 cycle 回溯 | 导师 / 学院 / 论文评审 / 外部 reviewer |
| 词汇 | 含 Dream / Dream3R / cycle / SPEC / DEC / CR / W-task / agent 等 | 完全剥离上述词汇 |
| 系统命名 | Dream3R | 候选架构 X / 本研究架构 |
| 引用方式 | 直接 SPEC ID / DEC ID / cycle ID / 服务器 path | 学术化中文命名 + 模糊化 ID |
| 篇幅比例 | 比外部稿长 ~30% (带技术细节 + 工件引用) | ~10-25 页 A4 中文 |
| 风格 | 工程报告风格 | 学术开题报告风格 |
| 正式度 | 中等正式 (项目内部沟通) | 比导师 1-on-1 design doc 稍正式; 比院系开题答辩松 |

## 2. 9-section 大纲对照 (1:1 章节镜像)

| § | 外部稿章节 (vocab-clean) | 内部稿章节 (Dream-vocab) | 外稿字数 | 内稿字数 | 起草所需上游 |
|---|---|---|---|---|---|
| 1 | 研究背景与问题 | 项目背景与研究问题 | ~1800 | ~2500 | 综述 §1 + DEC-20260506-001 + 综述 §10 失败模式 + **支柱 B: 模型多样化带来的管理挑战 → 统一平台必要性** |
| 2 | 国内外研究现状 | 比较谱系与现状 | ~4500 | ~5200 | 综述 §2-§9 全章 + SOTA_MATRIX_V2 + SPEC-20260507-001 v0.2 + references.bib 44 entries + **支柱 B: §2.8 现有 3R 工具链与平台综述** |
| 3 | 研究问题与目标 | 候选研究问题 | ~2100 | ~2600 | DEC-20260501-011 + DEC-20260504-002 + 综述 §10 + **支柱 B: Q4 统一聚合管理与评估平台** |
| 4 | 研究方案 (§4-A 架构 + §4-B 平台) | Dream3R v0.3 架构 + KYKT 平台架构 | ~5500 | ~7000 | SPEC-20260506-004 v0.2 + SPEC-20260508-001 v0.3 + CROSS_SPEC_SIGNAL_CONTRACT v2.1 + COMPOSER_CAPABILITY_DESCRIPTORS + **支柱 B: KYKT.md + PROJECT_PROGRESS + vision_ui/README** |
| 5 | 实验设计与评测协议 | 消融与评测设计 | ~2600 | ~3400 | SPEC-20260506-005 v0.2 ABL-v02-1..9 + SPEC-20260507-002 v0.3 + SPEC-20260508-002 ABL-memory-0..11 + CRITIC_CALIBRATION_PLAN_V1 + LONG_SEQ_REAL_TABLE_PLAN + **支柱 B: 平台层评测标准** |
| 6 | 预期成果与创新点 | 预期成果 | ~1400 | ~1800 | DEC-20260501-011 candidate-not-final + DEC-20260504-002 no-all-in + **支柱 B: IP4 统一聚合管理平台** |
| 7 | 研究进展与已完成工作 | 已完成工作 | ~2500 | ~3200 | code/dream3r/RECENT_PROGRESS.md W1-W18 + KITTI smoke L2=20.47 + 综述 deliverable + cycle 033/034/035 deliverables + **支柱 B: KYKT 平台开发进展** |
| 8 | 研究计划与时间安排 | 时间安排 | ~1300 | ~1900 | code/dream3r/NEXT_PHASE_ROADMAP.md W19-W27 + 综述驱动优化提案 §6 重排 + **支柱 B: P-1..P-7 平台里程碑** |
| 9 | 风险分析与应对 | 研究风险 | ~1300 | ~1800 | WORK_RISK_REGISTER v1.2 17 rows + 3 new rows (cycle 036) + **支柱 B: 平台层风险** |
| **总计** | | | **~23000** | **~29400** | |

外部稿估算 24-28 页 A4 中文 (含 4-6 图 + 3-5 表)。内部稿因每节追加 "Dream 项目工件引用" 子块比外部稿长 ~28%。落在用户指定 "10-30 页中等篇幅" 区间, 偏上位。

### 2.1 支柱 B (KYKT 平台) 各章新增子节映射

| § | 支柱 B 新增内容 | 预估新增字数 (外稿) |
|---|---|---|
| 1 | 模型多样化带来的工程管理挑战 → 统一平台必要性 → 研究闭环 | +300 |
| 2 | §2.8 现有 3R 工具链与平台综述 (Nerfstudio / Polycam / Luma AI / 官方 demo 孤岛现状 → gap) | +1000 |
| 3 | Q4: 如何设计面向多模型 3R 研究的统一聚合管理与评估平台 (子问题 + 与 Q1-Q3 关系) | +600 |
| 4 | §4-B 独立节: KYKT 平台架构设计 (总体架构 / 模型注册与执行合同 / 统一评估框架 / 应用对接层 / 与 Dream3R 协同) | +2500 |
| 5 | 平台层评测标准 (新模型接入耗时 / 统一合同覆盖率 / 跨模型对比矩阵 / API 对接能力) | +600 |
| 6 | IP4: 面向前馌式 3R 的统一聚合管理平台 (工程创新点 + 与 IP1-IP3 关系) | +400 |
| 7 | KYKT 平台开发进展 (6 模型接入 / 4 smoke / 桌面端 / AI 评估 / 远端部署) | +1000 |
| 8 | P-1..P-7 平台里程碑嵌入 M1-M8 | +300 |
| 9 | 平台层风险 (多模型 env 冲突 / 服务器可用性 / Tauri 兼容性 / API 安全性) | +300 |
| **总计** | | **+7000** |

## 3. 章节映射表 (外稿 ↔ 内稿 ↔ 复用素材)

下表标注每个 § 的素材来源 (复用 = 双稿共享; 外稿独占 / 内稿独占 = 该稿特有):

| 外稿 § | 内稿 § | 复用素材 (双稿共享) | 外稿独占 | 内稿独占 |
|---|---|---|---|---|
| §1 | §1 | 综述 §1 引言 + §10 六类失败模式 (现象层) | "候选架构 X" 措辞 + 学术化研究背景叙事 | Dream3R 命名 + DEC-20260506-001 引用 + Track A 起源时间线 + cycle 035 反哺关系 |
| §2 | §2 | 综述 §2-§9 全章 + tab:foundation / tab:dynamic / tab:memory / tab:testtime / tab:application 五张表 + fig:paradigm / fig:lineage / fig:timeline / fig:memory 四图 + references.bib 44 entries | 学术化国内外研究现状叙事; 五子节 (基础谱系 / 多视角 / 视频动态 / 长序列内存 / 测试时机制) | SOTA_MATRIX_V2 直接表格引用 + SPEC-20260507-001 v0.2 Tier 1-5 ID + Axis 9-11 + 综述驱动优化提案 §3 覆盖矩阵 |
| §3 | §3 | 综述 §10 失败模式 + 综述 §6 长序列内存四类 + 综述 §7 测试时三类 | 三个核心研究问题学术化表述 (验证机制 / 长序列内存 / 多专家组合) + candidate-not-final 学术语言 | DEC-20260501-011 + DEC-20260504-002 直接引用 + Track A finalist 框架 (Critic / Memory / Permanence / Composer 四模块) |
| §4 | §4 | 综述 §6-§8 机制分类 + 综述 §10 失败模式 | 六模块学术化命名 (感知 / 记忆 / 永久性 / 校验 / 编排 / 总线) + 模块间信号契约高层描述 (信号校验规则族) + 与现有 3R 系统的结构差异 | C1-C6 编号 + SPEC-20260506-004 v0.2 六 Delta + SPEC-20260508-001 v0.3 C2 NSA 三分支 + AnchorBank K=256 + StateToken + CR-1..CR-6 信号编号 + COMPOSER_CAPABILITY_DESCRIPTORS 7 expert 池 + DINOV3_C1_INTEGRATION_MEMO + NSA_MEMORY_INTEGRATION_MEMO |
| §5 | §5 | 综述 §9 四类证据 + 综述 §10 失败模式 (用于消融子样本规则) | 学术化评测协议 + 三层证据阶梯 (综述层 / 代理用例层 / 原型实现层) + 评测数据集 (KITTI / DTU 等) + 消融实验高层描述 | SPEC-20260506-005 v0.2 ABL-v02-1..9 ID + SPEC-20260507-002 v0.3 ablation addendum + SPEC-20260508-002 ABL-memory-0..11 + CRITIC_CALIBRATION_PLAN_V1 5-metric validation gate + LONG_SEQ_REAL_TABLE_PLAN 4 度量 + ablate_recurrence 4 variants |
| §6 | §6 | DEC-20260501-011 candidate-not-final motivation | "评估候选架构 X 是否..." 学术句式 + 创新点声明 (架构层失败模式响应 / 长序列内存机制统一 / 多专家组合 best practice 评估) | DEC-20260501-011 + DEC-20260504-002 直接引用 + Dream3R 命名 |
| §7 | §7 | 综述 deliverable (路线 C wound-down 状态) | 学术化"实现里程碑 1-18" + KITTI smoke 集成证据 + 综述发布事实 | W1-W18 编号 + cycle 033 / 034 / 035 ID + 服务器 path /hdd3/kykt26/code/dream3r/ + KITTI 真实 smoke L2=20.47 数值 + cycle 035 4 个 deliverables + ablate_recurrence.py / evaluate_real_sequence.py 文件名 |
| §8 | §8 | 综述驱动优化提案 §6 W19-W30 重排 | 学术化阶段安排 (M1-M8 三阶段: 候选架构完善 / 原型推进 / 论文撰写) | W19-W27 NEXT_PHASE_ROADMAP 编号 + B1/B2/B3 v0.4 spec delta 候选 + SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §6 重排建议 + cycle 037-042 起草顺序自指 |
| §9 | §9 | WORK_RISK_REGISTER 17 rows (含 cycle 035 +4 + cycle 036 +3) | 4-6 条精选学术化风险 (域外检测缺口 / 外部先验冲突 / 4DGS 许可链 / 算力约束 / 评测成本 / 候选架构被替换的可能) | R-XXX-N 编号 + 全 20 行 (含 R-OOD-1 / R-EXT-PRIOR-1 / R-4DGS-LIC-1 / R-INPUT-EXT-1 / R-PROP-VOCAB-1 / R-PROP-CLAIM-1 / R-PROP-SYNC-1 等) + 风险登记跨 spec 的元结构 |

## 4. cycle 037+ 起草顺序建议

下表给出 cycle 037-042 的逐 cycle 起草目标。每 cycle 完成 1-2 个 § 的双稿同步起草 + STYLE_CONTRACT §6 sync log 追加。

| Cycle | 起草目标 | 优先级理由 | 预期 cycle 字数 |
|---|---|---|---|
| 037 | §2 国内外研究现状 (双稿同步起草) | 最大单一章节 (~3500 外 + ~4000 内 = ~7500 字); 最依赖综述复用; 双稿同步起草最能 stress-test STYLE_CONTRACT vocab 替换表 | ~8000 (含 sync log) |
| 038 | §4 研究方案 (双稿同步起草) | 核心技术章节; 中等大 (~3000 外 + ~4000 内 = ~7000 字); 决定六模块学术化命名的最终方案 | ~7500 |
| 039 | §3 研究问题与目标 + §6 预期成果与创新点 | 两章 framing 一起做, 因为问题表述与成果声明高度耦合 | ~5500 |
| 040 | §5 实验设计 + §7 已完成工作 + §8 时间安排 | 三章实证 framing 一起做; §5 + §7 + §8 都需要消化 W-task 系列素材 | ~7000 |
| 041 | §9 风险分析 + 通稿审查 + STYLE_CONTRACT sync | §9 最后写 (汇总所有前章风险); 通稿审查 = 双稿一致性 grep + 句式审查 | ~3500 |
| 042 | 最终修订 + PDF 编译 + 提交 packaging | 复用 cycle 036 Part A pattern: 编 PDF + 写 SUBMISSION_PACKAGE_ADVISOR + SUBMISSION_RECORD; 准备外发 | ~2000 |

**总计 cycle 037-042 + expansion cycle**: 约 7 个 cycle, ~42000 字新增 (外稿 ~23000 + 内稿 ~29400 + sync log + 修订 + 重复) → 落地 ~25 页 A4 外部稿。

**关键 cycle 037 决策点**: §2 起草过程中可能发现章节结构需要调整。如果发现, cycle 037 close 时 OUTLINE_V1 升级为 OUTLINE_V2, 反映新章节结构 (保留 V1 不动, 历史留档)。

## 5. §1 第一段风格样本 (200 字双稿对照)

为锁定语言风格, 在 DRAFT_INTERNAL_V1.md / DRAFT_EXTERNAL_V1.md §1 中各起草约 1000 字完整正文 (作为对齐样本)。下面是 §1 第一段的双稿对照 (仅 200 字, 完整 §1 见 DRAFT_*_V1.md):

### 外部稿 §1 第一段样本 (vocab-clean):

> 前馈式三维重建 (feed-forward 3D reconstruction, 简称 3R) 作为 DUSt3R 谱系延伸的研究方向, 近三年在跨视图几何回归 / 长序列状态管理 / 多专家组合等子方向上呈现快速演化。然而, 现有工作在弱纹理 / 镜面玻璃 / 快速运动 / 长基线 / 尺度漂移 / 域外六类典型几何失败模式下的置信度衰减仍未系统解决, 长序列累积误差与外部先验注入机制亦缺乏统一架构性回应。本研究面向这一问题, 提出并评估一个代号为 "候选架构 X" (Candidate Architecture X) 的前馈式 3R 架构. 为简洁计, 以下正文均以 "候选架构 X" 或 "本研究架构" 指代该架构。

### 内部稿 §1 第一段样本 (Dream-vocab):

> Dream3R 是 Track A 主线 (per DEC-20260506-001 architecture-first 决策, 2026-05-06 user-locked) 提出的前馈式 3R 架构, 当前处于 v0.3 server-verified 状态 (per cycle 034 KITTI real-data smoke 2 windows + W1-W18 实装完成)。Track B 3R-mix 中文综述 (路线 C, 2026-05-14 wound down, 18 A4 页 44 引文) 识别了四轴判断 (六类失败模式 / 长序列内存四类 / 测试时三类 / 输出资产三类), 并通过 cycle 035 反哺 Track A 主线 (planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md + SOTA_MATRIX_V2 + CRITIC_CALIBRATION_PLAN_V1 + LONG_SEQ_REAL_TABLE_PLAN 4 个 deliverables + WORK_RISK_REGISTER +4 cross-spec 风险)。Dream3R v0.3 通过 C1 Perceiver (DINOv3-S frozen backbone) + C2 Memory (NSA three-branch + AnchorBank K=256 + StateToken + Mamba hybrid) + C3 Permanence (Slot Attention + permanence_link) + C4 Critic (Sampson / depth / 共视 conflict + repair actions 0/1/2) + C5 Composer (7 expert pool: MASt3R / Fast3R / Spann3R / CUT3R / MoGe-2 / DepthAnything-V2 / Test3R) + C6 Bus (CR-1..CR-6 cross-spec signal contract v2.1) 六模块响应综述四轴判断。

观察: 内部稿同一段落约 320 字, 外部稿约 200 字。内部稿密度更高, 因含 ID 与编号; 外部稿清爽, 因学术化通用语言。这与 §1 总字数估算 (~2000 内 vs ~1500 外) 比例一致。

## 6. 起草前的检查清单

cycle 037+ 起草任何一章前, 务必复核:

- [ ] STYLE_CONTRACT.md §2 vocab 替换表是否覆盖本章所有内部术语 (没有则在 §6 sync log 中追加新条目)
- [ ] STYLE_CONTRACT.md §5 candidate-not-final 句式表是否覆盖本章可能 over-claim 的位置
- [ ] 上游素材 (综述 § / SPEC / DEC / cycle log) 是否最新 (避免引用过期版本)
- [ ] 双稿同步顺序: 内部稿先, 外部稿后 (per STYLE_CONTRACT §3 规则 1)
- [ ] 章节字数估算与 §2 表是否一致 (允许 ±20% 偏差)
- [ ] vocab 防火墙 grep 验证: DRAFT_EXTERNAL_V1.md §X 起草完成后立即 grep verify
- [ ] cycle log 中追加本章起草记录 (含本 cycle 字数 + sync log 条目)

## 7. 不在本 outline 范围内的事项

本 outline **不** 规定:

- 具体术语翻译 (留给 STYLE_CONTRACT.md §2 替换表 + cycle 037+ 扩充)
- 具体引文管理与 references.bib 结构 (留给 cycle 037 §2 起草)
- 具体 figure / table 生成或复用 (留给 cycle 037+; 可能复用 Track B TikZ 源)
- 提交格式 (PDF / Word / LaTeX 模板) — cycle 042 决定
- 实际提交动作 (邮件 / 当面交付) — cycle 042 之后由用户执行

## 8. 元数据与上游链接

| 字段 | 取值 |
|---|---|
| 文件路径 | `Dream/planning/proposal_dream3r/OUTLINE_V1.md` |
| 创建日期 | 2026-05-16 |
| 状态 | v1.1 (cycle 036 启动 → expansion cycle 双支柱扩展) |
| 作者 | Dream agent (cycle 036) |
| 上游决策 | DEC-20260516-001 (cycle 036 launch) |
| 同级文件 | STYLE_CONTRACT.md (语言契约) + DRAFT_INTERNAL_V1.md (内部稿) + DRAFT_EXTERNAL_V1.md (外部稿) |
| 上游素材引用 (不修改) | `Dream/3R-mix/main.tex` + 综述 §1-§10 + 5 tables + 6 figures + references.bib 44 entries / `Dream/planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md` + SOTA_MATRIX_V2 + CRITIC_CALIBRATION_PLAN_V1 + LONG_SEQ_REAL_TABLE_PLAN + WORK_RISK_REGISTER / `Dream/specs/SPEC-20260506-004 v0.2` + SPEC-005 v0.2 + SPEC-007 v0.2 + SPEC-008 v0.3 + SPEC-009 + SPEC-010 / `Dream/decisions/DEC-20260506-001` + DEC-20260504-002 + DEC-20260501-011 + DEC-20260503-001 + DEC-20260515-001 / `Dream/paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v2.1 / `Dream/code/dream3r/RECENT_PROGRESS.md` + NEXT_PHASE_ROADMAP.md |
| 下游 | cycle 037-042 逐章起草; cycle 037 close 时如章节结构有调整, 升级为 OUTLINE_V2 (保留 V1 不动) |

---

**End of outline v1.** 本文件是 cycle 036 P0-B 子任务 deliverable; cycle 037+ 按 §4 起草顺序逐章推进。
