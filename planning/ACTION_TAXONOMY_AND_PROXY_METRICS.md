# Action Taxonomy And Proxy Metrics

Last updated: 2026-05-04 (cycle 008.5 sync: A5 split (Composer routing facet vs Critic repair facet) annotated in Branch Pressure table; First Research Inference marked superseded)

Status: first compact taxonomy (cycle 006) + cycle 008.5 sync; not a thesis decision.

## Purpose

This file turns the broad mechanism intake into a small set of measurable 3R spatial-intelligence actions.

It is the bridge between:

```text
failure-mode graph -> mechanism intake -> branch comparison -> mechanism specs
```

The goal is not to claim performance. The goal is to define what Dream can measure before reproduction or model training.

The taxonomy also supports paper writing. A broad mechanism pool is useful because it lets the paper argue from field structure:

```text
modern 3R is not missing one module;
it is missing a principled control vocabulary over memory, verification, dynamics, priors, action, and evidence.
```

Therefore, action selection should consider both evidence feasibility and writing value. A mechanism can be retained as a paper-taxonomy asset even if it is not selected for the first prototype.

## Design Rule

A valid Dream action must satisfy all five:

1. It addresses at least one F1-F6 failure mode.
2. It can be triggered by a geometry or system evidence signal.
3. It maps to multiple candidate branches or comparator groups.
4. It has at least one proxy metric that can be estimated without heavy reproduction.
5. It can appear in a teacher-facing explanation without pretending measured SOTA.

For paper-readiness, also record whether the action helps one of these writing functions:

- organizes related work
- sharpens novelty against comparators
- supports a figure or taxonomy
- creates a measurable benchmark axis
- strengthens the bridge from system demo to research claim

## Core Action Set V1

The earlier draft had many small actions. For research comparison, collapse them into eight core actions.

| ID | Core action | Contains draft actions | Main failure modes | Evidence trigger | Primary proxy metrics | Comparator pressure | Branches |
|---|---|---|---|---|---|---|---|
| A1 | State Update Control | weak update; strong update; Kalman-style update; reset state | F1, F3 | pose novelty, confidence drop, reprojection residual, latent drift, uncertainty | update selectivity, drift-risk proxy, conflict reduction, action entropy | CUT3R, STream3R, LONG3R, PAS3R, FILT3R | Executive Memory, Continual |
| A2 | Spatial Memory Governance | write pointer; read pointer; merge pointer; ignore memory | F1, F6 | memory overlap, loop candidate, novelty, map conflict, retrieval value | memory growth, later retrieval usefulness, duplicate rate, anchor retention | Spann3R, Point3R, LoGeR, Mem3R | Executive Memory, Composer |
| A3 | Context / Anchor Budgeting | protect anchor; evict cache; request global context; sparse retrieval | F1, F3, F6 | anchor importance, loop candidate, cache pressure, conflict region, long sequence length | anchor retention, cache budget, compute-quality tradeoff, route regret | LongStream, OVGGT, LoGeR, Mem3R, sparse/linear attention work | Executive Memory, Composer |
| A4 | Geometry Verification | verify geometry; check consistency; check prior conflict | F3, F5, F6 | low overlap, confidence conflict, triplet inconsistency, prior/RGB mismatch | conflict detection, false alarm rate, prior conflict detection, demo clarity | Test3R, TTT3R, MASt3R-SfM, G-CUT3R | Geometry Critic, Composer, Cross-Modal |
| A5 | Repair / Reroute Decision | revise hypothesis; rerun local region; reroute model; allocate compute | F3, F6 | critic failure, route uncertainty, model capability mismatch, hard-case label | revision success proxy, route regret, compute-quality tradeoff | Test3R, TTT3R, CTRL, MASt3R-SfM, SLAM3R | Geometry Critic (repair facet, cycle 008.5), Composer (routing facet, cycle 008.5) |
| A6 | Dynamic/Object State Separation | split dynamic/static; reject dynamic update; preserve object identity | F2, F3 | dynamic ratio, optical flow conflict, motion field, object track, static-map conflict | dynamic pollution, static-map stability, object identity consistency | MonST3R, POMATO, D^2USt3R, Easi3R, RayMap3R | Dynamic Object Permanence, Executive Memory |
| A7 | Prior / Modality Arbitration | add sensor prior; route to guided mode; request sensing mode; reject conflicting prior | F5, F2, F3 | blur, low light, high speed, texturelessness, guided-prior conflict | robustness label, prior conflict detection, sensing-mode gain, hardware burden | EAG3R, Event-3DGS, G-CUT3R, guided 3R | Cross-Modal, Geometry Critic, Active |
| A8 | Evidence Acquisition / Adaptation Budget | request new view; revisit region; open adapter budget; constrained self-update | F4, F1, F3, F5 | high uncertainty, blind spot, persistent conflict, domain shift | uncertainty reduction, view gain, forgetting risk, adaptation budget | NBV, active perception, TTT3R, SEAL, CTRL | Active Perception, Continual, Critic |

## Why This Compression Matters

The eight actions separate Dream from a generic model zoo:

- A1-A3 are memory and context governance.
- A4-A5 are System-2 verification and action.
- A6 is dynamic object permanence.
- A7 is sensor / prior arbitration.
- A8 is active evidence acquisition and constrained adaptation.

This structure lets different branches share a common action language while retaining distinct research claims.

### Cycle 008.5 A5 Split

Cycle 008.5 split A5 into two functional facets owned by different finalist specs:

- **A5 repair facet** — owned by Geometry Critic (`specs/SPEC-20260503-001-geometry-critic.md`). Sub-actions: `rerun_local_region`, `open_anchor_budget` (handoff to Memory), `request_prior` (handoff to future Cross-Modal). Trigger: per-window critic conflict_score above threshold.
- **A5 routing facet** — owned by 3R Composer (`specs/SPEC-20260504-001-3r-composer.md`). Sub-action: `reroute_model`. Trigger: across-model regime card + capability_match join; Critic A5 reroute_model consumes Composer's `route_recommendation` per `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` rule CR-1.

The split is intentional: repair is verification-coupled (per-window evidence), routing is regime-coupled (across-model regime fit). Owning both inside Critic alone would either fragment routing across specs or duplicate Composer's regime card.

## Evidence Signal Vector V1

For a frame, chunk, model output, or sample regime, Dream can reason over:

```text
e = [
  pose_novelty,
  view_overlap,
  reprojection_residual,
  pointmap_conflict,
  confidence_drop,
  latent_drift_proxy,
  dynamic_ratio,
  optical_flow_conflict,
  object_track_stability,
  loop_candidate_score,
  anchor_importance,
  cache_pressure,
  external_memory_overlap,
  prior_rgb_conflict,
  blur_or_low_light_score,
  uncertainty_area,
  model_capability_match
]
```

Claim status:

```text
The evidence vector is inferred.
Individual signals are common in 3R / vision systems, but Dream has not measured their combined predictive value.
```

## Proxy Metric Protocols

### P1: Conflict Detection

Purpose:

```text
Check whether A4 can identify hard geometric inconsistency before claiming System-2 3R.
```

Inputs without reproduction:

- public paper examples
- existing KYKT job metadata if available
- manually labeled sample cards
- synthetic scenario descriptions

Measurement:

```text
conflict_detection = detected_conflicts / labeled_conflict_cases
false_alarm_rate = false_conflicts / labeled_non_conflict_cases
```

Minimum acceptable output:

- a table of sample cases
- predicted conflict type
- supporting evidence signal
- recommended action A5 / A3 / A7

### P2: Anchor Retention

Purpose:

```text
Check whether A3 protects geometrically important frames, gauges, or cache tokens in long sequences.
```

Inputs without reproduction:

- sequence timeline
- keyframe / loop-candidate labels
- memory budget assumption
- comparator policy assumptions

Measurement:

```text
anchor_retention = protected_important_anchors / total_important_anchors
cache_pressure = retained_tokens / token_budget
```

Compare:

- fixed sliding window
- uniform keyframe sampling
- confidence-only retention
- Dream evidence-triggered retention

### P3: Memory Growth And Usefulness

Purpose:

```text
Check whether A2 writes useful memory rather than unbounded logs.
```

Inputs without reproduction:

- frame/chunk list
- novelty labels
- loop/revisit labels
- dynamic/static labels when available

Measurement:

```text
memory_growth = number_of_memory_entries
write_rate = writes / frames_or_chunks
reuse_rate = useful_retrievals / memory_entries
duplicate_rate = duplicate_entries / memory_entries
```

Minimum claim:

```text
Dream policy can be compared as a controller design.
No performance gain is claimed.
```

### P4: Dynamic Pollution

Purpose:

```text
Check whether A6 prevents moving objects from corrupting static memory.
```

Inputs without reproduction:

- dynamic/static case labels
- object-motion labels
- public dynamic 3R examples
- manually annotated frame regions

Measurement:

```text
dynamic_pollution = dynamic_regions_allowed_to_static_memory / dynamic_regions
static_preservation = static_regions_kept / static_regions
identity_consistency = linked_object_instances / visible_object_instances
```

Relevant branches:

- Dynamic Object Permanence
- Executive Memory
- Cross-Modal if event or prior signals help separate motion

### P5: Route Regret

Purpose:

```text
Check whether A5 / Composer chooses a plausible model or action for each input regime.
```

Inputs without reproduction:

- model capability cards
- sample regime cards
- paper-reported strengths / limitations
- KYKT model catalog when available

Measurement:

```text
route_regret = chosen_route_score_gap_to_best_known_route
capability_match = matched_capabilities / required_capabilities
```

Compare:

- single default model
- user-chosen model
- rule-based Composer L1
- critic-triggered Composer L2 action

### P6: Action Entropy

Purpose:

```text
Detect whether a proposed controller is actually using meaningful actions or always choosing one default.
```

Measurement:

