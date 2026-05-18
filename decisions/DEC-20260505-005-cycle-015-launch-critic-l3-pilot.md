# DEC-20260505-005 cycle 015 launch and Critic L3 pilot scope authorization

decision_id: DEC-20260505-005

date: 2026-05-05

status: locked

cycle: 015 (launches cycle 015; closes the launch handoff from cycle 014)

parents:
- DEC-20260505-004-cycle-014-launch.md (cycle 014 launch)
- DEC-20260505-001-cycle-011-launch-and-d3-demo-target.md (D3 = Critic)
- DEC-20260505-003-cycle-013-launch.md (Phase 2 prep + research)

linked_artifacts:
- planning/L3_PILOT_SELECTION.md (recommends Critic first; Composer backup)
- experiments/EXP-20260505-001-l3-prerequisites-critic.md (the prereq inventory)
- specs/SPEC-20260503-001-geometry-critic.md
- paradigm/CROSS_SPEC_SIGNAL_CONTRACT.md v2.1
- cases/CASE-20260504-CRITIC-01.md, CASE-20260504-CRITIC-02.md, CASE-20260504-CRITIC-03.md
- storyboards/STORY-20260505-001-critic.md (still draft; not promoted by this DEC)
- TASK_SNAPSHOT.md (sync chain head)
- cycles/CYCLE-20260505-006.md (cycle 015 log)

## One line summary

Cycle 015 is launched. The user authorizes the Critic L3 pilot scope as written in `planning/L3_PILOT_SELECTION.md` "Recommended first-pilot scope". The authorization is scope-level only. Each operational step (clone, checkpoint download, install, run) remains a per-step micro-gate that requires a separate user go in the active conversation before execution.

## What the user authorized

User message in this session:

```text
"授权 Critic L3 窄域 pilot"
```

selected as the cycle 015 entry. This satisfies the open user decision phrased in `planning/L3_PILOT_SELECTION.md` line 167-171:

```text
Authorize Critic L3 pilot only: clone / install / download / run the
minimum EXP-20260505-001 stack for one hard-case smoke loop, with no
training, no KYKT navigation, no frontend, no storyboard promotion, and
no G2 closure claim.
```

Evidence label for this DEC: user-decided. The DEC text itself records that decision; no L3 evidence is produced or claimed by this DEC.

## Allowed by this DEC

Scope locked to:

```text
1. Clone the minimum repos listed in EXP-20260505-001 section (a) Primary:
     Test3R, CTRL, DUSt3R, MASt3R.
   Secondary repos (TTT3R / tttLRM / MASt3R-SfM / SLAM3R) are NOT in scope.
2. Download only the checkpoints required for one smoke loop on a single
   hard-case input (DUSt3R + MASt3R + Test3R-style checkpoint; CTRL is a
   pattern reference, no checkpoint expected for the smoke).
3. Install the minimum env (PyTorch + CUDA + 4 repos) on a single box.
4. Run one smoke loop end-to-end:
     image pair (or triplet) -> DUSt3R pointmap A -> Test3R-style
     consistency signal S -> if S > theta_critic, Composer-backed reroute
     to MASt3R -> pointmap B -> consistency on B -> delta log.
5. Create the thin orchestration wrapper dream_critic_loop.py and a
   capability_match YAML hand-derived from cases/CASE-20260505-COMPOSER-
   01..04.md.
6. Emit one JSONL log line per (input, S, reroute decision, revised
   output, delta) for one hard-case input.
```

## Not allowed by this DEC

```text
1. No full benchmark sweep across multiple regimes / backbones beyond
   the DUSt3R / MASt3R pair plus Test3R-style consistency.
2. No training, no fine-tuning, no LoRA, no parameter updates of any
   kind.
3. No KYKT navigation change. No frontend implementation. No reusable
   Codex skill packaging.
4. No promotion of STORY-20260505-001 (Critic storyboard) past `draft`.
5. No G2 closure claim from this pilot. G2 still requires measured
   route_regret on a multi-regime workload, not a single-case delta.
6. No retroactive edits to existing L2 case cards (CRITIC-01..03,
   COMPOSER-01..05, MEMORY-*, PERMANENCE-*) to "pre-populate" measured
   fields.
7. No retiring of any non-finalist track. No final thesis selection.
8. No teacher-demo readiness claim.
9. No system-level changes (no driver downgrade, no system-wide CUDA
   reinstall, no kernel module change). Per EXP-20260505-001 stop
   condition (d).
10. No silent upstream patches to Test3R / CTRL / DUSt3R / MASt3R.
    Required API stubs go in a fork note, not a silent upstream edit.
```

## Per step micro gates that still require user go

Even though scope is authorized, each of the following operational steps requires a separate user "go" in the active conversation, immediately before that step is taken. The agent will surface a brief gate message and wait. Treat each as a hard gate; not having a per-step go means do not take that step.

