"""Tests for per-slot Permanence and CR-2 aggregation."""

import torch

from dream3r.bus import EvidenceLabel, MemoryBus
from dream3r.model import _select_cr2_suppress_mask
from dream3r.modules import Permanence


def test_permanence_returns_per_slot_dynamic_ratio_and_suppress():
    torch.manual_seed(0)
    perm = Permanence(d_input=32, d_slot=16, n_slots=4, n_iters=1)
    out = perm(torch.randn(2, 5, 32))

    assert out["dynamic_ratio"].shape == (2, 4, 1)
    assert out["dynamic_mask_proxy"].shape == (2, 4)
    assert out["dynamic_mask_proxy"].dtype == torch.bool
    assert out["suppress_static_write"].shape == (2, 4)
    assert out["slot_match_indices"].shape == (2, 4)


def test_cr2_prefers_dynamic_mask_final_then_proxy():
    proxy = torch.tensor([[False, True, False]])
    final = torch.tensor([[True, False, False]])

    selected, source = _select_cr2_suppress_mask({
        "dynamic_mask_proxy": proxy,
        "dynamic_mask_final": final,
        "suppress_static_write": torch.zeros(1, 3),
    })
    assert source == "dynamic_mask_final"
    assert torch.equal(selected, final.float())

    selected, source = _select_cr2_suppress_mask({
        "dynamic_mask_proxy": proxy,
        "suppress_static_write": torch.zeros(1, 3),
    })
    assert source == "dynamic_mask_proxy"
    assert torch.equal(selected, proxy.float())


def test_cr2_aggregation_is_not_any_slot_suppress():
    bus = MemoryBus()
    per_slot = torch.tensor([[1.0, 0.0, 0.0, 0.0]])
    bus.publish_handoff("suppress_static_write", per_slot, "permanence", timestep=0)

    assert torch.equal(bus.cr2_per_slot_suppress(), per_slot)
    assert bus.gate_cr2().item() == 0.0

    bus.publish_handoff("suppress_static_write", torch.tensor([[1.0, 1.0, 1.0, 0.0]]),
                        "permanence", timestep=1)
    assert bus.gate_cr2().item() == 1.0


def test_slot_matching_tracks_previous_slot_identity():
    torch.manual_seed(0)
    perm = Permanence(d_input=32, d_slot=16, n_slots=4, n_iters=1)
    first = perm(torch.randn(1, 6, 32))
    second = perm(torch.randn(1, 6, 32), prev_slots=first["object_track_set"])

    assert second["slot_match_indices"].shape == (1, 4)
    assert second["slot_match_indices"].min() >= 0
    assert second["slot_match_indices"].max() < 4
    assert torch.isfinite(second["slot_match_scores"]).all()


def test_cr3_permanence_bias_aggregates_per_slot_dynamic_ratio():
    bus = MemoryBus()
    dyn = torch.tensor([[[0.2], [0.4], [0.6], [0.8]]])
    bus.publish("dynamic_ratio", dyn, EvidenceLabel.INFERRED, "permanence", timestep=0)

    bias = bus.cr3_permanence_bias()
    assert bias.shape == (1, 1)
    assert torch.allclose(bias, torch.tensor([[0.5]]))




def test_slot_matching_is_one_to_one_assignment():
    prev = torch.eye(4).view(1, 4, 4)
    current = prev[:, [2, 0, 3, 1], :]

    indices, scores = Permanence.match_slots(current, prev)

    assert indices.tolist() == [[2, 0, 3, 1]]
    assert torch.allclose(scores, torch.ones_like(scores), atol=1e-6)
    assert len(set(indices[0].tolist())) == 4


def test_anchor_write_uses_per_slot_dynamic_suppress():
    from dream3r.anchor_bank import AnchorBank

    bank = AnchorBank(capacity=8, d_key=8, d_value=8, dynamic_threshold=0.5)
    bank.reset(batch_size=1)
    keys = torch.randn(1, 4, 8)
    values = torch.randn(1, 4, 8)
    dynamic = torch.tensor([[[0.1], [0.9], [0.2], [0.8]]])

    wr = bank.write(keys, values, bus_dynamic_ratio=dynamic)

    assert wr.written_mask.tolist() == [[True, False, True, False]]
    assert wr.n_written == 2
    assert wr.n_suppressed == 2

if __name__ == "__main__":
    test_permanence_returns_per_slot_dynamic_ratio_and_suppress()
    test_cr2_aggregation_is_not_any_slot_suppress()
    test_slot_matching_tracks_previous_slot_identity()
    test_cr3_permanence_bias_aggregates_per_slot_dynamic_ratio()
    test_slot_matching_is_one_to_one_assignment()
    test_anchor_write_uses_per_slot_dynamic_suppress()
    print("All Permanence v2 tests passed.")
