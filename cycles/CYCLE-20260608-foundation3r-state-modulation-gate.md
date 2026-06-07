# Cycle 2026-06-08 - Foundation3R State-Modulation Gate

Status: complete; mechanism implemented, gate negative.

## Trigger

The user identified that the current model lacks clear architectural
distinctiveness and asked to push toward a genuinely useful improved 3R model
today.

## Work Done

Implemented explicit state modulation in the proposal-free Foundation3R line:

```text
state_scale = tanh(Ws(state))
state_shift = Wb(state)
tokens = tokens * (1 + 0.25 * state_scale) + 0.25 * state_shift + gated_state
```

Added trainer support for state-contrastive margin loss:

```text
loss = positive_supervision_loss
     + state_contrast_weight * relu(pos_loss - shuffled_state_loss + margin)
```

Updated tests to assert:

```text
Foundation3R remains proposal-free
VGGT feature decoder uses state modulation
different Dream states change geometry
training result records state-modulation and contrastive-gate parameters
```

## Verification

Local:

```text
12 passed, 7 warnings
```

BUAA-Server:

```text
12 passed, 7 warnings
```

## GPU1 Gate

Contrast teacher-only 20e:

```text
artifact root: runs/stage6_fusion/foundation3r_state_mod_contrast20_20260608/
state:    KITTI 0.3222, ETH3D 0.1504
no-state: KITTI 0.3392, ETH3D 0.1484
shuffle:  KITTI 0.3500, ETH3D 0.1353
```

Hybrid retry 20e:

```text
artifact root: runs/stage6_fusion/foundation3r_state_mod_hybrid20_20260608/
state: KITTI 0.4734, ETH3D 0.3271
```

## Verdict

Negative for promotion. The model has a clearer state-modulated mechanism now,
but the cross-domain control gate fails because ETH3D prefers shuffle-state.

The current usable model remains `v1.1-rc1`. The next Foundation3R step must
change target/data/architecture, not rerun the same small VGGT-feature decoder.
