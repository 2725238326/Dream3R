"""Contract tests for the KITTI real-data smoke loader."""

import tempfile
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from dream3r.data_kitti import (
    KITTIRectifiedSequenceDataset,
    default_kitti_intrinsics,
    pointmap_from_depth,
)


def _write_frame(seq_dir: Path, idx: int):
    rgb = np.zeros((32, 64, 3), dtype=np.uint8)
    rgb[..., 0] = idx * 20
    rgb[..., 1] = np.arange(64, dtype=np.uint8).reshape(1, 64)
    rgb[..., 2] = 128
    depth = np.full((32, 64), 5.0 + idx, dtype=np.float32)
    depth[0, 0] = 0.0
    stem = f"{idx:010d}"
    Image.fromarray(rgb).save(seq_dir / f"{stem}.jpg")
    np.save(seq_dir / f"{stem}.npy", depth)


def test_pointmap_from_depth_projects_valid_depths():
    depth = torch.tensor([[2.0, 2.0], [0.0, 4.0]], dtype=torch.float32)
    intr = torch.tensor(
        [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 1.0]],
        dtype=torch.float32,
    )
    pointmap, mask = pointmap_from_depth(depth, intr, n_patches=4)

    assert pointmap.shape == (4, 3)
    assert mask.tolist() == [1.0, 1.0, 0.0, 1.0]
    assert torch.allclose(pointmap[0], torch.tensor([0.0, 0.0, 2.0]))
    assert torch.allclose(pointmap[3], torch.tensor([2.0, 2.0, 4.0]))


def test_kitti_rectified_sequence_dataset_contract():
    with tempfile.TemporaryDirectory() as tmp:
        seq_dir = Path(tmp) / "kitti" / "rectified" / "seq_001"
        seq_dir.mkdir(parents=True)
        for idx in range(4):
            _write_frame(seq_dir, idx)

        dataset = KITTIRectifiedSequenceDataset(
            data_root=tmp,
            n_frames=4,
            n_patches=16,
            d_model=8,
            max_sequences=1,
        )
        sample = dataset[0]

        assert len(dataset) == 1
        assert sample["features"].shape == (4, 16, 8)
        assert sample["images"].shape == (4, 3, 32, 64)
        assert sample["depth"].shape == (4, 32, 64)
        assert sample["pointmap_gt"].shape == (4, 16, 3)
        assert sample["pointmap_mask"].shape == (4, 16)
        assert sample["intrinsics"].shape == (4, 3, 3)
        assert sample["camera_poses"].shape == (4, 4, 4)
        assert sample["pointmap_mask"].sum() > 0
        assert sample["sequence_name"] == "seq_001"
        assert sample["frame_ids"] == [f"{idx:010d}" for idx in range(4)]


def test_default_kitti_intrinsics_scales_to_image_size():
    intr = default_kitti_intrinsics(416, 128)

    assert intr.shape == (3, 3)
    assert intr[0, 0] > 0
    assert intr[1, 1] > 0
    assert intr[2, 2] == 1


if __name__ == "__main__":
    test_pointmap_from_depth_projects_valid_depths()
    test_kitti_rectified_sequence_dataset_contract()
    test_default_kitti_intrinsics_scales_to_image_size()
    print("All KITTI loader contract tests passed.")
