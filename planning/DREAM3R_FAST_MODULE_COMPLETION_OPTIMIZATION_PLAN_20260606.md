# Dream3R Fast Module Completion And Optimization Plan

Date: 2026-06-06

Update: Sprint 1 and Sprint 2 have now executed on BUAA-Server GPU1. Both
objective patches are implemented and tested, but neither beats the selected
release candidate. Keep this document as the optimization record and stop
repeating the same small native-student objective sweeps.

## Objective

Move quickly without destabilizing the current release candidate.

Current RC:

```text
frozen StatePrior + bounded residual refinement
KITTI / ETH3D abs-rel: 0.1448 / 0.1475
```

This plan has two tracks:

1. Finish the module explanation/packaging needed for release.
2. Run one bounded optimization lane that can actually improve the model.

## Non-Negotiable Guardrails

- Do not edit frozen core for the first optimization pass:

```text
code/dream3r/model.py
code/dream3r/modules.py
code/dream3r/bus.py
code/dream3r/anchor_bank.py
code/dream3r/nsa_attention.py
code/dream3r/contracts.py
code/dream3r/orchestrator.py
code/dream3r/repair.py
code/dream3r/config.py
```

- Do not rerun Qwen as a model path.
- Do not rerun image-state U1 unchanged.
- Do not promote VGGT-Omega without state/no-state/shuffle controls.
- Do not call any result publishable unless it beats the RC and passes
  causality controls.

## Module Completion Matrix

| Module | Current State | Missing To Be "Complete" | Fast Action |
| --- | --- | --- | --- |
| `StatePriorHead` | implemented, diagnostic-positive | nothing urgent | keep frozen as teacher/control |
| `ProposalSetDecoder` | RC surface; bounded residual works | package exact RC command and artifact lineage | keep as release baseline |
| `NativeStudentDecoder` | executable; causal; objective patches implemented; still flat vs RC | larger bounded target change if model improvement is required | stop same-loss sweeps; consider stronger teacher/target redesign only |
| `ImageStateStudentDecoder` | implemented; negative | better image-token target and less anchor collapse | defer, do not rerun unchanged |
| `SCFHead` | accepted precursor | no more headline work | use metrics/helpers only |
| VGGT-Omega | real teacher; oracle-positive ETH3D | domain-conditional teacher rule | defer until RC packaging is stable |
| Qwen semantic controller | diagnostic-negative | broader task definition only | freeze as diagnostic |
| Release docs | mostly complete | final manuscript/deck conversion | continue in `release/` |

## Priority Order

### P0: Freeze RC And Explain It

Status: nearly done.

Artifacts already exist:

```text
release/METHOD_ONEPAGER.md
release/METHOD_FIGURE.md
release/RESULT_TABLE.md
release/PRESENTATION_OUTLINE.md
release/VERIFY_REPORT.md
planning/DREAM3R_IMPLEMENTATION_MODULE_MAP_20260606.md
```

Remaining completion:

```text
write one manuscript-ready methods section
write one manuscript-ready experiments/results section
```

This can be done without touching code.

### P1: Native Student Optimization

Status: executed and release-negative.

This was the only near-term model optimization worth trying before changing a
larger modeling surface.

Why:

- Native student already preserves state causality.
- It is very close to the RC:

```text
native: 0.1451 / 0.1480
RC:     0.1448 / 0.1475
```

- It has proposal dropout, temporal proxy, scale proxy, and fallback
  contamination metrics already in the trainer.

Do not change the architecture first. Change the objective.

Candidate losses:

| Loss | Target | Rationale |
| --- | --- | --- |
| Dropout consistency | output with proposal dropout should match full-teacher output | makes student robust when proposals are missing |
| Temporal proxy penalty | reduce adjacent-frame depth-change error | uses an already reported metric |
| Scale drift proxy penalty | reduce per-frame median-scale drift | targets known weak point |

Executed first patch:

```text
Add optional dropout-consistency loss to train_native_student_decoder.py.
```

Minimal implementation:

1. During training, run the student once with dropout and once with
   `proposal_dropout=0.0`.
2. Stop gradients through the no-dropout output.
3. Add smooth-L1 consistency between dropped and full outputs.
4. Gate by `--dropout-consistency-weight`.
5. Keep default `0.0` so existing behavior is unchanged.

Why this was the first patch:

- It is reversible.
- It does not touch frozen core.
- It directly uses the already implemented dropout mechanism.
- It can be tested locally with synthetic tensors.
- It can be run on GPU1 with the existing native sweep script.

Gate20 result:

```text
OUT=runs/stage6_fusion/native_student_dropout_consistency_gate20_seed7
correct-state: 0.1451 / 0.1480
no-state:      0.1557 / 0.1730
shuffle-state: 0.1525 / 0.2468
fallback:      0
```

