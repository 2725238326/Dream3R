"""Build oracle expert labels from real expert pointmap metrics."""

import argparse
import gc
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn.functional as F

from dream3r.composer_experts.fast3r_adapter import Fast3RAdapter
from dream3r.composer_experts.mast3r_adapter import MASt3RAdapter
from dream3r.composer_experts.spann3r_adapter import Spann3RAdapter
from dream3r.composer_experts.method_profiles import REGIME_ORDER
from dream3r.data.kitti_long import KITTILongSequenceDataset


DEFAULT_EXPERT_ORDER = ["fast3r", "mast3r"]
EXPERT_CLASSES = {
    "fast3r": Fast3RAdapter,
    "mast3r": MASt3RAdapter,
    "spann3r": Spann3RAdapter,
}


def _top_regime(probs: List[float], order: List[str]) -> str:
    return order[max(range(len(probs)), key=lambda idx: probs[idx])]


def _select_sequences(regime_data: Dict[str, object], max_per_regime: int) -> List[str]:
    order = regime_data.get("regime_order", REGIME_ORDER)
    buckets: Dict[str, List[Tuple[float, str]]] = defaultdict(list)
    for seq, probs in regime_data["labels"].items():
        top = _top_regime(probs, order)
        buckets[top].append((float(max(probs)), seq))

    selected = []
    for regime in order:
        rows = sorted(buckets.get(regime, []), reverse=True)
        selected.extend(seq for _, seq in rows[:max_per_regime])
    return selected


def _resize_images(images: torch.Tensor, size: int) -> torch.Tensor:
    if images.shape[-2:] == (size, size):
        return images
    bsz, n_frames = images.shape[:2]
    resized = F.interpolate(
        images.reshape(bsz * n_frames, *images.shape[2:]),
        size=(size, size),
        mode="bilinear",
        align_corners=False,
    )
    return resized.reshape(bsz, n_frames, *resized.shape[1:])


def _pointmap_abs_rel(pred: torch.Tensor, target: torch.Tensor,
                      mask: torch.Tensor,
                      align_scale: bool = False) -> float:
    pred_depth = pred[..., 2].float()
    target_depth = target[..., 2].float()
    valid = (
        mask.bool()
        & torch.isfinite(pred_depth)
        & torch.isfinite(target_depth)
        & (target_depth.abs() > 1e-6)
    )
    if not bool(valid.any()):
        return float("inf")
    if align_scale:
        denom = pred_depth[valid].median()
        denom = torch.where(denom.abs() > 1e-6, denom, denom.new_tensor(1e-6))
        scale = target_depth[valid].median() / denom
        pred_depth = pred_depth * scale
    rel = (pred_depth - target_depth).abs() / target_depth.abs().clamp_min(1e-6)
    return float(rel[valid].mean().item())


def _normalize_expert_order(expert_order: Optional[List[str]] = None) -> List[str]:
    order = list(expert_order or DEFAULT_EXPERT_ORDER)
    unknown = [name for name in order if name not in EXPERT_CLASSES]
    if unknown:
        raise ValueError(f"unsupported experts: {unknown}")
    if len(set(order)) != len(order):
        raise ValueError(f"duplicate expert in order: {order}")
    return order


def _load_adapter(name: str):
    try:
        adapter = EXPERT_CLASSES[name]()
    except KeyError as exc:
        raise ValueError(f"unsupported expert: {name}") from exc
    adapter.load_checkpoint()
    if not adapter.is_loaded:
        raise RuntimeError(f"{name} did not load a real checkpoint")
    return adapter


def _sequence_sample(root: str, sequence: str, window_frames: int,
                     max_frames_per_sequence: int, n_patches: int):
    dataset = KITTILongSequenceDataset(
        root=root,
        sequence=sequence,
        sequence_length=window_frames,
        overlap=max(0, window_frames - 1),
        windows_per_sample=1,
        min_sequence_frames=window_frames,
        max_frames_per_sequence=max_frames_per_sequence,
        max_sequences=0,
        n_patches=n_patches,
        d_model=8,
    )
    if len(dataset) == 0:
        return None
    return dataset[0]


