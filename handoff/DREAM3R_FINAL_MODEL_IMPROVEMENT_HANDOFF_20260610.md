# Dream3R Final Model Improvement Handoff

Date: 2026-06-10

## Purpose

This handoff starts the final-model improvement lane.

The goal is to make the current final Dream3R model stronger and better
evidenced without reopening broad architecture exploration.

The next agent should execute, not only plan:

1. lock the current v1.1.0 baseline with fresh evidence;
2. build a final evaluation package that is stronger than the current runtime
   demo evidence;
3. attempt one small, reversible improvement around the existing
   candidate-geometry fusion line;
4. promote only if the existing metric and state-causality gates remain green;
5. otherwise record the attempt as neutral/negative and keep v1.1.0 official.

## Current Official Model

```text
official model: Dream3R v1.1.0
type: state-conditioned proposal-fusion 3R
api: dream3r.release_v11.build_dream3r_v11_release
stable fallback: v1.0-rc1
metric: AbsRel, lower is better
KITTI / ETH3D: 0.1448 / 0.0570
```

The current policy is domain-conditional:

```text
KITTI -> v1.0-rc1 bounded StatePrior + residual
ETH3D -> VGGT-Omega-expanded SCF correct-state
```

The current state controls are locked:

```text
KITTI normal/no-state/shuffle: 0.1448 / 0.1553 / 0.1521
ETH3D normal/no-state/shuffle: 0.0570 / 0.0583 / 0.0598
```

## Read First

Read these in order:

```text
TASK_SNAPSHOT.md
handoff/DREAM3R_FINAL_MODEL_IMPROVEMENT_HANDOFF_20260610.md
handoff/CONTEXT_COMPACTION_20260608_V11_USABLE_MODEL.md
planning/DREAM3R_FINAL_STAGE_READINESS_PLAN_20260609.md
release/EFFECTIVE_ARCHITECTURE_V1_1.md
release/MODEL_CARD_V1_1.md
release/VERIFY_REPORT.md
release/ARTIFACTS.json
reports/midterm/DREAM3R_NEXT_OPTIMIZATION_PLAN.md
```

Use `AGENT_MASTER_PROMPT.md`, `README.md`, `INDEX.md`, and
`WORKFLOW_STATUS.md` only after these if more context is needed.

## What Is Missing

The current deliverable is complete enough for final reporting, but the final
model can still be strengthened in three practical ways:

1. **Final evaluation pack is thin.** The real-cache demo verifies cache
   consumption and branch ordering, but it is not a formal benchmark rerun.
2. **Fusion confidence is not calibrated.** Proposal confidence is consumed by
   the fusion path, but the repo does not yet have a final reliability summary
   or per-teacher calibration gate.
3. **Conflict handling is still coarse.** The interface already carries
   `conflict_score`; the final model can try a small conflict-aware residual or
   weight dampening rule without changing the overall architecture.

Do not solve these by inventing a new large architecture.

## Allowed Work

The next agent is allowed to edit code, tests, scripts, and docs in these
scopes:

```text
code/dream3r/release_v11.py
code/dream3r/scf_head.py
code/dream3r/release_candidate.py
code/dream3r/scripts/*v11*
code/dream3r/scripts/*release*
code/dream3r/scripts/*fusion*
code/dream3r/tests/test_release_v11_*.py
code/dream3r/tests/test_v11_demo_script.py
release/*.md
release/ARTIFACTS.json
reports/final/*.md
planning/*.md
handoff/*.md
runs/release/
```

Adding a new focused script or test is allowed when it proves or rejects the
small improvement. Prefer small new scripts over changing stable core runtime.

Avoid editing stable substrate files unless a directly verified bug requires it:

```text
code/dream3r/bus.py
code/dream3r/orchestrator.py
code/dream3r/contracts.py
code/dream3r/repair.py
code/dream3r/anchor_bank.py
code/dream3r/nsa_attention.py
```

## Forbidden Work

Do not do the following in this lane:

- do not promote Qwen to geometry, Router, Critic, or official model status;
- do not promote Foundation3R, proposal-free decoding, or v1.2-exp0;
- do not download or stage new checkpoints;
- do not start broad architecture search;
- do not rewrite the final model as VGGT-only;
- do not claim SOTA, image-only inference, proposal-free foundation 3R, or
  long-sequence deployment;
- do not bump the official version unless every gate below passes.

## Execution Plan

### Step 0: Baseline Guard

Run the current release checks before changing behavior:

```powershell
python -B code\dream3r\scripts\verify_v11_release.py --root .
python -B code\dream3r\scripts\verify_release_candidate.py --root .
python -B -m pytest --assert=plain code\dream3r\tests\test_release_candidate_architecture.py code\dream3r\tests\test_release_candidate_verifier.py code\dream3r\tests\test_release_v11_architecture.py code\dream3r\tests\test_release_v11_verifier.py code\dream3r\tests\test_release_v11_smoke_model.py code\dream3r\tests\test_v11_demo_script.py -q
```

