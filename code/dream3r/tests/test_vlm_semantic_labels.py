"""Tests for the V11 VLM semantic-controller label cache."""

import json
from pathlib import Path

from dream3r.scripts.build_vlm_semantic_labels import (
    DEFAULT_MODEL_ID,
    FEATURE_ORDER,
    RECORD_KEYS,
    QwenSemanticBackend,
    build_vlm_semantic_labels,
    record_to_feature_vector,
    validate_record_schema,
    validate_semantic_payload,
)


def _write_manifest(path: Path, windows):
    path.write_text(json.dumps({"windows": windows}), encoding="utf-8")


def test_mock_backend_writes_strict_records_and_causality_controls(tmp_path):
    manifest = tmp_path / "windows.json"
    _write_manifest(
        manifest,
        [
            {
                "window_id": "kitti/2011_09_26/0000000000",
                "dataset": "kitti",
                "frames": [
                    "kitti_000.png",
                    "kitti_001.png",
                    "kitti_002.png",
                    "kitti_003_car.png",
                ],
            },
            {
                "window_id": "eth3d/courtyard/000000",
                "dataset": "eth3d",
                "frames": [
                    "eth3d_000_building.png",
                    "eth3d_001_building.png",
                    "eth3d_002_building.png",
                    "eth3d_003_building.png",
                ],
            },
        ],
    )
    output = tmp_path / "labels.json"
    report = tmp_path / "schema_report.json"

    cache = build_vlm_semantic_labels(
        window_manifest=str(manifest),
        output=str(output),
        schema_report=str(report),
        backend="mock",
        mock_mode="valid",
        shuffle_seed=3,
    )

    assert output.exists()
    assert report.exists()
    assert cache["schema_report"]["n_windows"] == 2
    assert cache["schema_report"]["valid_records"] == 2
    assert cache["schema_report"]["failure_records"] == 0
    assert cache["schema_report"]["schema_pass_rate"] == 1.0
    assert cache["controls"]["feature_order"] == list(FEATURE_ORDER)

    for record in cache["records"]:
        assert set(record) == set(RECORD_KEYS)
        assert validate_record_schema(record) == []
        assert record["failure_flags"] == []
        assert record["model_id"] == DEFAULT_MODEL_ID

    features = cache["features"]
    shuffled = cache["controls"]["shuffled_features"]
    disabled = cache["controls"]["disabled_features"]
    assert set(features) == set(shuffled) == set(disabled)
    assert all(len(vector) == len(FEATURE_ORDER) for vector in features.values())
    assert all(vector == [0.0] * len(FEATURE_ORDER) for vector in disabled.values())
    assert list(shuffled.values()) != list(features.values())


def test_invalid_backend_output_becomes_explicit_failure_record(tmp_path):
    manifest = tmp_path / "windows.json"
    _write_manifest(
        manifest,
        [{
            "window_id": "kitti/invalid/000000",
            "dataset": "kitti",
            "frames": ["a.png", "b.png", "c.png", "d.png"],
        }],
    )
    output = tmp_path / "labels.json"

    cache = build_vlm_semantic_labels(
        window_manifest=str(manifest),
        output=str(output),
        backend="mock",
        mock_mode="invalid",
    )

    record = cache["records"][0]
    assert validate_record_schema(record) == []
    assert record["scene_type"] == "unknown"
    assert record["confidence"] == 0.0
    assert any(flag.startswith("invalid_json") for flag in record["failure_flags"])
    assert cache["schema_report"]["valid_records"] == 0
    assert cache["schema_report"]["failure_records"] == 1
    feature = cache["features"][record["window_id"]]
    assert feature[FEATURE_ORDER.index("schema_failure")] == 1.0


def test_semantic_payload_rejects_out_of_range_and_extra_geometry_fields():
    window = {
        "window_id": "eth3d/test/000000",
        "dataset": "eth3d",
        "frames": ["a.png", "b.png", "c.png", "d.png"],
    }
    payload = {
        "scene_type": "building",
        "risk_dynamic": 1.5,
        "risk_low_texture": 0.1,
        "risk_reflection": 0.1,
        "risk_occlusion": 0.1,
        "risk_large_baseline": 0.1,
        "risk_scale_drift": 0.1,
        "risk_repeated_structure": 0.1,
        "important_objects": [],
        "visible_failure_causes": [],
        "suggest_verify_geometry": True,
        "suggest_expensive_teacher": False,
        "confidence": 0.8,
        "metric_depth": 3.0,
    }

    record = validate_semantic_payload(payload, window, backend="unit")

    assert validate_record_schema(record) == []
    assert record["failure_flags"]
    assert any("risk_dynamic:not_unit_interval" in flag for flag in record["failure_flags"])
    assert any("unexpected_fields:metric_depth" in flag for flag in record["failure_flags"])


def test_visible_failure_causes_provide_risk_feature_floor():
    window = {
        "window_id": "kitti/cause_floor/000000",
        "dataset": "kitti",
        "frames": ["a.png", "b.png", "c.png", "d.png"],
    }
    payload = {
        "scene_type": "road",
        "risk_dynamic": 0.0,
        "risk_low_texture": 0.0,
        "risk_reflection": 0.0,
        "risk_occlusion": 0.0,
        "risk_large_baseline": 0.0,
        "risk_scale_drift": 0.0,
        "risk_repeated_structure": 0.0,
        "important_objects": ["building"],
        "visible_failure_causes": ["low_texture"],
        "suggest_verify_geometry": True,
        "suggest_expensive_teacher": False,
        "confidence": 0.8,
    }

    record = validate_semantic_payload(payload, window, backend="unit")
    features = record_to_feature_vector(record)

    assert validate_record_schema(record) == []
    assert features[FEATURE_ORDER.index("risk_low_texture")] >= 0.5


def test_qwen_backend_defaults_to_local_files_only_without_approval():
    backend = QwenSemanticBackend(
        model_id=DEFAULT_MODEL_ID,
        model_path=None,
        allow_remote_model_load=False,
    )

    assert backend.model_source == DEFAULT_MODEL_ID
    assert backend.local_files_only is True
