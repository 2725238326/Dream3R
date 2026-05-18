# SPEC-20260503-002 Executive Memory / State Governance

## Identity

spec_id: SPEC-20260503-002

branch_name:

```text
Executive Memory / State Governance (working title: GEM-3R)
```

date: 2026-05-03

status: draft (pending L2 case-card evidence in cycle 009)

cycle_of_origin: CYCLE-20260503-002

## Approval

user_approval_for_branch: yes

approval_decision_id: DEC-20260503-002

approval_note:

```text
User approved option B (Critic + Memory + Permanence finalists). This spec
covers the Memory finalist. It does NOT promote GEM-3R to final thesis;
that gate is still open.
```

## Failure Modes

primary_failure_mode: F1 Long-Context Drift / Forgetting

secondary_failure_modes:

- F3 Hard-Case Geometric Ambiguity (when memory write is gated by critic signal)
- F6 Fragmented Model Ecology (when memory policy spans outputs from multiple 3R models)

failure_mode_evidence:

- `planning/RESEARCH_GRAPH_AND_PAPER_START.md` rows F1, F3, F6
- F1 source mechanisms paper-proven across CUT3R / STream3R / LONG3R / LoGeR / Mem3R / PAS3R / FILT3R / OVGGT / Point3R; the Dream-specific *governance controller* over them is `inferred`.

## Owned Actions

owned_actions:

- A1 State Update Control
- A2 Spatial Memory Governance
- A3 Context / Anchor Budgeting

support_actions:

- A4 Geometry Verification (read-only signal from Critic spec; Memory does not own A4)
- A6 Dynamic / Object State Separation (read-only signal from Permanence spec; Memory does not own A6)

action_ownership_justification:

```text
Discipline rule 2 caps owned actions at <=3, and Memory hits the cap exactly.
This is intentional: A1 / A2 / A3 are the three governance levers
(state update, memory write, context budget). Splitting any of them out
into a separate spec would either fragment the controller or duplicate the
input signal vector. A4 and A6 are explicitly held by Critic and Permanence
respectively, so the Memory controller reads them as inputs but does not
fire them.
```

## Comparator Set

comparator_anchors:

- CUT3R (persistent latent state)
- STream3R (causal streaming geometry)
- LONG3R (long-sequence streaming)
- LoGeR (long-geometric memory; hybrid context)
- Mem3R (external memory)
- PAS3R (pose-adaptive update)
- FILT3R (Kalman-style update)
- OVGGT (constant-budget cache + anchor protection)
- Point3R (external sparse pointer memory)
- LongStream (long-sequence streaming)

closest_comparator: OVGGT + LoGeR combined (closest in spirit to anchor + cache + retrieval governance)

weakest_comparator_pressure:

```text
The memory field is crowded. Almost every named comparator already publishes
*one* memory mechanism (cache budget, pose-adaptive update, hybrid memory,
external pointer, Kalman update). Dream cannot claim novelty by adding a
fourth memory primitive. The novelty must live in the *controller* that
chooses among A1 / A2 / A3 sub-actions on a per-window evidence vector.
```

novelty_gap_against_comparators:

- Each comparator hard-wires one update / memory / cache rule. Dream Memory selects from a small policy bank on each window based on the evidence signal.
- OVGGT is the closest (anchor + cache budget) but does not condition on dynamic / critic / loop-candidate signals. Dream Memory uses cross-spec inputs from Critic and Permanence to gate writes.
- Point3R / Mem3R own external memory primitives. Dream Memory does not redefine the memory store; it defines the *write / read / merge / ignore* policy over an existing store contract.
- The comparison axis the paper would emphasize: *policy bank vs single rule*, not *new memory primitive*.

## Core Claim

claim_paragraph:

```text
Long-context 3R is not solved by adding another memory primitive. The unmet
need is a small, measurable policy bank that decides on each window whether
to update state, write memory, protect an anchor, evict cache, or pull
global context, based on geometry-grounded evidence rather than fixed
windows or confidence-only thresholds. The Dream contribution is the
controller and its falsifiable proxy bank, not a new memory store.
```

one_line_thesis:

```text
3R memory needs governance, not yet another memory module.
```

## Mechanism Pseudocode

inputs:

- per-window 3R outputs (pointmap, confidence, pose) from one or more comparator models
- evidence signal vector `e` from `ACTION_TAXONOMY_AND_PROXY_METRICS.md`
- read-only signals from Critic spec: conflict_score, route_history
- read-only signals from Permanence spec: dynamic_ratio, object_track_stability
- memory store contract: `{write(anchor), read(query), merge(a,b), ignore(window)}` (assumed; not designed in this spec)

