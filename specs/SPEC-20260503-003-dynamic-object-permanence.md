# SPEC-20260503-003 Dynamic Object Permanence / 4D Memory

## Identity

spec_id: SPEC-20260503-003

branch_name:

```text
Dynamic Object Permanence / 4D Memory
```

date: 2026-05-03

status: draft (pending L2 case-card evidence in cycle 009)

cycle_of_origin: CYCLE-20260503-002

## Approval

user_approval_for_branch: yes

approval_decision_id: DEC-20260503-002

approval_note:

```text
User approved option B explicitly to add Dynamic Object Permanence as the
third finalist (alongside Critic and Memory). This spec is therefore the
"+1 cycle cost" deliverable the user accepted. It does NOT promote
Permanence to final thesis; that gate is still open.
```

## Failure Modes

primary_failure_mode: F2 Dynamic-Static Entanglement

secondary_failure_modes:

- F1 Long-Context Drift / Forgetting (when dynamic regions corrupt the static map and induce drift)
- F3 Hard-Case Geometric Ambiguity (when motion fields conflict with pose / depth)

failure_mode_evidence:

- `planning/RESEARCH_GRAPH_AND_PAPER_START.md` rows F2, F1, F3
- F2 source mechanisms paper-proven across MonST3R / POMATO / D^2USt3R / Easi3R / RayMap3R; the Dream-specific *object permanence policy* over them is `inferred`.

## Owned Actions

owned_actions:

- A6 Dynamic / Object State Separation

support_actions:

- A2 Spatial Memory Governance (read-only into Memory spec; Permanence emits "do not write this region" signals, Memory spec applies them)
- A4 Geometry Verification (read-only into Critic spec; Permanence reads conflict_score for hard motion cases)
- A7 Prior / Modality Arbitration (read-only into future Cross-Modal spec; Permanence reads prior signals if available)

action_ownership_justification:

```text
Discipline rule 2 caps owned actions at <=3 and prefers the smallest set.
Permanence owns exactly one action because A6 is the discriminative axis:
the dynamic/static split + object-identity preservation is what
distinguishes this branch from Memory and Critic. A2 and A4 are explicitly
NOT owned here, which keeps Memory and Critic free to do their own work
without policy collisions.
```

## Comparator Set

comparator_anchors:

- MonST3R (dynamic 4D pointmap)
- POMATO (dynamic pointmap)
- D^2USt3R (dynamic-aware DUSt3R)
- Easi3R (training-free dynamic correction)
- RayMap3R (ray-based dynamic 3R)
- 4DGS variants (4D Gaussian Splatting; demo / asset path)
- G-CUT3R (guided-prior boundary; relevant when prior helps separate motion)

closest_comparator: MonST3R + Easi3R combined

weakest_comparator_pressure:

```text
Dynamic 3R already has multiple strong submissions. Dream cannot claim
novelty on dynamic pointmap output. The novelty must live in (a) a
preservation-of-object-identity-over-time signal that none of the
comparators report end-to-end, and (b) a policy that prevents dynamic
writes from polluting static memory across long sequences. If neither
shows up in the case cards, the branch collapses into a generic dynamic
reconstruction.
```

novelty_gap_against_comparators:

- MonST3R / POMATO / D^2USt3R produce dynamic pointmaps but do not maintain object identity across the sequence as a first-class output.
- Easi3R offers training-free dynamic correction but operates per-frame, not as a persistent identity track.
- 4DGS variants build asset-quality dynamic representations but are graphics-tooled, not memory-tooled.
- The comparison axis the paper would emphasize: *object identity persistence + static-map immunity*, not *better dynamic pointmap*.

## Core Claim

claim_paragraph:

```text
Dynamic 3R should not be measured only by per-frame motion accuracy. It
should be measured by whether (a) moving regions are kept out of the
long-term static map, and (b) object instances retain identity across
frames even when their motion is hard. The Dream contribution is the
pair: a static-pollution policy plus an identity-consistency proxy, both
operable on existing dynamic-3R outputs without retraining.
```

one_line_thesis:

```text
Dynamic 3R must remember objects, not just motion fields.
```

## Mechanism Pseudocode

inputs:

- per-frame 3R outputs from a dynamic-aware comparator (preferred: MonST3R job 20260420-222928, with 96 dynamic masks + 96 confidence arrays)
- evidence signal vector `e` from `ACTION_TAXONOMY_AND_PROXY_METRICS.md`
- optional: external object-detection / segmentation labels (cycle 009 uses manual labels; no detector required)

state_variables:

