# Dream3R V11 VLM semantic-controller research plan

Date: 2026-06-03
Status: active research plan, implementation gated
Decision: `decisions/DEC-20260603-027-vlm-semantic-controller-plan.md`
Handoff: `handoff/ARCHITECTURE_V11_VLM_SEMANTIC_CONTROLLER_AGENT_PROMPT.md`

Post-gate status, 2026-06-03:

- DEC-20260603-028 implemented the strict semantic label-cache gate.
- DEC-20260603-029 implemented KITTI/ETH3D window-manifest generation and a
  Router/Critic dry-run evaluator with real/shuffle/disabled controls.
- DEC-20260603-030 staged Qwen3-VL-2B-Instruct weights on BUAA-Server, created
  an isolated smoke venv, and ran GPU1 5-window KITTI labels with strict schema
  pass rate 1.0.
- DEC-20260603-031 ran the first oracle-aligned 50-window Qwen gate. Strict
  schema passed 50/50, but the controller dry-run was negative:
  `vlm_real = vlm_shuffle = vlm_disabled = 0.2365` versus oracle `0.1489`.
  The current Qwen prompt/features/policy are not promotable.
- DEC-20260603-032 repaired the feature/policy surface by deriving risk floors
  from `visible_failure_causes` and routing low-texture/reflection/repeated/
  occlusion risks before road fallback. Fresh v2 is weak-positive but still not
  promotable: real `0.1750`, shuffle `0.1759`, disabled `0.2365`, oracle
  `0.1489`.
- DEC-20260603-033 added a held-out calibrated controller gate. Leave-one-
  group-out calibration over the same 50 Qwen v2 windows gives real `0.1813`,
  shuffle `0.1776`, disabled `0.2365`, oracle `0.1489`. Real does not beat
  shuffle, so the current Qwen cache is not promotable.
- Further Qwen work needs broader windows, a pre-registered real > shuffle >
  disabled threshold, and Router/Critic state-causality controls. Do not keep
  tuning deterministic rules on the same 50-window set.

## Executive summary

Dream3R is not yet usable as a native reconstruction model. The locked usable
bounded baseline remains:

```text
proposal teachers + Dream state -> frozen StatePrior -> bounded residual
KITTI/ETH3D: 0.1448/0.1475
```

The recent native directions are clear:

- proposal-only native student is executable and state-causal, but flat;
- image-state U1 is negative because correct-state loses to no-state;
- VGGT-Omega teacher admission is blocked on an approved checkpoint.

V11 therefore adds a different research lane: use Qwen3-VL-2B-Instruct, and
compatible compact open VLMs, as an offline semantic controller signal. The VLM
does not replace MASt3R, Fast3R, Spann3R, StatePrior, VGGT-Omega, or any 3D
geometry backend. It labels visual regimes, failure risks, dynamic/static
objects, and compute-trigger hints that can improve Router, Critic, Dream state
supervision, and teacher-admission scheduling.

The first executable gate is not "Qwen makes depth." It is:

```text
existing window caches + sampled frames
  -> strict JSON semantic risk labels
  -> validated vlm_regime_labels.json
  -> VLM-augmented router / critic trigger controls
  -> leave-one-sequence and cross-domain metrics
```

Promotion requires a quantitative gain over current router/control baselines,
with shuffled and disabled VLM controls worse than the real VLM labels.

## Why this lane exists

The current failure pattern is not only geometry quality. It is controller
quality:

- the Router has coarse regime labels and robust numeric stats;
- the Critic can react to geometry conflicts but lacks semantic prior knowledge;
- the Dream state contains useful expert-prior signal, but joint decoders can
override or collapse it;
- expensive teacher admission needs a better trigger so heavy models are used
only on windows likely to benefit.

Compact VLMs are useful exactly at this boundary. They can read image evidence
and produce semantic risk labels such as "low texture tunnel", "reflective
glass", "dynamic vehicles", "large baseline", "repeated structure", or
"occluded foreground". These are not pointmaps, but they are meaningful
conditioning signals for 3R system control.

