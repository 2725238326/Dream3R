"""Tests for the Stage 2 KITTI long-window dataset."""

import tempfile
from pathlib import Path

import numpy as np
from PIL import Image
from torch.utils.data import DataLoader

from dream3r.data.kitti_long import KITTILongSequenceDataset, collate_kitti_long


def _write_frame(seq_dir: Path, idx: int):
    rgb = np.zeros((24, 48, 3), dtype=np.uint8)
    rgb[..., 0] = idx * 5
    rgb[..., 1] = np.arange(48, dtype=np.uint8).reshape(1, 48)
    rgb[..., 2] = 96
    depth = np.full((24, 48), 3.0 + idx * 0.1, dtype=np.float32)
    depth[0, 0] = 0.0
    stem = f"{idx:010d}"
    Image.fromarray(rgb).save(seq_dir / f"{stem}.jpg")
    np.save(seq_dir / f"{stem}.npy", depth)


def _write_oxts(root: Path, idx: int):
    oxts_dir = (
        root / "kitti" / "2011_09_26" /
        "2011_09_26_drive_0001_sync" / "oxts" / "data"
    )
    oxts_dir.mkdir(parents=True, exist_ok=True)
    values = [
        49.0 + idx * 1e-6,
        8.0,
        100.0,
        0.0,
        0.0,
        0.01 * idx,
    ] + [0.0] * 24
    (oxts_dir / f"{idx:010d}.txt").write_text(" ".join(str(v) for v in values))


def _make_rectified_sequence(root: Path, name: str, n_frames: int):
    seq_dir = root / "kitti" / "rectified" / name
    seq_dir.mkdir(parents=True, exist_ok=True)
    np.savetxt(seq_dir / "cam.txt", np.eye(3, dtype=np.float32))
    for idx in range(n_frames):
        _write_frame(seq_dir, idx)
    return seq_dir


def test_kitti_long_dataset_uses_oxts_poses_and_overlapping_windows():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _make_rectified_sequence(root, "2011_09_26_drive_0001_sync_02", 12)
        for idx in range(12):
            _write_oxts(root, idx)

        dataset = KITTILongSequenceDataset(
            root=str(root),
            sequence_length=4,
            overlap=2,
            windows_per_sample=3,
            min_sequence_frames=8,
            max_sequences=1,
            n_patches=16,
            d_model=8,
        )
        sample = dataset[0]

        assert len(dataset) == 3
        assert sample["features"].shape == (3, 4, 16, 8)
        assert sample["images"].shape == (3, 4, 3, 24, 48)
        assert sample["depth_gt"].shape == (3, 4, 24, 48)
        assert sample["pointmap_gt"].shape == (3, 4, 16, 3)
        assert sample["pointmap_mask"].shape == (3, 4, 16)
        assert sample["intrinsics"].shape == (3, 4, 3, 3)
        assert sample["camera_poses"].shape == (3, 4, 4, 4)
        assert sample["regime"].shape == (3, 6)
        assert sample["region_label"].shape == (3, 16)
        assert sample["pose_source"] == "oxts"
        assert sample["frame_ids"][0][-2:] == sample["frame_ids"][1][:2]
        assert sample["camera_poses"][0, 0, 0, 3] == 0
        assert sample["camera_poses"][0, -1, :3, 3].norm() > 0


def test_kitti_long_dataset_falls_back_to_linear_poses_and_collates():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _make_rectified_sequence(root, "seq_001", 10)

        dataset = KITTILongSequenceDataset(
            root=str(root),
            sequence_length=4,
            overlap=2,
            windows_per_sample=2,
            min_sequence_frames=6,
            max_sequences=1,
            n_patches=16,
            d_model=8,
        )
        sample = dataset[0]
        assert sample["pose_source"] == "linear_fallback"
        assert sample["camera_poses"][0, -1, 0, 3] > 0

        loader = DataLoader(dataset, batch_size=2, collate_fn=collate_kitti_long)
        batch = next(iter(loader))
        assert batch["features"].shape == (2, 2, 4, 16, 8)
        assert len(batch["sequence_name"]) == 2
        assert len(batch["frame_ids"]) == 2
