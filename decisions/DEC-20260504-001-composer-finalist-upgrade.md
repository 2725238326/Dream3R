# DEC-20260504-001 Composer Finalist Upgrade

decision_id: DEC-20260504-001

date: 2026-05-04

scope: thesis shortlist / mechanism-spec authorization

decision: Upgrade 3R Composer / Unified Model Ecology from supporting layer to a fourth finalist mechanism spec. Drafting happens now in cycle 008.5, not after one of the three existing finalists clears its first L2 case card.

status: accepted

requires_user_approval: yes (this DEC IS the user approval gate)

## Context

DEC-20260503-002 approved option B from `planning/BRANCH_SHORTLIST_DECISION_SURFACE.md` (Critic + Memory + Permanence as finalists; Composer as supporting layer). The cycle 008 close-out `cycles/CYCLE-20260503-002.md` carried four explicit user decisions forward, including:

```text
Discussion point 2: Composer L1 vs L2 framing - draft Composer as a fourth
spec when one finalist clears its first case card, or keep Composer as
undocumented support until then?
```

In the session that produced `handoff/SESSION-HANDOFF-20260504-001-cycle-008-closeout-and-cycle-009-prep.md`, the user resolved that question in favor of upgrading now and accelerated the timing via "全力提速".

`AGENT_MASTER_PROMPT.md` section 6 lists "drafting a mechanism spec only for an approved finalist branch" under decisions that may proceed without further user prompt once branch finalist approval is on file. Composer was already named in DEC-20260503-002 as part of the option-B finalist context (as supporting layer); this DEC promotes it to finalist status with the user's explicit decision and authorizes the corresponding spec drafting.

## Evidence

- User verbatim on D2: "决策2改成升格吧，因为确实有效果"
- User verbatim on tempo: "全力提速了" in the same turn
- Cross-spec dependency observed in cycle 008:
  - SPEC-20260503-001 (Critic) action A5 reroute_model reads `model_capability_match` from a Composer-style capability card.
  - Without a written Composer spec, A5 case cards in cycle 009 fall back to hand-written capability assumptions, which is exactly the failure mode `paradigm/RESEARCH_CODE_DISCIPLINE.md` rule 5 (Honesty Override) warns against.
- Cycle 008 already documented Composer's L1/L2 distinction in `planning/BRANCH_SHORTLIST_DECISION_SURFACE.md` Candidate 3 and `planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md` "Branch Pressure After Taxonomy" table. The L2 mechanism-distillation framing was the bottleneck, not the L1 capability-card framing.
- Composer's owned-action set is small (A5 only). Discipline rule 2 (Minimum Viable Mechanism) is satisfied without further reduction.

## Options

A. Defer Composer spec until one of the three finalists clears its first case card. *(declined; user requested acceleration; A5 case cards in cycle 009 would otherwise rely on un-versioned Composer assumptions)*

B. Draft Composer as a fourth finalist spec now. *(approved by user)*

C. Keep Composer as undocumented support, never escalate. *(declined; would silently bake Composer assumptions into Critic A5 logic without an evidence trail)*

## Decision

1. Authorize drafting `specs/SPEC-20260504-001-3r-composer.md` using `templates/finalist_mechanism_spec.md`.

2. The Composer finalist spec:

   - owns A5 only (single owned action; Composer's leverage is the capability-card matrix, not a wide action set)
   - reads from A3 / A4 / A7 as support actions
   - declares F6 Fragmented Model Ecology as primary failure mode; F3 / F1 / F2 as secondary
   - uses P5 route_regret as primary proxy and capability_match as secondary
   - reserves three CASE-20260505-COMPOSER-* slots for cycle 009

3. Composer's specific cross-spec consumers (Critic A5 reads Composer's `capability_match` signal) are formalized in the new file `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` rather than smuggled into the Composer spec body. The contract is itself drafted in this same cycle 008.5 session.

4. The promotion does not change the user's posture on thesis selection. DEC-20260504-002 (no all-in on a single finalist) is the controlling posture and applies to Composer just as to Critic / Memory / Permanence.

5. Update `registry/research_unit_registry.md` so RU-002 decision moves from "best near-term demo" to "spec_drafted (linked to SPEC-20260504-001)".

6. Update `units/RESEARCH_UNIT_BANK.md` RU-002 with a 2026-05-04 decision line carrying the same content.

## Risks

- **Four parallel finalist case-card passes increase annotation budget pressure.** Mitigated by DEC-20260504-002 fixing per-card budget at 90 to 120 minutes. If aggregate budget overruns, retire whichever spec has the weakest case-card evidence first (no preferential rescue for Composer).
- **Composer L1 framing risks reading as system engineering rather than paper-grade architecture.** This is the weakest_comparator_pressure already named in `planning/BRANCH_SHORTLIST_DECISION_SURFACE.md` Candidate 3. Mitigated by attaching P5 route_regret as the falsifying axis: if route_regret has zero spread across all three case cards, Composer retires to "support layer only" rather than redrafting.
- **Cross-spec contract drift.** Critic's A5 reroute logic reads Composer's `capability_match`; if the contract drifts during cycle 009 case cards, both specs' results move together rather than independently. Mitigated by versioning the contract in `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` and treating contract revision as a new entry rather than a silent edit (Discipline rule 5).
- **Counter-recommendation in `ACTION_TAXONOMY_AND_PROXY_METRICS.md` "First Research Inference"** had treated Composer as evidence infrastructure. The user's decision overrides that inference; the inference is not retracted, only superseded for cycle 009 planning.

## User Approval Required

This DEC IS the user approval gate for upgrading Composer to a finalist spec.

User approval IS still required for, and is NOT granted by this decision:

- selecting Composer (or any single finalist) as the final thesis (DEC-20260504-002 explicitly forbids treating any finalist as the thesis spine)
- moving Composer from L2 case-card evidence to L3 prototype runner
- reproducing any candidate model
- training, fine-tuning, or downloading any new checkpoint
- changing KYKT navigation
- Codex directly editing KYKT frontend code
- packaging a reusable Codex skill
- declaring teacher-demo readiness
- discarding any non-finalist track (Cross-Modal, Active Perception)

## Next Action

Draft `specs/SPEC-20260504-001-3r-composer.md` and `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` in this cycle 008.5 session. Their first L2 case cards (CASE-20260505-COMPOSER-01..03) are reserved for cycle 009 and execute in parallel with Critic / Memory / Permanence case cards under the per-card budget set in DEC-20260504-002.
