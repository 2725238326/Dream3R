# L3 Pilot Selection

Last updated: 2026-05-05 (cycle 014 S4)

Status: recommendation; not L3 authorization.

## Purpose

Cycle 013 produced four L3 prerequisite briefs. This file chooses the
first recommended L3 pilot and one backup while preserving all execution
gates.

Inputs:

- `experiments/EXP-20260505-001-l3-prerequisites-critic.md`
- `experiments/EXP-20260505-002-l3-prerequisites-memory.md`
- `experiments/EXP-20260505-003-l3-prerequisites-permanence.md`
- `experiments/EXP-20260505-004-l3-prerequisites-composer.md`
- `cases/CASE-20260505-COMPOSER-05.md`
- `literature/PAPER_PHASE2_BLUEPRINT.md`

## Decision summary

Recommended first L3 pilot:

```text
Critic L3 pilot (EXP-20260505-001)
```

Backup pilot:

```text
Composer route-regret sweep (EXP-20260505-004), but only after the
VGGT capability-card row is included or explicitly excluded with reason.
```

Evidence label: `inferred`.

This is a recommendation, not authorization. A separate user-approved DEC
is required before clone / download / install / run.

## Selection criteria

| Criterion | Meaning |
|---|---|
| Minimal closure size | How small is the first smoke loop? |
| Dependency risk | Number of repos, checkpoint ambiguity, CUDA/env conflict risk |
| Teacher-demo leverage | Does the result strengthen D3 or storyboard readiness? |
| Paper leverage | Does it support a central paper claim? |
| Goal closure leverage | Does it close or materially advance G2 / G6 / G7? |
| Failure interpretability | If the smoke fails, does the failure teach us what to do next? |
| Contract risk | Does it require changing v2.1 signals? |

## Candidate comparison

| Pilot | Minimal closure size | Dependency risk | Teacher-demo leverage | Paper leverage | Goal closure leverage | Failure interpretability | Contract risk | Net |
|---|---|---|---|---|---|---|---|---|
| Critic | small: DUSt3R / MASt3R / Test3R-style loop over one hard case | medium | high: D3 first target is Critic | high: validates verify-then-act loop | advances D3; does not close G2 | high: can distinguish no-conflict, bad reroute, no improvement | low: consumes existing v2.1 Composer signals | best first pilot |
| Composer | medium-to-large: 3+ backbones x 4 regimes | high | medium: supports Composer storyboard but not D3 | very high: direct route_regret evidence | strongest G2 closure path | medium: failures may be env / metric / comparator mix | low: v2.1 schema fits; VGGT row needed | best second pilot |
| Memory | large: streaming workload + two memory-equipped backbones | high | medium | high if it works, but broad | targets G6 | medium-low: failures may be env / workload / threshold | medium: Memory governance externalization remains hard | not first |
| Permanence | large: MonST3R + SAM 2 + CoTracker + clip selection | high | medium-high visually | medium-high | supports F2; no current headline goal closure | medium: clip choice can dominate result | low-to-medium | not first |

## Why Critic first

Critic is the best first L3 pilot because it has the shortest path from
current artifacts to a measurable closed loop:

```text
input hard case -> baseline output -> conflict signal -> Composer-backed
reroute -> revised output -> delta log
```

This pilot directly supports the D3 story:

```text
"Catch a near-failure and repair it on the spot."
```

It also tests the most important integration seam in the four-finalist
graph: Critic must not invent a reroute; it must consume Composer's
`capability_match` / `route_recommendation` under v2.1.

Evidence label: `inferred`. No run has happened.

## Why Composer second

Composer is the most important measured route for G2, but it should not be
the first L3 pilot for two reasons:

1. Its first meaningful sweep is heavier: at least three backbones across
   multiple regimes, with comparable accuracy / latency / cost metrics.
2. Cycle 014 identified a live capability-card gap: VGGT should be added
   or explicitly excluded before a paper-facing route_regret sweep is
   frozen.

Composer should be the second pilot if the user wants measured G2 closure
over teacher-demo speed.

Evidence label: `inferred`.

## Why Memory is deferred

Memory has strong thesis value but weak first-pilot ergonomics. The smoke
requires a streaming workload, at least two memory-equipped backbones, a
budget definition, and a policy-bank stub. Failures could come from
environment setup, workload mismatch, metric mismatch, or the actual
Memory thesis being wrong. That makes it valuable but not the first
execution target.

Memory remains the likely third pilot if Critic + Composer establish the
control-graph story.

## Why Permanence is deferred

Permanence is visually strong and important for F2, but the first L3 smoke
depends on clip selection, segmentation / tracking priors, MonST3R output,
and static-map drift measurement. It is a good demo candidate after the
pipeline has execution muscle, but it is too dependency-heavy as the first
pilot.

## Recommended first-pilot scope

If the user authorizes the Critic pilot later, the first execution DEC
should be narrow:

```text
Goal:
  Produce one JSONL log showing Critic conflict score, Composer-backed
  reroute, and before/after delta on one hard-case input.

Allowed:
  clone / install only the minimum repos listed in EXP-20260505-001;
  download only required checkpoints;
  run one smoke case;
  create a thin wrapper script and log schema.

Not allowed:
  full benchmark sweep;
  training / fine-tuning;
  KYKT navigation change;
  storyboard promotion;
  G2 closure claim;
  final thesis selection.
```

## Acceptance criteria for future Critic L3 execution

A future authorized Critic run should be considered minimally successful
only if all of these exist:

1. a reproducible input reference,
2. a baseline output reference,
3. a logged `conflict_score` or equivalent critic signal,
4. a logged Composer-backed reroute rationale,
5. a revised output reference,
6. a delta metric with sign and scale,
7. a stop-condition note if the delta is not positive.

If any one is missing, the run is an environment smoke, not an L3 evidence
pilot.

## Open user decision for execution

The next execution decision should be phrased as:

```text
Authorize Critic L3 pilot only: clone / install / download / run the
minimum EXP-20260505-001 stack for one hard-case smoke loop, with no
training, no KYKT navigation, no frontend, no storyboard promotion, and
no G2 closure claim.
```

Until the user explicitly approves that, this file remains a planning
artifact only.
