# DEC-20260503-001 Research & Code Discipline

decision_id: DEC-20260503-001

date: 2026-05-03

scope: paradigm / agent behavior

decision: Adopt `paradigm/RESEARCH_CODE_DISCIPLINE.md` as the active behavior rulebook for research synthesis and Dream-driven code, adapted from the four Karpathy CLAUDE.md principles plus a Dream-native Honesty Override.

status: accepted

## Context

Dream's existing operating documents cover *what* to research (`RESEARCH_CONTENT_ROADMAP.md`, `MULTI_TRACK_RESEARCH_CANVAS.md`), *how* to organize the workflow (`RESEARCH_WORKFLOW.md`, `RESEARCH_DATA_MODEL.md`), and *why* the project exists (`RESEARCH_PARADIGM.md`). They do not cover *how an agent should behave* when producing a durable artifact: when to ask, when to push back, when to keep a mechanism small, when to leave adjacent files alone, and how to set falsifiable goals.

This gap matters more than typical product code because:

- the artifacts are markdown across a thick cross-link graph (`paradigm/` ↔ `planning/` ↔ `registries/` ↔ `cycles/`)
- evidence is mostly `inferred` or `speculative`; silent assumptions corrupt the registry
- mechanism specs invite buzzword stacking (Mamba + critic + 4DGS + active perception)
- "improvement" edits to adjacent files easily desync four documents at once
- research success criteria are easy to leave fuzzy ("explore X")

The user pointed at `https://github.com/forrestchang/andrej-karpathy-skills` as a community-distilled set of behavioral rules for LLM coding and asked Dream to add a similar convention.

## Evidence

- Karpathy original X post (cited by the source repo): LLMs make wrong assumptions silently, overcomplicate, drive-by edit unrelated code, and need declarative success criteria.
- Source repo `forrestchang/andrej-karpathy-skills`: distills observations into four principles in a 2.4 KB CLAUDE.md plus a Claude Code skill plugin and Cursor `.mdc`. Tradeoff note: biases caution over speed.
- Dream's existing failure pattern (observable from the registries): the Align3R / CUT3R curope diagnosis was wrong from cycle 003 through cycle 008; only on 2026-05-03 was it corrected. A behavior rule that requires retracted claims to be stated rather than silently overwritten would have surfaced the contradiction earlier.
- Dream's `AGENT_MASTER_PROMPT.md` section 6 already lists "prompt/rule refinement" as not requiring user approval, so this decision falls inside the agent's autonomous scope.

## Options

A. Single new `paradigm/RESEARCH_CODE_DISCIPLINE.md`, wired into the mandatory load protocol.

B. Inline-merge the four principles into `RESEARCH_PARADIGM.md` and `RESEARCH_SKILL_RULES_DRAFT.md`. No new file.

C. Package as a Claude Code skill at `.claude/skills/dream-discipline/SKILL.md`.

D. Defer; rely on `RESEARCH_SKILL_RULES_DRAFT.md` as-is.

## Recommendation

A.

Reasoning:

- A fits Dream's topical structure cleanly. Each `paradigm/` file already has one focused role; adding a discipline file is consistent with that pattern.
- B would extend two already-long files past the point of clear focus and would erase the Karpathy provenance.
- C jumps a gate. `RESEARCH_SKILL_RULES_DRAFT.md` is explicitly draft and packaging-as-a-skill requires user approval per `AGENT_MASTER_PROMPT.md` section 6. The discipline file can be folded into a packaged skill once stable.
- D is the status quo failure mode that motivated this decision.

## Decision

1. Create `paradigm/RESEARCH_CODE_DISCIPLINE.md` adapting Karpathy's four principles into Dream's synthesis context (Think Before Synthesizing, Minimum Viable Mechanism, Surgical Edits, Falsifiable Research Goals) and add a fifth Dream-native Honesty Override.
2. Insert the discipline file at position 9 of the mandatory load protocol in `AGENT_MASTER_PROMPT.md` (between `RESEARCH_SKILL_RULES_DRAFT.md` and `RESEARCH_CONTENT_ROADMAP.md`).
3. Reference the discipline file from `AGENT_MASTER_PROMPT.md` section 11 Tone And Final Response so the Honesty Override is reinforced when an agent writes a final report.
4. Cross-reference from `paradigm/RESEARCH_SKILL_RULES_DRAFT.md` so future skill-packaging work will fold both files together.
5. Apply the Guidance File Sync Rule: update `README.md`, `INDEX.md`, `WORKFLOW_STATUS.md`, `RESEARCH_STATE.md`, the current cycle log, and the decision registry.
6. Do not change any RU, source, mechanism, or branch. Behavior rules should be neutral with respect to the active research content.

## Risks

- The discipline file can be ignored if agents skip the load protocol. Mitigated by also referencing it under `AGENT_MASTER_PROMPT.md` section 11 and from the "most relevant active file" map.
- Adding another file slightly raises the load-protocol read cost. Mitigated by keeping the discipline file ~250 lines and concrete; it is not a re-statement of the workflow.
- Overlap with `RESEARCH_SKILL_RULES_DRAFT.md` may confuse new agents. Mitigated by an explicit cross-reference at the top of both files: the draft is the long-form ruleset; the discipline file is the lighter behavior layer below it.
- Risk that the rules become aspirational instead of enforced. Mitigated by the fail-fast condition recorded in the cycle log: if the next two research cycles still produce > 3-action specs or silent label changes, escalate to inline merge or skill packaging.

## User Approval Required

No.

This decision is an agent-side prompt/rule refinement. `AGENT_MASTER_PROMPT.md` section 6 explicitly lists "prompt/rule refinement" as not requiring user approval. The user request to add a convention is itself the trigger.

The decision does not touch:

- thesis selection
- branch deepening or discarding
- reproduction
- checkpoint downloads
- KYKT navigation
- frontend implementation
- packaging a reusable Codex skill (which still requires approval; this file is positioned to support that future packaging without performing it)

## Next Action

`paradigm/RESEARCH_CODE_DISCIPLINE.md` becomes active immediately. The next research-content cycle (e.g., the eventual A / B / C / D shortlist response) is the first place its effects should be visible: cycle log header with explicit failure mode + owned actions + proxy + fail-fast condition; mechanism specs that constrain owned actions to ≤ 3; cross-file edits limited to Sync-Rule-required files.

If after two cycles the indicators in `paradigm/RESEARCH_CODE_DISCIPLINE.md` "Indicators That The Discipline Is Working" do not improve, revisit options B or C.
