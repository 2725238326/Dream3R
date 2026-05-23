"""Tests for the external memory-conditioned pointmap residual head."""

import torch

from dream3r.memory_pointmap_head import MemoryPointmapResidualHead


def test_memory_pointmap_residual_head_shapes_and_gradients():
    head = MemoryPointmapResidualHead(d_memory=8, hidden_dim=4)
    pointmap = torch.randn(2, 3, 5, 3, requires_grad=True)
    state = torch.randn(2, 4, 8, requires_grad=True)

    corrected, log = head(pointmap, state)
    loss = corrected.pow(2).mean()
    loss.backward()

    assert corrected.shape == pointmap.shape
    assert log["scale"].shape == (2, 3)
    assert log["shift"].shape == (2, 3)
    assert log["blend"].shape == (2, 1)
    assert pointmap.grad is not None
    assert state.grad is not None


def test_memory_pointmap_residual_head_can_blend_previous_window():
    head = MemoryPointmapResidualHead(d_memory=8, hidden_dim=4)
    pointmap = torch.zeros(1, 2, 3, 3)
    state = torch.randn(1, 4, 8)
    prev = torch.ones(1, 2, 3, 3)

    corrected, _ = head(pointmap, state, prev_pointmap=prev, overlap_frames=1)

    assert corrected.shape == pointmap.shape
    assert corrected[:, 0].mean() > 0
