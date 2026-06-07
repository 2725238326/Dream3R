"""Integration tests for V11 VLM controller architecture hooks."""

import json
import tempfile
from pathlib import Path

import numpy as np

from dream3r.scripts.build_vlm_semantic_labels import build_vlm_semantic_labels
from dream3r.scripts.build_vlm_window_manifest import build_vlm_window_manifest
from dream3r.scripts.eval_vlm_calibrated_controller import evaluate_vlm_calibrated_controller
from dream3r.scripts.eval_vlm_controller_dryrun import evaluate_vlm_controller_dryrun
from dream3r.scripts.eval_vlm_semantic_critic_gate import evaluate_vlm_semantic_critic_gate


def _write_kitti_sequence(root: Path, sequence: str, n_frames: int = 6) -> None:
    seq_dir = root / "kitti" / "rectified" / sequence
    seq_dir.mkdir(parents=True, exist_ok=True)
    for idx in range(n_frames):
        stem = f"{idx:010d}"
        (seq_dir / f"{stem}.jpg").write_bytes(b"fake-jpg-for-manifest-only")
        np.save(seq_dir / f"{stem}.npy", np.ones((4, 4), dtype=np.float32))


def test_build_vlm_window_manifest_writes_kitti_frame_paths(tmp_path):
    root = tmp_path / "data"
    _write_kitti_sequence(root, "2011_09_26_drive_0001_sync_02", n_frames=6)
    regime = tmp_path / "regime.json"
    output = tmp_path / "manifest.json"
    regime.write_text(json.dumps({
        "labels": {
            "2011_09_26_drive_0001_sync_02": [0, 1, 0, 0, 0, 0],
        },
    }), encoding="utf-8")

    result = build_vlm_window_manifest(
        dataset="kitti_long",
        root=str(root),
        regime_labels=str(regime),
        output=str(output),
        window_frames=4,
    )

    assert output.exists()
    assert result["schema_version"] == "dream3r_vlm_window_manifest_v1"
    assert result["n_windows"] == 1
    window = result["windows"][0]
    assert window["dataset"] == "kitti"
    assert window["window_id"].startswith("kitti/2011_09_26_drive_0001_sync_02/")
    assert len(window["frames"]) == 4
    assert all(frame.endswith(".jpg") for frame in window["frames"])


def test_build_vlm_window_manifest_can_use_oracle_sequence_ids(tmp_path):
    root = tmp_path / "data"
    sequence = "2011_09_26_drive_0001_sync_02"
    _write_kitti_sequence(root, sequence, n_frames=6)
    regime = tmp_path / "oracle_like.json"
    output = tmp_path / "manifest.json"
    regime.write_text(json.dumps({
        "expert_order": ["fast3r", "mast3r"],
        "labels": {sequence: 0},
    }), encoding="utf-8")

    result = build_vlm_window_manifest(
        dataset="kitti_long",
        root=str(root),
        regime_labels=str(regime),
        output=str(output),
        window_frames=4,
        window_id_mode="sequence",
    )

    assert result["windows"][0]["window_id"] == sequence


def test_vlm_controller_dryrun_compares_real_shuffle_disabled_controls(tmp_path):
    manifest = tmp_path / "manifest.json"
    cache_path = tmp_path / "vlm_labels.json"
    oracle_path = tmp_path / "oracle.json"
    output = tmp_path / "dryrun.json"
    manifest.write_text(json.dumps({
        "windows": [
            {
                "window_id": "kitti/mock/0000000000",
                "dataset": "kitti",
                "frames": ["a.png", "b.png", "c.png", "d_car.png"],
            },
            {
                "window_id": "eth3d/mock_building/0000",
                "dataset": "eth3d",
                "frames": ["building_0.png", "building_1.png", "building_2.png", "building_3.png"],
            },
        ],
    }), encoding="utf-8")
    cache = build_vlm_semantic_labels(
        window_manifest=str(manifest),
        output=str(cache_path),
        backend="mock",
        mock_mode="valid",
        shuffle_seed=1,
    )
    assert cache["schema_report"]["schema_pass_rate"] == 1.0

    oracle_path.write_text(json.dumps({
        "expert_order": ["fast3r", "mast3r", "spann3r"],
        "labels": {
            "kitti/mock/0000000000": 2,
            "eth3d/mock_building/0000": 0,
        },
        "metrics": {
            "kitti/mock/0000000000": {
                "fast3r": 0.50,
                "mast3r": 0.45,
                "spann3r": 0.20,
            },
            "eth3d/mock_building/0000": {
                "fast3r": 0.22,
                "mast3r": 0.40,
                "spann3r": 0.55,
            },
        },
        "summary": {"metric": "abs_rel"},
    }), encoding="utf-8")

    result = evaluate_vlm_controller_dryrun(
        vlm_cache=str(cache_path),
        oracle_labels=str(oracle_path),
        output=str(output),
        hard_window_gap=0.05,
    )

    assert output.exists()
    assert result["schema_version"] == "dream3r_vlm_controller_dryrun_v1"
    assert result["n_windows"] == 2
    assert result["variants"]["vlm_real"]["routes"]["kitti/mock/0000000000"] == "spann3r"
    assert result["variants"]["vlm_disabled"]["routes"]["kitti/mock/0000000000"] == "fast3r"
    assert result["variants"]["vlm_real"]["mean_metric"] < result["variants"]["vlm_disabled"]["mean_metric"]
    assert "promotable" in result["diagnostic"]
    assert result["diagnostic"]["promotable"] is False


