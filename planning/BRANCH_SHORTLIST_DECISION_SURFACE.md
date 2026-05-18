# Branch Shortlist Decision Surface

Last updated: 2026-05-02

Status: decision surface draft; no branch selected.

## Purpose

Prepare the user decision before any single branch receives a full mechanism spec.

This file compares branches using the current Dream structure:

```text
F1-F6 failure modes
-> A1-A8 core actions
-> P1-P8 proxy metrics
-> comparator pressure
-> paper-writing value
-> teacher demo form
-> fail-fast condition
```

No branch is finalized here. No branch is discarded here.

## Shortlist Reading Rule

Choose 2-3 branches for mechanism-spec drafting only after reading:

- `planning/BRANCH_COMPARISON_MATRIX.md`
- `planning/ARCHITECTURE_MECHANISM_INTAKE.md`
- `planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md`
- this file

The selected branches should optimize for:

- strongest failure-mode claim
- clearest comparator gap
- cheapest credible proxy evidence
- strongest paper-writing value
- plausible teacher demo
- controlled engineering cost

## Candidate 1: Geometry Critic / System-2 3R

### Core Claim

Modern 3R models can be confidently wrong under hard geometric ambiguity. A 3R system needs a verification-and-action loop that detects inconsistency and triggers repair, rerouting, or extra context.

### Failure Modes

- F3 Hard-Case Geometric Ambiguity
- F6 Fragmented Model Ecology
- F1 Long-Context Drift / Forgetting when critic gates memory or context retrieval

### Owned Actions

- A4 Geometry Verification
- A5 Repair / Reroute Decision

Support actions:

- A3 Context / Anchor Budgeting
- A7 Prior / Modality Arbitration

### Comparator Pressure

- Test3R
- TTT3R
- MASt3R-SfM
- SLAM3R
- G-CUT3R
- CTRL-style critic-revision

Weakest pressure point:

```text
If Dream only detects errors but does not trigger a concrete action, this branch becomes diagnostics rather than a research mechanism.
```

### First Proxy Test

Use P1 + P5:

- P1 conflict detection
- P5 route regret

Minimum evidence:

- sample cards with conflict labels
- predicted conflict type
- evidence signal
- recommended action: retry, reroute, request context, or check prior

### Teacher Demo

Show a difficult sample where a standard 3R route looks plausible but violates geometry. Dream flags the conflict and recommends a corrective action.

### Paper-Writing Value

High.

This branch creates a clear "System-2 3R" story:

```text
3R should not be single-pass prediction only;
it should verify hard geometry and spend compute/action only when needed.
```

### Fail-Fast Condition

If conflict labels cannot be made reliable from public examples / KYKT metadata, or if no concrete A5 action can be attached to A4 verification, do not deepen first.

### Current Recommendation

Strong finalist candidate.

## Candidate 2: Executive Memory / State Governance

### Core Claim

Long-context 3R is not solved by adding memory alone. The missing mechanism is governance: deciding when to update state, write spatial memory, protect anchors, evict cache, retrieve global context, or reject unreliable evidence.

### Failure Modes

- F1 Long-Context Drift / Forgetting
- F3 Hard-Case Geometric Ambiguity
- F2 Dynamic-Static Entanglement when memory writes must be gated
- F6 Fragmented Model Ecology when memory policy spans multiple model outputs

### Owned Actions

- A1 State Update Control
- A2 Spatial Memory Governance
- A3 Context / Anchor Budgeting

Support actions:

- A4 Geometry Verification
- A6 Dynamic/Object State Separation

### Comparator Pressure

- Spann3R
- Point3R
- CUT3R
- STream3R
- LONG3R
- LoGeR
- Mem3R
- PAS3R
- FILT3R
- LongStream
- OVGGT

Weakest pressure point:

```text
The memory field is crowded. Dream must not claim memory, streaming state, hybrid memory, pose-adaptive update, Kalman filtering, or cache protection as new by themselves.
```

### First Proxy Test

Use P2 + P3:

- P2 anchor retention
- P3 memory growth and usefulness

Minimum evidence:

- compare fixed sliding window, uniform keyframes, confidence-only policy, and Dream evidence-triggered policy
- report anchor retention, memory growth, write rate, duplicate rate, and expected retrieval usefulness

