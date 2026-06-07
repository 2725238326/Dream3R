"""Tests for the non-core Dream3R native student decoder gate."""

import torch

from dream3r.native_student_decoder import NativeStudentDecoder
from dream3r.scripts.train_native_student_decoder import (
    _dropout_consistency_loss,
    _scale_drift_loss,
    _temporal_proxy_loss,
    load_state_prior_checkpoint,
)
from dream3r.state_prior_head import StatePriorHead


def test_native_student_decoder_shapes_and_epoch0_teacher_match():
    student = NativeStudentDecoder(
        n_experts=3,
        d_memory=8,
        token_dim=16,
        state_dim=12,
        hidden=24,
        num_layers=1,
        num_heads=4,
        residual_scale=0.05,
    )
    pointmaps = torch.randn(2, 3, 2, 5, 3, requires_grad=True)
    confidences = torch.rand(2, 3, 2, 5, 1, requires_grad=True)
    memory = torch.randn(2, 8, requires_grad=True)
    conflict = torch.randn(2, 1)

    out = student(pointmaps, confidences, memory, conflict)
    loss = out["final_pointmap"].pow(2).mean() + out["final_confidence"].mean()
    loss.backward()

    assert out["final_pointmap"].shape == (2, 2, 5, 3)
    assert out["teacher_pointmap"].shape == (2, 2, 5, 3)
    assert out["dropout_teacher_pointmap"].shape == (2, 2, 5, 3)
    assert out["residual_delta"].shape == (2, 2, 5, 3)
    assert out["final_confidence"].shape == (2, 2, 5, 1)
    assert out["prior_weights"].shape == (2, 3, 2, 5)
    assert out["kept_prior_weights"].shape == (2, 3, 2, 5)
    assert torch.allclose(out["final_pointmap"], out["teacher_pointmap"])
    assert torch.allclose(out["residual_delta"], torch.zeros_like(out["residual_delta"]))
    assert torch.allclose(
        out["kept_prior_weights"].sum(dim=1),
        torch.ones(2, 2, 5),
        atol=1e-5,
    )
    assert pointmaps.grad is not None
    assert confidences.grad is not None
    assert memory.grad is not None


def test_native_student_decoder_proposal_dropout_keeps_teacher():
    student = NativeStudentDecoder(
        n_experts=3,
        d_memory=4,
        token_dim=12,
        state_dim=8,
        hidden=16,
        num_layers=1,
        num_heads=4,
    )
    student.train()
    pointmaps = torch.randn(4, 3, 1, 3, 3)
    confidences = torch.rand(4, 3, 1, 3, 1)
    memory = torch.randn(4, 4)

    out = student(pointmaps, confidences, memory, None, proposal_dropout=1.0)

    assert out["kept_mask"].shape == (4, 3, 1, 1)
    assert torch.all(out["kept_mask"].sum(dim=1) >= 1)
    assert torch.allclose(
        out["kept_prior_weights"].sum(dim=1),
        torch.ones(4, 1, 3),
        atol=1e-5,
    )


def test_load_state_prior_checkpoint_freezes_teacher(tmp_path):
    prior = StatePriorHead(n_experts=2, d_memory=3, state_dim=4, hidden=8)
    with torch.no_grad():
        prior.prior_mlp[-1].bias[:] = torch.tensor([-2.0, 2.0])
    ckpt = tmp_path / "prior.pt"
    torch.save({"state_dict": prior.state_dict()}, ckpt)

    student = NativeStudentDecoder(
        n_experts=2,
        d_memory=3,
        token_dim=8,
        state_dim=4,
        hidden=16,
        num_layers=1,
        num_heads=2,
        prior_hidden=8,
    )
    load_state_prior_checkpoint(student, str(ckpt), torch.device("cpu"), freeze=True)

    assert torch.allclose(student.state_prior.prior_mlp[-1].bias, torch.tensor([-2.0, 2.0]))
    assert not student.state_prior.context_proj.weight.requires_grad
    assert not student.state_prior.prior_mlp[-1].bias.requires_grad


def test_dropout_consistency_loss_detaches_full_output_target():
    dropped = torch.zeros(1, 2, 3, 3, requires_grad=True)
    full = torch.ones(1, 2, 3, 3, requires_grad=True)
    mask = torch.ones(1, 2, 3, dtype=torch.bool)

    loss = _dropout_consistency_loss(dropped, full, mask)
    loss.backward()

    assert dropped.grad is not None
    assert full.grad is None


def test_temporal_and_scale_proxy_losses_backprop_to_prediction():
    pred = torch.tensor(
        [[
            [[0.0, 0.0, 1.0], [0.0, 0.0, 2.0]],
            [[0.0, 0.0, 1.5], [0.0, 0.0, 2.5]],
        ]],
        requires_grad=True,
    )
    target = torch.tensor(
        [[
            [[0.0, 0.0, 1.0], [0.0, 0.0, 2.0]],
            [[0.0, 0.0, 2.0], [0.0, 0.0, 3.0]],
        ]]
    )
    mask = torch.ones(1, 2, 2, dtype=torch.bool)

    loss = _temporal_proxy_loss(pred, target, mask) + _scale_drift_loss(pred, target, mask)
    loss.backward()

    assert torch.isfinite(loss)
    assert pred.grad is not None
