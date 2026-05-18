# Branch Comparison Matrix

Last updated: 2026-05-04 (cycle 008.5 sync: Composer promoted to fourth finalist; no-all-in posture recorded; Next Action superseded)

Status: filled first comparative pass (cycle 004); four-finalist set drafted at L1 (cycle 008 + cycle 008.5); not a thesis decision.

## Purpose

Compare multiple research branches before betting on one direction.

## Reading Rule

Scores are 1-5, where higher is better. They are branch-comparison signals, not approval to deepen a branch.

Evidence labels:

- `paper-proven`: mechanism is directly supported by cited papers/projects in the current source map.
- `inferred`: Dream synthesis from source mechanisms.
- `speculative`: plausible but not yet source/proxy backed.
- `unknown`: performance or implementation result not measured.

## Branch Matrix

| Branch | Failure modes addressed | Closest competitors | Mechanism ingredients | Possible compositions | Novelty gap | Smallest evidence path | Teacher-facing demo | Engineering cost | Top-conference risk | KYKT support path | Recommendation |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Executive Memory / State Governance | F1 primary; F2/F3 secondary | Spann3R, CUT3R, STream3R, LONG3R, Point3R, LoGeR, Mem3R, PAS3R, FILT3R, LongStream, OVGGT | persistent latent state, uncertainty, external pointer memory, local cache, protected anchors, sparse/linear context budget, dynamic branch trigger, critic trigger | C1 Kalman update + anchor cache; C2 external memory + critic; C3 dynamic/static split + memory governance; C5 route-scan + hybrid memory; C13 sparse context + anchor protection | not "memory" itself; gap is explicit action policy over latent update, cache, anchors, external memory, critic, sparse context, and dynamic branch | L1 policy graph plus L2 proxy simulation comparing uniform update, pose-adaptive update, Kalman update, cache protection, external write, sparse retrieval, critic-triggered revision | timeline showing what the model writes, protects, forgets, verifies, and refuses to trust | medium for proxy; high for learned controller | close 2026 memory competitors; too broad unless action set is small and measurable | Dream research lane, Advisor/report, Sample Matrix, future management area | strong candidate, but do not deepen until compared with critic/composer/dynamic branches |
| Geometry Critic / System-2 3R | F3 primary; F1/F6 secondary | Test3R, TTT3R, CTRL-style critic-revision, geometry consistency methods, MASt3R-SfM, SLAM3R, MV-DUSt3R+, G-CUT3R | non-learned or learned geometry critic, reprojection residuals, pointmap conflict, confidence disagreement, revision queue, adaptive compute, model reroute, visual/semantic failure signal | C2 external memory + critic; C4 critic + composer rerouting; C7 critic + adapter budget; C10 guided priors + critic conflict check; C16 RL policy + critic/composer actions | critic-only diagnostics are insufficient; novelty requires concrete accept/retry/reroute/revise actions | L2 non-learned critic report over existing/public outputs; no checkpoint run required if using metadata/public artifacts | difficult sample where Dream detects a geometric conflict and explains the chosen repair action | low for report; medium for Test3R-style integration later | may be seen as evaluator unless revision changes the output or route | Advisor/report, JobDetail diagnostics, Sample Matrix quality flags | best low-cost research bridge; keep in top comparison pool |
| Dynamic Object Permanence / 4D Memory | F2 primary; F1/F3 secondary | MonST3R, POMATO, D^2USt3R, Easi3R, RayMap3R, 4DGS variants, 4DGS in the Wild, G-CUT3R as guided boundary | dynamic pointmaps, motion-aware validity, static/dynamic memory split, object identity, object uncertainty, segmentation/tracking/flow priors, 4D asset bridge | C3 dynamic/static split + memory governance; C6 event signal + dynamic branch; C9 object permanence + 4DGS initialization; C15 visual prior + dynamic memory split | dynamic pointmaps are occupied; gap is long-horizon object permanence and memory policy, not just motion estimation | L1 dynamic failure taxonomy plus L2 simulated policy for static-map update, dynamic object memory, and reject/conflict regions | moving object remains tracked separately while static map stays stable | medium for taxonomy/proxy; high for 4D prototype | can collapse into graphics demo; object identity evidence may be hard | dynamic sample lane, future 4D asset bridge, research report | keep as required major branch and comparator; do not reduce it to 4DGS demo |
| Cross-Modal / Event-Augmented 3R | F5 primary; F2/F3 secondary | EAG3R, Event-3DGS, event depth/reconstruction, G-CUT3R/guided 3R | event/RGB fusion, blur-free temporal evidence, depth/pose/calibration priors, sensor-prior conflict check, dynamic trigger | C6 event signal + dynamic branch; C10 guided priors + critic conflict check; C12 active sensing + event/guided mode | obvious event-augmented pointmap idea is already emerging; gap is policy: when sensor priors should override, support, or be rejected by RGB geometry | L1 source/dataset analysis and failure taxonomy; L2 only if public event/RGB artifacts are available without heavy setup | blurred RGB failure compared with event- or prior-stabilized geometry explanation | medium-high; hardware/data burden for real demo | may be peripheral to RGB 3R and hard to verify locally | research lane first; not immediate runner | keep alive as robustness branch; not first implementation target under current constraints |
| 3R Composer / Unified Model Ecology | F6 primary; F3/F1/F2 secondary | DUSt3R, MASt3R, MASt3R-SfM, Fast3R, Spann3R, MonST3R, CUT3R, STream3R, SLAM3R, MV-DUSt3R+, Splatt3R, InstantSplat, NoPoSplat | capability cards, unified output contracts, model routing, benchmark matrix, artifact evidence reports, sample-regime classifier, two-layer composer L1/L2 | C4 critic + composer rerouting; C8 composer + benchmark matrix; C10 guided priors + critic conflict check; C16 RL policy + critic/composer actions | routing alone is system work; paper-grade gap appears only if the composer exposes a failure-mode benchmark or distills model strengths into unified actions | L2 capability matrix and unified evidence report using existing KYKT/public metadata; no reproduction required | system chooses and justifies model route by input regime and failure mode | low-medium | may be rejected as engineering unless paired with a new controller, benchmark, or mechanism-distillation claim | strongest KYKT fit: research lane, runner planning, Sample Matrix, Advisor | best infrastructure/demo branch; keep L1 for support and L2 for paper-grade mechanism distillation |
| Active Spatial Perception / RL-3R | F4 primary; F3/F2 secondary | next-best-view, active perception, robotics reconstruction, VLA-style systems, NextBestSense-style stacks | uncertainty map, information gain, next-view policy, action budget, route/revisit policy, RL/planning, critic-triggered action selection | C11 active view + uncertainty map; C12 active sensing + event/guided mode; C16 RL policy + critic/composer actions | NBV is established; gap is coupling 3R pointmap uncertainty, memory state, and critic signals into an action policy | L1 design and simulation-only study using mock uncertainty maps and non-RL action logs first; no robot or sim stack yet | model asks for a new view because uncertainty remains high | high for real prototype; low only for mock/simulation design | high scope and sim-to-real risk; likely too broad for first concrete cycle | future robotics/embodied lane; possible proposal story | high-upside long-range branch; keep alive but avoid implementation now |

