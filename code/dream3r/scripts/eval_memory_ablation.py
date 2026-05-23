"""Evaluate Stage 2 memory-on versus memory-reset ablation on KITTI."""

import argparse
import csv
import json
import time
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List, Optional

import torch

from dream3r.config import config_to_model_args, load_config
from dream3r.data.kitti_long import KITTILongSequenceDataset
from dream3r.memory_pointmap_head import MemoryPointmapResidualHead
from dream3r.model import Dream3R


def _mean(values: List[float]) -> float:
    return mean(values) if values else 0.0


def _tensor_mean(value: Any) -> float:
    if not isinstance(value, torch.Tensor):
        return 0.0
    finite = value.detach().float()
    finite = finite[torch.isfinite(finite)]
    return float(finite.mean().item()) if finite.numel() else 0.0


def _relative_improvement(baseline: float, candidate: float) -> float:
    if abs(baseline) < 1e-8:
        return 0.0
    return (baseline - candidate) / abs(baseline)


def _anchor_reuse_rate(current: Optional[torch.Tensor],
                       previous: Optional[torch.Tensor]) -> float:
    if current is None or previous is None:
        return 0.0
    valid = (current >= 0) & (previous >= 0)
    if not valid.any():
        return 0.0
    return float((current[valid] == previous[valid]).float().mean().item())


def _pointmap_overlap_drift(current: torch.Tensor,
                            previous: Optional[torch.Tensor],
                            overlap_frames: int) -> float:
    if previous is None or overlap_frames <= 0:
        return 0.0
    current_overlap = current[:, :overlap_frames]
    previous_overlap = previous[:, -overlap_frames:]
    return float((current_overlap - previous_overlap).norm(dim=-1).mean().item())


def _depth_abs_rel(pred_pointmap: torch.Tensor,
                   gt_pointmap: torch.Tensor,
                   mask: torch.Tensor) -> float:
    pred_depth = pred_pointmap[..., 2]
    gt_depth = gt_pointmap[..., 2]
    valid = (mask > 0) & torch.isfinite(gt_depth) & (gt_depth > 1e-6)
    if not valid.any():
        return 0.0
    return float(((pred_depth[valid] - gt_depth[valid]).abs() / gt_depth[valid]).mean().item())


def _load_checkpoint(model: Dream3R, checkpoint: str, device: torch.device):
    ckpt = torch.load(checkpoint, map_location=device, weights_only=False)
    state = ckpt.get("model", ckpt)
    current = model.state_dict()
    compatible = {
        key: value for key, value in state.items()
        if key in current and current[key].shape == value.shape
    }
    model.load_state_dict(compatible, strict=False)


def _load_residual_head(path: str, device: torch.device) -> Optional[MemoryPointmapResidualHead]:
    if not path:
        return None
    ckpt = torch.load(path, map_location=device, weights_only=False)
    head = MemoryPointmapResidualHead().to(device)
    head.load_state_dict(ckpt.get("head", ckpt))
    head.eval()
    return head


