# SPEC-20260506-002 Dream3R Ablation Plan v0.1

## Identity

spec_id: SPEC-20260506-002

date: 2026-05-06

status: draft v0.1 (cycle 016 S3; markdown only; no training, no GPU runs; input for future experimental authorization)

cycle_of_origin: cycle 016

parent_spec: SPEC-20260506-001 (Dream3R architecture v0.1)

## Purpose

This document specifies which experiments would falsify which architectural claims in Dream3R v0.1. It is a DESIGN-TIME ablation plan — it defines the experiments that WOULD be run IF training is ever authorized. No training is authorized by this file.

The plan answers: "if you could train Dream3R, what experiments would you run first, and what outcome would kill which claim?"

## Ablation plan structure

Each ablation is specified as:

```text
- WHAT is removed or changed (the ablation itself)
- WHICH architectural claim it targets (what is at stake)
- WHAT outcome would FALSIFY the claim (the kill condition)
- WHAT outcome would SUPPORT the claim (the survive condition)
- PRIORITY (which ablations must run first)
- DEPENDENCIES (which ablations depend on others)
- PROXY METRICS used to measure the outcome
```

## Priority ordering

Ablations are grouped into three tiers:

```text
Tier 1 (must-run): These ablations target the LOAD-BEARING architectural
  claims — the things that make Dream3R different from "modular composition
  with conventions." If Tier 1 ablations fail, the architecture story
  collapses. Run these first.

Tier 2 (should-run): These ablations target per-module claims — whether
  each module's specific substrate choice matters. If Tier 2 ablations
  fail, the module design changes but the overall architecture story
  survives.

Tier 3 (nice-to-have): These ablations target secondary interactions,
  evidence-signal weighting, and hyperparameter sensitivity. They refine
  the architecture but do not threaten the core story.
```

---

## Tier 1: Load-bearing architecture ablations

### ABL-1: Bus removal (flat baseline)

```text
Target claim  : "the cross-spec memory bus with CR-rules-as-gates is
                architecturally novel and load-bearing" (architecture spec
                sections: bus design, CR-1..CR-6, block diagram)

Ablation      : REMOVE the bus entirely. Each module (Perceiver, Memory,
                Critic, Permanence, Composer) runs independently. No
                cross-spec signals, no handoffs, no gates. Each module
                receives only Perceiver output (T1 + T2) and its own
                internal state. The modules are otherwise identical
                (same substrate, same parameter count).

                Concretely:
                - Critic reads T2 + T3-perceive-only (no dynamic_ratio,
                  no capability_match, no latent_drift_proxy)
                - Memory reads T1 summary + T3-perceive-only (no
                  dynamic_ratio, no conflict_score, no suppress_static_
                  write handoff)
                - Permanence reads T2 + dynamic_mask (no conflict_score
                  feedback, no route info)
                - Composer reads metadata only (no route_history from
                  Critic)
                - CR-1..CR-6 gates are all removed

Expected if claim holds (survive):
  - Full Dream3R (with bus) outperforms flat baseline on at least 3 of
    the 6 proxy metrics (P1 conflict detection, P2 anchor retention,
    P3 memory growth, P4 dynamic pollution, P5 route regret, P6 action
    entropy) by a statistically significant margin.
  - CR-rule firing rate in the full model is nonzero on benchmark inputs
    (CR-1 fires on at least some inputs where capability_match spread is
    small; CR-2 fires on at least some windows with dynamic regions).

Expected if claim fails (kill):
  - Flat baseline matches or exceeds full Dream3R on 4+ of 6 proxy
    metrics. This would mean the bus adds complexity without benefit;
    the architecture story collapses to "modular composition."

Proxy metrics : P1, P2, P3, P4, P5, P6 + CR-rule firing rates

Priority      : HIGHEST. This is the single most important ablation.
                If the bus does not help, nothing else in the
                architecture spec matters.

Dependencies  : none (this is the root ablation)

Risk ref      : R2 (bus-as-novelty collapse if CR-rules never fire)
```