## Score Matrix

| Branch | Novelty after comparator check | Paper crispness | Evidence feasibility | Demo surprise | Engineering feasibility | KYKT fit | Risk control | Current signal |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Executive Memory / State Governance | 4 | 4 | 3 | 4 | 3 | 5 | 3 | strongest architecture umbrella if action policy is formalized |
| Geometry Critic / System-2 3R | 4 | 5 | 4 | 5 | 4 | 5 | 4 | strongest low-cost bridge from research to visible evidence |
| Dynamic Object Permanence / 4D Memory | 4 | 3 | 3 | 5 | 2 | 4 | 3 | high visual surprise, but must prove permanence rather than motion handling |
| Cross-Modal / Event-Augmented 3R | 3 | 3 | 2 | 4 | 2 | 2 | 2 | robustness branch with high data/hardware risk |
| 3R Composer / Unified Model Ecology | 3 | 4 | 5 | 5 | 5 | 5 | 4 | best support infrastructure and demo surface, weaker as standalone thesis |
| Active Spatial Perception / RL-3R | 4 | 3 | 2 | 5 | 1 | 3 | 2 | high-upside future branch, too costly for first implementation |

## Cross-Branch Interpretation

The current matrix suggests a three-layer research structure, not a final thesis:

1. Architecture candidates: Executive Memory, Geometry Critic, Dynamic Object Permanence, Active Perception.
2. Evidence infrastructure: 3R Composer / Unified Model Ecology.
3. Robustness extension: Cross-Modal / Event-Augmented 3R.

No branch is discarded. No finalist set is approved yet.

## Cycle 008.5 Update

The cycle 004 layer-structure framing above is preserved as historical interpretation. The current state after cycle 008 + cycle 008.5 supersedes it:

```text
Four user-approved finalists (parallel; no thesis spine per DEC-20260504-002):
  Finalist 1: Geometry Critic / System-2 3R           (SPEC-20260503-001; A4 + A5 repair facet; P1 + P5)
  Finalist 2: Executive Memory / State Governance     (SPEC-20260503-002; A1 + A2 + A3; P2 + P3)
  Finalist 3: Dynamic Object Permanence / 4D Memory   (SPEC-20260503-003; A6; P4 + identity_consistency)
  Finalist 4: 3R Composer / Unified Model Ecology     (SPEC-20260504-001; A5 routing facet; P5 + capability_match)

Lower-priority reserves (alive in canvas; not finalists):
  Cross-Modal / Event-Augmented 3R     (A7 owner; deferred)
  Active Spatial Perception / RL-3R    (A8 owner; deferred)
```

A5 ownership is split across finalists 1 and 4: Critic owns the per-window repair facet (rerun_local_region, open_anchor_budget, request_prior); Composer owns the across-model routing facet (reroute_model). The split is formalized in `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v1 conflict rule CR-1.

The "evidence infrastructure" framing for Composer is no longer current. Composer is now a finalist with its own falsification axis (route_regret); its evidence-infrastructure character continues but is not the primary claim.

The score matrix above is preserved as a cycle 004 signal. It has not been re-scored after cycle 008.5; Composer's score row in particular reflects the original "evidence infrastructure" framing rather than its current finalist status. Re-scoring is deferred until cycle 009 case-card data lands.

## Open Comparison Questions

| Question | Why it matters | Branches affected | Evidence needed before deepening |
|---|---|---|---|
| Can "executive memory" be reduced to 5-7 measurable actions? | avoids broad system wrapper criticism | Executive Memory; Dynamic; Critic | action taxonomy and proxy metrics |
| Can a geometry critic perform an actual action, not just report failure? | separates System-2 3R from diagnostics | Critic; Composer; Memory | retry / reroute / local revise policy |
| What is the smallest object permanence signal? | prevents dynamic branch from becoming generic 4D reconstruction | Dynamic; Event; Memory | identity, uncertainty, and memory-update labels on dynamic samples |
| Is Composer a paper claim or only KYKT infrastructure? | controls top-conference risk | Composer; all branches | capability-card benchmark and failure-mode routing objective |
| Can active perception be studied without robot/sim overhead? | keeps the branch alive without derailing Phase 1.5 | Active; Memory; Critic | mock uncertainty map and next-view policy design |

Status of each question after cycle 008.5:

- Memory action set reduced to A1 + A2 + A3 in `specs/SPEC-20260503-002-executive-memory.md`. Cycle 009 case cards test whether this passes the "5-7 measurable actions" bar via P2/P3.
- Critic concrete-action question answered at L1 by `specs/SPEC-20260503-001-geometry-critic.md` action policy table (rerun_local_region / reroute_model / open_anchor_budget / request_prior). Cycle 009 case cards test whether each fires non-trivially.
- Permanence object-identity signal defined in `specs/SPEC-20260503-003-dynamic-object-permanence.md` as identity_consistency proxy under P4. Cycle 009 case cards test whether it is hand-labelable within the D4 budget.
- Composer paper-vs-infrastructure question answered by promoting Composer to finalist with route_regret falsification axis in `specs/SPEC-20260504-001-3r-composer.md`. Cycle 009 case cards test whether route_regret has nonzero spread.
- Active perception remains deferred; no spec drafted; question stays open.

## Next Action

The action taxonomy and proxy metric first pass now lives in:

```text
planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md
```

Before drafting a mechanism spec for any single branch, prepare a shortlist decision surface:

1. one-page summary per candidate branch
2. owned A1-A8 actions
3. weakest comparator pressure
4. first proxy test
5. teacher demo form
6. fail-fast condition
7. ask the user which 2-3 branches should be deepened

## Next Action (Superseded; Cycle 008.5)

The cycle 004 next-action plan above has been executed:

- Step 1-7 produced `planning/BRANCH_SHORTLIST_DECISION_SURFACE.md`.
- The user shortlist decision was DEC-20260503-002 (option B: Critic + Memory + Permanence) plus DEC-20260504-001 (Composer added as fourth finalist).
- Mechanism specs were drafted for all four finalists.

The current next action is:

1. Authorize cycle 009 to start filling L2 case cards (`CASE-20260504-CRITIC-01..03` first per cycle 008 D1).
2. Run the four parallel case-card tracks under the per-card 90-120 minute budget (D4) and the cross-spec signal contract v1.
3. After case-card data lands, re-surface D3 (first teacher demo target) once `paradigm/TEACHER_AUDIENCE_PROFILE.md` is populated.
4. Re-score this matrix in cycle 010+ with case-card evidence rather than cycle 004 design-only signals.
