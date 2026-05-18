# DEC-20260501-008: Collaboration Pathway

Date: 2026-05-01

Status: superseded by DEC-20260501-010.

## Context

The user asked to begin thinking through how we should advance and collaborate on the research path.

The project already has:

- Dream workspace
- canonical agent prompt
- research workflow
- data model
- source and research unit registries
- frontend handoff boundary
- planned-only experiment policy

The missing piece is a clear collaboration rhythm.

## Decision Proposal

Run Dream as a staged human-agent collaboration:

```text
User intent -> Codex research control -> cycle artifact -> decision memo -> user steering -> next lane
```

Codex should maintain the process and documents. The user should make high-leverage decisions only when direction, cost, or commitment changes.

## Recommended Near-Term Sequence

This sequence is historical and has been superseded by DEC-20260501-010.

1. Collaboration protocol
2. Backend research pipeline contract
3. Dream3R thesis validation cycle
4. Teacher-facing storyboard
5. Planned experiment selection

## Why This Sequence

- It avoids premature reproduction.
- It avoids premature frontend implementation.
- It gives KYKT backend integration a data/task contract before UI.
- It keeps the candidate thesis under pressure before we present it as a direction.
- It preserves the possibility of a strong demo later.

## User Approval Required

Approval is not required to document this pathway.

Approval is required before:

- moving to model reproduction
- changing KYKT app navigation
- assigning Gemini CLI a major frontend redesign
- finalizing Dream3R as the thesis

## Next Action

Superseded. The current next action is:

```text
Research content / Dream3R thesis validation cycle.
```
