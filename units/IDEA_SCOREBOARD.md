# Idea Scoreboard

Last updated: 2026-05-01

Scores are first-pass estimates. Scale: 1 low, 5 high. `shallow risk` is inverted in total: lower risk is better.

| ID | Track | Novelty | 3R relevance | Bottleneck severity | Demo value | Feasibility | KYKT fit | Paper story | Code/data | Shallow risk | First-pass decision |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| RU-001 Geometry-Gated State-Space 3R | Memory/State | 5 | 5 | 5 | 4 | 2 | 4 | 5 | 3 | 3 | Keep as architecture candidate |
| RU-002 3R Composer Controller | Composer | 3 | 5 | 4 | 5 | 5 | 5 | 3 | 5 | 4 | Best near-term demo |
| RU-003 Test-Time Geometry Self-Check | Reasoning/TTC | 4 | 5 | 4 | 5 | 4 | 5 | 4 | 4 | 2 | Strong demo + research bridge |
| RU-004 External Sparse Spatial Memory | Memory/State | 4 | 5 | 5 | 4 | 3 | 4 | 5 | 3 | 2 | Foundational design rule |
| RU-005 3R-to-4DGS Bridge | Demo/4D | 3 | 4 | 4 | 5 | 3 | 4 | 3 | 4 | 3 | Demo enabler |
| RU-006 Event-Augmented Pointmap 3R | Cross-modal | 3 | 4 | 4 | 4 | 2 | 2 | 3 | 2 | 3 | Background/enabler |
| RU-007 Attention-Residual / KDA 3R | Architecture transfer | 4 | 3 | 4 | 3 | 1 | 3 | 4 | 2 | 4 | Speculative only |
| RU-008 Pose-Free Gaussian Demo Bridge | Demo/GS | 3 | 4 | 3 | 5 | 4 | 4 | 3 | 5 | 3 | Strong short-term demo enabler |
| RU-009 Route-Scan Policy Bank | Memory/State | 4 | 5 | 4 | 4 | 3 | 4 | 4 | 3 | 2 | Architecture subunit |
| RU-010 Hybrid Context Router | Memory/State | 4 | 5 | 5 | 4 | 3 | 5 | 5 | 3 | 2 | High-priority design candidate |
| RU-011 Geometry Critic-Revision Loop | Reasoning/TTC | 5 | 5 | 4 | 5 | 4 | 5 | 5 | 4 | 2 | Best System-2 paper bridge |
| RU-012 Self-Adapt Adapter for 3R | Continual | 4 | 4 | 4 | 3 | 2 | 3 | 4 | 3 | 3 | Second-wave research |
| RU-013 Dynamic 4D Pointmap Branch | Dynamic/4D | 4 | 5 | 5 | 4 | 3 | 4 | 4 | 3 | 2 | Required comparator branch |
| RU-014 Long-Context Hybrid Memory Benchmark | Benchmark/System | 3 | 5 | 5 | 4 | 4 | 5 | 4 | 4 | 1 | Evidence infrastructure |
| RU-015 Geometry-Governed Executive Memory for 3R | Architecture thesis | 5 | 5 | 5 | 5 | 3 | 5 | 5 | 3 | 2 | Strong candidate branch, not sole bet |

## Initial Ranking

### Near-Term Demo

1. RU-002 3R Composer Controller
2. RU-011 Geometry Critic-Revision Loop
3. RU-008 Pose-Free Gaussian Demo Bridge
4. RU-014 Long-Context Hybrid Memory Benchmark
5. RU-005 3R-to-4DGS Bridge

### Architecture Candidate Branches

Do not treat this as a final ranking. Use it as a branch pool.

1. RU-015 Geometry-Governed Executive Memory for 3R
2. RU-011 Geometry Critic-Revision Loop
3. RU-013 Dynamic 4D Pointmap Branch
4. RU-010 Hybrid Context Router
5. RU-004 External Sparse Spatial Memory
6. RU-001 Geometry-Gated State-Space 3R
7. RU-009 Route-Scan Policy Bank
8. RU-006 Event-Augmented Pointmap 3R

### Speculative Watchlist

1. RU-007 Attention-Residual / KDA 3R
2. RU-012 Self-Adapt Adapter for 3R
3. RU-006 Event-Augmented Pointmap 3R

## First Interpretation

The best current strategy is probably:

```text
Architecture thesis:
  Geometry-gated spatial memory / state update for streaming 3R.

Near-term teacher demo:
  3R Composer + Geometry Critic-Revision + Pose-Free Gaussian Quick Win inside KYKT.
```

This does not commit the project yet. It is a hypothesis for the next research batch.

## Second-Pass Interpretation

After subagent merge, the best non-shallow framing is:

```text
Dream studies how 3R systems route, store, compress, verify, and adapt spatial state.
```

This is stronger than a direct "Mamba-3R" title because it absorbs SSM, causal transformer, explicit spatial memory, test-time training, and dynamic 4D pointmaps under one falsifiable research program.

## Third-Pass Interpretation

After the Dream3R thesis stress test, one strong framing is:

```text
Dream should study geometry-governed executive memory:
the policy that decides when 3R should write, preserve, compress, evict, verify, revise, or adapt spatial state.
```

This can reframe RU-001, RU-004, RU-010, RU-011, RU-012, RU-013, and RU-014 as components or evidence lanes under RU-015, but that should not be accepted until compared against other branches.

It is not a final thesis decision.

## Fourth-Pass Process Correction

User correction on 2026-05-02:

```text
Do not bet on one small direction too early.
```

Next scoring step:

```text
Compare branches, not only Research Units:
executive memory, System-2 geometry critic, dynamic object permanence,
cross-modal/event 3R, 3R composer, and active perception.
```
