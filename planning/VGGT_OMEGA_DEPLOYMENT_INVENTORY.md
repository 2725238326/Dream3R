# VGGT-Omega deployment inventory

date: 2026-05-30
status: inventory complete; execution gated
sources:
  - https://vggt-omega.github.io/
  - https://github.com/facebookresearch/vggt-omega
  - https://arxiv.org/abs/2605.15195

## Purpose

This inventory prepares the first Dream3R-PD teacher admission lane:

```text
VGGT-Omega -> ExpertProposal -> SCF / ProposalSetDecoder cache
```

It does not authorize checkpoint download, server install mutation, or model
execution.

## Upstream facts

| field | value |
| --- | --- |
| repo | `https://github.com/facebookresearch/vggt-omega` |
| project page | `https://vggt-omega.github.io/` |
| paper | `https://arxiv.org/abs/2605.15195` |
| venue label | CVPR 2026 Oral, per project page / repo README |
| code state | public GitHub repo; one public main-branch commit visible on 2026-05-30 |
| package root | `vggt_omega/` |
| demo entry | `demo_gradio.py` |
| license | upstream `LICENSE`; must be checked before redistribution |

## Checkpoint policy

The upstream README says checkpoint access must be requested on Hugging Face
before download.

Models listed by upstream:

| model | resolution | text alignment | Dream3R use |
| --- | ---: | --- | --- |
| `VGGT-Omega-1B-512` | 512 | no | primary geometry teacher candidate |
| `VGGT-Omega-1B-256-Text-Alignment` | 256 | yes | optional language-aligned register analysis, not first smoke |

Dream3R first smoke should use:

```text
VGGT-Omega-1B-512
```

unless GPU memory forces a lower-resolution adaptation.

## Dependency surface

Upstream install path:

```bash
git clone git@github.com:facebookresearch/vggt-omega.git
cd vggt-omega
pip install -r requirements.txt
pip install -e .
```

Demo-only dependencies:

```bash
pip install -r requirements_demo.txt
```

Dream3R should avoid demo dependencies for first smoke. The first adapter
needs only model import, image preprocessing, camera decoding, and tensor
output capture.

## Minimal upstream inference shape

Upstream quick-start imports:

```python
from vggt_omega.models import VGGTOmega
from vggt_omega.utils.load_fn import load_and_preprocess_images
from vggt_omega.utils.pose_enc import encoding_to_camera
```

Expected call:

```python
model = VGGTOmega().to("cuda").eval()
model.load_state_dict(torch.load(checkpoint_path, map_location="cpu"))
images = load_and_preprocess_images(image_names, image_resolution=512).to("cuda")

with torch.inference_mode():
    predictions = model(images)

extrinsics, intrinsics = encoding_to_camera(
    predictions["pose_enc"],
    predictions["images"].shape[-2:],
)
```

Outputs explicitly named upstream:

```text
predictions["pose_enc"]
predictions["images"]
predictions["depth"]
predictions["depth_conf"]
predictions["camera_and_register_tokens"]
predictions["text_alignment_embedding"]  # text-aligned checkpoint only
```

## ExpertProposal normalization

Dream3R adapter target:

```text
expert_name: "vggt_omega"
backend: "real"
version: upstream commit + checkpoint id
pointmap: unprojected depth using predicted camera intrinsics/extrinsics
confidence: depth_conf normalized to [0, 1] if needed
optional_depth: predictions["depth"]
optional_camera: {extrinsics, intrinsics}
optional_tracks: null for first smoke
optional_dynamic_mask: null for first smoke
method_state:
  camera_tokens
  registers
runtime_ms: measured
vram_mb: measured if torch cuda stats available
failure_flags: []
```

Open implementation point:

```text
The upstream quick start returns depth and cameras, not a Dream3R pointmap.
First adapter must add a deterministic depth-to-pointmap unprojection step.
```

## Runtime / memory expectation

Upstream README reports A100 peak GPU memory for `VGGT-Omega-1B-512` with
624x416 inputs from 1 to 500 frames. First smoke should use 2-4 frames and
record actual memory on BUAA-Server GPU 1.

Risk:

```text
TITAN RTX / local server memory may differ from upstream A100 measurements.
If smoke OOMs, retry only after a DEC changes image_resolution or frame count.
```

## Proposed server layout

```text
/hdd3/kykt26/externals/vggt-omega/
/hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt
/hdd3/kykt26/code/dream3r/runs/v22_admission/vggt_omega_smoke/
```

These paths are proposed only. The execution DEC must confirm or change them.

## First smoke command shape

Do not run until DEC-20260530-016 is explicitly active for execution.

```bash
ssh BUAA-Server
cd /hdd3/kykt26/code/dream3r
CUDA_VISIBLE_DEVICES=1 python -m dream3r.scripts.smoke_vggt_omega_adapter \
  --repo /hdd3/kykt26/externals/vggt-omega \
  --checkpoint /hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt \
  --image-list <small_kitti_or_eth3d_list.txt> \
  --image-resolution 512 \
  --output runs/v22_admission/vggt_omega_smoke/results.json
```

The script does not exist yet. It is the recommended implementation target
after checkpoint access and install policy are confirmed.

## Go / no-go

Go only if:

- checkpoint access is approved;
- license is acceptable for research use;
- dependency delta does not break existing Dream3R env;
- one-window smoke can record `backend == "real"`;
- fallback/stub entries are excluded from cache.

No-go if:

- checkpoint cannot be obtained;
- install requires destructive env replacement;
- first smoke cannot normalize depth/camera to a pointmap;
- memory exceeds available GPU under 2-4 frames.
