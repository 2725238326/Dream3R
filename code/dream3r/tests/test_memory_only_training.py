"""Contract tests for Stage 2 memory-only training wiring."""

import tempfile
from pathlib import Path

import numpy as np
from PIL import Image
from torch.utils.data import DataLoader

from dream3r.config import config_to_model_args, load_config
from dream3r.model import Dream3R
from dream3r.train import apply_train_mode, build_datasets, collate_for_dataset


def _write_frame(seq_dir: Path, idx: int):
    rgb = np.zeros((24, 48, 3), dtype=np.uint8)
    rgb[..., 0] = idx
    rgb[..., 1] = 32
    rgb[..., 2] = 96
    depth = np.full((24, 48), 5.0 + idx * 0.1, dtype=np.float32)
    stem = f"{idx:010d}"
    Image.fromarray(rgb).save(seq_dir / f"{stem}.jpg")
    np.save(seq_dir / f"{stem}.npy", depth)


def _make_kitti_root(tmp: str):
    seq_dir = Path(tmp) / "kitti" / "rectified" / "seq_001"
    seq_dir.mkdir(parents=True)
    for idx in range(10):
        _write_frame(seq_dir, idx)


def test_memory_only_preset_builds_kitti_long_datasets_and_collate():
    with tempfile.TemporaryDirectory() as tmp:
        _make_kitti_root(tmp)
        cfg = load_config(preset="memory_only", overrides={
            "data_root": tmp,
            "kitti_window_frames": 4,
            "kitti_window_overlap": 2,
            "kitti_windows_per_sample": 2,
            "kitti_min_sequence_frames": 6,
            "kitti_max_sequences": 1,
            "d_model": 8,
            "n_patches": 16,
        })

        train_ds, val_ds = build_datasets(cfg)
        assert len(train_ds) > 0
        assert len(val_ds) > 0

        loader = DataLoader(
            train_ds,
            batch_size=2,
            collate_fn=collate_for_dataset(cfg),
        )
        batch = next(iter(loader))
        assert batch["features"].shape == (2, 2, 4, 16, 8)
        assert batch["regime"].shape == (2, 2, 6)


def test_memory_only_train_mode_freezes_non_memory_parameters():
    cfg = load_config(preset="memory_only")
    model = Dream3R(config_to_model_args(cfg))

    n_trainable = apply_train_mode(model, cfg)
    trainable_names = [
        name for name, param in model.named_parameters()
        if param.requires_grad
    ]

    assert n_trainable > 0
    assert trainable_names
    assert all(name.startswith("memory.") for name in trainable_names)
