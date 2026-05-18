# DEC-20260503-002 Finalist Shortlist Approval (B Path)

decision_id: DEC-20260503-002

date: 2026-05-03

scope: thesis shortlist / mechanism-spec authorization

decision: User approved option B from `planning/BRANCH_SHORTLIST_DECISION_SURFACE.md`. The finalist set for mechanism-spec drafting is Geometry Critic / System-2 3R + Executive Memory / State Governance + Dynamic Object Permanence / 4D Memory, with 3R Composer as supporting layer. Cross-Modal and Active Perception remain alive in the multi-track canvas at lower priority but are not finalists.

status: accepted

requires_user_approval: yes (this decision IS the user approval gate)

## Context

`BRANCH_SHORTLIST_DECISION_SURFACE.md` had four candidate moves:

```text
A. Critic + Memory finalists; Composer support.
B. Add Dynamic Object Permanence as third finalist.
C. Keep all six branches; first prepare proxy case cards.
D. Mine more sources before choosing.
```

The previous turn presented a side-by-side analysis of each path against the user's original intent (architecture novelty + paper-grade story + visible demo + KYKT integration), with explicit fail-fast conditions and Honesty-Override notes per the new `paradigm/RESEARCH_CODE_DISCIPLINE.md`.

`AGENT_MASTER_PROMPT.md` section 6 lists "final thesis selection" and "deepening any single branch as the default thesis" as user-approval gates. Drafting mechanism specs for an approved finalist set is *not* the same as finalizing a thesis — it is the design-level (L1) artifact that the data model schema names "finalist mechanism spec." The branch approval gate is therefore narrower: it authorizes spec drafting and L2 proxy planning, not thesis selection.

## Evidence

- User message verbatim: "B方案吧，同时我们在这个过程里还需要很多次讨论，请你继续推进！"
- Translation context: "Go with option B; we'll need many discussions during the process; please continue pushing forward."
- Source recommendation alignment: `BRANCH_SHORTLIST_DECISION_SURFACE.md` "Provisional Synthesis" section pre-recommended adding Dynamic Object Permanence as a third finalist. The user's choice matches that recommendation.
- Counter-recommendation in `ACTION_TAXONOMY_AND_PROXY_METRICS.md` "First Research Inference" had leaned toward A (Critic + Memory + Composer support) with Permanence as close reserve. The conflict was disclosed to the user in the previous turn.
- The user accepted the `+1 cycle cost` of the third spec (B vs A) explicitly, by choosing B knowing this from the previous turn's comparison.

## Options

A. Critic + Memory finalists; Composer support. *(declined by user)*

B. Add Dynamic Object Permanence as third finalist. *(approved by user)*

C. Keep all six branches; first prepare proxy case cards. *(declined; would have deferred specs by ≥ 1 cycle)*

D. Mine more sources before choosing finalists. *(declined; cycle 005 already closed the named comparator gaps)*

## Decision

1. The user-approved finalist set is:

   - Finalist 1: **Geometry Critic / System-2 3R** (links RU-003, RU-011)
   - Finalist 2: **Executive Memory / State Governance** (links RU-015 primary; RU-001, RU-004, RU-009, RU-010, RU-014 related)
   - Finalist 3: **Dynamic Object Permanence / 4D Memory** (links RU-013)

2. **3R Composer / Unified Model Ecology** stays as supporting layer for evidence infrastructure and KYKT integration. It does not receive a finalist spec in cycle 008. Whether it gets one in a later cycle is decision point #2 in the cycle log.

3. **Cross-Modal / Event-Augmented 3R** and **Active Spatial Perception / RL-3R** remain in the multi-track canvas at lower priority. They are not retired; they are simply not in the finalist set this round.

4. Authorize cycle 008 to draft three finalist mechanism specs using `templates/finalist_mechanism_spec.md`. Each spec:

   - owns ≤ 3 actions from A1–A8 per Discipline rule 2
   - defines a primary proxy + fail-fast threshold per Discipline rule 4
   - uses existing KYKT job outputs as L2 evidence path (no reproduction)
   - carries honest evidence labels per Discipline rule 5

5. Update RU registry decision fields for RU-003, RU-011, RU-013, RU-015 from "candidate / required / strong-bridge" to **`spec_drafted`** to reflect that they now have an active mechanism spec attached.

6. Update WORKFLOW_STATUS active workstreams to include the three specs.

## Risks

- **Three specs in parallel risk diluting any one of them.** Mitigated by per-spec fail-fast thresholds in cycle 008 header and Discipline rule 2 owned-actions cap. If a spec hits its fail-fast within cycle 009 case-card filling, it retires cleanly without forcing the cycle to drag.
- **Permanence proxy (object identity) is the most labor-heavy of the three.** Mitigated by ceiling annotation cost on the existing MonST3R 48-frame job to ~1 hour of human effort; surfaced as decision point #4 to the user.
- **B path defers Composer L2 framing.** Mitigated by surfacing it as decision point #2 in the cycle log so it does not get silently dropped.
- **Two finalist branches (Critic + Memory) overlap on F3 secondary failure mode coverage.** Mitigated by enforcing distinct owned-action sets in the specs (Critic = A4+A5; Memory = A1+A2+A3); the F3 overlap is intentional in support actions only.

## User Approval Required

This decision IS the user approval gate. No further user approval is required for:

- drafting the three finalist mechanism specs (this cycle)
- filling proxy case cards in cycle 009 using existing KYKT artifacts
- updating registries and status files

User approval IS still required for, and is NOT granted by this decision:

- selecting one finalist as the final thesis
- moving from L2 proxy evidence to L3 prototype code
- reproducing any candidate model
- training or fine-tuning
- downloading any new checkpoint
- changing KYKT navigation
- Codex directly editing KYKT frontend code
- packaging a reusable Codex skill
- declaring teacher-demo readiness
- discarding any non-finalist track (Cross-Modal, Active Perception)

## Next Action

Draft the three finalist specs in this cycle (cycle 008). Their first L2 case cards are the next-cycle (cycle 009) workload.

The specs themselves end with explicit "next discussion point" lines so the user can choose:

1. Which spec to deepen first in cycle 009.
2. Whether to spin Composer up as a fourth spec when one finalist clears its first case card.
3. Which spec's proxy outcome should drive the first teacher-facing KYKT demo.
