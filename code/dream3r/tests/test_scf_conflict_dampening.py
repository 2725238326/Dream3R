from __future__ import annotations

import torch

from dream3r.scf_head import SCFHead


def test_conflict_dampening_scales_logits_toward_uniform_softmax() -> None:
    logits = torch.tensor([[[[3.0]], [[0.0]], [[-3.0]]]])
    conflict = torch.tensor([[1.0]])

    damped = SCFHead._apply_conflict_dampening(logits, conflict, 0.5)

    assert torch.allclose(damped, logits * 0.5)
    original_weights = torch.softmax(logits, dim=1)
    damped_weights = torch.softmax(damped, dim=1)
    uniform = torch.full_like(original_weights, 1.0 / logits.shape[1])
    assert (damped_weights - uniform).abs().mean() < (
        original_weights - uniform
    ).abs().mean()


def test_conflict_dampening_zero_strength_is_identity() -> None:
    logits = torch.randn(2, 4, 3, 5)
    conflict = torch.rand(2, 1)

    assert torch.equal(SCFHead._apply_conflict_dampening(logits, conflict, 0.0), logits)


def test_conflict_dampening_keeps_forward_contract() -> None:
    head = SCFHead(n_experts=4, d_memory=32, conflict_dampening_strength=0.35)
    pointmaps = torch.randn(2, 4, 2, 5, 3)
    confidences = torch.rand(2, 4, 2, 5, 1)
    memory = torch.randn(2, 32)
    conflict = torch.ones(2, 1)

    out = head(pointmaps, confidences, memory, conflict)

    assert out["final_pointmap"].shape == (2, 2, 5, 3)
    assert out["final_confidence"].shape == (2, 2, 5, 1)
    assert out["expert_weights"].shape == (2, 4, 2, 5)
    assert torch.allclose(out["expert_weights"].sum(dim=1), torch.ones(2, 2, 5))