## Official-source capability boundary

Qwen3-VL official sources describe the family as upgraded for visual perception,
reasoning, spatial perception, long-context/video understanding, OCR, and agent
interaction. The official repository notes the 2025-10-21 release of the 2B
Instruct and Thinking variants, and the repository is Apache-2.0. The Hugging
Face model card for `Qwen/Qwen3-VL-2B-Instruct` provides Transformer usage and
describes capabilities including spatial perception, video understanding, OCR,
and multimodal reasoning.

Sources checked:

- `https://github.com/QwenLM/Qwen3-VL`
- `https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct`

Dream3R interpretation:

| Capability | Use in Dream3R | Not allowed as |
| --- | --- | --- |
| Visual recognition | detect scene type, object classes, texture/reflectance risk | expert pointmap |
| Spatial relation reasoning | flag occlusion, viewpoint, large-baseline risk | metric camera solver |
| Video/long-context understanding | label temporal risk across 4-frame windows | streaming 3R memory |
| OCR/document ability | mostly irrelevant for KITTI/ETH3D geometry | evidence of 3R performance |
| Agent/tool following | strict JSON output and schema compliance | autonomous training loop |

## Model selection

### First choice

`Qwen/Qwen3-VL-2B-Instruct`

Why:

- compact enough to serve as an offline labeler or small local/server model;
- official model card supports image-text-to-text usage;
- strong enough for scene and risk classification;
- Apache-2.0 code repository is favorable for research tooling;
- better fit than older Qwen2.5-VL-3B because the user explicitly selected
  Qwen3-VL-2B and it has a newer official capability surface.

### Backup candidates

Backups should be used only if Qwen3-VL-2B is blocked by dependency, license,
memory, or download/access constraints.

| Candidate | Dream3R role | Risk |
| --- | --- | --- |
| InternVL3.5 1B/2B family | alternative offline labeler | verify current weights and license before use |
| SmolVLM2 500M/2.2B | cheaper labeler for coarse risks | may be weaker on spatial reasoning |
| LFM2.5-VL-450M | very compact triage model | schema reliability must be measured |
| Moondream 2B/0.5B | caption/VQA/object hints | weaker structured multi-frame reasoning |
| Florence-2 base/base-ft | specialist detection/OCR/grounding helper | not conversational controller |
| MiniCPM-V | stronger offline teacher option | larger and may be overkill for first gate |

The plan does not require adopting all candidates. Qwen3-VL-2B is the default
lane; backups are for blocked execution only.

## Architecture role

V11 inserts a support signal beside existing Dream3R control paths:

```text
images / 4-frame window
  -> Qwen3-VL-2B offline semantic labeler
  -> vlm_semantic_features
  -> Router / Critic / compute gate / Dream state auxiliary loss
  -> existing proposal teachers and frozen baseline remain geometry owners
```

The VLM signal is stored in cache and consumed as structured features. It is
never treated as geometry ground truth.

### Integration points

1. Router enhancement

Current local surfaces:

- `code/dream3r/modules.py`: `ComposerRouter`
- `code/dream3r/scripts/train_router_only.py`
- `code/dream3r/scripts/train_router_joint_domain.py`
- `code/dream3r/scripts/eval_router_loo.py`
- `code/dream3r/scripts/eval_cross_domain_router.py`

V11 adds VLM feature columns to the same router feature surface:

```text
old: regime_probs + robust_stats + optional critic/domain features
new: old + vlm_scene_probs + vlm_risk_vector + vlm_uncertainty_flags
```

2. Critic trigger enhancement

The Critic should use VLM labels as a prior over likely failure causes, not as a
replacement for geometry consistency. Example:

```text
if low_texture_risk high and pointmap_confidence low:
  lower verify_geometry threshold

if dynamic_actor_risk high and temporal conflict high:
  prefer dynamic/static split or reject_dynamic_update

if reflection_risk high and proposal disagreement high:
  request expensive teacher or mark unreliable
```

