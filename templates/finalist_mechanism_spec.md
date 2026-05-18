# Finalist Mechanism Spec Template

Status: branch-neutral form. One spec per user-approved finalist branch.

This template must not be populated until the user has approved the branch as a finalist via a decision logged in `registry/decision_registry.md`.

A finalist mechanism spec is design evidence (Level 1) plus a defined L2 proxy plan. It does not authorize reproduction, training, checkpoint download, or KYKT navigation change.

## Identity

spec_id: SPEC-YYYYMMDD-NNN

branch_name:

date:

status: draft | user-approved | revising | blocked

## Approval

user_approval_for_branch: yes | no

approval_decision_id:

approval_note:

## Failure Modes

primary_failure_mode: F1 | F2 | F3 | F4 | F5 | F6

secondary_failure_modes:

failure_mode_evidence:

## Owned Actions

owned_actions: A1 | A2 | A3 | A4 | A5 | A6 | A7 | A8

support_actions:

action_ownership_justification:

## Comparator Set

comparator_anchors:

closest_comparator:

weakest_comparator_pressure:

novelty_gap_against_comparators:

## Core Claim

claim_paragraph:

one_line_thesis:

## Mechanism Pseudocode

inputs:

state_variables:

trigger_conditions:

action_logic:

output_artifacts:

## Evidence Signal Vector Used

active_signals:

inactive_signals:

derived_signals:

## Action Policy Definition

For each owned action, define when it fires and with what scope.

| Action | Trigger condition | Scope of effect | Failure-aware fallback |
|---|---|---|---|
| A_x |  |  |  |

## Proxy Validation Plan

primary_proxy: P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8

secondary_proxy:

case_cards_to_fill: list CASE-IDs from `templates/proxy_case_card.md`

acceptance_threshold:

fail_fast_threshold:

writing_value_if_only_negative_result:

## Teacher Demo Form

what_is_visible:

why_it_surprises_a_teacher:

artifact_format:

approval_required_for_demo: yes | no

## KYKT Integration Surface

surface_list: research_lane | runner | sample_matrix | advisor_report | system_readiness | management_area

backend_contract_needed:

frontend_handoff_needed: yes | no

frontend_handoff_brief_id:

## Engineering Cost

L1_design_cost: low | medium | high

L2_proxy_cost: low | medium | high

L3_prototype_cost: blocked_until_approval

L4_model_change_cost: blocked_until_approval

## Risks

novelty_risk:

overlap_with_comparator:

engineering_risk:

demo_risk:

paper_writing_risk:

## Evidence Labels

mechanism_status: paper-proven | inferred | speculative | unknown

action_policy_status: inferred | speculative

performance_status: unknown

## Boundaries

no_reproduction_yet: yes

no_training_yet: yes

no_checkpoint_download_yet: yes

no_kykt_navigation_change: yes

no_frontend_implementation_yet: yes

approval_gates_required_to_advance:

## Linked Artifacts

linked_research_units:

linked_sources:

linked_failure_modes:

linked_actions:

linked_proxy_metrics:

linked_cycle:

## Next Step

planned_only: yes

next_action: refine_spec | fill_case_cards | request_user_approval | escalate_to_experiment_plan | retire | needs_user_decision

linked_next_artifact:
