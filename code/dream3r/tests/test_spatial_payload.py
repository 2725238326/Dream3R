"""Tests for AnchorBank spatial payload storage and retrieval."""

import torch

from dream3r.anchor_bank import AnchorBank
from dream3r.model import build_dream3r
from dream3r.modules import SpatialMemory


def test_anchor_bank_writes_and_reads_spatial_payload():
    bank = AnchorBank(capacity=8, d_key=4, d_value=4)
    bank.reset(batch_size=1)

    keys = torch.randn(1, 3, 4)
    values = torch.randn(1, 3, 4)
    poses = torch.eye(4).view(1, 1, 4, 4).repeat(1, 3, 1, 1)
    poses[0, :, 0, 3] = torch.tensor([1.0, 2.0, 3.0])
    patch_ids = torch.tensor([[10, 11, 12]])
    points = torch.tensor([[[1.0, 0.0, 0.0],
                            [0.0, 2.0, 0.0],
                            [0.0, 0.0, 3.0]]])

    bank.write(keys, values, source_frame_pose=poses,
               source_patch_ids=patch_ids, points3d_mean=points)
    rr = bank.read(torch.randn(1, 1, 4), top_k=3)

    expected_points = bank.points3d_mean.gather(
        1, rr.indices.reshape(1, -1).unsqueeze(-1).expand(-1, -1, 3)
    ).view(1, 1, 3, 3)
    expected_patch_ids = bank.source_patch_ids.gather(1, rr.indices.reshape(1, -1)).view(1, 1, 3)

    assert torch.equal(rr.points3d_mean, expected_points)
    assert torch.equal(rr.source_patch_ids, expected_patch_ids)
    assert rr.source_frame_pose.shape == (1, 1, 3, 4, 4)


def test_anchor_bank_spatial_payload_survives_quarantine_and_prune():
    bank = AnchorBank(capacity=4, d_key=4, d_value=4)
    bank.reset(batch_size=1)

    points = torch.arange(12, dtype=torch.float32).view(1, 4, 3)
    bank.write(torch.randn(1, 4, 4), torch.randn(1, 4, 4),
               points3d_mean=points, source_patch_ids=torch.tensor([[0, 1, 2, 3]]))
    bank.quarantine(torch.tensor([[0, 1]]))
    assert torch.equal(bank.points3d_mean[0, 0], points[0, 0])

    bank.prune(keep_ratio=0.5)
    assert bank.valid[0].sum().item() == 2
    assert torch.equal(bank.points3d_mean[0, ~bank.valid[0]], torch.zeros(2, 3))


def test_spatial_memory_logs_written_and_retrieved_payloads():
    torch.manual_seed(0)
    mem = SpatialMemory(d_model=32, n_state_tokens=4, bank_capacity=16,
                        nsa_n_select_k=2, nsa_n_heads=2, sliding_window=2)
    B, P = 1, 8
    state = mem.init_state(B, torch.device("cpu"))
    pointmap = torch.arange(B * P * 3, dtype=torch.float32).view(B, P, 3)

    out_0 = mem(torch.randn(B, P, 768), torch.randn(B, 17 * 32), state,
                t2_pointmap=pointmap)
    out_1 = mem(torch.randn(B, P, 768), torch.randn(B, 17 * 32),
                out_0["latent_state_tokens"].detach(), t2_pointmap=pointmap)

    log = out_1["memory_retrieval_log"]
    assert log["retrieved_points3d_mean"].shape == (B, P, 2, 3)
    assert log["retrieved_source_patch_ids"].shape == (B, P, 2)
    assert log["retrieved_source_frame_pose"].shape == (B, P, 2, 4, 4)
    assert log["written_points3d_mean"].shape == (B, min(8, P), 3)


def test_model_output_contains_memory_spatial_payload_log():
    torch.manual_seed(0)
    model = build_dream3r("small")
    model.eval()
    x = torch.randn(1, 4, 16, 768)

    with torch.no_grad():
        out = model(x)

    log = out["memory_retrieval_log"]
    assert "retrieved_points3d_mean" in log
    assert "written_points3d_mean" in log


if __name__ == "__main__":
    test_anchor_bank_writes_and_reads_spatial_payload()
    test_anchor_bank_spatial_payload_survives_quarantine_and_prune()
    test_spatial_memory_logs_written_and_retrieved_payloads()
    test_model_output_contains_memory_spatial_payload_log()
    print("All spatial payload tests passed.")
