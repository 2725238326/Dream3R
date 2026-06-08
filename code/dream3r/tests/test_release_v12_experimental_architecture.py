from __future__ import annotations

import pytest
import torch

from dream3r.release_v11 import build_dream3r_v11_release
from dream3r.release_v12_experimental import (
    RELEASE_V12_EXPERIMENTAL_VERSION,
    V12_BRANCH,
    Dream3RV12ExperimentalConfig,
    build_dream3r_v12_experimental,
)


def _tiny_config() -> Dream3RV12ExperimentalConfig:
    return Dream3RV12ExperimentalConfig(
        d_model=16,
        d_memory=16,
        n_state_tokens=4,
        bank_capacity=16,
        nsa_select_k=2,
        nsa_heads=2,
        d_evidence=4,
        d_slot=16,
        n_slots=4,
        d_critic=16,
        d_routing=8,
        n_experts=3,
        proposal_token_dim=16,
        proposal_state_dim=8,
        proposal_hidden=24,
        proposal_num_layers=1,
        proposal_num_heads=2,
    )


def test_v12_experimental_integrates_core_memory_with_proposal_fusion() -> None:
    torch.manual_seed(0)
    model = build_dream3r_v12_experimental(_tiny_config())
    model.eval()

    x = torch.randn(2, 2, 5, 16)
    pointmaps = torch.randn(2, 3, 2, 5, 3)
    confidences = torch.rand(2, 3, 2, 5, 1)

    with torch.no_grad():
        out = model(x, pointmaps, confidences, timestep=0)

    assert out["release_version"] == RELEASE_V12_EXPERIMENTAL_VERSION
    assert out["architecture_branch"] == V12_BRANCH
    assert bool(out["proposal_fusion_enabled"].item()) is True
    assert out["final_pointmap"].shape == (2, 2, 5, 3)
    assert out["final_confidence"].shape == (2, 2, 5, 1)
    assert out["expert_weights"].shape == (2, 3, 2, 5)
    assert out["proposal_fusion_memory_context"].shape == (2, 16)
    assert torch.allclose(
        out["expert_weights"].sum(dim=1),
        torch.ones(2, 2, 5),
        atol=1e-5,
    )
    assert "latent_state_tokens" in out
    assert out["claim_boundary"].startswith("experimental core-integrated")


def test_v12_core_rejects_half_proposal_inputs() -> None:
    model = build_dream3r_v12_experimental(_tiny_config())
    x = torch.randn(1, 2, 4, 16)
    pointmaps = torch.randn(1, 3, 2, 4, 3)

    with pytest.raises(ValueError, match="provided together"):
        model.core(x, proposal_pointmaps=pointmaps, timestep=0)


def test_v12_metadata_keeps_v11_as_fallback() -> None:
    meta = build_dream3r_v12_experimental(_tiny_config()).release_metadata()

    assert meta["version"] == RELEASE_V12_EXPERIMENTAL_VERSION
    assert meta["architecture_branch"] == V12_BRANCH
    assert meta["official_fallback"] == "v1.1.0"
    assert meta["metric_direction"] == "lower_is_better"
    assert "correct-state beats no-state" in " ".join(meta["promotion_gate"])


def test_v12_does_not_replace_v11_official_api() -> None:
    meta = build_dream3r_v11_release().release_metadata()

    assert meta["version"] == "v1.1.0"
    assert meta["release_candidate"] == "domain_conditional_vggt_teacher"
