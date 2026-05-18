# DEC-20260517-002: Cycle 041 Dream3R proposal § 9 风险分析 + 通稿审查 + STYLE_CONTRACT final sync

Status: accepted

Date: 2026-05-17

Cycle: 041

Decision type: bounded markdown deliverable execution (single scope: cycle 041 § 9 风险分析与应对 dual-draft drafting + full-document consistency review + STYLE_CONTRACT final sync)

Authorized trigger: user 2026-05-17 handoff prompt requesting cycle 041 launch per DEC-20260517-001 §Next Direction If Passed option A; cycle 040 was closed earlier the same session with 8 file ops + G0-G6 all passing (5 corrective edits at G3a + G3b).

## Decision

Proceed with cycle 041 to draft § 9 in both drafts + run full-document consistency review across § 1-§ 9 + finalize STYLE_CONTRACT vocab table and sync log.

### § 9 风险分析与应对 (6 sub-sections per handoff prompt mapping)

1. § 9.1 架构层风险 (per-spec 风险: Critic 标定缺口 / Memory 校准精度 / Permanence 静态写入覆盖 / Composer 零 spread fail-fast / 总线信号契约漂移)
2. § 9.2 跨模块风险 (cycle 035 v1.1 +4: R-OOD-1 / R-EXT-PRIOR-1 / R-4DGS-LIC-1 / R-INPUT-EXT-1)
3. § 9.3 实证执行风险 (KITTI 集成证据 vs 训练后质量 boundary + ABL 计划 plan-only F-002 gate + 数据集 license)
4. § 9.4 工程时序风险 (W19-W30 timeline + B1/B2/B3 v0.4 spec delta 候选 + 3DGS license)
5. § 9.5 开题报告 process 风险 (cycle 036 v1.2 +3: R-PROP-VOCAB-1 vocab 泄漏 / R-PROP-CLAIM-1 over-claim / R-PROP-SYNC-1 双稿语义漂移)
6. § 9.6 风险应对策略 (per-risk mitigation 表 + 整体优先级 + 监控机制)

Target word count per OUTLINE_V1.md § 2 表:

- 外部稿 § 9 ~1000 字
- 内部稿 § 9 ~1500 字

Tolerance ±20%.

Order of operation: internal first (master), then external snapshot per STYLE_CONTRACT § 3 规则 1.

### 通稿审查 scope

Per cycle 040 cycle log §What remains unvalidated + cycle 039 Observation §G4:

- § 7.3 KITTI L2=20.4747 + "集成证据" 限定语 advisor-readability check
- § 5 评测协议 "plan-only" 标注 sufficiency check
- § 8 M3-M5 timeline candidate-vs-committed framing check
- § 3.5 + § 6.2 + § 6.3 candidate-not-final 措辞 advisor-readability check
- § 7.6 cycle 历史 中编号密度 check
- vocab 表 48 行覆盖 § 9 check; 可能 +2-3 行

## Scope

Allowed in cycle 041:

- edit `Dream/planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` to replace § 9 placeholder with body text (~1500 字, 6 sub-sections)
- edit `Dream/planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md` similarly with vocabulary-clean snapshot (~1000 字, 4-6 selected risks)
- edit `Dream/planning/proposal_dream3r/STYLE_CONTRACT.md` § 2 vocab substitution table (append 2-3 new rows for risk vocabulary) + § 6 sync log (cycle 041 entry) + 授权根 metadata
- update both drafts' top metadata blocks (Last updated + 状态 fields)
- surgical edits to § 1-§ 8 in either draft if 通稿审查 surfaces genuine inconsistency (each surgical edit recorded in cycle log)
- create this DEC
- create `Dream/cycles/CYCLE-20260517-002.md` (cycle 041 log)
- update `Dream/TASK_SNAPSHOT.md` (sync first per F-001) + `Dream/WORKFLOW_STATUS.md` + `Dream/INDEX.md`

Not authorized in cycle 041:

- editing `Dream/3R-mix/main.tex` / `references.bib` / `notes/*` (Track B wound down)
- editing any SPEC file under `Dream/specs/` / code under `Dream/code/` / paradigm under `Dream/paradigm/` / `/hdd3/kykt26/*`
- editing `OUTLINE_V1.md` / `WORK_RISK_REGISTER.md`
- server actions, checkpoint download, training, calibration runs, ablation runs
- v0.4 spec delta drafting (B1/B2/B3)
- introducing `cycle` / `SPEC-` / `DEC-` / `CR-N` / `agent` / `skill` / `workflow` / `本地项目` strings or raw `Dream3R` into `DRAFT_EXTERNAL_V1.md`
- introducing forbidden over-claim phrasings into either draft § 9
- over-claiming risk mitigation as fully resolved (per RESEARCH_CODE_DISCIPLINE rule 5 Honesty Override; use "缓解措施 ... 残余风险" framing)

