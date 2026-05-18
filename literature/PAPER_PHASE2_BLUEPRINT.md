# Paper Phase 2 Blueprint

Last updated: 2026-05-05 (cycle 014 S2; markdown-only blueprint, not full paper)

Status: draft blueprint; does not claim paper readiness.

## Purpose

This file converts the cycle-013 related-work prose draft into a Phase 2
paper-writing plan. It is not a submitted paper, not a final outline, and
not evidence that the Dream mechanisms work beyond their current evidence
labels.

Source anchors:

- `literature/PAPER_RELATED_WORK_SKELETON.md` (cycle 013 prose draft)
- `specs/SPEC-20260503-001-geometry-critic.md`
- `specs/SPEC-20260503-002-executive-memory.md`
- `specs/SPEC-20260503-003-dynamic-object-permanence.md`
- `specs/SPEC-20260504-001-3r-composer.md`
- `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v2.1
- `cases/` L2 portfolio (13 cards)
- `experiments/EXP-20260505-001..004-l3-prerequisites-*.md`

## Working title candidates

```text
Dream3R: Geometry-Governed Control for Long-Context 3R
```

Evidence label: `inferred`.

Reason: this title captures the four-finalist structure without claiming
that a final architecture has already been validated.

```text
Geometry-Governed Executive Control for Fragmented 3R Systems
```

Evidence label: `inferred`.

Reason: this title is more precise for the current L2 state. It avoids
the risk that "Dream3R" sounds like a trained model that already exists.

## Problem statement

Current post-DUSt3R 3R systems are strong but fragmented. One line improves
long-context state, another handles dynamic motion, another verifies
geometry, and another accelerates or generalizes feed-forward
reconstruction. The missing object is not one more backbone; it is a small
control layer that decides when to verify, when to route, when to write
memory, and when to protect static structure from dynamic pollution.

Evidence label: `inferred`, grounded in the source map and L2 case-card
portfolio. This is a framing claim, not a measured result.

## Core paper claim ladder

### Claim C0: Field fragmentation is real

Claim:

```text
3R model families now specialize by regime: pairwise geometry, matching,
many-view feed-forward reconstruction, streaming memory, dynamic scenes,
and Gaussian asset paths.
```

Current evidence: `paper-proven` at source level via DUSt3R / MASt3R /
Fast3R / Spann3R / MonST3R / CUT3R / STream3R / VGGT / MapAnything and
related entries in `registry/source_registry.md`.

Needed before paper submission: source table cleanup and exact citation
format. No L3 execution required for this claim.

### Claim C1: A shared action vocabulary exposes the missing control layer

Claim:

```text
The A1-A8 action taxonomy provides a compact language for comparing
state update, memory governance, verification, rerouting, dynamic
separation, prior arbitration, and evidence acquisition.
```

Current evidence: `inferred`, grounded in
`planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md` and the four finalist
specs.

Needed before paper submission: tighten the taxonomy table and make
every action map to at least one source-side comparator and one Dream
case card.

### Claim C2: Four finalists form a minimal control graph

Claim:

```text
Critic, Memory, Permanence, and Composer are not four independent ideas;
they form a control graph where Composer publishes capability priors,
Critic verifies and triggers repair / reroute, Permanence blocks dynamic
pollution, and Memory governs state writes and anchor budgets.
```

Current evidence: `inferred-with-L2-case-card-anchor`, grounded in the
four specs, v2.1 cross-spec signal contract, and 13 L2 case cards.

Needed before paper submission: one diagram and one signal-flow table.
This claim can be described as design contribution before L3, but must
not be presented as measured performance.

### Claim C3: The first executable proof should target Critic

Claim:

```text
The shortest L3 path is a Critic-Composer loop that catches a geometric
near-failure and routes to a better comparator under a logged
capability_match signal.
```

Current evidence: `inferred`, grounded in
`EXP-20260505-001-l3-prerequisites-critic.md`,
`CASE-20260504-CRITIC-02.md`, `CASE-20260505-COMPOSER-01.md`, and the
D3 selection in `DEC-20260505-001`.

Needed before paper submission: actual L3 run or a clear statement that
this remains proposed work. Current cycle 014 does not run it.

### Claim C4: Route-regret is the key falsification axis for Composer

Claim:

```text
If Composer cannot reduce cost-typed route_regret versus naive default
routing, its routing layer is engineering infrastructure rather than a
paper-grade mechanism.
```

Current evidence: `inferred-with-real-inventory-anchor`, grounded in
COMPOSER-04 and contract v2 / v2.1. G2 is not closed.

Needed before paper submission: measured multi-regime route_regret via
the Composer L3 sweep. VGGT must be added to the capability-card gap
analysis before the sweep design is frozen.

## Proposed paper structure

### 1. Introduction

Purpose: state the fragmentation problem and the control-graph thesis.

Must include:

- one paragraph on why one more 3R backbone is not enough,
- one paragraph on the Dream control graph,
- one paragraph on evidence discipline: L2 case cards now, L3 pilot next.

Must avoid:

- claiming a trained Dream3R model exists,
- claiming route_regret is measured,
- implying teacher demo readiness.

### 2. Related work by failure mode

Purpose: reuse `PAPER_RELATED_WORK_SKELETON.md` Sections 1-7 as source
material.

Write order:

1. pose-free / feed-forward 3R foundations,
2. long-context and memory,
3. dynamic 3R and object permanence,
4. test-time verification and correction,
5. model ecology and Composer,
6. parallel but non-owned axes: Cross-Modal and Active Perception.

### 3. Action vocabulary

Purpose: introduce A1-A8 as the paper's abstraction layer.

Minimum table:

| Action | Owner in Dream | Comparator pressure | Current evidence |
|---|---|---|---|
| A1 / A2 / A3 | Memory | CUT3R / Spann3R / Mem3R / OVGGT | inferred |
| A4 | Critic | Test3R / MASt3R-SfM | inferred |
| A5 repair facet | Critic | Test3R / TTT3R | inferred |
| A5 route facet | Composer | no direct 3R composer; MoE analog | inferred |
| A6 | Permanence | MonST3R / Easi3R / RayMap3R | inferred |
| A7 / A8 | deferred tracks | cross-modal / active perception | speculative-to-inferred |

### 4. Dream control graph

Purpose: show four finalists as one system.

Required figure:

```text
sample_regime_card -> Composer capability_match
                  -> Critic verify / reroute decision
                  -> Memory write / anchor policy
                  -> Permanence suppress / admit static write
                  -> logged evidence report
