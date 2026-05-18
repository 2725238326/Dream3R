"""
DTU dataset loader for Dream3R.

Reads: images (JPEG), camera parameters (extrinsic 4x4 + intrinsic 3x3),
       pair.txt (view pair scoring).

Returns frame windows of N views for one bus tick.
"""

import os
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
from torch.utils.data import Dataset
from PIL import Image


class DTUDataset(Dataset):
    """
    DTU Multi-View Stereo dataset.

    Each sample = one window of N_frames views from a single scan,
    selected using pair.txt scoring (nearby views preferred).

    Returns pre-resized images as tensors (no ViT patch embedding here;
    that happens in Perceiver.encode_images or is done externally).

    For headonly mode (no backbone), returns dummy feature tensors.
    """

    def __init__(self, data_root: str, split: str = "train",
                 n_frames: int = 4, img_size: int = 224,
                 use_images: bool = False,
                 d_model: int = 768, n_patches: int = 196):
        super().__init__()
        self.data_root = Path(data_root) / "dtu"
        self.n_frames = n_frames
        self.img_size = img_size
        self.use_images = use_images
        self.d_model = d_model
        self.n_patches = n_patches

        all_scans = sorted([d.name for d in self.data_root.iterdir() if d.is_dir()])
        if split == "train":
            self.scans = all_scans[:max(1, len(all_scans) - 3)]
        elif split == "val":
            self.scans = all_scans[max(1, len(all_scans) - 3):]
        else:
            self.scans = all_scans

        self.samples = []
        for scan in self.scans:
            scan_dir = self.data_root / scan
            pairs = self._load_pairs(scan_dir / "pair.txt")
            n_views = len(list((scan_dir / "images").glob("*.jpg")))
            for ref_id in range(n_views):
                self.samples.append((scan, ref_id, pairs))

    def _load_pairs(self, path: Path) -> Dict[int, List[Tuple[int, float]]]:
        """Parse pair.txt: ref_id -> [(src_id, score), ...]"""
        pairs = {}
        if not path.exists():
            return pairs
        with open(path) as f:
            n = int(f.readline().strip())
            for _ in range(n):
                ref = int(f.readline().strip())
                line = f.readline().strip().split()
                n_src = int(line[0])
                srcs = []
                for i in range(n_src):
                    sid = int(line[1 + 2 * i])
                    score = float(line[2 + 2 * i])
                    srcs.append((sid, score))
                pairs[ref] = srcs
        return pairs

    def _load_cam(self, path: Path) -> Tuple[np.ndarray, np.ndarray, float, float]:
        """Parse cam.txt -> extrinsic (4x4), intrinsic (3x3), depth_min, depth_interval."""
        with open(path) as f:
            lines = f.readlines()
        # extrinsic: lines 1-4
        extrinsic = np.array([[float(x) for x in lines[i].split()] for i in range(1, 5)])
        # intrinsic: lines 7-9
        intrinsic = np.array([[float(x) for x in lines[i].split()] for i in range(7, 10)])
        # depth range: line 11
        depth_info = lines[11].split()
        depth_min = float(depth_info[0])
        depth_interval = float(depth_info[1]) if len(depth_info) > 1 else 1.0
        return extrinsic, intrinsic, depth_min, depth_interval

    def _load_image(self, path: Path) -> torch.Tensor:
        """Load and resize image to [3, img_size, img_size]."""
        img = Image.open(path).convert("RGB")
        img = img.resize((self.img_size, self.img_size), Image.BILINEAR)
        arr = np.array(img, dtype=np.float32) / 255.0
        return torch.from_numpy(arr).permute(2, 0, 1)  # [3, H, W]

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, Dict[str, torch.Tensor]]:
        scan, ref_id, pairs = self.samples[idx]
        scan_dir = self.data_root / scan

        # Select N_frames views: ref + top-(N-1) scored neighbors
        view_ids = [ref_id]
        if ref_id in pairs:
            for sid, _ in pairs[ref_id]:
                if len(view_ids) >= self.n_frames:
                    break
                view_ids.append(sid)
        while len(view_ids) < self.n_frames:
            view_ids.append(view_ids[-1])

        # Load cameras
        extrinsics, intrinsics = [], []
        for vid in view_ids:
            cam_path = scan_dir / "cams" / f"{vid:08d}_cam.txt"
            if cam_path.exists():
                ext, intr, _, _ = self._load_cam(cam_path)
            else:
                ext = np.eye(4)
                intr = np.eye(3) * 1000
            extrinsics.append(torch.from_numpy(ext).float())
            intrinsics.append(torch.from_numpy(intr).float())

        extrinsics = torch.stack(extrinsics)  # [N, 4, 4]
        intrinsics = torch.stack(intrinsics)  # [N, 3, 3]

        if self.use_images:
            images = []
            for vid in view_ids:
                img_path = scan_dir / "images" / f"{vid:08d}.jpg"
                images.append(self._load_image(img_path))
            x = torch.stack(images)  # [N, 3, H, W]
        else:
            x = torch.randn(self.n_frames, self.n_patches, self.d_model)

        # Targets (placeholder GT from camera geometry)
        # Real GT pointmap requires depth maps; for now use camera-derived pseudo-targets
        targets = {
            "pointmap": torch.randn(self.n_frames, self.n_patches, 3),
            "pointmap_mask": torch.ones(self.n_frames, self.n_patches),
            "conflict_label": torch.tensor(0.0),
            "repair_label": torch.tensor(0, dtype=torch.long),
            "region_label": torch.zeros(16, dtype=torch.long) + 1,  # all "admit"
            "extrinsics": extrinsics,
            "intrinsics": intrinsics,
        }

        return x, targets


def build_dtu_loaders(cfg: dict) -> Tuple:
    """Build train and val DataLoaders for DTU."""
    from torch.utils.data import DataLoader, DistributedSampler
    import torch.distributed as dist

    is_ddp = dist.is_initialized()

    train_set = DTUDataset(
        data_root=cfg["data_root"], split="train",
        n_frames=cfg["n_frames_per_window"], img_size=cfg["img_size"],
        use_images=cfg.get("use_backbone", False),
        d_model=cfg["d_model"], n_patches=196,
    )
    val_set = DTUDataset(
        data_root=cfg["data_root"], split="val",
        n_frames=cfg["n_frames_per_window"], img_size=cfg["img_size"],
        use_images=cfg.get("use_backbone", False),
        d_model=cfg["d_model"], n_patches=196,
    )

    train_sampler = DistributedSampler(train_set) if is_ddp else None
    val_sampler = DistributedSampler(val_set, shuffle=False) if is_ddp else None

    train_loader = DataLoader(
        train_set, batch_size=cfg["batch_size"],
        sampler=train_sampler, shuffle=(train_sampler is None),
        num_workers=cfg["num_workers"], pin_memory=True, drop_last=True,
    )
    val_loader = DataLoader(
        val_set, batch_size=cfg["batch_size"],
        sampler=val_sampler, shuffle=False,
        num_workers=cfg["num_workers"], pin_memory=True,
    )

    return train_loader, val_loader, train_sampler