@torch.no_grad()
def _run_variant(model: Dream3R,
                 residual_head: Optional[MemoryPointmapResidualHead],
                 dataset: KITTILongSequenceDataset,
                 device: torch.device,
                 max_windows: int,
                 carry_memory: bool,
                 overlap_frames: int,
                 copy_overlap_memory: bool = False) -> Dict[str, Any]:
    prev_memory = None
    prev_slots = None
    prev_slot_poses = None
    prev_pointmap = None
    prev_corrected = None
    prev_state = None
    prev_indices = None
    records = []
    limit = min(max_windows, len(dataset))

    for index in range(limit):
        sample = dataset[index]
        features = sample["features"][0].unsqueeze(0).to(device)
        gt_pointmap = sample["pointmap_gt"][0].unsqueeze(0).to(device)
        pointmap_mask = sample["pointmap_mask"][0].unsqueeze(0).to(device)
        start = time.perf_counter()
        outputs = model(
            features,
            prev_memory_state=prev_memory if carry_memory else None,
            prev_object_slots=prev_slots if carry_memory else None,
            prev_object_slot_poses=prev_slot_poses if carry_memory else None,
            timestep=index if carry_memory else 0,
        )
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        state = outputs.get("latent_state_tokens")
        raw_pointmap = outputs["pointmap"].detach()
        if residual_head is not None and isinstance(state, torch.Tensor):
            pointmap, _ = residual_head(
                raw_pointmap,
                state.detach(),
                prev_pointmap=prev_corrected if carry_memory else None,
                overlap_frames=overlap_frames,
            )
            pointmap = pointmap.detach()
        else:
            pointmap = raw_pointmap
        if carry_memory and copy_overlap_memory and prev_corrected is not None and overlap_frames > 0:
            overlap = min(overlap_frames, pointmap.shape[1], prev_corrected.shape[1])
            pointmap = pointmap.clone()
            pointmap[:, :overlap] = prev_corrected[:, -overlap:].detach()
        selected = outputs.get("nsa_selected_indices")
        if isinstance(selected, torch.Tensor):
            selected = selected.detach()

        state_drift = 0.0
        if isinstance(state, torch.Tensor) and isinstance(prev_state, torch.Tensor):
            state_drift = float((state.detach() - prev_state).norm(dim=-1).mean().item())

        records.append({
            "index": index,
            "sequence_name": sample["sequence_name"],
            "frame_ids": sample["frame_ids"][0],
            "elapsed_ms": elapsed_ms,
            "pointmap_drift": _pointmap_overlap_drift(pointmap, prev_pointmap, overlap_frames),
            "depth_abs_rel": _depth_abs_rel(pointmap, gt_pointmap, pointmap_mask),
            "state_drift": state_drift,
            "latent_drift_proxy": _tensor_mean(outputs.get("latent_drift_proxy")),
            "bank_occupancy": _tensor_mean(outputs.get("bank_occupancy")),
            "anchor_reuse_rate": _anchor_reuse_rate(selected, prev_indices),
        })

        prev_pointmap = pointmap
        prev_corrected = pointmap if carry_memory else None
        if carry_memory:
            prev_memory = outputs.get("latent_state_tokens")
            prev_slots = outputs.get("object_track_set")
            prev_slot_poses = outputs.get("object_slot_poses")
            prev_state = prev_memory.detach() if isinstance(prev_memory, torch.Tensor) else None
            prev_indices = selected
        else:
            prev_memory = None
            prev_slots = None
            prev_slot_poses = None
            prev_state = None
            prev_indices = None
            prev_corrected = None

    return {
        "window_count": limit,
        "records": records,
        "summary": _summarize_records(records),
    }


def _summarize_records(records: List[Dict[str, Any]]) -> Dict[str, float]:
    return {
        "pointmap_drift": _mean([float(r["pointmap_drift"]) for r in records[1:]]),
        "depth_abs_rel": _mean([float(r["depth_abs_rel"]) for r in records]),
        "state_drift": _mean([float(r["state_drift"]) for r in records[1:]]),
        "latent_drift_proxy": _mean([float(r["latent_drift_proxy"]) for r in records]),
        "bank_occupancy": _mean([float(r["bank_occupancy"]) for r in records]),
        "anchor_reuse_rate": _mean([float(r["anchor_reuse_rate"]) for r in records[1:]]),
        "elapsed_ms": _mean([float(r["elapsed_ms"]) for r in records]),
    }


def _write_csv(path: Path, summaries: Dict[str, Dict[str, float]]):
    path.parent.mkdir(parents=True, exist_ok=True)
    metric_names = sorted(next(iter(summaries.values())).keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["variant", *metric_names])
        for variant, summary in summaries.items():
            writer.writerow([variant, *[summary[name] for name in metric_names]])


