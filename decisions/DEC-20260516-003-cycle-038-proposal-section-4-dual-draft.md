# DEC-20260516-003: Cycle 038 Dream3R proposal § 4 研究方案 / 架构 dual-draft drafting

Status: accepted

Date: 2026-05-16

Cycle: 038

Decision type: bounded markdown deliverable execution (single scope: cycle 038 § 4 研究方案 / Dream3R v0.3 架构 C1-C6 dual-draft drafting in `planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` and `planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md`)

Authorized trigger: user 2026-05-16 message "继续推进" approving cycle 038 launch as the recommended next direction per DEC-20260516-002 §Next Direction If Passed option A; cycle 037 was closed earlier the same session with all 8 file ops + G0-G6 passing on first pass.

## Decision

Proceed with cycle 038 to draft § 4 研究方案 (外部稿) / Dream3R v0.3 架构 (内部稿) in both drafts. § 4 covers the eight sub-sections proposed in `OUTLINE_V1.md` §2 大纲表 + §3 chapter mapping table row §4:

1. § 4.1 整体设计 + 帧预算 (Delta 1 in SPEC-20260506-004 v0.2: 30-50 ms/frame; speed priority)
2. § 4.2 感知模块 / C1 Perceiver (Delta 2: DINOv3-S frozen backbone replaces ViT-L, ~14x 参数减少 + ~5x 延迟加速)
3. § 4.3 记忆模块 / C2 Memory (Delta 3 + SPEC-20260508-001 v0.3 addendum: 三分支稀疏注意力 compressed/selected/sliding + AnchorBank K=256 + StateToken + Mamba-Transformer 混合循环结构)
4. § 4.4 永久性模块 / C3 Permanence (Slot Attention + permanence_link)
5. § 4.5 校验模块 / C4 Critic (Sampson 几何 + depth 一致性 + 共视 conflict 三类信号 + repair actions 0/1/2 stub 3/4/5)
6. § 4.6 编排模块 / C5 Composer (Delta 5: 7 admitted lightweight experts MASt3R / Fast3R / Spann3R / CUT3R / MoGe-2 / DepthAnything-V2 / Test3R; capability descriptor + routing axis)
7. § 4.7 总线模块 / C6 Bus (CR-1..CR-6 cross-spec signal contract v2.1)
8. § 4.8 与现有 3R 系统的结构差异 (本研究架构 / Dream3R v0.3 整体结构与单一支线方法的对比)

Target word count per `OUTLINE_V1.md` §2 表: 外部稿 ~3000 字, 内部稿 ~4000 字; tolerance ±20%.

Order of operation: internal first (master), then external snapshot per STYLE_CONTRACT §3 规则 1. § 4 是 OUTLINE_V1.md §4 关键 cycle 决策点之一: 因 module-internal terminology dense 程度最高, 预计 STYLE_CONTRACT §2 vocab table 可能新增 5-10 行 (e.g., 帧预算 / Slot Attention / Sampson 几何 / 共视 conflict / repair actions / capability descriptor / attention regime / Sparse Attention as architectural optimization 等模块内部术语外稿对译规则)。

## Scope

Allowed in cycle 038:

