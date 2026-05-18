# Dream3R ablation plan v0.3 addendum (delta on v0.2)

spec_id: SPEC-20260507-002

spec_kind: ablation plan addendum, delta-only (NOT a rewrite of v0.2 or v0.1)

parent_spec: SPEC-20260506-005 (v0.2 ablation plan addendum; preserved unchanged)

parent_decision: DEC-20260507-003 (cycle 023 launch + v0.3 planning addenda + ablation update)

date: 2026-05-07

cycle: 023 (S3 deliverable; per DEC-20260507-003)

status: v0.3 addendum (candidate-not-final per DEC-20260501-004; iteration on v0.2 ablation plan)

honesty_label: every addition below carries an inline evidence label.

linked_artifacts:
- specs/SPEC-20260506-005-dream3r-ablation-plan-v02.md (v0.2; 9 ABL-v02; substrate; NOT restated here)
- specs/SPEC-20260506-002-dream3r-ablation-plan.md (v0.1; 10 ABL; substrate)
- specs/SPEC-20260507-001-dream3r-comparator-map-v02.md (v0.2 comparator; Q1 + Q2 sources)
- specs/SPEC-20260506-004-dream3r-architecture-v02.md (v0.2 architecture; Delta 6 main-claim A+D)
- planning/PLANNING_ADDENDUM_V03_EXPERT_ADAPTER_ABC.md (cycle 023; ExpertAdapter interface)
- planning/PLANNING_ADDENDUM_V03_CHECKPOINT_INVENTORY.md (cycle 023; checkpoint status)
- cycles/CYCLE-20260507-002.md (cycle 022; Path C findings; RA-07 source)

---

## Identity

This spec is a v0.3 addendum on SPEC-005 (v0.2 ablation plan). It adds:

1. ABL-v02-10: Test3R-alone comparator (Q1 from SPEC-20260507-001)
2. Pillar A falsification coverage map (addresses RA-07 from Path C Agent B)
3. ABL-v02-4 VGGT offline-batch baseline annotation (Q2 from SPEC-20260507-001)

It does NOT restate ABL-v02-1..9 from SPEC-005. Those remain canonical.

---

## ABL-v02-10: Test3R-alone comparator

```text
ablation_id:     ABL-v02-10
tests_delta:     SPEC-004 Delta 6 main-claim pillar A
                 (Verification-as-architecture)
v01_relation:    independent (v0.1 had no Test3R-alone comparator)
tier:            1 (load-bearing for pillar A robustness)
evidence_label:  inferred (no existing Test3R-vs-multi-model-Critic comparison)
source:          Q1 from SPEC-20260507-001 (comparator map v0.2);
                 §"Updated threat ranking" — Test3R = HIGH threat
                 to pillar A because its built-in verifier could
                 substitute for Dream3R's Critic + EXPERT-07 path.
```

### Motivation

Test3R (EXPERT-07 in the Composer pool) has a built-in verifier head that enforces
test-time consistency within a single model family. Dream3R's pillar A claims that
verification-as-architecture — a structural Critic gate wired to the bus, driving
Memory retrieval and routing across model families — is superior to single-model
verification.

If Test3R-alone achieves comparable verification quality to the full Dream3R Critic
pipeline, pillar A's novelty claim weakens significantly. ABL-v02-10 tests this
directly.

### Baseline

Full Dream3R v0.2 with:
- C4 Critic head active (A4 verifier + A5 repair classifier)
- CR-1/CR-2 bus gates active
- EXPERT-07 Test3R invoked lazily via Critic (off streaming path)
- NSA selection gate biased by Critic confidence (Delta 3)

### Variant

Test3R-alone: replace the entire Critic → Bus → Expert-07 pipeline with
Test3R's native verification:
- Remove C4 Critic head
- Remove CR-1/CR-2 bus gates
- Run Test3R's built-in verifier on every N-th frame (frequency matched
  to Dream3R's Critic trigger rate for fair comparison)
- Test3R's verification decisions drive Memory write-blocking directly
  (bypassing the bus)

### Test setup

