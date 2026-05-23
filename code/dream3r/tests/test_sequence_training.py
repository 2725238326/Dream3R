"""Tests for sequence-level training unroll."""

import torch

from dream3r.data.synthetic import SyntheticSequenceDataset
from dream3r.losses import Dream3RLoss
from dream3r.model import build_dream3r
from dream3r.train import _forward_sequence, collate_synthetic


def _loss_fn():
    return Dream3RLoss(weights={
        "pointmap": 1.0,
        "critic_p1": 0.5,
        "critic_p5": 0.3,
        "memory_p2": 0.3,
        "memory_p3": 0.2,
        "permanence_p4": 0.5,
        "action_entropy": 0.1,
        "retrieval": 0.1,
        "retrieval_quality": 0.05,
        "routing": 0.05,
        "geometric_consistency": 0.1,
        "drift_consistency": 0.1,
        "state_drift_regularization": 0.01,
    })


def test_synthetic_dataset_sequence_shapes():
    ds = SyntheticSequenceDataset(n_sequences=2, n_frames=3, n_patches=8,
                                  sequence_length=3, d_model=768, seed=7)
    sample = ds[0]

    assert sample["features"].shape == (3, 3, 8, 768)
    assert sample["pointmap_gt"].shape == (3, 3, 8, 3)
    assert sample["regime"].shape == (3, 6)
    assert sample["region_label"].shape == (3, 16)


def test_forward_sequence_carries_state_across_windows():
    torch.manual_seed(0)
    model = build_dream3r("small")
    model.eval()

    seen_prev_state = []
    original_forward = model.forward

    def capture_forward(*args, **kwargs):
        seen_prev_state.append(kwargs.get("prev_memory_state"))
        return original_forward(*args, **kwargs)

    model.forward = capture_forward

    ds = SyntheticSequenceDataset(n_sequences=1, n_frames=4, n_patches=8,
                                  sequence_length=3, d_model=768, seed=11)
    batch = collate_synthetic([ds[0]])

    outputs, losses = _forward_sequence(
        model, batch, _loss_fn(), torch.device("cpu"), tbptt_detach_every=1
    )

    assert seen_prev_state[0] is None
    assert seen_prev_state[1] is not None
    assert seen_prev_state[2] is not None
    assert outputs["bank_occupancy"].item() > 0
    assert losses["total"].requires_grad


def test_sequence_training_backward_step():
    torch.manual_seed(0)
    model = build_dream3r("small")
    model.train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

    ds = SyntheticSequenceDataset(n_sequences=1, n_frames=4, n_patches=8,
                                  sequence_length=3, d_model=768, seed=19)
    batch = collate_synthetic([ds[0]])

    optimizer.zero_grad(set_to_none=True)
    _, losses = _forward_sequence(
        model, batch, _loss_fn(), torch.device("cpu"), tbptt_detach_every=1
    )
    losses["total"].backward()
    grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    optimizer.step()

    assert torch.isfinite(grad_norm)


if __name__ == "__main__":
    test_synthetic_dataset_sequence_shapes()
    test_forward_sequence_carries_state_across_windows()
    test_sequence_training_backward_step()
    print("All sequence training tests passed.")
