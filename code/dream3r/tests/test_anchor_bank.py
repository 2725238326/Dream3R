"""Unit tests for AnchorBank."""

import torch
from dream3r.anchor_bank import AnchorBank


def test_basic_write_read():
    bank = AnchorBank(capacity=16, d_key=32, d_value=32)
    bank.reset(batch_size=1)

    keys = torch.randn(1, 5, 32)
    values = torch.randn(1, 5, 32)
    wr = bank.write(keys, values)
    assert wr.n_written == 5
    assert wr.n_suppressed == 0
    assert bank.occupancy.item() == 5

    queries = torch.randn(1, 3, 32)
    rr = bank.read(queries, top_k=3)
    assert rr.values.shape == (1, 3, 3, 32)
    assert rr.keys.shape == (1, 3, 3, 32)
    assert rr.scores.shape == (1, 3, 3)
    assert rr.source_frame_pose.shape == (1, 3, 3, 4, 4)
    assert rr.source_patch_ids.shape == (1, 3, 3)
    assert rr.points3d_mean.shape == (1, 3, 3, 3)


def test_write_gating_dynamic():
    bank = AnchorBank(capacity=16, d_key=32, d_value=32, dynamic_threshold=0.5)
    bank.reset(batch_size=1)

    wr = bank.write(
        torch.randn(1, 3, 32), torch.randn(1, 3, 32),
        bus_dynamic_ratio=torch.tensor([[0.8]]),
    )
    assert wr.n_written == 0
    assert wr.n_suppressed == 3


def test_write_gating_conflict():
    bank = AnchorBank(capacity=16, d_key=32, d_value=32, conflict_threshold=0.6)
    bank.reset(batch_size=1)

    wr = bank.write(
        torch.randn(1, 4, 32), torch.randn(1, 4, 32),
        bus_conflict_score=torch.tensor([[0.9]]),
    )
    assert wr.n_written == 0


def test_quarantine():
    bank = AnchorBank(capacity=16, d_key=32, d_value=32)
    bank.reset(batch_size=1)

    bank.write(torch.randn(1, 5, 32), torch.randn(1, 5, 32))
    bank.quarantine(torch.tensor([[0, 1, 2]]))
    assert bank.quarantined[0, :3].all()
    assert not bank.quarantined[0, 3:5].any()

    readable = bank.readable_mask[0].sum().item()
    assert readable == 2

    bank.unquarantine(torch.tensor([[1]]))
    assert not bank.quarantined[0, 1].item()
    assert bank.readable_mask[0].sum().item() == 3


def test_capacity_overflow():
    bank = AnchorBank(capacity=4, d_key=16, d_value=16)
    bank.reset(batch_size=1)

    for i in range(3):
        bank.write(torch.randn(1, 2, 16), torch.randn(1, 2, 16))
        bank.tick()

    assert bank.valid[0].sum().item() == 4


def test_prune():
    bank = AnchorBank(capacity=8, d_key=16, d_value=16)
    bank.reset(batch_size=1)

    for i in range(4):
        bank.write(torch.randn(1, 2, 16), torch.randn(1, 2, 16))
        bank.tick()

    assert bank.valid[0].sum().item() == 8
    pr = bank.prune(keep_ratio=0.5)
    assert pr.n_pruned == 4
    assert bank.valid[0].sum().item() == 4


def test_tick_decay():
    bank = AnchorBank(capacity=8, d_key=16, d_value=16, utility_decay=0.9)
    bank.reset(batch_size=1)

    bank.write(torch.randn(1, 2, 16), torch.randn(1, 2, 16),
               confidence=torch.tensor([[1.0, 1.0]]))
    initial_util = bank.utility[0, 0].item()

    bank.tick()
    decayed_util = bank.utility[0, 0].item()
    assert decayed_util < initial_util


def test_batch_operation():
    bank = AnchorBank(capacity=8, d_key=16, d_value=16)
    bank.reset(batch_size=3)

    keys = torch.randn(3, 4, 16)
    values = torch.randn(3, 4, 16)
    wr = bank.write(keys, values)
    assert wr.n_written == 12

    queries = torch.randn(3, 2, 16)
    rr = bank.read(queries, top_k=2)
    assert rr.values.shape == (3, 2, 2, 16)


if __name__ == "__main__":
    test_basic_write_read()
    test_write_gating_dynamic()
    test_write_gating_conflict()
    test_quarantine()
    test_capacity_overflow()
    test_prune()
    test_tick_decay()
    test_batch_operation()
    print("All AnchorBank tests passed.")
