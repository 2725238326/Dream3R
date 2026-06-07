# Cycle 20260606: Foundation3R Contract And Dense Teacher Smoke

Date: 2026-06-06
Status: closed scaffold-positive
Decision: `decisions/DEC-20260606-044-foundation3r-contract-dense-teacher-smoke.md`

## Goal

Start the real proposal-free Foundation3R line without repeating the negative
shallow-head path.

## Action

Added:

```text
code/dream3r/foundation3r_decoder.py
code/dream3r/scripts/build_foundation3r_dense_teacher_cache.py
code/dream3r/tests/test_foundation3r_contract.py
```

Synced to BUAA-Server and ran:

```text
local targeted tests: 11 passed
server Foundation3R contract tests: 3 passed
server mock dense cache smoke: pass
server real VGGT-Omega KITTI 1-window dense cache: pass
server real VGGT-Omega ETH3D 1-window dense cache: pass
server leak audit: pass
```

## Result

Real cache reports were mirrored locally:

```text
runs/stage6_fusion/foundation3r_dense_teacher_real_smoke_20260606/kitti_dense_teacher_cache.json
runs/stage6_fusion/foundation3r_dense_teacher_real_smoke_20260606/eth3d_dense_teacher_cache.json
```

Both real smoke caches have:

```text
teacher_backend=vggt_omega
n_windows=1
fallback_contamination_count=0
proposal_fields_stripped=true
proposal_inputs_used=false
teacher_used_at_inference=false
teacher_pointmap=[4,196,3]
teacher_confidence=[4,196,1]
teacher_valid_mask=[4,196]
has_gt=true
has_state=true
```

## Verdict

Sprint 0/1 is scaffold-positive. We now have the first valid proposal-free
contract and real dense teacher cache path. This is not a trained model result.

Next work is 50+50 real dense teacher cache generation and leak audit, followed
by Foundation3R v0 training code.