state_variables:

- `latent_state(t)`: persistent compressed state, OVGGT / CUT3R style
- `anchor_set(t)`: set of protected anchor indices in the memory store
- `cache_window(t)`: bounded sliding window of recent contributions, eviction-eligible
- `policy_log(t)`: append-only log of which sub-action fired with which input signal

trigger_conditions:

- Memory controller runs every input window. It is cheap; it operates on already-produced outputs and metadata.
- Each owned sub-action has its own trigger; multiple sub-actions can fire on the same window (they are not mutually exclusive).

action_logic:

```text
on each window t:

  signals = read(e, critic_signals, permanence_signals)

  # A1 State Update Control
  update_kind = pick_update_policy(signals)  # one of:
    {full_update, pose_adaptive_update, kalman_update, skip_update, reset_state}
  apply update_kind to latent_state(t)

  # A2 Spatial Memory Governance
  for each candidate write w from this window:
    decision = pick_write_policy(w, signals)  # one of:
      {write, merge_with_existing, ignore, defer}
    apply decision

  # A3 Context / Anchor Budgeting
  if signals.loop_candidate_score high OR signals.anchor_importance high:
    add to anchor_set(t)
  if cache_pressure exceeds budget:
    evict_eligible = cache_window minus anchor_set
    evict by oldest-then-lowest-importance, never anchors
  if signals.conflict_score high (read from Critic) OR signals.long_horizon_drift:
    request global context (sparse retrieval over memory store)

  log policy choices into policy_log(t)
```

output_artifacts:

- per-window policy report: `{update_kind, write_decisions, anchor_changes, retrieval_request}`
- per-job timeline: aggregate of per-window reports
- comparator-policy contrast table: same job replayed under {fixed_window, uniform_keyframe, confidence_only, GEM-3R} policy strings to show divergence

## Evidence Signal Vector Used

active_signals:

- pose_novelty
- view_overlap
- confidence_drop
- latent_drift_proxy
- loop_candidate_score
- anchor_importance
- cache_pressure
- external_memory_overlap

inactive_signals (held by other specs):

- reprojection_residual (held by Critic A4)
- pointmap_conflict (held by Critic A4)
- prior_rgb_conflict (held by future Cross-Modal A7)
- dynamic_ratio (held by Permanence A6; Memory reads as input only)
- optical_flow_conflict (held by Permanence A6)
- object_track_stability (held by Permanence A6; Memory reads as input only)
- model_capability_match (held by Critic A5 / future Composer)
- blur_or_low_light_score (held by future Cross-Modal)
- uncertainty_area (held by future Active Perception A8)

derived_signals:

- update_pressure (combination of pose_novelty + confidence_drop + latent_drift_proxy)
- write_value_estimate (combination of loop_candidate_score + anchor_importance + external_memory_overlap, minus duplicate_rate)
- context_demand (combination of cache_pressure + critic conflict_score + drift)

## Action Policy Definition

| Action | Trigger condition | Scope of effect | Failure-aware fallback |
|---|---|---|---|
| A1 full_update | high update_pressure, low dynamic_ratio (read), no critic conflict | latent_state(t) | if critic later flags conflict on the updated state, downgrade to skip_update on next window |
| A1 pose_adaptive_update | medium update_pressure, stable dynamic_ratio | latent_state(t), gain modulated by pose novelty | if pose_novelty unreliable, fallback to skip_update |
| A1 kalman_update | medium update_pressure, partial conflict signal | latent_state(t), confidence-weighted blend | if no confidence signal exists, fallback to pose_adaptive_update |
| A1 skip_update | high dynamic_ratio (read) OR high critic conflict_score (read) | no change to latent_state(t) | always available; no fallback needed |
| A1 reset_state | persistent drift over N windows AND anchor_set still intact | reset latent_state(t), keep anchor_set | if anchor_set empty, escalate to user (do not silently reset) |
| A2 write | write_value_estimate > theta_write, low duplicate_rate | append to memory store | if duplicate_rate spikes after write, retroactively merge |
| A2 merge | duplicate_rate high on candidate write | merge into existing entry | if merge target ambiguous, defer (do not pick blindly) |
| A2 ignore | dynamic region (read from Permanence) OR high critic conflict | drop candidate | always available |
| A2 defer | borderline write_value_estimate AND short_horizon_decision_window not closed | hold candidate in cache_window | if cache_pressure forces eviction before deferral resolves, escalate to ignore |
| A3 protect anchor | anchor_importance OR loop_candidate_score above threshold | add to anchor_set(t); never evictable while protected | if anchor_set exceeds anchor_budget, downgrade lowest-importance anchor (log it) |
| A3 evict cache | cache_pressure > budget AND eviction candidate is not in anchor_set | remove from cache_window | if no eligible eviction candidate, raise context_demand for next window |
| A3 request global context | context_demand > theta_context | sparse retrieval over memory store | if retrieval returns empty, log unmet_context_request, do not block pipeline |

