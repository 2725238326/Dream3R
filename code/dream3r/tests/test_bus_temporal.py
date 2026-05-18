"""Unit tests for MemoryBus temporal signal semantics."""

import torch

from dream3r.bus import EvidenceLabel, MemoryBus
from dream3r.model import build_dream3r


def test_reset_rotates_current_signals_to_previous():
    bus = MemoryBus()
    signal = torch.tensor([[0.75]])

    bus.publish("conflict_score", signal, EvidenceLabel.INFERRED, "critic", timestep=3)
    bus.reset()

    assert bus.read("conflict_score", "memory") is None
    previous = bus.read_previous("conflict_score", "memory")
    assert previous is not None
    assert previous.producer == "critic"
    assert previous.timestep == 3
    assert torch.equal(previous.tensor, signal)


def test_contract_log_distinguishes_current_and_previous_reads():
    bus = MemoryBus()
    bus.publish("dynamic_ratio", torch.tensor([[0.2]]), EvidenceLabel.INFERRED,
                "permanence", timestep=0)
    assert bus.read("dynamic_ratio", "memory") is not None

    bus.publish("conflict_score", torch.tensor([[0.9]]), EvidenceLabel.INFERRED,
                "critic", timestep=0)
    bus.reset()
    assert bus.read_previous("conflict_score", "memory") is not None

    current_entry = next(
        entry for entry in bus.get_contract_log()
        if entry["signal"] == "dynamic_ratio"
    )
    previous_entry = next(
        entry for entry in bus.get_contract_log()
        if entry["signal"] == "conflict_score"
    )
    assert current_entry["source"] == "current"
    assert previous_entry["source"] == "previous"


def test_two_window_forward_passes_previous_conflict_to_memory():
    torch.manual_seed(0)
    model = build_dream3r("small")
    model.eval()

    seen_conflict = []
    original_forward = model.memory.forward

    def capture_forward(*args, **kwargs):
        seen_conflict.append(kwargs.get("bus_conflict_score"))
        return original_forward(*args, **kwargs)

    model.memory.forward = capture_forward

    x = torch.randn(1, 4, 16, 768)
    with torch.no_grad():
        out_0 = model(x, timestep=0)
        out_1 = model(x, prev_memory_state=out_0["latent_state_tokens"],
                      prev_object_slots=out_0["object_track_set"], timestep=1)

    assert seen_conflict[0] is None
    assert seen_conflict[1] is not None
    assert torch.equal(seen_conflict[1], out_0["conflict_score"])
    assert any(
        entry["signal"] == "conflict_score"
        and entry["consumer"] == "memory"
        and entry["source"] == "previous"
        for entry in out_1["contract_log"]
    )


if __name__ == "__main__":
    test_reset_rotates_current_signals_to_previous()
    test_contract_log_distinguishes_current_and_previous_reads()
    test_two_window_forward_passes_previous_conflict_to_memory()
    print("All MemoryBus temporal tests passed.")
