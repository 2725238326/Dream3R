# Dream Multi-Track Research Canvas

Last updated: 2026-05-04 (cycle 008.5 sync: four-finalist set + no-all-in posture appended; original cycle 003 GEM-3R framing preserved)

Status: active.

## Purpose

This file prevents Dream from prematurely betting on one narrow direction.

Current rule:

```text
Do not collapse Dream into GEM-3R, Mamba-3R, Event-DUSt3R, 4DGS, or any single thesis branch yet.
```

The next research phase should compare multiple candidate branches under the same evidence standard.

## Candidate Branches

### Branch A: Executive Memory / State Governance

Representative unit:

```text
RU-015 Geometry-Governed Executive Memory for 3R
```

Core question:

```text
Can 3R systems learn or follow explicit policies for writing, reading, preserving, compressing, and revising spatial state?
```

Closest competitors:

- Spann3R
- CUT3R
- Point3R
- LONG3R
- LoGeR
- Mem3R
- PAS3R
- FILT3R
- OVGGT

Why it is interesting:

- directly attacks long-sequence forgetting, drift, cache growth, and state corruption
- naturally connects to test-time reasoning and dynamic/static separation

Risk:

- may look incremental unless the controller/action space is formalized sharply

### Branch B: Geometry Critic / System-2 3R

Representative units:

```text
RU-003 Test-Time Geometry Self-Check
RU-011 Geometry Critic-Revision Loop
```

Core question:

```text
Can 3R reconstruction become self-verifying and spend more compute only on geometrically hard cases?
```

Closest competitors:

- Test3R
- TTT3R
- VLM / reasoning-style verifier work

Why it is interesting:

- teacher-facing story is clear
- low-cost proxy demo is possible
- gives a rigorous route toward test-time compute in 3R

Risk:

- if no revision action exists, it becomes only diagnostics

### Branch C: Dynamic Object Permanence / 4D Memory

Representative units:

```text
RU-013 Dynamic 4D Pointmap Branch
RU-005 3R-to-4DGS Bridge
```

Core question:

```text
Can dynamic 3R preserve object identity, geometry, uncertainty, and memory across long time instead of merely estimating motion frame by frame?
```

Closest competitors:

- MonST3R
- POMATO
- D^2USt3R
- Easi3R
- RayMap3R
- 4DGS variants

Why it is interesting:

- strong visual surprise path
- connects directly to world-model / 4D asset narrative

Risk:

- can become a graphics demo unless the memory/permanence claim is real

### Branch D: Cross-Modal / Event-Augmented 3R

Representative unit:

```text
RU-006 Event-Augmented Pointmap 3R
```

Core question:

```text
Can event streams or other sensors solve failure modes that RGB-only 3R cannot solve, especially blur and high-speed motion?
```

Closest competitors:

- EAG3R
- Event-3DGS
- event-based depth / reconstruction literature

Why it is interesting:

- high novelty perception
- hardware story is memorable

Risk:

- hardware/data burden is high
- EAG3R already occupies the obvious Event-DUSt3R framing

### Branch E: 3R Composer / Unified Model Ecology

Representative units:

```text
RU-002 3R Composer Controller
RU-008 Pose-Free Gaussian Demo Bridge
RU-014 Long-Context Hybrid Memory Benchmark
```

Core question:

```text
Can we turn fragmented 3R models into a regime-aware research system with unified contracts, capability cards, and evidence reports?
```

Closest competitors:

- MASt3R / MASt3R-SfM
- Fast3R
- SLAM3R
- Splatt3R
- NoPoSplat
- MV-DUSt3R+

Why it is interesting:

- lowest-cost visible demo path
- strongest KYKT integration path
- useful for managing future research

Risk:

- more system/composer than paper-grade architecture unless paired with critic, memory, or benchmark novelty

### Branch F: Active Spatial Perception / RL-3R

Representative future unit:

```text
RU-TBD Active Perception / Next-Best-View 3R
```

Core question:

```text
Can a 3R system actively choose the next view or robot motion to reduce reconstruction uncertainty?
```

Closest competitors:

- Next-Best-View literature
- active perception / VLA systems
- robotics reconstruction pipelines

Why it is interesting:

- strongest embodied-AI / world-model expansion
- high teacher-surprise potential

Risk:

- engineering cost and data/simulation burden are high
- likely not the first implementation target

## Comparison Criteria

Score each branch on:

- novelty after 2026 comparator check
- mathematical / architectural crispness
- smallest defensible evidence path
- teacher-facing surprise
- engineering cost
- KYKT integration value
- risk of being only a system wrapper
- risk of being already occupied

## Near-Term Rule

Before drafting a full mechanism spec for any one branch, do one comparative round:

```text
Branch survey -> branch comparison matrix -> 2-3 finalist branches -> user decision -> mechanism spec
```

GEM-3R remains a strong candidate branch, but not the default thesis.

## Cycle 008.5 Update

The cycle 003 framing above (GEM-3R as one candidate branch among many; near-term rule for one comparative round) is preserved as historical posture. The current state after cycle 008 + cycle 008.5 supersedes it on two axes:

1. **The comparative round has run.** The shortlist decision surface (`planning/BRANCH_SHORTLIST_DECISION_SURFACE.md`) was completed; user chose option B (DEC-20260503-002), then upgraded Composer to fourth finalist (DEC-20260504-001). Mechanism specs are drafted at L1 for all four finalists. The "before drafting a spec" precondition is therefore satisfied for the current finalist set.

2. **No single finalist is the thesis spine.** Per DEC-20260504-002, memory / critic / permanence / composer are treated as parallel borrowable components, not thesis-level commitments. The "GEM-3R remains a strong candidate" line is honored: GEM-3R is the working title for the Memory finalist (`specs/SPEC-20260503-002-executive-memory.md`), one of four parallel finalists, and is explicitly not the spine.

Current four-finalist set:

```text
Branch A: Executive Memory / State Governance       SPEC-20260503-002 (GEM-3R working title)
Branch B: Geometry Critic / System-2 3R             SPEC-20260503-001
Branch C: Dynamic Object Permanence / 4D Memory     SPEC-20260503-003
Branch E: 3R Composer / Unified Model Ecology       SPEC-20260504-001
```

Lower-priority reserves (alive in canvas; not finalists):

```text
Branch D: Cross-Modal / Event-Augmented 3R          (A7 owner; deferred)
Branch F: Active Spatial Perception / RL-3R         (A8 owner; deferred)
```

Anti-collapse rule (current):

```text
Do not collapse Dream into Critic alone, Memory alone, Permanence alone, or
Composer alone. Cycle 009 case cards run on parallel tracks; agent must not
auto-promote any single result to "leading" status without a user decision turn.
```

The cycle 003 anti-collapse rule (do not collapse into GEM-3R / Mamba-3R / Event-DUSt3R / 4DGS / single-thesis-branch) remains active and now subsumes the cycle 008.5 anti-collapse rule.
