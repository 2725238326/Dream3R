# Dream3R Context Compaction - 2026-06-08

Status: compressed handoff after v1.1 usable-model packaging.

Read this after `TASK_SNAPSHOT.md` when resuming Dream3R work. It is a
compressed state anchor, not a new architecture decision. Older decision/cycle
files remain the source of detailed evidence.

## Current Stop Condition

```text
status: idle
usable tonight: Dream3R v1.1-rc1
official stable identity: Dream3R v1.0-rc1
metric: AbsRel, lower is better
server rule: use BUAA-Server GPU1 only for model-code execution
frozen core: preserved
```

## Required Read Order

```text
1. TASK_SNAPSHOT.md
2. handoff/CONTEXT_COMPACTION_20260608_V11_USABLE_MODEL.md
3. ARCHITECTURE.md
4. release/USABLE_MODEL_V1_1.md
5. release/ARTIFACTS.json
6. release/ARCHITECTURE_STATUS.json
7. decisions/DEC-20260607-049-v11-usable-model-package.md
```

## Usable Model

Dream3R v1.1-rc1 is the strongest usable model surface currently available.
It is a reversible domain-conditional wrapper:

```text
KITTI -> Dream3R v1.0-rc1 bounded StatePrior + residual
ETH3D -> VGGT-Omega-expanded SCF correct-state
```

Import surface:

```python
from dream3r.release_v11 import build_dream3r_v11_release

model = build_dream3r_v11_release()
out = model(proposal_pointmaps, proposal_confidences, memory_context, conflict_score, domain="kitti")
```

Files:

```text
code/dream3r/release_v11.py
code/dream3r/scripts/verify_v11_release.py
code/dream3r/tests/test_release_v11_architecture.py
code/dream3r/tests/test_release_v11_verifier.py
release/USABLE_MODEL_V1_1.md
```

Metrics and controls:

```text
KITTI state/no-state/shuffle: 0.1448 / 0.1553 / 0.1521
ETH3D state/no-state/shuffle: 0.0570 / 0.0583 / 0.0598
usable score: KITTI 0.1448, ETH3D 0.0570
unified gate: promotable_to_official=true
artifact: runs/v22_admission/domain_conditional_teacher/unified_gate_candidate_with_kitti_no_state_server.json
```

Interpretation:

```text
0.1448 / 0.0570 are AbsRel values; lower is better.
Correct-state beats no-state and shuffled-state on both domains.
v1.1-rc1 is usable, but official stable remains v1.0-rc1 until the release
identity files are deliberately switched.
```

## Official Stable Fallback

Dream3R v1.0-rc1 remains the official stable package:

```text
policy: frozen StatePrior + bounded residual
KITTI/ETH3D: 0.1448 / 0.1475
api: dream3r.release_candidate.build_dream3r_release_candidate
verifier: code/dream3r/scripts/verify_release_candidate.py
docs: release/OFFICIAL_VERSION.md, release/ARCHITECTURE_V1_0_RC.md
```

The 0.1448/0.1475 values are not "particularly bad" within this project
context; they are the selected controlled release baseline and are lower-is-
better AbsRel metrics. The v1.1 ETH3D branch improves ETH3D to 0.0570 by using
VGGT-Omega-expanded SCF.

## VGGT-Omega Status

VGGT-Omega is real and staged on BUAA-Server, but it is not a standalone
Dream3R geometry claim.

```text
external repo: /hdd3/kykt26/externals/vggt-omega
checkpoint: /hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt
one-window smoke: backend=real, fallback_contamination_count=0
smoke artifact: runs/v22_admission/vggt_omega_smoke/results_after_upload_fix_20260604.json
oracle admission: positive
release-control gate: negative on KITTI as universal replacement
accepted use: ETH3D branch inside v1.1 domain-conditional policy; dense teacher and feature cache for Foundation3R experiments
```

## Qwen Status

Qwen3-VL-2B-Instruct is not part of the geometry model and is not promotable
for routing/Critic with current evidence.

```text
server checkpoint: /hdd3/kykt26/checkpoints/qwen/Qwen3-VL-2B-Instruct
isolated smoke env: /hdd3/kykt26/envs/qwen3vl2b_smoke
schema smoke: 5/5 strict JSON pass
50-window controller: real/shuffle/disabled all route to Fast3R and score 0.2365 vs oracle 0.1489
v2 calibrated controller: oracle 0.1489, real 0.1813, shuffle 0.1776, disabled 0.2365
semantic Critic-prior: geometry-only F1 0.9211, real+geometry F1 0.8947, disabled+geometry F1 0.9211
current rule: keep Qwen as offline annotation/diagnostic evidence only
```

