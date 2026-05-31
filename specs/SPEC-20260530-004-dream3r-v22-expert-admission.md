# SPEC-20260530-004 — Dream3R v2.2 expert admission

status: accepted admission contract; execution gated
date: 2026-05-30
depends_on: DEC-20260530-013, DEC-20260530-014, SPEC-20260530-003

## Purpose

This spec turns the next expert-bank step into a bounded admission process.
Dream3R remains:

```text
proposal encoders + Dream state + state-conditioned reconstruction decoder
```

New external 3R systems are admitted only when they improve the proposal bank
or the Dream3R decoder. They are not allowed to become a loose ensemble or a
new hard-router story.

## Candidate order

| priority | candidate | role | initial verdict |
| --- | --- | --- | --- |
| P1 | VGGT-Omega | upgraded VGGT-family proposal expert / teacher | first deployment research target |
| P1 | CUT3R | persistent-state proposal expert | second target |
| P1 | MonST3R | dynamic-scene pointmap proposal expert | third target |

Vanilla VGGT is a baseline and schema ancestor. OVGGT is a memory/cache
comparator and is not interchangeable with VGGT-Omega.

## Adapter output contract

Each candidate adapter must normalize its native outputs into:

```text
ExpertProposal:
  expert_name: str
  backend: "real" | "fallback" | "stub" | "error"
  version: str
  pointmap: float[N, P, 3]
  confidence: float[N, P, 1]
  optional_depth: float[N, H, W] | null
  optional_camera: object | null
  optional_tracks: object | null
  optional_dynamic_mask: float[N, P, 1] | null
  method_state: object | null
  runtime_ms: float
  vram_mb: float | null
  failure_flags: list[str]
```

Only `backend == "real"` entries may enter admission result tables.

## Cache extension

The proposal cache must support:

```text
proposal_bank:
  mast3r: ExpertProposal
  fast3r: ExpertProposal
  spann3r: ExpertProposal
  vggt_omega?: ExpertProposal
  cut3r?: ExpertProposal
  monst3r?: ExpertProposal

proposal_metadata:
  source_repo
  commit
  checkpoint_id
  adapter_version
  command
  device
  created_at
```

The cache may store candidate outputs separately until the decoder consumes
them. Existing SCF caches must remain readable.

## Admission metrics

A candidate passes only if it improves at least one Dream3R-relevant axis:

| metric | pass meaning |
| --- | --- |
| standalone_abs_rel | candidate is a credible proposal, not just noise |
| oracle_gain_pp | candidate raises best-single or per-patch oracle ceiling |
| patch_oracle_gap_pp | candidate reduces remaining gap for SCF / decoder |
| scf_delta | SCF output improves when the candidate is added |
| decoder_delta | proposal-set decoder improves when the candidate is added |
| temporal_delta | temporal coherence does not degrade |
| scale_drift | scale stability does not degrade |
| runtime_ms / vram_mb | cost is acceptable for the intended experiment scale |

If a candidate is strong standalone but does not improve Dream3R output, keep
it as a comparator or teacher. Do not promote it as an architecture win.

## Candidate-specific expectations

### VGGT-Omega

Expected complement:

- broad feed-forward geometry prior;
- camera / depth / point / track-rich signals if exposed by the upstream API;
- stronger first candidate than vanilla VGGT.

Primary risk:

- output schema may be richer than Dream3R's pointmap cache and require a
  thin normalization layer.

Pass gate:

```text
VGGT-Omega adds oracle ceiling or decoder output beyond MASt3R/Fast3R/Spann3R
without fallback contamination.
```

### CUT3R

Expected complement:

- persistent-state proposal signal;
- external state that can test whether Dream state learns from or competes
  with a stateful expert.

Primary risk:

- stateful execution order and cache serialization may be brittle.

### MonST3R

Expected complement:

- dynamic scene pointmap proposal;
- real dynamic signal for Permanence / Critic arbitration.

Primary risk:

- dynamic-video assumptions may not transfer to the current KITTI/ETH3D
  smoke slices without a better dynamic subset.

## Stop rules

- Stop integrating a candidate if its real backend cannot be verified.
- Stop after smoke if dependency installation breaks the existing SCF env.
- Stop after oracle evaluation if patch-oracle ceiling does not improve.
- Stop after decoder evaluation if no-state catches correct-state.
- Do not edit frozen core files for admission. Use adapters, cache builders,
  and non-core decoder scripts first.

## Immediate deliverable

The next agent should execute the planning lane in
`planning/DREAM3R_V22_ADMISSION_RUNBOOK.md`, starting with VGGT-Omega.
