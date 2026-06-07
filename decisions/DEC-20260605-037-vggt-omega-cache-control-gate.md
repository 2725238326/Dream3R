# DEC-20260605-037: VGGT-Omega cache/control gate

Date: 2026-06-05
Status: accepted; oracle-positive but release-control negative
Scope: Dream3R release-readiness R1/R2

## Context

DEC-20260605-036 required VGGT-Omega to pass oracle admission and then
state-causality controls before it could displace the bounded baseline as the
release candidate.

VGGT-Omega one-window smoke was already real-backend admitted:

```text
backend: real
fallback_contamination_count: 0
```

## Decision

Run VGGT-Omega oracle admission on existing SCF cache windows, then build a
50+50 VGGT-expanded cache and evaluate SCF correct-state / no-state /
shuffle-state controls.

## Implementation

Updated:

```text
code/dream3r/scripts/eval_vggt_omega_oracle_admission.py
code/dream3r/tests/test_vggt_integration.py
```

The evaluator now can also write VGGT-expanded SCF caches:

```text
runs/v22_admission/vggt_omega_cache_gate/scf_kitti_vggt_omega_cache.pt
runs/v22_admission/vggt_omega_cache_gate/scf_eth3d_vggt_omega_cache.pt
```

## Verification

Local:

```text
python -B -m pytest --assert=plain code/dream3r/tests/test_vggt_integration.py -q
# 27 passed
```

Server:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/hdd3/kykt26/code/dream3r \
conda run --no-capture-output -n dream3r python -B -m pytest --assert=plain \
  dream3r/tests/test_vggt_integration.py -q
# 27 passed
```

## R1 Oracle Admission

50 KITTI + 50 ETH3D:

```text
artifact: runs/v22_admission/vggt_omega_oracle/oracle_admission_50x2_cache_20260605.json
fallback_contamination_count: 0
failure_flags: []
```

KITTI:

```text
old_oracle_mean: 0.17628515735268593
new_oracle_mean: 0.1742069125175476
oracle_gain_pct: 1.1789108432881128
vggt_omega_wins: 2 / 50
vggt_omega_mean: 0.3072756989300251
```

ETH3D:

```text
old_oracle_mean: 0.1418548844754696
new_oracle_mean: 0.1158284376654774
oracle_gain_pct: 18.3472334465105
vggt_omega_wins: 35 / 50
vggt_omega_mean: 0.13829341546632348
```

R1 verdict: positive, but domain-conditional. VGGT-Omega is highly useful on
ETH3D-like windows and only marginally useful on KITTI.

## R2 State-Causality Controls

VGGT-expanded SCF on the 50+50 cache, seed 7, 200 epochs:

```text
correct-state artifact:
runs/v22_admission/vggt_omega_cache_gate/scf_state_seed7/results.json

no-state artifact:
runs/v22_admission/vggt_omega_cache_gate/scf_no_state_seed7/results.json

shuffle-state artifact:
runs/v22_admission/vggt_omega_cache_gate/scf_shuffle_state_seed7/results.json
```

Final eval:

| Domain | correct-state | no-state | shuffle-state | best single | baseline target |
| --- | ---: | ---: | ---: | ---: | ---: |
| KITTI | 0.2296 | 0.1966 | 0.2180 | 0.2049 | 0.1448 |
| ETH3D | 0.0570 | 0.0583 | 0.0598 | 0.0913 | 0.1475 |

R2 verdict: failed for release. Correct-state does not beat no-state on KITTI
and does not match the locked KITTI baseline. ETH3D improves strongly, but the
state-causality requirement is not robust enough for a publishable Dream3R
candidate.

## Verdict

VGGT-Omega is admitted as a real optional teacher/proposal source, especially
for ETH3D/indoor-like windows. It is not admitted as the release model path.

Release candidate remains:

```text
frozen StatePrior + bounded residual
KITTI/ETH3D: 0.1448 / 0.1475
```

Next work should package the bounded baseline and record VGGT-Omega as a
release-note limitation / future teacher lane, not continue broad VGGT tuning.