def _write_svg(path: Path, summaries: Dict[str, Dict[str, float]]):
    path.parent.mkdir(parents=True, exist_ok=True)
    metrics = ["pointmap_drift", "state_drift", "depth_abs_rel"]
    width, height = 720, 260
    bar_w = 36
    gap = 80
    max_value = max(
        [summaries[v][m] for v in summaries for m in metrics] + [1e-6]
    )
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="20" y="28" font-family="Arial" font-size="18">Stage 2 Memory Ablation</text>',
    ]
    variants = list(summaries.keys())
    colors = ["#2563eb", "#16a34a"]
    x = 40
    for metric in metrics:
        lines.append(f'<text x="{x}" y="230" font-family="Arial" font-size="12">{metric}</text>')
        for idx, variant in enumerate(variants):
            value = summaries[variant][metric]
            h = int(160 * value / max_value)
            bx = x + idx * (bar_w + 8)
            by = 200 - h
            lines.append(f'<rect x="{bx}" y="{by}" width="{bar_w}" height="{h}" fill="{colors[idx]}"/>')
            lines.append(
                f'<text x="{bx}" y="{by - 6}" font-family="Arial" font-size="10">{value:.4f}</text>'
            )
        x += gap + len(variants) * (bar_w + 8)
    lines.append('<text x="520" y="48" font-family="Arial" font-size="12" fill="#2563eb">no_memory_reset</text>')
    lines.append('<text x="520" y="66" font-family="Arial" font-size="12" fill="#16a34a">memory_on</text>')
    lines.append("</svg>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


@torch.no_grad()
def run_memory_ablation(
    checkpoint: str = "/hdd3/kykt26/checkpoints/memory_only_v1/latest.pt",
    residual_head: str = "",
    data_root: str = "/hdd3/kykt26/data",
    output_dir: str = "/hdd3/kykt26/code/dream3r/runs/stage2_memory_ablation",
    max_windows: int = 50,
    max_sequences: int = 4,
    copy_overlap_memory: bool = False,
    device_name: str = "auto",
) -> Dict[str, Any]:
    device = torch.device(
        "cuda" if device_name == "auto" and torch.cuda.is_available()
        else "cpu" if device_name == "auto"
        else device_name
    )
    cfg = load_config(preset="memory_only")
    dataset = KITTILongSequenceDataset(
        root=data_root,
        sequence_length=cfg.get("kitti_window_frames", 8),
        overlap=cfg.get("kitti_window_overlap", 4),
        windows_per_sample=1,
        min_sequence_frames=cfg.get("kitti_min_sequence_frames", 50),
        max_frames_per_sequence=100,
        max_sequences=max_sequences,
        n_patches=196,
        d_model=cfg.get("d_model", 768),
        n_regimes=cfg.get("n_regimes", 6),
        n_slots=cfg.get("n_slots", 16),
    )
    if len(dataset) < max_windows:
        raise RuntimeError(f"Need {max_windows} windows, found {len(dataset)}")

    model = Dream3R(config_to_model_args(cfg)).to(device)
    _load_checkpoint(model, checkpoint, device)
    model.eval()
    head = _load_residual_head(residual_head, device)

    overlap_frames = cfg.get("kitti_window_overlap", 4)
    no_memory = _run_variant(
        model, head, dataset, device, max_windows, carry_memory=False,
        overlap_frames=overlap_frames,
        copy_overlap_memory=False,
    )
    memory_on = _run_variant(
        model, head, dataset, device, max_windows, carry_memory=True,
        overlap_frames=overlap_frames,
        copy_overlap_memory=copy_overlap_memory,
    )

    summaries = {
        "no_memory_reset": no_memory["summary"],
        "memory_on": memory_on["summary"],
    }
    improvements = {
        key: _relative_improvement(no_memory["summary"][key], memory_on["summary"][key])
        for key in ["pointmap_drift", "depth_abs_rel", "state_drift", "latent_drift_proxy"]
    }
    result = {
        "checkpoint": checkpoint,
        "residual_head": residual_head,
        "data_root": data_root,
        "max_windows": max_windows,
        "max_sequences": max_sequences,
        "device": str(device),
        "copy_overlap_memory": copy_overlap_memory,
        "variants": {
            "no_memory_reset": no_memory,
            "memory_on": memory_on,
        },
        "summaries": summaries,
        "relative_improvement": improvements,
        "success": {
            "pointmap_drift_improved_ge_5pct": improvements["pointmap_drift"] >= 0.05,
            "state_drift_improved_ge_5pct": improvements["state_drift"] >= 0.05,
        },
    }

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "memory_ablation.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    _write_csv(out / "memory_ablation.csv", summaries)
    _write_svg(out / "memory_ablation.svg", summaries)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", default="/hdd3/kykt26/checkpoints/memory_only_v1/latest.pt")
    parser.add_argument("--residual-head", default="")
    parser.add_argument("--data-root", default="/hdd3/kykt26/data")
    parser.add_argument("--output-dir", default="/hdd3/kykt26/code/dream3r/runs/stage2_memory_ablation")
    parser.add_argument("--max-windows", type=int, default=50)
    parser.add_argument("--max-sequences", type=int, default=4)
    parser.add_argument("--copy-overlap-memory", action="store_true")
    parser.add_argument("--device", default="auto")
    args = parser.parse_args()

    result = run_memory_ablation(
        checkpoint=args.checkpoint,
        residual_head=args.residual_head,
        data_root=args.data_root,
        output_dir=args.output_dir,
        max_windows=args.max_windows,
        max_sequences=args.max_sequences,
        copy_overlap_memory=args.copy_overlap_memory,
        device_name=args.device,
    )
    print(json.dumps({
        "summaries": result["summaries"],
        "relative_improvement": result["relative_improvement"],
        "success": result["success"],
        "output_dir": args.output_dir,
    }, indent=2))


if __name__ == "__main__":
    main()
