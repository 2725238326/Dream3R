# Dream3R v1.1.0 Complete Model Package

Date: 2026-06-08
Status: complete official model package

## Completion Verdict

Dream3R v1.1.0 is complete as the current official model package.

It is a state-conditioned proposal-fusion 3R model with a domain-conditional
policy:

```text
KITTI -> v1.0-rc1 bounded StatePrior + residual
ETH3D -> VGGT-Omega-expanded SCF correct-state
```

Metric:

```text
AbsRel, lower is better
KITTI / ETH3D: 0.1448 / 0.0570
```

## What Is Complete

```text
API:        dream3r.release_v11.build_dream3r_v11_release
Verifier:   code/dream3r/scripts/verify_v11_release.py
Smoke:      code/dream3r/scripts/smoke_v11_release_model.py
Runbook:    release/RUNBOOK.md
Fallback:   dream3r.release_candidate.build_dream3r_release_candidate
Docs:       release/EFFECTIVE_ARCHITECTURE_V1_1.md
```

The full-model smoke executes both runtime branches and writes:

```text
runs/release/v11_smoke/smoke_v11_release_model.json
```

## Required Commands

Local:

```powershell
python -B code\dream3r\scripts\verify_v11_release.py --root .
python -B code\dream3r\scripts\smoke_v11_release_model.py --output runs\release\v11_smoke\smoke_v11_release_model.json
python -B code\dream3r\scripts\verify_release_candidate.py --root .
python -B -m pytest --assert=plain code\dream3r\tests\test_release_candidate_architecture.py code\dream3r\tests\test_release_candidate_verifier.py code\dream3r\tests\test_release_v11_architecture.py code\dream3r\tests\test_release_v11_verifier.py code\dream3r\tests\test_release_v11_smoke_model.py -q
```

Server:

```text
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -B dream3r/scripts/verify_v11_release.py --root . --skip-frozen-core
conda run -n dream3r python -B dream3r/scripts/smoke_v11_release_model.py --output runs/release/v11_smoke/smoke_v11_release_model.json
conda run -n dream3r python -B -m pytest --assert=plain dream3r/tests/test_release_candidate_architecture.py dream3r/tests/test_release_candidate_verifier.py dream3r/tests/test_release_v11_architecture.py dream3r/tests/test_release_v11_verifier.py dream3r/tests/test_release_v11_smoke_model.py -q
```

## Current Evidence

Local:

```text
v1.1 verifier: pass
v1.1 smoke: pass
v1.0 fallback verifier: pass
release tests: 12 passed
full test suite: 300 passed, 2 skipped
```

BUAA-Server:

```text
v1.1 verifier: pass
v1.1 smoke: pass
v1.0 fallback verifier: pass
release tests: 12 passed
```

## Claim Boundary

Safe to claim:

```text
Dream3R v1.1.0 is a complete official state-conditioned proposal-fusion 3R
package with verified KITTI/ETH3D domain branches.
```

Do not claim:

```text
proposal-free foundation 3R
image-only inference
Qwen geometry improvement
Foundation3R promotion
universal SOTA
```

## Next Work After Completion

Next work is presentation/manuscript/demo packaging around v1.1, or a new
separate proposal-free Foundation3R redesign. Do not mix those lines.
