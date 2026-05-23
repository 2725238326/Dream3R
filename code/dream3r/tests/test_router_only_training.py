"""Schema tests for Stage 3 router-only supervised training."""

import json
import tempfile
from pathlib import Path

from dream3r.config import load_config
from dream3r.scripts.train_router_only import train_router_only


def test_router_only_preset_points_at_stage3_artifacts():
    cfg = load_config(preset="router_only")

    assert cfg["train_mode"] == "router_only"
    assert cfg["save_dir"].endswith("router_only_v1")
    assert cfg["regime_labels_path"].endswith("stage3_regime_labels/regime_labels.json")
    assert cfg["oracle_labels_path"].endswith("stage3_oracle_labels/oracle_expert_labels.json")


def test_train_router_only_saves_checkpoint_and_improves_accuracy():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        regime_path = root / "regime_labels.json"
        oracle_path = root / "oracle_labels.json"
        output_dir = root / "router"

        regime_path.write_text(json.dumps({
            "labels": {
                "dense_a": [0.02, 0.12, 0.05, 0.05, 0.7, 0.06],
                "dense_b": [0.02, 0.12, 0.05, 0.05, 0.68, 0.08],
                "sparse_a": [0.02, 0.15, 0.05, 0.68, 0.05, 0.05],
                "sparse_b": [0.02, 0.15, 0.05, 0.66, 0.07, 0.05],
            }
        }), encoding="utf-8")
        oracle_path.write_text(json.dumps({
            "expert_order": ["fast3r", "mast3r"],
            "labels": {
                "dense_a": 0,
                "dense_b": 0,
                "sparse_a": 1,
                "sparse_b": 1,
            },
        }), encoding="utf-8")

        summary = train_router_only(
            regime_labels=str(regime_path),
            oracle_labels=str(oracle_path),
            output_dir=str(output_dir),
            epochs=80,
            lr=0.05,
            batch_size=4,
            d_routing=16,
        )

        assert summary["final_accuracy"] >= summary["initial_accuracy"]
        assert summary["final_accuracy"] >= 0.75
        assert (output_dir / "latest.pt").exists()
        assert (output_dir / "summary.json").exists()
