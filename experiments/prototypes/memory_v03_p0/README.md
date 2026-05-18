# Memory v0.3 P0 local static tensor prototype

This directory contains the cycle 031 local prototype scaffold authorized by
`DEC-20260508-007`.

## Boundary

Implemented in this cycle:

- deterministic P0 synthetic fixture generation
- oracle-bus field tagging and validation
- raw fixture label exclusion audit
- `ABL-memory-0` as the fixture/logging validity gate
- local output serialization for manifest, logs, metrics, summary, and
  evidence boundary

Not implemented or claimed in this cycle:

- `ABL-memory-1..8` ablation behavior
- `ABL-memory-9..11`
- server integration
- `Dream/code/` edits
- model inference, training, checkpoint use, or paper evidence

## Run

From this directory:

```powershell
python run_ablations.py --output outputs
python -m pytest tests
```

If running from the repository root:

```powershell
python Dream\experiments\prototypes\memory_v03_p0\run_ablations.py --output Dream\experiments\prototypes\memory_v03_p0\outputs
python -m pytest Dream\experiments\prototypes\memory_v03_p0\tests
```

## Required Outputs

`ABL-memory-0` writes:

- `fixtures_manifest.json`
- `write_log.jsonl`
- `metrics_abl_memory_0_8.csv`
- `summary_go_no_go.md`
- `evidence_boundary_update.md`

Passing this gate only means the P0 fixture/logging substrate is locally
valid enough for later ablation implementation.
