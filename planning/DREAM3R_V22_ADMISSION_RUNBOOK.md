# Dream3R v2.2 admission runbook

date: 2026-05-30
status: active deployment research plan
decision: `decisions/DEC-20260530-014-v22-vggt-omega-admission.md`
spec: `specs/SPEC-20260530-004-dream3r-v22-expert-admission.md`

Post-runner status, 2026-06-04:

- DEC-20260604-035 adds a resumable staging runner:
  `code/dream3r/scripts/stage_vggt_omega_admission.py`.
- Local and BUAA-Server integration tests pass: 22/22.
- BUAA-Server staging initially wrote a blocked status because no HF token was
  present and the checkpoint was missing.
- After the user provided `E:\Download\vggt_omega_1b_512.pt`, the checkpoint was
  uploaded to `/hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt`.
- The one-window GPU1 smoke now records `backend == "real"` with zero fallback
  contamination at
  `runs/v22_admission/vggt_omega_smoke/results_after_upload_fix_20260604.json`.
- Continue to Stage G4 tiny cache build.

Release-readiness update, 2026-06-05:

- A dedicated oracle-admission evaluator now exists locally at
  `code/dream3r/scripts/eval_vggt_omega_oracle_admission.py`.
- Local VGGT tests pass 25/25.
- VGGT 50+50 oracle admission passed as a teacher gate:
  KITTI +1.18%, ETH3D +18.35%.
- VGGT-expanded SCF state controls failed the release gate:
  KITTI correct-state 0.2296 loses to no-state 0.1966 and locked baseline
  0.1448.
- Keep VGGT-Omega as a real optional teacher/proposal source, especially for
  ETH3D/indoor-like windows. Do not use it as the release model path yet.

## Goal

Start from the current real proposal bank:

```text
MASt3R / Fast3R / Spann3R
```

Then admit only candidates that improve Dream3R:

```text
VGGT-Omega -> CUT3R -> MonST3R
```

The first target is VGGT-Omega, not vanilla VGGT. Vanilla VGGT remains a
baseline. OVGGT remains a separate memory/cache comparator.

## Stage G0 — local documentation gate

Status: done by this runbook.

Artifacts:

- DEC-014;
- SPEC-004;
- this runbook;
- v08 handoff prompt.

## Stage G1 — repository and dependency inventory

Allowed:

```text
read upstream README / install docs
inspect dependency files
write a local inventory note
```

Not allowed:

```text
download checkpoints
run long server jobs
modify frozen core files
```

Expected output:

```text
vggt_omega_inventory:
  repo
  commit
  license
  checkpoint_policy
  python_version
  cuda_version
  dependency_delta
  native_outputs
  minimal_inference_entry
```

## Stage G2 — execution DEC

Before any checkpoint or server run, write a small DEC that names:

- exact repository path on server;
- exact checkpoint source and storage path;
- exact conda/env strategy;
- exact smoke input;
- exact command with `CUDA_VISIBLE_DEVICES=1`;
- expected output files;
- fallback exclusion check.

## Stage G3 — one-window smoke

Target shape:

```text
ssh BUAA-Server
cd /hdd3/kykt26/code/dream3r
CUDA_VISIBLE_DEVICES=1 <vggt_omega_smoke_command>
```

The smoke passes only if:

- the upstream model loads a real checkpoint;
- one small image window produces geometry output;
- adapter metadata records `backend == "real"`;
- runtime and VRAM are captured;
- no fallback/stub entry is accepted.

## Stage G4 — tiny cache build

Build a tiny cache with existing SCF entries plus VGGT-Omega:

```text
datasets:
  KITTI: 5-10 windows
  ETH3D: 5-10 windows if cheap
experts:
  mast3r
  fast3r
  spann3r
  vggt_omega
```

Do not overwrite the existing ver2.1 cache. Use a new run folder.

## Stage G5 — oracle admission

Compute:

- standalone abs_rel;
- best-single rank;
- patch-oracle ceiling;
- oracle gain versus the 3-expert bank;
- failure windows;
- cost table.

Decision:

```text
if oracle ceiling does not improve:
  keep VGGT-Omega as comparator / baseline only
else:
  proceed to SCF / ProposalSetDecoder admission
```

## Stage G6 — decoder admission

Two ablations are enough for the first pass:

```text
SCF 3 experts
SCF 4 experts with VGGT-Omega
```

If a proposal-set decoder exists, add:

```text
ProposalSetDecoder 3 experts
ProposalSetDecoder 4 experts with VGGT-Omega
```

Pass condition:

```text
4-expert Dream3R improves output or closes patch-oracle gap
and correct-state remains better than no-state / shuffled-state.
```

## Stage G7 — next candidate

Only after VGGT-Omega has a clear verdict:

```text
1. CUT3R
2. MonST3R
```

Do not parallel-integrate all three unless separate agents own isolated
inventory notes and no server env mutation is required.

## Working constraints

- Windows local: docs, code edits, scp only.
- Model execution: `ssh BUAA-Server`.
- GPU: `CUDA_VISIBLE_DEVICES=1`.
- Frozen core files stay untouched unless a DEC names them.
- Existing SCF/ver2.1 evidence remains the baseline. Do not reopen broad
  architecture search.