3. State auxiliary supervision

The Dream state can receive auxiliary labels:

- scene type
- dynamic risk
- low-texture risk
- reflective risk
- occlusion risk
- large-baseline risk
- scale-drift risk

This should regularize state without letting semantic labels dominate geometry
loss. The first gate should test labels as frozen cached features before any
joint state retraining.

4. Teacher-admission compute gate

Use VLM labels to decide when to spend heavy teacher budget:

```text
suggest_expensive_teacher = true
```

This can later gate VGGT-Omega, CUT3R, or MonST3R admission runs. The gate is
accepted only if it improves compute-quality tradeoff and does not hide hard
windows from evaluation.

## Strict label schema

The first label cache should be a deterministic JSON file with one record per
window.

```json
{
  "schema_version": "dream3r_vlm_semantic_v1",
  "model_id": "Qwen/Qwen3-VL-2B-Instruct",
  "window_id": "dataset/sequence/start_frame",
  "dataset": "kitti|eth3d",
  "frames": ["..."],
  "scene_type": "road|indoor|forest|tunnel|building|unknown",
  "risk_dynamic": 0.0,
  "risk_low_texture": 0.0,
  "risk_reflection": 0.0,
  "risk_occlusion": 0.0,
  "risk_large_baseline": 0.0,
  "risk_scale_drift": 0.0,
  "risk_repeated_structure": 0.0,
  "important_objects": ["car", "pedestrian"],
  "visible_failure_causes": ["low_texture", "occlusion"],
  "suggest_verify_geometry": true,
  "suggest_expensive_teacher": false,
  "confidence": 0.0,
  "failure_flags": []
}
```

Validation rules:

- all risk values must be finite floats in `[0, 1]`;
- `scene_type` must be from an allowlist;
- unknown or invalid output must become `failure_flags`, not silent defaults;
- no free-form prose is consumed by training;
- every record keeps `model_id`, prompt hash, and input image list.

## Prompt template for label generation

The labeler prompt should be short, stable, and hostile to prose:

```text
You are labeling a 4-frame visual-geometry reconstruction window for Dream3R.
Return only valid JSON matching the requested schema.

Task:
Classify scene type and visual risk factors that may affect 3D reconstruction.
Use the images only. Do not estimate metric depth or camera pose. Do not invent
hidden objects. If uncertain, lower confidence and use "unknown".

Schema:
{
  "scene_type": "road|indoor|forest|tunnel|building|unknown",
  "risk_dynamic": 0.0,
  "risk_low_texture": 0.0,
  "risk_reflection": 0.0,
  "risk_occlusion": 0.0,
  "risk_large_baseline": 0.0,
  "risk_scale_drift": 0.0,
  "risk_repeated_structure": 0.0,
  "important_objects": [],
  "visible_failure_causes": [],
  "suggest_verify_geometry": true,
  "suggest_expensive_teacher": false,
  "confidence": 0.0
}
```

## Phase plan

### Phase 0: Documentation and boundary lock

Status: this document.

Outputs:

- V11 plan;
- DEC and cycle log;
- new-agent prompt;
- project document sync.

Hard boundary:

- no checkpoint download;
- no model training;
- no server mutation;
- no frozen-core edit.

### Phase 1: Offline label cache smoke

Goal: label a tiny fixed sample from existing KITTI and ETH3D windows.

Proposed files:

```text
code/dream3r/scripts/build_vlm_semantic_labels.py
code/dream3r/tests/test_vlm_semantic_labels.py
```

Proposed outputs:

```text
runs/vlm_semantic_controller/qwen3vl2b_smoke/kitti_labels.json
runs/vlm_semantic_controller/qwen3vl2b_smoke/eth3d_labels.json
runs/vlm_semantic_controller/qwen3vl2b_smoke/schema_report.json
```

Acceptance:

- strict schema pass rate >= 95 percent on the smoke set;
- invalid records are explicit failures;
- runtime and VRAM recorded if run on BUAA-Server;
- no label is used as ground-truth geometry.