## Proxy Validation Plan

primary_proxy: P2 anchor retention

secondary_proxy: P3 memory growth and usefulness

case_cards_to_fill:

```text
CASE-20260504-MEMORY-01  on 20260420-222928 (MonST3R 48-frame; primary L2 case)
CASE-20260504-MEMORY-02  on 20260425-113227 (Spann3R transforms timeline)
CASE-20260504-MEMORY-03  on 20260420-222729 (MASt3R small-N baseline)
```

acceptance_threshold:

```text
On the labeled L2 cases (~3 case cards, ~48 + ~N + small-N windows):
  P2 anchor_retention(GEM-3R policy) >= anchor_retention(confidence_only)
      AND >= anchor_retention(fixed_sliding_window)
  P3 reuse_rate(GEM-3R) > reuse_rate(uniform_keyframe baseline)
      AND duplicate_rate(GEM-3R) <= duplicate_rate(write_everything)
  AND policy_log on the MonST3R 48-frame job shows that A1 / A2 / A3 each
      fire at least once and not always with the same sub-action (i.e.
      the controller is not a renamed single policy).
```

fail_fast_threshold:

```text
If after the cycle 009 case cards:
  GEM-3R policy <= confidence_only baseline on BOTH P2 and P3
  OR action_entropy across A1 / A2 / A3 sub-actions is effectively zero
      (i.e. the controller always picks the same sub-action; reduces to
      a single policy)
then retire Memory spec back to "close reserve" and refocus cycle 010 on
the remaining two finalists. Do not redraft to keep alive.
```

writing_value_if_only_negative_result:

```text
A clean negative is paper-relevant: it shows that an evidence-vector
controller without a learned policy cannot beat confidence-only retention
on existing 3R outputs, motivating either richer signals (e.g. learned
anchor importance) or a learned policy. Paper-grade negative documented
via the comparator-policy contrast table is acceptable cycle 009 output.
```

## Teacher Demo Form

what_is_visible:

```text
Single MonST3R 48-frame timeline panel with five rows:
  Row 1: original frames thumbnail strip
  Row 2: signal traces (pose_novelty, confidence_drop, dynamic_ratio,
         conflict_score, loop_candidate_score)
  Row 3: A1 update decision per window (color-coded)
  Row 4: A2 write/merge/ignore decisions on candidate writes
  Row 5: A3 anchor_set evolution + cache_pressure + context requests

Side-by-side: same timeline replayed under fixed_window / confidence_only
baselines so divergence is visible.
```

why_it_surprises_a_teacher:

```text
The teacher sees a 3R model "explaining" its memory: which frames it
considers anchors, which writes it skips because of dynamic regions, when
it requests context, and how it differs from naive policies on the same
inputs. This is not present in any single comparator's published demo.
```

artifact_format:

- markdown report with timeline image references plus a comparator-policy contrast table
- no live model inference; everything is offline post-processing of MonST3R job 20260420-222928

approval_required_for_demo: yes

## KYKT Integration Surface

surface_list:

- research_lane (memory timeline as research artifact)
- advisor_report (per-job memory policy summary attaches to Advisor output)
- management_area (long-running research surface; future, NOT this cycle)

NOT in scope this spec:

- runner (no runner change; Memory post-processes existing job outputs)
- sample_matrix (no scoring change)
- system_readiness (no system change)
- KYKT navigation change (still approval-gated)

backend_contract_needed:

```text
Read-only access to existing job artifact paths under model_uploads/. The
memory store contract is *assumed* by this spec, not implemented. Any
write-side contract (e.g. for the future management area) is a separate
backend handoff and is NOT authorized by this spec.
```

frontend_handoff_needed: no

frontend_handoff_brief_id: not_applicable_yet

## Engineering Cost

L1_design_cost: low

```text
This spec plus three case cards in cycle 009. ~6-8 hours of synthesis work.
Annotation budget per case card: 90-120 minutes per cycle 008 D4 (no
optional uplift; this is the ceiling). The MonST3R 48-frame job is still
the longest of the three case cards inside that shared cap.
```

L2_proxy_cost: medium

```text
Higher than Critic because the comparator-policy contrast table requires
running four policy strings (fixed_window, uniform_keyframe, confidence_only,
GEM-3R) over the same input. All four are scripted policies, no model
invocation needed. Memory store is mocked via in-memory dict for the case
cards.
```

