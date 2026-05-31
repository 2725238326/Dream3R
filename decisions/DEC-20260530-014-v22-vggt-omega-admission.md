# DEC-20260530-014 — Use VGGT-Omega for v2.2 admission

decision_id: DEC-20260530-014
date: 2026-05-30
scope: Dream3R v2.2 expert admission
status: accepted for research and deployment planning; execution gated

## Context

DEC-20260530-013 narrowed Dream3R's next proposal-bank candidates to
VGGT / CUT3R / MonST3R. The user then pointed out that the newer
VGGT-Omega line is likely the stronger VGGT-family candidate than vanilla
VGGT.

The check performed on 2026-05-30 found the relevant official surfaces:

- VGGT-Omega project page: https://vggt-omega.github.io/
- VGGT-Omega code: https://github.com/facebookresearch/vggt-omega
- vanilla VGGT code: https://github.com/facebookresearch/vggt

This decision treats VGGT-Omega as the admission candidate and keeps vanilla
VGGT as the baseline / compatibility ancestor.

## Decision

For Dream3R v2.2, replace the first admission candidate:

```text
old: VGGT / CUT3R / MonST3R
new: VGGT-Omega / CUT3R / MonST3R
```

Vanilla VGGT remains useful as:

- a baseline in result tables;
- a checkpoint/schema ancestor for adapter work;
- historical context for the existing Composer v2.2 capability-card surface.

It is no longer the preferred first integration target if VGGT-Omega can be
installed and run under the same resource envelope.

## Deconfusion rule

Do not conflate these two names:

| name | role in Dream3R |
| --- | --- |
| VGGT-Omega / VGGT-Ω | v2.2 proposal expert candidate; upgraded VGGT-family reconstruction surface |
| OVGGT | separate 2026 memory/cache comparator about constant-budget cache compression and dynamic anchor protection |

OVGGT stays in the memory/cache comparator lane. It is not the same as
VGGT-Omega and must not be used as a substitute checkpoint.

## Candidate bank after this DEC

Keep the proven proposal bank:

```text
MASt3R / Fast3R / Spann3R
```

Admit next candidates only through contract gates:

```text
P1: VGGT-Omega
P1: CUT3R
P1: MonST3R
```

Keep later comparators separate:

```text
STream3R / InfiniteVGGT / OVGGT / Test3R / TTT3R
```

## Execution gates

VGGT-Omega integration is not authorized by this DEC alone. The next work is
a deployment runbook and adapter contract.

Before any checkpoint download or server run, a follow-up execution DEC must
name:

1. repository path and commit;
2. checkpoint URL / license / storage path;
3. dependency delta versus the existing Dream3R server env;
4. expected output fields that can be normalized to Dream3R proposal cache;
5. one-window smoke command on BUAA-Server GPU 1;
6. fallback exclusion rule so no stub result enters a result table.

## Rejected alternatives

- Keep vanilla VGGT as the main v2.2 candidate: weaker target if
  VGGT-Omega is available, and it would waste the two-day deployment window.
- Treat VGGT-Omega as a final model replacement for Dream3R: unsupported.
  It is a proposal expert / teacher candidate, not the whole Dream3R model.
- Merge OVGGT and VGGT-Omega into one lane: incorrect mechanism mapping.
  OVGGT is a memory/cache comparator; VGGT-Omega is a reconstruction expert
  candidate.

## Next action

Use `specs/SPEC-20260530-004-dream3r-v22-expert-admission.md` and
`planning/DREAM3R_V22_ADMISSION_RUNBOOK.md` to start the deployment research
lane. No broad expert search is needed.
