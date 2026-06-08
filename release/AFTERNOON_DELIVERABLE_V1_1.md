# Dream3R Afternoon Deliverable

Date: 2026-06-08
Status: submit-ready package target, locally and BUAA-Server GPU1 verified

## Deliver This Model

Use Dream3R `v1.1.0` as the model to hand over this afternoon.

```text
API: dream3r.release_v11.build_dream3r_v11_release
Model type: state-conditioned proposal-fusion 3R
KITTI / ETH3D AbsRel: 0.1448 / 0.0570
Metric direction: lower is better
Fallback: v1.0-rc1, KITTI / ETH3D 0.1448 / 0.1475
```

## One-Sentence Description

Dream3R v1.1.0 is a state-conditioned proposal-fusion 3R model that uses Dream
state to fuse proposal experts, with a KITTI branch based on the bounded
StatePrior residual release and an ETH3D branch using VGGT-Omega-expanded SCF.

## Demo Commands

Local:

```powershell
python -B code\dream3r\scripts\run_dream3r_v11_demo.py --domain kitti --output runs\release\v11_demo\demo_kitti.json
python -B code\dream3r\scripts\run_dream3r_v11_demo.py --domain eth3d --output runs\release\v11_demo\demo_eth3d.json
```

Server:

```bash
cd /hdd3/kykt26/code/dream3r
CUDA_VISIBLE_DEVICES=1 conda run -n dream3r python -B dream3r/scripts/run_dream3r_v11_demo.py --domain kitti --output runs/release/v11_demo/demo_kitti.json
CUDA_VISIBLE_DEVICES=1 conda run -n dream3r python -B dream3r/scripts/run_dream3r_v11_demo.py --domain eth3d --output runs/release/v11_demo/demo_eth3d.json
```

Expected demo artifacts:

```text
runs/release/v11_demo/demo_kitti.json
runs/release/v11_demo/demo_eth3d.json
```

Real proposal-cache runtime demo on BUAA-Server GPU1:

```bash
cd /hdd3/kykt26/code/dream3r
CUDA_VISIBLE_DEVICES=1 conda run -n dream3r python -B dream3r/scripts/run_dream3r_v11_cache_demo.py --domain kitti --output runs/release/v11_cache_demo/cache_demo_kitti.json --max-entries 1 --device cuda
CUDA_VISIBLE_DEVICES=1 conda run -n dream3r python -B dream3r/scripts/run_dream3r_v11_cache_demo.py --domain eth3d --output runs/release/v11_cache_demo/cache_demo_eth3d.json --max-entries 1 --device cuda
```

Cache-demo artifacts:

```text
runs/release/v11_cache_demo/cache_demo_kitti.json
runs/release/v11_cache_demo/cache_demo_eth3d.json
```

Interpretation: this proves v1.1 consumes real proposal-cache entries with the
official branch policy. It is not a benchmark rerun.

## Required Verification

```powershell
python -B code\dream3r\scripts\verify_v11_release.py --root .
python -B code\dream3r\scripts\smoke_v11_release_model.py --output runs\release\v11_smoke\smoke_v11_release_model.json
python -B -m pytest --assert=plain code\dream3r\tests\test_v11_demo_script.py code\dream3r\tests\test_release_v11_architecture.py code\dream3r\tests\test_release_v11_smoke_model.py code\dream3r\tests\test_release_v12_experimental_architecture.py -q
```

Observed evidence:

```text
Local: v1.1/v1.0 verifiers pass, release tests 14 passed, cache-demo focused tests 11 passed, JSON checks pass.
BUAA-Server GPU1: synthetic demo KITTI/ETH3D pass, real-cache demo KITTI/ETH3D pass, v1.1/v1.0 verifiers pass, release tests 14 passed, v1.2 tests 4 passed.
```

## What To Say Under Questioning

Safe:

```text
The official model is v1.1.0.
It is not proposal-free yet.
It is a controlled state-conditioned proposal-fusion 3R package.
VGGT-Omega contributes through the ETH3D branch and teacher/proposal pipeline.
Qwen is diagnostic-only and not used for geometry.
v1.2-exp0 is the next experimental core-bridge direction, not the official model.
```

Do not say:

```text
We already have a proposal-free 3R foundation model.
Qwen improves 3D geometry.
VGGT-Omega alone is Dream3R.
v1.2 beats v1.1.
```

## Current Risk

The package is deliverable because the release API, smoke path, demo path,
state-causality controls, and fallback are documented and testable. The main
research risk is that the deeper proposal-free architecture is not solved yet;
that should be presented as future work, not as the afternoon deliverable.
