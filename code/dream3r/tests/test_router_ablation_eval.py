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
        assert result["success"]["beats_best_single"]
        assert result["success"]["correlation_gt_0_3"]
        assert result["success"]["stage3"]


def test_eval_router_ablation_supports_stage5_three_experts():
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
                "dense_a": [0.01, 0.08, 0.04, 0.04, 0.78, 0.05],
                "dense_b": [0.01, 0.08, 0.04, 0.04, 0.76, 0.07],
                "sparse_a": [0.02, 0.12, 0.04, 0.70, 0.06, 0.06],
                "sparse_b": [0.02, 0.12, 0.04, 0.68, 0.08, 0.06],
                "dynamic_a": [0.02, 0.12, 0.70, 0.06, 0.04, 0.06],
                "dynamic_b": [0.02, 0.12, 0.68, 0.08, 0.04, 0.06],
            },
            "stats": {
                "dense_a": {"frame_count": 100, "depth_mean": 15, "valid_ratio": 0.3, "depth_temporal_change": 0.01, "oxts_available": 1, "mean_speed": 2, "speed_std": 0.5},
                "dense_b": {"frame_count": 110, "depth_mean": 16, "valid_ratio": 0.3, "depth_temporal_change": 0.02, "oxts_available": 1, "mean_speed": 2, "speed_std": 0.6},
                "sparse_a": {"frame_count": 70, "depth_mean": 11, "valid_ratio": 0.2, "depth_temporal_change": 0.01, "oxts_available": 1, "mean_speed": 1, "speed_std": 0.2},
                "sparse_b": {"frame_count": 75, "depth_mean": 12, "valid_ratio": 0.2, "depth_temporal_change": 0.02, "oxts_available": 1, "mean_speed": 1, "speed_std": 0.3},
                "dynamic_a": {"frame_count": 150, "depth_mean": 18, "valid_ratio": 0.4, "depth_temporal_change": 0.08, "oxts_available": 1, "mean_speed": 8, "speed_std": 2.0},
                "dynamic_b": {"frame_count": 155, "depth_mean": 17, "valid_ratio": 0.4, "depth_temporal_change": 0.09, "oxts_available": 1, "mean_speed": 9, "speed_std": 2.1},
            },
        }), encoding="utf-8")
        oracle_path.write_text(json.dumps({
            "expert_order": ["fast3r", "mast3r", "spann3r"],
            "labels": {
                "dense_a": 0,
                "dense_b": 0,
                "sparse_a": 1,
                "sparse_b": 1,
                "dynamic_a": 2,
                "dynamic_b": 2,
            },
            "regime_top": {
                "dense_a": "dense_sequential",
                "dense_b": "dense_sequential",
                "sparse_a": "sparse_view",
                "sparse_b": "sparse_view",
                "dynamic_a": "dynamic_scene",
                "dynamic_b": "dynamic_scene",
            },
            "metrics": {
                "dense_a": {"fast3r": 0.20, "mast3r": 0.50, "spann3r": 0.55},
                "dense_b": {"fast3r": 0.21, "mast3r": 0.52, "spann3r": 0.56},
                "sparse_a": {"fast3r": 0.50, "mast3r": 0.22, "spann3r": 0.54},
                "sparse_b": {"fast3r": 0.51, "mast3r": 0.23, "spann3r": 0.55},
                "dynamic_a": {"fast3r": 0.55, "mast3r": 0.60, "spann3r": 0.18},
                "dynamic_b": {"fast3r": 0.56, "mast3r": 0.61, "spann3r": 0.19},
            },
            "summary": {"metric": "scale_aligned_abs_rel"},
        }), encoding="utf-8")

        train_router_only(
            regime_labels=str(regime_path),
            oracle_labels=str(oracle_path),
            output_dir=str(ckpt_dir),
            epochs=120,
            lr=0.05,
            batch_size=6,
            d_routing=16,
            feature_mode="regime_stats",
        )
        result = evaluate_router_ablation(
            regime_labels=str(regime_path),
            oracle_labels=str(oracle_path),
            router_checkpoint=str(ckpt_dir / "latest.pt"),
            output=str(output),
            feature_mode="regime_stats",
        )

        assert result["expert_order"] == ["fast3r", "mast3r", "spann3r"]
        assert result["feature_mode"] == "regime_stats"
        assert result["success"]["beats_spann3r"]
        assert result["success"]["beats_best_single"]
        assert result["success"]["improves_best_single_ge_5pct"]
        assert result["success"]["stage5_s1"]