```

This figure is `inferred` until L3 code exists.

### 5. L2 proxy portfolio

Purpose: summarize the 13 case cards without overclaiming.

Table columns:

- case id,
- finalist,
- input regime,
- owned action,
- proxy metric,
- cross-spec signals consumed,
- evidence label,
- fail-fast outcome.

Current evidence: `inferred-with-L2-case-card-anchor`.

### 6. L3 pilot plan

Purpose: present the first executable step.

Recommended first pilot: Critic (pending S4 downselect in cycle 014).

Backup: Composer route-regret sweep if the research priority is G2 closure
instead of D3 demo support.

Must state: no L3 result exists until the run happens and logs are stored.

### 7. Discussion and limitations

Required limitations:

- all thresholds are inferred unless measured,
- current capability cards are incomplete without VGGT / MapAnything gap
  handling,
- route_regret is not closed,
- Memory and Permanence L3 paths are heavier,
- storyboards are draft only,
- no final thesis has been selected.

## Evidence table for current paper readiness

| Component | Current status | Evidence label | Blocking gap |
|---|---|---|---|
| Related work | prose draft exists | inferred-with-prose-draft-anchor | citation cleanup + venue shaping |
| Action taxonomy | first compact pass exists | inferred | table tightening |
| Four finalist specs | draft specs exist | inferred | no L3 measurement |
| Cross-spec contract | v2.1 active | inferred-with-L2-usage-anchor | no code-level signal serialization |
| L2 case cards | 13 cards exist | inferred-with-case-card-anchor | manual / proxy only |
| Critic demo story | draft storyboard exists | inferred | not authorized for showing |
| Composer route_regret | L2 + KYKT metadata anchor | inferred-with-real-inventory-anchor | measured sweep missing |
| L3 readiness | 4 briefs exist | inferred | no execution authorization |

## Recommended write order

1. Tighten Section 1 introduction around "control graph, not backbone".
2. Convert the related-work prose into citation-ready paragraphs.
3. Draft the action-vocabulary table.
4. Draft the control-graph figure caption.
5. Insert L2 portfolio table.
6. Add L3 pilot plan as "planned validation", not "results".

## Stop conditions

Stop paper writing and return to planning if any of these happens:

```text
(a) A paragraph needs a measured claim that current artifacts do not have.
(b) VGGT / MapAnything changes the Composer story enough that route_regret
    needs a new L2 addendum before prose can continue.
(c) The title implies a trained Dream3R model rather than a framework.
(d) The paper structure forces final thesis selection before L3 evidence.
```
