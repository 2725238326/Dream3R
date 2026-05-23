"""Schema tests for Stage 4 repair ablation evaluation."""

import tempfile
from pathlib import Path

import torch

from dream3r.scripts.eval_repair_ablation import evaluate_repair_ablation
from dream3r.scripts.train_critic_only import train_critic_only


def test_eval_repair_ablation_reports_repair_improvement():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        data_path = root / "critic_data.pt"
        ckpt_dir = root / "critic"
        output = root / "repair.json"

        n = 8
        torch.manual_seed(4)
        evidence = torch.randn(n, 4, 8)
        abs_rel = torch.tensor([0.1, 0.12, 0.15, 0.18, 0.35, 0.38, 0.42, 0.46])
        evidence[:, 0, 0] = abs_rel
        pointmap_pair = torch.randn(n, 2, 16, 3) * 0.01
        pointmap_pair[:, 0, :, 2] = abs_rel.view(n, 1)
        pointmap_pair[:, 1, :, 2] = 0.1
        confidence_pair = torch.ones(n, 2, 16, 1)
        repair_action = torch.tensor([0, 0, 0, 0, 3, 3, 3, 3])
        meta = [
            {
                "sequence": f"seq_{idx}",
                "expert": "fast3r",
                "regime_top": "dynamic_scene",
                "abs_rel": float(abs_rel[idx]),
                "alt_abs_rel": 0.2,
            }
            for idx in range(n)
        ]
        torch.save({
            "evidence": evidence,
            "pointmap_pair": pointmap_pair,
            "confidence_pair": confidence_pair,
            "abs_rel": abs_rel,
            "repair_action": repair_action,
            "summary": {"conflict_threshold": 0.2, "metric": "scale_aligned_abs_rel"},
            "meta": meta,
        }, data_path)

        train_critic_only(
            data_path=str(data_path),
            output_dir=str(ckpt_dir),
            epochs=80,
            lr=0.01,
            d_critic=16,
            n_heads=2,
            n_layers=1,
        )
        result = evaluate_repair_ablation(
            data_path=str(data_path),
            critic_checkpoint=str(ckpt_dir / "latest.pt"),
            output=str(output),
        )

        assert output.exists()
        assert result["success"]["repair_beats_repair_off"]
        assert result["success"]["one_example_gt_5pct"]
