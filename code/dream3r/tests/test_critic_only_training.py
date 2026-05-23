"""Schema tests for Stage 4 critic-only training."""

import tempfile
from pathlib import Path

import torch

from dream3r.scripts.train_critic_only import (
    _contract_to_critic_target,
    _critic_to_contract_action,
    train_critic_only,
)


def test_contract_action_mapping_for_critic_head():
    actions = torch.tensor([0, 1, 3, 4])
    raw = _contract_to_critic_target(actions)
    assert raw.tolist() == [0, 1, 2, 4]
    assert _critic_to_contract_action(raw).tolist() == [0, 1, 3, 4]


def test_train_critic_only_saves_checkpoint_and_beats_action0_baseline():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        data_path = root / "critic_data.pt"
        output_dir = root / "critic_ckpt"
        n = 8
        torch.manual_seed(3)
        evidence = torch.randn(n, 4, 8)
        abs_rel = torch.tensor([0.1, 0.12, 0.15, 0.18, 0.35, 0.38, 0.42, 0.46])
        evidence[:, 0, 0] = abs_rel
        pointmap_pair = torch.randn(n, 2, 16, 3) * 0.01
        pointmap_pair[:, 0, :, 2] = abs_rel.view(n, 1)
        pointmap_pair[:, 1, :, 2] = 0.1
        confidence_pair = torch.ones(n, 2, 16, 1)
        repair_action = torch.tensor([0, 0, 0, 0, 3, 3, 3, 3])

        torch.save({
            "evidence": evidence,
            "pointmap_pair": pointmap_pair,
            "confidence_pair": confidence_pair,
            "abs_rel": abs_rel,
            "repair_action": repair_action,
            "summary": {},
            "meta": [],
        }, data_path)

        summary = train_critic_only(
            data_path=str(data_path),
            output_dir=str(output_dir),
            epochs=80,
            lr=0.01,
            d_critic=16,
            n_heads=2,
            n_layers=1,
        )

        assert summary["repair_action_accuracy"] > summary["baseline_action0_accuracy"]
        assert (output_dir / "latest.pt").exists()
        assert (output_dir / "summary.json").exists()