### ABL-2: Substrate hypothesis (hybrid vs. single-substrate)

```text
Target claim  : "the hybrid substrate (transformer perception + SSM
                executive memory + slot memory for Permanence) is
                load-bearing; forcing all substrates into one type
                degrades performance" (architecture spec: substrate
                hypothesis section)

Ablation      : THREE variants compared:

  ABL-2a: Hybrid (v0.1 default)
    - Perceiver = transformer, Memory = SSM, Permanence = slot,
      Critic = small transformer head, Composer = param-free
    - This is the baseline / v0.1 architecture

  ABL-2b: Transformer-only
    - Perceiver = transformer (unchanged)
    - Memory = transformer with sliding-window attention replacing SSM
      (same parameter budget as SSM core; ~50-150M)
    - Permanence = transformer cross-attention over object tokens
      (replacing slot attention; same parameter budget)
    - Critic = small transformer head (unchanged)
    - Composer = param-free (unchanged)
    - Bus = unchanged

  ABL-2c: SSM-only
    - Perceiver = SSM-based encoder (Mamba-vision or similar;
      same parameter budget as transformer perceiver; ~300-700M)
    - Memory = SSM (unchanged)
    - Permanence = SSM with structured state for object slots
      (replacing slot attention; same parameter budget)
    - Critic = small SSM head (replacing small transformer head;
      same parameter budget)
    - Composer = param-free (unchanged)
    - Bus = unchanged

Expected if claim holds (survive):
  - ABL-2a (hybrid) outperforms both ABL-2b and ABL-2c on aggregate
    proxy metrics (weighted average of P1-P6).
  - Specifically: ABL-2c (SSM-only) should degrade on per-frame tasks
    (perception quality, P1 conflict detection) because SSM perception
    is not the dominant 3R paradigm. ABL-2b (transformer-only) should
    degrade on long-sequence tasks (P2 anchor retention, P3 memory
    growth) because O(N^2) attention over long sequences is either
    infeasible or requires heavy windowing that loses context.

Expected if claim fails (kill):
  - ABL-2b (transformer-only) matches hybrid on ALL proxy metrics.
    This would mean SSM-for-Memory is not needed; the substrate story
    collapses. The modular mapping (4 modules + bus) survives, but
    the claim that SSM is the right Memory substrate does not.
  - OR: ABL-2c (SSM-only) matches hybrid on ALL proxy metrics. This
    would mean transformer-for-perception is not needed (surprising
    given literature dominance); the substrate story collapses in
    the other direction.

Proxy metrics : P1, P2, P3 (primary); P4, P5, P6 (secondary)
                + per-frame pointmap quality (standard 3R benchmarks:
                absolute trajectory error, relative pose error,
                pointmap RMSE where available)

Priority      : HIGH. Second most important ablation. The substrate
                hypothesis is the second load-bearing claim after the
                bus.

Dependencies  : none (independent of ABL-1, can run in parallel)

Risk ref      : R1 (substrate hypothesis falsification at training time)
```

### ABL-3: State-ownership isolation (gradient-isolated vs. gradient-flowing)

