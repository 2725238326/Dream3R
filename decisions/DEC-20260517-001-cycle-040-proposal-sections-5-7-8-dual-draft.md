# DEC-20260517-001: Cycle 040 Dream3R proposal § 5 + § 7 + § 8 dual-draft drafting

Status: accepted

Date: 2026-05-17

Cycle: 040

Decision type: bounded markdown deliverable execution (single scope: cycle 040 § 5 实验设计与评测协议 + § 7 研究进展与已完成工作 + § 8 研究计划与时间安排 dual-draft drafting in `planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` and `planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md`)

Authorized trigger: user 2026-05-17 message "A" approving cycle 040 launch as the recommended next direction per DEC-20260516-004 §Next Direction If Passed option A; cycle 039 was closed earlier the same session with 8 file ops + G0-G6 passing on first pass for G3a + G3b, with 7 corrective edits per side on G4 negation-context hits per cycle 036 precedent.

## Decision

Proceed with cycle 040 to draft § 5 + § 7 + § 8 in both drafts together (per OUTLINE_V1.md §4 cycle 040 target — three implementation-anchored chapters drafted together because all three need to digest W1-W18 + KITTI smoke + cycle 033/034/035 deliverables + NEXT_PHASE_ROADMAP). These are the proposal's most evidence-dense chapters.

### § 5 实验设计与评测协议 (7 sub-sections per OUTLINE §3 chapter mapping + cycle 036 plan §B1.1)

1. § 5.1 三层证据阶梯 (论文层 / 代理用例层 / 原型实现层)
2. § 5.2 架构层消融实验组 (ABL-v02-1..10; tier 1 load-bearing ABL-v02-1+4+6+10)
3. § 5.3 记忆机制消融实验组 (ABL-memory-0..11; cycle 029 v1.1 oracle-bus + hard/soft fail rule)
4. § 5.4 校验阈值标定方案 (CRITIC_CALIBRATION_PLAN_V1 六类失败模式 × 5 sub-signal 表; method A vs B)
5. § 5.5 长序列真实数据评测 (LONG_SEQ_REAL_TABLE_PLAN; 4 variants × 4 metrics × windows ∈ {10,20,50,100}; B4 缓存治理 coverage gap)
6. § 5.6 评测数据集 (KITTI 主, DTU 拟扩展, 合成 fixture P0 + R1-R5)
7. § 5.7 主要评测指标 (pointmap L2 / depth RMSE / route_regret / scale_drift_proxy / memory_decay_proxy / anchor_fill_rate / retrieval_diversity / failure-mode detection rate)

### § 7 研究进展与已完成工作 (6 sub-sections per OUTLINE §3 chapter mapping + cycle 036 plan §B1.1)

1. § 7.1 架构设计文档系列 (SPEC v0.1 / v0.2 / v0.3 七份)
2. § 7.2 实现里程碑 W1-W18 (Tier 1 集成验证 11 项 + Tier 2 真实数据 smoke)
3. § 7.3 KITTI 真实数据集成证据 (pointmap L2 = 20.4747 on 2011_09_26_drive_0001_sync_02; integration evidence, not 训练后质量)
4. § 7.4 综述发布 (Track B 3R-mix 18 A4 页 / 44 引文 / 6 图 5 表 / 路线 C arXiv-only / 2026-05-15 prose naturalization deliverable)
5. § 7.5 综述反哺主线 (cycle 035 4 markdown deliverables + WORK_RISK_REGISTER v1.1 +4 行)
6. § 7.6 cycle 历史 (cycle 015 起架构主线 -> cycle 016 SPEC v0.1 -> cycle 018-021 v0.2 trio -> cycle 022 paper v1.2 -> cycle 023-027 v0.3 memory 设计 -> cycle 028-031 P0 + ablation -> cycle 032 server verify -> cycle 033-034 W1-W18 -> cycle 035 综述反哺 -> cycle 036-039 开题报告)

