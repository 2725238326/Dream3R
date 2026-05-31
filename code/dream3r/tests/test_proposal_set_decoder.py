"""Tests for the non-core Dream3R-PD proposal-set decoder."""

import torch

from dream3r.proposal_set_decoder import ProposalSetDecoder
from dream3r.scripts.train_proposal_set_decoder import _load_state_prior_checkpoint
from dream3r.state_prior_head import StatePriorHead


def test_proposal_set_decoder_shapes_and_gradients():
    decoder = ProposalSetDecoder(
        n_experts=3,
        d_memory=8,
        token_dim=16,
        state_dim=12,
        hidden=24,
        num_layers=1,
        num_heads=4,
    )
    pointmaps = torch.randn(2, 3, 2, 5, 3, requires_grad=True)
    confidences = torch.rand(2, 3, 2, 5, 1, requires_grad=True)
    memory = torch.randn(2, 8, requires_grad=True)
    conflict = torch.randn(2, 1)

    out = decoder(pointmaps, confidences, memory, conflict)
    loss = out["final_pointmap"].pow(2).mean() + out["uncertainty"].mean()
    loss.backward()

    assert out["final_pointmap"].shape == (2, 2, 5, 3)
    assert out["final_confidence"].shape == (2, 2, 5, 1)
    assert out["expert_weights"].shape == (2, 3, 2, 5)
    assert out["state_prior_weights"].shape == (2, 3)
    assert out["uncertainty"].shape == (2, 2, 5, 1)
    assert torch.allclose(
        out["expert_weights"].sum(dim=1),
        torch.ones(2, 2, 5),
        atol=1e-5,
    )
    assert pointmaps.grad is not None
    assert confidences.grad is not None
    assert memory.grad is not None


def test_proposal_set_decoder_supports_no_state_ablation():
    decoder = ProposalSetDecoder(
        n_experts=2,
        d_memory=4,
        token_dim=8,
        state_dim=8,
        hidden=16,
        num_layers=1,
        num_heads=2,
        use_state=False,
    )
    pointmaps = torch.randn(1, 2, 1, 3, 3)
    confidences = torch.rand(1, 2, 1, 3, 1)
    memory = torch.randn(1, 4)

    out = decoder(pointmaps, confidences, memory, None)

    assert out["final_pointmap"].shape == (1, 1, 3, 3)
    assert torch.isfinite(out["final_pointmap"]).all()


def test_proposal_set_decoder_state_can_shift_expert_prior():
    decoder = ProposalSetDecoder(
        n_experts=2,
        d_memory=3,
        token_dim=8,
        state_dim=4,
        hidden=16,
        num_layers=1,
        num_heads=2,
    )
    with torch.no_grad():
        decoder.context_proj.weight.fill_(0.0)
        decoder.context_proj.bias.fill_(0.0)
        decoder.state_bias_head.weight.fill_(0.0)
        decoder.state_bias_head.bias[:] = torch.tensor([3.0, -3.0])

    pointmaps = torch.randn(1, 2, 1, 4, 3)
    confidences = torch.rand(1, 2, 1, 4, 1)
    memory = torch.randn(1, 3)
    out = decoder(pointmaps, confidences, memory, torch.zeros(1, 1))

    assert out["expert_weights"][:, 0].mean() > out["expert_weights"][:, 1].mean()


def test_proposal_set_decoder_state_prior_branch_can_shift_weights():
    decoder = ProposalSetDecoder(
        n_experts=2,
        d_memory=3,
        token_dim=8,
        state_dim=4,
        hidden=16,
        num_layers=1,
        num_heads=2,
        prior_hidden=8,
    )
    with torch.no_grad():
        decoder.context_proj.weight.fill_(0.0)
        decoder.context_proj.bias.fill_(0.0)
        decoder.state_bias_head.weight.fill_(0.0)
        decoder.state_bias_head.bias.fill_(0.0)
        decoder.state_prior_mlp[-1].weight.fill_(0.0)
        decoder.state_prior_mlp[-1].bias[:] = torch.tensor([-3.0, 3.0])

    pointmaps = torch.randn(1, 2, 1, 4, 3)
    confidences = torch.rand(1, 2, 1, 4, 1)
    memory = torch.randn(1, 3)
    out = decoder(pointmaps, confidences, memory, torch.zeros(1, 1))

    assert out["state_prior_weights"][:, 1].mean() > out["state_prior_weights"][:, 0].mean()
    assert out["expert_weights"][:, 1].mean() > out["expert_weights"][:, 0].mean()


def test_load_state_prior_checkpoint_can_freeze_prior(tmp_path):
    prior = StatePriorHead(n_experts=2, d_memory=3, state_dim=4, hidden=8)
    with torch.no_grad():
        prior.prior_mlp[-1].bias[:] = torch.tensor([-2.0, 2.0])
    ckpt = tmp_path / "prior.pt"
    torch.save({"state_dict": prior.state_dict()}, ckpt)

    decoder = ProposalSetDecoder(
        n_experts=2,
        d_memory=3,
        token_dim=8,
        state_dim=4,
        hidden=16,
        num_layers=1,
        num_heads=2,
        prior_hidden=8,
    )
    _load_state_prior_checkpoint(decoder, str(ckpt), torch.device("cpu"), freeze=True)

    assert torch.allclose(decoder.state_prior_mlp[-1].bias, torch.tensor([-2.0, 2.0]))
    assert not decoder.context_proj.weight.requires_grad
    assert not decoder.state_prior_mlp[-1].bias.requires_grad
