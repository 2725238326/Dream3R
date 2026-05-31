# Dream3R v2.2 admission runbook

date: 2026-05-30
status: active deployment research plan
decision: `decisions/DEC-20260530-014-v22-vggt-omega-admission.md`
spec: `specs/SPEC-20260530-004-dream3r-v22-expert-admission.md`

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
