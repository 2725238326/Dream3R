# DEC-20260508-007: Cycle 031 P0 local static tensor scaffold

Status: accepted

Date: 2026-05-08

Cycle: 031

Decision type: bounded local prototype execution

Authorized trigger: user approved proceeding after the cycle 030 template
and GitHub CLI discussion with "那就先进行后续操作吧".

## Decision

Proceed with a local Memory v0.3 P0 static tensor scaffold and implement
`ABL-memory-0` as the fixture/logging validity gate.

This decision authorizes only a deterministic local prototype under
`Dream/experiments/prototypes/memory_v03_p0/`. The goal is to prove that
the synthetic fixtures, oracle-bus boundary, raw-label exclusion audit,
output serialization, and reproducibility checks are mechanically sound
before any Memory v0.3 ablation logic is treated as admissible.

## Scope

Allowed in cycle 031:

- create local prototype files under
  `Dream/experiments/prototypes/memory_v03_p0/`
- generate deterministic tensor fixtures from fixed seeds
- define the oracle-bus field contract and raw-label exclusion audit
- implement `ABL-memory-0` checks only
- emit local output artifacts:
  - `fixtures_manifest.json`
  - `write_log.jsonl`
  - `metrics_abl_memory_0_8.csv`
  - `summary_go_no_go.md`
  - `evidence_boundary_update.md`
- add a focused local test for the `ABL-memory-0` validity gate
- update cycle log, decision registry, guidance files, and task snapshot

Not authorized in cycle 031:

- implementing or claiming performance for `ABL-memory-1..8`
- any work on `ABL-memory-9..11`
- server integration
- edits under `Dream/code/`
- edits under `/hdd3/kykt26/code/dream3r/dream3r/`
- importing CUT3R, Spann3R, Dream3R, or server model runtime code
- checkpoint download or checkpoint use
- training or fine-tuning
- real model inference
- frontend or navigation work
- paper claim promotion

## Required Boundary

`ABL-memory-0` is a validity gate, not an ablation result. Later ablations
are inadmissible unless this gate passes.

The following raw fixture labels may be used only for fixture construction,
manifesting, and audit checks. They must not be passed as hidden variant
inputs:

- `group_id`
- `is_dynamic`
- `is_corrupt`
- `expected_loop_id`
- future-use labels not represented through the oracle bus

The permitted oracle-bus fields for this cycle are:

- `dynamic_ratio`
- `conflict_score`
- `permanence_score`
- `expected_future_use`
- `reset_mask`

Each bus field must be tagged as `oracle_bus` in the manifest and output
audit.

## Output Interpretation

If the gate passes, the strongest allowed claim is:

```text
Cycle 031 locally demonstrates that the Memory v0.3 P0 fixture and logging
substrate can be deterministically generated, audited for raw-label
leakage, serialized, and checked for the ABL-memory-0 validity gate.
```

The following remain unvalidated:

- spatial memory retrieval quality
- state-token recurrence quality
- hybrid memory behavior
- bus-gated write policy benefit
- reconstruction quality
- training stability
- server integration
- paper-level empirical claims

## Stop Gates

- G0 authorization: passed by this DEC.
- G1 path setup: only local prototype path may be created.
- G2 fixture implementation: all default P0 tensor dimensions must match
  the cycle 028 prototype plan.
- G3 oracle boundary: bus fields must carry `oracle_bus` tags and raw
  fixture labels must be excluded from the variant-input contract.
- G4 outputs: all required output files must be generated locally.
- G5 verification: focused local tests or equivalent CLI verification must
  pass before the cycle is closed.

## Next Direction If Passed

The next admissible implementation step is a separate decision or cycle for
`ABL-memory-1`, starting from a vector-memory baseline and explicit retrieval
metrics. No later ablation should be claimed until it has its own local
implementation and evidence boundary.
