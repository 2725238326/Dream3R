# Critical Notes: Common Confusions And Deconfusions

Last updated: 2026-05-05 (cycle 013 refresh: Julian Ost AAAI-2026 driving permanence name-collision deconfusion added)

Status: running log of "looks like X is X' but actually" insights.

## Purpose

This file lives between the inventories (`sources/FRONTIER_SOURCE_MAP.md`, `registry/source_registry.md`) and the SPINE files. The inventories say what exists; the SPINE files say what to read in what order; this file says where future readers will trip over commonly-confused mechanisms or borrowed terminology.

Each entry is short on purpose. Long entries usually mean the confusion belongs in a SPINE file's "cross-paper disagreement" section instead.

## Entry Format

```text
### Title (the confusion in one short phrase)

One paragraph note (max 5 sentences).

Linked sources: by registry ID.

Last-updated: YYYY-MM-DD.
```

## Seed Entries (Cycle 008.5)

### Test3R (consistency self-check) is not TTT3R (lightweight train-at-test)

Both Test3R and TTT3R carry a "test-time" label and both target hard cases, but the compute scope differs. Test3R scores consistency between predicted views without modifying state; TTT3R updates a lightweight CUT3R state during inference. Treating them as interchangeable masks an architecture decision: Critic SPEC-20260503-001 takes Test3R-side scope (no state update at verify time), and the cycle 009 case cards must respect that to avoid double-counting "test-time" novelty.

Linked sources: SRC-2025-007 Test3R, SRC-2025-004 TTT3R.

Last-updated: 2026-05-04.

### Mem3R memory != OVGGT memory != Point3R memory

Three memory primitives often grouped as "3R memory" but with different stores. Mem3R uses a hybrid KV cache for tracking + a separate map memory; OVGGT uses a constant-budget anchor cache with dynamic anchor protection; Point3R uses an explicit external spatial pointer. Dream Memory SPEC-20260503-002 does not redefine the store; it defines the *write / read / merge / ignore policy* over an assumed store contract. Conflating these primitives leads readers to expect Dream Memory to publish a fourth store, which it does not.

Linked sources: SRC-2026-003 Mem3R, SRC-2026-007 OVGGT, SRC-2025-003 Point3R.

Last-updated: 2026-05-04.

### POMATO and D2USt3R both extend DUSt3R with dynamics, but differently

POMATO trains on a dynamic-aware loss; D2USt3R uses dynamic-aware token routing. Both produce dynamic pointmaps that look similar at the output level, so they are easy to merge into "dynamic-aware DUSt3R variants" in a related-work sentence. The mechanism differs: loss-side modification vs architecture-side routing. Permanence SPEC-20260503-003 reads either as input but does not borrow either training trick; the contribution is on top of (not beside) these papers.

Linked sources: SRC-2025-010 POMATO, SRC-2025-011 D2USt3R, SRC-2024-001 DUSt3R.

Last-updated: 2026-05-04.

### SLAM3R is a SLAM-shaped consumer of 3R outputs, not a new 3R model family member

SLAM3R uses pointmap predictions inside a sliding-window SLAM front-end. It is downstream of 3R, not a 3R model in the DUSt3R / MASt3R / Fast3R / Spann3R / CUT3R sense. Composer SPEC-20260504-001 capability cards must reflect this: SLAM3R appears in the regime "consumer of 3R outputs", not "static_pair" or "many_view" peer to MASt3R. Treating SLAM3R as a peer inflates the comparator pool with a downstream system, which weakens route_regret claims.

Linked sources: SRC-2024-010 SLAM3R, SRC-2024-001 DUSt3R, SRC-2024-002 MASt3R.

Last-updated: 2026-05-04.

### RayMap3R uses ray representations for dynamics; not a 4D Gaussian variant

The "4D" qualifier on RayMap3R refers to temporal coverage of dynamic scenes, not to 4D Gaussian Splatting. RayMap3R's representation is ray-based, sometimes confused with 4DGS variants because the published demos look graphics-flavored. Permanence SPEC-20260503-003 explicitly excludes 4DGS asset rendering; RayMap3R is allowed as a comparator anchor for the dynamics regime, but it does not import a 4DGS asset path.

Linked sources: SRC-2026-008 RayMap3R, 4DGS variants (cited in SPINE_PERMANENCE).

Last-updated: 2026-05-04.

## Cycle 013 Refresh Entries

### Julian Ost AAAI-2026 "object permanence" is driving-NVS, not Dream Permanence

The shared phrase "object permanence" names two unrelated contributions. Julian Ost's AAAI-2026 paper uses **scene-graph driving generation with explicit object permanence + causal NVS**, where each vehicle is maintained as a persistent node in a scene graph to make generated novel views temporally consistent in the *driving-NVS generative* pipeline. Dream SPEC-20260503-003 Permanence operates on MonST3R's dynamic-mask outputs in a 3R *reconstruction* pipeline and owns `suppress_static_write(r)` handoffs to Memory. The pipelines, evaluation metrics, and signal contracts do not overlap. Cite Julian Ost only as a positioning anchor in related-work (a driving-domain peer that also uses the term); never fold its metrics into Permanence's `identity_consistency` proxy.

Linked sources: SRC-2026-010 Julian Ost AAAI-2026 driving permanence, SPEC-20260503-003, SPINE_PERMANENCE.md Advanced Reading.

Last-updated: 2026-05-05.

### tttLRM is a long-context A1 comparator, not a long-context Test3R

tttLRM (cycle-013-mined) extends the TTT3R axis at the *long-context* reconstructor scale: state updates at inference time on sequence-level drift. Readers who know Test3R + TTT3R may collapse tttLRM into "long-context Test3R", but the Test3R-vs-TTT3R distinction still applies: tttLRM sits on the TTT3R side (state is updated at inference), whereas Test3R sits on the inference-only consistency-scoring side. Critic SPEC-20260503-001 still takes the Test3R-side scope (no state update at verify time); tttLRM enters through SPINE_MEMORY as an A1 long-sequence regime comparator and is cross-noted in SPINE_CRITIC. Conflating tttLRM with Test3R misplaces which spec owns the mechanism.

Linked sources: SRC-2026-011 tttLRM, SRC-2025-007 Test3R, SRC-2025-004 TTT3R, SPEC-20260503-001, SPEC-20260503-002.

Last-updated: 2026-05-05.

### VGGT is a comparator gap in the current Composer capability cards

VGGT (cycle-013-mined) is a feed-forward visual-geometry transformer in the DUSt3R / MASt3R / Fast3R family, but `cases/CASE-20260505-COMPOSER-01..04.md` were all authored before VGGT was surfaced in cycle 013 and do **not** include a VGGT capability_card row. Readers who see the Composer L2 portfolio may assume VGGT was evaluated and omitted; it was not. This is a cycle-014+ per-card revision candidate, not a contract revision — the v2 `capability_card` schema already accommodates a new model row, so no contract change is needed.

Linked sources: SRC-2026-015 VGGT, CASE-20260505-COMPOSER-01..04, SPINE_COMPOSER.md Advanced Reading, `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v2.

Last-updated: 2026-05-05.

## Adding New Entries

- Add when a paper is added to inventories AND it could be confused with an existing comparator.
- Use the entry format above.
- If the entry exceeds 5 sentences, route to the relevant SPINE file's "cross-paper disagreement" section instead.
- Carry the producer's evidence label on each cited source per Discipline rule 5.