- edit `Dream/planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` to replace § 4 `<!-- TBD cycle 038 -->` placeholder with body text (8 sub-sections + section intro + closing 落点 paragraph)
- edit `Dream/planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md` similarly with vocabulary-clean snapshot
- edit `Dream/planning/proposal_dream3r/STYLE_CONTRACT.md` §2 vocab substitution table to append new rows surfaced during § 4 drafting (additions only; no removals)
- edit `Dream/planning/proposal_dream3r/STYLE_CONTRACT.md` §6 sync log to append the cycle 038 entry
- update both drafts' top metadata blocks (Last updated + 状态 fields)
- create `Dream/decisions/DEC-20260516-003-cycle-038-proposal-section-4-dual-draft.md` (this file; cycle 038 authorization root)
- create `Dream/cycles/CYCLE-20260516-003.md` (cycle 038 log)
- update `Dream/TASK_SNAPSHOT.md` (sync first per F-001) + `Dream/WORKFLOW_STATUS.md` + `Dream/INDEX.md`
- reference SPEC-20260506-004 v0.2 / SPEC-20260508-001 v0.3 / SPEC-20260506-005 v0.2 / SPEC-20260507-001 v0.2 / SPEC-20260507-002 v0.3 / SPEC-20260508-002 by section / Delta / line anchor; do NOT modify any of them
- reference `Dream/paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v2.1 §Conflict Resolution Rules CR-1..CR-6 by section anchor; do NOT modify
- reference `Dream/planning/COMPOSER_CAPABILITY_DESCRIPTORS.md` + `Dream/planning/DINOV3_C1_INTEGRATION_MEMO.md` + `Dream/planning/NSA_MEMORY_INTEGRATION_MEMO.md` by section anchor; do NOT modify
- reference `Dream/code/dream3r/RECENT_PROGRESS.md` W1-W18 + KITTI smoke L2 = 20.47 for § 4 整体设计 + § 4.8 实证锚点 only; do NOT modify

Not authorized in cycle 038:

- editing `Dream/3R-mix/main.tex` / `references.bib` / `notes/*` (Track B wound down 2026-05-14)
- editing any SPEC file under `Dream/specs/`
- editing any file under `Dream/code/` / `Dream/paradigm/` / `/hdd3/kykt26/code/dream3r/`
- editing `DRAFT_INTERNAL_V1.md` / `DRAFT_EXTERNAL_V1.md` sections other than § 4 (§ 1 + § 2 already complete; § 3 / § 5-§ 9 stay placeholders)
- editing `OUTLINE_V1.md` (cycle 038 § 4 structural revisions, if any surfaced, would be deferred to OUTLINE_V2 in a later cycle per cycle 036 plan §4)
- editing `WORK_RISK_REGISTER.md` (no new proposal-cycle risks expected; if any surfaces, append in cycle 041 §9 风险章节起草时)
- checkpoint download, training, model inference, server actions, ablation runs
- launching any v0.4 spec delta drafting (B1 / B2 / B3 from cycle 035 proposal §5 still proposal-status)
- frontend / navigation work, demo storyboard promotion past `draft`
- retiring any non-finalist track, declaring teacher-demo readiness
- introducing `cycle` / `SPEC-` / `DEC-` / `CR-N` (where N is a literal digit) / `agent` / `skill` / `workflow` / `本地项目` strings into `DRAFT_EXTERNAL_V1.md` § 4 prose, OR raw `Dream3R` into the external draft main text (only 代号 "候选架构 X" / "本研究架构" / 六模块中文化命名 is allowed externally)
- introducing forbidden over-claim phrasings (`证明.{0,10}优于` / `最佳.{0,5}架构` / `最终.{0,5}架构` / `X 解决了` / `Dream3R 解决了`) into either draft § 4; candidate-not-final language per STYLE_CONTRACT §5 句式对比表 mandatory throughout the architecture description

## Required Boundary

§ 4 研究方案 is **architecture-positioning** text. It describes the candidate architecture (Dream3R v0.3 in internal; 候选架构 X in external) at the research-plan level, not at the spec / implementation level. It does NOT:

- promote Dream3R from candidate to finalist (DEC-20260501-011 candidate-not-final remains in force; the architecture description must remain compatible with "X 是当前迭代的候选; 后续版本可能修订或替换" framing)
- collapse the 4 finalist mechanisms (Critic / Memory / Permanence / Composer) into a single one (DEC-20260504-002 no-all-in remains in force; the 6-module description must preserve each finalist's independence)
- start any v0.4 spec delta drafting (the architecture description must reflect v0.3 state; B1 / B2 / B3 v0.4 candidates from cycle 035 proposal §5 appear as forward-looking 候选 only, not as locked architecture)
- start any server / ablation / calibration run (F-002 remains in force; cycle 038 is markdown-only)
- modify the W19-W30 roadmap (the cycle 035 proposal §6 W-task reorder is still recommendation-status; § 8 时间安排 in cycle 040 will revisit, not cycle 038)
- claim architecture-level superiority over comparator methods on any specific metric

The reuse of SPEC-20260506-004 v0.2 / SPEC-20260508-001 v0.3 / CROSS_SPEC_SIGNAL_CONTRACT v2.1 content is by paraphrase + structural reorganization into the 开题报告 §4 narrative; no verbatim copy of spec paragraphs. Where the spec already defines a module (e.g., "C2 Memory NSA three-branch"), the proposal § 4 may state the same with a parallel paraphrase, but the proposal must own the framing (i.e., must explain why this design choice matters for the proposal's three research questions Q1/Q2/Q3 introduced in § 1.4).

## Output Interpretation

If cycle 038 closes cleanly, the strongest allowed claim is:

```text
Cycle 038 lands § 4 研究方案 / Dream3R v0.3 架构 in both
DRAFT_INTERNAL_V1.md (~4000 字) and DRAFT_EXTERNAL_V1.md (~3000 字),
covering 8 sub-sections: 整体设计 + 帧预算 / C1 感知模块 / C2 记忆
模块 / C3 永久性模块 / C4 校验模块 / C5 编排模块 / C6 总线模块 /
与现有 3R 系统的结构差异. The deliverables are architecture-
positioning text at research-plan level; no spec change, code
change, calibration run, ablation run, or v0.4 delta drafting has
been validated by cycle 038. The candidate-not-final framing is
preserved throughout. The bilingual sync contract (STYLE_CONTRACT
§3) survives its second major stress test under ~7000 字 of
module-dense synchronized content; the §2 vocab substitution table
is extended with N new rows for newly surfaced module-internal
terminology, recorded in §6 sync log.
```

The following remain unvalidated by cycle 038:

- whether the 8-sub-section breakdown reads naturally to advisor / committee (cycle 041 通稿审查 covers; structural revisions deferred to OUTLINE_V2 if surfaced)
- whether the C1-C6 / 六模块中文化命名 reads naturally in external Chinese academic prose (this is the load test for the STYLE_CONTRACT vocab table)
- whether the § 4.8 与现有 3R 系统的结构差异 prose matches advisor expectation on architecture-novel claims (advisor feedback post-cycle)
- whether the candidate-not-final 句式 contrast 表 needs new entries for architecture-claim language (cycle 038 close + cycle 041 通稿审查 will revisit)
- whether the new vocab substitution rows added in cycle 038 are stable enough to carry into § 5 / § 7 / § 8 (cycle 039-040 drafting will exercise; if rows need revision, they are revised in §6 sync log not silently)

## Stop Gates

| Gate | Pass criterion |
|---|---|
| G0 authorization | this DEC accepted; scope matches the approved direction (DEC-20260516-002 §Next Direction option A); explicit allowed / not-authorized lists present |
| G1 path setup | only the 8 paths listed in §Decision receive content (`DRAFT_INTERNAL_V1.md` § 4 only / `DRAFT_EXTERNAL_V1.md` § 4 only / `STYLE_CONTRACT.md` §2 + §6 appends only / this DEC / `CYCLE-20260516-003.md` / 3 sync targets); specifically NOT touched: `Dream/3R-mix/*`, `Dream/specs/*`, `Dream/code/*`, `Dream/paradigm/*`, `/hdd3/kykt26/*`, `OUTLINE_V1.md`, `WORK_RISK_REGISTER.md` |
| G2 vocab firewall (Track B side) | n/a; cycle 036 G2 verification stands |
| G3a vocab firewall (external proposal forbidden patterns) | `Grep` on full `DRAFT_EXTERNAL_V1.md` for pattern `cycle\|SPEC-\|DEC-\|CR-N\|agent\|skill\|workflow\|本地项目` returns 0 hits (covers § 1 + § 2 + new § 4) |
| G3b vocab firewall (external Dream3R case-insensitive) | `Grep -i` on full `DRAFT_EXTERNAL_V1.md` for `Dream3R` returns 0 hits |
| G4 candidate-not-final language | `Grep` on full `DRAFT_EXTERNAL_V1.md` + full `DRAFT_INTERNAL_V1.md` for over-claim patterns `证明.{0,10}优于\|最佳.{0,5}架构\|最终.{0,5}架构\|X 解决了\|Dream3R 解决了` returns 0 hits on both |
| G5 outputs and traceability | DRAFT_INTERNAL_V1.md § 4 body present (~4000 字, within ±20% of estimate); DRAFT_EXTERNAL_V1.md § 4 body present (~3000 字, within ±20%); 8 sub-sections + intro + closing paragraph all in place; § 4 architecture素材 traceable to SPEC-20260506-004 v0.2 Deltas 1-6 + SPEC-20260508-001 v0.3 + CROSS_SPEC_SIGNAL_CONTRACT v2.1 CR-1..CR-6 + COMPOSER_CAPABILITY_DESCRIPTORS + DINOV3_C1_INTEGRATION_MEMO + NSA_MEMORY_INTEGRATION_MEMO; STYLE_CONTRACT §2 vocab table grew by 0+ rows (acceptable: 0 means seed coverage was complete; any added rows recorded in §6 sync log); §6 sync log carries the cycle 038 entry |
| G6 sync chain | `TASK_SNAPSHOT.md` updated first per F-001; `WORKFLOW_STATUS.md` updated; `INDEX.md` updated (cycles row + proposal draft status); cycle log links to this DEC + edited files + sync targets |

Failing any gate → cycle 038 does NOT close; resume from the failing gate.

## Next Direction If Passed

After cycle 038 closes, the next admissible decision is one of:

- A: launch cycle 039 to draft § 3 候选研究问题 + § 6 预期成果与创新点 (per OUTLINE_V1 §4 cycle 039 target — two framing chapters drafted together because problem statement and outcome claim are tightly coupled; ~1500 外 + ~1800 内 字 for § 3, ~1000 外 + ~1300 内 字 for § 6; total ~5600 字)
- B: revise § 4 based on cycle-end self-review or advisor feedback
- C: launch the cycle 035 §Next Direction A-C alternatives (calibration / long-seq ablation / v0.4 spec delta drafting)
- D: pause and reassess after § 4 is on paper
- E: user executes the Track B survey submission action (independent of cycle 038)
- F: return to architecture-first mainline non-proposal work (W22 / W23 / Fast3R omegaconf)

DEC-20260506-001 architecture-first mainline, DEC-20260504-002 no-all-in, DEC-20260501-011 candidate-not-final, DEC-20260503-001 research-code-discipline, DEC-20260515-001 cycle 035 launch, DEC-20260516-001 cycle 036 launch, DEC-20260516-002 cycle 037 launch, F-001 anti-32MB, F-002 server-side discipline all remain in force unchanged.
