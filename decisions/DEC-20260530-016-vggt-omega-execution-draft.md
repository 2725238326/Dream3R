# DEC-20260530-016 — VGGT-Omega one-window execution draft

decision_id: DEC-20260530-016
date: 2026-05-30
scope: Dream3R-PD VGGT-Omega admission execution draft
status: draft; not authorized for execution

## Context

DEC-20260530-015 selected Dream3R-PD as the final architecture path.
DEC-20260530-014 made VGGT-Omega the first v2.2 teacher admission candidate.
`planning/VGGT_OMEGA_DEPLOYMENT_INVENTORY.md` records the upstream deployment
surface.

This DEC is a draft of the execution gate. It is intentionally not active:
no checkpoint download, install mutation, server run, or cache build is
authorized until this draft is promoted.

## Proposed action

Run a one-window VGGT-Omega adapter smoke on BUAA-Server GPU 1.

## Proposed paths

```text
repo:       /hdd3/kykt26/externals/vggt-omega
checkpoint: /hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt
dream3r:    /hdd3/kykt26/code/dream3r
output:     /hdd3/kykt26/code/dream3r/runs/v22_admission/vggt_omega_smoke/results.json
```

## Proposed implementation target

```text
code/dream3r/scripts/smoke_vggt_omega_adapter.py
```

Responsibilities:

- import upstream `VGGTOmega`;
- load checkpoint from an explicit path;
- load 2-4 image filenames from an explicit list;
- call upstream preprocessing and inference;
- decode `pose_enc` to camera parameters;
- convert depth + camera to Dream3R pointmap;
- write JSON metadata plus a small `.pt` tensor payload;
- assert `backend == "real"` before success.

## Proposed command

```bash
ssh BUAA-Server
cd /hdd3/kykt26/code/dream3r
CUDA_VISIBLE_DEVICES=1 python -m dream3r.scripts.smoke_vggt_omega_adapter \
  --repo /hdd3/kykt26/externals/vggt-omega \
  --checkpoint /hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt \
  --image-list runs/v22_admission/vggt_omega_smoke/images.txt \
  --image-resolution 512 \
  --output runs/v22_admission/vggt_omega_smoke/results.json
```

## Success criteria

- checkpoint loads without fallback;
- output includes `depth`, `depth_conf`, `pose_enc`, cameras, and register
  tokens;
- Dream3R pointmap shape is recorded;
- `backend == "real"`;
- runtime and peak VRAM are recorded;
- fallback contamination count is zero.

## Failure handling

| failure | action |
| --- | --- |
| checkpoint access denied | keep VGGT-Omega as planned comparator; continue ProposalSetDecoder on 3-expert cache |
| dependency conflict | do not mutate existing env; draft isolated env plan |
| OOM | draft lower-resolution/frame-count DEC update |
| no pointmap normalization | stop admission and implement depth-to-pointmap converter in isolation |

## Non-authorization

This draft does not authorize:

- Hugging Face checkpoint download;
- `pip install` on the existing Dream3R env;
- server execution;
- cache rebuild;
- benchmark table update;
- frozen core edits.
