# DEC-20260508-001: Cycle 024 — v0.2 server-side scaffold (T-v02-A repo skeleton)

decision_id:    DEC-20260508-001
date:           2026-05-08
cycle:          024
status:         accepted
authorized_by:  user "授权" 2026-05-08 (G_run gate; user also provided SSH credentials)
decision_type:  server-side code task execution (T-v02-A)
parent_decision: DEC-20260507-003 (cycle 023; post-023 trajectory: cycle 024 first server-side code task)

---

## Context

All v0.2/v0.3 markdown deliverables complete (cycles 016–023). Cycle 024 is the first
server-side code task: T-v02-A repo scaffold on 172.17.140.97 under /hdd3/kykt26/code/dream3r/.

Cycle 015 (Critic L3 pilot) was bypassed: its v0.1 smoke loop design is obsolete under v0.2.
The infrastructure it built (dream3r conda env, shallow clones) is reused.

## Scope

Server: 172.17.140.97 (kykt26@; SSH via BUAA-Server alias + id_rsa_buaa key).
Env: dream3r conda env (Python 3.10, PyTorch + CUDA).
GPU: TITAN RTX 24GB × 4 (use GPU 0 only; leave 1-3 for other users per lab rules).
Path: /hdd3/kykt26/code/dream3r/dream3r/

### Deliverables

1. `composer_experts/` subdirectory with:
   - `base.py`: ExpertAdapter ABC (per PLANNING_ADDENDUM_V03_EXPERT_ADAPTER_ABC.md)
   - `__init__.py`: expert registry with get_expert() + available_experts()
   - 7 adapter stubs (mast3r/fast3r/spann3r/cut3r/moge2/depthanything_v2/test3r)
   - Error protocol: CheckpointNotFoundError / ExpertForwardError / ExpertOutputError

2. `memory_anchor_bank.py`: bounded anchor bank (K=256; LRU eviction; permanence protection)

3. `nsa_attention.py`: NSA three-branch selective retrieval (compressed / selected-topk / sliding)
   with Critic confidence bias on gate weights

4. `bench_frame_budget.py`: per-component latency benchmark with pass/fail thresholds
   (per PLANNING_ADDENDUM_V03_LATENCY_THRESHOLDS.md)

### Verification

- v0.1 smoke_test.py: PASSED (all bus signals, loss, backward, CR-1 gate, memory carry-over)
- v0.2 integrated smoke test: PASSED (AnchorBank + NSA + all 7 adapters on GPU 0)

### Not done

- DINOv3-S backbone substitution in modules.py (T-v02-C1; separate task)
- C2 Memory integration of AnchorBank + NSA into MemorySSM (T-v02-C2-mem-bank; separate task)
- No checkpoint downloads
- No training

## Cycle 026 correction note

The "Not done" section above records the initial DEC scope for cycle 024. The later `cycles/CYCLE-20260508-001.md` version-history tail records additional same-cycle work beyond this initial scaffold scope, including real adapter deployment, one DepthAnything-V2 checkpoint download, and a synthetic training dry-run.

Per DEC-20260508-002, those later cycle 024 events are treated as engineering smoke / implementation-baseline evidence only. They do not validate C2 memory quality, reconstruction quality, routing quality, pillar A, pillar D, or the later C2 Memory v0.3 design. `SPEC-20260508-001` supersedes the v0.2 GRU/vector AnchorBank/NSA path as the current C2 memory research direction.

## Discipline

- F-002 honored: all code at /hdd3/kykt26/; GPU 0 only; dream3r conda env
- Lab rules honored: no data/models in home; GPU 0 only (1-3 free)
- v0.1 code NOT modified (additive only)

## Version history

```text
v1  2026-05-08  cycle 024. First server-side code task. T-v02-A
                scaffold: composer_experts/ + memory_anchor_bank +
                nsa_attention + bench_frame_budget. Both smoke tests
                passed.
v1.1 2026-05-08  cycle 026 correction note. Initial DEC scope preserved,
                but later cycle 024 log tail records additional adapter,
                checkpoint, and synthetic dry-run work. Evidence bounded
                to engineering smoke per DEC-20260508-002.
```
