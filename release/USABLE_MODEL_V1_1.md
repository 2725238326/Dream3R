# Dream3R v1.1.0 Usable Model

Date: 2026-06-08
Status: current effective architecture, reversible to v1.0-rc1 stable fallback

Compressed handoff:

```text
handoff/CONTEXT_COMPACTION_20260608_V11_USABLE_MODEL.md
```

## Identity

```text
name: Dream3R
version: v1.1.0
candidate: domain_conditional_vggt_teacher
metric: AbsRel, lower is better
KITTI / ETH3D: 0.1448 / 0.0570
```

This is the strongest controlled model surface currently available and is the
current effective Dream3R architecture. It is not a proposal-free foundation
model. It is a domain-conditional
proposal-bank 3R model:

```text
KITTI -> Dream3R v1.0-rc1 bounded StatePrior + residual
ETH3D -> VGGT-Omega-expanded SCF correct-state
```

## Import

```python
from dream3r.release_v11 import build_dream3r_v11_release

model = build_dream3r_v11_release()

out_kitti = model(
    proposal_pointmaps_kitti,      # [B, 3, N, P, 3]
    proposal_confidences_kitti,    # [B, 3, N, P, 1]
    memory_context,
    conflict_score,
    domain="kitti",
)

out_eth3d = model(
    proposal_pointmaps_eth3d,      # [B, 4, N, P, 3], includes vggt_omega
    proposal_confidences_eth3d,    # [B, 4, N, P, 1]
    memory_context,
    conflict_score,
    domain="eth3d",
)
```

## Evidence

Unified gate artifact:

```text
runs/v22_admission/domain_conditional_teacher/unified_gate_candidate_with_kitti_no_state_server.json
```

Controls:

```text
KITTI  state/no-state/shuffle: 0.1448 / 0.1553 / 0.1521
ETH3D  state/no-state/shuffle: 0.0570 / 0.0583 / 0.0598
```

The correct-state branch beats no-state and shuffled-state on both domains.

Real proposal-cache runtime evidence:

```text
runs/release/v11_cache_demo/cache_demo_kitti.json
runs/release/v11_cache_demo/cache_demo_eth3d.json
```

These reports were generated on BUAA-Server GPU1 by
`code/dream3r/scripts/run_dream3r_v11_cache_demo.py`. They prove that the
official v1.1 API consumes existing SCF/VGGT-Omega proposal caches with strict
expert-order validation. They are not a benchmark rerun.

## Verification

```powershell
cd E:\Dream3R
python -B code\dream3r\scripts\verify_v11_release.py --root .
python -B -m pytest --assert=plain code\dream3r\tests\test_release_v11_architecture.py -q
```

Server cache runtime check:

```bash
cd /hdd3/kykt26/code/dream3r
CUDA_VISIBLE_DEVICES=1 conda run -n dream3r python -B dream3r/scripts/run_dream3r_v11_cache_demo.py --domain kitti --output runs/release/v11_cache_demo/cache_demo_kitti.json --max-entries 1 --device cuda
CUDA_VISIBLE_DEVICES=1 conda run -n dream3r python -B dream3r/scripts/run_dream3r_v11_cache_demo.py --domain eth3d --output runs/release/v11_cache_demo/cache_demo_eth3d.json --max-entries 1 --device cuda
```

Expected verifier status:

```text
"status": "pass"
"version": "v1.1.0"
```

## Boundaries

Do not claim:

- proposal-free native 3R foundation model;
- Qwen geometry capability;
- end-to-end image-only inference;
- universal SOTA.

This package is the current effective controlled model for the existing
Dream3R proposal-bank runtime. The proposal-free Foundation3R/VGGT-feature
line remains experimental and is not the effective release.
