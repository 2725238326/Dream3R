# Research Skill / Rules Draft

Last updated: 2026-05-03

This draft will later become:

1. a project-local Dream research rulebook
2. possibly a reusable Codex skill

A lighter behavior layer sits below this draft:

```text
E:\kykt\Dream\paradigm\RESEARCH_CODE_DISCIPLINE.md
```

`RESEARCH_CODE_DISCIPLINE.md` adapts Andrej Karpathy's four LLM-coding principles
(Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution)
into Dream's synthesis context and adds a fifth Dream-native Honesty Override.
This draft remains the long-form ruleset; the discipline file is what an agent
should mentally pass through before producing a durable artifact.

## Candidate Skill Name

```text
dream-3r-research
```

## Canonical Prompt Dependency

This rules draft depends on:

```text
E:\kykt\Dream\AGENT_MASTER_PROMPT.md
```

Agents should use `AGENT_MASTER_PROMPT.md` as the entry prompt, then use this file as the rulebook that can later become a reusable Codex skill.

Frontend handoff prompt:

```text
E:\kykt\Dream\handoff\FRONTEND_DESIGN_HANDOFF_PROMPT.md
```

Use this when KYKT app frontend design tasks must be handed to Gemini CLI or another frontend implementation agent.

## Candidate Skill Description

Use when working on Dream / KYKT 3R research: frontier 3R model architecture ideation, paper and GitHub mining, architecture synthesis, demo planning, KYKT app integration planning, and teacher-facing research proposal construction.

## Core Behavior

When this skill is active, the agent should:

1. prioritize architecture-level mechanisms over surface-level application ideas
2. map every external idea back to a concrete 3R bottleneck
3. separate evidence from speculation
4. keep engineering cost visible
5. always propose a minimal experiment or demo path
6. maintain a connection to KYKT app integration
7. run Dream as a two-track process: Breadth Map + Minimal Demo
8. follow the Dream workflow before implementation:

```text
Source -> Mechanism -> 3R Translation -> Research Unit -> Score -> Decision -> Plan -> Implementation
```

## User-Discussion Gates

Discuss with the user before:

- choosing the primary research thesis
- committing to one architecture family
- starting heavy training or large data construction
- making major KYKT app information-architecture changes
- packaging the draft rules as a reusable Codex skill
- declaring a teacher demo ready
- discarding a major candidate track
- moving an experiment from `planned` to `running`
- cloning/installing heavy model repositories
- downloading large checkpoints
- Codex directly editing KYKT frontend code
- instructing Gemini CLI to perform a major frontend redesign

Proceed without interruption for lightweight note updates, small prompt refinements, source triage, and mock artifacts.

## Research Intake Rules

For each paper/project:

- Record title, source, year, code availability, and task.
- Extract the mechanism, not only the result.
- Ask: what does this change about memory, compute, geometry, dynamics, sensing, or adaptation?
- Ask: what would happen if this mechanism were inserted into a 3R pipeline?
- Reject items that cannot be translated into a 3R hypothesis.

## GitHub Mining Rules

Search broadly but filter aggressively.

Allowed sources:

- 3R / 3D reconstruction repos
- visual geometry foundation models
- Mamba / SSM / long-context architectures
- residual attention and efficient attention mechanisms
- continual learning
- RL / active perception
- 4DGS / dynamic scene representations
- event camera / sensor fusion

Reject or defer:

- generic LLM tools with no spatial mechanism
- repos with no working code unless the idea is unusually strong
- projects requiring heavy training beyond current resources unless they can be reduced to a small experiment

## Innovation Rules

A good Dream idea should satisfy at least three:

- changes the architecture, not only the UI or dataset
- attacks a known 3R bottleneck
- can be demonstrated with existing or lightly modified code
- produces a clear teacher-facing visual
- can be integrated into KYKT as a lane, runner, report, or comparison surface
- has a plausible paper narrative

## Evidence Ladder

Use the cheapest adequate evidence.

Level 1:

- architecture diagram
- pseudo-code
- synthetic or mock demo

Level 2:

- existing model outputs compared on several KYKT samples
- qualitative screenshots
- failure-case analysis

Level 3:

- modified code path
- prototype module
- small runner integration

Level 4:

- quantitative metrics
- ablation
- runtime/memory analysis

The agent should recommend an evidence level rather than force all ideas to Level 4.

## KYKT Integration Rules

Every candidate should map to at least one:

- `model_registry.py`
- backend runner
- `scene_meta.json` output contract
- Sample Matrix comparison
- Advisor/report workflow
- Overview research lane
- System/deployment readiness view

If no integration path exists, classify as background research.

## Frontend Delegation Rules

KYKT frontend design and implementation are delegated to Gemini CLI / a designated frontend implementation agent by default.

Codex / Dream should:

- write the frontend task prompt
- specify required reading
- define target surfaces and constraints
- define functional vs placeholder boundaries
- define acceptance criteria and build/test commands
- update `handoff/FRONTEND_DESIGN_HANDOFF_PROMPT.md` or a task-specific prompt under `Coding\4.06\vision_ui`

Codex / Dream should not edit frontend code unless the user explicitly asks for direct frontend implementation.

## Anti-Slop Rules

Do not produce only buzzword combinations.

Bad:

```text
Mamba + 3R + world model will solve long video.
```

Better:

```text
Replace temporal attention with a geometry-gated selective state update. The gate is driven by reprojection residual, confidence, dynamic mask, and baseline. The GPU recurrent state remains fixed-size, while scene memory is stored in an external sparse map.
```

## Convergence Rules

Every batch of research should end with:

- one near-term demo candidate
- one architecture candidate
- one long-term speculative candidate
- one rejected/deferred category with reasons

Do not keep expanding the idea pool without pruning.

## Registry Rules

When a research cycle adds durable information, update the registries:

- new paper/repo/project: `registry/source_registry.md`
- new or changed idea: `registry/research_unit_registry.md`
- commitment/defer/reject decision: `registry/decision_registry.md`

If the change is only exploratory, log it in `cycles/` first.

## Experiment Planning Rules

An experiment plan can be drafted without approval.

Actual execution requires approval when it includes:

- heavy repo clone/install
- large checkpoint download
- training or fine-tuning
- external paid service
- KYKT app navigation or information-architecture changes

Experiment plans should live in `experiments/` and include success criteria and stop conditions.

## Future Skill Packaging

When stable, create both:

- project-local rules under `E:\kykt\Dream`
- reusable Codex skill under the Codex skills directory

The reusable skill should stay concise and move long examples into references.