```text
Target claim  : "state is owned by exactly one module; cross-spec reads
                are read-only; the ownership invariant is load-bearing"
                (architecture spec: state ownership section, invariant 1)

Ablation      : TWO variants compared:

  ABL-3a: Gradient-isolated (v0.1 default)
    - Every cross-spec bus read is wrapped in stop_gradient.
    - A consumer module cannot update a producer module's parameters
      via backward pass through a bus read.
    - Example: Critic reads latent_drift_proxy from Memory; the
      gradient from Critic's loss does NOT flow back into Memory's
      SSM parameters through that read.

  ABL-3b: Gradient-flowing
    - Cross-spec bus reads are NOT wrapped in stop_gradient.
    - Gradients flow freely across module boundaries.
    - This is the standard practice in most end-to-end trained
      multi-module systems.

Expected if claim holds (survive):
  - ABL-3a (gradient-isolated) produces per-module metrics that are
    individually interpretable. Each module's loss converges on its
    own terms. CR-5 evidence-label propagation is meaningful because
    each signal's confidence is not contaminated by cross-module
    gradient noise.
  - ABL-3b (gradient-flowing) may produce HIGHER aggregate
    performance but at the cost of interpretability: per-module
    attribution becomes noisy.

Expected if claim partially fails (nuance):
  - ABL-3b significantly outperforms ABL-3a on aggregate metrics.
    The ownership invariant is architecturally clean but hurts
    performance. v0.2 would need to decide: keep interpretability
    at a performance cost, or allow gradient flow and weaken the
    ownership story.

Expected if claim fully fails (kill):
  - ABL-3a performs WORSE on ALL per-module metrics AND aggregate.
    This would mean the ownership invariant is actively harmful,
    not just a performance tradeoff. The architecture story around
    "modules as independently falsifiable components" weakens.

Proxy metrics : P1-P6 (aggregate); per-module loss convergence curves;
                per-module metric attribution clarity

Priority      : HIGH. Third-priority ablation. The ownership invariant
                is architecturally elegant but empirically untested.

Dependencies  : should run AFTER ABL-1 (bus must be shown useful before
                testing gradient flow through it)

Risk ref      : R3 (state-ownership invariant violation under training)
```

---

## Tier 2: Per-module substrate ablations

### ABL-4: Critic removal

```text
Target claim  : "the Critic module (C4, A4 + A5 repair facet) is
                load-bearing for hard-case geometric ambiguity (F3)"

Ablation      : REMOVE Critic entirely. All inputs get single-pass
                output (no A4 verification, no A5 repair/reroute).
                Composer still routes inputs to models, but reroute
                never fires. The bus still exists but conflict_score
                and recommended_action are absent.

Expected if claim holds:
  - Full Dream3R outperforms Critic-removed on P1 (conflict detection
    drops to zero by definition) AND on downstream pointmap quality
    for hard cases (ambiguous geometry, repeated textures, symmetric
    scenes).

Expected if claim fails:
  - Removing Critic has no measurable effect on pointmap quality.
    This would mean verification and repair are not needed — the
    perception backbone is already good enough. The F3 failure
    mode would be a non-problem.

Proxy metrics : P1 (primary); pointmap quality on hard-case subset;
                P5 route regret (secondary, via Composer-only routing
                without Critic feedback)

Priority      : MEDIUM.

Dependencies  : ABL-1 must show bus is useful first.
```

### ABL-5: Memory removal (per-window only)

```text
Target claim  : "the Memory module (C2, A1 + A2 + A3) is load-bearing
                for long-context drift (F1)"

Ablation      : REMOVE Memory's persistent state. Each window is
                processed independently with no latent_state carry-over,
                no anchor set, no cache. Effectively, the model becomes
                a per-window system (like DUSt3R or MASt3R applied
                window-by-window with no memory).

Expected if claim holds:
  - Full Dream3R outperforms Memory-removed on P2 (anchor retention
    drops to zero by definition), P3 (memory growth is undefined),
    and on long-sequence pointmap consistency (drift across 100+
    frames).

Expected if claim fails:
  - Removing Memory has no measurable effect on long-sequence tasks.
    This would mean per-window perception is sufficient and the
    SSM-based memory is wasted computation. Unlikely given existing
    literature (Spann3R, CUT3R show memory helps), but must be
    verified for Dream3R's specific architecture.

Proxy metrics : P2 (primary); P3 (primary); long-sequence absolute
                trajectory error; per-window vs. accumulated pointmap
                consistency

Priority      : MEDIUM.

Dependencies  : ABL-1 must show bus is useful first.
```

### ABL-6: Permanence removal (static-only 3R)

```text
Target claim  : "the Permanence module (C3, A6) is load-bearing for
                dynamic-static entanglement (F2)"

Ablation      : REMOVE Permanence entirely. All regions are treated as
                static. No dynamic_ratio signal, no suppress_static_
                write handoff, no object_track_set. Memory writes all
                regions to the static map without filtering.

Expected if claim holds:
  - Full Dream3R outperforms Permanence-removed on P4 (dynamic
    pollution drops to worst-case by definition) and on pointmap
    quality in scenes with dynamic content (people, vehicles,
    moving objects). Static-only reconstruction is corrupted by
    dynamic content; Dream3R's Permanence prevents this.

Expected if claim fails:
  - Removing Permanence has no measurable effect on pointmap quality
    even in dynamic scenes. This would mean the dynamic-static
    split is not needed (unlikely given MonST3R / POMATO results),
    or that the perception backbone already handles dynamics
    implicitly.

Proxy metrics : P4 (primary); pointmap quality on dynamic-scene
                subset; static_map purity (fraction of static map
                entries that correspond to truly static geometry)

Priority      : MEDIUM.

Dependencies  : ABL-1 must show bus is useful first.
```

### ABL-7: Composer removal (default-model only)

```text
Target claim  : "the Composer module (C5, A5 routing facet) is
                load-bearing for fragmented model ecology (F6)"

Ablation      : REMOVE Composer. All inputs are routed to a single
                default model (e.g. DUSt3R or MASt3R). No regime
                classification, no capability_match, no route_
                recommendation. CR-1 becomes vacuous (no spread to
                check). Critic A5 reroute_model branch is always
                masked off.

Expected if claim holds:
  - Full Dream3R outperforms Composer-removed on P5 (route regret
    increases for the default-model-only variant because inputs
    are not matched to the best-fit model).
  - Specifically: inputs in the "streaming" or "dynamic_video"
    regime should suffer when forced through a static-pair model,
    and vice versa.

Expected if claim fails:
  - Removing Composer has no measurable effect. This would mean
    one model handles all regimes equally well (unlikely given
    the diversity of existing 3R models), or that Composer's
    regime classification does not capture the relevant variation.

Proxy metrics : P5 (primary); per-regime pointmap quality breakdown;
                route_regret delta between single-model and
                Composer-routed

Priority      : MEDIUM-LOW. Composer is parameter-free in v0.1, so
                removing it is architecturally cheap. But the F6
                claim (fragmented ecology) is a paper-level story
                that needs supporting evidence.

Dependencies  : ABL-1 must show bus is useful first.
```

---

## Tier 3: Interaction and sensitivity ablations

### ABL-8: Per-CR-rule ablation (individual gate removal)

```text
Target claim  : "each CR-rule (CR-1..CR-6) is individually
                meaningful"

Ablation      : SIX sub-ablations, one per CR-rule:

  ABL-8a: Remove CR-1 (Critic A5 reroute not gated by Composer spread)
    -> reroute_model can fire even when all models are equally matched
    -> measure: does reroute fire spuriously? does P5 route regret
       increase?

  ABL-8b: Remove CR-2 (suppress_static_write not binding on Memory)
    -> Memory can write dynamic regions to static map
    -> measure: does P4 dynamic pollution increase?

  ABL-8c: Remove CR-3 (latent_drift_proxy can gate Critic A4)
    -> Critic A4 score is influenced by Memory's drift estimate
    -> measure: does P1 false alarm rate change? does Critic become
       coupled to Memory failures?

  ABL-8d: Remove CR-4 (no tiebreak on capability ties)
    -> Critic A5 picks arbitrarily among tied models
    -> measure: does P5 route regret increase on cases where multiple
       models are similarly capable?

  ABL-8e: Remove CR-5 (no evidence-label propagation)
    -> modules can silently upgrade evidence labels
    -> measure: does interpretability degrade? does any metric change?
       (CR-5 is primarily an audit invariant; removing it may have no
       metric effect but weakens the trustworthiness story)

  ABL-8f: Remove CR-6 (no contract usage audit)
    -> no bookkeeping; no observable metric effect expected
    -> measure: confirm that removing CR-6 has zero metric effect
       (validates that CR-6 is purely an audit mechanism)

Expected outcomes:
  - CR-1 removal: moderate P5 degradation on mixed-regime benchmarks
  - CR-2 removal: significant P4 degradation on dynamic scenes
  - CR-3 removal: moderate P1 false-alarm-rate change
  - CR-4 removal: small P5 degradation (ties are rare in practice)
  - CR-5 removal: no metric change; interpretability degradation
  - CR-6 removal: no metric change (validates audit-only role)

Proxy metrics : P1, P4, P5 per sub-ablation

Priority      : LOW. Individual CR-rule effects are secondary to ABL-1
                (bus-as-a-whole). Run AFTER ABL-1 confirms bus value.

Dependencies  : ABL-1 must show bus is useful; these ablations refine
                which parts of the bus matter.
```

