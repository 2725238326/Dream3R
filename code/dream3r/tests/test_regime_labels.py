"""Schema tests for Stage 3 KITTI regime label generation."""

import json
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

from dream3r.composer_experts.method_profiles import REGIME_ORDER
from dream3r.scripts.generate_regime_labels import generate_regime_labels


def _write_sequence(root: Path, name: str, n_frames: int, depth_step: float = 0.0):
    seq_dir = root / "kitti" / "rectified" / name
    seq_dir.mkdir(parents=True, exist_ok=True)
    for idx in range(n_frames):
        stem = f"{idx:010d}"
        image = np.full((12, 20, 3), idx % 255, dtype=np.uint8)
        depth = np.full((12, 20), 4.0 + idx * depth_step, dtype=np.float32)
        Image.fromarray(image).save(seq_dir / f"{stem}.jpg")
        np.save(seq_dir / f"{stem}.npy", depth)
    return seq_dir


def _write_oxts(root: Path, raw_name: str, n_frames: int):
    oxts_dir = root / "kitti" / "2011_09_26" / raw_name / "oxts" / "data"
    oxts_dir.mkdir(parents=True, exist_ok=True)
    for idx in range(n_frames):
        values = [0.0] * 30
        values[8] = 2.0 + (idx % 3)
        (oxts_dir / f"{idx:010d}.txt").write_text(
            " ".join(str(value) for value in values),
            encoding="utf-8",
        )


def _prob(label_map, sequence, regime):
    return label_map[sequence][REGIME_ORDER.index(regime)]


def test_generate_regime_labels_writes_normalized_six_way_labels():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write_sequence(root, "short_seq", 8)
        _write_sequence(root, "2011_09_26_drive_0001_sync_02", 120, depth_step=0.02)
        (root / "kitti" / "rectified" / "empty_seq").mkdir(parents=True)
        _write_oxts(root, "2011_09_26_drive_0001_sync", 120)
        output = root / "labels" / "regime_labels.json"

        result = generate_regime_labels(
            root=str(root),
            output=str(output),
            sample_frames=5,
        )

        assert output.exists()
        saved = json.loads(output.read_text(encoding="utf-8"))
        assert saved["regime_order"] == REGIME_ORDER
        assert result["labels"].keys() == saved["labels"].keys()
        assert "empty_seq" not in saved["labels"]
        assert saved["skipped_empty"] == ["empty_seq"]

        for probs in saved["labels"].values():
            assert len(probs) == 6
            assert abs(sum(probs) - 1.0) < 1e-5

        labels = saved["labels"]
        assert _prob(labels, "short_seq", "sparse_view") > _prob(
            labels, "short_seq", "dense_sequential"
        )
        assert _prob(labels, "2011_09_26_drive_0001_sync_02", "dense_sequential") > _prob(
            labels, "2011_09_26_drive_0001_sync_02", "sparse_view"
        )
        assert saved["features"]["2011_09_26_drive_0001_sync_02"]["oxts_available"] == 1.0
        assert len(saved["sanity"]) == 2
