"""Tests for the Dream-state-only prior head."""

import torch

from dream3r.state_prior_head import StatePriorHead


def test_state_prior_head_shapes_and_gradients():
    head = StatePriorHead(n_experts=3, d_memory=8, state_dim=12, hidden=24)
    pointmaps = torch.randn(2, 3, 2, 5, 3, requires_grad=True)
    confidences = torch.rand(2, 3, 2, 5, 1, requires_grad=True)
    memory = torch.randn(2, 8, requires_grad=True)
    conflict = torch.randn(2, 1)

    out = head(pointmaps, confidences, memory, conflict)
    loss = out["final_pointmap"].pow(2).mean() + out["final_confidence"].mean()
    loss.backward()

    assert out["final_pointmap"].shape == (2, 2, 5, 3)
    assert out["final_confidence"].shape == (2, 2, 5, 1)
    assert out["expert_weights"].shape == (2, 3, 2, 5)
    assert torch.allclose(
        out["expert_weights"].sum(dim=1),
        torch.ones(2, 2, 5),
        atol=1e-5,
    )
    assert pointmaps.grad is not None
    assert confidences.grad is not None
    assert memory.grad is not None


def test_state_prior_head_no_state_ignores_memory():
    head = StatePriorHead(n_experts=2, d_memory=4, state_dim=8, hidden=16, use_state=False)
    pointmaps = torch.randn(1, 2, 1, 3, 3)
    confidences = torch.rand(1, 2, 1, 3, 1)
    memory_a = torch.randn(1, 4)
    memory_b = torch.randn(1, 4)

    out_a = head(pointmaps, confidences, memory_a, None)
    out_b = head(pointmaps, confidences, memory_b, None)

    assert torch.allclose(out_a["expert_weights"], out_b["expert_weights"])
