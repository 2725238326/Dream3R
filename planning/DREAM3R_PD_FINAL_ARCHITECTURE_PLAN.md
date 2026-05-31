# Dream3R-PD final architecture plan

date: 2026-05-30
status: active final-selection plan
decision: `decisions/DEC-20260530-015-final-architecture-selection.md`
spec: `specs/SPEC-20260530-005-dream3r-pd-final-architecture.md`

## Requirements summary

Dream3R needs a final route that can be defended after midterm:

- keep the real SCF evidence;
- stop presenting expert selection as the model;
- use VGGT-Omega as the first new teacher candidate;
- produce a route toward a native Dream3R model;
- avoid frozen-core edits until non-core gates pass.

## RALPLAN-DR summary

Principles:

1. Evidence-first: no fallback/stub result can support an architecture claim.
2. Dream3R owns reconstruction: external models are teachers/proposals.
3. State must matter: correct-state must beat no-state/shuffled-state.
4. Native only after teacher evidence: distill after proposal-set decoding wins.
5. Smallest executable path: start with cached proposal training.

Decision drivers:

1. Two-day/midterm pressure requires a defensible final story now.
2. Current evidence supports state-conditioned fusion but not native decoding.
3. VGGT-Omega may improve the teacher bank but must not replace Dream3R.

Viable options:

| option | verdict | rationale |
| --- | --- | --- |
| A. Keep SCF as final | fallback final prototype | honest and supported, but weak as final model |
| B. Proposal-set decoder + distillation | selected | turns SCF evidence into a native-model path |
| C. VGGT-Omega-only | rejected | too dependent on external model; not Dream3R-owned |
| D. Broad expert search | rejected | high churn; low causal clarity |

## ADR

Decision:

```text
Select Dream3R-PD: proposal teachers + Dream state + proposal-set decoder
+ native distillation with proposal dropout.
```

Drivers:

- SCF has positive evidence on real proposals.
- Correct state is useful but temporal/scale remain unsolved.
- The user wants a final architecture, not another route search.
- VGGT-Omega is the strongest immediate teacher candidate.

Alternatives considered:

- SCF-only final prototype;
- VGGT-Omega-only wrapper;
- hard router;
- memory-only model;
- direct native decoder training.

Why chosen:

Dream3R-PD is the only route that preserves current evidence while making a
credible final product: a Dream3R-owned decoder that can eventually run with
fewer external teachers.

Consequences:

- We stop broad expert search.
- We evaluate VGGT-Omega only through admission gates.
- We implement decoder work outside frozen core first.
- Native Dream3R claims wait for distillation evidence.

Follow-ups:

- VGGT-Omega G1 inventory and G2 execution DEC.
- ProposalSetDecoder prototype from existing 3-expert caches.
- Trained-state projection / Critic calibration.
- Native dropout distillation once decoder gate passes.

## Execution ladder

### P0 — final architecture package

Status: done by this plan.

Artifacts:

- DEC-015;
- SPEC-005;
- this plan;
- v09 handoff prompt;
- cycle log and guidance sync.

### P1 — VGGT-Omega admission inventory

Status: done for documentation.

Use `planning/DREAM3R_V22_ADMISSION_RUNBOOK.md` Stage G1.

Deliverable:

```text
planning/VGGT_OMEGA_DEPLOYMENT_INVENTORY.md
decisions/DEC-20260530-016-vggt-omega-execution-draft.md
```

Contents:

- repo commit;
- license;
- checkpoint path/policy;
- dependency delta;
- native outputs;
- minimal smoke command;
- adapter normalization plan;
- exact G2 execution DEC draft.

Acceptance:

- no checkpoint download;
- no server mutation;
- one clear go/no-go execution DEC draft.

### P2 — ProposalSetDecoder v0 over existing caches

Status: local non-core prototype added; server training gated.

Scope:

```text
inputs: existing MASt3R / Fast3R / Spann3R caches
model: small non-core proposal-set decoder
baseline: SCFHead
```

Candidate files:

```text
code/dream3r/proposal_set_decoder.py
code/dream3r/scripts/train_proposal_set_decoder.py
code/dream3r/scripts/eval_proposal_set_decoder.py
```

Implemented files:

```text
code/dream3r/proposal_set_decoder.py
code/dream3r/scripts/train_proposal_set_decoder.py
code/dream3r/tests/test_proposal_set_decoder.py
```

Acceptance:

- fallback contamination count is zero;
- decoder beats SCFHead on at least one domain;
- patch_oracle_gap_pp improves or does not regress;
- correct-state remains above no-state and shuffled-state.

### P3 — trained-state projection

Scope:

```text
train state projection / critic calibration outside frozen core
```

Candidate files:

```text
code/dream3r/state_projection_head.py
code/dream3r/scripts/train_state_projection.py
```

Acceptance:

- trained-state > current-state > no-state / shuffled-state where feasible;
- temporal_delta and scale_drift do not degrade;
- state diagnostic tables are emitted.

### P4 — VGGT-Omega 4-teacher admission

Run only if P1/G2 authorizes a real smoke.

Compare:

```text
SCF 3 experts
SCF 4 experts with VGGT-Omega
ProposalSetDecoder 3 experts
ProposalSetDecoder 4 experts with VGGT-Omega
```

Acceptance:

- VGGT-Omega backend is real;
- oracle ceiling improves or candidate stays comparator-only;
- decoder output improves before any architecture claim.

### P5 — native decoder distillation

Run only if P2/P4 pass.

Scope:

```text
train native decoder with proposal dropout
```

Acceptance:

- native decoder keeps most proposal-set decoder quality;
- at least one teacher can be dropped at inference;
- temporal/scale metrics do not regress;
- final report states exactly which teachers remain required.

## Verification

Minimum verification for each code stage:

```text
python -m py_compile <changed scripts>
targeted pytest if module tests exist
one cached-proposal smoke
git diff --check
frozen-core diff audit
```

Current local verification:

```text
python -m py_compile code/dream3r/proposal_set_decoder.py \
  code/dream3r/scripts/train_proposal_set_decoder.py \
  code/dream3r/tests/test_proposal_set_decoder.py

python -m pytest code/dream3r/tests/test_proposal_set_decoder.py -q
# 2 passed
```

Server verification:

```text
ssh BUAA-Server
cd /hdd3/kykt26/code/dream3r
CUDA_VISIBLE_DEVICES=1 <single-stage command>
```

No long sweep starts until a DEC names the command and expected output path.

## Risks and mitigations

| risk | mitigation |
| --- | --- |
| VGGT-Omega install is heavy | inventory first; keep 3-expert path alive |
| decoder overfits tiny caches | compare held-out windows and no-state controls |
| state signal is leakage | shuffled-state must stay worse than correct-state |
| native decoder loses quality | keep proposal-set decoder as final prototype |
| core edits become tempting | enforce non-core scripts until gates pass |

## Stop condition

Stop the architecture selection phase here. Future work should execute the
selected path, not reopen route exploration unless a gate fails with evidence.
