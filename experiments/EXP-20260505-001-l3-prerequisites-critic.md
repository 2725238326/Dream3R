# EXP-20260505-001: L3 Prerequisites Brief — Critic (Geometry Critic / System-2 3R)

experiment_id: EXP-20260505-001

name: L3 Prerequisites Brief — Critic (SPEC-20260503-001 Geometry Critic)

linked_ru_ids: RU-003, RU-011, RU-012

status:

```text
brief only; not an L3 authorization; gated per AGENT_MASTER_PROMPT.md section 6
```

approval_required:

```text
yes, before cloning / downloading / running anything listed below. Filing
this brief does NOT constitute authorization; a separate user DEC is
required before any repo clone, checkpoint download, install, or run.
```

## Goal

Inventory the minimum prerequisites for producing L3-measured evidence behind the Critic finalist's claim (cross-model A5 reroute action set bound to Composer's `capability_match`). "Minimum" means: what must be in place for a single smoke-test loop that exercises the cross-family boundary Critic claims, not a full ablation sweep.

## Linked Artifacts

- spec: `specs/SPEC-20260503-001-geometry-critic.md`
- contract: `paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md` v2.1 (forward-reference null protocol relevant)
- L2 evidence: `cases/CASE-20260504-CRITIC-01.md`, `CASE-20260504-CRITIC-02.md`, `CASE-20260504-CRITIC-03.md`
- storyboard: `storyboards/STORY-20260505-001-critic.md` (draft; D3 first-demo target per DEC-20260505-001)
- parent decision: `decisions/DEC-20260505-003-cycle-013-launch.md`

## Prerequisite Inventory

### (a) Repos + Checkpoints

Primary (required for Critic smoke test):

```text
Test3R   : https://github.com/nopQAQ/Test3R
  - role: in-family geometric self-check baseline (SRC-2025-007)
  - checkpoint: paper-provided; verify at clone time
  - license: check at clone time

CTRL     : https://github.com/HKUNLP/critic-rl
  - role: cross-domain critic-revision pattern reference (SRC-2025-008;
    LM domain, not 3R; used as pattern template)
  - checkpoint: paper-provided; verify at clone time

DUSt3R   : https://github.com/naver/dust3r
  - role: one of two 3R backbones for cross-family A5 reroute target
    (SRC-2024-001; paper checkpoints linked in repo README)

MASt3R   : https://github.com/naver/mast3r
  - role: second 3R backbone for cross-family reroute (SRC-2024-002;
    shares ecosystem with DUSt3R but distinct matching head)
```

Secondary (useful for contextualizing but not strictly required for first smoke):

```text
TTT3R    : code page claimed per SRC-2025-004; verify URL at clone time
tttLRM   : https://github.com/cwchenwang/tttLRM (SRC-2026-011; cycle-013-mined;
           long-context successor to Test3R / TTT3R)
MASt3R-SfM (SRC-2024-009) and SLAM3R (SRC-2024-010) as pipeline-stage comparators.
```

### (b) GPU / Disk / Compile-Time Budget

All numbers inferred from public model size + repo conventions; NOT measured on any local box. Discipline rule 5 (Honesty Override) requires this label to stay until actual measurement happens.

```text
GPU memory (inference-only smoke):
  DUSt3R / MASt3R pair inference: ~8-12 GB VRAM per forward (inferred
    from repo READMEs; actual varies with image resolution and pair count)
  Test3R consistency objective over triplets: similar order of magnitude,
    +headroom for three simultaneous forwards or sequential with cache
  Single-GPU smoke target: 24 GB class (RTX 3090 / 4090 / A5000 class;
    inferred sufficient, NOT verified locally)

Disk:
  Per-repo clone: 0.5-2 GB code + 1-5 GB checkpoints each
  4-repo total (Test3R + CTRL + DUSt3R + MASt3R): ~20-40 GB
    (inferred; NOT measured)

Compile / env setup time:
  PyTorch + CUDA stack + 4 repos: ~1-2 hours first-time on a clean box
    (inferred from repo README estimates; NOT measured)

Wall-clock for first smoke loop (image pair in, Critic signal out,
Composer reroute, revised output): ~5-20 minutes once env is built
  (inferred; dominated by model load time for first call)
```

