"""Tests for Critic repair action feedback loop."""

import torch

from dream3r.bus import EvidenceLabel, MemoryBus
from dream3r.model import build_dream3r
from dream3r.modules import Critic


def test_high_conflict_recommends_increase_retrieval():
    critic = Critic(n_evidence=2, d_evidence=4, d_critic=8, n_heads=2, n_layers=1)
    for p in critic.parameters():
        p.data.zero_()
    critic.conflict_head.bias.data.fill_(8.0)

    out = critic(torch.zeros(1, 2, 4))
    assert out["recommended_action"].item() == 1


def test_previous_repair_action_increases_memory_retrieval():
    torch.manual_seed(0)
    model = build_dream3r("small")
    model.eval()
    model.bus.publish("recommended_action", torch.tensor([[1.0]]),
                      EvidenceLabel.INFERRED, "critic", timestep=0)

    with torch.no_grad():
        out = model(torch.randn(1, 4, 16, 768), timestep=1)

    assert out["memory_retrieval_log"]["effective_top_k"] >= 16
    assert out["repair_action_log"]["increase_retrieval"] is True


def test_previous_reroute_action_reaches_composer_log():
    torch.manual_seed(0)
    model = build_dream3r("small")
    model.eval()
    model.bus.publish("recommended_action", torch.tensor([[2.0]]),
                      EvidenceLabel.INFERRED, "critic", timestep=0)

    with torch.no_grad():
        out = model(torch.randn(1, 4, 16, 768), timestep=1)

    assert out["repair_action_log"]["reroute"] is True
    assert any(
        entry["signal"] == "recommended_action"
        and entry["consumer"] == "composer"
        and entry["source"] == "previous"
        for entry in out["contract_log"]
    )


def test_cr1_blocks_reroute_when_capability_spread_is_low():
    bus = MemoryBus()
    bus.publish("capability_match", torch.ones(1, 7), EvidenceLabel.INFERRED,
                "composer", timestep=0)
    cr1 = bus.gate_cr1()

    critic = Critic(n_evidence=2, d_evidence=4, d_critic=8, n_heads=2, n_layers=1)
    for p in critic.parameters():
        p.data.zero_()
    critic.repair_head.bias.data[2] = 10.0

    out = critic(torch.zeros(1, 2, 4), cr1)
    assert out["recommended_action"].item() != 2




def test_previous_noop_action_is_consumed_as_noop():
    torch.manual_seed(0)
    model = build_dream3r("small")
    model.eval()
    model.bus.publish("recommended_action", torch.tensor([[0.0]]),
                      EvidenceLabel.INFERRED, "critic", timestep=0)

    with torch.no_grad():
        out = model(torch.randn(1, 4, 16, 768), timestep=1)

    log = out["repair_action_log"]
    assert log["noop"] is True
    assert log["increase_retrieval"] is False
    assert log["reroute"] is False
    assert log["implemented_actions"] == [0, 1, 2]

if __name__ == "__main__":
    test_high_conflict_recommends_increase_retrieval()
    test_previous_repair_action_increases_memory_retrieval()
    test_previous_reroute_action_reaches_composer_log()
    test_previous_noop_action_is_consumed_as_noop()
    test_cr1_blocks_reroute_when_capability_spread_is_low()
    print("All Critic loop tests passed.")