### ABL-9: Evidence signal subset ablation

```text
Target claim  : "the 17-signal evidence vector V1 is a useful
                combined representation; individual signals are
                not redundant"

Ablation      : systematic leave-one-out over the 17 V1 signals.
                For each signal, zero it out in T3 evidence tokens
                and measure effect on the consuming module's primary
                proxy metric.

                Signal groups (organized by primary consumer):

                Critic-consumed (A4 primary):
                  pose_novelty, view_overlap, reprojection_residual,
                  pointmap_conflict, confidence_drop,
                  model_capability_match, prior_rgb_conflict
                  -> measure: P1 conflict detection

                Memory-consumed (A1/A2/A3 primary):
                  pose_novelty, confidence_drop, latent_drift_proxy,
                  cache_pressure, anchor_importance,
                  external_memory_overlap, loop_candidate_score
                  -> measure: P2 anchor retention, P3 memory growth

                Permanence-consumed (A6 primary):
                  dynamic_ratio, optical_flow_conflict,
                  object_track_stability
                  -> measure: P4 dynamic pollution

                Composer-consumed:
                  model_capability_match, view_overlap, pose_novelty,
                  dynamic_ratio, blur_or_low_light_score
                  -> measure: P5 route regret

Expected outcomes:
  - Some signals are expected to be dominant for their consumer
    (e.g. reprojection_residual dominates P1; dynamic_ratio
    dominates P4). Removing these should cause measurable
    degradation.
  - Some signals may be redundant or weakly correlated with their
    metric. Identifying these informs V1 simplification in v0.2.

Proxy metrics : P1-P5, per-signal

Priority      : LOW. This is a refinement ablation.

Dependencies  : ABL-4, ABL-5, ABL-6 (per-module removal ablations
                establish module-level baselines first)
```

### ABL-10: Training loss weighting sensitivity

```text
Target claim  : "the multi-loss training objective (L_total) is
                robust to weight perturbation"

Ablation      : sweep the training loss weights w_* in the
                training-objective sketch:

                Sweep 1: dominant-loss baseline
                  w_pointmap = 1.0; all others = 0.0
                  (standard 3R training; no module-specific losses)

                Sweep 2: equal-weight
                  all w_* = 1.0 / N_losses

                Sweep 3: v0.1 inferred weights (baseline)
                  weights as specified in a future training config

                Sweep 4: per-module dominance
                  for each module loss, set that loss weight to 10x
                  others, measure whether one module dominates training

Expected outcomes:
  - Sweep 1 (pointmap-only) should train a functional 3R model but
    with poor module-specific behavior (Critic, Memory, Permanence
    heads are untrained).
  - Sweep 2 (equal-weight) may produce training instability if
    losses have different scales.
  - Sweep 3 (inferred) should produce balanced module training.
  - Sweep 4 (per-module dominance) should show each loss improving
    its own metric at the expense of others.

Proxy metrics : P1-P6 + training loss convergence + pointmap quality

Priority      : LOW. This is a training-time hyperparameter sweep.

Dependencies  : all Tier 1 ablations must establish that the
                architecture is worth training at all.
```

---

## Benchmark input selection for ablations

