# SPEC-20260527-001 — Dream3R state-conditioned reconstruction addendum

spec_id: SPEC-20260527-001
date: 2026-05-27
status: architecture addendum; candidate-not-final
scope: post-midterm Dream3R architecture direction
decision_anchor: DEC-20260527-009-state-conditioned-reconstruction-pivot
supersedes: SPEC-20260506-004 Delta 6 pillar D as the headline claim only
does_not_supersede: SPEC-20260506-001, SPEC-20260522-001, v0.3/v0.4 code

## Context

Dream3R v0.2 narrowed the main claim to:

```text
A. Verification-as-architecture
D. Heterogeneous best-of-N Composer
```

The 2026-05-25 to 2026-05-27 evidence makes that framing too narrow for
the research goal.

- DEC-007 shows that expert routing is learnable on KITTI and ETH3D, but
  its quality gain is domain-dependent and bounded by the fixed expert pool.
- DEC-008 shows that Critic -> Router reroute is wired but does not add
  value at the current data scale.
- MIDTERM §3 shows the decisive architectural gap: `V04Pipeline`'s final
  depth equals one selected expert's standalone `pointmap`; Memory,
  AnchorBank, NSA, Permanence, and Critic state are emitted but do not
  directly condition the final reconstruction.
- Stage 6 exposes the right missing wire, but the first cache surfaced an
  adapter-loading pathology: `build_dream3r("small_real")` can register
  adapters without calling `adapter.load_checkpoint()`.

The resulting lesson is not "the router failed". The lesson is that hard
expert selection is a control-plane probe, not a reconstruction-plane
architecture.

## Revised architectural claim

Dream3R's post-midterm architecture should be:

```text
state-conditioned reconstruction
```

The final pointmap must be a function of:

```text
current images
+ expert proposal pointmaps/confidences
+ persistent Memory / AnchorBank / NSA state
+ Permanence dynamic/static state
+ Critic and geometric conflict signals
+ Composer prior
-> final pointmap + confidence + correction/reliability maps
```

Composer remains useful, but its role changes:

```text
old role: final hard selector of one expert
new role: proposal prior / regime probe / diagnostic baseline
```

This addendum demotes "best-of-N Composer" from the headline research
claim to a baseline and input signal. It does not delete Composer, DEC-007,
or the expert-pool work. It changes what those pieces are for.

## Optimized architecture

### Stage S1. Perception backbone

Input images are still encoded by the active perception backbone. This
stage publishes image tokens, pointmap proposals where available, and
low-level evidence signals.

Evidence label: code-observed for current ONNX/DINOv3 path; not changed
by this addendum.

### Stage S2. Persistent state

Memory, AnchorBank, and NSA own long-sequence state:

- `memory.fused_context`
- selected anchor statistics
- anchor reuse / stability signals
- NSA compressed / selected / sliding branch weights
- latent drift proxies

The key change is downstream use: these signals must condition the final
pointmap path, not only logs or routing decisions.

### Stage S3. Expert proposal bank

Experts produce candidate geometry proposals. The architecture no longer
treats expert dispatch as mutually exclusive by default.

Minimum proposal bank:

```text
fast3r pointmap + confidence
mast3r pointmap + confidence
spann3r pointmap + confidence
```

Cost-aware execution is allowed. For expensive experts, Composer can rank
which proposals to run first, but any "single selected expert" result is a
baseline, not the final architecture claim.

### Stage S4. Conflict and reliability estimation

Critic and deterministic geometry produce reliability evidence:

- conflict score
- sampson distance
- depth inconsistency
- confidence drop
- cross-window disagreement
- dynamic/static mask evidence

The output is not primarily "reroute". The output is a reliability field
that tells the fusion/correction module where to trust, downweight, or
repair proposals.

### Stage S5. State-conditioned fusion and correction

This is the new load-bearing reconstruction plane.

Inputs:

```text
proposal_pointmaps      [B, E, N, P, 3]
proposal_confidences    [B, E, N, P, 1]
memory_context          [B, D]
anchor_state_summary    [B, K or D_a]
nsa_state_summary       [B, D_n]
critic_conflict         [B, 1 or N,P,1]
geometry_features       [B, E or E,E, ...]
composer_prior          [B, E]
```

Outputs:

```text
final_pointmap          [B, N, P, 3]
final_confidence        [B, N, P, 1]
proposal_weights        [B, E, N, P] or [B, E]
residual_delta          [B, N, P, 3]
correction_mask         [B, N, P, 1]
```

