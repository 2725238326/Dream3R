# DEC-20260516-004: Cycle 039 Dream3R proposal § 3 候选研究问题 + § 6 预期成果与创新点 dual-draft drafting

Status: accepted

Date: 2026-05-16

Cycle: 039

Decision type: bounded markdown deliverable execution (single scope: cycle 039 § 3 候选研究问题 + § 6 预期成果与创新点 dual-draft drafting in `planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` and `planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md`)

Authorized trigger: user 2026-05-16 message "请你全面推进，同时啊整理并且更新文档" approving cycle 039 launch as the recommended next direction per DEC-20260516-003 §Next Direction If Passed option A; cycle 038 was closed earlier the same session with 8 file ops + G0-G6 passing (1 corrective edit on G3a for cycle-037-residue metadata leakage).

## Decision

Proceed with cycle 039 to draft § 3 候选研究问题 + § 6 预期成果与创新点 in both drafts together (per OUTLINE_V1.md §4 cycle 039 target — two framing chapters drafted together because problem statement and outcome claim are tightly coupled).

§ 3 covers 5 sub-sections per OUTLINE_V1.md §3 chapter mapping table row §3 + cycle 036 plan §B1.1:

1. § 3.1 Q1 验证机制路径 (Critic; built on §1.4 Q1 + §2.5 测试时三类机制 + §4.5 校验模块 hybrid 配置)
2. § 3.2 Q2 长序列内存机制统一 (Memory; built on §1.4 Q2 + §2.4 长序列内存四类 + §4.3 记忆模块 NSA three-branch 覆盖关系)
3. § 3.3 Q3 多专家组合实证评估 (Composer; built on §1.4 Q3 + §2.7 落点 + §4.6 编排模块 7 专家池)
4. § 3.4 候选架构 X 的四个 finalist 模块边界 (校验 / 记忆 / 永久性 / 编排; built on DEC-20260504-002 no-all-in + 4 finalist 独立性)
5. § 3.5 候选 vs 最终的研究地位声明 (built on DEC-20260501-011 candidate-not-final)

§ 6 covers 3 sub-sections per OUTLINE_V1.md §3 chapter mapping table row §6 + cycle 036 plan §B1.1:

1. § 6.1 预期交付物 (架构设计文档 + 原型实现 + 评测结果)
2. § 6.2 创新点声明 (verification-as-architecture / heterogeneous best-of-N / NSA-hybrid memory; 严格使用 candidate-not-final 句式)
3. § 6.3 与现有工作的实证差异 (不主张优于 SOTA, 主张提供对照实验证据)

Target word count per `OUTLINE_V1.md` §2 表 + §4 cycle 039 行:

- 外部稿 §3 ~1500 字 + 外部稿 §6 ~1000 字 = ~2500 字
- 内部稿 §3 ~1800 字 + 内部稿 §6 ~1300 字 = ~3100 字
- 双稿合计 ~5600 字

Tolerance ±20%.

Order of operation: internal first (master), then external snapshot per STYLE_CONTRACT §3 规则 1. § 3 + § 6 一起起草因 §3 三个 Q 与 §6 三个创新点 一一对应 (Q1 → 创新点 1 verification-as-architecture; Q2 → 创新点 3 NSA-hybrid memory; Q3 → 创新点 2 heterogeneous best-of-N); 两章框架性最强 + 候选措辞密度最高 + 受 §5 candidate-not-final 句式表约束最重。

