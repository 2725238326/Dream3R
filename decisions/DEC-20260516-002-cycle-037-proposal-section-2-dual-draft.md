# DEC-20260516-002: Cycle 037 Dream3R proposal § 2 国内外研究现状 dual-draft drafting

Status: accepted

Date: 2026-05-16

Cycle: 037

Decision type: bounded markdown deliverable execution (single scope: cycle 037 § 2 国内外研究现状 dual-draft drafting in `planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` and `planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md`)

Authorized trigger: user 2026-05-16 message "你好好推进吧" approving the cycle 037 launch as the recommended next direction per DEC-20260516-001 §Next Direction If Passed option A; cycle 036 was just closed earlier in the same session with all 13 file ops + stop gates G0-G6 passing.

## Decision

Proceed with cycle 037 to draft § 2 国内外研究现状 in both DRAFT_INTERNAL_V1.md (master, Dream-vocabulary) and DRAFT_EXTERNAL_V1.md (snapshot, vocabulary-clean using 代号 "候选架构 X" / "本研究架构"). § 2 covers the seven sub-sections proposed in `OUTLINE_V1.md` §2 子节建议:

1. § 2.1 基础谱系 (DUSt3R / MASt3R / MASt3R-SfM 系)
2. § 2.2 多视角规模化与统一视觉几何 (Fast3R / MV-DUSt3R+ / VGGT / MapAnything / Pow3R)
3. § 2.3 视频、动态场景与 4D 重建 (Align3R / MonST3R / POMATO / D²USt3R / Easi3R / RayMap3R)
4. § 2.4 长序列重建中的状态、记忆与缓存四类机制 (递推状态 / 空间指针 / 混合记忆 / 缓存治理)
5. § 2.5 测试时验证、修正与先验输入三类机制 (一致性优化 / 测试时参数更新 / 先验注入)
6. § 2.6 从几何预测到可查看输出三类资产 (4D pointmap / dynamic mask / 4DGS)
7. § 2.7 综述四轴覆盖矩阵 + 本研究架构 / Dream3R v0.3 落点

Target word count per `OUTLINE_V1.md` §2 表: 外部稿 ~3500 字, 内部稿 ~4000 字; tolerance ±20%.

Order of operation: internal first (master), then external snapshot per STYLE_CONTRACT §3 规则 1. Vocabulary firewall + over-claim greps run on external draft after each major sub-section lands.

## Scope

Allowed in cycle 037:

