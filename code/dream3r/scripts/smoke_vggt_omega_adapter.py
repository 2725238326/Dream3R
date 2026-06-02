"""One-window VGGT-Omega admission smoke.

This script is intentionally outside the frozen Dream3R core. It validates
whether a VGGT-Omega checkpoint can act as a real proposal teacher and writes a
small normalized payload for later oracle/cache admission. Fallback outputs are
not accepted as success.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import torch


REQUIRED_KEYS = ("depth", "depth_conf", "pose_enc", "camera_and_register_tokens")


def _as_path(path: str) -> Path:
    return Path(path).expanduser().resolve()


def _read_image_list(path: Path) -> List[str]:
    if not path.exists():
        raise FileNotFoundError(f"image list not found: {path}")
    images = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not 1 <= len(images) <= 4:
        raise ValueError(f"expected 1-4 images for one-window smoke, got {len(images)}")
    missing = [name for name in images if not Path(name).expanduser().exists()]
    if missing:
        raise FileNotFoundError(f"image files not found: {missing}")
    return images


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _shape(value: Any) -> List[int] | None:
    if isinstance(value, torch.Tensor):
        return list(value.shape)
    return None


def _tensor_to_cpu(value: Any) -> Any:
    if isinstance(value, torch.Tensor):
        return value.detach().cpu()
    return value


def _normalize_depth(depth: torch.Tensor) -> torch.Tensor:
    depth = depth.detach().float()
    if depth.ndim == 5 and depth.shape[0] == 1:
        depth = depth.squeeze(0)
    if depth.ndim == 4 and depth.shape[-1] == 1:
        depth = depth.squeeze(-1)
    if depth.ndim != 3:
        raise ValueError(f"expected depth shaped [N,H,W], got {tuple(depth.shape)}")
    return depth


def _normalize_intrinsics(intrinsics: torch.Tensor, n_frames: int) -> torch.Tensor:
    intrinsics = intrinsics.detach().float()
    if intrinsics.ndim == 4 and intrinsics.shape[0] == 1:
        intrinsics = intrinsics.squeeze(0)
    if intrinsics.ndim != 3 or intrinsics.shape[-2:] != (3, 3):
        raise ValueError(f"expected intrinsics shaped [N,3,3], got {tuple(intrinsics.shape)}")
    if intrinsics.shape[0] == 1 and n_frames > 1:
        intrinsics = intrinsics.expand(n_frames, -1, -1)
    if intrinsics.shape[0] != n_frames:
        raise ValueError(
            f"intrinsics frame count {intrinsics.shape[0]} does not match depth {n_frames}"
        )
    return intrinsics


def depth_to_camera_pointmap(depth: torch.Tensor, intrinsics: torch.Tensor) -> torch.Tensor:
    """Convert depth maps to camera-frame pointmaps shaped [N, H*W, 3]."""
    depth = _normalize_depth(depth)
    intrinsics = _normalize_intrinsics(intrinsics, int(depth.shape[0])).to(depth.device)
    n_frames, height, width = depth.shape

    ys, xs = torch.meshgrid(
        torch.arange(height, device=depth.device, dtype=depth.dtype),
        torch.arange(width, device=depth.device, dtype=depth.dtype),
        indexing="ij",
    )
    xs = xs.reshape(1, height, width).expand(n_frames, -1, -1)
    ys = ys.reshape(1, height, width).expand(n_frames, -1, -1)

    fx = intrinsics[:, 0, 0].reshape(n_frames, 1, 1).clamp_min(1e-6)
    fy = intrinsics[:, 1, 1].reshape(n_frames, 1, 1).clamp_min(1e-6)
    cx = intrinsics[:, 0, 2].reshape(n_frames, 1, 1)
    cy = intrinsics[:, 1, 2].reshape(n_frames, 1, 1)

    z = depth.clamp_min(0.0)
    x = (xs - cx) * z / fx
    y = (ys - cy) * z / fy
    return torch.stack([x, y, z], dim=-1).reshape(n_frames, height * width, 3)


def _flatten_confidence(depth_conf: torch.Tensor, n_frames: int) -> torch.Tensor:
    conf = depth_conf.detach().float()
    if conf.ndim == 5 and conf.shape[0] == 1:
        conf = conf.squeeze(0)
    if conf.ndim == 4 and conf.shape[-1] == 1:
        conf = conf.squeeze(-1)
    if conf.ndim != 3:
        raise ValueError(f"expected depth_conf shaped [N,H,W], got {tuple(conf.shape)}")
    if conf.shape[0] != n_frames:
        raise ValueError(f"depth_conf frame count {conf.shape[0]} != {n_frames}")
    return conf.reshape(n_frames, -1, 1)


def _load_upstream(repo: Path):
    if not repo.exists():
        raise FileNotFoundError(f"VGGT-Omega repo not found: {repo}")
    sys.path.insert(0, str(repo))
    models_mod = importlib.import_module("vggt_omega.models")
    load_mod = importlib.import_module("vggt_omega.utils.load_fn")
    pose_mod = importlib.import_module("vggt_omega.utils.pose_enc")
    return (
        getattr(models_mod, "VGGTOmega"),
        getattr(load_mod, "load_and_preprocess_images"),
        getattr(pose_mod, "encoding_to_camera"),
    )


def _failure_payload(args: argparse.Namespace, reason: str) -> Dict[str, Any]:
    return {
        "adapter": "vggt_omega",
        "backend": "error",
        "failure_flags": [reason],
        "fallback_contamination_count": 1,
        "repo": str(_as_path(args.repo)),
        "checkpoint": str(_as_path(args.checkpoint)),
        "image_list": str(_as_path(args.image_list)),
    }


@torch.inference_mode()
def run_smoke(args: argparse.Namespace) -> Dict[str, Any]:
    repo = _as_path(args.repo)
    checkpoint = _as_path(args.checkpoint)
    image_list = _as_path(args.image_list)
    output = Path(args.output)
    pt_output = Path(args.pt_output) if args.pt_output else output.with_suffix(".pt")

    try:
        image_names = _read_image_list(image_list)
        missing_paths = []
        if not repo.exists():
            missing_paths.append(f"repo not found: {repo}")
        if not checkpoint.exists():
            missing_paths.append(f"checkpoint not found: {checkpoint}")
        if missing_paths:
            raise FileNotFoundError("VGGT-Omega preflight failed; " + "; ".join(missing_paths))
        VGGTOmega, load_and_preprocess_images, encoding_to_camera = _load_upstream(repo)

        device = torch.device(
            "cuda" if args.device == "auto" and torch.cuda.is_available()
            else "cpu" if args.device == "auto"
            else args.device
        )
        if device.type == "cuda":
            torch.cuda.reset_peak_memory_stats(device)

        start = time.perf_counter()
        model_kwargs = {"enable_alignment": True} if args.enable_alignment else {}
        model = VGGTOmega(**model_kwargs).to(device).eval()
        state = torch.load(checkpoint, map_location="cpu")
        model.load_state_dict(state)

        images = load_and_preprocess_images(
            image_names,
            image_resolution=args.image_resolution,
            mode=args.resize_mode,
        ).to(device)
        predictions = model(images)
        missing = [key for key in REQUIRED_KEYS if key not in predictions]
        if missing:
            raise KeyError(f"VGGT-Omega predictions missing required keys: {missing}")

        extrinsics, intrinsics = encoding_to_camera(
            predictions["pose_enc"],
            predictions["images"].shape[-2:],
        )
        depth = _normalize_depth(predictions["depth"])
        depth_conf = predictions["depth_conf"]
        pointmap = depth_to_camera_pointmap(depth, intrinsics)
        confidence = _flatten_confidence(depth_conf, int(pointmap.shape[0]))
        camera_and_register_tokens = predictions["camera_and_register_tokens"]
        camera_tokens = camera_and_register_tokens[:, :, :1]
        registers = camera_and_register_tokens[:, :, 1:]

        runtime_ms = (time.perf_counter() - start) * 1000.0
        vram_mb = None
        if device.type == "cuda":
            vram_mb = torch.cuda.max_memory_allocated(device) / (1024.0 * 1024.0)

        payload = {
            "expert_name": "vggt_omega",
            "backend": "real",
            "version": "VGGT-Omega-1B",
            "pointmap": pointmap.detach().cpu(),
            "confidence": confidence.detach().cpu(),
            "optional_depth": depth.detach().cpu(),
            "optional_camera": {
                "extrinsics": _tensor_to_cpu(extrinsics),
                "intrinsics": _tensor_to_cpu(intrinsics),
            },
            "optional_tracks": None,
            "optional_dynamic_mask": None,
            "method_state": {
                "camera_tokens": _tensor_to_cpu(camera_tokens),
                "registers": _tensor_to_cpu(registers),
            },
            "runtime_ms": runtime_ms,
            "vram_mb": vram_mb,
            "failure_flags": [],
        }
        pt_output.parent.mkdir(parents=True, exist_ok=True)
        torch.save(payload, pt_output)

        result = {
            "adapter": "vggt_omega",
            "backend": "real",
            "fallback_contamination_count": 0,
            "failure_flags": [],
            "repo": str(repo),
            "checkpoint": str(checkpoint),
            "image_names": image_names,
            "image_resolution": args.image_resolution,
            "resize_mode": args.resize_mode,
            "device": str(device),
            "runtime_ms": runtime_ms,
            "vram_mb": vram_mb,
            "prediction_keys": sorted(predictions.keys()),
            "images_shape": _shape(predictions.get("images")),
            "depth_shape": _shape(depth),
            "depth_conf_shape": _shape(depth_conf),
            "pose_enc_shape": _shape(predictions["pose_enc"]),
            "extrinsics_shape": _shape(extrinsics),
            "intrinsics_shape": _shape(intrinsics),
            "camera_and_register_tokens_shape": _shape(camera_and_register_tokens),
            "pointmap_shape": list(pointmap.shape),
            "confidence_shape": list(confidence.shape),
            "pt_output": str(pt_output),
        }
        _write_json(output, result)
        print(json.dumps(result, indent=2, sort_keys=True), flush=True)
        return result
    except Exception as exc:
        result = _failure_payload(args, f"{type(exc).__name__}: {exc}")
        _write_json(output, result)
        print(json.dumps(result, indent=2, sort_keys=True), flush=True)
        raise


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--image-list", required=True)
    parser.add_argument("--image-resolution", type=int, default=512)
    parser.add_argument("--resize-mode", default="balanced")
    parser.add_argument("--enable-alignment", action="store_true")
    parser.add_argument("--output", required=True)
    parser.add_argument("--pt-output", default="")
    parser.add_argument("--device", default="auto")
    args = parser.parse_args()
    run_smoke(args)


if __name__ == "__main__":
    main()