```text
The ablation plan requires benchmark inputs that exercise the
architectural claims. The following input categories are needed:

B1: Static pair (2 views, no motion, no dynamics)
    -> baseline case; most comparators handle this well
    -> purpose: sanity check that Dream3R does not regress on easy cases
    -> source: existing KYKT job 20260420-222729 (MASt3R static pair)
       or standard 3R benchmarks (ScanNet, ETH3D, DTU)

B2: Many-view static (10-50 views, no motion, no dynamics)
    -> exercises Memory A3 context budgeting
    -> purpose: test anchor retention (P2) and memory growth (P3)
    -> source: standard 3R benchmarks (ScanNet, Tanks & Temples,
       MipNeRF-360)

B3: Long dynamic video (100+ frames, moving objects)
    -> exercises Memory A1 state update + Permanence A6 dynamic split
    -> purpose: test long-context drift + dynamic pollution (P4)
    -> source: existing KYKT job 20260420-222928 (MonST3R 48-frame;
       extend to longer sequences); DAVIS, Sintel, TUM-RGBD
       dynamic sequences

B4: Mixed-regime batch (multiple inputs spanning different regimes)
    -> exercises Composer A5 routing
    -> purpose: test route regret (P5) across regime boundaries
    -> source: construct a batch mixing B1, B2, B3 inputs and
       measuring Composer's per-input regime classification and
       model routing decisions

B5: Hard-case geometric ambiguity (symmetric scenes, repeated
    textures, textureless surfaces, near-degenerate baselines)
    -> exercises Critic A4 verification + A5 repair
    -> purpose: test conflict detection (P1)
    -> source: ETH3D outdoor, Waymo Open (symmetric buildings),
       custom synthetic scenes

B6: Adversarial CR-rule-triggering inputs
    -> exercises bus gates specifically
    -> purpose: ensure CR-rules fire on SOME inputs (addresses R2)
    -> source: CONSTRUCT inputs designed to trigger each CR-rule:
       CR-1: inputs where all models are equally (in)capable
             (e.g. extreme blur where no model excels)
       CR-2: inputs with strong dynamic content in specific regions
       CR-3: inputs with high latent drift but no geometric conflict
       CR-4: inputs where top-2 models are within epsilon_tie
    -> note: adversarial inputs are NOT the primary benchmark;
       they verify that the bus is NOT inert

Open question (from architecture spec Q2): whether to rely on
existing KYKT job inputs (which may show low CR-rule firing) or
construct adversarial inputs. This plan recommends BOTH: primary
benchmarks (B1-B5) for performance metrics, adversarial inputs
(B6) for CR-rule firing verification.
```

---

## Ablation dependency graph

```text
                    ABL-1 (bus removal)
                        |
           +------+-----+------+------+
           |      |            |      |
        ABL-3  ABL-4       ABL-5   ABL-6   ABL-7
   (grad isolation) (Critic-)  (Memory-) (Perm-) (Comp-)
           |      |            |      |      |
           |      +-----+------+------+------+
           |            |
           |         ABL-8 (per-CR-rule)
           |            |
           |         ABL-9 (evidence signal subset)
           |            |
           +------+-----+
                  |
              ABL-10 (loss weighting)


ABL-2 (substrate hypothesis) is INDEPENDENT of ABL-1.
It can run in parallel with the entire ABL-1 subtree.

Read order:
  Phase 1 (parallel): ABL-1 + ABL-2
  Phase 2 (after ABL-1 passes): ABL-3, ABL-4, ABL-5, ABL-6, ABL-7
  Phase 3 (after Phase 2): ABL-8, ABL-9
  Phase 4 (after Phase 3): ABL-10
```

---

## Falsification summary table

