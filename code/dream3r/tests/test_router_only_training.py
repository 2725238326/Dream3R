"""Schema tests for Stage 3 router-only supervised training."""

import json
import tempfile
from pathlib import Path

import torch

from dream3r.composer_experts import ExpertRegistry
from dream3r.composer_experts.fast3r_adapter import Fast3RAdapter
from dream3r.composer_experts.mast3r_adapter import MASt3RAdapter
from dream3r.config import load_config
from dream3r.modules import ComposerRouter
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


def test_train_router_only_with_metrics_makes_router_respond_to_critic_confidence():
    """When oracle has per-expert metrics, the trained router must:

    - keep regime-driven routing when no critic_confidence is provided
    - flip toward the alternate expert on at least some sequences when low
      critic_confidence (= recent high conflict) is provided.

    This is the supervision the Stage-4 pipeline ablation depends on; without
    it `confidence_gate` is randomly initialised and the critic-on path is
    indistinguishable from the both-off path.
    """
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        regime_path = root / "regime_labels.json"
        oracle_path = root / "oracle_labels.json"
        output_dir = root / "router"

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
                "dynamic_a": [0.02, 0.10, 0.70, 0.05, 0.08, 0.05],
                "dynamic_b": [0.02, 0.10, 0.68, 0.05, 0.10, 0.05],
                "sparse_a": [0.02, 0.15, 0.05, 0.68, 0.05, 0.05],
                "sparse_b": [0.02, 0.15, 0.05, 0.66, 0.07, 0.05],
            },
        }), encoding="utf-8")
        oracle_path.write_text(json.dumps({
            "expert_order": ["fast3r", "mast3r"],
            "labels": {
                "dense_a": 0,
                "dense_b": 0,
                "dynamic_a": 0,
                "dynamic_b": 0,
                "sparse_a": 1,
                "sparse_b": 1,
            },
            "metrics": {
                "dense_a": {"fast3r": 0.12, "mast3r": 0.30},
                "dense_b": {"fast3r": 0.13, "mast3r": 0.28},
                "dynamic_a": {"fast3r": 0.18, "mast3r": 0.24},
                "dynamic_b": {"fast3r": 0.19, "mast3r": 0.25},
                "sparse_a": {"fast3r": 0.32, "mast3r": 0.14},
                "sparse_b": {"fast3r": 0.30, "mast3r": 0.15},
            },
            "summary": {
                "metric": "scale_aligned_abs_rel",
                "conflict_threshold": 0.20,
            },
        }), encoding="utf-8")

        summary = train_router_only(
            regime_labels=str(regime_path),
            oracle_labels=str(oracle_path),
            output_dir=str(output_dir),
            epochs=500,
            lr=0.05,
            batch_size=4,
            d_routing=16,
        )

        assert summary["augmented_with_critic_confidence"] is True
        assert summary["conf_high_val"] is not None
        assert summary["conf_low_val"] is not None
        assert summary["conf_threshold_val"] is not None
        assert summary["conf_low_val"] < summary["conf_high_val"]
        assert summary["high_conf_accuracy_vs_best"] >= 0.75
        # The whole point: low conf must flip routing on at least some sequences.
        assert summary["low_conf_flip_rate_vs_no_conf"] > 0.0
        assert summary["low_conf_avoid_prev_best_accuracy"] >= 0.75
        assert summary["low_conf_avoid_prev_alt_accuracy"] >= 0.75
        assert summary["zero_conf_avoid_prev_best_accuracy"] >= 0.75
        assert summary["zero_conf_avoid_prev_alt_accuracy"] >= 0.75
        assert summary["threshold_dynamic_flip_rate_vs_no_conf"] > 0.0
        assert summary["threshold_dynamic_avoid_prev_best_accuracy"] > 0.0
        assert summary["threshold_dynamic_avoid_prev_alt_accuracy"] > 0.0

        # Reload checkpoint and confirm the no-conf branch still hits oracle.
        registry = ExpertRegistry()
        registry.register_class("fast3r", Fast3RAdapter)
        registry.register_class("mast3r", MASt3RAdapter)
        ckpt = torch.load(output_dir / "latest.pt", map_location="cpu", weights_only=False)
        router = ComposerRouter(
            n_regimes=6,
            d_routing=ckpt["router_state_dict"]["regime_encoder.0.weight"].shape[0],
            cost_alpha=0.0,
            expert_registry=registry,
        )
        router.load_state_dict(ckpt["router_state_dict"])
        router.eval()

        regime_data = json.loads(regime_path.read_text(encoding="utf-8"))
        oracle_data = json.loads(oracle_path.read_text(encoding="utf-8"))
        sequences = sorted(oracle_data["labels"])
        x = torch.tensor(
            [regime_data["labels"][seq] for seq in sequences],
            dtype=torch.float32,
        )
        y = torch.tensor(
            [int(oracle_data["labels"][seq]) for seq in sequences],
            dtype=torch.long,
        )
        with torch.no_grad():
            no_conf_pred = router(x)["routing_logits"].argmax(dim=-1)
            conf_low = torch.full((x.shape[0], 1), float(summary["conf_low_val"]))
            low_conf_pred = router(x, critic_confidence=conf_low)["routing_logits"].argmax(dim=-1)
            avoid_best_pred = router(
                x,
                critic_confidence=conf_low,
                previous_expert_id=y,
            )["routing_logits"].argmax(dim=-1)
            alt_y = 1 - y
            avoid_alt_pred = router(
                x,
                critic_confidence=conf_low,
                previous_expert_id=alt_y,
            )["routing_logits"].argmax(dim=-1)
            conf_zero = torch.zeros((x.shape[0], 1))
            zero_avoid_best_pred = router(
                x,
                critic_confidence=conf_zero,
                previous_expert_id=y,
            )["routing_logits"].argmax(dim=-1)
            zero_avoid_alt_pred = router(
                x,
                critic_confidence=conf_zero,
                previous_expert_id=alt_y,
            )["routing_logits"].argmax(dim=-1)
        no_conf_accuracy = float((no_conf_pred == y).float().mean().item())
        flip = (no_conf_pred != low_conf_pred).any().item()
        assert no_conf_accuracy >= 0.75, "Stage 3 no-conf accuracy regressed"
        assert flip, "low-conf input did not change router output on any sequence"
        assert (avoid_best_pred == alt_y).any(), "router did not avoid previous best expert"
        assert (avoid_alt_pred == y).any(), "router did not avoid previous alternate expert"
        assert (zero_avoid_best_pred == alt_y).any(), "zero-conf did not avoid previous best expert"
        assert (zero_avoid_alt_pred == y).any(), "zero-conf did not avoid previous alternate expert"
