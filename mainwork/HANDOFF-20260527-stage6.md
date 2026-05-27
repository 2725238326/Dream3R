# HANDOFF — Stage 6 Fusion Head (2026-05-27 afternoon)

**To**: next agent picking up Dream3R midterm prep
**From**: claude (this conversation)
**Deadline**: 2026-05-30/31 weekend midterm review
**Days remaining**: ~2 (Thu/Fri) + Sat morning buffer

---

## TL;DR

The Stage 6 fusion head infrastructure is **fully built and exercised**:
module + V04PipelineWithFusion subclass + cache-build + trainer +
5-seed sweep orchestrator. Cache is built, 3/5 training seeds finished
on GPU 1, sweep continues. **But the cached baseline is invalid**:
`build_dream3r("small_real")` never calls `adapter.load_checkpoint()`,
so V04Pipeline's `expert.pointmap` is fallback-stub output (abs_rel
~0.94 KITTI / ~0.53 ETH3D) instead of real expert forward (~0.14-0.16
per DEC-007). The "head improves abs_rel by +60pp" reading is therefore
spurious. The Day 3 task is to fix the baseline and rerun, OR to ship
this as a deeper structural finding.

## Where things live

### New files this session (all synced to server `/hdd3/kykt26/code/dream3r/dream3r/`)

- `code/dream3r/fusion_head.py` — `Stage6FusionHead` module. 42k params.
  Identity-at-init (zero-init final linear; tanh-conflict gate). Inputs:
  `expert_pointmap [B,N,P,3]`, `expert_confidence [B,N,P,1]`,
  `memory_context [B, D_mem]`, `conflict_score [B,1]`.
- `code/dream3r/scripts/v04_pipeline_with_fusion.py` —
  `V04PipelineWithFusion(V04Pipeline)`. Subclass; overrides `forward`
  to swap final `pointmap` for head output via `dataclasses.replace`.
  `orchestrator.py` **not modified**.
- `code/dream3r/scripts/train_fusion_head.py` — three modes:
  - `build-cache`: one `V04Pipeline.forward()` per window, saves
    `(expert_pointmap, expert_confidence, memory_context,
    conflict_score, gt_pointmap, gt_mask, expert_name)` per entry.
  - `train`: loads caches, 80/20 stratified per-domain split (seeded),
    Adam(lr=1e-3), 300 epochs, abs_rel loss with detached scale
    factor; saves `latest.pt` + `results.json`.
- `code/dream3r/scripts/run_stage6_seed_sweep.sh` — idempotent cache +
  5-seed train orchestrator (`seed ∈ {7,11,13,17,19}`, GPU 1).
- `code/dream3r/scripts/smoke_stage6_one_window.py` — single-window
  smoke. **Use this first** to verify any changes — runs in ~30s.

### Server artifacts

```text
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/
├── kitti_cache.pt          (6.6MB, 246 windows, BUT baseline is stub — see below)
├── eth3d_cache.pt          (1.4MB, 50 windows)
├── sweep_main.log          (sweep nohup output)
└── sweep/
    ├── progress.log         (per-step START/OK/FAIL)
    ├── cache_kitti.log
    ├── cache_eth3d.log
    ├── train_s{7,11,13,17,19}.log
    └── seed_{7,11,13,17,19}/
        ├── latest.pt        (head checkpoint + train state)
        └── results.json     (per-seed final eval)
```

Sweep PID on server: 1670160 (was running at 13:44; finishing ~13:55).
To check: `ssh BUAA-Server "ps -p 1670160 -o pid,etime,cmd"`.

### Docs

- `mainwork/midterm/MIDTERM-20260530.md` — midterm report.
  §1-§3 done. §4.1-§4.3 (design + subclass + training setup) done.
  §4.4 (results) drafted with the **baseline pathology caveat** — DO
  NOT take the +60pp numbers at face value when reading.
- `C:\Users\27252\.claude\plans\cheerful-snuggling-puppy.md` — plan
  file with status snapshot.
- This handoff doc.

## The critical bug

Cache shows `expert_name=Counter({'fast3r': 246})`. Two problems
nested:

