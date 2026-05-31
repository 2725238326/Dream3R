# SPEC-20260530-005 — Dream3R-PD final architecture

status: accepted final architecture candidate; staged implementation gated
date: 2026-05-30
depends_on: DEC-20260530-011, DEC-20260530-012, DEC-20260530-013, DEC-20260530-014, DEC-20260530-015

## Model identity

Dream3R-PD is:

```text
Proposal-bank Distilled State-Conditioned 3R
```

It is not:

- a hard expert selector;
- a permanent full ensemble;
- VGGT-Omega wrapped with a local head;
- a memory-only architecture.

The final product is a Dream3R-owned reconstruction decoder trained from
proposal teachers and conditioned on Dream state.

## Data flow

```text
images
  -> proposal teachers
       MASt3R / Fast3R / Spann3R
       + admitted VGGT-Omega / CUT3R / MonST3R candidates
  -> proposal cache
  -> Dream state encoder
       memory_context
       anchor_summary
       nsa_summary
       permanence_summary
       critic_reliability
       composer_metadata
  -> proposal-set decoder
  -> final pointmap + confidence + uncertainty + diagnostics
  -> native decoder distillation with proposal dropout
```

## Components

### Proposal teachers

Each teacher must satisfy the `ExpertProposal` contract from
`SPEC-20260530-004`.

Core bank:

| teacher | role |
| --- | --- |
| MASt3R | high-quality static / pairwise proposal |
| Fast3R | many-view feed-forward proposal |
| Spann3R | memory-like global-coordinate proposal |

Admission candidates:

| candidate | role |
| --- | --- |
| VGGT-Omega | stronger VGGT-family global geometry proposal / teacher |
| CUT3R | persistent-state streaming proposal |
| MonST3R | dynamic-scene pointmap proposal |

### Dream state encoder

Input state features:

```text
memory.fused_context
anchor_bank summary
nsa branch weights / retrieval stats
permanence slots / dynamic-mask evidence
critic conflict / confidence / reliability
composer backend / cost / regime metadata
```

Output:

```text
StateTokenSet:
  state_tokens: float[B, S, D]
  reliability: float[B, S, 1]
  diagnostics: dict
```

The first implementation may be a frozen-state projection head outside frozen
core files.

### Proposal-set decoder

Input:

```text
ProposalTokenSet:
  proposal_tokens: float[B, E, P, D]
  pointmaps: float[B, E, P, 3]
  confidences: float[B, E, P, 1]
  expert_metadata: dict

StateTokenSet:
  state_tokens
  reliability
```

Output:

```text
Dream3RDecoderOutput:
  pointmap: float[B, P, 3]
  confidence: float[B, P, 1]
  bounded_weights: float[B, E, P, 1]
  uncertainty: float[B, P, 1]
  diagnostics: dict
```

Constraints:

- weights are bounded and inspectable;
- fallback/stub proposals are masked out;
- no output may depend on unknown backend status;
- decoder must run from cached proposals before core edits.

### Native decoder

The native decoder is trained only after the proposal-set decoder passes.

Training targets:

```text
proposal-set decoder pointmap
patch oracle
SCF weights
expert dropout consistency
temporal consistency
scale stability
```

Expected behavior:

```text
native decoder can drop one or more external proposal teachers at inference
while keeping most of the proposal-set decoder quality.
```

## Losses and metrics

Primary:

- abs_rel;
- patch_oracle_gap_pp;
- relative improvement versus best single;
- correct-state versus no-state versus shuffled-state.

Required secondary:

- temporal_delta;
- scale_drift;
- fallback contamination count;
- runtime_ms;
- vram_mb;
- teacher dropout robustness.

Pass rule:

```text
proposal-set decoder > SCFHead
correct-state > no-state > shuffled-state where feasible
temporal_delta and scale_drift do not degrade
fallback contamination == 0
```

## Implementation boundary

Allowed first:

- non-core `ProposalSetDecoder` module;
- state projection head;
- cache schema adapters;
- training/eval scripts over cached proposals;
- visualization and report tables.

Gated:

- checkpoint download;
- install mutation on BUAA-Server;
- long server runs;
- frozen core edits;
- native decoder inside core modules;
- final performance claims.

## Stop rules

- If VGGT-Omega cannot pass real-backend smoke, keep the 3-expert bank.
- If proposal-set decoder does not beat SCF, keep SCF as the final prototype.
- If no-state catches correct-state, pause state claims and debug state leakage.
- If temporal / scale regress, do not claim memory improvement.
- If native dropout loses too much quality, keep native decoder as future work.
