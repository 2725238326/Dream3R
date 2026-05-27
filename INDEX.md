# Dream Index

Last updated: 2026-05-27 (state-conditioned reconstruction pivot: added `specs/SPEC-20260527-001-dream3r-state-conditioned-reconstruction.md`, `decisions/DEC-20260527-009-state-conditioned-reconstruction-pivot.md`, and `cycles/CYCLE-20260527-state-conditioned-reconstruction.md`; hard expert selection demoted to proposal-prior / diagnostic-baseline role.)

Last updated: 2026-05-22 (cycle 043 architecture-focus round after user re-prioritization "架构是最重要的内容; 开题报告和综述放一边": W20 SOTA Feature Matrix expanded to family-grouped second pass at `code/dream3r/SOTA_FEATURE_MATRIX.md` (8 family sections covering MASt3R / Fast3R / Spann3R / CUT3R / VGGT / STream3R / Point3R / Mem3R / LONG3R / DINOv2-v3 / MoGe-2 / DepthAnything / Test3R / NSA / Mamba / 3DGS family / OnlineX-AnchorSplat flag); v0.5 axes spec drafted at `specs/SPEC-20260522-001-dream3r-v05-axes.md` (8 axes A1-A8: DINOv3-S backbone / adapter ckpt loading / dynamic_mask_proxy → D2 promotion / VGGT adapter + capability_card v2.2 / Test3R Critic-triggered off-path / NSA sliding branch utility / GaussianHead conditional main-forward entry — kept deferred / tttLRM A1 sub-action design); both files candidate-not-final per DEC-20260501-004; no code change; v0.3 + v0.4 layers byte-identical. Earlier last-updated note follows.) (v0.4 architecture closure round: added `code/dream3r/contracts.py`, `code/dream3r/repair.py`, `code/dream3r/orchestrator.py`, three test files `test_v04_architecture_contract.py` + `test_repair_executor_contract.py` + `test_composer_dispatch_contract.py`, and `ARCHITECTURE_V04_STATUS.md`; 24 new tests pass; 130 existing tests still pass; v0.3 model.py / modules.py / bus.py / anchor_bank.py / nsa_attention.py / composer_experts/* are byte-identical to before. Driven by `ARCHITECTURE_V04_AGENT_PROMPT.md`; non-proposal work, parallel to the proposal track. Earlier last-updated note follows.) (cycle 040 closed — DEC-20260517-001 authorized § 5 实验设计与评测协议 + § 7 研究进展与已完成工作 + § 8 研究计划与时间安排 dual-draft drafting; DRAFT_INTERNAL_V1 + DRAFT_EXTERNAL_V1 § 5 ~2800 内 + ~2000 外 字 across 7 sub-sections (三层证据阶梯 / ABL-v02-1..10 / ABL-memory-0..11 / Critic 标定 / 长序列真实评测 / 评测数据集 / 主要评测指标) + § 7 ~2200 内 + ~1500 外 字 across 6 sub-sections (架构设计文档系列 / 实现里程碑 W1-W18 / KITTI 集成证据 / 综述发布 / 综述反哺 / cycle 历史) + § 8 ~1500 内 + ~1000 外 字 across 3 sub-sections (短期 M1-M2 / 中期 M3-M5 / 长期 M6-M8); § 1 + § 2 + § 3 + § 4 + § 5 + § 6 + § 7 + § 8 累计 ~17800 内 + ~14000 外 字 ≈ 85% of OUTLINE_V1 §2 表 总字数估算; only § 9 placeholder for cycle 041; STYLE_CONTRACT §2 vocab table 43→48 rows (+5 evaluation-protocol terminology: hard_fail / soft_fail / oracle-bus / monotone upgrade gate / fixture regime R1-R5 / 集成证据); §6 sync log appended; G3a + G3b 5 corrective edits on first pass (4 G3a "cycle"-leak + 1 G3b lowercase "dream3r" repo-name leak in § 5.3 + § 7.5 + § 8.1 + § 8.2 rephrased to 本阶段 / 开题报告阶段 / 本研究架构 per cycle 036 + cycle 039 precedent); G4 0 hits on first pass; cycle 039 + 038 + 037 + 036 + 035 + 034 + Track A Dream3R v0.3 server-verified through cycle 034 + Track B 3R-mix 2026-05-15 deliverable + SHA256 pre-filled all unchanged)

Quick navigation for humans and agents. **Read `TASK_SNAPSHOT.md` first** (it is the highest-authority resume pointer; if its status is `in_progress` or `blocked`, do not start new work). Then read `AGENT_MASTER_PROMPT.md` for full operating rules.

## How To Read This Workspace

1. Start with `TASK_SNAPSHOT.md` (highest-authority resume pointer; tells you whether a task is in flight, what subtask is next, and whether forward motion is gated).
2. Then `AGENT_MASTER_PROMPT.md` (entry prompt with mandatory load protocol; `TASK_SNAPSHOT.md` is item 1 of that protocol, the rest follows).
3. Check `WORKFLOW_STATUS.md` for current phase, blocked decisions, and recommended next user decision.
4. Check `RESEARCH_STATE.md` for living state and cycle history.
5. Use this `INDEX.md` to find any specific file by topic.

## Root-Level Files (Always-On Entry Points)

| File | Role |
|---|---|
| `TASK_SNAPSHOT.md` | **Read first.** Highest-authority resume pointer: current task id, subtask board, status (`idle` / `in_progress` / `blocked`), `If interrupted, resume from` block, recent failure modes |
| `README.md` | Workspace overview, purpose, non-negotiables |
| `INDEX.md` | This file; topic-based navigation |
| `AGENT_MASTER_PROMPT.md` | Canonical agent operating prompt + mandatory load protocol (lists `TASK_SNAPSHOT.md` as item 1) |
| `WORKFLOW_STATUS.md` | Current phase, active workstreams, blocked decisions, recommended next user decision |
| `RESEARCH_STATE.md` | Living state log; cycle history; current recommendations |
| `ARCHITECTURE_V04_AGENT_PROMPT.md` | v0.4 architecture closure agent prompt — drives the orchestrator + contract + repair round |
| `ARCHITECTURE_V04_STATUS.md` | v0.4 closure verification: per-axis checklist (Perception / Memory / Permanence / Critic / Repair / Composer / Final), test results, and explicit stub/fallback/proxy list |

## Subdirectories By Purpose

### `paradigm/` - How Dream Operates

| File | Role |
|---|---|
| `RESEARCH_PARADIGM.md` | Operating paradigm, two-track plan, evidence ladder, user-discussion gates |
| `RESEARCH_WORKFLOW.md` | Source-to-implementation operational workflow |
| `RESEARCH_DATA_MODEL.md` | Schema for sources, mechanisms, RUs, decisions, experiments |
| `RESEARCH_SKILL_RULES_DRAFT.md` | Evolving rules for a future Codex skill |
| `RESEARCH_CODE_DISCIPLINE.md` | Behavior rules for synthesis and Dream-driven code (Karpathy-adapted + honesty override) |
| `RESEARCH_CONTENT_ROADMAP.md` | Research-content-first roadmap and axes |
| `CROSS_SPEC_SIGNAL_CONTRACT.md` | Formal contract for read-only / handoff signals between finalist specs; v1 covers Critic / Memory / Permanence / Composer |
| `TEACHER_AUDIENCE_PROFILE.md` | Placeholder file for the user to populate; gates D3 (first teacher demo target) |

### `planning/` - Active Research Planning

| File | Role |
|---|---|
| `MULTI_TRACK_RESEARCH_CANVAS.md` | Multi-branch comparison canvas (do not collapse to single thesis prematurely) |
| `RESEARCH_GRAPH_AND_PAPER_START.md` | Failure-mode / mechanism / composition graph; paper scaffold |
| `BRANCH_COMPARISON_MATRIX.md` | Branch-level comparison matrix and score table |
| `BRANCH_SHORTLIST_DECISION_SURFACE.md` | User decision surface for choosing 2-3 finalist branches |
| `ARCHITECTURE_MECHANISM_INTAKE.md` | Branch-neutral intake map for broad architecture and visual mechanisms |
| `ACTION_TAXONOMY_AND_PROXY_METRICS.md` | Compact A1-A8 actions and P1-P8 proxy validation protocols |
| `DREAM3R_THESIS_STRESS_TEST.md` | Stress test for the Dream3R / GEM-3R candidate branch |
| `MINIMAL_DEMO_CANDIDATES.md` | Teacher-demo candidate analysis |
| `WORK_RISK_REGISTER.md` | Consolidated cross-spec risk view across the four finalist specs and the cross-spec contract |
| `L3_PILOT_SELECTION.md` | Cycle 014 L3 downselect: recommends Critic as first pilot and Composer as backup; planning only, not L3 authorization. Cycle 015 acted on this recommendation: DEC-20260505-005 authorized the Critic L3 pilot SCOPE (per-step micro gates still required) |
| `COMPOSER_CAPABILITY_DESCRIPTORS.md` | Cycle 018 S2 deliverable: 7 admitted lightweight 3R experts (MASt3R / Fast3R / Spann3R / CUT3R / MoGe-2 / DepthAnything-V2 / Test3R) with capability descriptor schema (innovation point / input / output / cost / attention regime / adapter / capability_match / failure modes / evidence labels); routing policy sketch; cross-axis summary table; pool admission criteria + drops (VGGT, MapAnything, Kimi-KDA) |
| `NSA_MEMORY_INTEGRATION_MEMO.md` | Cycle 018 S3 deliverable: NSA × C2 Memory integration sketch; three-branch (compressed / selected / sliding) mapped to v0.2 Memory hierarchy A+B; bounded anchor bank K=256 proposed; selection gate driven by Critic confidence + Permanence link; LM-to-3R transfer labeled speculative |
| `MEMORY_V03_DESIGN_STUDY.md` | Cycle 025 direction 3.1 deliverable: code-observed study of CUT3R learned state-token recurrence and Spann3R explicit SpatialMemory; compares both against current Dream3R GRU + vector AnchorBank + NSAThreeBranch C2; proposes C2 v0.3 as latent state tokens + explicit spatial key/value bank + bus-gated writes; markdown research only |
| `MEMORY_V03_P0_PROTOTYPE_PLAN.md` | Cycle 027 deliverable: markdown-only P0 static tensor prototype plan for C2 Memory v0.3. Defines deterministic tensor fixtures, regimes R1-R5, variants V0 vector AnchorBank / V1 spatial key-value bank / V2 state-token recurrence / V3 hybrid bus-gated writes, metrics M1-M8, kill conditions K1-K7, reviewer checklist, and separate execution gate. Engineering plan only; no implementation authorized |
| `MEMORY_V03_ABLATION_REVIEW.md` | Cycle 029 review artifact for SPEC-20260508-002. Verdict: approved for planning use after corrections, not approved for execution. Captures R-029-1..5 corrections: oracle-bus boundary, state-token stale-smooth fail, op-proxy-only cost claim, hard/soft fail rules, narrowed controlled loop/revisit claim |
| `MEMORY_V03_P0_EXECUTION_DEC_TEMPLATE.md` | Cycle 030 deliverable: future execution authorization template for local static tensor P0 ABL-memory-0..8. Predefines allowed path, forbidden paths/actions, oracle-bus boundary, required outputs, stop gates, result labels, go/no-go rules, and evidence boundary. Template only; no implementation authorized |
| `DINOV3_C1_INTEGRATION_MEMO.md` | Cycle 018 S3 deliverable: DINOv3 × C1 Perceiver integration sketch; DINOv3-S replaces ViT-L (~14x param reduction; ~5x latency speedup; paper-derived); -B fallback documented; frozen-backbone default; heads from scratch |
| `DREAM3R_V02_CODE_STRUCTURE.md` | Cycle 020 S2 deliverable: v0.2 code structure planning. Maps SPEC-20260506-004 v0.2 architecture Delta 1..6 to per-file changes in `code/dream3r/`. Per-file change manifest with MODIFIED (modules.py / model.py / losses.py / smoke_test.py / config.py / train.py) + NEW (memory_anchor_bank.py / nsa_attention.py / composer_experts/ subdir with 7 expert adapters / latency_bench.py) + STABLE (bus.py CR-1..CR-6 carry forward). Explicit review surface subsection per MODIFIED + NEW file per user request "其他agent审阅修改". Server-side deployment surface per F-002. Honest evidence labels: speculative for NSA-related; paper-derived for DINOv3-S; engineering-judgment for expert pool composition; inferred for line-of-code estimates. Sibling artifact to `DREAM3R_V02_IMPLEMENTATION_ROADMAP.md` |
| `DREAM3R_V02_IMPLEMENTATION_ROADMAP.md` | Cycle 020 S3 deliverable: v0.2 implementation roadmap. Breaks `DREAM3R_V02_CODE_STRUCTURE.md` per-file changes into 22 reviewable tasks across 4 tiers — Tier 1 prerequisites (T-v02-A repo skeleton + T-v02-B test harness); Tier 2 per-module (T-v02-C1 DINOv3-S backbone / T-v02-C2-mem-bank / T-v02-C2-nsa / T-v02-C5 Composer routing / T-v02-EXPERT-1..7 per-expert adapters); Tier 3 integration (T-v02-D model wiring / T-v02-E losses update / T-v02-F smoke + latency bench); Tier 4 ABL harnesses (T-v02-ABL-1..9 one per ABL-v02-N from SPEC-005). Per-task scope/inputs/outputs/effort/pre-execution review checklist/post-execution validation checklist/execution gate. Task dependency DAG. ~250-380 engineering-hours total inferred (post-first-task calibration needed). Per-task review checklists are the load-bearing other-agent handoff hook per user request "其他agent审阅修改" |
| `SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md` | Cycle 035 upstream proposal (2026-05-15, draft awaiting user review): maps 2026-05-15 3R-mix survey four-axis findings (six failure modes / long-seq memory four types / test-time three subtypes / output asset three types) plus input-extension bonus axis to Dream3R v0.3 architecture. Outputs 21-row coverage matrix (6 ✓ / 11 ⚠ / 4 ✗), P0/P1/P2 gap identification, type A/B/C/D optimization suggestions, W19-W30 roadmap reorder recommendation. Proposal status; not spec; cycle 035 only lands its P0 markdown deliverables, does NOT ratify proposal as v0.4 design input |
| `SOTA_MATRIX_V2.md` | Cycle 035 P0-2 deliverable: re-labels SPEC-20260507-001 v0.2 19 comparator entries (T1 in-pool 7 + T2 dropped 3 + T3 oos 1 + T4 foundation 1 + T5 orthogonal 8) plus Point3R / Mem3R / G-CUT3R / Pow3R / MASt3R-SfM appendix entries against survey's five axes (failure modes / long-seq memory / test-time / output asset + input extension bonus). Five tables A-E with ✓ primary / ⚠ partial / — not first-class / n/a inapplicable cell labels; per-row evidence labels; identifies 4 first-class-support gaps (OOD / external prior / 4DGS license / input extension axis) feeding WORK_RISK_REGISTER v1.1 additions. Planning artifact only; not spec; does not modify SPEC-007 v0.2 |
| `CRITIC_CALIBRATION_PLAN_V1.md` | Cycle 035 P0-1 deliverable: per-failure-mode threshold standardization plan for C4 Critic anchored to survey six failure modes (弱纹理 / 镜面玻璃 / 快速运动 / 长基线 / 尺度漂移 / 域外). Maps each mode to primary + secondary signal channels among C4 Critic's 5 sub-signals (pose_novelty / view_overlap / reprojection_residual / pointmap_conflict / confidence_drop); defines sub-sample sampling rules; outlines method A distribution-quantile P95 vs method B supervised classifier with selection decision tree; sets per-mode threshold table schema; 5-metric validation gate (mode-estimate accuracy / KITTI smoke regression / repeatability / dataset license / fallback completeness). Plan-only; execution needs independent DEC + F-002 server authorization |
| `LONG_SEQ_REAL_TABLE_PLAN.md` | Cycle 035 P0-3 deliverable: extension plan for the 4 existing `ablate_recurrence` variants (baseline_cross_attention / mamba_hybrid / no_nsa / no_stable_memory) on KITTI long windows (≥10). Maps 4 variants to survey §6 four memory mechanism types (B1 空间指针 / B2 causal-AR / B3 hybrid / B4 预算治理 — last is explicit B4 coverage gap acknowledgement). Defines 4 long-seq-specific metrics (scale_drift_proxy / memory_decay_proxy / anchor_fill_rate / retrieval_diversity); outlines windows ∈ {10, 20, 50, 100} staged execution with monotonic upgrade gate; 6-metric validation gate; resource estimate ~10 hr single-GPU for full sweep. Plan-only; execution needs independent DEC + F-002 server authorization |
| `DREAM3R_V05_ITERATION_TEST_PLAN.md` | 2026-05-22 architecture execution plan: turns v0.4 closure + v0.5 axes into sprintable testing work. Defines L0-L4 completion standards, S0 local v0.4 edge tests, S1 A6 KITTI 8-10 window memory evidence, S2 A2 staged adapter real-backend closure, S3 A5 Test3R off-path, S4 A3 dynamic mask promotion, server runbook outline, evidence schema, gates, risks, and a short agent prompt. Planning artifact only; does not close any v0.5 axis |

### `planning/proposal_dream3r/` - Dream3R 开题报告 dual-draft (Track C)

New subdirectory created cycle 036 (per DEC-20260516-001). Hosts the Chinese Dream3R 开题报告 dual-draft: Dream-vocabulary 内部稿 + academic-Chinese 外部稿 (uses 代号 "候选架构 X" / "本研究架构"; no raw "Dream3R" in main text). **Proposal track functionally closed** through cycle 042: §1-§9 dual-draft complete (~19300 内 + ~15000 外 字); PDF compiled (263 KB); advisor cover note + submission record ready. The actual Track B survey submission and this 开题报告 are sibling artifacts that share `references.bib` material but do not cite each other.

| File | Role |
|---|---|
| `OUTLINE_V1.md` | Cycle 036 P0-B-1 deliverable: 9-section dual outline (外稿 ~16000 字 / 内稿 ~21100 字) + §3 chapter mapping table (外稿 ↔ 内稿 ↔ 复用素材 + 外稿独占 + 内稿独占 per § 1-§ 9) + §4 cycle 037-042 drafting order (cycle 037 §2 first as largest single-section block + heaviest Track B 综述 reuse + STYLE_CONTRACT stress-test) + §5 §1 200-字 双稿 风格 样本 + §6 pre-drafting checklist + §7 explicit non-scope clauses. Anchors §2 国内外研究现状 → Track B 综述 §1-§10 + 5 tables + 6 figures + 44 references; §4 研究方案 → SPEC-004 v0.2 + SPEC-008 v0.3 + CR-1..CR-6; §5 实验设计 → SPEC-005 v0.2 + SPEC-007 v0.2 + CRITIC_CALIBRATION_PLAN_V1 + LONG_SEQ_REAL_TABLE_PLAN; §7 已完成工作 → code/dream3r/RECENT_PROGRESS.md W1-W18 + KITTI smoke L2=20.47; §8 时间安排 → code/dream3r/NEXT_PHASE_ROADMAP.md W19-W30 + cycle 035 proposal §6 重排建议; §9 风险 → WORK_RISK_REGISTER v1.2 17+ rows. Total feeds into cycle 037-042 逐章起草 |
| `STYLE_CONTRACT.md` | Cycle 036-042 deliverable: bilingual style contract. **v1 closed**. §2 vocabulary substitution table 50 rows. §3 sync rule internal-is-master. §4 候选架构 X 命名规则. §5 candidate-not-final 句式对比表 (9 pairs). §6 append-only sync log (7 entries: cycle 036-042). 14 corrective edits total across all cycles |
| `DRAFT_INTERNAL_V1.md` | Cycle 036-042 deliverable: Dream-vocabulary 内部稿. §1-§9 全部完整 (~19300 字). master per STYLE_CONTRACT §3. Content frozen cycle 041; metadata + §8.1 updated cycle 042 |
| `DRAFT_EXTERNAL_V1.md` | Cycle 036-042 deliverable: academic-Chinese 外部稿 (vocab-clean per G3a + G3b). §1-§9 全部完整 (~15000 字). Content frozen cycle 041; metadata + §8.1 updated cycle 042. PDF source for `deliverables/proposal_external_v1_2026-05-17.pdf` |
| `references.bib` | 44 BibTeX entries copied from Track B survey (shared citation pool) |
| `deliverables/proposal_external_v1_2026-05-17.pdf` | Cycle 042: compiled PDF (263 KB, pandoc 3.9 + xelatex + SimSun). Advisor review copy |
| `deliverables/SUBMISSION_PACKAGE_ADVISOR_PROPOSAL_2026-05-17.md` | Cycle 042: Chinese cover note (~500 字, 6 sections). G3a + G3b vocab firewall verified 0 hits |
| `deliverables/SUBMISSION_RECORD_PROPOSAL_2026-05-17.md` | Cycle 042: submission metadata (yaml) + checklist. Recipient/channel slots pending user fill |

### `sources/` - Source Mining

| File | Role |
|---|---|
| `FRONTIER_SOURCE_MAP.md` | Verified and pending source map; cycle-tagged source-mining passes |

### `units/` - Research Units, Scoring, Reproduction Readiness

| File | Role |
|---|---|
| `RESEARCH_UNIT_BANK.md` | Structured Dream Research Units (RU-001..) |
| `IDEA_SCOREBOARD.md` | Score table for candidate ideas |
| `REPRODUCTION_READINESS_MATRIX.md` | Repo-level smoke-test and KYKT integration readiness |

### `handoff/` - Collaboration And Frontend

| File | Role |
|---|---|
| `FRONTEND_DESIGN_HANDOFF_PROMPT.md` | Canonical frontend handoff prompt for Gemini CLI |
| `COLLABORATION_ROADMAP.md` | Human-agent collaboration path and near-term deployment sequence |
| `ARCHITECTURE_V05_AGENT_START_PROMPT.md` | Short startup prompt for another agent to begin the v0.5 evidence-closure pass from `planning/DREAM3R_V05_ITERATION_TEST_PLAN.md`; starts with S0 edge tests and S1 A6 server runbook, with no checkpoint download, training, or v0.5 closure claims |

### `logs/` - Running Logs

| File | Role |
|---|---|
| `QUESTION_LOG.md` | Interview history and next questions |

### `archive/` - Historical / Superseded

| File | Role |
|---|---|
| `PHASE1_RESEARCH_PLAN.md` | Phase 1 plan (historical; Phase 1.5 is current) |
| `PHASE1_EXECUTION_LOG.md` | Phase 1 running log (historical) |
| `PHASE1_DECISION_MEMO.md` | Phase 1 synthesis and gates (historical) |
| `MASTER_RESEARCH_PROMPT_DRAFT.md` | Superseded by `AGENT_MASTER_PROMPT.md` |

### `cycles/` - Per-Cycle Research Logs

Format: `CYCLE-YYYYMMDD-NNN.md`. Newest is the active cycle.

Recent (most relevant for resume):

| File | Cycle | Role |
|---|---|---|
| `CYCLE-20260522-001.md` | 043 | Architecture-focus round after user re-prioritization "架构是最重要的内容; 开题报告和综述放一边". W20 SOTA Feature Matrix expansion to family-grouped second pass (`code/dream3r/SOTA_FEATURE_MATRIX.md`; 8 family sections; 30+ external methods mapped) + v0.5 axes spec drafting (`specs/SPEC-20260522-001-dream3r-v05-axes.md`; 8 axes A1-A8 with explicit `closes_iff`; v0.5 additive to v0.4 by default). Markdown only; v0.3 + v0.4 code byte-identical; both candidate-not-final per DEC-20260501-004; no DEC proposed; sync chain applied (INDEX.md + WORKFLOW_STATUS.md + TASK_SNAPSHOT.md). Auto-memory updated: track-priorities feedback recorded |
| `CYCLE-20260517-003.md` | 042 | Dream3R 开题报告最终修订 + PDF 编译 + advisor 提交 packaging (DEC-20260517-003 authorized; content frozen; bottom metadata cleanup + §8.1 past-tense; references.bib 44 entries; PDF 263 KB pandoc+xelatex; cover note + submission record G3a/G3b clean; STYLE_CONTRACT v1 closed 50 rows 7 entries; proposal track functionally closed; no spec / code / server action) |
| `CYCLE-20260517-002.md` | 041 | Dream3R 开题报告 § 9 风险分析与应对 dual-draft + 通稿审查 + STYLE_CONTRACT final sync (DEC-20260517-002; §1-§9 全部章节完整 ~19300 内 + ~15000 外 字) |
| `CYCLE-20260517-001.md` | 040 | Dream3R 开题报告 § 5 实验设计与评测协议 + § 7 研究进展与已完成工作 + § 8 研究计划与时间安排 dual-draft drafting (DEC-20260517-001 authorized; DRAFT_INTERNAL_V1 + DRAFT_EXTERNAL_V1 § 5 ~2800 内 + ~2000 外 字 across 7 sub-sections 5.1 三层证据阶梯 / 5.2 架构层消融 ABL-v02-1..10 / 5.3 记忆机制消融 ABL-memory-0..11 / 5.4 Critic 标定 CRITIC_CALIBRATION_PLAN_V1 / 5.5 长序列真实评测 LONG_SEQ_REAL_TABLE_PLAN / 5.6 评测数据集 KITTI + DTU + 合成 fixture / 5.7 主要评测指标 + § 7 ~2200 内 + ~1500 外 字 across 6 sub-sections 7.1 架构设计文档系列 / 7.2 实现里程碑 W1-W18 / 7.3 KITTI 集成证据 (pointmap L2 = 20.4747 集成证据 非训练后质量) / 7.4 综述发布 / 7.5 综述反哺 / 7.6 cycle 历史 + § 8 ~1500 内 + ~1000 外 字 across 3 sub-sections 8.1 短期 M1-M2 / 8.2 中期 M3-M5 / 8.3 长期 M6-M8; STYLE_CONTRACT §2 vocab table 43→48 rows (+5: hard_fail / soft_fail / oracle-bus / monotone upgrade gate / fixture regime R1-R5 / 集成证据); §6 sync log appended; G3a + G3b 5 corrective edits on first pass (4 G3a "cycle"-leak + 1 G3b lowercase "dream3r" repo-name leak rephrased to 本阶段 / 开题报告阶段 / 本研究架构 per cycle 036 + cycle 039 precedent); G4 0 hits on first pass; no spec / code / server action) |
| `CYCLE-20260516-004.md` | 039 | Dream3R 开题报告 § 3 候选研究问题 + § 6 预期成果与创新点 dual-draft drafting (DEC-20260516-004 authorized; DRAFT_INTERNAL_V1 + DRAFT_EXTERNAL_V1 § 3 ~1800 内 + ~1500 外 字 across 5 sub-sections 3.1 Q1 验证机制 / 3.2 Q2 长序列内存 / 3.3 Q3 多专家组合 / 3.4 4-finalist 模块独立性 / 3.5 候选 vs 最终 研究地位 + § 6 ~1300 内 + ~1000 外 字 across 3 sub-sections 6.1 预期交付物 / 6.2 三个 IP 声明 (Q1↔IP1 / Q2↔IP3 / Q3↔IP2) / 6.3 与现有工作的实证差异; STYLE_CONTRACT §2 vocab table 41→43 rows (+2: C4' / Innovation Point); §6 sync log appended; G3a + G3b 0 hits on first pass; G4 7 hits per side from negation-context candidate-not-final 句式 examples, applied 7 corrective edits per side per cycle 036 precedent (最终架构方案 → 最终方案 / X 解决了 → X 已完全解决 / Dream3R 解决了 → Dream3R 已完全解决 / 证明 ... 优于 → 宣称 ... 优于), re-grep all 0 hits; no spec / code / server action) |
| `CYCLE-20260516-003.md` | 038 | Dream3R 开题报告 § 4 研究方案 / Dream3R v0.3 架构 dual-draft drafting (DEC-20260516-003 authorized; DRAFT_INTERNAL_V1 + DRAFT_EXTERNAL_V1 § 4 ~4000 内 + ~3000 外 字 across 8 sub-sections: 整体设计 + 帧预算 / C1 感知模块 DINOv3-S / C2 记忆模块 NSA + AnchorBank + StateToken + Mamba hybrid / C3 永久性模块 Slot Attention + permanence_link / C4 校验模块 Sampson + depth + 共视 + 修复动作 0-5 / C5 编排模块 7 专家池 / C6 总线模块 CR-1..CR-6 / 与现有 3R 系统的结构差异; STYLE_CONTRACT §2 vocab table 22→41 rows; §6 sync log appended; G3a + G3b + G4 greps all 0 hits after 1 corrective edit on cycle-037-residue leakage; no spec / code / server action) |
| `CYCLE-20260516-002.md` | 037 | Dream3R 开题报告 § 2 国内外研究现状 dual-draft drafting (DEC-20260516-002 authorized; DRAFT_INTERNAL_V1 + DRAFT_EXTERNAL_V1 § 2 ~4200 内 + ~3700 外 字 across 7 sub-sections 基础谱系 / 多视角规模化 / 视频动态 4D / 长序列内存四类 / 测试时三类 / 输出资产三类 / 综述四轴覆盖矩阵 + 落点; STYLE_CONTRACT §6 sync log appended; G3a + G3b + G4 greps all 0 hits on first pass; 22-row seed vocab substitution table unchanged; no spec / code / server action) |
| `CYCLE-20260516-001.md` | 036 | Survey advisor submission packaging + Dream3R proposal dual-draft kickoff (DEC-20260516-001 authorized; Part A 3 files in `3R-mix/deliverables/` SUBMISSION_PACKAGE_ADVISOR + SUBMISSION_RECORD + RELATION_TO_TRACK_A + Part B 4 files in new `planning/proposal_dream3r/` OUTLINE_V1 + STYLE_CONTRACT + DRAFT_INTERNAL_V1 + DRAFT_EXTERNAL_V1 § 1 only + WORK_RISK_REGISTER v1.2 +3 proposal-cycle risk rows R-PROP-VOCAB-1 / R-PROP-CLAIM-1 / R-PROP-SYNC-1 + sync chain; G2 + G3a + G3b + G4 vocab firewall + over-claim greps all 0 hits; no spec / code / server action) |
| `CYCLE-20260515-001.md` | 035 | Survey-driven markdown deliverables launch (DEC-20260515-001 authorized; 3 new planning files SOTA_MATRIX_V2 / CRITIC_CALIBRATION_PLAN_V1 / LONG_SEQ_REAL_TABLE_PLAN + 4 new cross-spec risk rows R-OOD-1 / R-EXT-PRIOR-1 / R-4DGS-LIC-1 / R-INPUT-EXT-1 in WORK_RISK_REGISTER + sync chain; no spec / code / server action) |
| `CYCLE-20260511-001.md` | 034 | Stabilization + Mamba/GaussianHead + KITTI real-data smoke + Track B 3R-mix survey kickoff (retroactively logged 2026-05-13) |
| `CYCLE-20260510-001.md` | 033 | Dream3R v0.3 architecture advancement W1-W16 on server (DINOv2 backbone, 3D-aware retrieval, active/stable state, Grassmannian regularizer, geometric Critic, ISA slots, real MASt3R + Spann3R adapters) (retroactively logged 2026-05-13) |
| `CYCLE-20260508-008.md` | 031 | Local Memory v0.3 P0 scaffold + ABL-memory-0 validity gate |

Cycle 032 (v0.3 codebase implementation, optimization, server verification; 2026-05-09) was closed via `TASK_SNAPSHOT.md` update without a dedicated cycle log; its onboarding successor is `code/dream3r/REVIEW_PROMPT.md`.

### `3R-mix/` - Chinese 3R / feed-forward 3D reconstruction survey (Track B, parallel workspace)

Separate LaTeX workspace deliberately decoupled from Dream / KYKT internal vocabulary. Manuscript surface contains no `KYKT` / `Dream` / `Dream3R` / `agent` / `skill` / `workflow` / `本地项目` strings (`Grep`-verified). Track A architecture-first mainline remains primary per DEC-20260506-001; Track B is a separate survey product, not a Dream3R paper.

| File | Role |
|---|---|
| `NEW_CHAT_HANDOFF.md` | Canonical top-level handoff for the survey workspace |
| `main.tex` | 18-page LaTeX (`ctexart` + `xelatex` + `unsrtnat`); 10 sections; 6 figures (4 TikZ + 2 paper Fig.1 composites); 5 booktabs tables (last column unified to "适用条件与局限") |
| `references.bib` | 44 BibTeX entries, all cited (no `\nocite{*}`); CroCo added 2026-05-14 |
| `notes/work_log.md` | Append-only fine-grained editing log |
| `notes/{paper_inventory,model_inventory,chapter_structure,fact_cards,figure_prompts,figure_selection,review_quality_audit}.md` | Per-axis working notes |
| `figures/{dust3r,vggt,monst3r,cut3r}_fig1.png` | Paper Fig.1 crops embedded after user-confirmed reuse license |
| `deliverables/SUBMISSION_PACKAGE_ADVISOR_2026-05-16.md` | Cycle 036 Part A advisor cover note (~600 字 Chinese, G2 vocab-clean: 0 hits on `Dream\|Dream3R\|KYKT\|agent\|skill\|workflow\|本地项目\|cycle\|SPEC-\|DEC-\|CR-`); 6 sections (主旨 / 范围 / 与英文综述差异 / 证据边界 / 路线说明 / 请求审阅事项) |
| `deliverables/SUBMISSION_RECORD_2026-05-16.md` | Cycle 036 Part A submission metadata + checklist with slots for recipient / channel / pdf_sha256 (PowerShell `Get-FileHash`) / submitted_by / contact / submitted_at; pre-filled page_count = 18, ref_count = 44, figure_count = 6, table_count = 5, vocab_grep_verified = 2026-05-16; actual submission action (email / IM / portal / offline) is user post-cycle action |
| `deliverables/RELATION_TO_TRACK_A_2026-05-16.md` | Cycle 036 Part A internal meta (~600 字; NOT delivered to advisor); documents Track B / Track A relationship + 2-track parallel run since 2026-05-06 + Track B wound down 2026-05-14 route C + Track A Dream3R v0.3 active + cycle 035 反哺 + 词汇隔离声明; only Track B-side file allowed to mention Dream-vocabulary |
| `deliverables/3r_survey_stage_final_2026-05-15_natural.pdf` | Current recommended deliverable (18 A4 pages, 44 refs, 0 LaTeX errors / 0 warnings; 2026-05-15 prose naturalization pass on top of 2026-05-14 quality pass); this is the PDF the SUBMISSION_RECORD_2026-05-16.md points to |
| `deliverables/3r_survey_stage_final_2026-05-14_quality.pdf` | Earlier 2026-05-14 quality pass snapshot |
| `deliverables/3r_survey_stage_final_2026-05-13{,_polished,_caption_polished,_refined}.pdf` | Earlier polish-pass snapshots |
| `COMPREHENSIVE_OPTIMIZATION_PROMPT.md` | Driving prompt for the 2026-05-13 comprehensive optimization pass |
| `GENERATION_PROMPT.md` | Original generation prompt |

### `decisions/` - Decision Memos

Format: `DEC-YYYYMMDD-NNN-<slug>.md`. Indexed in `registry/decision_registry.md`.

### `code/dream3r/` - Dream3R PyTorch Implementation

Dream3R v0.1 code. Runs on remote server `/hdd3/kykt26/code/dream3r/` (dream3r conda env). Local copy is for editing; deploy via SFTP.

| File | Role |
|---|---|
| `bus.py` | C6 Memory Bus: typed signal namespace + CR-1..CR-6 gates (zero parameters) |
| `modules.py` | C1 Perceiver (ViT backbone + heads), C2 Memory (GRU/Mamba), C3 Permanence (Slot Attention), C4 Critic (TransformerEncoder), C5 Composer (table join) |
| `model.py` | Dream3R main model: wires C1-C6 in bus tick order; preset configs (small / small_vit) |
| `contracts.py` | v0.4 typed dataclasses for every module boundary (`PerceptionOutput`, `MemoryOutput`, `PermanenceOutput`, `CriticDecision`, `ComposerDecision`, `DispatchedExpertOutput`, `RepairReport`, `ReconstructionOutput`); also defines v0.4 action codes 0..3 |
| `repair.py` | v0.4 `RepairExecutor`: action=1 local rerun, action=2 window rerun, action=3 reroute hint; `max_repair_attempts` honored; every attempt recorded in `repair_action_log` |
| `orchestrator.py` | v0.4 `V04Pipeline`: wraps `Dream3R` with closed-loop (primary forward → critic decision → repair executor → composer dispatch → final `ReconstructionOutput`) |
| `losses.py` | Multi-loss L_total: pointmap + critic P1/P5 + permanence P4 + action entropy |
| `smoke_test.py` | End-to-end validation: forward + backward + bus signals + CR-1 gate + memory carry-over |
| `PLAN.md` | Implementation roadmap (6 phases) with checklist |
| `tests/test_v04_architecture_contract.py` | v0.4 round: 11 tests asserting full `ReconstructionOutput` contract from `V04Pipeline` |
| `tests/test_repair_executor_contract.py` | v0.4 round: 6 tests asserting action 1/2/3 actually rerun / reroute / cap |
| `tests/test_composer_dispatch_contract.py` | v0.4 round: 7 tests asserting composer dispatches a real adapter and reroute hint changes the expert |
| `SOTA_FEATURE_MATRIX.md` | Cycle 043 W20 second pass: family-grouped mapping of 30+ external 3R-relevant methods (MASt3R / Fast3R / Spann3R / CUT3R / VGGT / STream3R / Point3R / Mem3R / LONG3R / DINOv2-v3 / MoGe-2 / DepthAnything / Test3R / NSA / Mamba / 3DGS family / etc.) → Dream3R modules + implementation status (real-wired vs deterministic fallback vs stub vs comparator-only) + per-method evidence/test + gap report. Supersedes the 2026-05-10 first pass while preserving its differentiation list + evidence map at the end. Cross-links to `ARCHITECTURE_V04_STATUS.md` and `specs/SPEC-20260522-001-dream3r-v05-axes.md` |
| `NEXT_PHASE_ROADMAP.md` | W19-W29 roadmap (real data / SOTA matrix / ablation / visualization / expert routing quality / critic calibration / TTT / STream3R relation / 3DGS / training hardening / paper pack). Origin of cycle 043 W20 work |
| `RECENT_PROGRESS.md` | Tier 1/2/3 evidence ledger; KITTI smoke result reference |

### `experiments/` - Experiment Plans

Format: `EXP-YYYYMMDD-NNN-<slug>.md`. Filing here does not mean the experiment was run. Cycle 013 added 4 L3 prerequisites briefs (one per finalist; brief-only, NOT L3 authorization).

| File | Finalist | Role |
|---|---|---|
| `EXP-20260501-001-dust3r-splatt3r-smoke-plan.md` | Phase 1 baseline | First reproducibility plan; planned only, do not run until user confirms |
| `EXP-20260505-001-l3-prerequisites-critic.md` | Geometry Critic (SPEC-20260503-001) | L3 prerequisites brief: repos + checkpoints + GPU/disk/time (`inferred`) + smoke-test path + minimum code change. Cycle 015 SCOPE authorized per DEC-20260505-005; per-step micro gates G_clone / G_install / G_download / G_run / G_log_use still required before any operational step |
| `EXP-20260505-002-l3-prerequisites-memory.md` | Executive Memory (SPEC-20260503-002) | L3 prerequisites brief; same structure |
| `EXP-20260505-003-l3-prerequisites-permanence.md` | Dynamic Object Permanence (SPEC-20260503-003) | L3 prerequisites brief; same structure |
| `EXP-20260505-004-l3-prerequisites-composer.md` | 3R Composer (SPEC-20260504-001) | L3 prerequisites brief; same structure; closure of G2 inventoried but not executed |
| `prototypes/memory_v03_p0/README.md` | C2 Memory v0.3 | Cycle 031 local P0 scaffold. `ABL-memory-0` passed 22/22 fixture/logging validity checks and generated `outputs/` artifacts. Later `ABL-memory-1..8` behavior remains unimplemented and requires new DEC |

### `cases/` - L2 Proxy Case Cards

Format: `CASE-YYYYMMDD-<SPEC>-NNN.md`. One file per (input, finalist spec) pair under `templates/proxy_case_card.md`. Filing a case card does not claim measured performance; the template enforces evidence labels (paper-proven / inferred / demo-observed / code-observed). Cycle 009 populated the first portfolio:

| File | Spec | Role |
|---|---|---|
| `CASE-20260504-CRITIC-01.md` | SPEC-20260503-001 | Static pair (MASt3R upstream); A5 = rerun_local_region; CR-1 not exercised |
| `CASE-20260504-CRITIC-02.md` | SPEC-20260503-001 | Fast3R vs Spann3R; CR-1 reroute_model + Composer agree/veto loop |
| `CASE-20260504-CRITIC-03.md` | SPEC-20260503-001 | MonST3R 48-frame; CR-3 forward-reference read of Memory latent_drift_proxy |
| `CASE-20260505-COMPOSER-01.md` | SPEC-20260504-001 | Static-collection regime; CR-1 closure paired with CRITIC-02 |
| `CASE-20260505-COMPOSER-02.md` | SPEC-20260504-001 | Regime-typed route_regret central thesis card |
| `CASE-20260505-COMPOSER-03.md` | SPEC-20260504-001 | Fast3R vs MASt3R-SfM; v1 -> v2 cost-typed route_regret canonical under v2 (per DEC-20260504-004) |
| `CASE-20260505-COMPOSER-04.md` | SPEC-20260504-001 | KYKT-metadata-derived capability_card grounded to 4 KYKT job inventory (cycle 012; advances G2 inferred -> inferred-with-real-inventory-anchor; G2 NOT closed; first non-paper-derived Composer L2 card) |
| `CASE-20260505-COMPOSER-05.md` | SPEC-20260504-001 | Cycle 014 VGGT capability-card gap addendum; per-card gap, no v2.2 contract revision; G2 NOT closed |
| `CASE-20260504-MEMORY-01.md` | SPEC-20260503-002 | MonST3R 48-frame; primary Memory L2; CR-3 producer (closes cycle-009 CRITIC-03 forward-reference null) |
| `CASE-20260504-MEMORY-02.md` | SPEC-20260503-002 | Spann3R transforms timeline; externalization-of-governance argument |
| `CASE-20260504-MEMORY-03.md` | SPEC-20260503-002 | MASt3R small-N baseline; non-hallucination boundary on static-pair regime |
| `CASE-20260504-PERMANENCE-01.md` | SPEC-20260503-003 | MonST3R 48-frame; primary Permanence L2; CR-2 producer (closes cycle-009 gap G1 with MEMORY-01) |
| `CASE-20260504-PERMANENCE-02.md` | SPEC-20260503-003 | MASt3R static control; mint_object_id rate = 0 (closes PERMANENCE-01 fail_fast c) |
| `CASE-20260504-PERMANENCE-03.md` | SPEC-20260503-003 | Synthetic dynamic identity-validation; closes PERMANENCE-01 fail_fast b |

### `literature/` - Literature Guidance Board

Curated guidance, not inventory. Inventories live in `sources/FRONTIER_SOURCE_MAP.md` and `registry/source_registry.md`.

| File | Role |
|---|---|
| `INDEX.md` | Entry point; usage rules; pointers to inventories so guidance and inventory do not duplicate |
| `SPINE_CRITIC.md` | Required + advanced + skip-with-reason reading for the Critic finalist (SPEC-20260503-001); cross-paper disagreements; spec interface |
| `SPINE_MEMORY.md` | Same structure for the Executive Memory finalist (SPEC-20260503-002) |
| `SPINE_PERMANENCE.md` | Same structure for the Dynamic Object Permanence finalist (SPEC-20260503-003) |
| `SPINE_COMPOSER.md` | Same structure for the Composer finalist (SPEC-20260504-001); MoE routing as cross-domain analog |
| `CRITICAL_NOTES.md` | Running log of "looks like X is X' but actually" insights; deconfusion of commonly-confused mechanisms |
| `PAPER_RELATED_WORK_SKELETON.md` | Cycle 013 upgraded from skeleton to **prose draft** (Sections 1-7 prose anchored to L2 case cards + SRC-* IDs; Sections 8-9 drafted as prose). Filename retained per Surgical Edits |
| `PAPER_PHASE2_BLUEPRINT.md` | Cycle 014 claim-safe paper blueprint; separates current L2 / inferred claims from L3-required claims; not full paper readiness |

### `specs/` - Finalist Mechanism Specs and Architecture Specs

Format: `SPEC-YYYYMMDD-NNN-<slug>.md`. One file per user-approved finalist branch or architecture-level deliverable. Created via `templates/finalist_mechanism_spec.md`. Drafting a spec does not authorize reproduction, training, checkpoint download, or KYKT navigation change.

| File | Role |
|---|---|
| `SPEC-20260503-001-geometry-critic.md` | Geometry Critic / System-2 3R finalist spec (A4 + A5 repair facet; P1 + P5) |
| `SPEC-20260503-002-executive-memory.md` | Executive Memory / State Governance finalist spec (A1 + A2 + A3; P2 + P3) |
| `SPEC-20260503-003-dynamic-object-permanence.md` | Dynamic Object Permanence / 4D Memory finalist spec (A6; P4 + identity_consistency) |
| `SPEC-20260504-001-3r-composer.md` | 3R Composer / Unified Model Ecology finalist spec (A5 routing facet; P5 route_regret + capability_match) |
| `SPEC-20260506-001-dream3r-architecture.md` | Dream3R architecture v0.1: control-graph-as-architecture; hybrid substrate (transformer + SSM + slot + bus); 4 finalist specs synthesized as cores C1-C5 + C6 bus; CR-1..CR-6 as gates; A1-A8 mapped to concrete layers (cycle 016 S2) |
| `SPEC-20260506-002-dream3r-ablation-plan.md` | Dream3R ablation plan v0.1: 10 ablations in 3 tiers; falsification table per architectural claim; benchmark categories B1-B6; dependency graph (cycle 016 S3) |
| `SPEC-20260506-003-dream3r-comparator-map.md` | Dream3R comparator map v0.1: 14+ models across 7 groups; 8 comparison axes; threat ranking; architecture-novel elements with no comparator (cycle 016 S4) |
| `SPEC-20260506-004-dream3r-architecture-v02.md` | Dream3R architecture v0.2 delta spec: six numbered deltas on v0.1 (frame budget 30-50 ms/frame; C1 DINOv3-S replaces ViT-L; C2 bounded anchor bank + NSA-style retrieval A+B; sparse attention as engineering optimization; C5 Composer pool admits 7 lightweight experts; main-claim narrowed to A Verification-as-architecture + D Heterogeneous best-of-N Composer); v0.1 body unmodified per DEC-20260506-002 (cycle 018 S4) |
| `SPEC-20260506-005-dream3r-ablation-plan-v02.md` | Dream3R ablation plan v0.2 delta addendum: nine v0.2 ablations (ABL-v02-1..9) anchored to SPEC-20260506-004 v0.2 architecture deltas — NSA-removal / DINOv3 backbone tier (-S/-B/-L) / frozen vs partial-unfreeze / Composer best-of-N vs single-expert / capability_match measurement / selection-gate signal subsetting / head training schedule / frame-budget benchmark / NSA kernel decomposition. Tier 1 load-bearing: ABL-v02-1+4+6. Falsification mapping for main-claim A + D + E. Per-ABL review checklist subsection for other-agent handoff per user request "其他agent审阅修改". v0.1 body unmodified per DEC-20260506-003 (cycle 019 S2) |
| `SPEC-20260507-001-dream3r-comparator-map-v02.md` | Dream3R comparator map v0.2 delta addendum: reorganizes v0.1 16-entry comparator pool into 5 tiers per SPEC-004 Delta 5 — in-pool 7 admitted experts (MASt3R / Fast3R / Spann3R / CUT3R / MoGe-2 / DepthAnything-V2 / Test3R) + out-of-pool 3 drops (VGGT / MapAnything / Kimi-KDA per DEC-002 reasons) + out-of-scope 1 (ViT-L per Delta 2) + foundation 1 (DUSt3R) + orthogonal 8. Adds 3 NEW comparison axes 9-11 (NSA-style sparse attention / DINOv3 backbone tier / Composer expert pool composition) per Deltas 2-5. Re-ranks threats against pillar A + D narrowing — pillar A HIGH threats: Test3R alone + TTT3R; pillar D HIGH threats: VGGT offline-batch + each in-pool expert alone. Full v0.1 → v0.2 traceability matrix; 5 risks R-cm-1..5 + 5 open questions Q1-Q5 surfaced including ABL-v02-10 Test3R-alone candidate for pillar A robustness. v0.1 SPEC-003 body unmodified per DEC-20260507-001 (cycle 021 S3); v0.1 Version history v0.2 pointer entry appended. Closes v0.2 markdown trio (architecture / ablation / comparator) |
| `SPEC-20260507-002-dream3r-ablation-plan-v03-addendum.md` | Dream3R ablation plan v0.3 delta addendum on SPEC-005 (v0.2). Adds ABL-v02-10 Test3R-alone comparator (Tier 1; Q1 from comparator map; tests whether Test3R built-in verifier matches Dream3R Critic-gate pipeline on pillar A; 3 outcome scenarios; ~120 GPU-hours). Pillar A falsification coverage map (4 sub-claims × primary ABL; RA-07 from Path C Agent B). ABL-v02-4 VGGT offline-batch baseline annotation (Q2; Variant X; ~20 GPU-hours). Updated tier placement + compute budget ~1377 GPU-hours. SPEC-005 v0.2 body NOT modified (cycle 023 S3) |
| `SPEC-20260508-001-dream3r-c2-memory-v03-addendum.md` | Dream3R C2 Memory v0.3 architecture addendum. Supersedes SPEC-20260506-004 Delta 3 as current C2 memory design: vector GRU + vector AnchorBank + NSA-label becomes latent state-token recurrence + explicit spatial key/value memory + geometry-aware bus-gated writes. Reinterprets compressed/selected/sliding branches as CUT3R-like state tokens / Spann3R-like spatial bank / recent frame-value tokens. Adds state schema, bus publications/reads, prototype sequence P0-P5, memory-specific ablation candidates, risks, and paper evidence-boundary correction. Markdown only; no implementation authorized (cycle 026 S3) |
| `SPEC-20260508-002-dream3r-memory-v03-ablation-addendum.md` | Cycle 028 Memory v0.3 ablation addendum, reviewed and corrected in cycle 029. Maps P0 variants V0-V3 and claims C2M-C1..C2M-C11 to ABL-memory-0..11. Separates P0 tensor-only tests from future module/integration tests. Cycle 029 v1.1 adds oracle-bus boundary, hard/soft fail rule, narrowed C2M-C1/C8, and stronger ABL-memory-3. Engineering plan only; no implementation authorized |
| `SPEC-20260522-001-dream3r-v05-axes.md` | Cycle 043 deliverable: Dream3R v0.5 axes spec (candidate-not-final per DEC-20260501-004). Closes the v0.4 explicit stub / fallback / proxy / contract-only surface as 8 axes A1-A8 (A1 DINOv3-S backbone real / A2 Composer adapter real-checkpoint loading per-adapter / A3 Permanence dynamic_mask_proxy → D2 promotion + CR-2 v2.2 / A4 VGGT adapter + capability_card v2.2 / A5 Test3R as Critic-triggered off-path with new action code / A6 NSA sliding branch utility verification on longer KITTI / A7 GaussianHead conditional main-forward entry — explicitly kept deferred / A8 tttLRM-style long-context A1 sub-action design). Each axis carries explicit `closes_iff` + required actions + dependencies + non-promises + evidence label. v0.5 is additive to v0.4 by default; v0.3 main forward stays byte-identical unless an axis closure DEC says otherwise. Consumes `SOTA_FEATURE_MATRIX.md` Gap Report; reads from `ARCHITECTURE_V04_STATUS.md` |
| `SPEC-20260527-001-dream3r-state-conditioned-reconstruction.md` | 2026-05-27 architecture addendum after Stage 6 baseline pathology and user route adjustment. Demotes hard expert selection / best-of-N Composer from headline claim to proposal-prior / diagnostic-baseline role. Defines state-conditioned reconstruction as the post-midterm mainline: expert proposal bank + Memory / AnchorBank / NSA / Permanence / Critic state directly condition final pointmap via fusion/correction. Adds A9 real-backend guardrail, A10 multi-expert proposal bank, A11 long-sequence state objective, and L0-L4 roadmap |

### `literature/` - Paper artifacts

| File | Description |
|---|---|
| `PAPER_DRAFT_V1.md` | Dream3R paper draft v1.2 (cycle 022 update). §1-2, §4-8 = v0.1 cycle 017 baseline. §3.8 NEW: six v0.2 architecture deltas (Delta 1 frame budget / Delta 2 DINOv3-S / Delta 3 NSA anchor bank / Delta 4 attention regime / Delta 5 7-expert pool / Delta 6 A+D pillar narrowing). §6.0–6.3 NEW: v0.2 comparator positioning (5-tier pool / A+D threat table / 3 new axes). §6.4 = v0.1 threat table preserved. Source: SPEC-004 (§3.8) + SPEC-20260507-001 (§6). Per DEC-20260507-002 (cycle 022) |

### `storyboards/` - Teacher Demo Storyboards

Format: `STORY-YYYYMMDD-NNN-<slug>.md`. One file per finalist teacher demo. Created via `templates/demo_storyboard.md`. Drafting a storyboard does NOT authorize showing; showing requires a separate DEC per `AGENT_MASTER_PROMPT.md` section 6.

| File | Finalist | Status | Role |
|---|---|---|---|
| `STORY-20260505-001-critic.md` | Geometry Critic (SPEC-20260503-001) | draft | D3 first teacher demo target per DEC-20260505-001 (1); three placeholder panels on CRITIC-02 Fast3R-vs-Spann3R regime; locked surprise hook "Catch a near-failure and repair it on the spot"; showing NOT authorized |
| `STORY-20260505-002-memory.md` | Executive Memory (SPEC-20260503-002) | draft | cycle 012 (e); three placeholder panels on MEMORY-01 MonST3R 48-frame regime; locked surprise hook "Memory that knows what to drop survives a walk where memory that keeps everything drowns"; showing NOT authorized |
| `STORY-20260505-003-permanence.md` | Dynamic Object Permanence (SPEC-20260503-003) | draft | cycle 012 (e); three placeholder panels on PERMANENCE-01 + 02 + 03 portfolio; locked surprise hook "Watch the static map stay clean while the scene moves"; showing NOT authorized |
| `STORY-20260505-004-composer.md` | 3R Composer (SPEC-20260504-001) | draft | cycle 012 (e); three placeholder panels using COMPOSER-04 KYKT-metadata-derived capability_card scoreboard; locked surprise hook "Same reconstruction, less compute — when two models tie, pick the cheaper one"; showing NOT authorized |

### `registry/` - Lightweight Indexes

| File | Role |
|---|---|
| `source_registry.md` | Source ID -> title/url/track/evidence map |
| `research_unit_registry.md` | RU ID -> name/track/decision map |
| `decision_registry.md` | DEC ID -> scope/decision/status map |

### `templates/` - Reusable Forms

| File | Role |
|---|---|
| `source_card.md` | Source intake form |
| `research_unit.md` | Dream Research Unit form |
| `decision_memo.md` | Decision memo form |
| `cycle_log.md` | Cycle log form |
| `experiment_plan.md` | Experiment plan form |
| `frontend_design_handoff.md` | Frontend task brief form for Gemini CLI |
| `proxy_case_card.md` | Branch-neutral L2 proxy case-card form (P1-P8) |
| `finalist_mechanism_spec.md` | Branch-neutral mechanism spec form (requires user approval) |
| `demo_storyboard.md` | Branch-neutral teacher demo storyboard skeleton; filling does not authorize showing |

## Find By Question

| Question | Where to look |
|---|---|
| What phase are we in? | `WORKFLOW_STATUS.md` |
| What is the next user decision? | `WORKFLOW_STATUS.md` -> Recommended Next User Decision; current default after cycle 040 close is one of: A. launch cycle 041 § 9 风险分析 + 通稿审查 + STYLE_CONTRACT final sync (recommended; last remaining chapter; ~2500 字 total) / B. revise § 5 + § 7 + § 8 based on self-review or advisor feedback / C. launch cycle 035 §Next Direction A-C (calibration / long-seq ablation / v0.4 spec delta) / D. pause + reassess after § 5 + § 7 + § 8 quality review / E. user executes Track B survey submission (SHA256 pre-filled) / F. return to architecture-first mainline non-proposal work |
| What sources do we know about? | `sources/FRONTIER_SOURCE_MAP.md` and `registry/source_registry.md` |
| What ideas are on the table? | `units/RESEARCH_UNIT_BANK.md`, `units/IDEA_SCOREBOARD.md` |
| Why this branch and not that one? | `planning/BRANCH_COMPARISON_MATRIX.md`, `planning/BRANCH_SHORTLIST_DECISION_SURFACE.md` |
| Which branches are user-approved finalists, and what are their specs? | `specs/` (one file per finalist) |
| What can Dream do without asking the user? | `AGENT_MASTER_PROMPT.md` section 6 |
| What requires user approval? | `AGENT_MASTER_PROMPT.md` section 6 + `WORKFLOW_STATUS.md` Blocked Until User Decision |
| How should I behave when synthesizing or editing files? | `paradigm/RESEARCH_CODE_DISCIPLINE.md` |
| What is the latest research result? | newest file under `cycles/`; current latest is `cycles/CYCLE-20260517-001.md` (cycle 040 done; Dream3R 开题报告 § 5 实验设计与评测协议 + § 7 研究进展与已完成工作 + § 8 研究计划与时间安排 dual-draft 起草 ~2800 内 + ~2000 外 字 (§5) + ~2200 内 + ~1500 外 字 (§7) + ~1500 内 + ~1000 外 字 (§8); § 1 + § 2 + § 3 + § 4 + § 5 + § 6 + § 7 + § 8 累计 ~17800 内 + ~14000 外 字 ≈ 85% target; only § 9 remains for cycle 041; STYLE_CONTRACT §2 vocab table 43→48 rows; §6 sync log appended; G3a + G3b 5 corrective edits on first pass (4 "cycle"-leak + 1 lowercase "dream3r" repo-name leak), G4 0 hits on first pass; preceded by cycle 039 § 3 + § 6 dual-draft + cycle 038 § 4 dual-draft + cycle 037 § 2 dual-draft + cycle 036 advisor packaging + dual-draft kickoff + cycle 035 survey-driven markdown deliverables) |
| What did we decide? | `registry/decision_registry.md` and files under `decisions/` |
| What experiments are planned or locally scaffolded? | files under `experiments/` plus C2 v0.3 prototype sequence in `specs/SPEC-20260508-001-dream3r-c2-memory-v03-addendum.md`, P0 plan in `planning/MEMORY_V03_P0_PROTOTYPE_PLAN.md`, reviewed ablation map in `specs/SPEC-20260508-002-dream3r-memory-v03-ablation-addendum.md`, review in `planning/MEMORY_V03_ABLATION_REVIEW.md`, execution template in `planning/MEMORY_V03_P0_EXECUTION_DEC_TEMPLATE.md`, and local `ABL-memory-0` scaffold under `experiments/prototypes/memory_v03_p0/`; later ablations still require separate DEC + per-step gate |
| How should the frontend agent work? | `handoff/FRONTEND_DESIGN_HANDOFF_PROMPT.md` |
| How do humans and agents cooperate? | `handoff/COLLABORATION_ROADMAP.md` |

## Convention Reminders

- Evidence labels: `paper-proven`, `code-observed`, `engineering-demonstrated`, `demo-observed`, `inferred`, `speculative`, `unknown`.
- Decision approval gates: see `AGENT_MASTER_PROMPT.md` section 6.
- ID format: `SRC-YYYY-NNN`, `MECH-YYYY-NNN`, `RU-NNN`, `DEC-YYYYMMDD-NNN`, `EXP-YYYYMMDD-NNN`, `CYCLE-YYYYMMDD-NNN`, `CASE-YYYYMMDD-NNN`, `SPEC-YYYYMMDD-NNN`.
- Guidance file sync rule: when promoting a workflow artifact, also update `AGENT_MASTER_PROMPT.md`, `README.md`, `WORKFLOW_STATUS.md`, `RESEARCH_STATE.md`, current cycle log.
