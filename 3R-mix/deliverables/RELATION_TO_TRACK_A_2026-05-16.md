# 综述与 Dream3R 主线的关系（内部留档）

| 字段 | 取值 |
|---|---|
| 文件类型 | 内部留档 / 不与 PDF 同包提交 |
| 创建日期 | 2026-05-16 |
| 授权根 | DEC-20260516-001 (cycle 036 launch) |
| 触及范围 | 仅本文件;不动 Dream/3R-mix/main.tex / references.bib / notes/ |
| 词汇例外 | 本文件是 cycle 036 期间允许同时含 Track B 综述外发用词与 Dream/Track A 内部词汇的唯一文件 |

## 1. 为什么单独建立这个文件

Track B 3R-mix 综述于 2026-05-14 按 route C (arXiv-only) 收口时, manuscript 表面 (`main.tex` / `references.bib` / `notes/*`) 严格隔离了以下词汇:

```text
Dream / Dream3R / KYKT / agent / skill / workflow / 本地项目 / cycle / SPEC- / DEC- / CR-
```

`Dream/3R-mix/deliverables/SUBMISSION_PACKAGE_ADVISOR_2026-05-16.md` cover note 沿用同样的词汇防火墙 (per DEC-20260516-001 §G2 stop gate)。

但是综述与 Dream3R 主线之间存在真实的工程关系, 这个关系需要在某处记录, 以便:

- 未来 cycle 回溯综述判断如何反哺主线时有审计锚点
- 如果导师询问综述与本人主线研究的关系, 作者本人有清晰准备
- 不污染外发 cover note 的词汇防火墙

因此本文件作为独立留档存在, 不与 PDF 同包提交。

## 2. 关键时间线

| 日期 | 事件 |
|---|---|
| 2026-05-06 | DEC-20260506-001 user-locked: 主线研究方向 = architecture-first (设计新 3R 架构); 论文写作降为 support |
| 2026-05-06 ~ 2026-05-11 | Dream3R v0.3 主线 server-verified 至 cycle 034 (W1-W18 + KITTI smoke 2 windows) |
| 2026-05-11 | Track B 3R-mix 综述工作 kickoff (cycle 034 §Track B), 与主线并行 |
| 2026-05-13 | 综述 refined deliverable (16 页, 2026-05-13_refined.pdf) |
| 2026-05-14 | 综述按 route C (arXiv-only) wound down; manuscript 词汇隔离 grep-verified clean |
| 2026-05-15 | 综述 prose naturalization pass (10 段重写, 18 页, 2026-05-15_natural.pdf) — 当前推荐 deliverable |
| 2026-05-15 | cycle 035 close: 综述四轴判断反哺主线 (planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md + SOTA_MATRIX_V2.md + CRITIC_CALIBRATION_PLAN_V1.md + LONG_SEQ_REAL_TABLE_PLAN.md + WORK_RISK_REGISTER v1.1 +4 行) |
| 2026-05-16 | cycle 036: 综述提交 packaging + 主线开题报告双稿启动 (本 cycle) |

## 3. 综述与主线的关系（三点说明）

### 3.1 综述是主线的姊妹工件, 不是主线的子产品

综述 manuscript (`Dream/3R-mix/main.tex`) 的内容、章节结构、引文选择都不是为了支持 Dream3R 主线论点而设计的。综述按独立的学术综述标准撰写: 对 3R 研究方向作系统综合, 不预设某一架构是 "正确" 的。

这一独立性是综述 wound down 到 route C arXiv-only 的前提: 综述应作为独立工作发布, 而不是作为 Dream3R 论文的附录或引用支撑。

### 3.2 综述的判断已通过 cycle 035 反哺主线, 但反哺方向是单向的

cycle 035 (2026-05-15) 把综述识别的四轴判断 (六类失败模式 / 长序列内存四类 / 测试时三类 / 输出资产三类 + 隐含的输入扩展轴) 映射到 Dream3R v0.3 架构上, 输出 4 个 markdown deliverables:

- `Dream/planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md` (proposal, draft status)
- `Dream/planning/SOTA_MATRIX_V2.md` (re-label SPEC-007 v0.2 against survey four-axis)
- `Dream/planning/CRITIC_CALIBRATION_PLAN_V1.md` (per-failure-mode threshold plan)
- `Dream/planning/LONG_SEQ_REAL_TABLE_PLAN.md` (ablate_recurrence KITTI long-window plan)
- `Dream/planning/WORK_RISK_REGISTER.md` v1.1 (+4 rows: OOD / 外部 prior / 4DGS license / 输入扩展 axis)

反哺方向是单向: 综述 → Dream3R 主线; 不是 Dream3R 主线 → 综述。综述本身在 2026-05-14 wound down 之后没有再修改, manuscript 内容没有受到主线后续工作的回流污染。

### 3.3 综述与开题报告共享 references.bib, 但不互相引用

综述的 44 篇 references 是 3R 研究方向的标准引文池。Dream3R 开题报告 (cycle 036 起草中) 在 §2 国内外研究现状会复用同一组引文, 但开题报告与综述不互相引用 (sibling artifacts):

- 综述不引用开题报告 (综述发布在前, 且开题报告尚未发布)
- 开题报告不引用综述 PDF (两者并行交付给同一导师, 不需要引用嵌套; 复用引文池即可)
- references.bib 的具体条目可以从综述工作目录复制到开题报告工作目录, 这不构成引用关系

## 4. 提交时的口头说明建议（如果导师问起）

如果导师在审阅综述时询问 "你的主线研究方向是什么 / 综述与你的论文工作什么关系", 建议口头回答:

> 综述是我对 3R 研究方向做的独立系统化梳理, 按 arXiv 自存档发布, 不投会议或期刊。我自己的主线研究是设计一个候选的 3R 架构 (称作候选架构 X), 用综述的失败模式分类作为镜子检视这个架构的覆盖与空缺。开题报告会单独提交, 不和这份综述合并。

口头说明不需要提及 Dream / Dream3R / cycle / DEC / SPEC 等内部 workflow 术语。

## 5. 不外发声明

本文件 **不与 PDF 同包提交给导师 / 学校**。理由:

- 本文件含 Dream / Dream3R / cycle / SPEC- / DEC- / CR- 等内部 workflow 词汇, 违反综述外发的词汇防火墙
- 本文件是元层留档 (meta-level audit), 不是外发的学术材料
- 导师对综述本身的评审不需要了解主线研究的内部 workflow 细节

如果未来需要把综述与主线研究的关系写入外发材料, 必须重新用 vocabulary-clean 的学术化语言改写, 单独 cycle + DEC 启动。

## 6. 元数据与上游链接

| 字段 | 取值 |
|---|---|
| 文件路径 | `Dream/3R-mix/deliverables/RELATION_TO_TRACK_A_2026-05-16.md` |
| 创建日期 | 2026-05-16 |
| 状态 | 内部留档 / 不外发 |
| 作者 | Dream agent (cycle 036) |
| 上游决策 | DEC-20260516-001 (cycle 036 launch) |
| 关键引用 | DEC-20260506-001 / DEC-20260501-011 / DEC-20260504-002 / DEC-20260515-001 / `Dream/3R-mix/main.tex` (sibling, 不引用) / `Dream/planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md` |
| 下游候选 | 如果未来需要外发版本, 必须独立 cycle + DEC 起草 |

---

**End of internal meta.** 本文件不与综述 PDF 同包提交; 仅作项目内部审计锚点。
