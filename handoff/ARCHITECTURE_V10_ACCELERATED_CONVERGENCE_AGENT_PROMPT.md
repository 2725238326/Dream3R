# Dream3R accelerated architecture convergence agent prompt

Use this prompt for the next agent when the goal is to push Dream3R architecture
forward quickly and materially, not to continue small residual-head tweaks.

Release-readiness note, 2026-06-05: the next agent must start from
`decisions/DEC-20260605-037-vggt-omega-cache-control-gate.md` and
`release/DREAM3R_RC_CARD.md`. VGGT-Omega is oracle-positive but release-control
negative; package and verify frozen StatePrior + bounded residual as the RC.

Post-execution note, 2026-06-02: the first native student decoder/distillation
gate has been executed and documented in
`decisions/DEC-20260602-024-native-student-decoder-gate.md`. It is executable
and state-causal but metric-flat versus the bounded baseline. The image-state
U1 follow-up is documented in `decisions/DEC-20260602-025-image-state-native-student-u1.md`
and is negative: correct-state loses to no-state and the locked baseline.
The VGGT-Omega fallback is documented in
`decisions/DEC-20260602-026-vggt-omega-admission-preflight.md`; its smoke script
is ready, but real admission is blocked on the approved checkpoint. On
2026-06-04, `decisions/DEC-20260604-035-vggt-omega-admission-runner.md` added a
resumable staging runner. After user checkpoint upload, the BUAA-Server GPU1
one-window smoke is real-backend admitted. Future agents should not recreate
these scaffolds, rerun U1 unchanged, or repeat the same VGGT-Omega smoke.

```text
You are taking over Dream3R on 2026-06-02.

Workspace: E:\Dream3R
Server repo: /hdd3/kykt26/code/dream3r
Server: ssh BUAA-Server
GPU: CUDA_VISIBLE_DEVICES=1

Your job is to accelerate architecture convergence. Do not reopen broad route
search. Do not spend the session on tiny residual-head variants unless they are
needed as controls. The project needs a usable Dream3R model path.

Mandatory read order:
1. E:\Dream3R\TASK_SNAPSHOT.md
2. E:\Dream3R\decisions\DEC-20260602-023-architecture-acceleration-prompt.md
3. E:\Dream3R\planning\DREAM3R_ARCHITECTURE_ACCELERATION_PLAN_20260602.md
4. E:\Dream3R\decisions\DEC-20260601-022-bounded-prior-refinement.md
5. E:\Dream3R\cycles\CYCLE-20260601-bounded-prior-refinement.md
6. E:\Dream3R\decisions\DEC-20260531-019-state-prior-diagnostic.md
7. E:\Dream3R\decisions\DEC-20260531-020-prior-conditioned-decoder.md
8. E:\Dream3R\decisions\DEC-20260601-021-frozen-prior-decoder-sweep.md
9. E:\Dream3R\specs\SPEC-20260530-005-dream3r-pd-final-architecture.md
10. E:\Dream3R\planning\DREAM3R_PD_FINAL_ARCHITECTURE_PLAN.md
11. E:\Dream3R\planning\DREAM3R_V22_ADMISSION_RUNBOOK.md
12. E:\Dream3R\decisions\DEC-20260602-025-image-state-native-student-u1.md
13. E:\Dream3R\decisions\DEC-20260602-026-vggt-omega-admission-preflight.md
14. E:\Dream3R\decisions\DEC-20260604-035-vggt-omega-admission-runner.md
15. E:\Dream3R\cycles\CYCLE-20260604-vggt-omega-admission-runner.md
16. E:\Dream3R\WORKFLOW_STATUS.md

Current evidence:
- StatePriorHead is positive: Dream state predicts useful expert priors.
- Joint ProposalSetDecoder is negative: it collapses/overrides the state prior.
- Frozen StatePrior is scaffold-positive: it preserves state causality.
- Bounded residual refinement is small-positive and is the current baseline:
  correct-state KITTI/ETH3D = 0.1448/0.1475; shuffle = 0.1521/0.2467.
- Image-state U1 gate20 is negative: correct-state KITTI/ETH3D =
  0.1649/0.2842, no-state = 0.1526/0.1702.
- VGGT-Omega one-window admission is blocked until
  `/hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt` exists.
- The VGGT-Omega admission runner is available at
  `code/dream3r/scripts/stage_vggt_omega_admission.py`; the latest server
  smoke is admitted with `backend=real` and zero fallback contamination.

Architecture target:
Dream3R-AC = proposal teachers + Dream state + frozen StatePrior baseline
           + native student decoder/distillation candidate.

First priority:
Create and execute the smallest gate that can materially change the architecture
claim:
1. Native student decoder/distillation over existing proposal caches, with
   proposal dropout and frozen StatePrior control; or
2. VGGT-Omega one-window teacher admission if native student work is blocked.

Do not:
- do broad architecture brainstorming;
- add another unbounded residual correction;
- train a joint decoder without frozen-prior guardrails;
- claim progress from fallback/stub outputs;
- edit frozen core files without a new explicit DEC.

Frozen core files:
code/dream3r/model.py
code/dream3r/anchor_bank.py
code/dream3r/nsa_attention.py
code/dream3r/bus.py
code/dream3r/orchestrator.py
code/dream3r/repair.py
code/dream3r/modules.py
code/dream3r/contracts.py
code/dream3r/config.py

Concrete first 90 minutes:
1. Verify the two bounded baseline result files on BUAA-Server.
2. Write a short baseline-lock note inside the new cycle or plan.
3. Inspect ProposalSetDecoder / trainer only enough to reuse cache loading.
4. Draft or implement native_student_decoder.py and a one-epoch smoke command.
5. If implementation is too large, produce an execution DEC draft with exact
   files, command, output path, and stop gates, then do the first reversible
   local scaffold/test.

Success criteria for any new run:
- correct-state beats shuffle-state and no-state;
- correct-state matches or beats 0.1448 KITTI / 0.1475 ETH3D baseline;
- fallback/stub contamination is zero;
- temporal_delta_abs_rel and scale_drift_proxy are reported;
- results path is documented.

Final response must include:
- what architecture claim advanced or failed;
- changed files;
- exact commands/results paths;
- tests or verification;
- next single executable gate.

Before ending, update:
TASK_SNAPSHOT.md
WORKFLOW_STATUS.md
INDEX.md
mainwork.md
registry/decision_registry.md
cycle log
```

## Short paste prompt

```text
Read E:\Dream3R\TASK_SNAPSHOT.md, then E:\Dream3R\handoff\ARCHITECTURE_V10_ACCELERATED_CONVERGENCE_AGENT_PROMPT.md. Your task is not to do small residual tweaks. Lock the current bounded frozen-StatePrior baseline, then push one high-impact Dream3R architecture gate: native student decoder/distillation over existing proposal caches, or VGGT-Omega one-window teacher admission if native work is blocked. Preserve state-causality controls, avoid frozen-core edits, use BUAA-Server GPU1 for model code, and update the documented chain before final.
```
