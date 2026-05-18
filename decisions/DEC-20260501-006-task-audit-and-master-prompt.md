# DEC-20260501-006: Task Audit And Master Prompt

Date: 2026-05-01

Status: accepted

## Context

The user asked to review the recent Dream workflow work for omissions or poor judgment, then create a reusable master prompt for future agents. The prompt should evolve with project progress and force agents to use the Dream markdown files and future skills to advance the work systematically.

## Audit Findings

### Finding 1: Canonical Entry Point Was Missing

Issue:

- `archive/MASTER_RESEARCH_PROMPT_DRAFT.md` existed, but it was still a broad early draft.
- It did not clearly specify load order, workflow modes, update rules, decision gates, or how an agent should use the surrounding Dream files.

Correction:

- Create `AGENT_MASTER_PROMPT.md` as the canonical entry prompt.
- Keep the old draft only as historical material unless explicitly revived.

### Finding 2: Decisions Directory Was Underused

Issue:

- The `decisions/` directory existed, but no decision memo had been written inside it.
- The decision registry pointed to top-level files only.

Correction:

- Add this memo as the first concrete decision file under `decisions/`.
- Update `registry/decision_registry.md`.

### Finding 3: Reproduction Planning Could Be Misread As Reproduction Commitment

Issue:

- `experiments/EXP-20260501-001-dust3r-splatt3r-smoke-plan.md` is only a plan, but its presence could be mistaken by a future agent as permission to run it.

Correction:

- The master prompt must explicitly say planned experiments are not execution approval.
- Actual cloning, installation, checkpoint download, or smoke test execution still requires user confirmation.

### Finding 4: Dream3R Naming Could Look Too Final

Issue:

- `Dream3R` is currently a useful umbrella name, but repeated mention could make it feel like the final thesis.

Correction:

- The master prompt must preserve `Dream3R` as a candidate thesis only.
- Final thesis selection remains a user decision gate.

### Finding 5: Source Registry Is Seeded, Not Fully Audited

Issue:

- Some source readiness/license/checkpoint fields are based on README/project-page passes and subagent findings.
- They should not be treated as legal or engineering certainty.

Correction:

- Master prompt requires evidence labels and file-level verification before public use, heavy reproduction, or external presentation claims.

## Decision

Create `AGENT_MASTER_PROMPT.md` as the canonical prompt for future agents.

The prompt must:

- begin with a mandatory file-loading protocol
- enforce Dream's workflow and decision gates
- instruct agents to update itself when project state changes
- separate source evidence from inference
- prevent premature reproduction
- tie every action back to KYKT/Dream outputs

## User Approval Required

No approval required for creating the prompt and updating references.

Approval still required for:

- running model reproduction
- downloading large checkpoints
- changing KYKT app navigation
- final thesis selection
- packaging a reusable Codex skill

## Next Action

Create and reference `AGENT_MASTER_PROMPT.md`.

