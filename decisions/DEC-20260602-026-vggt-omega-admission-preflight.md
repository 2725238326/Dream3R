# DEC-20260602-026: VGGT-Omega admission preflight

Date: 2026-06-02
Status: blocked on gated checkpoint; smoke script ready
Scope: Dream3R v2.2 teacher-bank admission

## Context

DEC-025 closed the image-state native U1 gate negative. The fallback high-impact
architecture path from the V10 prompt is VGGT-Omega one-window teacher
admission, but it must stay a teacher/proposal-bank gate. VGGT-Omega is not
Dream3R itself and must not be substituted with vanilla VGGT or a fallback stub.

The upstream VGGT-Omega README exposes the intended API:

```text
VGGTOmega
load_and_preprocess_images
encoding_to_camera
predictions: depth, depth_conf, pose_enc, camera_and_register_tokens
```

It also states that checkpoints require Hugging Face access approval.

## Decision

Promote the prior DEC-016 execution draft into a concrete preflight gate by
adding:

```text
code/dream3r/scripts/smoke_vggt_omega_adapter.py
```

The script:

- imports upstream VGGT-Omega from an explicit repo path;
- loads an explicit checkpoint path;
- reads 1-4 image filenames from an explicit image list;
- runs upstream preprocessing and inference;
- decodes cameras with `encoding_to_camera`;
- converts depth + intrinsics into a Dream3R-shaped camera-frame pointmap;
- writes a JSON metadata file and a `.pt` ExpertProposal-like payload;
- rejects missing repo/checkpoint and fallback/stub outputs as non-success.

## Server preflight

Local clone of the public upstream repo succeeded at:

```text
commit: 39a0cb8af88554f15ddcb5354cd52bde588fa014
```

The BUAA-Server could not clone GitHub directly due a 443 timeout, so the
public code was copied to:

```text
/hdd3/kykt26/externals/vggt-omega
```

No conda environment mutation was performed and no checkpoint was downloaded.

The script was synchronized to:

```text
/hdd3/kykt26/code/dream3r/dream3r/scripts/smoke_vggt_omega_adapter.py
```

Server syntax check:

```text
conda run --no-capture-output -n dream3r \
  python -B -m py_compile dream3r/scripts/smoke_vggt_omega_adapter.py
```

Result: passed.

One-window preflight command:

```text
CUDA_VISIBLE_DEVICES=1 conda run --no-capture-output -n dream3r \
  python -m dream3r.scripts.smoke_vggt_omega_adapter \
    --repo /hdd3/kykt26/externals/vggt-omega \
    --checkpoint /hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt \
    --image-list runs/v22_admission/vggt_omega_smoke/images.txt \
    --image-resolution 512 \
    --output runs/v22_admission/vggt_omega_smoke/results.json
```

Result:

```json
{
  "adapter": "vggt_omega",
  "backend": "error",
  "failure_flags": [
    "FileNotFoundError: VGGT-Omega preflight failed; checkpoint not found: /hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt"
  ],
  "fallback_contamination_count": 1
}
```

## Verdict

The VGGT-Omega admission code path is ready, but real teacher admission is
blocked by missing approved checkpoint access. Do not mark VGGT-Omega admitted,
do not use vanilla VGGT as a substitute, and do not accept the Hugging Face demo
as a reproducible local teacher backend.

Once the approved checkpoint is present at the documented path, rerun the same
command. A pass requires `backend == "real"`, `fallback_contamination_count == 0`,
recorded runtime/VRAM, and a saved pointmap/confidence payload.

## Impact on "usable" status

Dream3R is not yet usable as a native model. The current usable bounded baseline
remains:

```text
proposal teachers + Dream state -> frozen StatePrior -> bounded residual
KITTI/ETH3D: 0.1448/0.1475
```

The next route to a usable prototype is either:

- approved VGGT-Omega checkpoint -> one-window real smoke -> tiny oracle cache;
- or a redesigned native objective that makes correct-state beat no-state and
  the locked baseline.
