"""Unit tests for SpatialMemory and ComposerRouter."""

import torch
from dream3r.modules import SpatialMemory, ComposerRouter
from dream3r.composer_experts import ExpertRegistry


def test_spatial_memory_init():
    mem = SpatialMemory(d_model=64, n_state_tokens=8, bank_capacity=32)
    B = 2
    device = torch.device("cpu")
    state = mem.init_state(B, device)
    assert state.shape == (B, 8, 64)


def test_spatial_memory_forward():
    mem = SpatialMemory(d_model=64, n_state_tokens=8, bank_capacity=32,
                        nsa_n_select_k=4, nsa_n_heads=2, sliding_window=2)
    B, P = 2, 16

    frame_tokens = torch.randn(B, P, 768)
    evidence_flat = torch.randn(B, 17 * 32)
    state = mem.init_state(B, torch.device("cpu"))

    out = mem(frame_tokens, evidence_flat, state)
    assert "latent_state_tokens" in out
    assert "latent_state" in out
    assert "update_kind" in out
    assert "nsa_branch_weights" in out
    assert "bank_occupancy" in out
    assert out["latent_state_tokens"].shape == (B, 8, 64)
    assert out["nsa_branch_weights"].shape[2] == 3


def test_spatial_memory_multi_window():
    mem = SpatialMemory(d_model=64, n_state_tokens=4, bank_capacity=16,
                        nsa_n_select_k=2, nsa_n_heads=2, sliding_window=3)
    B, P = 1, 8
    state = mem.init_state(B, torch.device("cpu"))

    states = []
    for t in range(5):
        frame_tokens = torch.randn(B, P, 768)
        evidence_flat = torch.randn(B, 17 * 32)
        out = mem(frame_tokens, evidence_flat, state)
        state = out["latent_state_tokens"].detach()
        states.append(state)

    assert not torch.allclose(states[0], states[-1]), "States should evolve over windows"

    occ = out["bank_occupancy"]
    assert occ.item() > 0, "Bank should have entries after multiple windows"


def test_spatial_memory_can_disable_nsa_for_ablation():
    mem = SpatialMemory(d_model=64, n_state_tokens=4, bank_capacity=16,
                        nsa_n_select_k=2, nsa_n_heads=2, memory_use_nsa=False)
    B, P = 1, 8
    state = mem.init_state(B, torch.device("cpu"))
    out = mem(torch.randn(B, P, 768), torch.randn(B, 17 * 32), state)

    log = out["memory_retrieval_log"]
    assert log["memory_use_nsa"] is False
    assert log["effective_top_k"] == 0
    assert out["nsa_branch_weights"].shape == (B, P, 3)
    assert torch.allclose(out["nsa_branch_weights"][..., 0], torch.ones(B, P))
    assert torch.allclose(out["nsa_branch_weights"][..., 1:], torch.zeros(B, P, 2))


def test_spatial_memory_can_disable_stable_memory_for_ablation():
    mem = SpatialMemory(d_model=64, n_state_tokens=4, bank_capacity=16,
                        nsa_n_select_k=2, nsa_n_heads=2, enable_stable_memory=False)
    B, P = 1, 8
    state = mem.init_state(B, torch.device("cpu"))
    out = mem(torch.randn(B, P, 768), torch.randn(B, 17 * 32), state)

    log = out["memory_retrieval_log"]
    assert log["enable_stable_memory"] is False
    assert out["write_result"]["n_written"] == 0
    assert out["bank_occupancy"].item() == 0
    assert not log["promoted_to_stable"].any()


def test_spatial_memory_bus_gating():
    mem = SpatialMemory(d_model=64, n_state_tokens=4, bank_capacity=16)
    B, P = 1, 8
    state = mem.init_state(B, torch.device("cpu"))

    out_normal = mem(
        torch.randn(B, P, 768), torch.randn(B, 17 * 32), state,
    )

    state2 = mem.init_state(B, torch.device("cpu"))
    out_gated = mem(
        torch.randn(B, P, 768), torch.randn(B, 17 * 32), state2,
        bus_dynamic_ratio=torch.tensor([[0.95]]),
        bus_conflict_score=torch.tensor([[0.9]]),
    )

    assert out_gated["write_result"]["n_suppressed"] >= out_normal["write_result"]["n_suppressed"]


