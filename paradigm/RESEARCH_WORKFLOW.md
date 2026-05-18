# Dream Research Workflow

Last updated: 2026-05-01

Status: active workflow. This document defines how Dream research should run before any heavy reproduction or KYKT app implementation.

## Purpose

Dream is now operated as a research pipeline, not a loose note folder.

The pipeline has five outputs:

1. credible architecture thesis candidates
2. source-grounded research units
3. teacher-facing demo plans
4. backend / KYKT integration decisions as support infrastructure
5. frontend design handoff prompts for Gemini CLI when app UI work is needed

Canonical entry prompt for agents:

```text
E:\kykt\Dream\AGENT_MASTER_PROMPT.md
```

Canonical frontend handoff prompt:

```text
E:\kykt\Dream\handoff\FRONTEND_DESIGN_HANDOFF_PROMPT.md
```

## Operating Principle

Do not jump from paper discovery directly to model reproduction.

Every direction must pass through:

```text
Source -> Mechanism -> 3R Translation -> Research Unit -> Score -> Decision -> Plan -> Implementation
```

## Workflow Stages

### Stage 0: Intake

Goal:

- collect candidate papers, repos, project pages, and architecture ideas
- record source metadata without over-interpreting it

Outputs:

- `registry/source_registry.md`
- raw source notes in `cycles/`

Completion rule:

- each source has URL, year, evidence type, and one-sentence mechanism

### Stage 1: Mechanism Extraction

Goal:

- identify what changes in the computation graph, memory, state, dynamics, sensing, or test-time loop

Outputs:

- mechanism notes in cycle log
- candidate source-to-mechanism mapping

Completion rule:

- each accepted source answers: what state is stored, what compute is avoided, what error mode is corrected, or what signal is added

### Stage 2: 3R Translation

Goal:

- convert external mechanisms into a concrete 3R hypothesis

Outputs:

- one or more Dream Research Units

Completion rule:

- every idea names a 3R bottleneck and a smallest experiment

### Stage 3: Scoring

Goal:

- decide which ideas deserve attention

Outputs:

- updated `units/IDEA_SCOREBOARD.md`
- cycle-specific ranking

Completion rule:

- each idea gets scores for novelty, 3R relevance, bottleneck severity, demo value, feasibility, KYKT fit, paper story, code/data, and shallow risk

### Stage 4: Decision Gate

Goal:

- avoid accidental commitment to a thesis, dependency, or app redesign

Outputs:

- decision memo in `decisions/`

Completion rule:

- one of these statuses is assigned:
  - `explore_next`
  - `prototype_next`
  - `demo_next`
  - `defer`
  - `reject`
  - `needs_user_decision`

### Stage 5: Planning

Goal:

- plan only the next smallest useful action

Outputs:

- `experiments/` plan if implementation is needed
- prompt for another agent if delegated work is needed
- KYKT integration brief if app work is needed

Completion rule:

- plan states inputs, commands or files, expected artifact, risk, and stop condition

### Stage 6: Implementation

Goal:

- only after user approval for heavy or app-impacting work

Outputs:

- local smoke result, app panel, report, or prototype

Completion rule:

- artifact exists and is logged back into Dream

## Cycle Cadence

Use one cycle per research push.

Each cycle should produce:

- 5-15 sources
- 3-8 accepted mechanisms
- 1-4 new or updated Research Units
- one short decision memo
- one next-action recommendation

Do not open a new cycle until the previous cycle has a decision status.

## Current Cycle Policy

Current phase:

```text
Phase 1.5: Workflow Deployment
```

Allowed:

- build registries and templates
- refine prompts and rules
- run research-content and thesis-validation cycles
- prepare Dream backend research pipeline contracts when they support selected research content
- plan smoke tests
- write decision memos

Not allowed without user confirmation:

- cloning or installing heavy model repos
- downloading large checkpoints
- changing KYKT navigation or app architecture
- Codex directly implementing KYKT frontend code
- declaring a final thesis
- discarding major research tracks

## Decision Gates

Ask the user before:

1. final thesis selection
2. first heavy reproduction target
3. first KYKT page/navigation change
4. reusable Codex skill packaging
5. any model training or fine-tuning
6. teacher-demo readiness claim
7. Codex directly editing KYKT frontend code

Proceed without asking for:

- source registry updates
- template edits
- scoring refinement
- prompt/rule refinement
- lightweight research notes

## Workflow Roles

### Main Research Controller

Owns:

- thesis coherence
- research-content priority
- Dream documents
- user decision gates
- final synthesis

### Source Scout

Owns:

- papers and repos
- code/checkpoint/license checks
- evidence labels

### Mechanism Synthesizer

Owns:

- architecture translation
- anti-hype filtering
- research unit drafting

### Demo Planner

Owns:

- smallest visible proof
- KYKT surface mapping
- teacher-facing story
- frontend task handoff brief for Gemini CLI when UI implementation is needed

Must not let demo or app planning replace the research question.

### Verifier

Owns:

- contradiction checks
- evidence vs inference separation
- reproduction risk notes

These roles can be handled by one agent or delegated to subagents when explicitly requested.

## Canonical Files

- `RESEARCH_STATE.md`: current global state
- `paradigm/RESEARCH_PARADIGM.md`: high-level research philosophy
- `paradigm/RESEARCH_WORKFLOW.md`: operational process
- `registry/source_registry.md`: source index
- `registry/research_unit_registry.md`: research unit index
- `registry/decision_registry.md`: decision index
- `cycles/`: per-cycle logs
- `decisions/`: decision memos
- `experiments/`: experiment and smoke-test plans
- `templates/`: reusable forms
- `handoff/FRONTEND_DESIGN_HANDOFF_PROMPT.md`: Gemini CLI / frontend agent handoff prompt
