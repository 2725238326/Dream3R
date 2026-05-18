"""
Deterministic synthetic sequence dataset for Dream3R development and ablation.

Generates controllable multi-view sequences with known ground truth:
  - Camera poses (translation + rotation along configurable trajectories)
  - 3D pointmaps per frame
  - Dynamic object masks
  - Occlusion patterns
  - Evidence signal ground truth

All randomness is seeded for reproducibility.
"""

import torch
from torch.utils.data import Dataset
from typing import Dict, Optional, Tuple
import math


class SyntheticSequenceDataset(Dataset):
    """
    Generates synthetic multi-view sequences for Dream3R training/testing.

    Each sample is one window of N frames with:
      - images:         [N, 3, H, W] (random textured, not photorealistic)
      - pointmap_gt:    [N, P, 3] ground truth 3D points
      - confidence_gt:  [N, P, 1]
      - dynamic_mask:   [N, P] True = dynamic region
      - camera_poses:   [N, 4, 4] world-to-camera transforms
      - regime:         [n_regimes] soft regime label
      - conflict_label: scalar — 1 if any conflict injected
      - repair_label:   int — which repair action is correct
      - region_label:   [n_slots] — suppress/admit/defer per slot
      - pointmap_change: scalar — normalized scene change between frames
    """

    def __init__(self, n_sequences: int = 100, n_frames: int = 4,
                 height: int = 224, width: int = 224,
                 n_patches: int = 196, n_slots: int = 16,
                 n_regimes: int = 5, d_model: int = 768,
                 seed: int = 42,
                 sequence_length: int = 1,
                 inject_dynamics: bool = True,
                 inject_conflicts: bool = True):
        self.n_sequences = n_sequences
        self.n_frames = n_frames
        self.H = height
        self.W = width
        self.P = n_patches
        self.n_slots = n_slots
        self.n_regimes = n_regimes
        self.d_model = d_model
        self.seed = seed
        self.sequence_length = sequence_length
        self.inject_dynamics = inject_dynamics
        self.inject_conflicts = inject_conflicts

    def __len__(self) -> int:
        return self.n_sequences

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        gen = torch.Generator()
        gen.manual_seed(self.seed + idx)
        if self.sequence_length > 1:
            windows = [self._generate_window(idx, t, gen) for t in range(self.sequence_length)]
            return {
                key: torch.stack([w[key] for w in windows])
                for key in windows[0].keys()
            }
        return self._generate_window(idx, 0, gen)

    def _generate_window(self, idx: int, window_idx: int,
                         gen: torch.Generator) -> Dict[str, torch.Tensor]:
        N = self.n_frames
        P = self.P

        trajectory = self._generate_trajectory(idx, window_idx, gen)
        pointmap_gt = self._generate_pointmap(trajectory, gen)
        confidence_gt = torch.rand(N, P, 1, generator=gen) * 0.5 + 0.5

        dynamic_mask = torch.zeros(N, P, dtype=torch.bool)
        if self.inject_dynamics and (idx + window_idx) % 3 == 0:
            n_dyn = max(1, P // 8)
            start = torch.randint(0, P - n_dyn, (1,), generator=gen).item()
            dynamic_mask[:, start:start + n_dyn] = True
            confidence_gt[:, start:start + n_dyn] *= 0.3

        base_features = torch.randn(1, P, self.d_model, generator=gen) * 0.1
        temporal_offset = window_idx * 0.03
        features = base_features.expand(N, -1, -1).clone()
        features = features + torch.randn(N, P, self.d_model, generator=gen) * 0.02
        features = features + temporal_offset

        regime = torch.zeros(self.n_regimes)
        regime_idx = (idx + window_idx) % self.n_regimes
        regime[regime_idx] = 0.7
        regime[(regime_idx + 1) % self.n_regimes] = 0.2
        regime[(regime_idx + 2) % self.n_regimes] = 0.1

        conflict = 0
        repair = 0
        if self.inject_conflicts and (idx + window_idx) % 5 == 0:
            conflict = 1
            repair = torch.randint(0, 6, (1,), generator=gen).item()

        region_label = torch.randint(0, 3, (self.n_slots,), generator=gen)

        delta = (pointmap_gt[1:] - pointmap_gt[:-1]).norm(dim=-1).mean()
        pointmap_change = (delta / (delta + 1.0)).item()

        return {
            "features": features,
            "pointmap_gt": pointmap_gt,
            "confidence_gt": confidence_gt,
            "dynamic_mask": dynamic_mask,
            "camera_poses": trajectory,
            "regime": regime,
            "conflict_label": torch.tensor(conflict, dtype=torch.float32),
            "repair_label": torch.tensor(repair, dtype=torch.long),
            "region_label": region_label,
            "pointmap_change": torch.tensor(pointmap_change, dtype=torch.float32),
            "sequence_idx": torch.tensor(idx, dtype=torch.long),
        }

    def _generate_trajectory(self, idx: int,
                              window_idx: int,
                              gen: torch.Generator) -> torch.Tensor:
        N = self.n_frames
        poses = torch.eye(4).unsqueeze(0).repeat(N, 1, 1)

        speed = 0.1 + (idx % 10) * 0.02
        for i in range(N):
            global_i = window_idx * N + i
            angle = speed * global_i * 0.3
            poses[i, 0, 3] = speed * global_i
            poses[i, 1, 3] = 0.05 * math.sin(angle * 2)
            poses[i, 2, 3] = 0.02 * math.cos(angle)
            c, s = math.cos(angle), math.sin(angle)
            poses[i, 0, 0] = c
            poses[i, 0, 2] = s
            poses[i, 2, 0] = -s
            poses[i, 2, 2] = c

        return poses

    def _generate_pointmap(self, poses: torch.Tensor,
                            gen: torch.Generator) -> torch.Tensor:
        N = self.n_frames
        P = self.P

        world_points = torch.randn(P, 3, generator=gen) * 2.0
        pointmaps = torch.zeros(N, P, 3)

        for i in range(N):
            R = poses[i, :3, :3]
            t = poses[i, :3, 3]
            pointmaps[i] = (world_points @ R.t()) + t.unsqueeze(0)

        return pointmaps


class DTUDataset(Dataset):
    """
    DTU multi-view stereo dataset loader.

    Expects the standard DTU directory structure at data_root:
      data_root/
        scan{id}/
          image/
          depth/
          cameras.npz

    This is a stub that defines the interface. Actual loading requires
    the dataset to be available on the server at /hdd3/kykt26/data/dtu/.
    """

    def __init__(self, data_root: str, split: str = "train",
                 n_frames: int = 4, img_size: Tuple[int, int] = (384, 512),
                 n_patches: int = 196):
        self.data_root = data_root
        self.split = split
        self.n_frames = n_frames
        self.img_size = img_size
        self.n_patches = n_patches
        self._scan_ids = self._load_split()

    def _load_split(self):
        splits = {
            "train": list(range(1, 80)),
            "val": list(range(80, 100)),
            "test": list(range(100, 125)),
        }
        return splits.get(self.split, splits["train"])

    def __len__(self) -> int:
        return len(self._scan_ids) * 10

    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        scan_idx = idx // 10
        window_idx = idx % 10
        scan_id = self._scan_ids[scan_idx % len(self._scan_ids)]

        N = self.n_frames
        P = self.n_patches
        H, W = self.img_size

        return {
            "images": torch.randn(N, 3, H, W),
            "pointmap_gt": torch.randn(N, P, 3),
            "confidence_gt": torch.rand(N, P, 1),
            "camera_poses": torch.eye(4).unsqueeze(0).repeat(N, 1, 1),
            "scan_id": torch.tensor(scan_id),
            "window_idx": torch.tensor(window_idx),
        }
