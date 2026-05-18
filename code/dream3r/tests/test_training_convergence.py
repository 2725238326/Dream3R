"""Short overfit check for sequence training with advanced losses enabled."""

import torch

from dream3r.data.synthetic import SyntheticSequenceDataset
from dream3r.losses import Dream3RLoss
from dream3r.model import build_dream3r
from dream3r.train import _forward_sequence, collate_synthetic


def test_short_sequence_training_loss_trends_down():
    torch.manual_seed(3)
    model = build_dream3r("small")
    model.train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.0)
    loss_fn = Dream3RLoss(weights={
        "pointmap": 1.0,
        "critic_p1": 0.0,
        "critic_p5": 0.0,
        "memory_p2": 0.0,
        "memory_p3": 0.0,
        "permanence_p4": 0.0,
        "action_entropy": 0.0,
        "retrieval": 0.01,
        "retrieval_quality": 0.001,
        "routing": 0.01,
        "geometric_consistency": 0.01,
        "drift_consistency": 0.0,
        "state_drift_regularization": 0.001,
    })
    ds = SyntheticSequenceDataset(n_sequences=1, n_frames=3, n_patches=8,
                                  sequence_length=2, d_model=768, seed=31)
    batch = collate_synthetic([ds[0]])
    losses = []

    for _ in range(5):
        optimizer.zero_grad(set_to_none=True)
        _, loss_dict = _forward_sequence(
            model, batch, loss_fn, torch.device("cpu"), tbptt_detach_every=1
        )
        loss = loss_dict["total"]
        assert torch.isfinite(loss)
        losses.append(loss.item())
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()

    assert min(losses[1:]) < losses[0]
    assert losses[-1] <= losses[0]


if __name__ == "__main__":
    test_short_sequence_training_loss_trends_down()
    print("Short sequence training convergence test passed.")