### Teacher Demo

Timeline demo: the system explains which frames/state cells it updates, which anchors it protects, what it evicts, and when it requests global context.

### Paper-Writing Value

Very high.

This branch can unify sparse attention, SSM/Mamba, attention residuals, Kalman updates, external memory, cache protection, and long-context 3R under one control vocabulary.

### Fail-Fast Condition

If the action set cannot be reduced to a small measurable policy, or if proxy metrics cannot distinguish Dream policy from simple keyframe/cache rules, do not deepen first.

### Current Recommendation

Strong finalist candidate, but must be sharply scoped.

## Candidate 3: 3R Composer / Unified Model Ecology

### Core Claim

The 3R ecosystem is fragmented across pair matching, many-view reconstruction, streaming, dynamic video, guided reconstruction, and Gaussian asset generation. A composer can turn this fragmentation into capability cards, evidence reports, and mechanism distillation.

### Failure Modes

- F6 Fragmented Model Ecology
- F3 Hard-Case Geometric Ambiguity
- F1 Long-Context Drift / Forgetting
- F2 Dynamic-Static Entanglement

### Owned Actions

- A5 Repair / Reroute Decision

Support actions:

- A3 Context / Anchor Budgeting
- A4 Geometry Verification
- A7 Prior / Modality Arbitration

### Comparator Pressure

- DUSt3R
- MASt3R
- MASt3R-SfM
- Fast3R
- Spann3R
- MonST3R
- CUT3R
- STream3R
- SLAM3R
- MV-DUSt3R+
- Splatt3R
- InstantSplat
- NoPoSplat

Weakest pressure point:

```text
If it remains only model routing, it is likely system engineering rather than paper-grade architecture.
```

### First Proxy Test

Use P5:

- P5 route regret

Minimum evidence:

- capability cards
- sample regime cards
- route recommendation
- route regret estimate against paper-reported strengths and known limitations

### Teacher Demo

Given an input, Dream explains why it chooses or rejects MASt3R, Fast3R, Spann3R, CUT3R, MonST3R, Splatt3R, or another route.

### Paper-Writing Value

Medium-high as L1, high as L2.

L1 system composer supports KYKT and demo. L2 mechanism distillation can support the paper by extracting unified actions from multiple 3R models.

### Fail-Fast Condition

If the branch cannot move from L1 routing to L2 mechanism distillation or benchmark claim, keep it as infrastructure rather than thesis.

### Current Recommendation

Best evidence infrastructure; likely pair with another finalist rather than stand alone.

## Candidate 4: Dynamic Object Permanence / 4D Memory

### Core Claim

Dynamic 3R should not merely estimate per-frame motion. It should preserve object identity, uncertainty, and memory while preventing dynamic regions from corrupting static scene state.

### Failure Modes

- F2 Dynamic-Static Entanglement
- F1 Long-Context Drift / Forgetting
- F3 Hard-Case Geometric Ambiguity

### Owned Actions

- A6 Dynamic/Object State Separation

Support actions:

- A2 Spatial Memory Governance
- A4 Geometry Verification
- A7 Prior / Modality Arbitration

### Comparator Pressure

- MonST3R
- POMATO
- D^2USt3R
- Easi3R
- RayMap3R
- 4DGS variants
- G-CUT3R as guided boundary

Weakest pressure point:

```text
Dynamic pointmaps and training-free dynamic correction are already occupied. Dream needs object permanence and memory-policy evidence, not just dynamic reconstruction.
```

### First Proxy Test

Use P4:

- P4 dynamic pollution
- object identity consistency

Minimum evidence:

- dynamic/static case labels
- object-motion labels
- static-map update decisions
- object identity / uncertainty notes

### Teacher Demo

Show a moving object being separated from static map updates while its identity and uncertainty persist across time.

### Paper-Writing Value

High.

It gives Dream a clear F2-specific claim and a strong visual narrative. It also connects memory, dynamics, segmentation/tracking/flow, event signals, and 4D assets.

### Fail-Fast Condition

If object identity cannot be measured or if the demo becomes only a 4DGS visualization, keep this as a major comparator branch rather than first mechanism spec.

### Current Recommendation

Close finalist candidate; should remain alive even if not first.

