# CYCLE-20260530 — v2.2 VGGT-Omega admission research

date: 2026-05-30
status: closed for documentation; execution gated

## Trigger

The user asked to switch from vanilla VGGT to the stronger VGGT-Omega line and
to prepare deployment research and documentation before user-assisted
execution.

## Actions

- Added DEC-20260530-014 to lock VGGT-Omega as the first v2.2 admission
  candidate.
- Added SPEC-20260530-004 to define the v2.2 admission contract.
- Added `planning/DREAM3R_V22_ADMISSION_RUNBOOK.md` for the deployment lane.
- Added `handoff/ARCHITECTURE_V08_V22_ADMISSION_AGENT_PROMPT.md` for the next
  agent.
- Updated existing model-first docs so the candidate bank reads
  VGGT-Omega / CUT3R / MonST3R.
- Added registry/source-map entries while preserving vanilla VGGT and OVGGT
  as separate rows.

## Key decision

```text
Use VGGT-Omega as the first v2.2 admission candidate.
Keep vanilla VGGT as baseline / schema ancestor.
Keep OVGGT as a separate memory/cache comparator.
```

## Boundary

No checkpoint was downloaded. No server run was launched. No frozen core file
was edited.

## Next step

Run Stage G1 of `planning/DREAM3R_V22_ADMISSION_RUNBOOK.md`: dependency,
checkpoint, output-schema, and one-window smoke inventory for VGGT-Omega.
