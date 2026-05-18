# Proxy Case Card Template

Status: branch-neutral form. One card per scenario, per proxy metric.

Use with:

```text
planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md (A1-A8, P1-P8, evidence vector)
planning/ARCHITECTURE_MECHANISM_INTAKE.md (mechanism families and comparator groups)
planning/BRANCH_SHORTLIST_DECISION_SURFACE.md (branch ownership of actions)
planning/RESEARCH_GRAPH_AND_PAPER_START.md (failure modes F1-F6, mechanism nodes M1-M18, composition edges C1-C16)
```

A case card must not claim measured performance. It records a predicted action, predicted proxy values, and a comparison against named comparator policies, with an explicit evidence label.

## Identity

case_id: CASE-YYYYMMDD-NNN

proxy_id: P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8

scenario_name:

date:

linked_failure_modes: F1 | F2 | F3 | F4 | F5 | F6

linked_actions: A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8

linked_branches: Executive_Memory | Geometry_Critic | Composer | Dynamic_Object_Permanence | Cross_Modal | Active_Perception

linked_research_units:

linked_sources:

## Input Artifact

source_type: paper_example | public_artifact | kykt_metadata | manual_label | synthetic | design_only

artifact_pointer:

evidence_label: paper-proven | code-observed | demo-observed | inferred | speculative | unknown

input_summary:

## Evidence Signals

Record only the signals relevant to the scenario. Use qualitative or numeric values. Mark unknowns explicitly.

pose_novelty:

view_overlap:

reprojection_residual:

pointmap_conflict:

confidence_drop:

latent_drift_proxy:

dynamic_ratio:

optical_flow_conflict:

object_track_stability:

loop_candidate_score:

anchor_importance:

cache_pressure:

external_memory_overlap:

prior_rgb_conflict:

blur_or_low_light_score:

uncertainty_area:

model_capability_match:

## Comparator Policies

List at least one comparator policy plus the Dream policy. Add more rows as needed.

| Policy | Action chosen | Predicted proxy value | Notes |
|---|---|---|---|
| comparator_1 (e.g., fixed sliding window) |  |  |  |
| comparator_2 (e.g., uniform keyframe sampling) |  |  |  |
| comparator_3 (e.g., confidence-only retention) |  |  |  |
| dream_policy (evidence-triggered) |  |  |  |

## Predicted Proxy Outcome

primary_metric: P{n}_{name}

unit_of_measurement:

threshold_for_useful_signal:

predicted_dream_value:

predicted_best_comparator_value:

expected_gap_direction: dream_better | comparator_better | tie | unknown

decision_signal_meaning:

## Writing Value

related_work_section: memory | critic | dynamic | sensor | composer | active

figure_or_taxonomy:

novelty_claim_supported:

## Risk And Boundaries

fail_fast_condition:

reproduction_required: no

training_required: no

frontend_change_required: no

approval_required: no

caveats:

## Next Action

next_action: refine_card | add_comparator | escalate_to_spec | retire | needs_user_decision

linked_next_artifact:
