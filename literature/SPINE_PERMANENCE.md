# SPINE_PERMANENCE: Dynamic Object Permanence / 4D Memory

Last updated: 2026-05-05 (cycle 013 refresh: Julian Ost AAAI-2026 driving permanence SRC-2026-010 added to Advanced Reading as driving-domain comparator; name-collision with Dream Permanence finalist deconfusion added to CRITICAL_NOTES.md)

Linked spec: `specs/SPEC-20260503-003-dynamic-object-permanence.md`

Linked finalist: Dynamic Object Permanence / 4D Memory

## One-Line Definition

A 3R policy that prevents dynamic regions from polluting the static map and preserves object identity across frames using existing dynamic-3R outputs (per-frame dynamic masks, confidence, optical flow), without 4DGS asset rendering.

Important: per SPEC-20260503-003 boundaries, 4DGS asset rendering is explicitly out of scope. The demo is timeline-based, not asset-based.

## Required Reading

These are the papers any Permanence case-card author must read before adding a `dynamic_ratio` or `object_track_set` line.

### SRC-2024-003 MonST3R (paper-proven)

What this paper actually claims: dynamic-video pointmap reconstruction; produces per-frame dynamic masks + confidence; trained on dynamic-aware loss.

What people often misread it as: a 4D memory paper. MonST3R produces per-frame dynamic outputs; it does not maintain object identity across the sequence. The cycle 009 PERMANENCE-01 case card uses MonST3R's 96-mask output as input, not as the comparator.

### SRC-2025-010 POMATO (paper-proven)

What this paper actually claims: pointmap matching plus temporal motion estimation; dynamic-aware token routing differs from MonST3R's dynamic-aware loss.

What people often misread it as: equivalent to D2USt3R. Both extend DUSt3R with dynamics, but POMATO trains on a dynamic-aware loss while D2USt3R uses dynamic-aware token routing. The mechanism is different.

### SRC-2025-011 D2USt3R (paper-proven)

What this paper actually claims: 4D pointmaps for dynamic scenes with dynamic-aware token routing.

What people often misread it as: a 4DGS variant. D2USt3R produces 4D pointmaps, not 4D Gaussian splats. The "4D" qualifier is about temporal coverage, not asset format.

### SRC-2025-013 Easi3R (paper-proven)

What this paper actually claims: training-free dynamic adaptation / motion separation; per-frame.

What people often misread it as: equivalent to MonST3R. Easi3R is training-free; it operates on top of an existing 3R model. MonST3R is trained with dynamic-aware loss. Computation budget differs.

### SRC-2026-008 RayMap3R (project + code claimed; paper-proven for the published claims)

What this paper actually claims: inference-time RayMap representation for dynamic streaming reconstruction.

What people often misread it as: a 4D Gaussian variant. RayMap3R uses ray-based representations for dynamics; not Gaussian splats.

## Advanced Reading

### 4DGS variants (cited; explicitly out of scope for Permanence)

4D Gaussian Splatting (CVPR 2024) and 4DGS in the Wild are demo-axis comparators. They produce visual assets; Permanence produces timeline decisions. Cite them in the related work to set the contrast, but do not let the case card drift into asset rendering. RU-005 (3R-to-4DGS Bridge) carries the asset path separately.

### SRC-2025-014 G-CUT3R (paper-proven; guided boundary)

Guided pointmap with depth / pose / calibration priors. Useful when Permanence needs a prior signal to disambiguate camera motion from object motion (Permanence reads, does not own).

### Visual prior comparators

- SRC-2024-012 SAM 2: video segmentation foundation model; if used, supplies dynamic mask priors at higher quality than MonST3R's masks.
- SRC-2023-003 CoTracker: long-video joint 2D point tracking; a stronger object-identity prior than per-frame matching.
- SRC-2024-013 SpatialTracker: 2D pixels in 3D space; V2 unifies track + depth + pose.

These are not required reading for cycle 009 case cards (MonST3R's existing 96 masks are sufficient), but they define the upgrade path for cycle 010+.

### SRC-2026-010 Julian Ost AAAI-2026 driving permanence (paper-proven for the driving-NVS domain)

Scene-graph driving generation with **explicit object permanence** + causal novel-view synthesis (driving domain). What it actually claims: in the autonomous-driving generative-NVS setting, representing each vehicle as a persistent object in a scene graph improves temporal consistency and causal plausibility of generated views.

What people often misread it as: the same "object permanence" concept that Dream SPEC-20260503-003 owns. **The name collides; the scope does not.** Julian Ost's paper operates in the driving-NVS *generative* pipeline where object identity is maintained *inside a scene graph for synthesis*; Dream Permanence operates on MonST3R's dynamic-mask outputs and owns the `suppress_static_write(r)` handoff to Memory. The shared phrase "object permanence" names two different contributions in two different pipelines. See `CRITICAL_NOTES.md` for the deconfusion.

Cite as a *positioning* anchor in the related-work section (driving-domain peer that also uses the term), not as a Permanence comparator. Do not fold its metrics into `identity_consistency` proxy evaluation.

## Skip With Reason

- 4DGS variants for asset rendering: out of scope per SPEC-003.
- robotics-stack 4D papers: not relevant to Permanence's L2 path; Permanence is offline post-processing of existing MonST3R outputs.
- pure object-detection papers without 3R framing: do not borrow detection metrics into Permanence's identity_consistency proxy.

## Cross-Paper Disagreement

- **MonST3R (dynamic-aware loss) vs POMATO (dynamic-aware loss with different target) vs D2USt3R (dynamic-aware token routing)**: three different mechanisms for similar goals. The dynamic-3R field is not consolidated. Permanence's contribution is *orthogonal* (object identity + static immunity), not a fourth dynamic-3R training trick.
- **Easi3R (training-free, per-frame) vs MonST3R (trained, sequence-aware)**: different cost / capability tradeoffs. Permanence reads either as input; the policy is the contribution.
- **RayMap3R representation vs pointmap representation**: rays vs points. The representation choice affects what evidence signals are available; Permanence assumes pointmap-style outputs (because that is what the existing KYKT MonST3R job provides).

## Interface To SPEC-20260503-003

- Permanence A6 reads MonST3R's 96 dynamic masks + 96 confidence arrays from KYKT job 20260420-222928.
- The `pollution_score` metric is anchored against the no-policy baseline (write everything with nonzero confidence).
- The `identity_consistency` metric is hand-labeled across at least 8 of 48 frames within 90-120 minutes per case card per cycle 008 D4.
- Cross-spec writes (per `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md`): Permanence emits `suppress_static_write(r)` and `admit_static_write(r)` as handoffs to Memory. Memory must honor or log refusal per CR-2.
- The static-control case (PERMANENCE-02) uses MASt3R static pair (KYKT job 20260420-222729) to verify GEM-3R does not hallucinate motion.

## Evidence Labels Summary

- MonST3R, POMATO, D2USt3R, Easi3R, RayMap3R: paper-proven for their published dynamic-3R claims.
- Julian Ost AAAI-2026 driving permanence: paper-proven for the driving-NVS domain; cited as positioning anchor only, NOT as Permanence comparator (see CRITICAL_NOTES.md).
- Object permanence + static-map immunity policy as a single contribution: inferred.
- theta_dynamic, theta_static, theta_flow, dynamic_horizon, mint_rate: inferred.
