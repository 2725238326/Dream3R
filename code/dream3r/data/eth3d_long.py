"""ETH3D Low-res many-view rig dataset, KITTI-compatible long-window interface.

Each sample is one window (`windows_per_sample=1`) of `sequence_length` frames
from a single rig camera in one scene. Pointmap GT is built from the
COLMAP sparse `points3D.txt` reconstruction projected into each image and
bucketed into a `n_patches = patch_grid**2` grid (median depth per patch).
"""

from pathlib import Path
from typing import Dict, List, Optional

import math
import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset


SCENES = ["delivery_area", "electro", "forest", "playground", "terrains"]


def _read_cameras_txt(path: Path) -> Dict[int, Dict[str, object]]:
    cams: Dict[int, Dict[str, object]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        cam_id = int(parts[0])
        cams[cam_id] = {
            "model": parts[1],
            "width": int(parts[2]),
            "height": int(parts[3]),
            "params": [float(p) for p in parts[4:]],
        }
    return cams


def _read_images_txt(path: Path) -> List[Dict[str, object]]:
    images: List[Dict[str, object]] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("#"):
            i += 1
            continue
        parts = line.split()
        observations: List = []
        if i + 1 < len(lines):
            obs_parts = lines[i + 1].strip().split()
            for j in range(0, len(obs_parts) - 2, 3):
                p3d_id = int(obs_parts[j + 2])
                if p3d_id == -1:
                    continue
                observations.append((float(obs_parts[j]), float(obs_parts[j + 1]), p3d_id))
        images.append({
            "image_id": int(parts[0]),
            "qw": float(parts[1]), "qx": float(parts[2]),
            "qy": float(parts[3]), "qz": float(parts[4]),
            "tx": float(parts[5]), "ty": float(parts[6]), "tz": float(parts[7]),
            "camera_id": int(parts[8]),
            "name": parts[9],
            "observations": observations,
        })
        i += 2
    return images


def _read_points3d_txt(path: Path) -> Dict[int, np.ndarray]:
    points: Dict[int, np.ndarray] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        points[int(parts[0])] = np.array(
            [float(parts[1]), float(parts[2]), float(parts[3])],
            dtype=np.float64,
        )
    return points


def _quaternion_to_rotation(qw: float, qx: float, qy: float, qz: float) -> np.ndarray:
    norm = math.sqrt(qw * qw + qx * qx + qy * qy + qz * qz)
    if norm < 1e-9:
        return np.eye(3, dtype=np.float64)
    qw, qx, qy, qz = qw / norm, qx / norm, qy / norm, qz / norm
    return np.array([
        [1 - 2 * qy * qy - 2 * qz * qz, 2 * qx * qy - 2 * qz * qw, 2 * qx * qz + 2 * qy * qw],
        [2 * qx * qy + 2 * qz * qw, 1 - 2 * qx * qx - 2 * qz * qz, 2 * qy * qz - 2 * qx * qw],
        [2 * qx * qz - 2 * qy * qw, 2 * qy * qz + 2 * qx * qw, 1 - 2 * qx * qx - 2 * qy * qy],
    ], dtype=np.float64)


def _world_to_camera(image_info: Dict[str, object]) -> np.ndarray:
    R = _quaternion_to_rotation(
        float(image_info["qw"]), float(image_info["qx"]),
        float(image_info["qy"]), float(image_info["qz"]),
    )
    t = np.array(
        [float(image_info["tx"]), float(image_info["ty"]), float(image_info["tz"])],
        dtype=np.float64,
    )
    pose = np.eye(4, dtype=np.float64)
    pose[:3, :3] = R
    pose[:3, 3] = t
    return pose


def _build_patch_pointmap(image_info: Dict[str, object], cam: Dict[str, object],
                          points3d: Dict[int, np.ndarray],
                          patch_grid: int) -> (torch.Tensor, torch.Tensor):
    W = int(cam["width"])
    H = int(cam["height"])
    pose_w2c = _world_to_camera(image_info)
    R = pose_w2c[:3, :3]
    t = pose_w2c[:3, 3]

    pointmap = np.zeros((patch_grid * patch_grid, 3), dtype=np.float32)
    mask = np.zeros((patch_grid * patch_grid,), dtype=np.float32)
    buckets: Dict[int, List[np.ndarray]] = {}

    for u, v, p3d_id in image_info["observations"]:
        p_world = points3d.get(p3d_id)
        if p_world is None:
            continue
        p_cam = R @ p_world + t
        z = p_cam[2]
        if not math.isfinite(z) or z <= 0:
            continue
        col = int(u / W * patch_grid)
        row = int(v / H * patch_grid)
        if col < 0 or col >= patch_grid or row < 0 or row >= patch_grid:
            continue
        idx = row * patch_grid + col
        buckets.setdefault(idx, []).append(p_cam.astype(np.float32))

    for idx, pts_list in buckets.items():
        zs = np.array([p[2] for p in pts_list], dtype=np.float32)
        median_idx = int(np.argsort(zs)[len(zs) // 2])
        pointmap[idx] = pts_list[median_idx]
        mask[idx] = 1.0

    return torch.from_numpy(pointmap), torch.from_numpy(mask)


class ETH3DLongSequenceDataset(Dataset):
    """ETH3D Low-res many-view: KITTI-shaped windows with SfM-sparse pointmap GT."""

    def __init__(
        self,
        root: str = "/hdd3/kykt26/data",
        scene: Optional[str] = None,
        sequence_length: int = 4,
        max_windows_per_scene: int = 10,
        max_windows_per_camera: int = 0,
        image_size: int = 224,
        n_patches: int = 196,
        n_regimes: int = 6,
        n_slots: int = 16,
        scenes: Optional[List[str]] = None,
    ):
        self.root = Path(root) / "eth3d" / "low_res_many_view" / "training"
        if not self.root.exists():
            raise FileNotFoundError(f"ETH3D training root not found: {self.root}")
        self.sequence_length = int(sequence_length)
        self.image_size = int(image_size)
        self.n_patches = int(n_patches)
        self.patch_grid = int(round(self.n_patches ** 0.5))
        if self.patch_grid * self.patch_grid != self.n_patches:
            raise ValueError("n_patches must be a square number")
        self.n_regimes = int(n_regimes)
        self.n_slots = int(n_slots)
        self.max_windows_per_scene = int(max_windows_per_scene)
        self.max_windows_per_camera = int(max_windows_per_camera)
        self._scene_cache: Dict[str, Dict[str, object]] = {}
        self.samples: List[Dict[str, object]] = []

        scene_list = [scene] if scene else (scenes or SCENES)
        for scene_name in scene_list:
            scene_dir = self.root / scene_name
            if not scene_dir.is_dir():
                continue
            self._load_scene(scene_name, scene_dir)

    def _load_scene(self, scene_name: str, scene_dir: Path):
        cal_dir = scene_dir / "rig_calibration_undistorted"
        cams = _read_cameras_txt(cal_dir / "cameras.txt")
        images = _read_images_txt(cal_dir / "images.txt")
        points3d = _read_points3d_txt(cal_dir / "points3D.txt")

        by_cam: Dict[int, List[Dict[str, object]]] = {}
        for img in images:
            by_cam.setdefault(int(img["camera_id"]), []).append(img)
        for cam_id in by_cam:
            by_cam[cam_id].sort(key=lambda x: x["name"])

        self._scene_cache[scene_name] = {
            "cams": cams,
            "points3d": points3d,
            "scene_dir": scene_dir,
        }

        windows_in_scene = 0
        for cam_id, imgs in sorted(by_cam.items()):
            windows_in_camera = 0
            n = len(imgs)
            for start in range(0, n - self.sequence_length + 1, self.sequence_length):
                if (self.max_windows_per_scene > 0
                        and windows_in_scene >= self.max_windows_per_scene):
                    break
                if (self.max_windows_per_camera > 0
                        and windows_in_camera >= self.max_windows_per_camera):
                    break
                window = imgs[start:start + self.sequence_length]
                cam_tag = window[0]["name"].split("/")[0]
                sequence_name = f"{scene_name}__{cam_tag}__{start:04d}"
                self.samples.append({
                    "sequence_name": sequence_name,
                    "scene_name": scene_name,
                    "camera_id": cam_id,
                    "camera_tag": cam_tag,
                    "window_start": start,
                    "images": window,
                })
                windows_in_scene += 1
                windows_in_camera += 1
            if (self.max_windows_per_scene > 0
                    and windows_in_scene >= self.max_windows_per_scene):
                break

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Dict[str, object]:
        sample = self.samples[idx]
        scene_name = sample["scene_name"]
        scene = self._scene_cache[scene_name]
        cams = scene["cams"]
        points3d = scene["points3d"]
        scene_dir = scene["scene_dir"]

        N = self.sequence_length
        S = self.image_size
        P = self.n_patches

        images = torch.zeros(N, 3, S, S, dtype=torch.float32)
        pointmap_gt = torch.zeros(N, P, 3, dtype=torch.float32)
        pointmap_mask = torch.zeros(N, P, dtype=torch.float32)
        intrinsics = torch.zeros(N, 3, 3, dtype=torch.float32)
        camera_poses = torch.eye(4).view(1, 4, 4).repeat(N, 1, 1).float()

        for i, img_info in enumerate(sample["images"]):
            cam_id = int(img_info["camera_id"])
            cam = cams[cam_id]

            img_path = scene_dir / "images" / img_info["name"]
            pil = Image.open(img_path).convert("RGB").resize((S, S), Image.BILINEAR)
            arr = np.asarray(pil, dtype=np.float32) / 255.0
            images[i] = torch.from_numpy(arr).permute(2, 0, 1)

            fx, fy, cx, cy = cam["params"][:4]
            sx = S / float(cam["width"])
            sy = S / float(cam["height"])
            intrinsics[i] = torch.tensor([
                [fx * sx, 0.0, cx * sx],
                [0.0, fy * sy, cy * sy],
                [0.0, 0.0, 1.0],
            ], dtype=torch.float32)

            pose = _world_to_camera(img_info)
            camera_poses[i] = torch.from_numpy(pose.astype(np.float32))

            pm, mk = _build_patch_pointmap(img_info, cam, points3d, self.patch_grid)
            pointmap_gt[i] = pm
            pointmap_mask[i] = mk

        first_inv = torch.linalg.inv(camera_poses[0])
        camera_poses = first_inv @ camera_poses

        return {
            "images": images.unsqueeze(0),
            "pointmap_gt": pointmap_gt.unsqueeze(0),
            "pointmap_mask": pointmap_mask.unsqueeze(0),
            "intrinsics": intrinsics.unsqueeze(0),
            "camera_poses": camera_poses.unsqueeze(0),
            "depth_gt": torch.zeros(1, N, S, S, dtype=torch.float32),
            "valid_mask": torch.zeros(1, N, S, S, dtype=torch.bool),
            "regime": torch.zeros(1, self.n_regimes, dtype=torch.float32),
            "conflict_label": torch.zeros(1, dtype=torch.float32),
            "repair_label": torch.zeros(1, dtype=torch.long),
            "region_label": torch.ones(1, self.n_slots, dtype=torch.long),
            "sequence_name": sample["sequence_name"],
            "scene_name": scene_name,
            "camera_tag": sample["camera_tag"],
            "window_start": sample["window_start"],
        }
