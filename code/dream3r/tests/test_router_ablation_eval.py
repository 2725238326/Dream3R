"""Schema tests for Stage 3 router ablation evaluation."""

import json
import tempfile
from pathlib import Path

from dream3r.scripts.eval_router_ablation import evaluate_router_ablation
from dream3r.scripts.train_router_only import train_router_only


def test_eval_router_ablation_reports_baselines_and_success():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        regime_path = root / "regime_labels.json"
        oracle_path = root / "oracle_labels.json"
        ckpt_dir = root / "router"
        output = root / "results.json"

        regime_path.write_text(json.dumps({
            "regime_order": [
                "indoor_static",
                "outdoor_static",
                "dynamic_scene",
                "sparse_view",
                "dense_sequential",
                "feed_forward_manyview",
            ],
            "labels": {
                "dense_a": [0.02, 0.12, 0.05, 0.05, 0.7, 0.06],
                "dense_b": [0.02, 0.12, 0.05, 0.05, 0.68, 0.08],
                "sparse_a": [0.02, 0.15, 0.05, 0.68, 0.05, 0.05],
                "sparse_b": [0.02, 0.15, 0.05, 0.66, 0.07, 0.05],
            },
        }), encoding="utf-8")
        oracle_path.write_text(json.dumps({
            "expert_order": ["fast3r", "mast3r"],
            "labels": {
                "dense_a": 0,
                "dense_b": 0,
                "sparse_a": 1,
                "sparse_b": 1,
            },
            "regime_top": {
                "dense_a": "dense_sequential",
                "dense_b": "dense_sequential",
                "sparse_a": "sparse_view",
                "sparse_b": "sparse_view",
            },
            "metrics": {
                "dense_a": {"fast3r": 0.20, "mast3r": 0.40},
                "dense_b": {"fast3r": 0.22, "mast3r": 0.42},
                "sparse_a": {"fast3r": 0.50, "mast3r": 0.25},
                "sparse_b": {"fast3r": 0.48, "mast3r": 0.23},
            },
            "summary": {"metric": "scale_aligned_abs_rel"},
        }), encoding="utf-8")

        train_router_only(
            regime_labels=str(regime_path),
            oracle_labels=str(oracle_path),
            output_dir=str(ckpt_dir),
            epochs=80,
            lr=0.05,
            batch_size=4,
            d_routing=16,
        )
        result = evaluate_router_ablation(
            regime_labels=str(regime_path),
            oracle_labels=str(oracle_path),
            router_checkpoint=str(ckpt_dir / "latest.pt"),
            output=str(output),
        )

        assert output.exists()
        assert result["success"]["beats_mast3r"]
        assert result["success"]["beats_fast3r"]
        assert result["success"]["correlation_gt_0_3"]
        assert result["success"]["stage3"]
