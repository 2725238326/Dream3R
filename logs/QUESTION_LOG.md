# Dream Question Log

Last updated: 2026-05-04 (cycle 008.5: catchup gap note added; Round 10 cycle 008.5 autonomy turn appended)

## Catchup Gap Note (2026-05-04)

This log captures user-facing questions and decisions as numbered Rounds. Between Round 9 (cycle 003 era) and Round 10 (cycle 008.5), several substantive cycles closed without a new Round entry because their decisions were captured in `decisions/DEC-*` memos, cycle logs under `cycles/`, and `RESEARCH_STATE.md` rather than as a single user question.

For audit completeness, the user-direction events between Round 9 and Round 10 are summarized below; each links to the canonical decision memo or cycle file. None of these supersede prior Rounds.

| Cycle | Date | User direction (one-liner) | Canonical artifact |
|---|---|---|---|
| 004 | 2026-05-01 | first multi-track-before-bet posture | `decisions/DEC-20260502-001-multi-track-before-bet.md` |
| 005 | 2026-05-02 | source mining beyond direct 3R; cover visual / depth / active perception / event priors | `sources/FRONTIER_SOURCE_MAP.md` (Cycle 005 Source Mining Pass section) |
| 006 | 2026-05-02 | workspace reorganization to topical subdirectories + archive/ + INDEX.md | `decisions/DEC-20260502-005-workspace-reorganization.md` |
| 007 | 2026-05-03 | research and code discipline rulebook | `decisions/DEC-20260503-001-research-code-discipline.md`, `paradigm/RESEARCH_CODE_DISCIPLINE.md` |
| 008 | 2026-05-03 | finalist shortlist approval (option B; three finalists) | `decisions/DEC-20260503-002-finalist-shortlist-approval.md` |
| 008.5 | 2026-05-04 | composer upgrade + no-all-in posture + literature board | `decisions/DEC-20260504-001-composer-finalist-upgrade.md`, `decisions/DEC-20260504-002-no-all-in-on-single-finalist.md`, `cycles/CYCLE-20260504-001.md` |

This Catchup Gap Note is documentation-only; no Round numbers are renumbered (per `paradigm/RESEARCH_CODE_DISCIPLINE.md` rule 3, no retro-renumber). Future cycles should add Round entries when the cycle introduces a user-facing question rather than a derivative decision memo.

## Round 1

Question: What kind of teacher-facing surprise should the research aim for?

Answer:

- Architecture-level innovation is the priority.
- Cross-modal / new-technology fusion is allowed.
- The work should eventually support paper writing, demo presentation, and KYKT app integration.
- Engineering cost should be light to medium unless the idea clearly deserves more.
- Final naming can wait.

## Round 2

Question: What should the research engine support?

Answer:

- The workspace should be created under `E:\kykt` as `Dream`.
- The desired output form is mixed: architecture story, demo, proposal, and KYKT integration.
- Memory/state, model composition, reasoning/test-time compute, and continual/lifelong learning should all remain open.
- GitHub and paper mining should be fused and adaptive.
- KYKT should eventually contain research idea, fast reproduction, prototype, paper workbench, and long-term work-management areas.
- Evidence standards should be chosen case-by-case using a ladder from mock demo to quantitative metrics.
- Research rules should exist both in the project and later as a reusable Codex skill.

## Next Round Candidate

## Round 3

Question: What should Dream optimize for first: breadth of idea discovery, depth of one architecture route, or a teacher-facing demo path?

Answer:

- Choose a balanced two-track plan.
- Establish a strong research paradigm first, because later results will be weak without it.
- Important decisions should be discussed with the user rather than silently committed.

Decision:

```text
Dream Phase 1 = Breadth Map + Minimal Demo.
```

## Next Round Candidate

## Round 4

Question: Should Dream now arrange a comprehensive research route survey and planning step for the discussed content?

Answer:

- Yes. This step is critical.
- Build the research paradigm and planning scheme first.
- Continue to discuss important decision points with the user.

