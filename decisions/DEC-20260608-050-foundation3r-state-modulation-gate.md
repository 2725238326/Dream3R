# DEC-20260608-050 - Foundation3R State-Modulation Gate

Date: 2026-06-08
Status: accepted, gate negative

## Decision

Foundation3R is advanced from weak additive state injection to explicit Dream
state modulation, but it is not promotable as a useful independent 3R model
after the 20-epoch GPU1 control gate.

The implemented mechanism is:

```text
VGGT-Omega patch features
+ patch coordinates
+ Dream state FiLM scale/shift
+ additive gated state
-> Transformer multi-view mixer
-> depth-to-pointmap head
```

The trainer also supports a state-contrastive margin loss so correct state is
trained to outperform shuffled state under the same teacher/GT supervision.

## Evidence

Code:

```text
code/dream3r/foundation3r_decoder.py
code/dream3r/scripts/train_foundation3r.py
code/dream3r/tests/test_foundation3r_contract.py
code/dream3r/tests/test_foundation3r_training.py
```

Local tests:

```text
python -B -m pytest --assert=plain code\dream3r\tests\test_foundation3r_contract.py code\dream3r\tests\test_foundation3r_training.py -q
12 passed
```

BUAA-Server tests:

```text
conda run -n dream3r python -B -m pytest --assert=plain dream3r/tests/test_foundation3r_contract.py dream3r/tests/test_foundation3r_training.py -q
12 passed
```

20e VGGT-feature + state-contrast gate on BUAA-Server GPU1:

```text
artifact root: runs/stage6_fusion/foundation3r_state_mod_contrast20_20260608/

state:    KITTI 0.3222, ETH3D 0.1504
no-state: KITTI 0.3392, ETH3D 0.1484
shuffle:  KITTI 0.3500, ETH3D 0.1353
```

Hybrid state retry:

```text
artifact: runs/stage6_fusion/foundation3r_state_mod_hybrid20_20260608/state_seed_7/results.json
state: KITTI 0.4734, ETH3D 0.3271
```

## Interpretation

The mechanism improves the state path on KITTI versus no-state and shuffle, but
ETH3D fails the required causality control because shuffle-state is best. This
means Dream state is still not a reliable geometry control signal in the
proposal-free Foundation3R student.

Therefore:

```text
do not promote Foundation3R as a useful independent 3R model
do not claim proposal-free foundation-model success
do not repeat the same VGGT-feature small decoder with more epochs
```

## Next Required Change

The next proposal-free attempt must change at least one load-bearing axis:

```text
1. train target: real dense pointmap/GT objective that does not collapse under hybrid loss;
2. data: larger and more diverse cache than 50+50 windows;
3. architecture: state tokens must interact through cross-attention or adapter blocks, not only global FiLM;
4. supervision: state must be tied to geometry differences that are visible in the target.
```

If the goal is a usable model today, keep using `v1.1-rc1`. If the goal is a
paper-worthy independent model, Foundation3R needs a stronger representation
and state-supervision redesign.

## Boundaries

No frozen core files were edited. Qwen remains diagnostic-only. VGGT-Omega
remains a visual feature/teacher source, not a universal replacement.
