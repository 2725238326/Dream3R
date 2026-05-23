"""KITTI long-window dataset for Stage 2 memory training."""

from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import math
import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset

from dream3r.data_kitti import (
    default_kitti_intrinsics,
    image_to_patch_features,
    pointmap_from_depth,
)


EARTH_RADIUS_M = 6378137.0


def _resolve_roots(root: str) -> Tuple[Path, Path]:
    path = Path(root)
    nested_rectified = path / "kitti" / "rectified"
    if nested_rectified.exists():
        return nested_rectified, path / "kitti"
    if path.name == "rectified":
        return path, path.parent
    return path, path.parent


def _read_intrinsics(seq_dir: Path, width: int, height: int) -> torch.Tensor:
    cam_path = seq_dir / "cam.txt"
    if cam_path.exists():
        cam = np.loadtxt(cam_path, dtype=np.float32)
        if cam.shape == (3, 3):
            return torch.from_numpy(cam)
    return default_kitti_intrinsics(width, height)


def _rotation_from_oxts(roll: float, pitch: float, yaw: float) -> np.ndarray:
    cr, sr = math.cos(roll), math.sin(roll)
    cp, sp = math.cos(pitch), math.sin(pitch)
    cy, sy = math.cos(yaw), math.sin(yaw)
    rx = np.array([[1.0, 0.0, 0.0], [0.0, cr, -sr], [0.0, sr, cr]], dtype=np.float64)
    ry = np.array([[cp, 0.0, sp], [0.0, 1.0, 0.0], [-sp, 0.0, cp]], dtype=np.float64)
    rz = np.array([[cy, -sy, 0.0], [sy, cy, 0.0], [0.0, 0.0, 1.0]], dtype=np.float64)
    return rz @ ry @ rx


def _oxts_pose(values: np.ndarray, scale: float) -> np.ndarray:
    lat, lon, alt, roll, pitch, yaw = values[:6].astype(np.float64)
    mx = scale * math.radians(lon) * EARTH_RADIUS_M
    my = scale * EARTH_RADIUS_M * math.log(math.tan(math.pi * (90.0 + lat) / 360.0))
    pose = np.eye(4, dtype=np.float64)
    pose[:3, :3] = _rotation_from_oxts(roll, pitch, yaw)
    pose[:3, 3] = np.array([mx, my, alt], dtype=np.float64)
    return pose


def _normalize_poses(poses: np.ndarray) -> torch.Tensor:
    first_inv = np.linalg.inv(poses[0])
    relative = np.stack([first_inv @ pose for pose in poses]).astype(np.float32)
    return torch.from_numpy(relative)


def _load_pose_txt(seq_dir: Path, frame_indices: Iterable[int]) -> Optional[torch.Tensor]:
    pose_path = seq_dir / "poses.txt"
    if not pose_path.exists():
        return None
    rows = np.loadtxt(pose_path, dtype=np.float64)
    if rows.ndim == 1:
        rows = rows.reshape(1, -1)
    poses = []
    for frame_idx in frame_indices:
        if frame_idx >= rows.shape[0]:
            return None
        row = rows[frame_idx]
        if row.size == 12:
            pose = np.eye(4, dtype=np.float64)
            pose[:3, :] = row.reshape(3, 4)
        elif row.size == 16:
            pose = row.reshape(4, 4)
        else:
            return None
        poses.append(pose)
    return _normalize_poses(np.stack(poses))


def _raw_oxts_dir(kitti_root: Path, sequence_name: str) -> Path:
    raw_name = sequence_name.rsplit("_", 1)[0]
    date = "_".join(raw_name.split("_")[:3])
    return kitti_root / date / raw_name / "oxts" / "data"


def _load_oxts_poses(kitti_root: Path, sequence_name: str,
                     stems: List[str]) -> Optional[torch.Tensor]:
    oxts_dir = _raw_oxts_dir(kitti_root, sequence_name)
    paths = [oxts_dir / f"{stem}.txt" for stem in stems]
    if not all(path.exists() for path in paths):
        return None

    first = np.loadtxt(paths[0], dtype=np.float64)
    scale = math.cos(math.radians(float(first[0])))
    poses = [_oxts_pose(first, scale)]
    for path in paths[1:]:
        poses.append(_oxts_pose(np.loadtxt(path, dtype=np.float64), scale))
    return _normalize_poses(np.stack(poses))


def _fallback_poses(n_frames: int) -> torch.Tensor:
    poses = torch.eye(4, dtype=torch.float32).view(1, 4, 4).repeat(n_frames, 1, 1)
    poses[:, 0, 3] = torch.arange(n_frames, dtype=torch.float32) * 0.1
    return poses