- `static_map(t)`: aggregated static-only memory (pointer into Memory spec store; Permanence does not own the store)
- `object_track_set(t)`: set of `{object_id, last_seen_t, last_position, identity_confidence}` records
- `dynamic_field(t)`: current short-horizon motion field; eviction-eligible after fixed horizon
- `pollution_log(t)`: append-only log of `{frame, region, suppressed_or_admitted, reason}` for each dynamic candidate

trigger_conditions:

- A6 runs every frame (or every input window). It is cheap; it operates on already-produced dynamic masks + confidence + flow.
- The split decision can be made independently per region; it does not require sequence-end batch processing.

action_logic:

```text
on each frame t:

  signals = read(e, dynamic_mask_t, confidence_t, optical_flow_t,
                 critic_signals, memory_signals)

  for each candidate region r in frame t:

    if signals.dynamic_ratio(r) > theta_dynamic
       OR signals.optical_flow_conflict(r) > theta_flow:
        # do NOT write to static_map
        emit suppress_static_write(r); log to pollution_log
        # try to assign to existing object track
        match = assign_to_object_track(r, object_track_set(t-1))
        if match:
          update object_track_set with {match.id, t, r.position, conf}
        else:
          new_id = mint_object_id()
          object_track_set add {new_id, t, r.position, conf}
        update dynamic_field(t)

    elif signals.dynamic_ratio(r) < theta_static
         AND signals.object_track_stability(r) is high:
        # safe static write (handed back to Memory spec write pipeline)
        emit admit_static_write(r); log to pollution_log

    else:
        # ambiguous; defer
        emit defer(r); next-window decision

  evict dynamic_field entries older than dynamic_horizon
```

output_artifacts:

- per-frame split decisions: `{region, decision, reason}`
- per-job pollution timeline: aggregate of pollution_log
- per-job object-track table: `{object_id, frames_visible, identity_breaks, identity_confidence_min}`

## Evidence Signal Vector Used

active_signals:

- dynamic_ratio
- optical_flow_conflict
- object_track_stability
- pose_novelty (read; needed to disambiguate camera motion from object motion)
- view_overlap (read)

inactive_signals (held by other specs):

- pointmap_conflict (held by Critic A4; Permanence reads only)
- reprojection_residual (held by Critic A4; Permanence reads only)
- confidence_drop (held by Memory A1)
- latent_drift_proxy (held by Memory A1)
- loop_candidate_score (held by Memory A2)
- anchor_importance (held by Memory A3)
- cache_pressure (held by Memory A3)
- prior_rgb_conflict (held by future Cross-Modal A7)
- model_capability_match (held by Critic A5 / future Composer)
- uncertainty_area (held by future Active Perception A8)

derived_signals:

- pollution_score (per-region; weighted sum of dynamic_ratio + optical_flow_conflict)
- identity_break_score (per object; weighted sum of frame gaps + position jumps + confidence drops)

## Action Policy Definition

| Action | Trigger condition | Scope of effect | Failure-aware fallback |
|---|---|---|---|
| A6 suppress_static_write | pollution_score(r) > theta_pollution | dynamic region r is excluded from static_map; Memory spec must honor the suppress flag | if Memory spec ignores the flag (cross-spec contract violation), surface to Advisor; do not silently retry |
| A6 admit_static_write | pollution_score(r) low AND object_track_stability(r) high | hand region r back to Memory spec write pipeline | if Memory rejects (e.g. duplicate), accept rejection and stop |
| A6 mint_object_id | unmatched dynamic region in frame t | new entry in object_track_set | if mint_rate exceeds budget per frame, log overflow and merge into a "noise" track rather than minting indefinitely |
| A6 update_object_track | dynamic region matches existing object by position + flow consistency | extend existing object_track entry to frame t | if match ambiguous (>1 candidate), defer to next frame; do not pick blindly |
| A6 defer | ambiguous pollution_score on borderline region | hold in dynamic_field for one window | if defer never resolves within `dynamic_horizon`, default to suppress_static_write (safer than polluting) |

## Proxy Validation Plan

primary_proxy: P4 dynamic pollution

secondary_proxy: identity_consistency (defined in `ACTION_TAXONOMY_AND_PROXY_METRICS.md` P4 protocol)

case_cards_to_fill:

```text
CASE-20260504-PERMANENCE-01  on 20260420-222928 (MonST3R 48-frame; 96 dynamic
                              masks + 96 confidence arrays; primary L2 case)
CASE-20260504-PERMANENCE-02  on 20260420-222729 (MASt3R static pair; static
                              control; expect zero pollution and no objects)
CASE-20260504-PERMANENCE-03  synthetic / public dynamic example with labeled
                              object identity over a short clip (used to
                              validate identity_consistency before relying
                              on it in 01)
```