Verdict: state-causal, but not better than RC `0.1448 / 0.1475`.

### P2: Temporal/Scale Supervision

Status: executed after P1 was flat and also release-negative.

Current trainer reports:

```text
temporal_delta_abs_rel
scale_drift_proxy
teacher_temporal_delta_abs_rel
teacher_scale_drift_proxy
```

But training loss currently optimizes:

```text
supervised abs-rel
distillation smooth-L1
residual L2
```

Executed patch:

```text
Add optional temporal/scale proxy loss terms to train_native_student_decoder.py.
```

Default weights must remain `0.0`.

Gate20 result:

```text
OUT=runs/stage6_fusion/native_student_temporal_scale_gate20_seed7
correct-state: 0.1451 / 0.1480
no-state:      0.1557 / 0.1730
shuffle-state: 0.1525 / 0.2468
fallback:      0
```

Verdict: still state-causal, but not better than RC.

### P3: Domain-Conditional VGGT Teacher

P1/P2 failed to improve the RC. If model improvement remains required, this is
the next meaningful model surface; do not start it as a broad search.

VGGT evidence:

```text
KITTI oracle gain: +1.18%, VGGT wins 2/50
ETH3D oracle gain: +18.35%, VGGT wins 35/50
```

The only sane VGGT path is domain-conditional:

```text
use VGGT on ETH3D/indoor-like windows
avoid broad KITTI promotion
preserve state/no-state/shuffle controls
```

## First Optimization Experiment

### Patch Scope

Edit:

```text
code/dream3r/scripts/train_native_student_decoder.py
code/dream3r/tests/test_native_student_decoder.py
```

Do not edit:

```text
code/dream3r/model.py
code/dream3r/modules.py
code/dream3r/proposal_set_decoder.py
release RC artifacts
```

### Local Test Gate

```powershell
cd E:\Dream3R
python -B -m pytest --assert=plain code/dream3r/tests/test_native_student_decoder.py -q
```

Expected:

```text
all tests pass
```

### Server Smoke Gate

```bash
ssh BUAA-Server
cd /hdd3/kykt26/code/dream3r
export CUDA_VISIBLE_DEVICES=1

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/hdd3/kykt26/code/dream3r \
conda run --no-capture-output -n dream3r python -B \
  -m pytest --assert=plain code/dream3r/tests/test_native_student_decoder.py -q
```

### Server Training Gate

Short smoke:

```bash
CUDA_VISIBLE_DEVICES=1 \
OUT=runs/stage6_fusion/native_student_dropout_consistency_smoke_seed7 \
EPOCHS=1 \
PROPOSAL_DROPOUT=0.35 \
bash dream3r/scripts/run_native_student_decoder_sweep.sh
```

Full first gate after smoke:

```bash
CUDA_VISIBLE_DEVICES=1 \
OUT=runs/stage6_fusion/native_student_dropout_consistency_gate20_seed7 \
EPOCHS=20 \
PROPOSAL_DROPOUT=0.35 \
bash dream3r/scripts/run_native_student_decoder_sweep.sh
```

The run script must pass the new flag only after the trainer supports it.

## Promotion Rule

Promote only if all conditions hold:

```text
1. correct-state beats 0.1448 / 0.1475
2. correct-state beats no-state
3. correct-state beats shuffle-state
4. fallback_contamination_count == 0
5. temporal/scale proxies do not regress badly
```

If it fails:

```text
do not tune blindly
record negative result
move to P2 temporal/scale loss
```

Current status: P1 and P2 both failed to beat the RC. The same-loss native
student lane is closed unless a new teacher/target design changes the premise.

## Fast Sprint Plan

### Sprint 1: Native Dropout-Consistency Patch

Deliverables:

```text
trainer flag
unit test
server smoke
gate20 correct/no-state/shuffle results
decision note
```

Estimated effort:

```text
1 local coding pass + 1 GPU1 smoke/gate run
```

### Sprint 2: Temporal/Scale Loss Patch

Start only if Sprint 1 is flat.

Deliverables:

```text
trainer flags
unit test
gate20 results
comparison against Sprint 1 and RC
```

### Sprint 3: Presentation/Manuscript Finalization

Can run in parallel with GPU jobs.

Deliverables:

```text
methods section
results section
limitations section
one slide deck
```

## Current Recommendation

Sprint 1 and Sprint 2 are complete and non-promotable.

Reason:

```text
NativeStudentDecoder is closest to RC and already causal.
Simple objective strengthening was a reasonable first test, but the gate stayed
flat at 0.1451 / 0.1480.
```

Next recommendation:

```text
Package the frozen-StatePrior bounded RC for release.
If more model optimization is required, change the bounded target/teacher
surface rather than repeating dropout/temporal/scale loss-weight sweeps.
```