### § 8 研究计划与时间安排 (3 sub-sections per OUTLINE §3 chapter mapping + cycle 036 plan §B1.1)

1. § 8.1 短期 (cycle 040-042 开题报告完稿 + 提交; M1-M2)
2. § 8.2 中期 (M3-M5; W19-W23 真实路由 + W24 Critic 校准 + W25 TTT + W26 输入扩展 + B1/B2/B3 v0.4 spec delta)
3. § 8.3 长期 (M6-M8; W27 3DGS renderer + 真实数据训练 + 论文撰写 + 综合评测)

Target word count per OUTLINE_V1.md §2 表:

- 外部稿 §5 ~2000 字 + §7 ~1500 字 + §8 ~1000 字 = ~4500 字
- 内部稿 §5 ~2800 字 + §7 ~2200 字 + §8 ~1500 字 = ~6500 字
- 双稿合计 ~11000 字

Tolerance ±20%.

Order of operation: internal first (master), then external snapshot per STYLE_CONTRACT §3 规则 1. § 5 / § 7 / § 8 一起起草因 (a) 三章都消费 W1-W18 + cycle 033/034/035 deliverables 相同上游素材, 单 cycle 内 batch read 一次效率最高; (b) §5 评测设计 与 §7 已完成工作 与 §8 时间安排 三章互为时间锚 (现状 + 计划); (c) 通稿一致性 stress 测试在三章并置时最有效。

预计 STYLE_CONTRACT §2 vocab table 可能新增 2-5 行 (实证-anchored 章节, 涉及 KITTI sequence ID / fixture regime R1-R5 / hard_fail vs soft_fail / W-task evidence labels / monotonic upgrade gate 等 module-internal + 评测 protocol 术语)。

## Scope

Allowed in cycle 040:

- edit `Dream/planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` to replace § 5 + § 7 + § 8 `<!-- TBD cycle 040 -->` placeholders with body text (7+6+3 = 16 sub-sections + intros + closing paragraphs)
- edit `Dream/planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md` similarly with vocabulary-clean snapshots
- edit `Dream/planning/proposal_dream3r/STYLE_CONTRACT.md` §2 vocab substitution table to append new rows surfaced during § 5 + § 7 + § 8 drafting (additions only; no removals)
- edit `Dream/planning/proposal_dream3r/STYLE_CONTRACT.md` §6 sync log to append the cycle 040 entry
- update both drafts' top metadata blocks (Last updated + 状态 fields)
- create `Dream/decisions/DEC-20260517-001-cycle-040-proposal-sections-5-7-8-dual-draft.md` (this file; cycle 040 authorization root)
- create `Dream/cycles/CYCLE-20260517-001.md` (cycle 040 log)
- update `Dream/TASK_SNAPSHOT.md` (sync first per F-001) + `Dream/WORKFLOW_STATUS.md` + `Dream/INDEX.md`
- reference SPEC-005 v0.2 (ABL-v02-1..9) + SPEC-007 v0.3 (ABL-v02-10 + VGGT baseline) + SPEC-008 v0.3 + SPEC-008-ablation (ABL-memory-0..11 + cycle 029 v1.1) + CRITIC_CALIBRATION_PLAN_V1 + LONG_SEQ_REAL_TABLE_PLAN + code/dream3r/RECENT_PROGRESS.md + code/dream3r/NEXT_PHASE_ROADMAP.md + SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §6 W-task reorder by section / line anchor; do NOT modify any of them

Not authorized in cycle 040:

- editing `Dream/3R-mix/main.tex` / `references.bib` / `notes/*` (Track B wound down 2026-05-14)
- editing any SPEC file under `Dream/specs/`
- editing any file under `Dream/code/` / `Dream/paradigm/` / `/hdd3/kykt26/code/dream3r/`
- editing `DRAFT_*_V1.md` sections other than § 5 + § 7 + § 8 (§ 1 + § 2 + § 3 + § 4 + § 6 already complete; § 9 stays placeholder)
- editing `OUTLINE_V1.md` / `WORK_RISK_REGISTER.md`
- checkpoint download, training, model inference, server actions, ablation runs
- launching any v0.4 spec delta drafting (B1 / B2 / B3 still proposal-status; cited as forward-looking only in § 8.2)
- frontend / navigation work, demo storyboard promotion past `draft`
- retiring any non-finalist track, declaring teacher-demo readiness
- introducing `cycle` / `SPEC-` / `DEC-` / `CR-N` (where N is literal digit) / `agent` / `skill` / `workflow` / `本地项目` strings into `DRAFT_EXTERNAL_V1.md` § 5 + § 7 + § 8 prose, OR raw `Dream3R` into external main text
- introducing forbidden over-claim phrasings (`证明.{0,10}优于` / `最佳.{0,5}架构` / `最终.{0,5}架构` / `X 解决了` / `Dream3R 解决了`) into either draft § 5 + § 7 + § 8 — § 7 + § 8 in particular must use "demo-observed" / "code-observed" / "engineering-judgment" / "尚未训练后质量" labels per RESEARCH_CODE_DISCIPLINE rule 5 Honesty Override; the pointmap L2 = 20.4747 数值 must be qualified as "集成证据, 非训练后质量" (per RECENT_PROGRESS.md line 78 boundary statement)

## Required Boundary

§ 5 实验设计 + § 7 研究进展 + § 8 时间安排 are **evidence-anchored** chapters. They state what has been done (§ 7), what evaluation will be done (§ 5), and when (§ 8) — all at the research-plan level. They do NOT:

- claim pointmap L2 = 20.4747 as training-quality / SOTA-comparable result (per RECENT_PROGRESS.md line 78: "This is real-data integration evidence, not SOTA reconstruction accuracy"; § 7.3 must repeat the integration-vs-quality caveat verbatim or via equivalent paraphrase)
- promise ABL-v02-1..10 / ABL-memory-0..11 / CRITIC_CALIBRATION_PLAN_V1 / LONG_SEQ_REAL_TABLE_PLAN results before they are run (§ 5 describes plans + 评测 protocol; § 7 says ABL-memory-0 passed fixture/logging gate as validity gate, NOT C2 memory quality validation)
- start any server / ablation / calibration run (F-002 remains in force; cycle 040 is markdown-only)
- modify the W19-W30 roadmap structure (§ 8 references NEXT_PHASE_ROADMAP.md task list by paraphrase; W-task reorder recommendation from cycle 035 SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §6 cited as recommendation-status, not as locked schedule)
- collapse the candidate-not-final framing (DEC-20260501-011 + DEC-20260504-002 in force; § 5 + § 7 + § 8 must remain compatible with v0.4 revision + B1/B2/B3 spec delta candidates + finalist independence)

The reuse of SPEC-005 v0.2 / SPEC-007 v0.3 / SPEC-008 v0.3 / SPEC-008-ablation / CRITIC_CALIBRATION_PLAN_V1 / LONG_SEQ_REAL_TABLE_PLAN / RECENT_PROGRESS / NEXT_PHASE_ROADMAP content is by paraphrase + structural reorganization into the §5/§7/§8 narrative; no verbatim copy of spec / plan paragraphs. Each ABL ID / W-task ID may be referenced by ID in internal draft, but in external draft these IDs are vocab-replaced per STYLE_CONTRACT §2 (ABL-v02-N → "本研究的消融实验组 N" or 学术化中文; W1-W18 → "实现里程碑 1-18"; etc.).

## Output Interpretation

If cycle 040 closes cleanly, the strongest allowed claim is:

```text
Cycle 040 lands § 5 实验设计与评测协议 + § 7 研究进展与已完成工作
+ § 8 研究计划与时间安排 in both DRAFT_INTERNAL_V1.md (~6500 字)
and DRAFT_EXTERNAL_V1.md (~4500 字). § 5 covers 7 sub-sections
(三层证据阶梯 + ABL-v02 架构消融 + ABL-memory 记忆消融 + Critic
标定 + 长序列真实评测 + 评测数据集 + 主要评测指标). § 7 covers
6 sub-sections (架构设计文档系列 + 实现里程碑 W1-W18 + KITTI
集成证据 + 综述发布 + 综述反哺 + cycle 历史). § 8 covers 3
sub-sections (短期 / 中期 / 长期). The deliverables are evidence-
anchored text at research-plan level; no spec change, code change,
calibration run, ablation run, or v0.4 delta drafting has been
validated by cycle 040. The candidate-not-final framing is
preserved throughout; § 7.3 KITTI smoke evidence is qualified as
"集成证据, 非训练后质量". STYLE_CONTRACT §2 vocab substitution
table may grow by 2-5 rows for newly surfaced evaluation-protocol
terminology. § 1 + § 2 + § 3 + § 4 + § 5 + § 6 + § 7 + § 8 累计
~17800 内 + ~14000 外 字 ≈ 85% of OUTLINE_V1 §2 表 总字数估算
(~21100 内 / ~16000 外). Only § 9 remains for cycle 041.
```

The following remain unvalidated by cycle 040:

- whether § 7.3 KITTI L2=20.47 数值 + "集成证据" 限定语 reads with sufficient evidence-boundary clarity to advisor (the digit looks substantial; advisor may misread as 重建质量数值 unless caveat is prominent)
- whether § 5 evaluation protocol reads as plan vs as already-run (the 表 format common in实证章节 may suggest "已跑" by visual convention; need to repeat "plan-only; 执行 gated on F-002 server authorization" caveats)
- whether § 8 medium-term M3-M5 timeline reads as committed schedule vs as proposed schedule (the M-numbering may carry committed-schedule connotation; § 8.1 须明示这是 candidate timeline 不是 committed timeline)
- whether the §7.6 cycle 历史 reads naturally without exposing too many cycle ID + DEC ID + SPEC ID 编号; STYLE_CONTRACT §2 已有对译规则但 cycle 040 是首次 stress test on 历史 narrative
- whether the 41-row + cycle 039 +2 = 43-row vocab substitution table holds up under § 5 + § 7 + § 8 drafting; if 评测 protocol 术语 surfaces > 5 new rows, may indicate the seed table needs structural revision (cycle 041 通稿审查 covers)
- whether the candidate-not-final 句式 contrast 表 (cycle 036 + cycle 039 9 + 7 rows) needs additional entries for evidence-anchored 句式 (e.g., "本研究跑出了 ... " vs "本研究 plan to 跑 ... "; "本研究在 ... 上的实证表现 ... " vs "本研究的对照实验数据 ... ")

## Stop Gates

