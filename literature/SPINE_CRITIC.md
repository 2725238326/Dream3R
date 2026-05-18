# SPINE_CRITIC: Geometry Critic / System-2 3R

Last updated: 2026-05-05 (cycle 013 refresh: tttLRM SRC-2026-011 added to Advanced Reading as long-context successor that extends the Test3R / TTT3R axis)

Linked spec: `specs/SPEC-20260503-001-geometry-critic.md`

Linked finalist: Geometry Critic / System-2 3R

## One-Line Definition

A 3R system that runs a verify-then-act loop on per-window output, scoring conflict over an evidence vector, then triggering one of {accept, rerun_local_region, reroute_model, open_anchor_budget, request_prior, conflict_unresolved} as a downstream action.

Important: the Critic finalist owns A4 (verify) and A5 (repair facet of repair/reroute). The reroute facet of A5 is owned by Composer SPEC-20260504-001. See `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` for the formal split.

## Required Reading

These are the papers any Critic case-card author must read before adding a `conflict_score` line.

### SRC-2025-007 Test3R (paper-proven)

What this paper actually claims: in-family test-time geometric self-check on DUSt3R/MASt3R outputs using consistency between predicted views; demonstrates that consistency residuals correlate with reconstruction error in a single model family.

What people often misread it as: "test-time training works for 3R". Test3R does not train at test time; it scores consistency. TTT3R (below) is the train-at-test-time variant.

### SRC-2025-004 TTT3R (paper-proven)

What this paper actually claims: lightweight test-time training (state update rule for CUT3R) targeted at hard cases; demonstrates that small state updates at inference time can move CUT3R outputs.

What people often misread it as: same as Test3R. The compute scope and update target are different. TTT3R updates internal state; Test3R does not.

### SRC-2025-008 CTRL (paper-proven for the LM domain; inferred when borrowed for 3R)

What this paper actually claims: critic-revision via an RL-trained critic in the language-model domain; the critic-then-revise pattern is the borrowable structure.

What people often misread it as: a 3R-ready System-2 module. CTRL is not 3R; the action vocabulary, evidence signals, and revision targets are language-specific. Dream uses the *pattern*, not the implementation.

### SRC-2024-009 MASt3R-SfM (paper-proven)

What this paper actually claims: matching + retrieval + global SfM alignment on MASt3R features; classical SfM-stage refinement that already does a form of consistency check.

What people often misread it as: a baseline Critic. MASt3R-SfM verifies via classical pipeline, not on per-window evidence vector. Dream Critic verifies *before* SfM-stage refinement.

## Advanced Reading

These are useful for second-round case-card authoring or paper-grade positioning.

### SRC-2025-014 G-CUT3R (paper-proven for guided priors; inferred for prior-conflict logic)

Guided pointmap with depth / pose / calibration priors. Critic's `prior_rgb_conflict` signal is informed by G-CUT3R's prior-handling behavior, but the conflict-detection action is Dream's, not G-CUT3R's.

### SRC-2024-010 SLAM3R (paper-proven)

Sliding-window SLAM as a consistency-loop comparator. SLAM3R does loop-closure-style consistency over a window; Critic does per-window, pre-SfM consistency. Both are useful in cycle 009 case-card 03 context.

### SRC-2025-005 MV-DUSt3R+ (paper-proven)

Sparse-view multiview reconstruction. Useful as a counter-example: not every Critic action set applies; sparse-view inputs have different conflict-signal saturation than streaming inputs.

### SRC-2025-013 Easi3R (paper-proven; counter-example)

Training-free dynamic correction. Easi3R operates per-frame on dynamic regions; it is not a Critic. Listing here as a counter-example to clarify Critic's scope: Critic is per-window cross-model verification, not per-frame dynamic correction.

### SRC-2026-011 tttLRM (paper-proven)

Test-time training for long-context autoregressive 3D reconstruction. What it actually claims: scaling the TTT3R idea from CUT3R-scale state to long-context 3D reconstructor state; TTT is the repair mechanism, not the verification mechanism.

What people often misread it as: a long-context Test3R. tttLRM does update state at test time (TTT3R side), whereas Test3R scores consistency without state update. Placed in Advanced Reading because it strengthens the Test3R-vs-TTT3R disagreement axis at a new compute scale, but does not change Critic SPEC-20260503-001's Test3R-side scope decision (Critic still does not update state at verify time).

Cross-note: tttLRM also surfaces in SPINE_MEMORY because the mechanism lives in A1 (state update) under Memory; Critic reads the *evidence residuals* tttLRM computes, not the update itself.

## Skip With Reason

- 4DGS variants: out of scope for Critic; Critic does not own visual asset generation. Demo paths through 4DGS are explicitly excluded by SPEC-20260503-003 and not relevant here.
- VLM/reasoning-style verifier work: relevant to the *idea* of System-2 3R, but Dream Critic uses geometry signals, not language reasoning. Skip unless adding a CRITICAL_NOTES.md deconfusion.

## Cross-Paper Disagreement

- **Test3R vs TTT3R on test-time scope**: Test3R uses inference-only consistency; TTT3R updates state. As of cycle 008.5 it is not settled which approach is preferable for cross-model verification. Critic SPEC explicitly takes the Test3R-side scope (no state update at verify time) but does not claim TTT3R is wrong.
- **MASt3R-SfM vs Test3R on verification stage**: classical SfM vs per-window evidence vector. Both detect inconsistency; their failure modes differ. Critic takes the per-window route because it composes with Composer's regime card.
- **CTRL applicability to 3R**: this is `inferred`. The pattern transfers; the implementation does not. Treat CTRL citations carefully when writing the related-work section.

## Interface To SPEC-20260503-001

- Critic A4 (verify) reads the evidence signal vector defined in `planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md`. The signals come from Test3R-style consistency residuals (paper-proven), TTT3R-style state-difference signals (paper-proven), and Dream-defined cross-model signals (`inferred`).
- Critic A5 repair facet borrows the critic-revision pattern from CTRL (`inferred`).
- Critic A5 reroute facet binds to Composer's `route_recommendation` per `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` rule CR-1.
- P1 conflict_detection metric is anchored against Test3R-style residual labels.
- P5 route_regret metric uses Composer capability_match; not present in Test3R or TTT3R individually.

## Evidence Labels Summary

- Test3R, TTT3R, CTRL, MASt3R-SfM, G-CUT3R, SLAM3R, MV-DUSt3R+, Easi3R, tttLRM: paper-proven for their published claims.
- Cross-model A5 reroute action set: inferred.
- Critic case-card thresholds (theta_conflict, repair_budget): inferred.