| Ablation | Target claim | Kill condition | Architecture consequence if killed |
|---|---|---|---|
| ABL-1 | Bus is load-bearing | Flat baseline matches full Dream3R on 4+/6 metrics | Architecture collapses to "modular composition"; paper claim retreats |
| ABL-2 | Hybrid substrate is load-bearing | Single-substrate matches hybrid on all metrics | Substrate story collapses; modular mapping survives |
| ABL-3 | State ownership invariant is meaningful | Gradient-flowing dominates gradient-isolated on ALL metrics | Ownership invariant is harmful; v0.2 must allow gradient flow |
| ABL-4 | Critic is load-bearing for F3 | Removing Critic has no effect on hard cases | Critic module is unnecessary; architecture shrinks |
| ABL-5 | Memory is load-bearing for F1 | Removing Memory has no effect on long sequences | Memory module is unnecessary (contradicts existing 3R literature) |
| ABL-6 | Permanence is load-bearing for F2 | Removing Permanence has no effect on dynamic scenes | Permanence module is unnecessary (contradicts MonST3R et al.) |
| ABL-7 | Composer is load-bearing for F6 | Removing Composer has no effect on mixed-regime batches | Composer module is unnecessary; single-model suffices |
| ABL-8 | Individual CR-rules are meaningful | Specific CR-rule removal has no metric effect | That CR-rule is ceremonial, not functional |
| ABL-9 | V1 evidence signals are non-redundant | Many signals are redundant in leave-one-out | V1 can be simplified in v0.2 |
| ABL-10 | Multi-loss objective is robust | Training is unstable under weight perturbation | Loss weighting is fragile; needs careful tuning |

## Relationship to paper story

```text
The ablation plan maps to the paper structure as follows:

Paper Section 4 (Architecture):
  -> described by architecture spec SPEC-20260506-001

Paper Section 5 (Experiments):
  -> Tier 1 ablations (ABL-1, ABL-2, ABL-3) become the main
     experimental tables. These are the results a reviewer would
     look for first.

Paper Section 5.x (Ablation Studies):
  -> Tier 2 ablations (ABL-4..ABL-7) become ablation study tables.
     Standard per-module removal experiments.

Paper Supplementary:
  -> Tier 3 ablations (ABL-8..ABL-10) go in supplementary.
     Per-CR-rule, per-signal, and loss-weight sensitivity.

Paper Section 6 (Related Work):
  -> The comparator map (cycle 016 S4 deliverable) anchors related
     work. ABL-7 (Composer removal) directly tests the
     "fragmented ecology" related-work claim.

The ablation plan is designed so that the paper can be written
from the results: Tier 1 results in Section 5, Tier 2 in ablation
studies, Tier 3 in supplementary. If a Tier 1 ablation FAILS,
the paper claim must be revised before submission.
```

## Compute budget estimate (for future authorization)

```text
Each ablation requires training Dream3R (or a variant) and
evaluating on benchmarks B1-B6. Rough estimates:

  ABL-1: 2 training runs (full + flat baseline) x budget TBD
  ABL-2: 3 training runs (hybrid + transformer-only + SSM-only)
  ABL-3: 2 training runs (gradient-isolated + gradient-flowing)
  ABL-4: 1 training run (Critic-removed)
  ABL-5: 1 training run (Memory-removed)
  ABL-6: 1 training run (Permanence-removed)
  ABL-7: 1 training run (Composer-removed)
  ABL-8: 6 training runs (one per CR-rule removal)
  ABL-9: 17 training runs (one per V1 signal leave-one-out)
  ABL-10: 4+ training runs (loss weight sweeps)

  Total: ~38 training runs minimum

  If Dream3R (full model, ~400M-1B params inferred) trains in
  ~X GPU-hours per run (unknown; depends on dataset size and
  convergence), the total compute budget is ~38X GPU-hours.

  IMPORTANT: this estimate is for PLANNING ONLY. No training is
  authorized. The estimate informs future authorization decisions
  about compute allocation.
```

## Boundaries

```text
1. NO TRAINING. This plan specifies experiments; it does not
   authorize running them.

2. NO GPU RUNS. All descriptions are markdown-only.

3. NO CHECKPOINT CREATION. Even a randomly-initialized ablation
   variant would require training authorization.

4. NO BENCHMARK DOWNLOAD. Benchmark inputs (B1-B6) are described
   but not downloaded or processed.

5. NO KYKT NAVIGATION CHANGE. This file does not modify any KYKT
   app surface.

6. SCOPE: this plan covers the v0.1 architecture only. If v0.2
   changes the substrate hypothesis, the plan must be revised to
   match.
```