Allowed minimal forms:

1. Single-expert residual correction, using one expert plus state.
2. Multi-expert soft fusion, using all cached expert outputs.
3. Reliability-weighted fusion, where Critic/geometric signals generate
   weights and optional residuals.
4. Temporal-coherence fusion, where the correction is trained or evaluated
   on cross-window stability, not only per-window abs_rel.

### Stage S6. Long-sequence objective and evaluation

Abs_rel remains necessary but no longer sufficient. Dream3R's state claim
requires long-sequence metrics:

- scale drift proxy
- temporal point stability
- cross-window consistency
- anchor reuse / anchor survival
- correction mask sparsity and locality
- conflict reduction before/after fusion

## New architecture axes

This addendum adds three post-v0.5 candidate axes. They do not close any
axis by themselves.

### Axis A9. Real-backend guardrail for state-to-depth experiments

`closes_iff`:

1. Every cache-building script that claims a real expert baseline either
   calls `adapter.load_checkpoint()` or asserts `adapter.is_loaded`.
2. A smoke script fails fast if a `small_real` path emits fallback backend
   status for the measured expert.
3. The cache records backend status per entry.

Does_not_promise: better depth quality. This axis protects experimental
validity only.

### Axis A10. Multi-expert proposal bank

`closes_iff`:

1. Cache format stores all available expert pointmaps/confidences per
   window, not only `selected_expert`.
2. Fusion training can compare hard routing, soft fusion, and oracle
   fusion on the same held-out split.
3. Composer prior is available as an input feature but is not the final
   selector.

Does_not_promise: that soft fusion beats the best single expert.

### Axis A11. Long-sequence state objective

`closes_iff`:

1. At least one temporal/coherence metric is computed on held-out long
   windows.
2. The Stage S5 head is evaluated on abs_rel and at least one coherence
   metric.
3. The cycle log states whether state improves depth, coherence, both, or
   neither.

Does_not_promise: that current Memory state is already depth-informative.

## Experimental ladder

### L0. Fix experimental truthfulness

Patch cache-building paths so real expert baselines are real. This is the
first required step before interpreting Stage 6 numbers.

### L1. Single-expert state-to-depth wire

Use the existing `Stage6FusionHead` as the smallest state-conditioned
reconstruction probe:

```text
selected expert pointmap + memory.fused_context + conflict_score
-> residual correction
```

Verdict:

- positive: current state already carries usable depth-correction signal.
- null: the wire is correct, but state is not depth-informative enough.
- negative: naive residual correction damages strong expert output.

### L2. Multi-expert soft fusion

Cache all expert outputs and train a head that can weight or fuse them.
This is the first architecture that moves beyond hard expert selection.

### L3. Reliability and temporal objectives

Add geometry reliability features and long-sequence coherence metrics.
This tests the Dream3R claim more directly than per-window abs_rel.

### L4. State representation retraining

Only if L1/L2 show null or weak signal: retrain Memory/Anchor state with a
depth/coherence-aware objective. This likely needs a separate DEC because
it may touch core modules or training assumptions.

## Relationship to prior specs

- SPEC-20260506-001 remains the historical control-graph architecture.
- SPEC-20260506-004 Delta 6 is partially superseded: pillar D is demoted
  from headline claim to baseline/proposal-prior role.
- SPEC-20260522-001 remains valid for A1-A8. A9-A11 are additive axes
  created by the Stage 6 structural finding.
- DEC-007 remains valid evidence that routing signals exist.
- DEC-008 remains valid negative evidence that reroute is not enough.

## Midterm wording

Use this claim for the 2026-05-30 midterm:

```text
Dream3R's first implementation validated the routing-side control plane,
but also exposed its ceiling: final depth was still a selected expert's
standalone pointmap. The post-midterm architecture therefore pivots from
hard expert selection to state-conditioned reconstruction, where persistent
Memory/Anchor/NSA state and Critic/geometric reliability directly condition
the final pointmap.
```

## Non-claims

- This addendum does not claim Stage 6 has improved real-expert depth.
- This addendum does not authorize core code edits.
- This addendum does not authorize training beyond the already approved
  Stage 6 rerun path.
- This addendum does not discard Composer; it repositions Composer.
- This addendum does not finalize Dream3R as the thesis.