1. **Random-init router**: `build_dream3r("small_real")` instantiates
   `ComposerRouter` with random weights. Its `selected_expert` is
   essentially constant (whichever index `argmax(random)` lands on at
   init). No external router checkpoint is loaded into
   `model.composer` along the V04Pipeline path. Not a correctness
   blocker for the head experiment (we just always test "improve
   one specific expert"), but reduces meaningful expert diversity.

2. **Adapter checkpoints not loaded**: `build_dream3r` calls
   `self.composer.load_from_registry()` (registers names in the
   `ExpertRegistry`) but **never calls `adapter.load_checkpoint()`**
   on the individual `Fast3RAdapter`/`MASt3RAdapter`/`Spann3RAdapter`
   instances. When `_dispatch_expert` calls
   `self.model.composer.dispatch(expert_id, images, ...)`, the adapter
   forwards through its **deterministic fallback stub path** (see
   `composer_experts/base_adapter.py` for `image_fallback_output`).
   The returned `expert.pointmap` is structured noise, not real
   fast3r depth.

The two existing scripts that DO get real adapter outputs explicitly
call `adapter.load_checkpoint()`:

- `code/dream3r/scripts/build_oracle_expert_labels.py:91-99` →
  `_load_adapter(name)`:
  ```python
  adapter = EXPERT_CLASSES[name]()
  adapter.load_checkpoint()
  if not adapter.is_loaded:
      raise RuntimeError(f"{name} did not load a real checkpoint")
  ```
- `code/dream3r/scripts/build_critic_cache.py:125` — same pattern via
  `_load_adapter` imported from `build_oracle_expert_labels`.

V04Pipeline's `_dispatch_expert` does **not** trigger this. The
adapter instances inside `model.composer.registry` start with
`is_loaded=False` and remain so.

## Day 3 — two paths

### Path A (preferred, ~3-5h): patch + rerun

Goal: get cache to use real loaded adapters. Then sweep on real
baseline.

**Where to patch**: this is delicate because `orchestrator.py` is in
the v0.3 core off-limits list (CLAUDE.md hard rule). Three options
ranked by surgicality:

A.1 **Load adapters externally before passing model to V04Pipeline**
(recommended, no v0.3 edit):

In `train_fusion_head.build_cache`, after `model = build_dream3r(...)`
but before `build_v04_pipeline(model, ...)`, walk
`model.composer.registry` and call `load_checkpoint()` on each
adapter:

```python
model = build_dream3r(preset)
model.eval()
registry = model.composer.registry
for name in registry.names:
    adapter = registry.get(name)
    adapter.load_checkpoint()
    if not adapter.is_loaded:
        raise RuntimeError(f"{name} did not load")
pipeline = build_v04_pipeline(model, max_repair_attempts=1).to(device)
```

Then rerun cache build (~3-5 min KITTI + 1-2 min ETH3D) and sweep
(~25 min for 5 seeds). Total ~30-40 min compute.

A.2 If A.1 reveals the adapter `load_checkpoint()` requires a path
arg or the checkpoints aren't where the build_oracle path expects:
check `composer_experts/fast3r_adapter.py` for default checkpoint
path; the build_oracle path works in production so the default
should be fine, but verify.

A.3 If `registry.names` doesn't return the three expected experts
(fast3r/mast3r/spann3r), check `dream3r.composer_experts.__init__`'s
`ExpertRegistry` setup.

**Expected outcome after A.1 rerun**:

- KITTI baseline abs_rel: ~0.14-0.16 (matching DEC-007 fast3r mean if
  router always picks fast3r; matching the per-window value if mixed).
- ETH3D baseline abs_rel: ~0.16-0.20 (matching dense-GT oracle).
- Head delta: probably ≪ +60pp; **the actual outcome** (positive/null/
  negative) becomes measurable.

### Path B (fallback, ~1-2h): ship the honest finding

If Path A turns out to be more than a 1-line patch (e.g., adapter
load needs args, registry access is non-trivial), document the
**deeper structural finding** as the Day 3 outcome:

> Dream3R's V04Pipeline as constructed by `build_dream3r("small_real")`
> does not load real expert adapters; the depth output is the
> fallback stub. The "Stage 4 ↔ Stage 5 closed loop" tested in
> DEC-008, while wired correctly, also ran through this same
> fallback path. Both DEC-008 and the Stage 6 prototype effectively
> tested "does the architecture help the perception/fallback's
> bad output", not "does it help a real expert". DEC-007's numbers
> (which DO use real adapters via `build_oracle_expert_labels.py`)
> remain the authoritative architecture-vs-single-best evidence.

This is a publishable closure — it explains why DEC-008 saw 0/177
KITTI reroute recommendations from the trained Critic (the Critic
was looking at fallback-stub features). It also tells the next
researcher: **before adding any new architectural component, fix the
adapter-load path in V04Pipeline first**.

Personally I'd push for Path A — 30-40 min compute is cheap relative
to the data quality gain. But B is acceptable if anything in A goes
sideways.

## Closure deliverables (any path)

Write these on Day 3 evening regardless of which path:

1. `decisions/DEC-20260529-009-stage6-fusion-prototype.md`:
   - Honest claim depending on path A/B outcome.
   - Server artifacts list.
   - Limitations.
2. `cycles/CYCLE-20260529-stage6-fusion-prototype.md`:
   - Mirror of DEC content with phase-by-phase narrative.
3. `mainwork.md` §5 — add addendum 5 (Stage 6 prototype outcome).
4. `mainwork/midterm/MIDTERM-20260530.md` §4.4 — finalize numbers,
   §5 — finalize roadmap based on outcome.

## Constraints (don't violate)

- **CLAUDE.md "v0.3/v0.5 core off-limits"**: do not edit `model.py`,
  `anchor_bank.py`, `nsa_attention.py`, `bus.py`, `orchestrator.py`,
  `repair.py`, `modules.py`, `contracts.py`, `config.py`. Path A.1
  works WITHOUT editing any of these.
- **Local Windows = edit + scp only**: never run model code locally;
  ssh BUAA-Server for all execution.
- **Match existing markdown style** (`-` bullets, not `+`); ignore
  MD004-plus lint warnings on the report file.

## Tools cheatsheet

```bash
# Check sweep status
ssh BUAA-Server "tail -30 /hdd3/kykt26/code/dream3r/runs/stage6_fusion/sweep/progress.log"

# Verify cache expert_name distribution
ssh BUAA-Server "cd /hdd3/kykt26/code/dream3r && conda run -n dream3r python -c \"
import torch
from collections import Counter
b = torch.load('runs/stage6_fusion/kitti_cache.pt', map_location='cpu', weights_only=False)
print(Counter(e['expert_name'] for e in b['entries']))
print('first abs_rel via _pointmap_abs_rel against gt for entry 0...')
\""

# Smoke a single window (after any code change)
ssh BUAA-Server "cd /hdd3/kykt26/code/dream3r && CUDA_VISIBLE_DEVICES=1 conda run -n dream3r python -m dream3r.scripts.smoke_stage6_one_window"

# Rebuild cache (after Path A.1 patch)
ssh BUAA-Server "cd /hdd3/kykt26/code/dream3r && CUDA_VISIBLE_DEVICES=1 conda run -n dream3r python -m dream3r.scripts.train_fusion_head build-cache --dataset kitti_long --regime-labels runs/stage3_regime_labels/regime_labels.json --output runs/stage6_fusion/kitti_cache.pt"

# Relaunch sweep (after cache rebuild)
ssh BUAA-Server "cd /hdd3/kykt26/code/dream3r && nohup bash dream3r/scripts/run_stage6_seed_sweep.sh > runs/stage6_fusion/sweep_main_v2.log 2>&1 & echo PID=\$!"
```

## Open questions

1. Does `registry.get(name)` return the same Fast3RAdapter instance
   that `dispatch()` uses? Verify before relying on Path A.1.
2. The `Critic`'s `conflict_score` in the cache is from the
   randomly-initialized model (also a fallback case). Once adapters
   load, conflict_score may also become more meaningful — but
   `model.critic` weights are still random. Worth noting in
   limitations.
3. Whether `memory.fused_context` from random-init memory carries any
   signal at all is unknown. If the head with proper baseline shows
   null result, this is the next thing to investigate.