def test_vlm_controller_routes_occlusion_before_road_fallback(tmp_path):
    cache_path = tmp_path / "vlm_labels.json"
    oracle_path = tmp_path / "oracle.json"
    output = tmp_path / "dryrun.json"
    feature_order = [
        "scene_road",
        "risk_dynamic",
        "risk_low_texture",
        "risk_reflection",
        "risk_occlusion",
        "risk_large_baseline",
        "suggest_verify_geometry",
    ]
    cache_path.write_text(json.dumps({
        "controls": {
            "feature_order": feature_order,
            "shuffled_features": {"road_occ": [1.0, 0.0, 0.0, 0.0, 0.65, 0.0, 1.0]},
            "disabled_features": {"road_occ": [0.0] * len(feature_order)},
        },
        "features": {
            "road_occ": [1.0, 0.0, 0.0, 0.0, 0.65, 0.0, 1.0],
        },
    }), encoding="utf-8")
    oracle_path.write_text(json.dumps({
        "expert_order": ["fast3r", "mast3r", "spann3r"],
        "labels": {"road_occ": 1},
        "metrics": {
            "road_occ": {
                "fast3r": 0.50,
                "mast3r": 0.20,
                "spann3r": 0.45,
            },
        },
        "summary": {"metric": "abs_rel"},
    }), encoding="utf-8")

    result = evaluate_vlm_controller_dryrun(
        vlm_cache=str(cache_path),
        oracle_labels=str(oracle_path),
        output=str(output),
    )

    assert result["variants"]["vlm_real"]["routes"]["road_occ"] == "mast3r"
    assert result["variants"]["vlm_disabled"]["routes"]["road_occ"] == "fast3r"
    assert result["variants"]["vlm_real"]["mean_metric"] < result["variants"]["vlm_disabled"]["mean_metric"]


def test_vlm_calibrated_controller_uses_heldout_groups_and_controls(tmp_path):
    cache_path = tmp_path / "vlm_labels.json"
    oracle_path = tmp_path / "oracle.json"
    output = tmp_path / "calibrated.json"
    feature_order = ["road", "texture"]
    windows = [
        "2011_09_26_drive_0001_sync_02",
        "2011_09_26_drive_0002_sync_02",
        "2011_09_26_drive_0003_sync_02",
        "2011_09_26_drive_0004_sync_02",
    ]
    cache_path.write_text(json.dumps({
        "controls": {
            "feature_order": feature_order,
            "shuffled_features": {
                window_id: [1.0, 0.0] for window_id in windows
            },
            "disabled_features": {
                window_id: [0.0, 0.0] for window_id in windows
            },
        },
        "features": {
            windows[0]: [1.0, 0.0],
            windows[1]: [1.0, 0.0],
            windows[2]: [0.0, 1.0],
            windows[3]: [0.0, 1.0],
        },
    }), encoding="utf-8")
    oracle_path.write_text(json.dumps({
        "expert_order": ["fast3r", "mast3r", "spann3r"],
        "labels": {
            windows[0]: 0,
            windows[1]: 0,
            windows[2]: 1,
            windows[3]: 1,
        },
        "metrics": {
            windows[0]: {"fast3r": 0.10, "mast3r": 0.50, "spann3r": 0.60},
            windows[1]: {"fast3r": 0.10, "mast3r": 0.50, "spann3r": 0.60},
            windows[2]: {"fast3r": 0.50, "mast3r": 0.10, "spann3r": 0.60},
            windows[3]: {"fast3r": 0.50, "mast3r": 0.10, "spann3r": 0.60},
        },
        "summary": {"metric": "abs_rel"},
    }), encoding="utf-8")

    result = evaluate_vlm_calibrated_controller(
        vlm_cache=str(cache_path),
        oracle_labels=str(oracle_path),
        output=str(output),
    )

    assert output.exists()
    assert result["schema_version"] == "dream3r_vlm_calibrated_controller_v1"
    assert result["split_strategy"] == "leave_one_group_out"
    assert result["n_groups"] == 4
    assert result["state_causality_controls"]["heldout_oracle_leakage"] is False
    assert result["variants"]["vlm_real"]["mean_metric"] == result["oracle_mean"]
    assert result["variants"]["vlm_real"]["mean_metric"] < result["variants"]["vlm_disabled"]["mean_metric"]
    assert result["variants"]["vlm_real"]["mean_metric"] < result["variants"]["vlm_shuffle"]["mean_metric"]
    assert all(
        fold["n_test"] == 1
        for fold in result["variants"]["vlm_real"]["folds"]
    )