Decision:

```text
Create Phase 1 research route survey plan.
```

Output:

- `archive/PHASE1_RESEARCH_PLAN.md`

## Round 5

Question: Should Dream start model reproduction now?

Answer:

- No.
- Deploy the research process first.

Decision:

```text
Phase 1.5 = Research Workflow Deployment.
```

Output:

- `paradigm/RESEARCH_WORKFLOW.md`
- `paradigm/RESEARCH_DATA_MODEL.md`
- `WORKFLOW_STATUS.md`
- registries, templates, cycle log, and planned-only experiment file

## Round 6

Question: Did the prior work miss anything or make weak judgments, and should we create a reusable master prompt for agents?

Answer:

- Yes, audit the prior work.
- Create a master prompt that is updated as the project progresses.
- The prompt should force agents to use the Dream markdown files, future skills, and workflow rather than proceeding ad hoc.

Decision:

```text
Create AGENT_MASTER_PROMPT.md as the canonical entry prompt.
Keep archive/MASTER_RESEARCH_PROMPT_DRAFT.md as historical only.
```

Output:

- `AGENT_MASTER_PROMPT.md`
- `decisions/DEC-20260501-006-task-audit-and-master-prompt.md`

## Next Round Candidate

The next useful question is:

```text
Should the next workflow lane be backend research pipeline contract, deeper prompt/rules refinement, planned-only smoke-test details, or a second Dream3R thesis research cycle?
```

Historical correction after user feedback, later superseded by Round 8:

```text
Backend/research pipeline is prioritized over frontend when system integration is needed. Frontend is downstream only.
```

## Round 7

Question: Who should own KYKT frontend design tasks going forward?

Answer:

- Frontend design / implementation tasks should still be handled by another agent, specifically Gemini CLI or a designated frontend implementation agent.
- Dream / Codex should only emphasize, arrange, and maintain the frontend design prompt and task constraints.

Decision:

```text
Gemini CLI owns KYKT frontend implementation by default.
Dream / Codex owns frontend handoff prompts, constraints, sequencing, and acceptance criteria.
```

Output:

- `handoff/FRONTEND_DESIGN_HANDOFF_PROMPT.md`
- `templates/frontend_design_handoff.md`
- `decisions/DEC-20260501-007-frontend-agent-boundary.md`

## Round 8

Question: Is the app/backend track the mainline, or only a support layer?

Answer:

- The app is only one part.
- The mainline is still researching new content, new mechanisms, and new directions.
- Backend-first should only mean backend before frontend when app integration becomes necessary.

Decision:

```text
Dream is research-content-first.
Backend, app, and frontend are supporting layers.
```

Output:

- `paradigm/RESEARCH_CONTENT_ROADMAP.md`
- `decisions/DEC-20260501-010-research-mainline-correction.md`

## Round 9

Question: Should Dream continue as a linear branch-selection process, or as a nonlinear graph-like research structure?

Answer:

- Many mentioned, unmentioned, or undiscovered modules, papers, techniques, and compositions may become useful at different stages.
- A nonlinear graph or higher-dimensional structure is more suitable than prematurely betting on one branch.
- If writing a top-conference paper, start from field-level problem formulation and mechanism graph, not a single model name.

Decision:

```text
Dream should use a failure-mode / mechanism / composition / evidence graph.
Fill branch comparison before deepening any single thesis branch.
```

Output:

- `planning/RESEARCH_GRAPH_AND_PAPER_START.md`
- `planning/BRANCH_COMPARISON_MATRIX.md`
- updated `AGENT_MASTER_PROMPT.md` short invocation

## Round 10

Question: Cycle 008.5 contains four user direction inputs in one session — D2 upgrade ("决策2改成升格吧，因为确实有效果"), no-all-in posture ("我觉得记忆系统啥的只是我们借鉴优点的一个部分，我觉得不能all in"), tempo acceleration ("全力提速了"), and the literature-guidance-board request. Should these be treated as one collapsed Round, or split into separate Rounds, given they were issued back-to-back in a single autonomy window?

