"""Tests for the Stage 1 KITTI image-pair dataset."""

import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

from dream3r.data.kitti_pair import KITTIPairDataset


def _write_frame(seq_dir: Path, idx: int):
    rgb = np.zeros((32, 64, 3), dtype=np.uint8)
    rgb[..., 0] = idx * 10
    rgb[..., 1] = np.arange(64, dtype=np.uint8).reshape(1, 64)
    rgb[..., 2] = 64
    depth = np.full((32, 64), 4.0 + idx, dtype=np.float32)
    depth[0, 0] = 0.0
    stem = f"{idx:010d}"
    Image.fromarray(rgb).save(seq_dir / f"{stem}.jpg")
    np.save(seq_dir / f"{stem}.npy", depth)


def test_kitti_pair_dataset_iterates_five_pairs():
    with tempfile.TemporaryDirectory() as tmp:
        seq_dir = Path(tmp) / "kitti" / "rectified" / "seq_001"
        seq_dir.mkdir(parents=True)
        np.savetxt(seq_dir / "cam.txt", np.eye(3, dtype=np.float32))
        for idx in range(8):
            _write_frame(seq_dir, idx)

        dataset = KITTIPairDataset(tmp, max_sequences=1)

        assert len(dataset) >= 5
        for idx in range(5):
            sample = dataset[idx]
            assert sample["images"].shape == (2, 3, 32, 64)
            assert sample["intrinsics"].shape == (2, 3, 3)
            assert sample["depth_gt"].shape == (2, 32, 64)
            assert sample["valid_mask"].shape == (2, 32, 64)
            assert sample["valid_mask"].any()
            assert sample["sequence_name"] == "seq_001"
            assert len(sample["frame_ids"]) == 2
