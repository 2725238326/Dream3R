# DEC-20260516-001: Cycle 036 survey advisor submission packaging + Dream3R proposal dual-draft kickoff

Status: accepted

Date: 2026-05-16

Cycle: 036

Decision type: bounded markdown deliverable execution (dual scope: Track B survey advisor-submission packaging + Track A Dream3R proposal dual-draft kickoff)

Authorized trigger: user 2026-05-16 message "综述我们得提交了，然后得开始搞 Dream3R 的开题报告了" + four AskUserQuestion answers locking the cycle scope (survey 提交目标 = 给导师/学校审阅; 开题报告受众 = 比导师 1-on-1 稍正式但比院系开题答辩松; 开题报告语言/篇幅 = 中文 / 中等篇幅 10-30 页; 开题报告与现有 Dream/ 工件关系 = 双稿 Dream-vocabulary 内部稿 + 学术语言外部稿; 外部稿 Dream3R 命名 = 代号 "候选架构 X" / "本研究架构") + user "推进吧" plan approval at the EnterPlanMode → ExitPlanMode gate.

## Decision

Proceed with cycle 036 to land the following 13 markdown artifacts in a single bounded session:

Part A — Track B survey advisor-submission packaging (3 files in `Dream/3R-mix/deliverables/`):

1. `SUBMISSION_PACKAGE_ADVISOR_2026-05-16.md` — Chinese cover note (~600 字), 100% vocabulary-clean (no `Dream` / `Dream3R` / `Track A` / `KYKT` / `agent` / `skill` / `workflow` / `本地项目` / `cycle` / `SPEC-` / `DEC-` / `CR-` strings)
2. `SUBMISSION_RECORD_2026-05-16.md` — submission metadata + recipient/channel/SHA256 slots (~150 字)
3. `RELATION_TO_TRACK_A_2026-05-16.md` — internal meta on the Track B / Track A relationship (~600 字); not delivered to advisor; the only escape valve allowed to mention Dream-vocabulary in this cycle's Track B-side outputs

Part B — Dream3R proposal dual-draft kickoff (4 files under new subdirectory `Dream/planning/proposal_dream3r/`):

4. `OUTLINE_V1.md` — 9-section dual outline + chapter mapping table + 字数 estimate + cycle 037+ drafting order
5. `STYLE_CONTRACT.md` — vocabulary substitution table + bilingual sync rule (internal-is-master + periodic external snapshot) + candidate-architecture-X naming introduction rule + candidate-not-final 句式 contrast table
6. `DRAFT_INTERNAL_V1.md` — Dream-vocabulary 内部稿; only § 1 complete (~1000 字) + § 2-§ 9 placeholder
7. `DRAFT_EXTERNAL_V1.md` — academic-Chinese 外部稿; only § 1 complete (~1000 字) + § 2-§ 9 placeholder; uses 代号 "候选架构 X" / "本研究架构"; no raw "Dream3R" in main text

Part C — Authorization + cycle log + risk register + sync chain (6 file ops):

8. This DEC (cycle 036 authorization root)
9. `Dream/cycles/CYCLE-20260516-001.md` — cycle 036 log
10. `Dream/planning/WORK_RISK_REGISTER.md` — v1.1 → v1.2 additive (+3 rows: R-PROP-VOCAB-1 / R-PROP-CLAIM-1 / R-PROP-SYNC-1)
11. `Dream/TASK_SNAPSHOT.md` — sync first per F-001
12. `Dream/WORKFLOW_STATUS.md` — Last updated + cycle logs row + Recommended Next User Decision refresh
13. `Dream/INDEX.md` — new `planning/proposal_dream3r/` subsection (4 entries) + `3R-mix/deliverables/` updated (+3 entries) + `cycles/` (+1 entry) + Q&A latest pointer

## Scope

Allowed in cycle 036:

- create the 9 new files listed above (3 in `Dream/3R-mix/deliverables/`, 4 in `Dream/planning/proposal_dream3r/`, 1 DEC, 1 cycle log)
- modify the 4 sync targets listed above (`WORK_RISK_REGISTER.md` v1.1 → v1.2 additive, `TASK_SNAPSHOT.md`, `WORKFLOW_STATUS.md`, `INDEX.md`)
- compute PDF SHA256 via PowerShell `Get-FileHash` (read-only) for the SUBMISSION_RECORD slot, if user invokes; otherwise leave the slot as `__<runtime fill>__`
- run `Grep` vocabulary-firewall verification on `SUBMISSION_PACKAGE_ADVISOR_2026-05-16.md` and `DRAFT_EXTERNAL_V1.md` § 1 prose (read-only)
- reference SPEC-20260506-004 v0.2 / SPEC-20260506-005 v0.2 / SPEC-20260507-001 v0.2 / SPEC-20260507-002 v0.3 / SPEC-20260508-001 v0.3 / SPEC-20260508-002 / DEC-20260506-001 / DEC-20260504-002 / DEC-20260501-011 / DEC-20260503-001 / DEC-20260515-001 / `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v2.1 / `code/dream3r/RECENT_PROGRESS.md` / `code/dream3r/NEXT_PHASE_ROADMAP.md` by section / line / ID anchor; do NOT modify any of them

Not authorized in cycle 036:

- editing any file under `Dream/3R-mix/` other than the 3 new files in `deliverables/` (no `main.tex` / `references.bib` / `notes/*` edits; Track B was wound down 2026-05-14 to route C arXiv-only and stays wound down)
- editing any SPEC file under `Dream/specs/`
- editing any file under `Dream/code/` (including `RECENT_PROGRESS.md` / `NEXT_PHASE_ROADMAP.md` / `REVIEW_PROMPT.md`)
- editing any file under `/hdd3/kykt26/code/dream3r/`
- editing any paradigm file (`CROSS_SPEC_SIGNAL_CONTRACT.md` / `RESEARCH_CODE_DISCIPLINE.md` / `TEACHER_AUDIENCE_PROFILE.md`)
- drafting § 2 through § 9 body text in either DRAFT_INTERNAL_V1.md or DRAFT_EXTERNAL_V1.md (placeholders only this cycle; § 1 is the alignment proof)
- importing CUT3R / Spann3R / Dream3R / server model runtime code
- checkpoint download or checkpoint use
- training or fine-tuning
- real model inference
- running `evaluate_real_sequence.py` or any other server-side execution
- running ABL-v02-1..9 / ABL-memory-1..11 / `ablate_recurrence` on KITTI long windows / any other ablation
- frontend or navigation work
- promoting any demo storyboard past `draft`
- paper claim promotion past current proposal-draft status
- launching any v0.4 spec delta drafting cycle (B1 Critic path split / B2 output asset contract / B3 input extension axis from cycle 035 proposal §5 remain proposal-status only; each requires its own DEC)
- retiring any non-finalist track
- declaring teacher-demo readiness
- introducing any of `Dream` / `Dream3R` / `Track A` / `KYKT` / `agent` / `skill` / `workflow` / `本地项目` / `cycle` / `SPEC-` / `DEC-` / `CR-` strings into `Dream/3R-mix/deliverables/SUBMISSION_PACKAGE_ADVISOR_2026-05-16.md` (cover note must remain Track-B-vocabulary-clean per the 2026-05-14 wound-down posture)
- introducing `cycle` / `SPEC-` / `DEC-` / `CR-N` / `agent` / `skill` / `workflow` / `本地项目` strings into `DRAFT_EXTERNAL_V1.md` § 1 prose, OR introducing a raw `Dream3R` string into `DRAFT_EXTERNAL_V1.md` § 1 main text (only the 代号 "候选架构 X" / "本研究架构" naming is allowed externally)

## Required Boundary

The 4 new files in `Dream/planning/proposal_dream3r/` are **planning + drafting artifacts only**. None of them by itself authorizes:

- promoting Dream3R from candidate to finalist (DEC-20260501-011 candidate-not-final remains in force)
- collapsing the 4 finalist mechanisms into a single one (DEC-20260504-002 no-all-in remains in force)
- starting any v0.4 spec delta drafting (B1 / B2 / B3 each require their own DEC)
- starting any server / ablation / calibration run (F-002 + DEC-20260515-001 §Not authorized remain in force)
- changing the architecture-first mainline framing (DEC-20260506-001 remains in force)
- modifying the W19-W30 roadmap in `code/dream3r/NEXT_PHASE_ROADMAP.md` (the cycle 035 proposal §6 W-task reorder is still recommendation-status; actual roadmap updates need their own DEC)

The 3 new files in `Dream/3R-mix/deliverables/` are **submission packaging artifacts only**, not authorization to perform the actual submission. The user executes the actual submission action (email / IM / portal / offline) outside this cycle and fills the `SUBMISSION_RECORD_2026-05-16.md` slots at that time.

The proposal upstream (`planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md`) status remains `draft, awaiting user review` until and unless a separate DEC formally accepts it as a v0.4 design input. Cycle 036's proposal_dream3r/ deliverables draw on the proposal as planning input, not as ratified spec input.

## Output Interpretation

If cycle 036 closes cleanly, the strongest allowed claim is:

```text
Cycle 036 lands six markdown artifacts that (a) package the 2026-05-15
3R-mix Chinese survey for advisor/school internal review (cover note +
submission record + Track-A relationship meta), and (b) launch a
Chinese Dream3R proposal dual-draft scaffold (9-section outline +
chapter mapping + bilingual style contract + § 1 complete draft pair as
style-and-vocabulary alignment proof). The deliverables are packaging
+ planning + § 1 evidence; no actual survey submission has been
performed, no § 2 through § 9 proposal body text has been drafted, no
spec change, code change, calibration run, or ablation run has been
validated.
```

The following remain unvalidated by cycle 036:

- whether the advisor / school accepts the survey under the route C arXiv-only posture (advisor review feedback is post-cycle)
- whether the dual-draft 9-section outline survives advisor / committee critique (cycle 037+ may revise)
- whether the candidate-architecture-X 代号 strategy reads naturally to an academic Chinese audience (only § 1 sample is in scope this cycle)
- whether the bilingual sync rule (internal-is-master + periodic external snapshot) holds up under § 2-§ 9 scaling (real stress test starts cycle 037)
- whether 候选架构 X / 本研究架构 should propagate into the actual Dream3R published paper (separate decision; not in this cycle's scope)

## Stop Gates

| Gate | Pass criterion |
|---|---|
| G0 authorization | this DEC accepted; scope matches the approved plan; explicit allowed/not-authorized lists present |
| G1 path setup | only the 13 paths listed in §Decision receive content; specifically NOT touched: `Dream/3R-mix/main.tex` / `Dream/3R-mix/references.bib` / `Dream/3R-mix/notes/*`; `Dream/specs/*`; `Dream/code/*`; `Dream/paradigm/*`; `/hdd3/kykt26/*` |
| G2 vocab firewall (Track B side) | `Grep` on `SUBMISSION_PACKAGE_ADVISOR_2026-05-16.md` for pattern `Dream\|Dream3R\|KYKT\|agent\|skill\|workflow\|本地项目\|cycle\|SPEC-\|DEC-\|CR-` returns 0 hits. (`RELATION_TO_TRACK_A_2026-05-16.md` is exempt — that file is the internal escape valve.) |
| G3 vocab firewall (external proposal draft side) | `Grep` on `DRAFT_EXTERNAL_V1.md` § 1 prose for pattern `cycle\|SPEC-\|DEC-\|CR-N\|agent\|skill\|workflow\|本地项目` returns 0 hits AND `Grep` for raw `Dream3R` (case-insensitive) in § 1 main text returns 0 hits (references region exempt if any). `DRAFT_INTERNAL_V1.md` is unconstrained on this gate. |
| G4 candidate-not-final language | `Grep` on `DRAFT_EXTERNAL_V1.md` § 1 + `DRAFT_INTERNAL_V1.md` § 1 for over-claim patterns (`证明.*优于` / `最佳.*架构` / `最终.*架构` / `X 解决了`) returns 0 hits. Allowed phrasing: `评估.*是否`, `X 是被评估的候选`, `X 的设计目标包括`, `候选方案`, etc. |
| G5 outputs and traceability | all 13 file ops complete; `OUTLINE_V1.md` chapter mapping table cites Track B 综述 sections + Dream specs + planning artifacts feeding each 开题报告 section; `STYLE_CONTRACT.md` carries vocabulary substitution table with at least 12 rows; 3 new risk rows present in `WORK_RISK_REGISTER.md` v1.2 with explicit Source / Trigger / Status / Owner |
| G6 sync chain | `TASK_SNAPSHOT.md` updated first per F-001; `WORKFLOW_STATUS.md` updated; `INDEX.md` updated with new `planning/proposal_dream3r/` subsection + `3R-mix/deliverables/` row count update + `cycles/` +1 row + Q&A "latest research result" pointer; cycle log links to this DEC + 9 new files + 3 risk rows + 4 sync targets |

Failing any gate → cycle 036 does NOT close; resume from the failing gate.

## Next Direction If Passed

After cycle 036 closes, the next admissible decision is one of:

- A: launch cycle 037 to draft § 2 国内外研究现状 (recommended starting point because § 2 is the largest single-section block and most heavily reuses Track B 综述 material; double-draft sync stress-tests the STYLE_CONTRACT immediately)
- B: user executes the actual survey submission action (email / IM / portal / offline) and fills the `SUBMISSION_RECORD_2026-05-16.md` slots; this is a manual action outside any cycle
- C: revise `OUTLINE_V1.md` chapter structure (e.g., merge / split sections, reorder, change 字数 distribution) before launching cycle 037
- D: pause and revise the cycle 036 deliverables based on quality review
- E: return to architecture-first mainline non-proposal work (W22 visualization pack / W23 expert adapter loading prerequisites / Fast3R `omegaconf` resolution per cycle 035 §Next Direction option D)
- F: launch one of the cycle 035 §Next Direction options A-C (calibration run / long-seq ablation / v0.4 spec delta) instead; cycle 036 close does not preempt those candidates

DEC-20260506-001 architecture-first mainline, DEC-20260504-002 no-all-in, DEC-20260501-011 thesis reframe candidate-not-final, DEC-20260503-001 research-code-discipline, DEC-20260515-001 cycle 035 launch + boundary, F-001 anti-32MB, F-002 server-side discipline all remain in force unchanged.