Answer (recorded post-cycle for the audit trail):

- Treat them as one collapsed Round 10 with four sub-items, because they were issued in a single user-direction block and the agent processed them inside a single sub-cycle (008.5).
- Splitting into four Rounds would break the one-Round-per-user-question convention by inflating numbering on derivative items (no-all-in is derivative of the finalist set; tempo is a process directive, not a research question).
- The four sub-items are still individually traceable via the canonical decision memos and the cycle 008.5 closeout, so the audit trail is intact.

Decision:

```text
Round 10 = cycle 008.5 user direction block, captured here as one Round with four
sub-items. Future cycles return to one-Round-per-user-question. The Catchup Gap
Note above documents Rounds 4-8 events that happened without dedicated Round
entries; that approach is acceptable when the cycle is purely derivative.
```

Sub-items:

1. **D2 upgrade**: Composer SPEC-20260504-001 drafted; finalist set grows from three to four. Canonical: `decisions/DEC-20260504-001-composer-finalist-upgrade.md`.
2. **No-all-in posture**: D3 (first teacher demo target) deferred until cycle 009 case-card data exists AND `paradigm/TEACHER_AUDIENCE_PROFILE.md` is populated; memory and other finalists are borrowable components, not the thesis spine. Canonical: `decisions/DEC-20260504-002-no-all-in-on-single-finalist.md`.
3. **Tempo acceleration**: cycle 008.5 closes as a single sub-cycle rather than a multi-cycle plan; supporting infrastructure (cross-spec contract, literature board, demo storyboard template, teacher audience profile placeholder, work risk register) lands in the same pass. Canonical: `cycles/CYCLE-20260504-001.md` Goal section.
4. **Literature guidance board**: existing source files are inventories, not guidance; the literature directory is created with one INDEX, four SPINE files (one per finalist), one CRITICAL_NOTES, and one PAPER_RELATED_WORK_SKELETON. Canonical: `literature/INDEX.md` (and the four SPINE files alongside it).

Output:

- `decisions/DEC-20260504-001-composer-finalist-upgrade.md`
- `decisions/DEC-20260504-002-no-all-in-on-single-finalist.md`
- `specs/SPEC-20260504-001-3r-composer.md`
- `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md`
- `paradigm/TEACHER_AUDIENCE_PROFILE.md` (placeholder; user must populate to unblock D3)
- `literature/INDEX.md`, `literature/SPINE_CRITIC.md`, `literature/SPINE_MEMORY.md`, `literature/SPINE_PERMANENCE.md`, `literature/SPINE_COMPOSER.md`, `literature/CRITICAL_NOTES.md`, `literature/PAPER_RELATED_WORK_SKELETON.md`
- `templates/demo_storyboard.md`
- `planning/WORK_RISK_REGISTER.md`
- `cycles/CYCLE-20260504-001.md`
- registry / inventory sync: `registry/source_registry.md` (SPINE Anchor Map), `sources/FRONTIER_SOURCE_MAP.md` (SPINE Anchor Map), `units/REPRODUCTION_READINESS_MATRIX.md` (cycle 008.5 dormancy + finalist mapping + cycle 008 source-mining P3 additions)

Open questions surfaced by this Round (not yet user-decided; surfaced in `WORKFLOW_STATUS.md` Recommended Next User Decision):

```text
1. Cycle 009 ordering: Composer case cards parallel with Critic, or sequential after Critic's first card lands.
2. Composer capability card source: paper-derived only (default) vs paper-derived + KYKT-job-derived.
3. Teacher audience profile: user must populate paradigm/TEACHER_AUDIENCE_PROFILE.md to unblock D3.
4. Cycle 009 launch authorization: confirmation requested before cycle 009 starts.
```

These four points carry into Round 11 (whenever the user lands the next user-direction block).
