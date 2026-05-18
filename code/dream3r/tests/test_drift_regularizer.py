"""Tests for W14 Grassmannian state drift regularization."""

import torch

from dream3r.config import load_config, config_to_model_args
from dream3r.model import Dream3R
from dream3r.modules import StateTokenRecurrence


def _parallel_energy(prev_state, next_state):
    delta = next_state - prev_state
    denom = prev_state.pow(2).sum(dim=-1, keepdim=True).clamp_min(1e-8)
    parallel = prev_state * (delta * prev_state).sum(dim=-1, keepdim=True) / denom
    return parallel.pow(2).sum(dim=-1).mean()


def test_grassmannian_regularizer_reduces_parallel_drift():
    torch.manual_seed(0)
    prev_state = torch.randn(2, 5, 16)
    parallel_update = prev_state * 0.5
    orthogonal_noise = torch.randn_like(prev_state) * 0.05
    next_state = prev_state + parallel_update + orthogonal_noise

    regularized = StateTokenRecurrence.grassmannian_regularize(
        prev_state, next_state, strength=0.8
    )

    assert _parallel_energy(prev_state, regularized) < _parallel_energy(prev_state, next_state)


def test_zero_strength_is_identity():
    prev_state = torch.randn(1, 3, 8)
    next_state = torch.randn(1, 3, 8)
    regularized = StateTokenRecurrence.grassmannian_regularize(
        prev_state, next_state, strength=0.0
    )
    assert torch.equal(regularized, next_state)


def test_config_threads_grassmannian_strength_to_model():
    cfg = load_config(preset="small", overrides={"grassmannian_strength": 0.35})
    args = config_to_model_args(cfg)
    assert args["grassmannian_strength"] == 0.35

    model = Dream3R(args)
    assert model.memory.state_recurrence.grassmannian_strength == 0.35

    x = torch.randn(1, 2, 8, 768)
    out = model(x)
    assert torch.isfinite(out["latent_state_tokens"]).all()


if __name__ == "__main__":
    test_grassmannian_regularizer_reduces_parallel_drift()
    test_zero_strength_is_identity()
    test_config_threads_grassmannian_strength_to_model()
    print("All drift regularizer tests passed.")
