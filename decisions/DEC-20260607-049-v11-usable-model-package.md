# DEC-20260607-049: v1.1 Usable Model Package

Status: accepted

## Decision

Package the passed domain-conditional VGGT policy as the tonight usable Dream3R model:

```text
version: v1.1-rc1
candidate: domain_conditional_vggt_teacher
KITTI -> Dream3R v1.0-rc1 bounded StatePrior + residual
ETH3D -> VGGT-Omega-expanded SCF correct-state
```

Keep `v1.0-rc1` as the official stable package and add `v1.1-rc1` as a reversible usable release candidate. This avoids silently overwriting the official identity while giving a callable best-current model surface.

## Implemented

- `code/dream3r/release_v11.py`
  - Adds `Dream3RDomainConditionalRelease`.
  - Adds `build_dream3r_v11_release()`.
  - Routes `domain="kitti"` to the v1.0 ProposalSetDecoder branch.
  - Routes `domain="eth3d"` to the 4-expert VGGT-Omega-expanded SCF branch.
- `code/dream3r/scripts/verify_v11_release.py`
  - Checks v1.1 manifest, unified gate pass, API metadata, docs, and optional frozen-core policy.
- `release/USABLE_MODEL_V1_1.md`
  - Documents import, tensor contract, metrics, controls, and non-claims.
- `release/ARTIFACTS.json`
  - Records `usable_model_v1_1`.

## Evidence

Unified gate:

```text
artifact: runs/v22_admission/domain_conditional_teacher/unified_gate_candidate_with_kitti_no_state_server.json
KITTI state/no-state/shuffle: 0.1448 / 0.1553 / 0.1521
ETH3D state/no-state/shuffle: 0.0570 / 0.0583 / 0.0598
```

Verification:

```text
local v1.1 architecture/verifier tests: 6 passed
local v1.1 verifier: pass
BUAA-Server v1.1 architecture/verifier tests: 6 passed
BUAA-Server v1.1 verifier: pass
BUAA-Server v1.0 verifier: pass
```

## Consequence

For tonight demos and internal use, use:

```python
from dream3r.release_v11 import build_dream3r_v11_release
```

This is still a proposal-bank model, not a proposal-free Foundation3R model.
Foundation3R/VGGT-feature remains experimental and must not be represented as the delivered usable model.