```text
Benchmarks:     B1 (static pair; sanity), B3 (long dynamic video;
                drift detection), B5 (geometric ambiguity; verification
                value), B6 (adversarial CR-triggering; bus verification)
Metrics:        P1 conflict detection rate + false alarm rate (primary);
                P2 anchor retention (secondary); route_regret on B3
                (does routing degrade without Critic-driven confidence?)
Compute:        ~60 GPU-hours per variant on TITAN RTX 24 GB (inferred);
                two variants -> ~120 GPU-hours total. Server-side per F-002.
```

### Expected outcome (evidence label: inferred)

```text
Scenario A (Dream3R wins): Dream3R's Critic + bus pipeline detects more
  conflicts with fewer false alarms than Test3R-alone, especially on B5
  (ambiguity) and B6 (adversarial). Pillar A is validated: architectural
  verification > single-model verification.

Scenario B (Test3R matches): Test3R-alone matches Dream3R on P1 conflict
  detection. Pillar A weakens: the Critic gate's bus wiring and cross-
  model verification add complexity without measurable benefit. v0.4
  would need to either (a) retract pillar A as a paper main claim, or
  (b) demonstrate that Critic-driven routing (A5 repair classifier)
  adds value beyond verification (rerouting to non-Test3R experts).

Scenario C (Test3R wins): Test3R-alone outperforms Dream3R. Pillar A
  is falsified. v0.4 restructures: Test3R becomes the primary verifier;
  Critic module is demoted or removed; pillar A is retracted from
  main claims.
```

### Falsification interpretation

```text
Scenario B is the critical edge case. If Test3R matches on P1 but Dream3R
shows lower route_regret on B3 (because Critic confidence drives Memory
retrieval quality), then pillar A survives in modified form: "verification
improves routing, not just conflict detection." This refinement should be
documented in v0.4 if observed.

Scenario C is clean falsification. No rescue.
```

### Execution gate

```text
Requires separate DEC + per-step micro gates (G_clone / G_install /
G_download / G_run / G_log_use) per F-002. NOT authorized by this spec.
Test3R checkpoint availability: confirmed (see PLANNING_ADDENDUM_V03_
CHECKPOINT_INVENTORY.md). ExpertAdapter interface: specified (see
PLANNING_ADDENDUM_V03_EXPERT_ADAPTER_ABC.md).
```

### Review checklist

```text
[ ] Verify Test3R-alone variant uses SAME input data, SAME evaluation
    benchmarks, SAME metrics as Dream3R baseline (apples-to-apples).
[ ] Verify Test3R verification frequency is matched to Dream3R's Critic
    trigger rate (not every-frame vs. 5%-of-frames comparison).
[ ] Verify Memory retrieval quality is measured in BOTH variants (not
    just conflict detection; route_regret captures routing degradation
    from missing Critic confidence signal).
[ ] Verify B5 + B6 benchmarks are included (these are where Critic
    gate architecture should show its value; B1 + B3 alone are
    insufficient for pillar A claims).
[ ] Verify expected-outcome reasoning covers ALL three scenarios
    (A/B/C) with explicit v0.4 action items per scenario.
[ ] Verify execution gate is intact (no implicit authorization).
[ ] If modifying baseline / variant / metrics, supersede via fresh
    DEC and v0.4 addendum; do NOT edit this section in-place.
```

---

## Pillar A falsification coverage map

Source: RA-07 from Path C Agent B (cycle 022) — "Pillar A lacks dedicated task
in IMPLEMENTATION_ROADMAP; only T-v02-E's CR-1..CR-6 gate triggering test touches it."

This section maps which ablations collectively cover Pillar A
(Verification-as-architecture) claims, closing the coverage gap.

### Pillar A claim decomposition

```text
A-claim-1: Critic gate is a STRUCTURAL write-blocker (CR-1, CR-2)
           → Bus gate activation is observable; removal degrades output.
A-claim-2: Critic confidence biases Memory retrieval (Delta 3 NSA gate)
           → Low confidence retrieves more anchors for verification.
A-claim-3: Test-time verification via EXPERT-07 Test3R is invoked
           lazily only when Critic flags a region
           → Architectural verification, not training-time verification.
A-claim-4: Cross-model-family verification (Critic routes across
           7 experts, not scoped to one model)
           → No existing 3R model does this.
```

### ABL coverage matrix for Pillar A