```text
G_clone     :  "go to clone these 4 repos under <path>?"
                <path> is proposed by the agent on the gate message;
                user can accept or redirect.
G_install   :  "go to create the conda / venv env and pip install ...?"
G_download  :  "go to download these specific checkpoint files
                (size estimate) from these specific URLs?"
G_run       :  "go to run the smoke loop on hard case <X>?"
                <X> is proposed by the agent based on CRITIC-01 failure
                taxonomy; user can accept or redirect.
G_log_use   :  "go to commit the smoke JSONL log under
                experiments/runs/... and update CASE-20260504-CRITIC-01
                evidence label?"
                Updating CRITIC-01 from inferred to measured is a
                separate edit-time gate.
```

If any micro gate fails (user says no, or redirects), the cycle does NOT proceed to the next step; the agent stops, records the gate result in the cycle log, and waits.

## Stop conditions inherited from EXP-20260505-001

```text
(a) Any prerequisite URL above 404s or the repo no longer hosts its
    claimed checkpoint -> stop; record in
    sources/FRONTIER_SOURCE_MAP.md update queue;
    surface to user before continuing.
(b) License on any checkpoint or repo prohibits the intended research
    use -> stop; re-scope to license-compatible alternatives;
    do NOT proceed silently.
(c) Smoke-test wall-clock exceeds 10x the inferred estimate
    (5-20 min inferred, so 200 min stop) -> budget event per
    AGENT_MASTER_PROMPT.md; stop and surface.
(d) Any env setup requires privileged system changes (driver
    downgrade, system-wide CUDA reinstall, kernel module) -> stop;
    this DEC does not cover system-level changes.
```

Additional cycle-015 specific stop conditions:

```text
(e) If any micro gate above returns "no" or "redirect", stop the
    relevant step and surface; do not proceed.
(f) If any output file would land outside the agreed pilot path
    (proposed at G_clone), stop and surface.
(g) If the smoke loop completes but produces no `delta` value with
    sign and scale (per EXP-20260505-001 acceptance criteria 6), it
    is an env smoke, not an L3 evidence pilot; record as such and
    do NOT claim CRITIC-01 evidence upgrade.
```

## Acceptance criteria

A cycle 015 pilot run is considered minimally successful as L3 evidence (not full paper claim) only if all 7 of the EXP-20260505-001 acceptance items exist:

```text
1. a reproducible input reference,
2. a baseline output reference,
3. a logged conflict_score or equivalent critic signal,
4. a logged Composer-backed reroute rationale,
5. a revised output reference,
6. a delta metric with sign and scale,
7. a stop-condition note if the delta is not positive.
```

Missing any one means the run is environment-smoke, not L3-evidence. Even on full success, the result upgrades CRITIC-01 evidence label only; G2 stays gated; storyboard stays draft; teacher-demo readiness stays unclaimed.

## Evidence labels in cycle 015 outputs

```text
- All env / GPU / disk / wall-clock numbers in the EXP-20260505-001
  brief stay `inferred` until measured on this box; one successful run
  upgrades only the items it actually measured.
- capability_match values consumed by the Composer-backed reroute
  remain `paper-derived` (COMPOSER-01..03) and `KYKT-metadata-derived`
  (COMPOSER-04). The smoke does NOT retroactively upgrade them.
- The delta metric upgrades to `measured` only on the specific input
  pair actually run; CRITIC-01 single-case smoke does NOT upgrade
  CRITIC-01 broadly.
```

Honesty Override (Discipline rule 5) requires every L3 cycle 015 output to carry the right label.

## Cycle 015 subtask board (this DEC sets the seed)

```text
S1  Write this DEC                                  -> done by this commit
S2  Write cycles/CYCLE-20260505-006.md (cycle log)  -> in_progress
S3  Update TASK_SNAPSHOT.md FIRST per F-001 rule 6  -> pending
S4  Sync chain: WORKFLOW_STATUS, RESEARCH_STATE,
    INDEX, registry/decision_registry              -> pending
S5  Surface G_clone gate to user                    -> pending
[S6..Sk reserved for execution sub-passes; each
 entered only after the matching micro gate]
```

The cycle 015 cycle log (`CYCLE-20260505-006.md`) tracks S1..Sk in detail.

## Sync chain anchors

This DEC is referenced from:

```text
- TASK_SNAPSHOT.md  -> Open user decisions; cycle 015 launch decision
- WORKFLOW_STATUS.md -> Current cycle pointer
- RESEARCH_STATE.md  -> Active cycle and active gates
- INDEX.md           -> Decisions index row
- registry/decision_registry.md -> Registry row
- cycles/CYCLE-20260505-006.md  -> Cycle 015 log
```

## Discipline notes

```text
- Surgical Edits: only cycle 014 closeout + this DEC + the cycle 015
  log + the sync chain are touched. No prior cycle log, case card,
  spec, contract, or storyboard is rewritten.
- Honesty Override: this DEC produces zero L3 evidence; every claim
  here carries `inferred` or `user-decided` label; no measurement
  claim is made.
- F-001 anti-32MB: TASK_SNAPSHOT.md is updated FIRST in the sync
  chain. Edits use Edit (diff-only), not Write. Active context
  large-file count stays <= 2.
```
