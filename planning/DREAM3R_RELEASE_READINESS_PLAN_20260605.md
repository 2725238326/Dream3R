# Dream3R Release Readiness Plan

Date: 2026-06-05
Status: release candidate selected after VGGT control gate
Decision: `decisions/DEC-20260605-036-dream3r-release-readiness-gate.md`

## Release Definition

A publishable Dream3R candidate must be a reproducible model path, not only an
admitted teacher or a promising smoke. It needs:

```text
real inputs -> real proposal/cache path -> state-conditioned output
```

and must report:

```text
KITTI / ETH3D metrics
correct-state / no-state / shuffled-state controls
fallback contamination
exact commands and artifact paths
known limitations
```

## Current Candidate Ranking

| Rank | Candidate | Status | Why |
| --- | --- | --- | --- |
| 1 | Frozen StatePrior + bounded residual | selected release candidate | current best bounded result, KITTI/ETH3D `0.1448/0.1475`, state-causal |
| 2 | VGGT-Omega-expanded proposal bank | teacher lane, not RC | oracle-positive, but state-control gate failed for release |
| 3 | Native student decoder | not release-ready | executable and state-causal, but metric-flat |
| 4 | Qwen semantic controller | diagnostic only | direct and Critic-prior promotion gates negative |
| 5 | Image-state U1 | rejected for release | correct-state loses to no-state and baseline |

## Executed Gates

VGGT-Omega oracle admission:

```text
artifact: runs/v22_admission/vggt_omega_oracle/oracle_admission_50x2_cache_20260605.json
KITTI: old oracle 0.1763 -> new oracle 0.1742, gain 1.18%, VGGT wins 2/50
ETH3D: old oracle 0.1419 -> new oracle 0.1158, gain 18.35%, VGGT wins 35/50
```

VGGT-expanded SCF controls:

```text
KITTI correct-state 0.2296, no-state 0.1966, shuffle-state 0.2180
ETH3D correct-state 0.0570, no-state 0.0583, shuffle-state 0.0598
```

Verdict:

```text
VGGT-Omega is a real optional teacher, not the release model path.
Release candidate = frozen StatePrior + bounded residual.
```

## Historical Execution Command

Retry server sync for the VGGT-Omega oracle evaluator:

```text
scp code/dream3r/scripts/eval_vggt_omega_oracle_admission.py \
  BUAA-Server:/hdd3/kykt26/code/dream3r/dream3r/scripts/eval_vggt_omega_oracle_admission.py

scp code/dream3r/tests/test_vggt_integration.py \
  BUAA-Server:/hdd3/kykt26/code/dream3r/dream3r/tests/test_vggt_integration.py
```

Then verify:

```text
cd /hdd3/kykt26/code/dream3r
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/hdd3/kykt26/code/dream3r \
conda run --no-capture-output -n dream3r python -B -m pytest --assert=plain \
  dream3r/tests/test_vggt_integration.py -q
```

Then run:

```text
CUDA_VISIBLE_DEVICES=1 PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=/hdd3/kykt26/code/dream3r \
conda run --no-capture-output -n dream3r python -B \
  -m dream3r.scripts.eval_vggt_omega_oracle_admission \
  --max-windows-per-domain 5 \
  --output runs/v22_admission/vggt_omega_oracle/tiny_oracle_admission_5x2_20260605.json
```

## Promotion Logic

### If VGGT-Omega Oracle Admission Passes

Proceed to:

```text
VGGT-expanded tiny cache -> state/no-state/shuffle controls -> compare to 0.1448/0.1475
```

Minimum next output:

```text
runs/v22_admission/vggt_omega_oracle/tiny_oracle_admission_5x2_20260605.json
runs/v22_admission/vggt_omega_cache_gate/
```

### If VGGT-Omega Control Admission Fails

Stop VGGT-Omega as a release candidate. Do not spend release time on more VGGT
integration. Package:

```text
frozen StatePrior + bounded residual
```

as the release candidate, with VGGT-Omega documented as a real but
non-improving teacher.

## Release Package Checklist

Release package files now added:

```text
release/DREAM3R_RC_CARD.md
release/RUNBOOK.md
release/ARTIFACTS.json
release/REPRODUCE.md
release/VERIFY_REPORT.md
release/LIMITATIONS.md
release/NON_CLAIMS.md
```

Required evidence:

```text
local tests
server tests
frozen-core diff empty
KITTI / ETH3D metrics
state-causality controls
fallback contamination count
```

## Do Not Do Next

- Do not keep tuning Qwen on the same 50 windows.
- Do not train a larger native decoder before oracle admission.
- Do not edit frozen core files to make the release look cleaner.
- Do not call VGGT-Omega publishable from one-window smoke alone.
