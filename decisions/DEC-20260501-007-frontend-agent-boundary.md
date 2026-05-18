# DEC-20260501-007: Frontend Agent Boundary

Date: 2026-05-01

Status: accepted

## Context

The user clarified that KYKT app frontend design tasks should continue to be completed by another agent, specifically Gemini CLI or a designated frontend implementation agent.

Dream / Codex should not take over frontend implementation by default.

## Decision

Frontend design and implementation ownership:

```text
Gemini CLI / designated frontend implementation agent
```

Dream / Codex ownership:

```text
Research process, product framing, design task prompt, constraints, acceptance criteria, and handoff sequencing.
```

## Practical Rule

When KYKT frontend work is needed:

1. Dream / Codex writes or updates a frontend design handoff prompt.
2. The prompt must include required reading, target surfaces, design constraints, functional/placeholder boundaries, and acceptance criteria.
3. Gemini CLI or the designated frontend agent performs the UI implementation.
4. Dream / Codex may review the result or prepare the next prompt, but does not edit frontend code unless the user explicitly asks it to.

## User Approval Required

No approval is required to maintain frontend handoff prompts.

User approval is required before:

- Codex edits frontend code directly
- KYKT navigation or information architecture changes
- Gemini CLI is instructed to perform a major redesign

