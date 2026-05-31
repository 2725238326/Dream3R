# CYCLE-20260530 — ProposalSetDecoder server training

date: 2026-05-30
status: active; server background run started
decision: `decisions/DEC-20260530-018-proposal-set-decoder-training-run.md`

## Trigger

The user asked to start training after the Dream3R-PD ProposalSetDecoder
prototype was added and locally verified.

## Actions

1. Synced non-core files to BUAA-Server:
   - `dream3r/proposal_set_decoder.py`
   - `dream3r/scripts/train_proposal_set_decoder.py`
   - `dream3r/tests/test_proposal_set_decoder.py`
   - `dream3r/scripts/run_proposal_set_decoder_sweep.sh`
2. Verified server-side Python compile for the new files.
3. Confirmed GPU 1 was idle before launch.
4. Ran a 1-epoch smoke on existing SCF caches.
5. Started the background sweep on GPU 1.

## Server Run

Root:

```text
/hdd3/kykt26/code/dream3r
```

Output:

```text
/hdd3/kykt26/code/dream3r/runs/stage6_fusion/proposal_set_decoder_sweep/
```

Live logs:

```text
tail -f /hdd3/kykt26/code/dream3r/runs/stage6_fusion/proposal_set_decoder_sweep/progress.log
tail -f /hdd3/kykt26/code/dream3r/runs/stage6_fusion/proposal_set_decoder_sweep/state_seed_7.log
```

Observed active process after restart with live logging:

```text
python -m dream3r.scripts.train_proposal_set_decoder ... --seed 7 --epochs 300
```

## Smoke Result

The smoke loaded:

```text
296 entries
d_memory = 128
experts = fast3r, mast3r, spann3r
```

Epoch 1 result:

```text
KITTI: Ours 0.1482 vs best_single 0.1523
ETH3D: Ours 0.1855 vs best_single 0.1585
```

This is only a runtime smoke, not a convergence result.

## First Full Result

`state_seed_7` completed at 2026-05-30 16:13 server time.

```text
KITTI:  Ours 0.1477 vs best_single 0.1523  (+3.01 pp relative)
ETH3D:  Ours 0.1857 vs best_single 0.1585  (-17.18 pp relative)
```

Interpretation:

```text
ProposalSetDecoder seed 7 gives a stable small KITTI gain but fails ETH3D
cross-domain generalization. This is a mixed result, not a broad positive
claim. Continue seed 11/13 to determine whether the KITTI gain is stable.
```

## Full Sweep Result

The first sweep completed:

```text
state seeds: 7, 11, 13
no-state seeds: 7, 11, 13
shuffle-state seeds: 7, 11, 13
summary: runs/stage6_fusion/proposal_set_decoder_sweep/summary.md
```

Aggregate:

```text
State / KITTI:  0.1478 +/- 0.0004 vs best_single 0.1526 +/- 0.0003
State / ETH3D:  0.1869 +/- 0.0292 vs best_single 0.1715 +/- 0.0269

Shuffle / KITTI: 0.1477 +/- 0.0006
Shuffle / ETH3D: 0.1863 +/- 0.0258

No-state / KITTI: 0.1595 +/- 0.0623
No-state / ETH3D: 0.2125 +/- 0.0741
```

Interpretation:

```text
The v0 decoder has a stable narrow KITTI gain but fails ETH3D and does not
prove Dream-state causality because correct-state and shuffled-state are
effectively tied. The seed-7 no-state win was an outlier; no-state is unstable
across seeds.
```

## State-Bias v1 Follow-up

To address the weak state-causality path, `ProposalSetDecoder` was updated
with a zero-initialized `state_bias_head` that maps Dream state + conflict to
expert-level logits. This keeps the convex output bound but gives state a
direct route into relative expert weights.

Local verification:

```text
python -m pytest code/dream3r/tests/test_proposal_set_decoder.py -q
3 passed
```

Server smoke:

```text
runs/stage6_fusion/proposal_set_decoder_state_bias_smoke_seed7
```

Active follow-up:

```text
runs/stage6_fusion/proposal_set_decoder_state_bias_sweep/state_seed_7
```

State-bias seed-7 result:

```text
Correct-state / KITTI: 0.1470 vs v0 0.1477
Shuffle-state / KITTI: 0.1477

Correct-state / ETH3D: 0.1829 vs v0 0.1857
Shuffle-state / ETH3D: 0.1827
```

Interpretation:

```text
State-bias v1 slightly improves KITTI and slightly improves ETH3D over v0
seed 7, but the correct-state advantage over shuffle-state is tiny on KITTI
and absent on ETH3D. Do not expand to a full v1 sweep before a better state
representation / trained state objective is available.
```

## Boundary

No cache rebuild, checkpoint download, environment mutation, or frozen-core edit
was performed.

## Next Check

Wait for state-bias `state_seed_7/results.json`, then compare against:

```text
runs/stage6_fusion/proposal_set_decoder_sweep/state_seed_7/results.json
runs/stage6_fusion/proposal_set_decoder_sweep/shuffle_state_seed_7/results.json
```

State-bias seed 7 improved over v0 but did not meaningfully separate from
shuffle-state. Stop expanding the v1 sweep and treat Dream-state causality as
not yet solved for ProposalSetDecoder.
