# DEC-20260606-044: Foundation3R contract and dense teacher smoke

Date: 2026-06-06
Status: accepted as Sprint 0/1 scaffold-positive
Scope: Dream3R proposal-free Foundation3R line

## Context

DEC-041 through DEC-043 closed the shallow proposal-free head family as
negative. The next route is not more scalar loss tuning; it is a real
proposal-free foundation path with dense teacher pretraining.

## Decision

Start Foundation3R as a separate non-core line:

```text
RGB images + optional Dream state -> pointmap / confidence
```

Inference must not accept:

```text
proposal pointmaps
proposal confidences
expert confidences
teacher pointmaps
teacher model calls
```

VGGT-Omega is allowed only as an offline dense teacher cache producer.

## Implementation

Added:

```text
code/dream3r/foundation3r_decoder.py
code/dream3r/scripts/build_foundation3r_dense_teacher_cache.py
code/dream3r/tests/test_foundation3r_contract.py
```

Updated:

```text
code/dream3r/__init__.py
```

The model forward contract consumes image tensors shaped `[B,N,C,H,W]`, optional
`memory_context`, and optional `conflict_score`. It reports:

```text
proposal_inputs_used=false
teacher_used_at_inference=false
```

The dense teacher cache builder supports:

```text
backend=mock
backend=vggt_omega
```

Saved entries strip forbidden proposal fields and keep only frames, offline
teacher pointmap/confidence/valid mask, optional GT, and optional Dream state.

## Server Gate

BUAA-Server tests:

```text
PYTHONPATH=/hdd3/kykt26/code/dream3r
conda env: dream3r
test: dream3r/tests/test_foundation3r_contract.py
result: 3 passed
```

Mock cache smoke:

```text
runs/stage6_fusion/foundation3r_dense_teacher_mock_20260606/dense_teacher_cache.pt
n_windows=2
proposal_fields_stripped=true
```

Real VGGT-Omega dense teacher smoke on GPU1:

```text
runs/stage6_fusion/foundation3r_dense_teacher_real_smoke_20260606/kitti_dense_teacher_cache.pt
runs/stage6_fusion/foundation3r_dense_teacher_real_smoke_20260606/eth3d_dense_teacher_cache.pt
```

Both real caches:

```text
teacher_backend=vggt_omega
n_windows=1
fallback_contamination_count=0
proposal_inputs_used=false
teacher_used_at_inference=false
proposal_fields_stripped=true
teacher_pointmap shape=[4,196,3]
teacher_confidence shape=[4,196,1]
teacher_valid_mask shape=[4,196]
has_gt=true
has_state=true
```

Server leak audit passed for both `.pt` caches: no `proposals`, `expert_order`,
`expert_confidences`, `proposal_pointmaps`, `proposal_confidences`, or
`teacher_model` fields in entries.

## Verdict

Sprint 0/1 scaffold is positive:

```text
contract_lock: pass
mock_cache_schema: pass
real_vggt_dense_teacher_smoke: pass on KITTI and ETH3D
leak_audit: pass
```

This is not a model-quality result yet. It is the first valid data/contract
foundation for training a real proposal-free Foundation3R v0.

## Next

Build the 50+50 real dense teacher cache on BUAA-Server GPU1, then implement
`train_foundation3r.py` only after the 50+50 cache passes schema and leak audit.