### Phase 2: Full cache over existing proposal windows

Goal: label all windows already used by SCF/native gates.

Targets:

```text
KITTI: 246 windows
ETH3D: 50 windows
```

Acceptance:

- every labeled window maps to an existing proposal/cache window;
- failure rate and unknown rate are reported;
- cache includes prompt hash, model id, and input frame paths;
- labels are deterministic enough under fixed generation settings or are
  averaged through a documented repeat-label protocol.

### Phase 3: Router augmentation gate

Goal: test whether VLM semantic features improve route decisions.

Variants:

| Variant | Meaning |
| --- | --- |
| `router_current` | current best router features, no VLM |
| `router_vlm` | current features plus real VLM labels |
| `router_vlm_shuffle` | VLM labels shuffled across windows |
| `router_vlm_disabled` | VLM feature columns zeroed |
| `router_vlm_textonly_ablate` | optional, semantic class only without risk scores |

Metrics:

- route accuracy against oracle/best expert labels;
- route regret;
- KITTI leave-one-sequence;
- ETH3D cross-domain;
- final downstream SCF/frozen-prior quality if routed outputs are consumed;
- calibration and confusion by failure cause.

Promotion:

```text
router_vlm must beat router_current on held-out or cross-domain metrics,
router_vlm_shuffle must be worse than router_vlm,
and no geometry metric may regress beyond a documented tolerance.
```

### Phase 4: Critic trigger gate

Goal: use VLM risk labels to decide when geometry verification or expensive
teacher admission should fire.

Variants:

- current Critic trigger;
- Critic plus VLM risks;
- VLM-only trigger;
- shuffled VLM trigger.

Metrics:

- hard-window detection precision/recall;
- avoided false positives;
- compute-quality tradeoff;
- downstream improvement on windows with high predicted risk;
- trigger stability across KITTI and ETH3D.

Promotion:

VLM can only reduce or increase trigger thresholds through geometry-confirmed
signals. A VLM-only trigger is a diagnostic baseline, not the promoted model.

### Phase 5: State auxiliary supervision

Goal: teach Dream state to predict semantic failure risk without letting it
override geometry.

Candidate losses:

```text
L_state_vlm = BCE(risk_vector_pred, risk_vector_cache)
L_total = L_geometry + lambda_state * L_state_vlm
```

First safe setting:

```text
lambda_state in {0.01, 0.03, 0.1}
frozen geometry baseline remains unchanged for control
```

Promotion:

- correct-state beats no-state and shuffle-state;
- correct-state matches or beats 0.1448/0.1475;
- VLM-shuffle loses semantic benefit;
- U1-style collapse does not repeat.

### Phase 6: Teacher-admission scheduler

Goal: decide when to run heavy teachers such as VGGT-Omega after checkpoints are
available.

Policy sketch:

```text
teacher_score =
  a * proposal_disagreement
  + b * critic_conflict
  + c * vlm_risk_large_baseline
  + d * vlm_risk_low_texture
  + e * vlm_risk_reflection
```

Acceptance:

- same quality at lower compute, or better quality at fixed compute;
- no hidden fallback contamination;
- no skipped hard-case reporting.

## Data and execution policy

Local Windows:

- write scripts and docs;
- inspect JSON/caches;
- run schema and unit tests.

BUAA-Server GPU1:

```text
ssh BUAA-Server
cd /hdd3/kykt26/code/dream3r
CUDA_VISIBLE_DEVICES=1 ...
```

Use the server for VLM inference or model-adjacent code only. Do not mutate
environments or download large checkpoints without an explicit active approval
when that approval is required by project policy.

## Non-goals

V11 does not:

- replace pointmap/depth/camera geometry with VLM prose;
- promote Qwen labels as ground truth;
- rerun U1 unchanged;
- reopen broad architecture search;
- modify frozen core files;
- download checkpoints as part of this planning pass;
- claim Dream3R is usable beyond the locked bounded baseline.

## Risk register

