# DEC-20260530-017 — Start Dream3R-PD with a non-core ProposalSetDecoder

decision_id: DEC-20260530-017
date: 2026-05-30
scope: Dream3R-PD first implementation step
status: accepted as local non-core prototype; server training gated

## Context

DEC-20260530-015 selected Dream3R-PD as the final architecture path. The first
implementation step that does not require checkpoint download, server mutation,
or frozen-core edits is a ProposalSetDecoder over existing SCF caches.

## Decision

Add a non-core `ProposalSetDecoder` and training script:

```text
code/dream3r/proposal_set_decoder.py
code/dream3r/scripts/train_proposal_set_decoder.py
code/dream3r/tests/test_proposal_set_decoder.py
```

The decoder consumes cached proposal pointmaps/confidences plus Dream state
features and predicts bounded convex weights after a per-patch proposal-token
mixer. This is stronger than SCFHead but still inspectable and bounded.

## Boundary

No frozen core files were edited. No server run was launched. No checkpoint was
downloaded. The script is ready for a future BUAA-Server cache run.

## Verification

```text
python -m py_compile code/dream3r/proposal_set_decoder.py \
  code/dream3r/scripts/train_proposal_set_decoder.py \
  code/dream3r/tests/test_proposal_set_decoder.py

python -m pytest code/dream3r/tests/test_proposal_set_decoder.py -q
```

Result:

```text
2 passed
```

Warnings:

```text
PyTorch TransformerEncoder nested-tensor warning caused by norm_first=True.
Not a correctness failure.
```

## Next step

Run this only after scp / server authorization:

```bash
CUDA_VISIBLE_DEVICES=1 python -m dream3r.scripts.train_proposal_set_decoder \
  --cache <kitti_cache.pt> <eth3d_cache.pt> \
  --output-dir runs/dream3r_pd/proposal_set_decoder/seed_7 \
  --seed 7
```

Compare against SCFHead before any final-model performance claim.
