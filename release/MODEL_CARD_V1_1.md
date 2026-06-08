# Dream3R v1.1.0 Model Card

Date: 2026-06-08
Status: official afternoon-deliverable model package

## Identity

```text
Name: Dream3R
Version: v1.1.0
Candidate: domain_conditional_vggt_teacher
API: dream3r.release_v11.build_dream3r_v11_release
Metric: AbsRel, lower is better
KITTI / ETH3D: 0.1448 / 0.0570
Stable fallback: v1.0-rc1, KITTI / ETH3D 0.1448 / 0.1475
```

## What The Model Is

Dream3R v1.1.0 is a state-conditioned proposal-fusion 3R model. It consumes a
proposal bank from existing 3R backbones plus Dream state/context tensors, then
outputs a fused pointmap, confidence map, and expert weights.

The official domain policy is:

```text
KITTI -> v1.0-rc1 bounded StatePrior + residual
ETH3D -> VGGT-Omega-expanded SCF correct-state
```

## What The Model Is Not

Do not present v1.1.0 as:

```text
proposal-free foundation 3R
image-only inference
Qwen geometry model
universal SOTA
full long-sequence streaming deployment
```

The proposal-free Foundation3R line remains research-only after the current
state-modulation gate failed promotion. Qwen remains diagnostic/offline
semantic-cache evidence only.

## Runtime Contract

The callable release wrapper expects:

```text
proposal_pointmaps:   [batch, experts, views, patches, 3]
proposal_confidences: [batch, experts, views, patches, 1]
memory_context:       [batch, d_memory]  # default 32; proposal caches may use 128
conflict_score:       [batch, 1]
domain:               "kitti" or "eth3d"
```

It returns:

```text
final_pointmap:    [batch, views, patches, 3]
final_confidence:  [batch, views, patches, 1]
expert_weights:    [batch, experts, views, patches]
domain_branch:     "kitti_v1_0_rc1" or "eth3d_vggt_omega_scf"
release_version:   "v1.1.0"
```

## Demo Command

Local:

```powershell
python -B code\dream3r\scripts\run_dream3r_v11_demo.py --domain kitti --output runs\release\v11_demo\demo_kitti.json
python -B code\dream3r\scripts\run_dream3r_v11_demo.py --domain eth3d --output runs\release\v11_demo\demo_eth3d.json
```

BUAA-Server GPU1:

```bash
cd /hdd3/kykt26/code/dream3r
CUDA_VISIBLE_DEVICES=1 conda run -n dream3r python -B dream3r/scripts/run_dream3r_v11_demo.py --domain kitti --output runs/release/v11_demo/demo_kitti.json
CUDA_VISIBLE_DEVICES=1 conda run -n dream3r python -B dream3r/scripts/run_dream3r_v11_demo.py --domain eth3d --output runs/release/v11_demo/demo_eth3d.json
```

The demo uses synthetic proposal-bank tensors to prove the release API and
runtime contract. It is not a benchmark rerun.

## Real Cache Runtime Demo

BUAA-Server GPU1:

```bash
cd /hdd3/kykt26/code/dream3r
CUDA_VISIBLE_DEVICES=1 conda run -n dream3r python -B dream3r/scripts/run_dream3r_v11_cache_demo.py --domain kitti --output runs/release/v11_cache_demo/cache_demo_kitti.json --max-entries 1 --device cuda
CUDA_VISIBLE_DEVICES=1 conda run -n dream3r python -B dream3r/scripts/run_dream3r_v11_cache_demo.py --domain eth3d --output runs/release/v11_cache_demo/cache_demo_eth3d.json --max-entries 1 --device cuda
```

Artifacts:

```text
runs/release/v11_cache_demo/cache_demo_kitti.json
runs/release/v11_cache_demo/cache_demo_eth3d.json
```

This consumes real proposal-cache entries and validates branch expert order:
KITTI uses `fast3r/mast3r/spann3r`; ETH3D uses
`fast3r/mast3r/spann3r/vggt_omega`. It is runtime-contract evidence, not a
formal benchmark rerun.

## Evidence

State-causality controls:

```text
KITTI state/no-state/shuffle: 0.1448 / 0.1553 / 0.1521
ETH3D state/no-state/shuffle: 0.0570 / 0.0583 / 0.0598
```

Verification entrypoints:

```text
code/dream3r/scripts/verify_v11_release.py
code/dream3r/scripts/smoke_v11_release_model.py
code/dream3r/scripts/run_dream3r_v11_demo.py
code/dream3r/scripts/run_dream3r_v11_cache_demo.py
code/dream3r/tests/test_v11_demo_script.py
```

Current verification:

```text
Local: v1.1 verifier pass, v1.0 fallback verifier pass, release tests 14 passed, cache-demo focused tests 11 passed.
BUAA-Server GPU1: synthetic demo KITTI/ETH3D pass, real-cache demo KITTI/ETH3D pass, v1.1/v1.0 verifiers pass, release tests 14 passed, focused cache-demo tests 11 passed.
```

Primary artifact docs:

```text
release/COMPLETE_MODEL_V1_1.md
release/EFFECTIVE_ARCHITECTURE_V1_1.md
release/ARCHITECTURE_DIAGRAM_V1_1.md
release/ARTIFACTS.json
```

## Limitation Summary

The official v1.1.0 model is useful as a controlled state-conditioned
proposal-fusion release package. It is not yet the final research ambition of a
native, proposal-free 3R foundation model. The next promotable v1.2 path must
show real-cache metric improvement and state/no-state/shuffle separation before
it replaces this package.