Do not claim Qwen geometry capability or Qwen-assisted model improvement.

## Proposal-Free and Foundation3R Status

The user requested a real proposal-free 3R direction. Current code has a real
proposal-free contract, but no promotable model yet.

ProposalFree3R:

```text
contract: image tokens + Dream state -> pointmap
forbidden inputs: proposal pointmaps, expert confidences
sparse gate20: state 0.3273/0.4029, no-state 0.3318/0.4050, shuffle 0.3221/0.4041
teacher-loss gate20: state 0.3319/0.4056, no-state 0.3292/0.4049, shuffle 0.3288/0.4116
AbsRel/capacity gate: state 0.3326/0.4058, no-state 0.3327/0.4080, shuffle 0.3328/0.4064
verdict: scaffold-positive, model-negative
```

Foundation3R dense teacher:

```text
50+50 KITTI/ETH3D dense teacher cache: pass
failures: 0
fallback: 0
proposal fields stripped for student cache
proposal_inputs_used=false
teacher_used_at_inference=false
```

Foundation3R scratch student:

```text
best diagnostic: train about 0.4620/0.3798, test about 0.4734/0.3271
teacher holdout: 0.3554/0.0913
verdict: negative; do not repeat unchanged scratch sweeps
```

Foundation3R VGGT feature student:

```text
feature caches: runs/stage6_fusion/foundation3r_vggt_feature_50x2_20260607/
vggt_patch_features shape: [4,196,128]
hybrid loss: collapses to 0.4734/0.3271
teacher-only 20e state: 0.3237/0.1424
teacher-only 20e no-state: 0.3260/0.1489
teacher-only 20e shuffle: 0.3246/0.1330
verdict: experimental-positive vs scratch, but state causality is not established
```

Next Foundation3R work must add explicit Dream-state modulation or a stronger
representation gate while preserving proposal-free inference. Do not spend
more runs on the unchanged scratch head or unchanged teacher-only feature head.

## Frozen Core

Do not edit these files for release/optimization work unless a new explicit
decision opens them:

```text
code/dream3r/model.py
code/dream3r/anchor_bank.py
code/dream3r/nsa_attention.py
code/dream3r/bus.py
code/dream3r/orchestrator.py
code/dream3r/repair.py
code/dream3r/modules.py
code/dream3r/contracts.py
code/dream3r/config.py
```

## Validation Evidence To Preserve

Local validation already passed for the v1.1 packaging:

```powershell
python -B -m pytest --assert=plain code\dream3r\tests\test_release_candidate_architecture.py code\dream3r\tests\test_release_candidate_verifier.py code\dream3r\tests\test_release_v11_architecture.py code\dream3r\tests\test_release_v11_verifier.py -q
# 11 passed

python -B code\dream3r\scripts\verify_v11_release.py --root .
# status pass

python -B code\dream3r\scripts\verify_release_candidate.py --root .
# status pass
```

BUAA-Server validation already passed:

```text
repo: /hdd3/kykt26/code/dream3r
v1.1 pytest subset: 6 passed
verify_v11_release.py --skip-frozen-core: pass
verify_release_candidate.py --skip-frozen-core: pass
```

## What Not To Claim

Do not claim:

```text
proposal-free foundation model is solved
image-only Dream3R inference is solved
Qwen improves geometry
Qwen is a trained Router/Critic
VGGT-Omega is universally better than the release baseline
v1.1-rc1 is official stable unless release/OFFICIAL_VERSION.md is switched
SOTA or broad benchmark superiority
```

## Next Work Priority

Near-term usable-model path:

```text
1. Use v1.1-rc1 for demo/package.
2. Keep v1.0-rc1 as stable fallback.
3. If promoting v1.1 to official stable, update official version docs and rerun all release verifiers locally and on BUAA-Server GPU1.
```

Research path:

```text
1. Continue proposal-free Foundation3R only through explicit state modulation or stronger pretrained representation.
2. Keep no-proposal and no-teacher-inference controls.
3. Require state/no-state/shuffle separation before any promotion.
4. Treat Qwen as optional diagnostic metadata only until a larger causal Critic/proposal-disagreement gate is built.
```

## Dirty Worktree Note

The worktree contains many modified and untracked files from the ongoing
release, Qwen, VGGT, proposal-free, and Foundation3R lanes. Do not revert them
blindly. Preserve unrelated user/generated changes and edit only the current
documented scope.