If these fail, fix the baseline before trying any improvement.

### Step 1: Build The Final Evaluation Pack

Create a compact final evaluation artifact before model changes.

Preferred output:

```text
runs/release/v11_final_eval/final_eval_summary.json
release/FINAL_EVAL_TABLE_V1_1.md
```

Minimum contents:

- v1.1 official KITTI/ETH3D metrics;
- v1.1 normal/no-state/shuffle controls;
- v1.0-rc1 fallback metrics;
- real-cache demo status;
- source JSON paths used;
- clear note that runtime cache demo is not a benchmark rerun;
- clear note that Qwen/Foundation3R are not official.

If no new benchmark rerun is available, say so explicitly and preserve the
existing metric claim.

### Step 2: Attempt One Small Fusion Improvement

Pick one, not both, unless the first is clearly completed and verified.

Option A: confidence calibration

```text
Goal: make proposal confidence more comparable across teachers.
Candidate mechanisms:
  - per-teacher temperature or scalar calibration;
  - reliability summary: confidence-to-error bins;
  - conservative weight dampening when confidence is unreliable.
```

Option B: conflict-aware residual / dampening

```text
Goal: use existing conflict_score to avoid over-trusting unstable fusion.
Candidate mechanisms:
  - shrink residual amplitude at high conflict;
  - damp low-reliability expert weights at high conflict;
  - keep the output contract unchanged.
```

Keep the change reversible and local. Do not add a new named architecture unless
it retires an existing negative lane and passes the gates.

### Step 3: Gate The Candidate

A candidate may be called `v1.1.1-candidate` only if all are true:

```text
KITTI AbsRel <= 0.1448
ETH3D AbsRel <= 0.0570
KITTI correct-state < KITTI no-state
KITTI correct-state < KITTI shuffle-state
ETH3D correct-state < ETH3D no-state
ETH3D correct-state < ETH3D shuffle-state
v1.0 fallback verifier still passes
v1.1 release verifier still passes
targeted release tests pass
```

Prefer promotion only if at least one domain improves by a visible margin:

```text
absolute AbsRel improvement >= 0.001
or relative improvement >= 0.5%
```

If the candidate is flat or mixed, keep `v1.1.0` official and document the
attempt as neutral or negative.

### Step 4: Sync Docs

If the candidate passes:

- add a decision or release note for the candidate;
- update `release/ARTIFACTS.json`;
- update `release/VERIFY_REPORT.md`;
- update `release/MODEL_CARD_V1_1.md` or add a clearly named v1.1.1 candidate
  note;
- update final report/PPT only if the claim is stable.

If the candidate does not pass:

- add a short negative/neutral note under `release/VERIFY_REPORT.md` or a new
  planning note;
- keep official model text at `v1.1.0`;
- explain why the failed lane should not be re-run unchanged.

## Expected Deliverables

At minimum, the next agent should leave:

```text
runs/release/v11_final_eval/final_eval_summary.json
release/FINAL_EVAL_TABLE_V1_1.md
release/VERIFY_REPORT.md updated with the final-model improvement attempt
TASK_SNAPSHOT.md updated with pass/fail evidence
WORKFLOW_STATUS.md updated with the final outcome
```

If a candidate passes, also leave:

```text
release/V1_1_1_CANDIDATE.md
focused tests for the changed behavior
updated release/ARTIFACTS.json
```

## Verification Before Stopping

Run these after all edits:

```powershell
python -B code\dream3r\scripts\verify_v11_release.py --root .
python -B code\dream3r\scripts\verify_release_candidate.py --root .
python -B -m pytest --assert=plain code\dream3r\tests\test_release_candidate_architecture.py code\dream3r\tests\test_release_candidate_verifier.py code\dream3r\tests\test_release_v11_architecture.py code\dream3r\tests\test_release_v11_verifier.py code\dream3r\tests\test_release_v11_smoke_model.py code\dream3r\tests\test_v11_demo_script.py -q
Get-Content release\ARTIFACTS.json -Raw | ConvertFrom-Json | Out-Null
git diff --check
```

If model behavior changes, add and run a focused test for that behavior.

## Stop Conditions

Stop only when one of these is true:

1. a candidate passes all gates and docs/tests are synced;
2. the attempted improvement is documented as neutral/negative and v1.1.0 is
   reaffirmed;
3. a hard blocker prevents evaluation, and the blocker plus next exact command
   are recorded in `TASK_SNAPSHOT.md`.

Do not leave the repo in a state where the official model claim is ambiguous.