| Claim | Primary ABL | Secondary ABL | Kill condition |
|---|---|---|---|
| A-claim-1 (Critic gate) | v0.1 ABL-4 (Critic removal) | v0.2 ABL-v02-6 (selection-gate signal subsetting) | Critic removal shows no degradation on B5+B6 |
| A-claim-2 (Critic → Memory retrieval) | v0.2 ABL-v02-6 (selection-gate signal subsetting: remove Critic confidence from gate input) | v0.2 ABL-v02-1 (NSA removal: removes the gate entirely) | Removing Critic confidence from gate shows no retrieval quality change |
| A-claim-3 (Lazy Test3R invocation) | v0.2 ABL-v02-10 (Test3R-alone comparator) | v0.2 ABL-v02-8 (frame-budget benchmark: verifies Test3R is off streaming path) | Test3R-alone matches full pipeline (Scenario B/C) |
| A-claim-4 (Cross-model verification) | v0.2 ABL-v02-10 (Test3R-alone: single-model vs cross-model) | v0.2 ABL-v02-4 (Composer best-of-N: routing quality with/without Critic signal) | Single-model verification matches cross-model |

### Coverage verdict

```text
All 4 Pillar A sub-claims are now covered by at least one primary ABL.
ABL-v02-10 (this addendum) fills the critical gap: A-claim-3 and
A-claim-4 had no direct primary ABL in SPEC-005 v0.2. The v0.1 ABL-4
(Critic removal) is necessary but insufficient alone — it tests
Critic presence, not whether architectural verification beats
single-model verification.

For IMPLEMENTATION_ROADMAP: T-v02-E (integration test) should include
a Pillar A sub-section that maps CR-1..CR-6 gate coverage to these
4 claims. This is a documentation addition, not a new task. Defer to
the next IMPLEMENTATION_ROADMAP v0.3 addendum if one is produced.
```

---

## ABL-v02-4 annotation: VGGT offline-batch baseline

Source: Q2 from SPEC-20260507-001 (comparator map v0.2) — "VGGT-on-offline-batch
baseline for ABL-v02-4 pillar D offline-batch framing gap."

### Annotation on ABL-v02-4 (Composer best-of-N vs single-expert)

```text
v0.2 ABL-v02-4 (SPEC-005 lines 297-396) specifies single-expert
isolation as the primary variant (route every input to one fixed
expert). The variant list should ADDITIONALLY include:

  Variant X (VGGT offline-batch baseline):
    Remove Composer routing entirely. Run VGGT (~1.2B) on the SAME
    benchmark inputs in offline-batch mode (not streaming). Compare
    final 3D reconstruction quality (pointmap accuracy, B1+B2+B4)
    against Dream3R's streaming-first Composer routing over 7
    lightweight experts.

  Purpose: tests whether VGGT's single-pass offline performance
  exceeds Dream3R's routing-based streaming performance on batch
  inputs. If VGGT wins on batch, the honest framing is: "Dream3R's
  pillar D advantage is streaming-specific; on batch inputs, a
  monolithic backbone dominates." This is the VGGT threat
  acknowledged in SPEC-20260507-001 §6.2.

  This variant does NOT require VGGT to fit in the streaming budget.
  VGGT runs as an external baseline at its native batch inference
  mode. VGGT checkpoint (~4.6 GB) is a one-time download; separate
  G_download DEC required.

  Evidence label: inferred. No existing comparison between multi-
  expert routing and VGGT batch exists. Outcome prediction:
  VGGT likely wins on batch pointmap accuracy for static scenes
  (B1+B2); Dream3R should win on B3 (long dynamic; VGGT has no
  state) and B4 (mixed-regime; routing switches experts). This
  is the honest framing for pillar D.
```

This is NOT a new ABL. It is an annotation on ABL-v02-4's variant list. The
implementation cost is incremental: one additional VGGT forward pass per
benchmark input set, plus comparison metrics. Estimated additional compute:
~20 GPU-hours on TITAN RTX (VGGT is heavy but runs only once per benchmark
set, not per ablation variant).

---

## Updated tier placement (v0.3)

```text
Tier 1 (load-bearing):
  ABL-v02-1   NSA-removal                    (unchanged from v0.2)
  ABL-v02-4   Composer best-of-N + VGGT      (VGGT baseline added; tier unchanged)
  ABL-v02-6   Selection-gate signal           (unchanged)
  ABL-v02-10  Test3R-alone comparator         (NEW; tier 1 for pillar A)

Tier 2 (should-run):
  ABL-v02-2..3, ABL-v02-7..8                  (unchanged)

Tier 3 (nice-to-have):
  ABL-v02-5, ABL-v02-9                        (unchanged)
```