acceptance_threshold:

```text
On the labeled L2 cases:
  P4 dynamic_pollution(GEM-3R policy) <= dynamic_pollution(no-policy baseline)
      where the no-policy baseline writes everything that has nonzero
      confidence regardless of dynamic mask
  AND P4 static_preservation(GEM-3R) >= static_preservation(no-policy)
  AND identity_consistency on the MonST3R 48-frame job is computable for
      at least one moving object across at least 8 frames within 120
      minutes of human annotation effort per cycle 008 D4
  AND CASE-PERMANENCE-02 confirms the static control: GEM-3R does NOT
      generate object tracks on a fully static pair (i.e. the controller
      is not hallucinating motion).
```

fail_fast_threshold:

```text
If after the cycle 009 case cards:
  identity_consistency cannot be labeled within 120 minutes of human
      effort per cycle 008 D4 on the MonST3R 48-frame job (annotation
      cost ceiling exceeded)
  OR GEM-3R policy fails to reduce dynamic_pollution vs the no-policy
      baseline on case 01
  OR case 02 (static control) shows GEM-3R minting object tracks where
      none exist (hallucinated motion)
then retire Permanence spec back to "close reserve" and re-allocate cycle
010 budget. Do not redraft to keep alive.
```

writing_value_if_only_negative_result:

```text
A clean negative is paper-relevant: it shows that signal-vector
permanence on existing dynamic-3R outputs is insufficient for object-level
identity preservation, and motivates either richer signals (segmentation
+ tracking heads) or a learned identity head. Negative result documented
via pollution timeline + object-track table is acceptable cycle 009 output.
```

## Teacher Demo Form

what_is_visible:

```text
Single MonST3R 48-frame timeline panel with three layers:

  Layer 1: original frames with dynamic mask overlay (already in the job)
  Layer 2: per-frame static/dynamic decision strip (color-coded admit /
           suppress / defer)
  Layer 3: object-track ribbons across frames; each object_id is a colored
           horizontal bar whose breaks indicate identity loss

Side-by-side: same 48-frame timeline rendered under "no-policy" baseline
that writes everything with nonzero confidence, so the static-pollution
divergence is visible.
```

why_it_surprises_a_teacher:

```text
The teacher sees a dynamic 3R model that "remembers objects" - the same
object identity persists across the timeline even when motion is hard,
and dynamic regions are visibly kept out of the static map. Most published
dynamic 3R demos show only better per-frame reconstruction.
```

artifact_format:

- markdown report with timeline image references plus pollution + identity tables
- no live model inference; everything is offline post-processing of MonST3R job 20260420-222928 + 96 dynamic masks
- 4DGS-style asset rendering is explicitly out of scope; the demo is timeline-based, not asset-based

approval_required_for_demo: yes

## KYKT Integration Surface

surface_list:

- research_lane (permanence timeline as research artifact)
- advisor_report (per-job permanence summary attaches to Advisor output)

NOT in scope this spec:

- runner (no runner change; Permanence post-processes existing MonST3R outputs + masks)
- sample_matrix (no scoring change)
- system_readiness (no system change)
- KYKT navigation change (still approval-gated)
- 4DGS asset surface (explicitly excluded; demo is timeline-only)

backend_contract_needed:

```text
Read-only access to existing MonST3R job artifacts under model_uploads/,
including the 96 dynamic masks and 96 confidence arrays. No new backend
service. No detector / tracker model. No training.
```

frontend_handoff_needed: no

frontend_handoff_brief_id: not_applicable_yet

## Engineering Cost

L1_design_cost: low

```text
This spec plus three case cards in cycle 009. ~5-7 hours of synthesis work.
Annotation budget per case card: 90-120 minutes per cycle 008 D4. The
120-minute ceiling is the hard fail-fast condition per cycle 008 D4; if
annotation overruns it, the spec retires.
```

L2_proxy_cost: medium

```text
Higher than Critic and on par with Memory. The 96 dynamic masks already
exist on disk. Object-identity labels must be hand-drawn for at least one
moving object across at least 8 of the 48 frames; this is the most
labor-intensive piece of the case card.
```

L3_prototype_cost: blocked_until_approval

L4_model_change_cost: blocked_until_approval

## Risks

novelty_risk:

```text
MonST3R / POMATO / D^2USt3R already publish dynamic pointmaps. Dream's
contribution is identity persistence + static-map immunity, not motion
estimation. If the case cards do not produce a clean identity track on
even one moving object, the novelty story collapses into "we re-rendered
MonST3R with masks".
```

