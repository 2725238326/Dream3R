# Dream3R v1.1.0 Official Version

Date: 2026-06-08
Status: formal official release

## Version Identity

```text
name: Dream3R
version: v1.1.0
release candidate: domain_conditional_vggt_teacher
metric: AbsRel, lower is better
KITTI / ETH3D: 0.1448 / 0.0570
stable fallback: v1.0-rc1
```

Dream3R v1.1.0 is the official usable release of the current architecture. It
is a state-conditioned proposal-fusion 3R model with a domain-conditional
policy:

```text
KITTI -> v1.0-rc1 bounded StatePrior + residual
ETH3D -> VGGT-Omega-expanded SCF correct-state
```

It is not a proposal-free foundation 3R model.

## Official Import

```python
from dream3r.release_v11 import build_dream3r_v11_release

model = build_dream3r_v11_release()
out = model(
    proposal_pointmaps,
    proposal_confidences,
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

State-causality controls:

```text
KITTI state/no-state/shuffle: 0.1448 / 0.1553 / 0.1521
ETH3D state/no-state/shuffle: 0.0570 / 0.0583 / 0.0598
```

The correct-state branch beats no-state and shuffled-state on both domains.

## Completion Evidence

```text
local v1.1 verifier: pass
local v1.1 smoke: pass
local v1.0 fallback verifier: pass
local release tests: 12 passed
local full test suite: 300 passed, 2 skipped
BUAA-Server v1.1 verifier: pass
BUAA-Server v1.1 smoke: pass
BUAA-Server v1.0 fallback verifier: pass
BUAA-Server release tests: 12 passed
```

Smoke artifact:

```text
runs/release/v11_smoke/smoke_v11_release_model.json
```

## Required Verification

Local:

```powershell
python -B code\dream3r\scripts\verify_v11_release.py --root .
python -B code\dream3r\scripts\smoke_v11_release_model.py --output runs\release\v11_smoke\smoke_v11_release_model.json
python -B code\dream3r\scripts\verify_release_candidate.py --root .
```

Server:

```text
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -B dream3r/scripts/verify_v11_release.py --root . --skip-frozen-core
conda run -n dream3r python -B dream3r/scripts/smoke_v11_release_model.py --output runs/release/v11_smoke/smoke_v11_release_model.json
```

## Stable Fallback

The previous v1.0 release-candidate is preserved as a stable fallback:

```text
doc: release/STABLE_FALLBACK_V1_0_RC.md
api: dream3r.release_candidate.build_dream3r_release_candidate
KITTI / ETH3D: 0.1448 / 0.1475
```

## Claim Boundary

Safe to claim:

```text
Dream3R v1.1.0 is a complete official state-conditioned proposal-fusion 3R
release with verified KITTI/ETH3D domain branches.
```

Do not claim:

```text
proposal-free foundation 3R
image-only inference
Qwen geometry improvement
Foundation3R promotion
universal SOTA
```
