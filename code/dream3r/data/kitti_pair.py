"""KITTI rectified image-pair dataset for Stage 1 real-data smoke runs."""

from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset

from dream3r.data_kitti import default_kitti_intrinsics


def _resolve_rectified_root(root: str) -> Path:
    path = Path(root)
    nested = path / "kitti" / "rectified"
    return nested if nested.exists() else path


def _read_intrinsics(seq_dir: Path, width: int, height: int) -> torch.Tensor:
    cam_path = seq_dir / "cam.txt"
    if cam_path.exists():
        cam = np.loadtxt(cam_path, dtype=np.float32)
        if cam.shape == (3, 3):
            return torch.from_numpy(cam)
    return default_kitti_intrinsics(width, height)


class KITTIPairDataset(Dataset):
    """Loads frame pairs from `/kitti/rectified/<sequence>` directories."""

    def __init__(
        self,
        root: str = "/hdd3/kykt26/data/kitti/rectified",
        sequence: Optional[str] = None,
        frame_gaps: Iterable[int] = (1, 2, 3),
        max_sequences: int = 0,
    ):
        self.root = _resolve_rectified_root(root)
        self.frame_gaps = tuple(sorted(set(int(gap) for gap in frame_gaps if int(gap) > 0)))
        self.pairs: List[Tuple[Path, str, str]] = []

        if not self.root.exists():
            raise FileNotFoundError(f"KITTI rectified root not found: {self.root}")

        sequence_dirs = sorted(path for path in self.root.iterdir() if path.is_dir())
        if sequence is not None:
            sequence_dirs = [path for path in sequence_dirs if path.name == sequence]
        if max_sequences > 0:
            sequence_dirs = sequence_dirs[:max_sequences]

        for seq_dir in sequence_dirs:
            stems = sorted(
                path.stem for path in seq_dir.glob("*.jpg")
                if (seq_dir / f"{path.stem}.npy").exists()
            )
            for index, stem in enumerate(stems):
                for gap in self.frame_gaps:
                    next_index = index + gap
                    if next_index < len(stems):
                        self.pairs.append((seq_dir, stem, stems[next_index]))

    def __len__(self) -> int:
        return len(self.pairs)

    def _load_image(self, path: Path) -> torch.Tensor:
        image = Image.open(path).convert("RGB")
        arr = np.asarray(image, dtype=np.float32) / 255.0
        return torch.from_numpy(arr).permute(2, 0, 1).contiguous()

    def _load_depth(self, path: Path) -> torch.Tensor:
        return torch.from_numpy(np.load(path).astype(np.float32))

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        seq_dir, stem_a, stem_b = self.pairs[idx]
        images, depths, masks = [], [], []
        for stem in (stem_a, stem_b):
            image = self._load_image(seq_dir / f"{stem}.jpg")
            depth = self._load_depth(seq_dir / f"{stem}.npy")
            images.append(image)
            depths.append(depth)
            masks.append((depth > 0) & torch.isfinite(depth))

        height, width = depths[0].shape
        intrinsics = _read_intrinsics(seq_dir, width, height).repeat(2, 1, 1)
        return {
            "images": torch.stack(images),
            "intrinsics": intrinsics,
            "depth_gt": torch.stack(depths),
            "valid_mask": torch.stack(masks),
            "sequence_name": seq_dir.name,
            "frame_ids": (stem_a, stem_b),
        }
