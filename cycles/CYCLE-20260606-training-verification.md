# Cycle 20260606: Training Verification Sweep

Date: 2026-06-06
Status: closed

## Goal

Run the training and architecture tests that had not yet been exercised after
formalizing Dream3R v1.0-rc1.

## Local Tests

Full local test suite:

```text
python -B -m pytest --assert=plain code/dream3r/tests -q
273 passed, 2 skipped, 83 warnings
```

Targeted local training/architecture tests:

```text
training/convergence/sequence/critic-data: 7 passed
state-prior/proposal/native/image-state: 16 passed
memory/router/critic-only: 9 passed
release/proposal/native combined: 16 passed
```

One collection blocker was fixed:

```text
code/dream3r/scripts/build_critic_training_data.py
```

The script now imports `DEFAULT_EXPERT_ORDER` from
`build_oracle_expert_labels.py` and preserves the legacy local `EXPERT_ORDER`
alias for downstream summary output.

## Server Tests

BUAA-Server GPU1 training/architecture pytest subset:

```text
CUDA_VISIBLE_DEVICES=1
37 passed, 21 warnings
```

Covered:

```text
critic training data
training convergence
sequence training
memory/router/critic-only training
StatePriorHead
ProposalSetDecoder
NativeStudentDecoder
ImageStateStudentDecoder
release candidate architecture/verifier
```

## Server Training Smokes

All ran on BUAA-Server GPU1 with `epochs=1`.

| Smoke | Result | Artifact |
| --- | --- | --- |
| StatePrior state/no-state/shuffle | passed | `runs/stage6_fusion/state_prior_train_smoke_20260606/` |
| ProposalSetDecoder frozen-prior state | passed | `runs/stage6_fusion/proposal_set_decoder_train_smoke_20260606/frozen_prior_state_seed_7/` |
| NativeStudent state/no-state/shuffle | passed, fallback 0 | `runs/stage6_fusion/native_student_train_smoke_20260606/` |
| ImageStateStudent state/no-state/shuffle | passed, fallback 0 | `runs/stage6_fusion/image_state_student_train_smoke_20260606/` |

These are entrypoint/cache/checkpoint smokes, not new promotion runs.

## Remaining Boundary

No frozen core files were edited. The official RC remains:

```text
Dream3R v1.0-rc1
frozen StatePrior + bounded residual
KITTI / ETH3D: 0.1448 / 0.1475
```
