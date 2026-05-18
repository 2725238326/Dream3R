# DEC-20260501-009: Backend-First Correction

Date: 2026-05-01

Status: superseded by DEC-20260501-010.

## Context

The user corrected the collaboration direction:

```text
我们后端为主，前端这个又不是核心，你别跑偏了
```

The previous roadmap correctly delegated frontend implementation to Gemini CLI, but its recommended next step used "research-lane data model" wording that could still over-emphasize a UI lane.

## Decision

Historical decision:

```text
Place backend/research-pipeline work before frontend work when integration becomes necessary.
```

Superseding clarification:

```text
Dream is research-content-first.
Backend/research-pipeline work is support infrastructure when integration becomes necessary.
```

Frontend remains a downstream presentation layer and is not the current core.

## Practical Rule

Prioritize:

- research data contracts
- backend-owned registries
- source / Research Unit / decision / experiment schemas
- API and task boundaries
- state machines and status transitions
- automation hooks for future agents
- evidence and artifact storage rules
- backend readiness for future KYKT integration

Deprioritize for now:

- frontend UI implementation
- visual polish
- navigation changes
- Gemini CLI tasks unless a backend contract already exists

## Corrected Next Action

Historical corrected action, now superseded by DEC-20260501-010:

Replace:

```text
KYKT research-lane data model
```

with:

```text
Backend research pipeline contract, no UI.
```

Current action after DEC-20260501-010:

```text
Research content / Dream3R thesis validation cycle.
```

## User Approval Required

No approval is needed to correct wording and planning documents.

Approval remains required before:

- backend implementation that changes existing KYKT services
- database or persistence changes
- model reproduction
- heavy downloads
- frontend implementation
