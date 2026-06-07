# Dream3R Foundation3R Proposal-Free Plan

Date: 2026-06-06
Status: execution plan

## Goal

Build a real proposal-free 3R model path for Dream3R.

Target inference contract:

```text
RGB images / windows + optional Dream state -> pointmap / confidence
```

Forbidden at inference:

```text
Fast3R proposal pointmaps
MASt3R proposal pointmaps
Spann3R proposal pointmaps
VGGT-Omega proposal pointmaps
expert confidences
proposal-bank routing outputs
teacher model calls
```

Allowed during training:

```text
offline dense teacher pointmaps
offline GT pointmaps / masks
offline teacher confidence / validity masks
offline Dream state summaries
```

## Current Evidence

The shallow proposal-free path is closed negative:

```text
sparse GT gate:        state 0.3273 / 0.4029
stripped teacher gate: state 0.3319 / 0.4056
AbsRel capacity gate:  state 0.3326 / 0.4058
teacher target:        0.1360 / 0.1470
official v1.0-rc1:     0.1448 / 0.1475
```

Conclusion:

```text
Do not continue scalar-loss or shallow-head capacity sweeps.
The missing piece is representation and dense geometry pretraining.
```

## Architecture Target

Foundation3R v0 should be a separate non-core module:

```text
code/dream3r/foundation3r_decoder.py
code/dream3r/scripts/build_foundation3r_dense_teacher_cache.py
code/dream3r/scripts/train_foundation3r.py
code/dream3r/tests/test_foundation3r_contract.py
```

Do not edit frozen core files.

### Module Shape

```text
ImageEncoder
  RGB frames -> dense patch tokens

MultiViewMixer
  cross-view attention over frame/patch tokens

StateAdapter
  optional Dream state -> conditioning tokens

GeometryDecoder
  dense tokens -> pointmap / confidence / scale

Foundation3RModel
  forward(images, memory_context=None, conflict_score=None)
```

The `forward` signature must not accept proposal pointmaps, proposal
confidences, expert names, or teacher pointmaps.

## Sprint Plan

### Sprint 0: Contract Lock

Add tests before real training:

```text
test_forward_rejects_proposal_inputs
test_poisoned_proposal_cache_is_ignored
test_teacher_fields_not_read_at_inference
test_state_no_state_shuffle_eval_controls_exist
```

Pass condition:

```text
proposal_inputs_used=false
teacher_used_at_inference=false
```

### Sprint 1: Dense Teacher Cache

Build a dense teacher cache from VGGT-Omega on BUAA-Server GPU1.

Input:

```text
KITTI / ETH3D window manifests
RGB images
optional GT pointmap / mask
Dream state metadata
```

Output:

```text
image tensors or image paths
teacher_pointmap
teacher_confidence
teacher_valid_mask
gt_pointmap / gt_mask when available
memory_context
conflict_score
domain
seq/window id
```

Cache rule:

```text
No proposal bank fields.
No expert confidence fields.
No teacher model object.
No inference-time VGGT-Omega dependency.
```

Initial target:

```text
small cache: 50 KITTI + 50 ETH3D windows
expanded cache: all currently available KITTI/ETH3D image-state windows
```

### Sprint 2: Foundation3R v0

Implement the smallest real model that consumes RGB-derived features, not
cached proposal pointmaps.

Minimum implementation:

```text
patch image encoder
cross-view transformer mixer
state adapter
dense geometry decoder
confidence head
```

This v0 may be weak. It must be architecturally honest:

```text
It is allowed to underperform.
It is not allowed to be proposal-fusion in disguise.
```

### Sprint 3: Training Objective

Train with a combined objective:

```text
GT AbsRel loss when GT exists
teacher dense pointmap distillation
teacher confidence weighted loss
valid-mask loss
temporal consistency proxy
scale consistency proxy
state-causality auxiliary loss
```

State-causality rule:

```text
correct-state must beat no-state and shuffle-state.
If it does not, do not claim Dream state helps.
```

### Sprint 4: Gate Ladder

Run gates in this order:

```text
G0 local contract tests
G1 server import + cache schema smoke
G2 1-epoch GPU1 training smoke
G3 20-epoch tiny gate on 50+50 windows
G4 all-current-window gate
G5 state / no-state / shuffle-state control gate
G6 leak audit: poison proposal fields and verify no metric change
```

Initial promotion thresholds:

```text
proposal_inputs_used=false
fallback_contamination_count=0
state < no-state on KITTI and ETH3D
state < shuffle-state on KITTI and ETH3D
state improves over shallow proposal-free by at least 20 percent
```

Stronger target:

```text
approach or beat 0.20 / 0.25 first
then approach v1.0-rc1 0.1448 / 0.1475
then compare against v1.1 domain-conditional teacher policy
```

The first Foundation3R gate should not be required to beat the official
release. That would encourage proposal leakage. The first real win is
proposal-free causality plus a large improvement over `0.33 / 0.40`.

## Stop Conditions

Stop or redesign if any condition holds:

```text
model reads proposal fields
state fails no-state/shuffle controls twice
dense teacher cache cannot be built without proposal leakage
20-epoch gate remains around 0.33 / 0.40
training loss falls but AbsRel does not move
```

## Relationship To Release

Keep release and foundation work separate:

```text
release line:    v1.0-rc1 and possible v1.1 packaging
foundation line: proposal-free Foundation3R
```

The release line is allowed to remain proposal-teacher/domain-conditional. The
foundation line is not.

## Immediate Next Task

Implement Sprint 0 and Sprint 1 only:

```text
1. Add Foundation3R cache schema and contract tests.
2. Add dense teacher cache builder reusing the existing VGGT-Omega server path.
3. Run mock/local tests.
4. Sync to BUAA-Server.
5. Build a small 50+50 dense teacher cache on GPU1.
6. Validate cache JSON/schema and leak audit.
```

Only after this succeeds should Foundation3R v0 training code be written.