def test_vlm_semantic_critic_gate_requires_real_semantic_plus_geometry(tmp_path):
    cache_path = tmp_path / "vlm_labels.json"
    oracle_path = tmp_path / "oracle.json"
    output = tmp_path / "critic_gate.json"
    feature_order = ["risk_dynamic", "suggest_verify_geometry"]
    windows = ["hard_a", "hard_b", "easy_high_disp", "easy_low_disp"]
    cache_path.write_text(json.dumps({
        "controls": {
            "feature_order": feature_order,
            "shuffled_features": {
                "hard_a": [0.0, 0.0],
                "hard_b": [0.0, 0.0],
                "easy_high_disp": [1.0, 1.0],
                "easy_low_disp": [1.0, 1.0],
            },
            "disabled_features": {
                window_id: [0.0, 0.0] for window_id in windows
            },
        },
        "features": {
            "hard_a": [1.0, 1.0],
            "hard_b": [1.0, 1.0],
            "easy_high_disp": [0.0, 0.0],
            "easy_low_disp": [0.0, 0.0],
        },
    }), encoding="utf-8")
    oracle_path.write_text(json.dumps({
        "expert_order": ["fast3r", "mast3r", "spann3r"],
        "labels": {
            "hard_a": 1,
            "hard_b": 1,
            "easy_high_disp": 0,
            "easy_low_disp": 0,
        },
        "metrics": {
            "hard_a": {"fast3r": 0.50, "mast3r": 0.10, "spann3r": 0.55},
            "hard_b": {"fast3r": 0.40, "mast3r": 0.20, "spann3r": 0.45},
            "easy_high_disp": {"fast3r": 0.20, "mast3r": 0.50, "spann3r": 0.55},
            "easy_low_disp": {"fast3r": 0.20, "mast3r": 0.25, "spann3r": 0.30},
        },
        "summary": {"metric": "abs_rel"},
    }), encoding="utf-8")

    result = evaluate_vlm_semantic_critic_gate(
        vlm_cache=str(cache_path),
        oracle_labels=str(oracle_path),
        output=str(output),
        hard_window_gap=0.05,
        semantic_weight=0.5,
    )

    assert output.exists()
    assert result["schema_version"] == "dream3r_vlm_semantic_critic_gate_v1"
    assert result["state_causality_controls"]["vlm_geometry_access"] is False
    assert result["variants"]["geometry_only"]["hard_window"]["f1"] < 1.0
    assert result["variants"]["vlm_real_qwen_only"]["hard_window"]["f1"] == 1.0
    assert result["variants"]["vlm_real_plus_geometry"]["hard_window"]["f1"] == 1.0
    assert (
        result["variants"]["vlm_real_plus_geometry"]["hard_window"]["f1"]
        > result["variants"]["vlm_shuffle_plus_geometry"]["hard_window"]["f1"]
    )
    assert (
        result["variants"]["vlm_real_plus_geometry"]["hard_window"]["f1"]
        > result["variants"]["vlm_disabled_plus_geometry"]["hard_window"]["f1"]
    )
    assert result["diagnostic"]["promotable"] is False
