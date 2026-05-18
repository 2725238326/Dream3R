"""KITTI rectified sequence loader for real-data Dream3R smoke evaluation."""

from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from torch.utils.data import Dataset


def default_kitti_intrinsics(width: int, height: int) -> torch.Tensor:
    """Approximate KITTI intrinsics scaled to the rectified image size."""
    # KITTI raw image is commonly around 1242x375 with fx~721, cx~609.
    sx = width / 1242.0
    sy = height / 375.0
    return torch.tensor([
        [721.5377 * sx, 0.0, 609.5593 * sx],
        [0.0, 721.5377 * sy, 172.8540 * sy],
        [0.0, 0.0, 1.0],
    ], dtype=torch.float32)


def pointmap_from_depth(depth: torch.Tensor,
                        intrinsics: torch.Tensor,
                        n_patches: int = 196) -> Tuple[torch.Tensor, torch.Tensor]:
    """Project depth image to a sampled pointmap [P, 3] plus valid mask [P]."""
    if depth.dim() != 2:
        raise ValueError("depth must have shape [H, W]")
    H, W = depth.shape
    grid = int(round(n_patches ** 0.5))
    if grid * grid != n_patches:
        raise ValueError("n_patches must be a square number")

    depth_small = F.interpolate(
        depth.view(1, 1, H, W).float(),
        size=(grid, grid),
        mode="nearest",
    ).view(grid, grid)
    ys = torch.linspace(0, H - 1, grid, dtype=torch.float32, device=depth.device)
    xs = torch.linspace(0, W - 1, grid, dtype=torch.float32, device=depth.device)
    yy, xx = torch.meshgrid(ys, xs, indexing="ij")

    fx = intrinsics[0, 0].clamp_min(1e-6)
    fy = intrinsics[1, 1].clamp_min(1e-6)
    cx = intrinsics[0, 2]
    cy = intrinsics[1, 2]
    z = depth_small
    x = (xx - cx) * z / fx
    y = (yy - cy) * z / fy
    pointmap = torch.stack([x, y, z], dim=-1).view(-1, 3)
    mask = (z.view(-1) > 0) & torch.isfinite(z.view(-1))
    pointmap = torch.where(mask.unsqueeze(-1), pointmap, torch.zeros_like(pointmap))
    return pointmap, mask.float()


def image_to_patch_features(image: torch.Tensor,
                            depth: torch.Tensor,
                            d_model: int = 768,
                            n_patches: int = 196) -> torch.Tensor:
    """Create deterministic patch features from RGB/depth for head-only smoke runs."""
    grid = int(round(n_patches ** 0.5))
    rgb = F.interpolate(
        image.unsqueeze(0), size=(grid, grid), mode="bilinear", align_corners=False
    ).squeeze(0).permute(1, 2, 0).reshape(n_patches, 3)
    depth_small = F.interpolate(
        depth.view(1, 1, *depth.shape), size=(grid, grid), mode="nearest"
    ).view(n_patches, 1)
    if (depth_small > 0).any():
        depth_norm = depth_small / depth_small[depth_small > 0].mean().clamp_min(1e-6)
    else:
        depth_norm = depth_small
    base = torch.cat([rgb, depth_norm.clamp(0, 10) / 10.0], dim=-1)
    reps = (d_model + base.shape[-1] - 1) // base.shape[-1]
    return base.repeat(1, reps)[:, :d_model].contiguous()


class KITTIRectifiedSequenceDataset(Dataset):
    """Loads windows from `/kitti/rectified/*` directories with jpg+npy pairs."""

    def __init__(self, data_root: str = "/hdd3/kykt26/data",
                 n_frames: int = 4,
                 n_patches: int = 196,
                 d_model: int = 768,
                 max_sequences: int = 0):
        self.root = Path(data_root)
        self.rectified_root = self.root / "kitti" / "rectified"
        self.n_frames = n_frames
        self.n_patches = n_patches
        self.d_model = d_model
        self.windows: List[Tuple[Path, List[str]]] = []

        if not self.rectified_root.exists():
            raise FileNotFoundError(f"KITTI rectified root not found: {self.rectified_root}")

        sequence_dirs = sorted([p for p in self.rectified_root.iterdir() if p.is_dir()])
        if max_sequences > 0:
            sequence_dirs = sequence_dirs[:max_sequences]
        for seq_dir in sequence_dirs:
            stems = sorted(
                p.stem for p in seq_dir.glob("*.jpg")
                if (seq_dir / f"{p.stem}.npy").exists()
            )
            for start in range(0, max(0, len(stems) - n_frames + 1), n_frames):
                self.windows.append((seq_dir, stems[start:start + n_frames]))

    def __len__(self) -> int:
        return len(self.windows)

    def _load_image(self, path: Path) -> torch.Tensor:
        image = Image.open(path).convert("RGB")
        arr = np.asarray(image, dtype=np.float32) / 255.0
        return torch.from_numpy(arr).permute(2, 0, 1).contiguous()

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        seq_dir, stems = self.windows[idx]
        images, depths, features, pointmaps, masks, intrinsics = [], [], [], [], [], []
        for frame_idx, stem in enumerate(stems):
            image = self._load_image(seq_dir / f"{stem}.jpg")
            depth = torch.from_numpy(np.load(seq_dir / f"{stem}.npy").astype(np.float32))
            intr = default_kitti_intrinsics(depth.shape[1], depth.shape[0])
            pointmap, mask = pointmap_from_depth(depth, intr, self.n_patches)
            feat = image_to_patch_features(image, depth, self.d_model, self.n_patches)
            images.append(image)
            depths.append(depth)
            features.append(feat)
            pointmaps.append(pointmap)
            masks.append(mask)
            intrinsics.append(intr)

        poses = torch.eye(4).view(1, 4, 4).repeat(self.n_frames, 1, 1)
        poses[:, 0, 3] = torch.arange(self.n_frames).float() * 0.1
        return {
            "features": torch.stack(features),
            "images": torch.stack(images),
            "depth": torch.stack(depths),
            "pointmap_gt": torch.stack(pointmaps),
            "pointmap_mask": torch.stack(masks),
            "intrinsics": torch.stack(intrinsics),
            "camera_poses": poses,
            "conflict_label": torch.tensor(0.0),
            "repair_label": torch.tensor(0, dtype=torch.long),
            "region_label": torch.ones(16, dtype=torch.long),
            "sequence_name": seq_dir.name,
            "frame_ids": stems,
        }