## Linked artifacts

- SPEC-20260506-001 (Dream3R architecture v0.1; parent spec; all ablation targets defined there)
- planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md (A1-A8 actions + V1 evidence vector + P1-P6 proxy metrics; ablation metrics defined there)
- paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md (v2.1 contract; CR-1..CR-6 rules that ABL-1 and ABL-8 target)
- planning/RESEARCH_GRAPH_AND_PAPER_START.md (F1-F6 failure modes; per-module ablations ABL-4..ABL-7 target these)

## Open questions

```text
Q1. Adversarial vs. natural CR-rule triggering (carried from
    architecture spec Q2): resolved in this plan as "both."
    Primary benchmarks for performance; adversarial B6 for
    CR-rule firing verification.

Q2. Should ABL-9 (leave-one-out over 17 V1 signals) use
    independently-trained models or fine-tuned from a common
    checkpoint? Independent training is clean but costs 17
    training runs. Fine-tuning is cheaper but may not fully
    surface signal importance due to residual learning from the
    common checkpoint.

Q3. If ABL-1 (bus removal) shows the bus is NOT useful, do we
    still run Tier 2 ablations? Recommended: NO. If the bus
    fails, the architecture needs fundamental revision before
    per-module ablations matter.

Q4. Minimum benchmark size for statistical significance: how
    many scenes / sequences per benchmark category (B1-B6) are
    needed to claim significance? Depends on effect size; likely
    50-100 scenes per category based on standard 3R evaluation
    practice.
```

## Version history

```text
v0.1  2026-05-06  cycle 016 S3 deliverable. First ablation plan for
                  Dream3R v0.1 architecture. 10 ablations in 3 tiers.
                  Falsification table for each architectural claim.
                  Benchmark input categories B1-B6 defined.
                  Dependency graph specified. No training authorized.

v0.2  2026-05-06  cycle 019 S2 deliverable; v0.2 lives in a NEW file
                  specs/SPEC-20260506-005-dream3r-ablation-plan-v02.md
                  (delta-only addendum; this v0.1 file body is NOT
                  rewritten per DEC-20260506-003 + Surgical Edits +
                  Honesty Override). v0.2 introduces nine numbered
                  ablations (ABL-v02-1..9) anchored to
                  SPEC-20260506-004 v0.2 architecture deltas: (1)
                  NSA-removal (Delta 3 + Delta 4; speculative);
                  (2) DINOv3 backbone tier -S/-B/-L (Delta 2;
                  paper-derived; extends v0.1 ABL-2); (3) frozen vs
                  partial-unfreeze (Delta 2; inferred);
                  (4) Composer best-of-N vs single-expert (Delta 5
                  + main-claim D; paper-derived; extends v0.1 ABL-7);
                  (5) capability_match measurement pass (Delta 5;
                  inferred -> measured-if-executed); (6) selection-
                  gate signal subsetting (Delta 3 + main-claim A;
                  speculative); (7) head training schedule (Delta 2;
                  inferred); (8) frame-budget benchmark (Delta 1;
                  inferred); (9) NSA kernel benefit decomposition
                  (Delta 4; inferred). Tier placement: ABL-v02-1+4+6
                  in Tier 1 (load-bearing); ABL-v02-2+3+7+8 in
                  Tier 2; ABL-v02-5+9 in Tier 3. Per-ABL review
                  checklist subsection added per user request
                  ("其他agent审阅修改") for other-agent handoff.
                  v0.1 ABL-1..ABL-10 remain canonical for v0.1
                  architecture testing; v0.2 ABLs cover surfaces
                  v0.1 does not address. Falsification mapping
                  table covers main-claim A + D + E (supporting).
                  Compute budget addendum: ~1237 GPU-hours total
                  across all 9 v0.2 ABLs (inferred on TITAN RTX).
                  No training authorized; markdown only; each
                  ABL-v02 execution requires fresh DEC + per-step
                  micro gates per F-002.
```