class KITTILongSequenceDataset(Dataset):
    """Loads overlapping KITTI windows with optional OXTS-relative poses."""

    def __init__(
        self,
        root: str = "/hdd3/kykt26/data",
        sequence: Optional[str] = None,
        sequence_length: int = 8,
        overlap: int = 4,
        windows_per_sample: int = 4,
        min_sequence_frames: int = 50,
        max_frames_per_sequence: int = 100,
        max_sequences: int = 0,
        n_patches: int = 196,
        d_model: int = 768,
        n_regimes: int = 6,
        n_slots: int = 16,
    ):
        if sequence_length <= 0:
            raise ValueError("sequence_length must be positive")
        if overlap < 0 or overlap >= sequence_length:
            raise ValueError("overlap must be in [0, sequence_length)")
        if windows_per_sample <= 0:
            raise ValueError("windows_per_sample must be positive")

        self.rectified_root, self.kitti_root = _resolve_roots(root)
        self.sequence_length = int(sequence_length)
        self.overlap = int(overlap)
        self.step = self.sequence_length - self.overlap
        self.windows_per_sample = int(windows_per_sample)
        self.n_patches = int(n_patches)
        self.d_model = int(d_model)
        self.n_regimes = int(n_regimes)
        self.n_slots = int(n_slots)
        self.samples: List[Tuple[Path, List[str]]] = []

        if not self.rectified_root.exists():
            raise FileNotFoundError(f"KITTI rectified root not found: {self.rectified_root}")

        sequence_dirs = sorted(path for path in self.rectified_root.iterdir() if path.is_dir())
        if sequence is not None:
            sequence_dirs = [path for path in sequence_dirs if path.name == sequence]
        if max_sequences > 0:
            sequence_dirs = sequence_dirs[:max_sequences]

        required_frames = self.sequence_length + (self.windows_per_sample - 1) * self.step
        for seq_dir in sequence_dirs:
            stems = sorted(
                path.stem for path in seq_dir.glob("*.jpg")
                if (seq_dir / f"{path.stem}.npy").exists()
            )
            if max_frames_per_sequence > 0:
                stems = stems[:max_frames_per_sequence]
            if len(stems) < max(min_sequence_frames, required_frames):
                continue
            for start in range(0, len(stems) - required_frames + 1, self.step):
                self.samples.append((seq_dir, stems[start:start + required_frames]))

    def __len__(self) -> int:
        return len(self.samples)

    def _load_image(self, path: Path) -> torch.Tensor:
        image = Image.open(path).convert("RGB")
        arr = np.asarray(image, dtype=np.float32) / 255.0
        return torch.from_numpy(arr).permute(2, 0, 1).contiguous()

    def _load_depth(self, path: Path) -> torch.Tensor:
        return torch.from_numpy(np.load(path).astype(np.float32))

    def _load_poses(self, seq_dir: Path, stems: List[str]) -> Tuple[torch.Tensor, str]:
        frame_indices = [int(stem) for stem in stems]
        poses = _load_pose_txt(seq_dir, frame_indices)
        if poses is not None:
            return poses, "poses.txt"
        poses = _load_oxts_poses(self.kitti_root, seq_dir.name, stems)
        if poses is not None:
            return poses, "oxts"
        return _fallback_poses(len(stems)), "linear_fallback"

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        seq_dir, segment_stems = self.samples[idx]
        segment_poses, pose_source = self._load_poses(seq_dir, segment_stems)

        windows = []
        for window_idx in range(self.windows_per_sample):
            start = window_idx * self.step
            stems = segment_stems[start:start + self.sequence_length]
            images, depths, valid_masks, features = [], [], [], []
            pointmaps, pointmap_masks, intrinsics = [], [], []
            for stem in stems:
                image = self._load_image(seq_dir / f"{stem}.jpg")
                depth = self._load_depth(seq_dir / f"{stem}.npy")
                intr = _read_intrinsics(seq_dir, depth.shape[1], depth.shape[0])
                pointmap, pointmap_mask = pointmap_from_depth(depth, intr, self.n_patches)
                images.append(image)
                depths.append(depth)
                valid_masks.append((depth > 0) & torch.isfinite(depth))
                features.append(image_to_patch_features(image, depth, self.d_model, self.n_patches))
                pointmaps.append(pointmap)
                pointmap_masks.append(pointmap_mask)
                intrinsics.append(intr)

            pose_slice = segment_poses[start:start + self.sequence_length]
            translation_delta = (pose_slice[-1, :3, 3] - pose_slice[0, :3, 3]).norm()
            windows.append({
                "features": torch.stack(features),
                "images": torch.stack(images),
                "depth_gt": torch.stack(depths),
                "valid_mask": torch.stack(valid_masks),
                "pointmap_gt": torch.stack(pointmaps),
                "pointmap_mask": torch.stack(pointmap_masks),
                "intrinsics": torch.stack(intrinsics),
                "camera_poses": pose_slice,
                "pointmap_change": translation_delta / (translation_delta + 1.0),
                "frame_ids": stems,
            })

        regime = torch.zeros(self.windows_per_sample, self.n_regimes, dtype=torch.float32)
        regime[:, 0] = 1.0
        return {
            "features": torch.stack([w["features"] for w in windows]),
            "images": torch.stack([w["images"] for w in windows]),
            "depth_gt": torch.stack([w["depth_gt"] for w in windows]),
            "depth": torch.stack([w["depth_gt"] for w in windows]),
            "valid_mask": torch.stack([w["valid_mask"] for w in windows]),
            "pointmap_gt": torch.stack([w["pointmap_gt"] for w in windows]),
            "pointmap_mask": torch.stack([w["pointmap_mask"] for w in windows]),
            "intrinsics": torch.stack([w["intrinsics"] for w in windows]),
            "camera_poses": torch.stack([w["camera_poses"] for w in windows]),
            "regime": regime,
            "conflict_label": torch.zeros(self.windows_per_sample, dtype=torch.float32),
            "repair_label": torch.zeros(self.windows_per_sample, dtype=torch.long),
            "region_label": torch.ones(self.windows_per_sample, self.n_slots, dtype=torch.long),
            "pointmap_change": torch.stack([w["pointmap_change"] for w in windows]),
            "sequence_name": seq_dir.name,
            "frame_ids": [w["frame_ids"] for w in windows],
            "pose_source": pose_source,
        }


def collate_kitti_long(batch: List[Dict[str, torch.Tensor]]) -> Dict[str, object]:
    """Stack tensor fields and keep metadata fields as Python lists."""
    result: Dict[str, object] = {}
    for key in batch[0].keys():
        values = [item[key] for item in batch]
        if torch.is_tensor(values[0]):
            result[key] = torch.stack(values)
        else:
            result[key] = values
    return result