L3_prototype_cost: blocked_until_approval

L4_model_change_cost: blocked_until_approval

## Risks

novelty_risk:

```text
Highest of the three finalists. The memory field is the most crowded.
Mitigated by framing the contribution as "policy bank over evidence vector"
rather than "new memory primitive", and by enforcing a >=2 sub-action
policy_log across A1 / A2 / A3 in the case cards.
```

overlap_with_comparator:

```text
Direct overlap with OVGGT (anchor + cache budget). Mitigated by the
cross-spec read of dynamic_ratio (Permanence) and conflict_score (Critic),
which OVGGT does not condition on. The case cards must show that this
cross-conditioning matters; if it does not, the spec collapses into a
relabeling of OVGGT.
```

engineering_risk:

```text
Low at L1/L2. The risk lives at L3 prototype, which is blocked.
```

demo_risk:

```text
The five-row timeline is dense. Mitigation: cycle 010 demo iteration can
collapse to a three-row simplified version after the case cards land.
```

paper_writing_risk:

```text
"Executive memory" is rhetorically strong but vague. The paper claim must
shift to a measurable controller story (policy bank + evidence-vector
gating + falsifiable P2/P3) rather than a memory architecture story, or
risk being read as relabeling existing memory work.
```

## Evidence Labels

mechanism_status: inferred

```text
A1 / A2 / A3 sub-actions are individually paper-proven across the comparator
set. The *controller that selects among them on an evidence vector* is
inferred; not yet demonstrated in any single source.
```

action_policy_status: inferred

```text
theta_write, theta_context, anchor_budget, and the sub-action priority
ordering are inferred from the comparator literature. No measurement yet.
```

performance_status: unknown

```text
No benchmark numbers. No claim of accuracy improvement over any comparator.
Cycle 009 case cards produce L2 proxy evidence only.
```

## Boundaries

no_reproduction_yet: yes

no_training_yet: yes

no_checkpoint_download_yet: yes

no_kykt_navigation_change: yes

no_frontend_implementation_yet: yes

approval_gates_required_to_advance:

- moving from L2 case-card evidence to L3 prototype runner: requires user approval
- adding a KYKT navigation surface for the memory timeline: requires user approval
- declaring this spec the final Dream thesis: requires user approval
- training a learned policy: requires user approval
- defining or owning a backend management-area contract: requires user approval

## Linked Artifacts

linked_research_units:

- RU-015 Geometry-Governed Executive Memory for 3R (primary)
- RU-001 Geometry-Gated State-Space 3R (related architecture candidate)
- RU-004 External Sparse Spatial Memory (related foundational rule)
- RU-009 Route-Scan Policy Bank (related: route-policy axis)
- RU-010 Hybrid Context Router (related: context budget)
- RU-014 Long-Context Hybrid Memory Benchmark (related: benchmark spine for cycle 010+)

linked_sources: CUT3R, STream3R, LONG3R, LoGeR, Mem3R, PAS3R, FILT3R, OVGGT, Point3R, LongStream, POMATO, D^2USt3R (see `registry/source_registry.md`)

linked_failure_modes: F1 (primary), F3, F6

linked_actions: A1 (owned), A2 (owned), A3 (owned), A4 (read-only support), A6 (read-only support)

linked_proxy_metrics: P2 (primary), P3 (secondary)

linked_cycle: CYCLE-20260503-002

linked_kykt_jobs:

- 20260420-222928 (MonST3R 48-frame; primary)
- 20260425-113227 (Spann3R transforms timeline)
- 20260420-222729 (MASt3R small-N baseline)

## Next Step

planned_only: yes

next_action: fill_case_cards

linked_next_artifact:

- `templates/proxy_case_card.md` -> populated as CASE-20260504-MEMORY-01..03 in cycle 009

## Next Discussion Point For The User

```text
Memory is the most ambitious of the three finalists, with the largest
comparator overlap. Two open user decisions:

  1. Annotation budget on the MonST3R 48-frame job is now 90-120 minutes
     per case card per cycle 008 D4 (no optional uplift). Inside that cap,
     do you prefer denser anchor-importance ground truth (closer to the
     120-minute end) or broader coverage with lighter anchor labels
     (closer to the 90-minute end)? Default: balanced 90-100 minutes.
  2. Whether to reserve a fourth case card for an MV-DUSt3R+ or Splatt3R
     output once a fresh KYKT job becomes available, or freeze the case
     card list at three. Default: freeze at three for cycle 009; revisit
     in cycle 010.
```