## Candidate 5: Cross-Modal / Event-Augmented 3R

### Core Claim

RGB-only 3R is fragile under blur, low light, high-speed motion, rolling shutter, and weak texture. The research question is not just adding sensors, but deciding when to trust, reject, or arbitrate priors.

### Failure Modes

- F5 Sensor / Modality Fragility
- F2 Dynamic-Static Entanglement
- F3 Hard-Case Geometric Ambiguity

### Owned Actions

- A7 Prior / Modality Arbitration

Support actions:

- A4 Geometry Verification
- A6 Dynamic/Object State Separation
- A8 Evidence Acquisition / Adaptation Budget

### Comparator Pressure

- EAG3R
- Event-3DGS
- G-CUT3R
- event depth / reconstruction
- guided 3R

Weakest pressure point:

```text
The obvious Event-DUSt3R framing is already emerging, and hardware/data burden is high.
```

### First Proxy Test

Use prior conflict detection / robustness labels:

- identify RGB-failure cases
- classify whether event/depth/pose/calibration prior would help
- mark cases where the prior could conflict with RGB geometry

### Teacher Demo

Blurred or low-light RGB sample where a sensor prior explains a geometry rescue or conflict.

### Paper-Writing Value

Medium-high.

Strong as a robustness and related-work axis, but not clearly first implementation under current constraints.

### Fail-Fast Condition

If public artifacts or datasets cannot support low-cost proxy labeling, keep as writing/taxonomy branch for now.

### Current Recommendation

Keep alive; not first finalist unless the user wants robustness/cross-modal focus.

## Candidate 6: Active Spatial Perception / RL-3R

### Core Claim

Some 3R failures are not model failures but observation failures. A spatial system should request views, revisit regions, or allocate action budget when uncertainty remains high.

### Failure Modes

- F4 Passive Observation Limit
- F3 Hard-Case Geometric Ambiguity
- F5 Sensor / Modality Fragility

### Owned Actions

- A8 Evidence Acquisition / Adaptation Budget

Support actions:

- A4 Geometry Verification
- A7 Prior / Modality Arbitration

### Comparator Pressure

- next-best-view
- active perception
- robotics reconstruction
- VLA-style systems
- NextBestSense-style stacks
- CTRL-style policy learning as action-selection analogy

Weakest pressure point:

```text
Engineering scope can explode into robotics or simulation before Dream has a stable 3R evidence loop.
```

### First Proxy Test

Use P7:

- P7 uncertainty reduction / view gain

Minimum evidence:

- mock uncertainty maps
- candidate next-view cards
- estimated view gain
- no robotics readiness claim

### Teacher Demo

Model says: "I cannot infer this hidden surface; move the camera here."

### Paper-Writing Value

High long-term.

This branch connects Dream to embodied spatial intelligence, but its first evidence path is the least direct.

### Fail-Fast Condition

If the proxy cannot avoid robotics/simulation overhead, defer implementation and keep as future expansion / paper outlook.

### Current Recommendation

High-upside future branch; not first unless we deliberately choose an embodied-AI framing.

## Provisional Synthesis

The strongest immediate package appears to be:

```text
Finalist A: Geometry Critic / System-2 3R
Finalist B: Executive Memory / State Governance
Support layer: 3R Composer / Unified Model Ecology
Close reserve: Dynamic Object Permanence / 4D Memory
```

Reason:

- Geometry Critic has the clearest low-cost proxy and demo.
- Executive Memory has the strongest architecture / paper umbrella.
- Composer makes evidence, KYKT integration, and model comparison operational.
- Dynamic Object Permanence gives the strongest F2-specific visual story but needs object-identity proxy evidence first.

This is not a final decision.

## Decision Needed From User

Choose one of these next moves:

```text
A. Draft mechanism specs for Geometry Critic + Executive Memory, with Composer as support.
B. Add Dynamic Object Permanence as a third finalist before mechanism specs.
C. Keep all six branches and first prepare proxy case-card templates.
D. Mine more sources before choosing finalists.
```

Current research recommendation:

```text
B. Add Dynamic Object Permanence as a third finalist before mechanism specs.
```

Reason:

It preserves the strongest dynamic / visual paper story while still keeping the first implementation path grounded in critic + memory + composer.
