# DEC-20260501-010: Research Mainline Correction

Date: 2026-05-01

Status: accepted.

## Context

The prior correction properly prevented frontend work from becoming the center of the project, but it overcorrected toward backend/research-pipeline implementation.

The user clarified:

```text
app只是一部分呀，我们的主线还是研究新的内容
```

## Decision

Dream is research-content-first.

The mainline is:

```text
new 3R / spatial-intelligence mechanisms -> thesis validation -> teacher-facing research story -> feasible evidence path
```

Backend, KYKT app integration, and frontend design are support layers.

## Consequences

- The default next step is a research content / Dream3R thesis validation cycle.
- Backend contracts should be drafted when they support a selected research workflow, not as the central task.
- KYKT app planning remains important but downstream.
- Frontend remains delegated to Gemini CLI / designated frontend agent.
- No reproduction or heavy install is implied by this decision.

## Updated Recommended Sequence

```text
1. Collaboration protocol
2. Research content / Dream3R thesis validation cycle
3. Mechanism mining from 3R and adjacent frontier work
4. Backend research pipeline contract as support infrastructure
5. Teacher-facing storyboard
6. Planned experiment selection
```
