"""Stage 1 real KITTI pair smoke: DINOv3 Perceiver + MASt3R pointmap."""

import argparse
import json
from pathlib import Path
from typing import Tuple

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

from dream3r.composer_experts.mast3r_adapter import MASt3RAdapter
from dream3r.data.kitti_pair import KITTIPairDataset, _resolve_rectified_root
from dream3r.model import CONFIGS, Dream3R


def _sequence_name(root: str, requested: str) -> str:
    rectified = _resolve_rectified_root(root)
    sequence_dirs = sorted(path for path in rectified.iterdir() if path.is_dir())
    if not sequence_dirs:
        raise RuntimeError(f"no KITTI sequences found under {rectified}")
    names = [path.name for path in sequence_dirs]
    if requested in names:
        return requested
    if requested.isdigit():
        index = int(requested)
        if index < len(names):
            return names[index]
    raise ValueError(f"sequence {requested!r} not found under {rectified}")


def _parse_pair(pair: str) -> Tuple[int, int]:
    left, right = pair.split(",", 1)
    return int(left), int(right)


def _depth_abs_rel(pred: torch.Tensor, target: torch.Tensor, mask: torch.Tensor) -> float:
    valid = mask & torch.isfinite(pred) & torch.isfinite(target) & (target > 0)
    if not valid.any():
        raise RuntimeError("no valid depth pixels for abs-rel")
    rel = (pred[valid] - target[valid]).abs() / target[valid].clamp_min(1e-6)
    return float(rel.mean().item())


def _save_depth_png(depth: torch.Tensor, path: Path) -> None:
    depth_np = depth.detach().float().cpu().numpy()
    finite = np.isfinite(depth_np) & (depth_np > 0)
    if finite.any():
        lo, hi = np.percentile(depth_np[finite], [2, 98])
        depth_np = np.clip((depth_np - lo) / max(hi - lo, 1e-6), 0.0, 1.0)
    else:
        depth_np = np.zeros_like(depth_np)
    image = (depth_np * 255.0).astype(np.uint8)
    Image.fromarray(image).resize((224, 224), Image.Resampling.NEAREST).save(path)


@torch.no_grad()
def run_smoke(args: argparse.Namespace) -> dict:
    device = torch.device(
        "cuda" if args.device == "auto" and torch.cuda.is_available()
        else "cpu" if args.device == "auto"
        else args.device
    )
    sequence = _sequence_name(args.kitti_root, args.kitti_seq)
    frame_a, frame_b = _parse_pair(args.pair)
    gap = max(1, frame_b - frame_a)
    dataset = KITTIPairDataset(args.kitti_root, sequence=sequence, frame_gaps=(gap,))
    sample = dataset[frame_a]

    images = sample["images"].unsqueeze(0).to(device)
    perceiver_images = F.interpolate(
        images.view(-1, *images.shape[2:]),
        size=(args.image_size, args.image_size),
        mode="bilinear",
        align_corners=False,
    ).view(1, 2, 3, args.image_size, args.image_size)
    mast3r_images = F.interpolate(
        images.view(-1, *images.shape[2:]),
        size=(args.mast3r_height, args.mast3r_width),
        mode="bilinear",
        align_corners=False,
    ).view(1, 2, 3, args.mast3r_height, args.mast3r_width)

    model = Dream3R(CONFIGS["small_real"]).to(device).eval()
    pipeline_out = model(perceiver_images, timestep=0)

    adapter = MASt3RAdapter(
        repo_path=args.mast3r_repo,
        checkpoint_path=args.mast3r_checkpoint,
    )
    adapter.load_checkpoint()
    expert_out = adapter.forward(mast3r_images)

    patch_grid = int(round(expert_out.pointmap.shape[2] ** 0.5))
    pred_depth = expert_out.pointmap[0, :, :, 2].view(2, patch_grid, patch_grid)
    gt_depth = F.interpolate(
        sample["depth_gt"].unsqueeze(1).float(),
        size=(patch_grid, patch_grid),
        mode="nearest",
    ).squeeze(1).to(device)
    valid_mask = F.interpolate(
        sample["valid_mask"].unsqueeze(1).float(),
        size=(patch_grid, patch_grid),
        mode="nearest",
    ).squeeze(1).bool().to(device)
    metric = _depth_abs_rel(pred_depth, gt_depth, valid_mask)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    depth_png = output_dir / "mast3r_depth_frame0.png"
    _save_depth_png(pred_depth[0], depth_png)

    result = {
        "sequence_name": sample["sequence_name"],
        "frame_ids": list(sample["frame_ids"]),
        "device": str(device),
        "perceiver_tokens": list(pipeline_out["frame_tokens"].shape),
        "mast3r_input_shape": list(mast3r_images.shape),
        "expert_backend": expert_out.metadata.get("backend"),
        "pointmap_shape": list(expert_out.pointmap.shape),
        "confidence_shape": list(expert_out.confidence.shape),
        "depth_abs_rel": metric,
        "depth_png": str(depth_png),
    }
    (output_dir / "metrics.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kitti-root", default="/hdd3/kykt26/data/kitti/rectified")
    parser.add_argument("--kitti_seq", default="00")
    parser.add_argument("--pair", default="0,1")
    parser.add_argument("--output", required=True)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--mast3r-height", type=int, default=160)
    parser.add_argument("--mast3r-width", type=int, default=512)
    parser.add_argument("--mast3r-repo", default="/hdd3/kykt26/code/mast3r")
    parser.add_argument("--mast3r-checkpoint", default="/hdd3/kykt26/checkpoints/mast3r-vitl")
    args = parser.parse_args()
    run_smoke(args)


if __name__ == "__main__":
    main()
