# CASE-20260505-COMPOSER-05: VGGT capability-card gap addendum

case_id: CASE-20260505-COMPOSER-05

linked_spec: SPEC-20260504-001 3R Composer / Unified Model Ecology

status:

```text
addendum; L2 capability-card gap analysis; not measured route_regret;
no contract revision
```

cycle_of_origin: CYCLE-20260505-005

parent_decision: DEC-20260505-004-cycle-014-launch

## Purpose

Cycle 013 source mining surfaced VGGT as a feed-forward visual-geometry
transformer missing from the existing Composer L2 portfolio
(`CASE-20260505-COMPOSER-01..04`). This card records the gap without
retroactively rewriting those earlier cards.

This addendum answers one question:

```text
Does VGGT require a v2.2 cross-spec contract revision, or only a new
capability_card model row under the existing v2.1 schema?
```

Answer:

```text
Only a new capability_card row is required. No v2.2 contract revision is
needed.
```

Evidence label: `inferred`, grounded in v2.1 schema compatibility and
cycle-013 source mining. No local run was performed.

## Source anchors

| Source | Role | Evidence label |
|---|---|---|
| SRC-2026-015 VGGT | missing feed-forward visual-geometry comparator | paper-proven at source level; local performance unknown |
| SRC-2026-013 DUSt3R / MASt3R / VGGT MVS evaluation | external evaluation sanity check for capability-card axes | paper-proven at source level; not locally reproduced |
| SRC-2026-009 MapAnything | adjacent universal feed-forward geometry comparator | paper-proven at source level; repo URL to verify before L3 |
| SRC-2026-012 awesome-dust3r | curated index for additional comparator discovery | curated-index; not evidence by itself |

## Regime-card interpretation

VGGT should be represented as a candidate model row in Composer's
`capability_card(model_id)` table.

Proposed row sketch:

| Model | Static pair | Many-view static | Sparse-view | Streaming long-context | Dynamic video | Cost axis | Evidence label |
|---|---:|---:|---:|---:|---:|---:|---|
| VGGT | medium | high | medium-to-high | low-to-unknown | low-to-unknown | medium | inferred from paper + external MVS evaluation |
| MapAnything | medium | medium-to-high | medium-to-high | unknown | unknown | medium-to-high | inferred from paper framing |

Notes:

- "high" for VGGT many-view static is an `inferred` Composer score, not
  a measured Dream score.
- dynamic video and streaming long-context remain `unknown` or low
  because this card has not run VGGT on the Memory / Permanence regimes.
- MapAnything is not inserted as a first L3 pilot target; it is a
  capability-card coverage reminder.

## Contract compatibility check

Existing v2.1 fields already cover VGGT:

```text
capability_card(model_id)
sample_regime_card(input)
capability_match(model_id, input)
cost_adjusted_match
route_recommendation(input)
route_regret(chosen, input)
```

No new cross-spec signal is required. VGGT is a new `model_id`, not a new
signal type. Therefore:

```text
v2.1 -> v2.2: no revision recommended.
```

## Route-regret implication

Before this addendum, a Composer route-regret sweep that used only DUSt3R
/ MASt3R / Fast3R could be criticized as omitting a strong 2026
feed-forward visual-geometry comparator. After this addendum, the correct
position is:

```text
First minimal sweep may still use DUSt3R / MASt3R / Fast3R for budget
reasons, but any paper-facing G2 closure sweep should include VGGT or
explicitly justify its exclusion.
```

Evidence label: `inferred`.

## Interaction with existing Composer cards

This card does NOT rewrite:

- `CASE-20260505-COMPOSER-01.md`
- `CASE-20260505-COMPOSER-02.md`
- `CASE-20260505-COMPOSER-03.md`
- `CASE-20260505-COMPOSER-04.md`

Those cards remain historically correct for the source set available at
their drafting time. This addendum supersedes only the assumption that the
Composer L2 portfolio has complete comparator coverage.

## Fail-fast condition

If future source verification shows VGGT's public artifacts are not usable
for the intended 3R comparison, do not silently drop the row. Mark VGGT as
`paper-only / no local smoke` in the Composer L3 sweep design and record
the reason in the cycle log.

## Non-authorizations

This addendum does NOT authorize:

- cloning or installing VGGT,
- downloading VGGT checkpoints,
- running VGGT,
- changing the cross-spec contract,
- closing G2,
- promoting Composer storyboard status,
- final thesis selection.
