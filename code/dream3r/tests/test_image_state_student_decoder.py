"""Tests for Dream3R-U1 image/state native student decoder."""

import pytest
import torch

from dream3r.image_state_student_decoder import ImageStateStudentDecoder
from dream3r.scripts.train_image_state_student import _load_image_caches


def test_image_state_student_supports_anchor_and_no_proposal_modes():
    model = ImageStateStudentDecoder(
        n_experts=3,
        d_image=16,
        d_memory=8,
        model_dim=24,
        state_dim=12,
        hidden=32,
    )
    image_tokens = torch.randn(2, 3, 5, 16, requires_grad=True)
    pointmaps = torch.randn(2, 3, 3, 5, 3, requires_grad=True)
    confidences = torch.rand(2, 3, 3, 5, 1, requires_grad=True)
    memory = torch.randn(2, 8, requires_grad=True)
    conflict = torch.randn(2, 1)

    anchored = model(image_tokens, memory, conflict, pointmaps, confidences)
    no_proposal = model(image_tokens, memory, conflict, None, None)
    loss = anchored["final_pointmap"].pow(2).mean() + no_proposal["final_pointmap"].pow(2).mean()
    loss.backward()

    assert anchored["final_pointmap"].shape == (2, 3, 5, 3)
    assert anchored["native_pointmap"].shape == (2, 3, 5, 3)
    assert anchored["anchor_pointmap"].shape == (2, 3, 5, 3)
    assert anchored["final_confidence"].shape == (2, 3, 5, 1)
    assert no_proposal["final_pointmap"].shape == (2, 3, 5, 3)
    assert bool(anchored["has_proposal_anchor"].item()) is True
    assert bool(no_proposal["has_proposal_anchor"].item()) is False
    assert image_tokens.grad is not None
    assert pointmaps.grad is not None
    assert confidences.grad is not None
    assert memory.grad is not None


def test_image_state_student_proposal_dropout_keeps_one_anchor():
    model = ImageStateStudentDecoder(
        n_experts=3,
        d_image=8,
        d_memory=4,
        model_dim=16,
        state_dim=8,
        hidden=24,
    )
    model.train()
    image_tokens = torch.randn(4, 2, 3, 8)
    pointmaps = torch.randn(4, 3, 2, 3, 3)
    confidences = torch.rand(4, 3, 2, 3, 1)
    memory = torch.randn(4, 4)

    out = model(image_tokens, memory, None, pointmaps, confidences, proposal_dropout=1.0)

    assert out["kept_mask"].shape == (4, 3, 1, 1)
    assert torch.all(out["kept_mask"].sum(dim=1) >= 1)
    assert torch.allclose(
        out["kept_prior_weights"].sum(dim=1),
        torch.ones(4, 2, 3),
        atol=1e-5,
    )


def test_image_state_cache_loader_rejects_old_scf_cache(tmp_path):
    old_cache = tmp_path / "old_scf_cache.pt"
    torch.save({
        "d_memory": 4,
        "expert_order": ["a", "b"],
        "entries": [{"memory_context": torch.zeros(4)}],
    }, old_cache)

    with pytest.raises(ValueError, match="no d_image"):
        _load_image_caches([str(old_cache)])