| Risk | Failure mode | Mitigation |
| --- | --- | --- |
| VLM hallucination | labels do not match image evidence | strict schema, unknown class, manual audit sample |
| Semantic leakage | labels correlate with dataset identity instead of geometry risk | KITTI LOO, ETH3D cross-domain, domain ablation |
| Router overfit | train metrics improve but held-out route regret worsens | holdout-first promotion rule |
| Prompt instability | repeated VLM calls differ | fixed generation settings, prompt hash, repeat-label audit |
| Geometry displacement | team treats VLM as depth/camera source | explicit non-goal and DEC boundary |
| Compute bloat | VLM online call slows pipeline | offline cache first; online only for uncertain windows later |
| Label shortcut | VLM labels duplicate scene name only | shuffle, zero, and risk-only ablations |

## First implementation gate

Recommended next executable task:

```text
Implement build_vlm_semantic_labels.py as an offline cache builder with a mock
backend and a Qwen backend interface, then run schema tests locally. If Qwen
weights are available or approved, run a 10-window smoke on BUAA-Server GPU1.
```

Minimum artifact set:

```text
code/dream3r/scripts/build_vlm_semantic_labels.py
code/dream3r/tests/test_vlm_semantic_labels.py
runs/vlm_semantic_controller/qwen3vl2b_smoke/schema_report.json
```

Minimum pass:

- mock backend schema tests pass locally;
- no frozen-core diff;
- Qwen backend is gated behind explicit model path/model id;
- failure records are explicit;
- no training starts before label-cache quality is known.

Gate status, 2026-06-03:

```text
code/dream3r/scripts/build_vlm_semantic_labels.py
code/dream3r/tests/test_vlm_semantic_labels.py
runs/vlm_semantic_controller/qwen3vl2b_smoke/schema_report.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win/schema_report_50win_t320.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win/controller_dryrun_50win_t320.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win_v2/schema_report_50win_t320_v2.json
runs/vlm_semantic_controller/qwen3vl2b_real_50win_v2/controller_dryrun_50win_t320_v2.json
```

Local mock gate passed, then DEC-20260603-030 staged Qwen3-VL-2B, and
DEC-20260603-031 ran the first 50-window real gate. The real cache includes
`features`, `shuffled_features`, and `disabled_features`, and strict schema
passes 50/50. The controller dry-run is negative:
`vlm_real = vlm_shuffle = vlm_disabled = 0.2365` versus oracle `0.1489`.
DEC-20260603-032 partially repairs this: fresh v2 real `0.1750`, shuffle
`0.1759`, disabled `0.2365`, oracle `0.1489`. The signal is measurable but too
weak for Router/Critic promotion.

## Success criteria for the V11 research lane

V11 becomes useful only if one of these gates passes:

1. Router gate: VLM labels improve held-out route regret and cross-domain
   routing versus current robust stats, with shuffled labels worse.
2. Critic gate: VLM risks improve hard-window trigger precision/recall or
   compute-quality tradeoff, with geometry confirmation still required.
3. State gate: VLM auxiliary supervision helps correct-state beat no-state,
   shuffle-state, and the locked 0.1448/0.1475 baseline.
4. Teacher scheduler gate: VLM risks help spend VGGT-Omega/CUT3R/MonST3R budget
   on windows that actually improve downstream quality.

If none pass, retire V11 to demo/report support only and return to native
geometry objective redesign or teacher-bank admission.

## Paper and demo value

If successful, V11 gives Dream3R a defensible story:

```text
Dream3R uses visual-language semantic risk only as a controller prior. Geometry
is still produced and validated by 3R backbones and state-conditioned proposal
fusion. The novelty is not "VLM reconstructs 3D"; it is "semantic risk improves
when and how a 3R system verifies, routes, and spends teacher compute."
```

Demo surface:

- show input 4-frame window;
- show VLM semantic risk card;
- show Router/Critic decision change;
- show whether geometry verification or heavy teacher admission was triggered;
- show final metric delta only after quantitative gate passes.
