"""W17 state recurrence contract tests."""

import torch

from dream3r.config import config_to_model_args, load_config
from dream3r.model import Dream3R
from dream3r.modules import (
    MambaHybridRecurrence,
    StateTokenRecurrence,
    build_state_recurrence,
)


def test_cross_attention_recurrence_factory_preserves_shape():
    recurrence = build_state_recurrence(
        "cross_attention", d_model=16, n_state_tokens=4, n_heads=2
    )
    prev_state = torch.randn(2, 4, 16)
    frame_tokens = torch.randn(2, 6, 16)
    out = recurrence(prev_state, frame_tokens)

    assert isinstance(recurrence, StateTokenRecurrence)
    assert out.shape == prev_state.shape
    assert torch.isfinite(out).all()


def test_config_threads_state_recurrence_type_to_model():
    cfg = load_config(overrides={
        "state_recurrence_type": "cross_attention",
        "use_backbone": False,
    })
    args = config_to_model_args(cfg)
    model = Dream3R(args)

    assert args["state_recurrence_type"] == "cross_attention"
    assert model.memory.state_recurrence_type == "cross_attention"


def test_mamba_hybrid_recurrence_factory_preserves_shape():
    recurrence = build_state_recurrence(
        "mamba_hybrid", d_model=16, n_state_tokens=4, n_heads=2
    )
    prev_state = torch.randn(2, 4, 16)
    frame_tokens = torch.randn(2, 6, 16)
    out = recurrence(prev_state, frame_tokens)

    assert isinstance(recurrence, MambaHybridRecurrence)
    assert recurrence.backend in {"mamba_ssm", "pytorch_selective_scan"}
    assert out.shape == prev_state.shape
    assert torch.isfinite(out).all()


def test_mamba_hybrid_threads_into_dream3r_forward():
    torch.manual_seed(0)
    cfg = load_config(overrides={
        "state_recurrence_type": "mamba_hybrid",
        "use_backbone": False,
    })
    model = Dream3R(config_to_model_args(cfg))
    model.eval()

    with torch.no_grad():
        out = model(torch.randn(1, 4, 16, 768), timestep=0)

    assert model.memory.state_recurrence_type == "mamba_hybrid"
    assert out["memory_retrieval_log"]["state_recurrence_type"] == "mamba_hybrid"
    assert out["latent_state_tokens"].shape == (1, cfg["n_state_tokens"], cfg["d_memory"])


if __name__ == "__main__":
    test_cross_attention_recurrence_factory_preserves_shape()
    test_config_threads_state_recurrence_type_to_model()
    test_mamba_hybrid_recurrence_factory_preserves_shape()
    test_mamba_hybrid_threads_into_dream3r_forward()
    print("All state recurrence factory tests passed.")
