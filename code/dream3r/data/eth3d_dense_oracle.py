"""Dense laser-scan ground-truth helpers for ETH3D Low-res many-view.

Reads ``rig_scan_eval/scan*.ply`` per scene plus the
``scan_alignment.mlp`` MeshLab project file that gives each scan PLY's
4x4 transform into the SfM world frame, and builds patch-level dense
pointmap GT compatible with ``ETH3DLongSequenceDataset.__getitem__``.

This is a strictly opt-in dense GT source. The sparse SfM path used by
the default ``ETH3DLongSequenceDataset`` is unchanged.
"""

import math
import struct
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List

import numpy as np
import torch


def _read_mlp_alignment(mlp_path: Path) -> Dict[str, np.ndarray]:
    """Parse a MeshLab project (.mlp) and return per-scan 4x4 transforms.

    Returns a dict {"scan1.ply": 4x4 numpy, ...}. The matrix transforms
    points from the scan's local frame into the SfM world frame.
    """
    tree = ET.parse(mlp_path)
    root = tree.getroot()
    out: Dict[str, np.ndarray] = {}
    for mesh in root.iter("MLMesh"):
        filename = mesh.attrib.get("filename") or mesh.attrib.get("label")
        if filename is None:
            continue
        mat_el = mesh.find("MLMatrix44")
        if mat_el is None or mat_el.text is None:
            continue
        nums: List[float] = []
        for tok in mat_el.text.strip().split():
            try:
                nums.append(float(tok))
            except ValueError:
                continue
        if len(nums) != 16:
            raise ValueError(
                f"MLMatrix44 for {filename}: expected 16 floats, got {len(nums)}"
            )
        out[filename] = np.array(nums, dtype=np.float64).reshape(4, 4)
    return out


def _read_ply_vertices_binary_le(ply_path: Path) -> np.ndarray:
    """Read xyz floats from a binary little-endian PLY.

    Assumes the first element is `vertex` with at least properties
    x, y, z (any further per-vertex properties are skipped). Stops
    reading after the vertex element; subsequent elements (camera,
    etc.) are ignored.

    Returns an (N, 3) float64 numpy array in the scan's local frame.
    """
    with open(ply_path, "rb") as f:
        header_lines: List[bytes] = []
        while True:
            line = f.readline()
            if not line:
                raise ValueError(f"unexpected EOF in PLY header: {ply_path}")
            header_lines.append(line)
            if line.strip() == b"end_header":
                break
        header = b"".join(header_lines).decode("ascii", errors="replace")
        if "format binary_little_endian" not in header:
            raise ValueError(
                f"only binary_little_endian PLYs supported here: {ply_path}"
            )

        # Parse the vertex element: count + property types in order.
        vertex_count = 0
        properties: List[str] = []
        in_vertex = False
        for raw in header.splitlines():
            line = raw.strip()
            if line.startswith("element "):
                parts = line.split()
                if parts[1] == "vertex":
                    in_vertex = True
                    vertex_count = int(parts[2])
                else:
                    in_vertex = False
            elif line.startswith("property ") and in_vertex:
                parts = line.split()
                # "property float x" -> "float"
                properties.append(parts[1])
        if vertex_count == 0 or not properties:
            raise ValueError(f"no vertex element in PLY: {ply_path}")

        type_map = {
            "float": ("<f", 4), "float32": ("<f", 4),
            "double": ("<d", 8), "float64": ("<d", 8),
            "int": ("<i", 4), "int32": ("<i", 4),
            "uint": ("<I", 4), "uint32": ("<I", 4),
            "short": ("<h", 2), "int16": ("<h", 2),
            "ushort": ("<H", 2), "uint16": ("<H", 2),
            "char": ("<b", 1), "int8": ("<b", 1),
            "uchar": ("<B", 1), "uint8": ("<B", 1),
        }
        per_vertex_size = 0
        prop_fmts: List[tuple] = []
        for p in properties:
            if p not in type_map:
                raise ValueError(f"unsupported PLY property type: {p}")
            fmt, size = type_map[p]
            prop_fmts.append((fmt, size))
            per_vertex_size += size

        # Use numpy structured read for speed: build a dtype matching
        # property order, then take the first 3 columns by name.
        names = ["x", "y", "z"] + [f"_p{i}" for i in range(3, len(properties))]
        np_types = []
        for (fmt, _size) in prop_fmts:
            np_types.append({
                "<f": np.float32, "<d": np.float64,
                "<i": np.int32, "<I": np.uint32,
                "<h": np.int16, "<H": np.uint16,
                "<b": np.int8, "<B": np.uint8,
            }[fmt])
        dtype = np.dtype({"names": names, "formats": np_types})
        if dtype.itemsize != per_vertex_size:
            # Falls back to manual unpack if numpy packs differently.
            raw_bytes = f.read(per_vertex_size * vertex_count)
            xyz = np.empty((vertex_count, 3), dtype=np.float64)
            offset = 0
            for i in range(vertex_count):
                vals = []
                for (fmt, size) in prop_fmts:
                    vals.append(struct.unpack(fmt, raw_bytes[offset:offset + size])[0])
                    offset += size
                xyz[i, 0] = vals[0]
                xyz[i, 1] = vals[1]
                xyz[i, 2] = vals[2]
            return xyz

        arr = np.frombuffer(
            f.read(per_vertex_size * vertex_count), dtype=dtype, count=vertex_count,
        )
        xyz = np.stack(
            [arr["x"].astype(np.float64),
             arr["y"].astype(np.float64),
             arr["z"].astype(np.float64)],
            axis=-1,
        )
        return xyz