```text
action_entropy = -sum(p(action) * log(p(action)))
```

Interpretation:

- Too low: controller may be a renamed single policy.
- Too high: controller may be random or underspecified.
- Useful range: actions vary by failure mode and evidence signal.

### P7: Uncertainty Reduction / View Gain

Purpose:

```text
Check whether A8 active perception can be studied before robotics or heavy simulation.
```

Inputs without reproduction:

- mock uncertainty map
- visible / hidden region labels
- candidate next-view descriptions

Measurement:

```text
view_gain = uncertainty_before - expected_uncertainty_after
blind_spot_reduction = newly_visible_uncertain_area / total_uncertain_area
```

Minimum output:

- design-only active perception case cards
- no claim of robotics readiness

### P8: Adaptation Benefit Versus Forgetting Risk

Purpose:

```text
Check whether A8 open_adapter_update_budget is justified or too risky.
```

Inputs without reproduction:

- persistent conflict labels
- domain shift labels
- hypothetical update budget

Measurement:

```text
adaptation_trigger_precision = justified_update_triggers / all_update_triggers
forgetting_risk = update_scope * affected_memory_importance
```

Minimum claim:

```text
This is an adaptation-policy design signal, not proof of online learning.
```

## Branch Pressure After Taxonomy

| Branch | Strong owned actions | Required support actions | Best first proxy | Main risk after taxonomy |
|---|---|---|---|---|
| Executive Memory / State Governance | A1, A2, A3 | A4, A6 | P2 anchor retention + P3 memory growth/usefulness | too broad unless reduced to state/memory/cache decisions |
| Geometry Critic / System-2 3R | A4, A5 (repair facet) | A3, A7 | P1 conflict detection + P5 route regret | diagnostic-only unless A5 changes route or output |
| Dynamic Object Permanence / 4D Memory | A6 | A2, A4, A7 | P4 dynamic pollution + identity consistency | can become motion estimation or graphics demo only |
| Cross-Modal / Event-Augmented 3R | A7 | A4, A6, A8 | prior conflict detection + robustness labels | hardware/data burden; event 3R is already emerging |
| 3R Composer / Unified Model Ecology | A5 (routing facet) | A3, A4, A7 | P5 route regret + capability match | system wrapper unless L2 mechanism distillation is explicit |
| Active Spatial Perception / RL-3R | A8 | A4, A7 | P7 view gain | too costly if it jumps to robotics/simulation too early |

## First Research Inference

The taxonomy suggests a near-term finalist pool should probably combine:

```text
Geometry Critic / System-2 3R
+ Executive Memory / State Governance
+ 3R Composer as evidence infrastructure
```

Dynamic Object Permanence should remain a close third/fourth candidate because it gives a strong F2-specific claim and visual demo path, but it needs object-identity proxy evidence before mechanism deepening.

This is an inference, not a decision. User approval is still required before drafting any finalist mechanism spec.

## First Research Inference (Superseded; Cycle 008.5)

The cycle 006 inference above is preserved for honesty (Discipline rule 5) but no longer reflects the current state. Superseding events:

- **DEC-20260503-002 (cycle 008)**: User approved option B (Critic + Memory + Permanence as finalists; Composer as supporting layer). The inference's "Composer as evidence infrastructure" framing was honored at that gate.
- **DEC-20260504-001 (cycle 008.5)**: User upgraded Composer to fourth finalist. The inference's framing of Composer as "evidence infrastructure" rather than finalist is therefore superseded.
- **DEC-20260504-002 (cycle 008.5)**: User locked the no-all-in posture. The inference's "near-term finalist pool" framing remains accurate at the set level but must not be read as preferring any single finalist.

Current state (after cycle 008.5):

```text
Four finalists with mechanism specs drafted at L1:
  Geometry Critic     (A4 + A5 repair facet; P1 + P5)
  Executive Memory    (A1 + A2 + A3; P2 + P3)
  Dynamic Object Permanence (A6; P4 + identity_consistency)
  3R Composer         (A5 routing facet; P5 + capability_match)

Cross-Modal (A7) and Active Perception (A8) remain alive at lower priority;
no specs drafted; no finalist status.

Cycle 009 fills L2 case cards on parallel tracks. Critic first per cycle 008
D1 is execution order, NOT preference order, per DEC-20260504-002.
```

## Immediate Next Research Task

Prepare the branch shortlist decision surface:

1. one-page summary per candidate branch
2. owned actions
3. weakest comparator pressure
4. first proxy test
5. what teacher demo would show
6. what would make the branch fail fast

## Immediate Next Research Task (Superseded; Cycle 008.5)

The cycle 006 task above produced `planning/BRANCH_SHORTLIST_DECISION_SURFACE.md`, which the user resolved via DEC-20260503-002 + DEC-20260504-001. The current next task is:

```text
Authorize cycle 009 to start filling L2 case cards on four parallel tracks
under the cross-spec signal contract v1 (`paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md`).
First card per cycle 008 D1: CASE-20260504-CRITIC-01.
```
