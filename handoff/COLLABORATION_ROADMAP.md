# Dream Collaboration Roadmap

Last updated: 2026-05-01

Status: active collaboration plan.

## Purpose

This document defines how the user and Dream / Codex should collaborate step by step.

The goal is not to produce one large brainstorm and stop. The goal is to run a repeatable research process that can gradually become:

- a credible research direction
- a teacher-facing demo plan
- a supportable KYKT backend integration plan
- future reproduction / prototype work
- eventually a paper/proposal base

## Roles

### User

Owns:

- research ambition and taste
- final thesis decisions
- teacher-facing priorities
- cost / time tolerance
- approval for reproduction, downloads, training, and app changes

Best use of user time:

- answer high-leverage questions
- choose between 2-4 concrete routes
- inject new ideas, constraints, or teacher preferences
- review decision memos before commitment

### Dream / Codex

Owns:

- research controller role
- file and process maintenance
- source-to-mechanism translation
- Research Unit creation
- scoring, pruning, and decision memo drafting
- research-content roadmap and thesis validation cycles
- backend/research pipeline contracts only as support infrastructure
- frontend handoff prompts for Gemini CLI only when a UI task is actually needed
- planned-only experiment briefs

Codex should not:

- run heavy reproduction without approval
- implement KYKT frontend by default
- finalize the thesis silently
- collapse the work into a single repo or buzzword

### Gemini CLI / Frontend Agent

Owns:

- KYKT frontend design implementation
- UI code changes
- build validation
- frontend implementation summary

Dream / Codex prepares the prompt and acceptance criteria.

### Future Reproduction Agent

Owns:

- local repo setup
- checkpoint download
- smoke test execution
- environment and artifact logging

This agent is used only after user approval.

## Collaboration Loop

Use this loop for every meaningful research push:

```text
1. User intent
2. Codex frames the task and reads Dream state
3. Codex updates or creates a cycle file
4. Codex gathers / organizes evidence
5. Codex converts evidence into Research Units or decisions
6. Codex asks for user decision only at real commitment points
7. User chooses route / gives new ideas
8. Codex updates state, registries, prompt, and next plan
```

## Cycle Types

### Type A: Thinking / Direction Cycle

Use when:

- choosing the research direction
- comparing possible theses
- turning broad ideas into structured units

Outputs:

- updated `units/RESEARCH_UNIT_BANK.md`
- updated `units/IDEA_SCOREBOARD.md`
- decision memo if a route should be chosen

### Type B: Source / Literature Cycle

Use when:

- mining new papers, GitHub repos, or architecture ideas
- updating source map

Outputs:

- `sources/FRONTIER_SOURCE_MAP.md`
- `registry/source_registry.md`
- cycle log
- new or updated RUs

### Type C: KYKT Integration Planning Cycle

Use when:

- mapping Dream research into KYKT app surfaces
- planning research lane, data model, reports, advisor, or management area

Outputs:

- data contract draft
- frontend handoff prompt for Gemini CLI if UI is needed
- no frontend implementation by Codex unless explicitly requested

Rule:

- this cycle is downstream of the research question; it must not replace source mining, mechanism synthesis, or thesis validation.

### Type D: Experiment Planning Cycle

Use when:

- planning a smoke test or prototype
- preparing reproduction without running it

Outputs:

- `experiments/` plan
- success criteria
- stop conditions
- approval required flag

### Type E: Execution Cycle

Use only after approval.

Outputs:

- smoke-test result
- artifact log
- failure log
- updated readiness matrix

## Research Conversation Pattern

Prefer short high-signal rounds.

Each round should end with one of:

```text
continue_exploring
needs_user_decision
ready_for_handoff_prompt
ready_for_planned_experiment
ready_for_reproduction_approval
defer
reject
```

## Question Style

Codex should avoid asking too many low-level questions.

Ask the user only when the answer changes direction or cost:

- Which thesis should be emphasized?
- Which demo surface matters most for the teacher?
- Is a heavy reproduction now worth the time?
- Should a KYKT navigation/page change be authorized?
- Should a major track be discarded?

Codex should decide without asking for:

- document organization
- registry updates
- scoring refinements
- prompt wording improvements
- cycle logging

## Near-Term Deployment Path

The next work should unfold in five steps.

### Step 1: Collaboration Protocol

Status:

```text
active now
```

Goal:

- make the workflow usable for repeated human-agent collaboration

Outputs:

- this roadmap
- cycle log
- decision registry update

### Step 2: Research Content / Thesis Validation Cycle

Goal:

- stress-test and expand the research content itself before system work dominates the project

Questions:

- What is genuinely new against CUT3R / Point3R / STream3R / TTT3R / LoGeR / Mem3R and adjacent 3R work?
- Which new non-3R mechanisms can become credible 3R hypotheses?
- Which part is paper-grade, demo-grade, or only speculative?
- What would surprise the teacher because it opens a direction rather than merely integrates tools?

Likely outputs:

- thesis comparison matrix
- updated Research Units and scores
- novelty/risk/evidence table
- decision memo for the next research branch

No reproduction yet.
No app code changes yet.

### Step 3: Backend Research Pipeline Contract

Goal:

- define what Dream should expose to KYKT backend/services after the research content needs a durable system layer

Outputs:

- backend-owned schemas for source / mechanism / RU / score / decision / experiment
- status transitions and lifecycle rules
- file-backed or service-backed storage plan
- API/task boundary draft for future KYKT integration
- artifact and evidence reference rules

No frontend work yet.

### Step 4: Teacher-Facing Storyboard

Goal:

- translate the research program into a convincing teacher-facing narrative

Outputs:

- 5-8 minute presentation skeleton
- demo storyboard
- claims / evidence / risk table

No claim of demo readiness yet.

### Step 5: Planned Experiment Selection

Goal:

- decide whether to prepare reproduction approval

Candidate choices:

- DUSt3R stable baseline
- Splatt3R visual surprise
- non-learned geometry critic report
- KYKT research-lane mock data

Output:

- one experiment plan selected for approval or deferred

## Recommended Immediate Next Action

Start with:

```text
Step 2: Research Content / Thesis Validation Cycle
```

Reason:

- research novelty is the mainline; KYKT app and backend are carriers
- it directly addresses the user's teacher-facing surprise goal
- it prevents the workflow from becoming ordinary app engineering
- it still preserves a later path to backend contracts, demos, and Gemini CLI frontend handoff
- it does not require model reproduction

## Current Non-Commitments

Not committed yet:

- final thesis
- model reproduction
- frontend implementation
- teacher demo readiness
- reusable Codex skill packaging
