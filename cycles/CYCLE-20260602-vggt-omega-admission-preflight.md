# CYCLE-20260602: VGGT-Omega admission preflight

Date: 2026-06-02
Status: blocked on gated checkpoint
Decision: `decisions/DEC-20260602-026-vggt-omega-admission-preflight.md`

## Trigger

The image-state native U1 gate failed. The V10 acceleration prompt named
VGGT-Omega one-window teacher admission as the fallback high-impact gate if
native work was blocked.

## Work completed

Added:

```text
code/dream3r/scripts/smoke_vggt_omega_adapter.py
```

The script normalizes VGGT-Omega outputs into Dream3R admission artifacts:

- JSON metadata;
- `.pt` ExpertProposal-like payload;
- camera-frame pointmap converted from depth + intrinsics;
- confidence flattened from depth confidence;
- camera/register tokens preserved as method state;
- explicit no-fallback success rule.

## Server actions

Public upstream code was cloned locally at commit:

```text
39a0cb8af88554f15ddcb5354cd52bde588fa014
```

The BUAA-Server direct GitHub clone failed with port-443 timeout, so the public
code was copied into:

```text
/hdd3/kykt26/externals/vggt-omega
```

No dependency install and no checkpoint download were performed.

Server verification:

```text
cd /hdd3/kykt26/code/dream3r
conda run --no-capture-output -n dream3r \
  python -B -m py_compile dream3r/scripts/smoke_vggt_omega_adapter.py
```

Result: passed.

## Preflight result

Input image list:

```text
runs/v22_admission/vggt_omega_smoke/images.txt
```

Output:

```text
runs/v22_admission/vggt_omega_smoke/results.json
```

Result:

```text
backend: error
failure: checkpoint not found:
  /hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt
fallback_contamination_count: 1
```

## Verdict

VGGT-Omega is not admitted. The code path is ready, but the one-window teacher
smoke is blocked until the approved checkpoint exists on BUAA-Server. The
official checkpoint policy requires access approval, so this cannot be bypassed
inside Dream3R without breaking the real-backend admission contract.

## Next action

After the approved checkpoint is staged:

```text
CUDA_VISIBLE_DEVICES=1 conda run --no-capture-output -n dream3r \
  python -m dream3r.scripts.smoke_vggt_omega_adapter \
    --repo /hdd3/kykt26/externals/vggt-omega \
    --checkpoint /hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt \
    --image-list runs/v22_admission/vggt_omega_smoke/images.txt \
    --image-resolution 512 \
    --output runs/v22_admission/vggt_omega_smoke/results.json
```

Pass only if `backend == "real"` and fallback contamination is zero.