预计 STYLE_CONTRACT §2 vocab table 可能新增 0-3 行 (research-claim language is the next stress dimension, but cycle 038's 41-row table already covers most module-internal terminology; 新增条目可能集中在: research-question 命名 / 创新点 命名 / 评测维度 命名 等)。如果 0 行新增, 表明 41-row table 已饱和; 如果有新增, 在 §6 sync log 中记录。

## Scope

Allowed in cycle 039:

- edit `Dream/planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` to replace § 3 + § 6 `<!-- TBD cycle 039 -->` placeholders with body text (5 sub-sections in §3 + 3 sub-sections in §6 + section intros + closing 落点 paragraphs)
- edit `Dream/planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md` similarly with vocabulary-clean snapshots
- edit `Dream/planning/proposal_dream3r/STYLE_CONTRACT.md` §2 vocab substitution table to append new rows surfaced during § 3 + § 6 drafting (additions only; no removals)
- edit `Dream/planning/proposal_dream3r/STYLE_CONTRACT.md` §6 sync log to append the cycle 039 entry
- update both drafts' top metadata blocks (Last updated + 状态 fields)
- create `Dream/decisions/DEC-20260516-004-cycle-039-proposal-sections-3-and-6-dual-draft.md` (this file; cycle 039 authorization root)
- create `Dream/cycles/CYCLE-20260516-004.md` (cycle 039 log)
- update `Dream/TASK_SNAPSHOT.md` (sync first per F-001) + `Dream/WORKFLOW_STATUS.md` + `Dream/INDEX.md`
- reference DEC-20260501-011 + DEC-20260504-002 + 综述 §10 失败模式 + §1.4 三个 Q + §2.4 + §2.5 + §2.7 + §4.3 + §4.5 + §4.6 by section anchor; do NOT modify
- reference `Dream/specs/SPEC-20260506-004` v0.2 + `SPEC-20260508-001` v0.3 by section / Delta anchor; do NOT modify
- reference `Dream/planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md` §5 B1 / B2 / B3 v0.4 spec delta candidates as forward-looking citations; do NOT modify

Not authorized in cycle 039:

- editing `Dream/3R-mix/main.tex` / `references.bib` / `notes/*` (Track B wound down 2026-05-14)
- editing any SPEC file under `Dream/specs/`
- editing any file under `Dream/code/` / `Dream/paradigm/` / `/hdd3/kykt26/code/dream3r/`
- editing `DRAFT_INTERNAL_V1.md` / `DRAFT_EXTERNAL_V1.md` sections other than § 3 + § 6 (§ 1 + § 2 + § 4 already complete; § 5 / § 7 / § 8 / § 9 stay placeholders)
- editing `OUTLINE_V1.md` (cycle 039 § 3 + § 6 structural revisions, if any surfaced, would be deferred to OUTLINE_V2 in a later cycle)
- editing `WORK_RISK_REGISTER.md` (no new proposal-cycle risks expected; if any surfaces, append in cycle 041 §9 风险章节起草时)
- checkpoint download, training, model inference, server actions, ablation runs
- launching any v0.4 spec delta drafting (B1 / B2 / B3 from cycle 035 proposal §5 still proposal-status; § 3 may reference them as candidate v0.4 deltas, but does not start their drafting)
- frontend / navigation work, demo storyboard promotion past `draft`
- retiring any non-finalist track, declaring teacher-demo readiness
- introducing `cycle` / `SPEC-` / `DEC-` / `CR-N` (where N is a literal digit) / `agent` / `skill` / `workflow` / `本地项目` strings into `DRAFT_EXTERNAL_V1.md` § 3 + § 6 prose, OR raw `Dream3R` into the external draft main text (only 代号 "候选架构 X" / "本研究架构" naming allowed externally)
- introducing forbidden over-claim phrasings (`证明.{0,10}优于` / `最佳.{0,5}架构` / `最终.{0,5}架构` / `X 解决了` / `Dream3R 解决了`) into either draft § 3 + § 6; candidate-not-final language per STYLE_CONTRACT §5 句式对比表 is mandatory throughout — § 3 + § 6 is THE highest-density stress test of the candidate-not-final 句式 因为它们直接对应"研究问题 + 预期成果"

## Required Boundary

§ 3 candidate research questions + § 6 expected outcomes are **claim-positioning** text. They state what the research will investigate + what evidence the research aims to provide, at the research-plan level, not at the result-claiming level. They do NOT:

- promote Dream3R / 候选架构 X from candidate to finalist (DEC-20260501-011 candidate-not-final remains in force; the three Q's and the three innovation points must remain compatible with "X 是当前迭代的候选; 后续版本可能修订或替换" framing)
- collapse the 4 finalist mechanisms (Critic / Memory / Permanence / Composer) into a single one (DEC-20260504-002 no-all-in remains in force; the three Q's anchor independently to three distinct finalist mechanisms; §3.4 explicitly preserves the 4-module independence including Permanence which is not the subject of any of the three Q's but remains a peer finalist)
- claim architecture-level superiority over comparator methods on any specific metric in § 6 (must use "评估 X 在 ... 维度上是否呈现优势" / "提供对照实验证据" style; never "证明 X 优于 Y" style)
- promise specific numeric performance targets in § 6 (must use "在 ... 评测维度上提供对照实验数据" not "在 KITTI 上达到 L2 < N")
- start any server / ablation / calibration run (F-002 remains in force; cycle 039 is markdown-only)
- modify the W19-W30 roadmap (the cycle 035 proposal §6 W-task reorder is still recommendation-status; § 8 时间安排 in cycle 040 will revisit, not cycle 039)
- expand the three research questions beyond the three established in §1.4 + §4.8 (Q1 verification / Q2 long-seq memory / Q3 composer); new research questions surfaced during § 3 drafting are recorded as observations in cycle log, not added to § 3 body

The reuse of §1.4 three Q's + §2.4 长序列内存四类 + §2.5 测试时三类 + §2.7 落点矩阵 + §4.3 + §4.5 + §4.6 + §4.8 结构差异 content is by paraphrase + structural reorganization into the §3 + §6 narrative; no verbatim copy of earlier section paragraphs. Where §1.4 already states Q1 / Q2 / Q3, § 3 expands each Q with: (a) why this is a research question (gap identification anchored to §2 谱系); (b) what the candidate-architecture-X 路径 is at structural level (anchored to §4 模块); (c) what falsification 路径 looks like at §5 evaluation level (forward-reference; §5 not yet drafted, so § 3 cites by name not by detail); (d) candidate-not-final 边界 声明.

## Output Interpretation

If cycle 039 closes cleanly, the strongest allowed claim is:

```text
Cycle 039 lands § 3 候选研究问题 + § 6 预期成果与创新点 in both
DRAFT_INTERNAL_V1.md (~3100 字) and DRAFT_EXTERNAL_V1.md (~2500 字).
§ 3 covers 5 sub-sections (Q1 + Q2 + Q3 + 4-module finalist 边界 +
候选 vs 最终 声明) and § 6 covers 3 sub-sections (预期交付物 +
创新点声明 + 与现有工作的实证差异). The deliverables are claim-
positioning text at research-plan level; no spec change, code
change, calibration run, ablation run, or v0.4 delta drafting has
been validated by cycle 039. The candidate-not-final framing is
preserved throughout, with §3.5 and §6.2 + §6.3 carrying the
densest candidate-not-final 句式 application across the entire
proposal. The bilingual sync contract (STYLE_CONTRACT §3) survives
its third major stress test under ~5600 字 of framework-dense
synchronized content; the §2 vocab substitution table may grow by
0-3 rows for any new research-claim-level terminology surfaced.
§ 1 + § 2 + § 3 + § 4 + § 6 累计 ~11300 内 + ~9500 外 字 ≈ 54% of
OUTLINE_V1 §2 表 总字数估算 (~21100 内 / ~16000 外).
```

The following remain unvalidated by cycle 039:

- whether the three Q's read naturally to advisor / committee at the framework level (cycle 041 通稿审查 covers)
- whether §3.5 + §6.2 + §6.3 candidate-not-final 措辞 reads naturally in external Chinese academic prose at scale (this is the highest-density claim-language stress test of STYLE_CONTRACT §5 句式对比表)
- whether § 6 三个创新点 与 §3 三个 Q 的对应关系 (Q1↔IP1 / Q2↔IP3 / Q3↔IP2) reads naturally in advisor context, or需要 reorder
- whether the §6.1 预期交付物 list reads as committed deliverables vs aspirational deliverables (the 候选-not-final framing should clarify this, but advisor reading may differ)
- whether the cycle-038 41-row vocab substitution table holds under § 3 + § 6 drafting (research-claim language is the next stress dimension)

## Stop Gates

| Gate | Pass criterion |
|---|---|
| G0 authorization | this DEC accepted; scope matches the approved direction (DEC-20260516-003 §Next Direction option A); explicit allowed / not-authorized lists present |
| G1 path setup | only the 8 paths listed in §Decision receive content (`DRAFT_INTERNAL_V1.md` § 3 + § 6 only / `DRAFT_EXTERNAL_V1.md` § 3 + § 6 only / `STYLE_CONTRACT.md` §2 + §6 appends only / this DEC / `CYCLE-20260516-004.md` / 3 sync targets); specifically NOT touched: `Dream/3R-mix/*`, `Dream/specs/*`, `Dream/code/*`, `Dream/paradigm/*`, `/hdd3/kykt26/*`, `OUTLINE_V1.md`, `WORK_RISK_REGISTER.md` |
| G2 vocab firewall (Track B side) | n/a; cycle 036 G2 verification stands |
| G3a vocab firewall (external proposal forbidden patterns) | `Grep` on full `DRAFT_EXTERNAL_V1.md` for pattern `cycle\|SPEC-\|DEC-\|CR-N\|agent\|skill\|workflow\|本地项目` returns 0 hits (covers § 1 + § 2 + § 3 + § 4 + § 6) |
| G3b vocab firewall (external Dream3R case-insensitive) | `Grep -i` on full `DRAFT_EXTERNAL_V1.md` for `Dream3R` returns 0 hits |
| G4 candidate-not-final language | `Grep` on full `DRAFT_EXTERNAL_V1.md` + full `DRAFT_INTERNAL_V1.md` for over-claim patterns `证明.{0,10}优于\|最佳.{0,5}架构\|最终.{0,5}架构\|X 解决了\|Dream3R 解决了` returns 0 hits on both — this is the cycle's hardest gate because § 3 + § 6 are the claim-positioning chapters |
| G5 outputs and traceability | DRAFT_INTERNAL_V1.md § 3 body present (~1800 字, within ±20% of estimate) + § 6 body present (~1300 字, within ±20%); DRAFT_EXTERNAL_V1.md § 3 body present (~1500 字, within ±20%) + § 6 body present (~1000 字, within ±20%); § 3 sub-sections 5 + § 6 sub-sections 3 + intros + closing paragraphs all in place; § 3 + § 6 素材 traceable to §1.4 三个 Q + §2 谱系 + §4 架构 + DEC-20260501-011 + DEC-20260504-002; STYLE_CONTRACT §2 vocab table grew by 0-3 rows (any added rows recorded in §6 sync log); §6 sync log carries the cycle 039 entry |
| G6 sync chain | `TASK_SNAPSHOT.md` updated first per F-001; `WORKFLOW_STATUS.md` updated; `INDEX.md` updated (cycles row + proposal draft status); cycle log links to this DEC + edited files + sync targets |

Failing any gate → cycle 039 does NOT close; resume from the failing gate.

## Next Direction If Passed

After cycle 039 closes, the next admissible decision is one of:

- A: launch cycle 040 to draft § 5 实验设计与评测协议 + § 7 研究进展与已完成工作 + § 8 研究计划与时间安排 together (per OUTLINE_V1 §4 cycle 040 target — three implementation-anchored chapters drafted together because all three need to digest W1-W18 + KITTI smoke + cycle 033/034/035 deliverables + NEXT_PHASE_ROADMAP; ~2000 外 + ~2800 内 字 for § 5, ~1500 外 + ~2200 内 字 for § 7, ~1000 外 + ~1500 内 字 for § 8; total ~11000 字)
- B: revise § 3 + § 6 based on cycle-end self-review or advisor feedback
- C: launch the cycle 035 §Next Direction A-C alternatives (calibration / long-seq ablation / v0.4 spec delta drafting)
- D: pause and reassess after § 3 + § 6 quality review
- E: user executes the Track B survey submission action (independent of cycle 039)
- F: return to architecture-first mainline non-proposal work (W22 / W23 / Fast3R omegaconf)

DEC-20260506-001 architecture-first mainline, DEC-20260504-002 no-all-in, DEC-20260501-011 candidate-not-final, DEC-20260503-001 research-code-discipline, DEC-20260515-001 cycle 035 launch, DEC-20260516-001 cycle 036 launch, DEC-20260516-002 cycle 037 launch, DEC-20260516-003 cycle 038 launch, F-001 anti-32MB, F-002 server-side discipline all remain in force unchanged.
