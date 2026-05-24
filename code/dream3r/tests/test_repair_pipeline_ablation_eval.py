"""Schema test for Stage 4 sequence-level repair ablation."""

import json
import tempfile
from pathlib import Path

import torch

from dream3r.scripts.eval_repair_pipeline_ablation import (
    evaluate_repair_pipeline_ablation,
)
from dream3r.scripts.train_critic_only import train_critic_only
from dream3r.scripts.train_router_only import train_router_only


def test_eval_repair_pipeline_ablation_reports_sequence_metrics():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        data_path = root / "critic_data.pt"
        regime_path = root / "regime.json"
        oracle_path = root / "oracle.json"
        critic_dir = root / "critic"
        router_dir = root / "router"
        output = root / "pipeline.json"

        sequences = ["seq_0", "seq_1", "seq_2"]
        expert_order = ["fast3r", "mast3r"]
        regime_labels = {
            "regime_order": [
                "indoor_static",
                "outdoor_static",
                "dynamic_scene",
                "sparse_view",
                "dense_sequential",
                "feed_forward_manyview",
            ],
            "labels": {
                "seq_0": [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                "seq_1": [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                "seq_2": [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            },
        }
        regime_path.write_text(json.dumps(regime_labels), encoding="utf-8")
        oracle_path.write_text(json.dumps({
            "expert_order": expert_order,
            "labels": {"seq_0": 0, "seq_1": 1, "seq_2": 1},
            "metrics": {
                "seq_0": {"fast3r": 0.10, "mast3r": 0.20},
                "seq_1": {"fast3r": 0.30, "mast3r": 0.12},
                "seq_2": {"fast3r": 0.35, "mast3r": 0.14},
            },
        }), encoding="utf-8")

        n = len(sequences) * len(expert_order)
        torch.manual_seed(11)
        evidence = torch.randn(n, 4, 8)
        abs_rel = torch.tensor([0.10, 0.20, 0.30, 0.12, 0.35, 0.14])
        evidence[:, 0, 0] = abs_rel
        pointmap_pair = torch.randn(n, 2, 16, 3) * 0.01
        pointmap_pair[:, 0, :, 2] = abs_rel.view(n, 1)
        pointmap_pair[:, 1, :, 2] = 0.1
        confidence_pair = torch.ones(n, 2, 16, 1)
        repair_action = torch.tensor([0, 0, 3, 0, 3, 0])
        meta = []
        for seq_idx, seq in enumerate(sequences):
            for expert_idx, expert in enumerate(expert_order):
                idx = seq_idx * 2 + expert_idx
                alt = expert_order[1 - expert_idx]
                meta.append({
                    "sequence": seq,
                    "expert": expert,
                    "alt_expert": alt,
                    "abs_rel": float(abs_rel[idx]),
                    "alt_abs_rel": float(abs_rel[seq_idx * 2 + (1 - expert_idx)]),
                    "regime_top": "dynamic_scene",
                })
        torch.save({
            "evidence": evidence,
            "pointmap_pair": pointmap_pair,
            "confidence_pair": confidence_pair,
            "abs_rel": abs_rel,
            "repair_action": repair_action,
            "summary": {
                "expert_order": expert_order,
                "conflict_threshold": 0.2,
                "metric": "scale_aligned_abs_rel",
            },
            "meta": meta,
        }, data_path)

        train_critic_only(
            data_path=str(data_path),
            output_dir=str(critic_dir),
            epochs=40,
            lr=0.01,
            d_critic=16,
            n_heads=2,
            n_layers=1,
        )
        train_router_only(
            regime_labels=str(regime_path),
            oracle_labels=str(oracle_path),
            output_dir=str(router_dir),
            epochs=40,
            lr=0.01,
            d_routing=16,
        )

        result = evaluate_repair_pipeline_ablation(
            data_path=str(data_path),
            regime_labels=str(regime_path),
            critic_checkpoint=str(critic_dir / "latest.pt"),
            router_checkpoint=str(router_dir / "latest.pt"),
            output=str(output),
        )

        assert output.exists()
        assert result["n_sequences"] == 3
        assert "full_pipeline_repair_on" in result["metrics"]
        assert "critic_on_repair_off" in result["metrics"]
        assert "both_off" in result["metrics"]
        assert "t4_3" in result["success"]