def _evaluate_expert(name: str, root: str, sequences: List[str],
                     window_frames: int, max_frames_per_sequence: int,
                     image_size: int, n_patches: int,
                     align_scale: bool,
                     device: torch.device) -> Dict[str, float]:
    adapter = _load_adapter(name)
    metrics: Dict[str, float] = {}
    for seq in sequences:
        sample = _sequence_sample(
            root, seq, window_frames, max_frames_per_sequence, n_patches,
        )
        if sample is None:
            metrics[seq] = float("inf")
            continue
        images = sample["images"][0].unsqueeze(0).to(device)
        images = _resize_images(images, image_size)
        target = sample["pointmap_gt"][0].unsqueeze(0).to(device)
        mask = sample["pointmap_mask"][0].unsqueeze(0).to(device)
        with torch.no_grad():
            out = adapter.forward(images)
        metrics[seq] = _pointmap_abs_rel(out.pointmap, target, mask, align_scale)

    del adapter
    gc.collect()
    if device.type == "cuda":
        torch.cuda.empty_cache()
    return metrics


def build_oracle_expert_labels(
    root: str,
    regime_labels: str,
    output: str,
    expert_order: Optional[List[str]] = None,
    max_per_regime: int = 3,
    window_frames: int = 4,
    max_frames_per_sequence: int = 32,
    image_size: int = 224,
    n_patches: int = 196,
    align_scale: bool = False,
) -> Dict[str, object]:
    expert_order = _normalize_expert_order(expert_order)
    regime_data = json.loads(Path(regime_labels).read_text(encoding="utf-8"))
    sequences = _select_sequences(regime_data, max_per_regime=max_per_regime)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    metric_by_expert = {
        name: _evaluate_expert(
            name, root, sequences, window_frames, max_frames_per_sequence,
            image_size, n_patches, align_scale, device,
        )
        for name in expert_order
    }

    labels = {}
    oracle_expert = {}
    metrics = {}
    for seq in sequences:
        seq_metrics = {name: metric_by_expert[name][seq] for name in expert_order}
        best_name = min(expert_order, key=lambda name: seq_metrics[name])
        labels[seq] = expert_order.index(best_name)
        oracle_expert[seq] = best_name
        metrics[seq] = seq_metrics

    counts = Counter(oracle_expert.values())
    result = {
        "expert_order": expert_order,
        "labels": labels,
        "oracle_expert": oracle_expert,
        "metrics": metrics,
        "regime_top": {
            seq: _top_regime(regime_data["labels"][seq], regime_data["regime_order"])
            for seq in labels
        },
        "summary": {
            "n_sequences": len(labels),
            "oracle_counts": dict(counts),
            "window_frames": window_frames,
            "image_size": image_size,
            "metric": "scale_aligned_abs_rel" if align_scale else "raw_abs_rel",
        },
    }
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/hdd3/kykt26/data")
    parser.add_argument(
        "--regime-labels",
        default="/hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json",
    )
    parser.add_argument(
        "--output",
        default="/hdd3/kykt26/code/dream3r/runs/stage3_oracle_labels/oracle_expert_labels.json",
    )
    parser.add_argument("--max-per-regime", type=int, default=3)
    parser.add_argument("--window-frames", type=int, default=4)
    parser.add_argument("--max-frames-per-sequence", type=int, default=32)
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--align-scale", action="store_true")
    parser.add_argument(
        "--experts",
        nargs="+",
        default=None,
        help="Expert order to evaluate, e.g. --experts fast3r mast3r spann3r",
    )
    args = parser.parse_args()

    result = build_oracle_expert_labels(
        root=args.root,
        regime_labels=args.regime_labels,
        output=args.output,
        expert_order=args.experts,
        max_per_regime=args.max_per_regime,
        window_frames=args.window_frames,
        max_frames_per_sequence=args.max_frames_per_sequence,
        image_size=args.image_size,
        align_scale=args.align_scale,
    )
    print(json.dumps({
        "summary": result["summary"],
        "regime_top": result["regime_top"],
        "oracle_expert": result["oracle_expert"],
        "output": args.output,
    }, indent=2))


if __name__ == "__main__":
    main()