- edit `Dream/planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` to replace the `<!-- TBD cycle 037 -->` placeholder with § 2 body text (7 sub-sections + section intro + closing 落点 paragraph)
- edit `Dream/planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md` similarly with vocabulary-clean snapshot of the same § 2 content
- edit `Dream/planning/proposal_dream3r/STYLE_CONTRACT.md` §6 sync log to append the cycle 037 sync entry (cycle / section / sync direction / vocab substitutions used / vocab-grep verification result)
- edit `Dream/planning/proposal_dream3r/STYLE_CONTRACT.md` §2 vocabulary substitution table to append new entries surfaced during § 2 drafting (e.g., new model names, dataset names, technical terms not already in the seed table); only additions, no removals
- run `Grep` G3 vocabulary-firewall + G4 over-claim verifications on `DRAFT_EXTERNAL_V1.md` (read-only)
- create `Dream/decisions/DEC-20260516-002-cycle-037-proposal-section-2-dual-draft.md` (this file; cycle 037 authorization root)
- create `Dream/cycles/CYCLE-20260516-002.md` (cycle 037 log)
- update `Dream/TASK_SNAPSHOT.md` (sync first per F-001) + `Dream/WORKFLOW_STATUS.md` + `Dream/INDEX.md`
- reference Track B survey `Dream/3R-mix/main.tex` §1-§10 + 5 tables + 6 figures + 44 references + `Dream/planning/SOTA_MATRIX_V2.md` + `Dream/specs/SPEC-20260507-001-dream3r-comparator-map-v02.md` by section / line / ID anchor; do NOT modify any of them
- reference `Dream/code/dream3r/RECENT_PROGRESS.md` only for § 2.7 内稿独占 Dream3R 落点 content (Dream3R v0.3 architecture's response to the four-axis findings); not modified

Not authorized in cycle 037:

- editing `Dream/3R-mix/main.tex` / `references.bib` / `notes/*` (Track B wound down 2026-05-14 to route C arXiv-only)
- editing any SPEC file under `Dream/specs/`
- editing any file under `Dream/code/` / `Dream/paradigm/` / `/hdd3/kykt26/code/dream3r/`
- editing `DRAFT_INTERNAL_V1.md` / `DRAFT_EXTERNAL_V1.md` sections other than § 2 (§ 1 was completed cycle 036; § 3-§ 9 stay as placeholders for cycles 038-041)
- editing `OUTLINE_V1.md` § 2 章节 estimates (if cycle 037 surfaces structural revisions, OUTLINE_V1 is preserved and OUTLINE_V2 created in a later cycle per cycle 036 plan §4 关键 cycle 037 决策点)
- checkpoint download, training, model inference, server actions
- running ABL-v02-1..9 / ABL-memory-1..11 / `ablate_recurrence` / `evaluate_real_sequence.py` / any other server execution
- frontend / navigation work, demo storyboard promotion past `draft`
- launching any v0.4 spec delta drafting (B1 / B2 / B3 from cycle 035 proposal §5 still proposal-status; each requires its own DEC)
- retiring any non-finalist track or declaring teacher-demo readiness
- introducing `cycle` / `SPEC-` / `DEC-` / `CR-N` / `agent` / `skill` / `workflow` / `本地项目` strings into `DRAFT_EXTERNAL_V1.md` § 2 prose, OR raw `Dream3R` into the external draft main text (only 代号 "候选架构 X" / "本研究架构" naming is allowed externally)
- introducing forbidden over-claim phrasings (`证明.{0,10}优于` / `最佳.{0,5}架构` / `最终.{0,5}架构` / `X 解决了` / `Dream3R 解决了`) into either draft § 2; candidate-not-final language per STYLE_CONTRACT §5 句式对比表 mandatory

## Required Boundary

§ 2 国内外研究现状 is **research positioning** text. It positions the wider 3R literature into a coverage matrix and then describes where 候选架构 X / Dream3R v0.3 sits in that matrix as a candidate response. It does NOT:

- promote Dream3R from candidate to finalist (DEC-20260501-011 candidate-not-final remains in force)
- collapse the 4 finalist mechanisms into a single one (DEC-20260504-002 no-all-in remains in force)
- start any v0.4 spec delta drafting (B1 / B2 / B3 each require their own DEC)
- start any server / ablation / calibration run (F-002 remains in force)
- modify the W19-W30 roadmap or any of the Dream specs / paradigm files
- claim superiority over comparator methods on any specific metric

The reuse of Track B survey content is by paraphrase + structural reorganization into the 开题报告 §2 narrative; no verbatim copy of survey paragraphs. Where the survey already states a fact (e.g., "DUSt3R 把图像对映射到稠密三维点图"), the proposal § 2 may state the same fact with a parallel paraphrase, but the proposal must own the framing (i.e., must explain why this fact matters for the proposal's three research questions Q1/Q2/Q3 introduced in § 1.4).

## Output Interpretation

If cycle 037 closes cleanly, the strongest allowed claim is:

```text
Cycle 037 lands § 2 国内外研究现状 in both DRAFT_INTERNAL_V1.md
(~4000 字) and DRAFT_EXTERNAL_V1.md (~3500 字), covering seven
sub-sections from foundational lineage through multi-view scaling,
dynamic 4D, long-sequence memory, test-time mechanisms, output
assets, and a four-axis coverage matrix that positions 候选架构 X /
Dream3R v0.3 as a candidate response. The deliverables are research
positioning text; no spec change, code change, calibration run, or
ablation run has been validated by cycle 037. The bilingual sync
contract (STYLE_CONTRACT §3) has its first real stress test under
~7500 字 of synchronized content; the sync log records the
substitutions used.
```

The following remain unvalidated by cycle 037:

- whether the seven-sub-section breakdown reads naturally as a Chinese 研究现状 chapter, or whether advisor / committee will request restructuring (cycle 041 通稿审查 covers; if needed, OUTLINE_V2 created in a later cycle)
- whether the four-axis coverage matrix (§ 2.7) needs to be a table vs prose (cycle 037 default: prose with embedded short list; can be promoted to a booktabs table in cycle 042 final revision if needed)
- whether the § 2.7 Dream3R 落点 wording (in 内部稿) and 候选架构 X 落点 wording (in 外部稿) match advisor expectation on candidate-not-final framing (advisor review feedback post-cycle)
- whether any of the surfaced new vocabulary substitutions (e.g., new model names not in the seed table) will require structural changes to the STYLE_CONTRACT (cycle 037 close appends rows but does not reorganize the table)
- whether the W22 visualization pack (Track A architecture-first mainline) should land before or after the proposal draft completes (independent decision; not in cycle 037 scope)

## Stop Gates

| Gate | Pass criterion |
|---|---|
| G0 authorization | this DEC accepted; scope matches the approved direction per DEC-20260516-001 §Next Direction If Passed option A; explicit allowed / not-authorized lists present |
| G1 path setup | only the 6 paths listed in §Decision receive content (`DRAFT_INTERNAL_V1.md` § 2 only / `DRAFT_EXTERNAL_V1.md` § 2 only / `STYLE_CONTRACT.md` §6 sync log + §2 table appends only / this DEC / `CYCLE-20260516-002.md` / 3 sync targets); specifically NOT touched: `Dream/3R-mix/*`, `Dream/specs/*`, `Dream/code/*`, `Dream/paradigm/*`, `/hdd3/kykt26/*`, `OUTLINE_V1.md`, `WORK_RISK_REGISTER.md` |
| G2 vocab firewall (Track B side) | not applicable this cycle (no Track B 3R-mix edits); cycle 036 G2 verification stands |
| G3a vocab firewall (external proposal forbidden patterns) | `Grep` on `DRAFT_EXTERNAL_V1.md` § 2 prose for pattern `cycle\|SPEC-\|DEC-\|CR-N\|agent\|skill\|workflow\|本地项目` returns 0 hits |
| G3b vocab firewall (external proposal Dream3R case-insensitive) | `Grep` for raw `Dream3R` (case-insensitive) in `DRAFT_EXTERNAL_V1.md` main text returns 0 hits (metadata + references regions exempt if any) |
| G4 candidate-not-final language | `Grep` on `DRAFT_EXTERNAL_V1.md` § 2 + `DRAFT_INTERNAL_V1.md` § 2 for over-claim patterns `证明.{0,10}优于\|最佳.{0,5}架构\|最终.{0,5}架构\|X 解决了\|Dream3R 解决了` returns 0 hits |
| G5 outputs and traceability | `DRAFT_INTERNAL_V1.md` § 2 body text replaces the cycle-036 placeholder with seven sub-sections + closing § 2.7 落点 paragraph; `DRAFT_EXTERNAL_V1.md` § 2 mirrors structurally with vocab-clean snapshot; `STYLE_CONTRACT.md` §6 sync log carries the cycle 037 entry with vocab substitutions used + grep verification timestamp; word counts within ±20% of OUTLINE_V1 §2 estimates (~4000 内 / ~3500 外) |
| G6 sync chain | `TASK_SNAPSHOT.md` updated first per F-001; `WORKFLOW_STATUS.md` updated; `INDEX.md` updated (cycle row + proposal draft status if needed); cycle log links to this DEC + 5 edited files + 3 sync targets |

Failing any gate → cycle 037 does NOT close; resume from the failing gate.

## Next Direction If Passed

After cycle 037 closes, the next admissible decision is one of:

- A: launch cycle 038 to draft § 4 研究方案 / Dream3R v0.3 架构 (core technical chapter; ~3000 外 + ~4000 内 字 per OUTLINE_V1 §2 table; per OUTLINE_V1 §4 cycle 038 target)
- B: revise § 2 based on cycle-end self-review or advisor / committee feedback (if any has been received by then)
- C: launch the cycle 035 §Next Direction A-C alternatives (calibration / long-seq ablation / v0.4 spec delta drafting), or DEC-20260516-001 §Next Direction E (architecture-first mainline non-proposal work like W22)
- D: pause and reassess after § 2 is on paper; user reviews the dual-draft alignment and decides whether the bilingual sync rule scales
- E: user executes the Track B survey submission action (independent of cycle 037; can happen at any time per DEC-20260516-001 §Next Direction option B)

DEC-20260506-001 architecture-first mainline, DEC-20260504-002 no-all-in, DEC-20260501-011 candidate-not-final, DEC-20260503-001 research-code-discipline, DEC-20260515-001 cycle 035 launch + boundary, DEC-20260516-001 cycle 036 launch + boundary, F-001 anti-32MB, F-002 server-side discipline all remain in force unchanged.