overlap_with_comparator:

```text
Direct overlap with Easi3R on training-free dynamic correction. Mitigated
by holding the persistent object_track_set across frames, which Easi3R
does not.
```

engineering_risk:

```text
Low at L1/L2. Annotation cost is the dominant risk, capped by the
120-minute fail-fast threshold per cycle 008 D4.
```

demo_risk:

```text
The 4DGS visual is more impressive than a timeline. Mitigated by an
explicit out-of-scope note: 4DGS asset rendering is forbidden in this
spec. If the timeline demo is judged unimpressive, the response is to
retire the spec, not to add 4DGS.
```

paper_writing_risk:

```text
"Object permanence" is rhetorically strong but psychology-loaded. The
paper claim must shift to a measurable identity_consistency + static
pollution story to avoid being read as borrowing terminology without
substance.
```

## Evidence Labels

mechanism_status: inferred

```text
Dynamic / static separation is paper-proven in MonST3R / Easi3R / POMATO.
The persistent object_track_set + identity_consistency proxy on existing
3R outputs is inferred; not yet demonstrated end-to-end in any single
source.
```

action_policy_status: inferred

```text
theta_dynamic, theta_static, theta_flow, dynamic_horizon, mint_rate budget,
and the suppress/admit/defer priority ordering are inferred. No
measurement yet.
```

performance_status: unknown

```text
No benchmark numbers. No claim of improvement on dynamic-3R metrics. Cycle
009 case cards produce L2 proxy evidence only.
```

## Boundaries

no_reproduction_yet: yes

no_training_yet: yes

no_checkpoint_download_yet: yes

no_kykt_navigation_change: yes

no_frontend_implementation_yet: yes

no_4dgs_asset_path_yet: yes

```text
4DGS asset rendering is explicitly out of scope for this spec, even
though RU-005 and RU-013 make the asset path technically near. Bringing
4DGS in would dilute the F2-specific identity claim into a graphics
demo.
```

approval_gates_required_to_advance:

- moving from L2 case-card evidence to L3 prototype runner: requires user approval
- adding a KYKT navigation surface for the permanence timeline: requires user approval
- declaring this spec the final Dream thesis: requires user approval
- adding a 4DGS asset path: requires user approval (separate decision)
- training a learned identity head: requires user approval

## Linked Artifacts

linked_research_units:

- RU-013 Dynamic 4D Pointmap Branch (primary)
- RU-005 3R-to-4DGS Bridge (related; explicitly out-of-scope this cycle)
- RU-015 Geometry-Governed Executive Memory (related; cross-spec read for static-write suppression)

linked_sources: MonST3R, POMATO, D^2USt3R, Easi3R, RayMap3R, MASt3R-SfM, SLAM3R, G-CUT3R (see `registry/source_registry.md`)

linked_failure_modes: F2 (primary), F1, F3

linked_actions: A6 (owned), A2 (read-only support), A4 (read-only support), A7 (read-only support)

linked_proxy_metrics: P4 (primary), identity_consistency (secondary; defined in P4 protocol)

linked_cycle: CYCLE-20260503-002

linked_kykt_jobs:

- 20260420-222928 (MonST3R 48 frames + 96 masks + 96 confidence; primary)
- 20260420-222729 (MASt3R static pair; static control)
- pending: a labeled public/synthetic dynamic clip (case 03)

## Next Step

planned_only: yes

next_action: fill_case_cards

linked_next_artifact:

- `templates/proxy_case_card.md` -> populated as CASE-20260504-PERMANENCE-01..03 in cycle 009

## Next Discussion Point For The User

```text
Permanence is the most labor-heavy of the three finalists due to object
identity annotation. Three open user decisions:

  1. Annotation budget on MonST3R 48-frame job is 90-120 minutes per case
     card per cycle 008 D4 (no optional uplift). The 120-minute mark is
     a hard fail-fast cap: if identity_consistency cannot be labeled
     within that budget, Permanence retires to "close reserve". Within
     the cap, do you want sparser identity labels for more objects, or
     denser labels on one moving object? Default: dense on one object.
  2. Source of CASE-PERMANENCE-03 dynamic clip: synthetic (cheaper, may
     not generalize) vs labeled public clip (slower to source). Default:
     synthetic for cycle 009; revisit if synthetic confounds the result.
  3. Whether to surface the permanence timeline as the FIRST teacher demo
     candidate (highest visual impact) or hold demo precedence to Critic
     (cheapest evidence). Note: per DEC-20260504-002 the first demo
     target is deferred until cycle 009 case-card data exists; this item
     stays open and is not picked unilaterally.
```