def load_dense_world_points(scene_dir: Path, max_total_points: int = 0) -> np.ndarray:
    """Load all scan PLYs for a scene and transform them into world frame.

    Returns an (N, 3) float64 numpy array of world-frame xyz points.

    When ``max_total_points > 0`` the final array is uniformly
    sub-sampled to at most that many points (for memory tractability).
    """
    scan_dir = scene_dir / "rig_scan_eval"
    if not scan_dir.is_dir():
        raise FileNotFoundError(f"no rig_scan_eval/ in {scene_dir}")
    mlp_paths = list(scan_dir.glob("*.mlp"))
    if not mlp_paths:
        raise FileNotFoundError(f"no scan_alignment.mlp in {scan_dir}")
    alignments = _read_mlp_alignment(mlp_paths[0])

    chunks: List[np.ndarray] = []
    for ply_name, T in alignments.items():
        ply_path = scan_dir / ply_name
        if not ply_path.exists():
            continue
        local = _read_ply_vertices_binary_le(ply_path)
        # Homogeneous transform local -> world
        ones = np.ones((local.shape[0], 1), dtype=np.float64)
        homo = np.concatenate([local, ones], axis=-1)
        world = (T @ homo.T).T[:, :3]
        chunks.append(world)
    if not chunks:
        raise RuntimeError(f"no scan PLY loaded for scene at {scene_dir}")
    world_pts = np.concatenate(chunks, axis=0)
    if max_total_points > 0 and world_pts.shape[0] > max_total_points:
        rng = np.random.default_rng(seed=7)
        sel = rng.choice(world_pts.shape[0], size=max_total_points, replace=False)
        world_pts = world_pts[sel]
    return world_pts


def build_dense_patch_pointmap(
    world_points: np.ndarray,
    image_info: Dict[str, object],
    cam: Dict[str, object],
    patch_grid: int,
    z_min: float = 0.05,
    z_max: float = 200.0,
) -> tuple:
    """Project world-frame dense points into one camera and bucket to patches.

    Mirrors ``eth3d_long._build_patch_pointmap`` but uses dense
    world-frame points instead of the COLMAP per-image SfM
    observations. Bucketing uses each projected point's (u, v); empty
    buckets get mask=0.

    Returns (pointmap [P, 3] float32, mask [P] float32).
    """
    from dream3r.data.eth3d_long import _world_to_camera

    W = int(cam["width"])
    H = int(cam["height"])
    fx, fy, cx, cy = (float(v) for v in cam["params"][:4])

    pose_w2c = _world_to_camera(image_info)
    R = pose_w2c[:3, :3]
    t = pose_w2c[:3, 3]

    # Vectorized: p_cam = R @ p_world.T + t (broadcast)
    p_cam = (R @ world_points.T).T + t  # (N, 3)
    z = p_cam[:, 2]
    finite = np.isfinite(z)
    front = (z > z_min) & (z < z_max) & finite
    if not front.any():
        return (torch.zeros(patch_grid * patch_grid, 3, dtype=torch.float32),
                torch.zeros(patch_grid * patch_grid, dtype=torch.float32))
    p_cam = p_cam[front]
    z = p_cam[:, 2]
    u = fx * (p_cam[:, 0] / z) + cx
    v = fy * (p_cam[:, 1] / z) + cy

    col = (u / W * patch_grid).astype(np.int32)
    row = (v / H * patch_grid).astype(np.int32)
    in_image = (col >= 0) & (col < patch_grid) & (row >= 0) & (row < patch_grid)
    if not in_image.any():
        return (torch.zeros(patch_grid * patch_grid, 3, dtype=torch.float32),
                torch.zeros(patch_grid * patch_grid, dtype=torch.float32))
    p_cam = p_cam[in_image]
    col = col[in_image]
    row = row[in_image]
    bucket = row * patch_grid + col

    P = patch_grid * patch_grid
    pointmap = np.zeros((P, 3), dtype=np.float32)
    mask = np.zeros(P, dtype=np.float32)

    # Per-bucket median-z point. We sort by bucket then pick median index.
    order = np.argsort(bucket, kind="stable")
    bucket_sorted = bucket[order]
    p_cam_sorted = p_cam[order]
    # Find run boundaries
    unique_buckets, starts = np.unique(bucket_sorted, return_index=True)
    ends = np.append(starts[1:], bucket_sorted.shape[0])
    for b, s, e in zip(unique_buckets, starts, ends):
        sub = p_cam_sorted[s:e]
        zs = sub[:, 2]
        med = int(np.argsort(zs)[zs.shape[0] // 2])
        pointmap[b] = sub[med].astype(np.float32)
        mask[b] = 1.0

    return torch.from_numpy(pointmap), torch.from_numpy(mask)