## Required Boundary

§ 9 is the risk-analysis chapter. It paraphrases WORK_RISK_REGISTER v1.2 17 rows into academic prose. It does NOT:

- modify the risk register itself (read-only reference)
- claim any risk is fully resolved (per RESEARCH_CODE_DISCIPLINE rule 5 Honesty Override)
- introduce new risks not traceable to the register (paraphrase + regroup only)
- start any server / ablation / calibration run
- modify any spec / code / paradigm file

## Output Interpretation

If cycle 041 closes cleanly, the strongest allowed claim is:

```text
Cycle 041 lands § 9 风险分析与应对 in both DRAFT_INTERNAL_V1.md (~1500 字)
and DRAFT_EXTERNAL_V1.md (~1000 字). § 9 covers 6 sub-sections (架构层风险 /
跨模块风险 / 实证执行风险 / 工程时序风险 / 开题报告 process 风险 / 风险应对
策略). Full-document consistency review completed across § 1-§ 9.
STYLE_CONTRACT § 2 vocab table grew from 48 to 50-51 rows. § 1-§ 9 累计
~19300 内 + ~15000 外 字 ≈ 92-95% of OUTLINE_V1 § 2 表 总字数估算.
All 9 sections of the dual-draft are now complete; ready for cycle 042
最终修订 + PDF 编译 + advisor submission packaging.
```

## Stop Gates

| Gate | Pass criterion |
|---|---|
| G0 authorization | this DEC accepted; scope matches DEC-20260517-001 §Next Direction option A |
| G1 path setup | only the 8 paths listed receive content; NOT touched: `Dream/3R-mix/*`, `Dream/specs/*`, `Dream/code/*`, `Dream/paradigm/*`, `/hdd3/kykt26/*`, `OUTLINE_V1.md`, `WORK_RISK_REGISTER.md`; § 1-§ 8 only surgical edits if 通稿审查 surfaces genuine inconsistency |
| G2 vocab firewall (Track B side) | n/a; cycle 036 G2 stands |
| G3a vocab firewall (external forbidden patterns) | `Grep` on full `DRAFT_EXTERNAL_V1.md` for `cycle\|SPEC-\|DEC-\|CR-[0-9]\|agent\|skill\|workflow\|本地项目` returns 0 hits |
| G3b vocab firewall (external Dream3R) | `Grep -i` on full `DRAFT_EXTERNAL_V1.md` for `Dream3R` returns 0 hits |
| G4 candidate-not-final | `Grep` on both full drafts for `证明.{0,10}优于\|最佳.{0,5}架构\|最终.{0,5}架构\|X 解决了\|Dream3R 解决了` returns 0 hits on both |
| G5 outputs + traceability | § 9 body present in both drafts within ±20% target; 6 sub-sections + intros + closing in place; STYLE_CONTRACT 48→50-51 rows; § 9 traceable to WORK_RISK_REGISTER v1.2 |
| G6 sync chain | TASK_SNAPSHOT updated first per F-001; WORKFLOW_STATUS + INDEX updated; cycle log links DEC + edited files + sync targets |

## Next Direction If Passed

After cycle 041 closes, the next admissible decision is one of:

- A: launch cycle 042 最终修订 + PDF 编译 + advisor submission packaging (per OUTLINE_V1 § 4 cycle 042 target)
- B: revise § 9 based on self-review or advisor feedback
- C: cycle 035 §Next Direction A-C alternatives (calibration / long-seq ablation / v0.4 spec delta drafting)
- D: pause + reassess after full dual-draft quality review
- E: user executes Track B survey submission (manual action)
- F: return to architecture-first mainline non-proposal work (W22 / W23 / Fast3R omegaconf)

DEC-20260506-001 architecture-first mainline, DEC-20260504-002 no-all-in, DEC-20260501-011 candidate-not-final, DEC-20260503-001 research-code-discipline, DEC-20260515-001 cycle 035 launch, DEC-20260516-001..004 cycles 036-039, DEC-20260517-001 cycle 040, F-001 anti-32MB, F-002 server-side discipline all remain in force unchanged.