| Gate | Pass criterion |
|---|---|
| G0 authorization | this DEC accepted; scope matches the approved direction (DEC-20260516-004 §Next Direction option A); explicit allowed / not-authorized lists present |
| G1 path setup | only the 8 paths listed in §Decision receive content (`DRAFT_INTERNAL_V1.md` § 5 + § 7 + § 8 only / `DRAFT_EXTERNAL_V1.md` § 5 + § 7 + § 8 only / `STYLE_CONTRACT.md` §2 + §6 appends only / this DEC / `CYCLE-20260517-001.md` / 3 sync targets); specifically NOT touched: `Dream/3R-mix/*`, `Dream/specs/*`, `Dream/code/*`, `Dream/paradigm/*`, `/hdd3/kykt26/*`, `OUTLINE_V1.md`, `WORK_RISK_REGISTER.md`, `DRAFT_*_V1.md` sections other than § 5 + § 7 + § 8 |
| G2 vocab firewall (Track B side) | n/a; cycle 036 G2 verification stands |
| G3a vocab firewall (external proposal forbidden patterns) | `Grep` on full `DRAFT_EXTERNAL_V1.md` for pattern `cycle\|SPEC-\|DEC-\|CR-N\|agent\|skill\|workflow\|本地项目` returns 0 hits (covers § 1 + § 2 + § 3 + § 4 + § 5 + § 6 + § 7 + § 8) — this is the cycle's most stressful G3a test because § 5 + § 7 + § 8 are the most ID-heavy chapters; expect first-pass hits requiring corrective edits, similar to cycle 036 § 1 pattern |
| G3b vocab firewall (external Dream3R case-insensitive) | `Grep -i` on full `DRAFT_EXTERNAL_V1.md` for `Dream3R` returns 0 hits |
| G4 candidate-not-final language | `Grep` on full `DRAFT_EXTERNAL_V1.md` + full `DRAFT_INTERNAL_V1.md` for over-claim patterns `证明.{0,10}优于\|最佳.{0,5}架构\|最终.{0,5}架构\|X 解决了\|Dream3R 解决了` returns 0 hits on both — per cycle 036 + cycle 039 precedent, may require corrective rephrasing; the new risk surface in cycle 040 is "本研究跑出了 ... " over-claim style (not in current G4 pattern); cycle log will note any surfacing of new over-claim styles for cycle 041 STYLE_CONTRACT §5 revisit |
| G5 outputs and traceability | DRAFT_INTERNAL_V1.md § 5 body present (~2800 字, within ±20%) + § 7 body present (~2200 字, within ±20%) + § 8 body present (~1500 字, within ±20%); DRAFT_EXTERNAL_V1.md § 5 body present (~2000 字, within ±20%) + § 7 body present (~1500 字, within ±20%) + § 8 body present (~1000 字, within ±20%); § 5 7 sub-sections + § 7 6 sub-sections + § 8 3 sub-sections + intros + closing paragraphs all in place; STYLE_CONTRACT §2 vocab table grew by 2-5 rows; §6 sync log carries cycle 040 entry; § 5 + § 7 + § 8 素材 traceable to SPEC-005 v0.2 + SPEC-007 v0.3 + SPEC-008 v0.3 + SPEC-008-ablation + CRITIC_CALIBRATION_PLAN_V1 + LONG_SEQ_REAL_TABLE_PLAN + RECENT_PROGRESS + NEXT_PHASE_ROADMAP + SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §6 |
| G6 sync chain | `TASK_SNAPSHOT.md` updated first per F-001; `WORKFLOW_STATUS.md` updated; `INDEX.md` updated (cycles row + proposal draft status); cycle log links to this DEC + edited files + sync targets |

Failing any gate → cycle 040 does NOT close; resume from the failing gate.

## Next Direction If Passed

After cycle 040 closes, the next admissible decision is one of:

- A: launch cycle 041 to draft § 9 风险分析 + 通稿审查 + STYLE_CONTRACT final sync (per OUTLINE_V1 §4 cycle 041 target — risk 章节 + full-document consistency review; ~1000 外 + ~1500 内 字; total ~2500 字)
- B: revise § 5 + § 7 + § 8 based on cycle-end self-review or advisor feedback
- C: launch the cycle 035 §Next Direction A-C alternatives (calibration / long-seq ablation / v0.4 spec delta drafting)
- D: pause and reassess after § 5 + § 7 + § 8 quality review
- E: user executes the Track B survey submission action (independent of cycle 040)
- F: return to architecture-first mainline non-proposal work (W22 / W23 / Fast3R omegaconf)

DEC-20260506-001 architecture-first mainline, DEC-20260504-002 no-all-in, DEC-20260501-011 candidate-not-final, DEC-20260503-001 research-code-discipline, DEC-20260515-001 cycle 035 launch, DEC-20260516-001 cycle 036 launch, DEC-20260516-002 cycle 037 launch, DEC-20260516-003 cycle 038 launch, DEC-20260516-004 cycle 039 launch, F-001 anti-32MB, F-002 server-side discipline all remain in force unchanged.
