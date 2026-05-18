# DEC-20260517-003 — Cycle 042: Dream3R 开题报告最终修订 + PDF 编译 + 提交 packaging

| 字段 | 取值 |
|---|---|
| 决策 ID | DEC-20260517-003 |
| 日期 | 2026-05-17 |
| 触发 | user 2026-05-17 chat "A吧" + DEC-20260517-002 §Next Direction option A |
| 类型 | cycle launch (cycle 042) |
| 前置 | DEC-20260517-002 (cycle 041 closed; §1-§9 全部章节完整; 通稿审查 clean; G3a/G3b/G4 all 0 hits) |
| 关联 | DEC-20260516-001 (cycle 036 launch: dual-draft kickoff + Part A packaging pattern) |

## Decision

Launch cycle 042: Dream3R 开题报告最终修订 + PDF 编译 + advisor 提交 packaging。

This is the final content cycle of the proposal track. It does NOT draft new body text; it polishes, compiles, and packages the existing §1-§9 dual-draft for advisor delivery.

## Scope

### Authorized

1. **Bottom metadata cleanup** in DRAFT_INTERNAL_V1.md + DRAFT_EXTERNAL_V1.md — update stale fields (状态 / 当前字数 / 下游 etc.) from cycle 036 scaffold to reflect §1-§9 completion
2. **§8.1 short-term timeline past-tense fix** in both drafts — cycle 040/041 are now past events, cycle 042 is current; update phrasing accordingly
3. **Remove stale bottom sync log** in DRAFT_INTERNAL_V1.md — the single-row sync table at bottom (lines 801-805) is a cycle 036 leftover; STYLE_CONTRACT §6 is the authoritative sync log; remove to avoid confusion
4. **Remove stale "End of DRAFT" footer** in both drafts — lines 824-825 internal / 707-708 external are cycle 036 placeholders no longer accurate
5. **Create `references.bib`** in `planning/proposal_dream3r/` — copy Track B survey's 44 entries as base; the external draft §2 references the same literature pool
6. **PDF compilation** of DRAFT_EXTERNAL_V1.md via `pandoc` + `xelatex` + `ctex` — produce `deliverables/proposal_external_v1_2026-05-17.pdf`; no custom LaTeX template needed; pandoc defaults + CJK font sufficient for advisor review copy
7. **Create `deliverables/SUBMISSION_PACKAGE_ADVISOR_PROPOSAL_2026-05-17.md`** — Chinese cover note (~400-600 字) adapted from cycle 036 Part A pattern; vocab-clean (G3a + G3b verified); 5-6 sections (主旨 / 范围 / 证据边界 / 与综述关系 / 候选 vs 最终声明 / 请求审阅事项)
8. **Create `deliverables/SUBMISSION_RECORD_PROPOSAL_2026-05-17.md`** — submission metadata (recipient / channel / pdf_sha256 slots) adapted from cycle 036 Part A pattern
9. **Final G3a + G3b grep** on cover note + any new deliverable files
10. **Update STYLE_CONTRACT** §6 sync log (cycle 042 entry) + metadata
11. **Create cycle log** CYCLE-20260517-003.md
12. **Sync chain**: TASK_SNAPSHOT → WORKFLOW_STATUS → INDEX

### Not authorized

- Drafting new body text in §1-§9 (content frozen after cycle 041 通稿审查)
- Any edit to OUTLINE_V1.md or WORK_RISK_REGISTER.md
- Figure/table TikZ generation (deferred — advisor review copy does not require embedded figures; figures are a cycle 043+ enhancement if needed)
- Editing `Dream/3R-mix/*` (Track B workspace)
- Editing `Dream/specs/*`, `Dream/code/*`, `Dream/paradigm/*`, `/hdd3/kykt26/*`
- Server actions, training, ablation, calibration runs

### Design Decisions

- **PDF pathway**: `pandoc` markdown → xelatex → PDF. Rationale: simplest pipeline; both tools available (pandoc 3.9 + MiKTeX xelatex); ctex CJK support automatic; no custom template needed for advisor review copy. If compilation fails, fallback to pandoc → wkhtmltopdf or manual .tex wrapper.
- **Figure strategy**: omitted from this cycle. The markdown proposal is text-only. Figures (if needed for formal submission) are cycle 043+ scope. The advisor review copy can be text-only for initial feedback.
- **references.bib**: full copy from Track B. The external draft §2 cites the same 44 literature entries. No filtering needed; unused entries are harmless in bib.
- **Deliverables directory**: create `planning/proposal_dream3r/deliverables/` to mirror Track B pattern.

## Stop Gates

| Gate | Check |
|---|---|
| G0 authorization | This DEC accepted by user ("A吧") |
| G1 path | Only authorized paths modified; no spec / code / paradigm / OUTLINE / RISK_REGISTER |
| G3a vocab firewall | grep on cover note + submission record: 0 hits on `cycle\|SPEC-\|DEC-\|CR-[0-9]\|agent\|skill\|workflow\|本地项目` |
| G3b Dream3R firewall | grep -i `Dream3R` on cover note: 0 hits |
| G5 PDF compilation | pandoc exit code 0; PDF file exists + non-zero size |
| G6 sync chain | TASK_SNAPSHOT + WORKFLOW_STATUS + INDEX all updated |

## Next Direction If Passed

- A. User reviews advisor copy and provides feedback → revision cycle 043
- B. User executes actual submission action (email / IM / portal / offline) and fills SUBMISSION_RECORD slots
- C. Return to Track A architecture-first mainline
- D. Pause

---

| 字段 | 取值 |
|---|---|
| 授权根 | DEC-20260517-003 (本文件) |
| 涉及文件上限 | ~12 (2 创建 deliverables + 1 创建 references.bib + 2 修改 drafts + 1 修改 STYLE_CONTRACT + 1 创建 cycle log + 3 修改 sync chain + 1 创建 DEC = ~12) |