### (c) Expected Smoke-Test Path

```text
1. One image pair (or triplet) from a known hard-case source (low-texture
   or symmetry case per CRITIC-01 failure taxonomy).
2. Run DUSt3R -> pointmap A.
3. Run Test3R-style geometric self-check consistency objective over
   triplet / pair -> inconsistency signal S (A5a).
4. If S exceeds threshold theta_critic, issue reroute request to Composer
   (per CRITIC-02 cross-pair with COMPOSER-01).
5. Composer reads `capability_match` for current regime and routes to
   MASt3R -> pointmap B (A5b).
6. Re-run consistency objective on B; compare to A; log delta.

Minimum single success criterion for smoke (L3 evidence for CRITIC-01
only, NOT full paper claim): exists at least one case where delta > 0
and the reroute decision is traceable to the published capability_match.
```

### (d) Minimum Code Change

Treat all four repos as read-only consumers of their own CLI; the Critic-Composer binding is a new thin layer.

```text
new file : dream_critic_loop.py  (~150-300 LOC estimated)
  - orchestrates steps 1-6 above
  - reads capability_match as a YAML table derived from
    cases/CASE-20260505-COMPOSER-01..04.md (paper + KYKT-metadata
    derived; hand-serialized, not programmatically regenerated)
  - calls each repo's inference entry point as subprocess OR via
    `pip install -e` editable installs if APIs permit
  - emits a JSON log line per (input pair, Critic signal, reroute
    decision, revised output, delta)

no edits to Test3R / CTRL / DUSt3R / MASt3R sources unless a specific
API stub is missing — in which case, document the stub in a fork note,
NOT a silent upstream patch.
```

## Evidence Label Discipline

- All GPU / disk / time numbers above are `inferred` (from repo READMEs + public model sizes). None is `measured`. Upgrading to `measured` requires running the smoke test on a specific box and logging the real numbers.
- `capability_match` values consumed by the reroute step are `paper-derived` (COMPOSER-01..03) and `KYKT-metadata-derived` (COMPOSER-04). They are not `measured`. A smoke-test success for CRITIC-01 produces `measured` evidence only for the delta metric; it does NOT retroactively upgrade capability_match labels.
- Running this smoke does NOT close G2 (route_regret closure still requires measured regret on a multi-regime workload, not a single reroute delta).

## Stop Conditions

Any of the following trigger an immediate stop and write-up (not silent abandonment):

```text
(a) Any prerequisite URL above 404s or the repo no longer hosts its
    claimed checkpoint -> record in FRONTIER_SOURCE_MAP.md update queue.
(b) License on any checkpoint or repo prohibits the intended research
    use -> re-scope to license-compatible alternatives; do NOT proceed
    silently.
(c) Smoke-test wall-clock exceeds 10x the inferred estimate -> budget
    event per AGENT_MASTER_PROMPT.md; surface before continuing.
(d) Any env setup requires privileged system changes (driver
    downgrade, system-wide CUDA reinstall, kernel module) -> stop;
    the L3 authorization does not cover system-level changes.
```

## What This Brief Does NOT Authorize

```text
- No clone, no download, no install, no run. Filing the brief is
  inventory. A separate per-finalist DEC (signed off by user) is
  required before any of the above.
- No edits to existing L2 case cards to "pre-populate" measured fields.
- No promotion of the Critic storyboard (STORY-20260505-001) past
  `draft`.
- No closure of G2 via Critic smoke-test alone.
- No KYKT navigation change, no frontend implementation, no teacher-
  demo readiness claim.
```
