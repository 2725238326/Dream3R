# Dream3R architecture acceleration plan

Date: 2026-06-02
Status: active acceleration plan; first native gate executed
Decision: `decisions/DEC-20260602-023-architecture-acceleration-prompt.md`
Handoff: `handoff/ARCHITECTURE_V10_ACCELERATED_CONVERGENCE_AGENT_PROMPT.md`

## Goal

Move Dream3R from small bounded-head improvements to a usable architecture
milestone that can be defended as a model:

```text
Dream3R-AC = proposal teachers + Dream state + frozen StatePrior baseline
           + native student decoder/distillation candidate
```

The current best bounded model remains the control:

```text
proposal teachers + Dream state
-> frozen trained StatePrior
-> bounded convex fusion
-> disagreement-bounded residual refinement
```

Seed-7 evidence:

| model/control | KITTI | ETH3D | interpretation |
| --- | ---: | ---: | --- |
| frozen-prior baseline | 0.1452 | 0.1480 | causal scaffold |
| bounded residual refinement | 0.1448 | 0.1475 | current best bounded baseline |
| shuffle-state bounded refinement | 0.1521 | 0.2467 | state remains load-bearing |

## What changes now

The next work is not another small mixer sweep. The next work must produce one
of these high-impact outcomes:

1. A native student decoder that beats the bounded frozen-prior baseline while
   keeping state controls.
2. A teacher-bank admission result that raises oracle/proposal diversity enough
   to justify a new cache.
3. A state-objective training result that improves temporal/scale proxies while
   preserving abs_rel.

## Lane A: lock the baseline

Purpose: prevent regressions and prevent agents from reinterpreting weak runs as
architecture progress.

Required baseline:

```text
runs/stage6_fusion/bounded_refine_sweep/frozen_prior_state_seed_7/results.json
runs/stage6_fusion/bounded_refine_sweep/frozen_prior_shuffle_state_seed_7/results.json
```

Success criteria for any new model:

- correct-state beats bounded baseline on at least one domain without regressing
  the other domain beyond noise;
- correct-state beats shuffle-state and no-state;
- fallback/stub proposal contamination remains zero;
- patch-oracle gap, temporal proxy, and scale proxy are reported.

## Lane B: native student decoder first

Purpose: turn proposal-teacher evidence into a Dream3R-owned model.

Recommended first implementation:

```text
code/dream3r/native_student_decoder.py
code/dream3r/scripts/train_native_student_decoder.py
code/dream3r/tests/test_native_student_decoder.py
code/dream3r/scripts/run_native_student_decoder_sweep.sh
```

Design:

- consume cached proposal pointmaps, confidence, Dream state, and frozen
  StatePrior weights;
- train a compact student decoder to predict final pointmap;
- use proposal dropout so the student cannot become a static ensemble copier;
- keep a distillation loss to the bounded frozen-prior output plus supervised
  depth/pointmap loss where available;
- report correct/no-state/shuffle controls.

Kill conditions:

- if no-state or shuffle beats correct-state, stop and diagnose state injection;
- if the student only copies the best single expert, stop and strengthen
  proposal dropout or state prior supervision;
- if it cannot match bounded baseline, keep it as negative evidence, not a model
  claim.

## Lane C: teacher-bank admission only if it changes the bound

Purpose: avoid blind expert search while still allowing stronger proposal
teachers.

Allowed candidates:

- VGGT-Omega first;
- CUT3R second if VGGT-Omega deployment stalls;
- MonST3R only for dynamic/temporal cases.

Admission gate:

1. one-window real-backend smoke;
2. adapter output normalized to the existing proposal schema;
3. oracle/proposal-diversity comparison against MASt3R/Fast3R/Spann3R;
4. cache build only if the candidate improves at least one oracle/diversity
   metric or covers a known failure regime.

## Lane D: state objective, not state concatenation

Purpose: make Dream state useful beyond expert-prior selection.

Targets:

- temporal_delta_abs_rel;
- scale_drift_proxy;
- patch_oracle_gap_pp;
- prior entropy calibration.

Recommended direction:

```text
train a state projection / calibration head against temporal and scale proxies,
then feed it into the native student decoder as an explicit control signal.
```

Do not repeat DEC-020's joint-prior collapse pattern.

## 24-hour execution shape

1. Read the mandatory files in the V10 handoff.
2. Verify the bounded baseline results and write a one-page baseline lock note.
3. Implement or draft the native student decoder gate.
4. Run a one-epoch smoke locally/server-side only when the command, output path,
   and expected files are documented.
5. If native smoke is blocked, execute the VGGT-Omega one-window admission draft
   instead of inventing another residual-head variant.

## Output contract

Every next agent must end with:

- changed files;
- exact command/results paths;
- whether the architecture claim advanced, stayed flat, or failed;
- next single executable gate;
- updated `TASK_SNAPSHOT.md`, `WORKFLOW_STATUS.md`, `INDEX.md`,
  `mainwork.md`, decision registry, and cycle log.

## Execution addendum: DEC-20260602-024

The first native student decoder/distillation gate has been executed:

```text
decision: decisions/DEC-20260602-024-native-student-decoder-gate.md
cycle:    cycles/CYCLE-20260602-native-student-decoder-gate.md
server:   /hdd3/kykt26/code/dream3r/runs/stage6_fusion/native_student_decoder_gate20_seed7/
```

Result:

| control | KITTI | ETH3D | fallback contamination |
| --- | ---: | ---: | ---: |
| native student correct-state | 0.1451 | 0.1480 | 0 |
| native student no-state | 0.1557 | 0.1730 | 0 |
| native student shuffle-state | 0.1525 | 0.2468 | 0 |

Interpretation: state causality is preserved, but the native student is
metric-flat versus the frozen StatePrior teacher and does not beat the locked
bounded baseline of 0.1448 / 0.1475. The next native gate should change the
training objective, not recreate the scaffold or run another small residual
sweep.
