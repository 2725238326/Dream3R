# DEC-20260605-036: Dream3R release-readiness gate

Date: 2026-06-05
Status: accepted as release path; superseded by DEC-037 result selection
Scope: Dream3R publishable model candidate

## Context

The user asked to push Dream3R toward a publishable model because the research
loop has taken too long. Recent evidence is mixed:

- Current best bounded baseline remains frozen-StatePrior + bounded residual:
  KITTI/ETH3D `0.1448/0.1475`.
- Qwen semantic-controller gates are diagnostic-negative and must not drive
  Router/Critic promotion.
- VGGT-Omega checkpoint is now uploaded and one-window GPU1 smoke is admitted:
  `backend=real`, fallback contamination 0.
- VGGT-Omega has not yet proved it improves the proposal bank; smoke is only a
  load/output gate.

## Decision

Define a narrow release-readiness path instead of continuing broad research:

1. Treat the current bounded StatePrior/residual result as the fallback release
   candidate.
2. Evaluate whether VGGT-Omega should enter the proposal bank by oracle
   admission on existing SCF cache windows.
3. If VGGT-Omega improves oracle ceiling, build a small VGGT-expanded cache and
   run state-causal SCF/decoder controls.
4. If VGGT-Omega does not improve oracle ceiling, stop the VGGT branch and
   prepare the bounded baseline for release.

## New executable surface

Added locally:

```text
code/dream3r/scripts/eval_vggt_omega_oracle_admission.py
code/dream3r/tests/test_vggt_integration.py
```

The evaluator consumes existing SCF caches, runs VGGT-Omega on matching image
windows, and reports:

- old MASt3R/Fast3R/Spann3R oracle;
- VGGT-Omega standalone metric;
- new oracle after adding VGGT-Omega;
- VGGT win count;
- fallback contamination.

Local verification:

```text
python -B -m pytest --assert=plain code/dream3r/tests/test_vggt_integration.py -q
# 25 passed
```

Server execution later completed under DEC-037. The first `scp` interruption
was transient infrastructure noise, not a model result.

## Release Gates

### Gate R0: Artifact Hygiene

Pass iff:

- frozen core diff is empty;
- tests pass locally and on BUAA-Server;
- no fallback/stub proposal enters a claimed result;
- all result JSONs are mirrored locally.

### Gate R1: VGGT-Omega Oracle Admission

Run `eval_vggt_omega_oracle_admission.py` on 5 KITTI + 5 ETH3D windows first.

Pass iff:

```text
fallback_contamination_count == 0
failure_flags == []
new_oracle_mean < old_oracle_mean on at least one domain
no domain shows catastrophic standalone VGGT failure
```

If R1 fails, do not spend more time on VGGT-Omega for release.

### Gate R2: Tiny Cache / Control Admission

Only if R1 passes:

- build a 20-50 window VGGT-expanded proposal cache;
- train/evaluate the existing SCF or proposal-set decoder head;
- run correct-state / no-state / shuffled-state controls.

Pass iff:

```text
correct-state beats no-state and shuffled-state
correct-state matches or beats 0.1448/0.1475
fallback contamination is zero
```

### Gate R3: Release Candidate Packaging

Package whichever candidate passes:

- primary path: VGGT-expanded state-causal model if R1/R2 pass;
- fallback path: frozen-StatePrior + bounded residual baseline if VGGT fails.

Required deliverables:

```text
release card
exact command runbook
checkpoint/result artifact table
known limitations
non-claim list
```

## Next Step

Retry server sync for:

```text
code/dream3r/scripts/eval_vggt_omega_oracle_admission.py
code/dream3r/tests/test_vggt_integration.py
```

Then run:

```text
cd /hdd3/kykt26/code/dream3r
CUDA_VISIBLE_DEVICES=1 PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=/hdd3/kykt26/code/dream3r \
conda run --no-capture-output -n dream3r python -B \
  -m dream3r.scripts.eval_vggt_omega_oracle_admission \
  --max-windows-per-domain 5 \
  --output runs/v22_admission/vggt_omega_oracle/tiny_oracle_admission_5x2_20260605.json
```

DEC-037 executed this gate and selected the fallback release candidate because
VGGT-expanded state controls did not pass.