def test_spatial_memory_gradient():
    mem = SpatialMemory(d_model=64, n_state_tokens=4, bank_capacity=16,
                        nsa_n_select_k=2, nsa_n_heads=2)
    B, P = 1, 8
    state = mem.init_state(B, torch.device("cpu"))

    frame_tokens = torch.randn(B, P, 768, requires_grad=True)
    evidence = torch.randn(B, 17 * 32)

    out = mem(frame_tokens, evidence, state)
    loss = out["latent_state"].sum() + out["latent_drift_proxy"].sum()
    loss.backward()

    assert frame_tokens.grad is not None
    assert not torch.isnan(frame_tokens.grad).any()


def test_composer_router_basic():
    router = ComposerRouter(n_regimes=6, d_routing=32)
    B = 2
    regime = torch.softmax(torch.randn(B, 6), dim=-1)
    out = router(regime)

    assert "capability_match" in out
    assert "route_recommendation" in out
    assert "route_regret" in out
    assert "routing_logits" in out
    assert "selected_expert" in out
    assert out["selected_expert"].shape == (B,)


def test_composer_router_with_confidence():
    router = ComposerRouter(n_regimes=6, d_routing=32)
    B = 2
    regime = torch.softmax(torch.randn(B, 6), dim=-1)
    conf = torch.rand(B, 1)

    out = router(regime, critic_confidence=conf)
    assert "cost_adjusted_scores" in out


def test_composer_router_with_registry():
    reg = ExpertRegistry()
    reg.register_all_defaults()
    router = ComposerRouter(n_regimes=6, d_routing=32, expert_registry=reg)
    router.load_from_registry()

    B = 1
    regime = torch.softmax(torch.randn(B, 6), dim=-1)
    out = router(regime)

    expert_id = out["selected_expert"][0].item()
    images = torch.randn(1, 4, 3, 224, 224)
    expert_out = router.dispatch(expert_id, images)
    assert expert_out is not None
    assert expert_out.pointmap.shape == (1, 4, 196, 3)
    assert "dispatch_latency_ms" in expert_out.metadata
    assert "selected_expert_name" in expert_out.metadata


def test_composer_router_prefers_mast3r_for_static_indoor_without_cost_penalty():
    reg = ExpertRegistry()
    reg.register_all_defaults()
    router = ComposerRouter(n_regimes=6, d_routing=32, cost_alpha=0.0, expert_registry=reg)
    router.load_from_registry()
    with torch.no_grad():
        router.routing_head.weight.zero_()
        router.routing_head.bias.zero_()

    regime = torch.tensor([[1.0, 0.0, 0.0, 0.0, 0.0, 0.0]])
    out = router(regime)
    selected_name = sorted(reg.names)[out["selected_expert"].item()]

    assert selected_name == "mast3r"


def test_composer_router_gradient():
    router = ComposerRouter(n_regimes=6, d_routing=32)
    regime = torch.randn(1, 6, requires_grad=True)
    regime_soft = torch.softmax(regime, dim=-1)
    out = router(regime_soft)
    loss = out["routing_logits"].sum()
    loss.backward()
    assert regime.grad is not None


if __name__ == "__main__":
    test_spatial_memory_init()
    test_spatial_memory_forward()
    test_spatial_memory_multi_window()
    test_spatial_memory_can_disable_nsa_for_ablation()
    test_spatial_memory_can_disable_stable_memory_for_ablation()
    test_spatial_memory_bus_gating()
    test_spatial_memory_gradient()
    test_composer_router_basic()
    test_composer_router_with_confidence()
    test_composer_router_with_registry()
    test_composer_router_prefers_mast3r_for_static_indoor_without_cost_penalty()
    test_composer_router_gradient()
    print("All SpatialMemory + ComposerRouter tests passed.")