ABL-v02-10 is placed in Tier 1 because it directly tests the load-bearing
pillar A claim. If pillar A fails ABL-v02-10 (Scenario B or C), the paper's
main-claim structure must be revised.

---

## Updated compute budget estimate (v0.3 delta)

```text
v0.2 total (SPEC-005):       ~1237 GPU-hours (9 ABLs)
ABL-v02-10 addition:         ~120 GPU-hours (2 variants × 60 GPU-hours)
ABL-v02-4 VGGT baseline:     ~20 GPU-hours (incremental)
v0.3 total:                  ~1377 GPU-hours

All estimates inferred on TITAN RTX 24GB. Server-side per F-002.
```

---

## Updated falsification mapping table (v0.3 delta)

| Main-claim pillar | ABL coverage (v0.3) | Kill condition |
|---|---|---|
| A (Verification-as-architecture) | v0.1 ABL-4 (Critic removal) + v0.2 ABL-v02-6 (selection-gate) + **v0.3 ABL-v02-10 (Test3R-alone)** | Any: no degradation on Critic removal (ABL-4); OR no retrieval quality change on gate subsetting (ABL-v02-6); OR Test3R-alone matches full pipeline (ABL-v02-10 Scenario B/C) |
| D (Heterogeneous best-of-N) | v0.2 ABL-v02-4 (Composer best-of-N) + **v0.3 VGGT baseline** + v0.2 ABL-v02-5 (capability_match) | Any: single-expert matches multi-expert on route_regret (ABL-v02-4); OR VGGT batch beats Dream3R streaming on ALL benchmarks including B3+B4 (VGGT baseline) |
| E (Identity-anchored memory; supporting) | v0.2 ABL-v02-1 (NSA-removal) + ABL-v02-6 (selection-gate) | NSA removal shows no degradation (ABL-v02-1) AND permanence_link removal shows no effect (ABL-v02-6 variant) |

---

## Boundaries (v0.3 addendum delta)

```text
B-v03-A: This addendum does NOT authorize execution of ABL-v02-10
         or VGGT baseline. Each requires a separate DEC + per-step
         micro gates per F-002.
B-v03-B: SPEC-005 v0.2 body is NOT modified. This is a NEW file.
B-v03-C: VGGT checkpoint download requires its own G_download DEC
         (separate from the 7 in-pool expert downloads).
B-v03-D: ABL-v02-10 depends on ExpertAdapter ABC (PLANNING_ADDENDUM_
         V03_EXPERT_ADAPTER_ABC.md) and Test3R checkpoint availability
         (PLANNING_ADDENDUM_V03_CHECKPOINT_INVENTORY.md; confirmed).
```

---

## Discipline notes

```text
- Surgical Edits: NEW file. SPEC-005 v0.2 and SPEC-002 v0.1 bodies
  NOT modified. Same pattern as SPEC-005 on SPEC-002, SPEC-004 on
  SPEC-001, SPEC-20260507-001 on SPEC-003.
- Honesty Override: ABL-v02-10 Scenario C (Test3R wins, pillar A
  falsified) is documented explicitly — no silent absorption. VGGT
  offline-batch baseline is framed honestly: Dream3R's advantage
  may be streaming-specific, not universal.
- Evidence labels: all additions carry inline labels.
- F-002: markdown only; server untouched in cycle 023.
- DEC-20260501-004 + DEC-20260504-002 still in force.
```

---

## Version history

```text
v0.1 (SPEC-20260506-002)  2026-05-06  cycle 016 S3. 10 ABLs.
v0.2 (SPEC-20260506-005)  2026-05-06  cycle 019 S2. 9 ABL-v02 added.
v0.3 (SPEC-20260507-002)  2026-05-07  cycle 023 S3. This file.
                          ABL-v02-10 Test3R-alone comparator (Tier 1;
                          Q1 from comparator map). Pillar A coverage
                          map (RA-07 from Path C). ABL-v02-4 VGGT
                          baseline annotation (Q2). Updated tier
                          placement, compute budget, falsification
                          table. No execution authorized.
```
