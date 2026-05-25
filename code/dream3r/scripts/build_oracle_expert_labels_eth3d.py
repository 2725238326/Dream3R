"""Build oracle expert labels on ETH3D Low-res many-view (cross-dataset eval).

Mirrors `build_oracle_expert_labels.py` but uses ETH3D windows instead of KITTI
long-windows. Sequence list comes from the ETH3D regime labels JSON so the
oracle and router-input share the same window set.
"""

import argparse
import gc
import json
from collections import Counter
from pathlib import Path
from typing import Dict, List, Optional

import torch

from dream3r.composer_experts.fast3r_adapter import Fast3RAdapter
from dream3r.composer_experts.mast3r_adapter import MASt3RAdapter
from dream3r.composer_experts.spann3r_adapter import Spann3RAdapter
from dream3r.data.eth3d_long import ETH3DLongSequenceDataset, SCENES
from dream3r.scripts.build_oracle_expert_labels import (
    _pointmap_abs_rel,
    _resize_images,
)


DEFAULT_EXPERT_ORDER = ["fast3r", "mast3r", "spann3r"]
EXPERT_CLASSES = {
    "fast3r": Fast3RAdapter,
    "mast3r": MASt3RAdapter,
    "spann3r": Spann3RAdapter,
}


def _normalize_expert_order(expert_order: Optional[List[str]] = None) -> List[str]:
    order = list(expert_order or DEFAULT_EXPERT_ORDER)
    unknown = [name for name in order if name not in EXPERT_CLASSES]
    if unknown:
        raise ValueError(f"unsupported experts: {unknown}")
    if len(set(order)) != len(order):
        raise ValueError(f"duplicate expert in order: {order}")
    return order


def _load_adapter(name: str):
    adapter = EXPERT_CLASSES[name]()
    adapter.load_checkpoint()
    if not adapter.is_loaded:
        raise RuntimeError(f"{name} did not load a real checkpoint")
    return adapter


def _build_dataset(root: str, sequence_length: int, image_size: int,
                   n_patches: int, max_windows_per_scene: int,
                   scenes: Optional[List[str]]) -> ETH3DLongSequenceDataset:
    return ETH3DLongSequenceDataset(
        root=root,
        sequence_length=sequence_length,
        max_windows_per_scene=max_windows_per_scene,
        image_size=image_size,
        n_patches=n_patches,
        scenes=scenes or SCENES,
    )


def _evaluate_expert(name: str, dataset: ETH3DLongSequenceDataset,
                     sequences: List[str], sample_index: Dict[str, int],
                     image_size: int, align_scale: bool,
                     device: torch.device) -> Dict[str, float]:
    adapter = _load_adapter(name)
    metrics: Dict[str, float] = {}
    for seq in sequences:
        idx = sample_index.get(seq)
        if idx is None:
            metrics[seq] = float("inf")
            continue
        sample = dataset[idx]
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


def build_oracle_expert_labels_eth3d(
    root: str,
    regime_labels: str,
    output: str,
    expert_order: Optional[List[str]] = None,
    sequence_length: int = 4,
    max_windows_per_scene: int = 10,
    image_size: int = 224,
    n_patches: int = 196,
    align_scale: bool = True,
    scenes: Optional[List[str]] = None,
) -> Dict[str, object]:
    expert_order = _normalize_expert_order(expert_order)
    regime_data = json.loads(Path(regime_labels).read_text(encoding="utf-8"))
    regime_sequences = list(regime_data["labels"].keys())

    rl_scenes = list(scenes or regime_data.get("scenes") or SCENES)
    rl_seq_len = int(regime_data.get("sequence_length", sequence_length))
    rl_img_size = int(regime_data.get("image_size", image_size))
    rl_n_patches = int(regime_data.get("n_patches", n_patches))
    rl_max_per_scene = int(regime_data.get(
        "max_windows_per_scene", max_windows_per_scene,
    ))
    dataset = _build_dataset(
        root=root,
        sequence_length=rl_seq_len,
        image_size=rl_img_size,
        n_patches=rl_n_patches,
        max_windows_per_scene=rl_max_per_scene,
        scenes=rl_scenes,
    )
    sample_index = {
        sample["sequence_name"]: idx
        for idx, sample in enumerate(dataset.samples)
    }
    sequences = [seq for seq in regime_sequences if seq in sample_index]
    missing = [seq for seq in regime_sequences if seq not in sample_index]
    if missing:
        raise ValueError(
            f"{len(missing)} regime sequences missing from dataset; "
            f"first={missing[:3]}"
        )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    metric_by_expert = {
        name: _evaluate_expert(
            name, dataset, sequences, sample_index,
            rl_img_size, align_scale, device,
        )
        for name in expert_order
    }

    labels: Dict[str, int] = {}
    oracle_expert: Dict[str, str] = {}
    metrics: Dict[str, Dict[str, float]] = {}
    for seq in sequences:
        seq_metrics = {name: metric_by_expert[name][seq] for name in expert_order}
        best_name = min(expert_order, key=lambda name: seq_metrics[name])
        labels[seq] = expert_order.index(best_name)
        oracle_expert[seq] = best_name
        metrics[seq] = seq_metrics

    counts = Counter(oracle_expert.values())
    regime_order = regime_data.get("regime_order", [])
    scene_regime_mapping = regime_data.get("scene_regime_mapping", {})

    def _seq_to_scene(seq: str) -> str:
        return seq.split("__", 1)[0] if "__" in seq else ""

    regime_top: Dict[str, str] = {}
    for seq in sequences:
        scene = _seq_to_scene(seq)
        regime_top[seq] = scene_regime_mapping.get(scene, "")

    result = {
        "dataset": "eth3d_low_res_many_view",
        "expert_order": expert_order,
        "labels": labels,
        "oracle_expert": oracle_expert,
        "metrics": metrics,
        "regime_top": regime_top,
        "summary": {
            "n_sequences": len(labels),
            "oracle_counts": dict(counts),
            "sequence_length": rl_seq_len,
            "image_size": rl_img_size,
            "n_patches": rl_n_patches,
            "max_windows_per_scene": rl_max_per_scene,
            "scenes": rl_scenes,
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
        default="/hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_regime_labels/regime_labels.json",
    )
    parser.add_argument(
        "--output",
        default="/hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_oracle/oracle_expert_labels.json",
    )
    parser.add_argument("--sequence-length", type=int, default=4)
    parser.add_argument("--max-windows-per-scene", type=int, default=10)
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--n-patches", type=int, default=196)
    parser.add_argument("--align-scale", action="store_true")
    parser.add_argument("--scenes", nargs="+", default=None)
    parser.add_argument(
        "--experts", nargs="+", default=None,
        help="Expert order, e.g. --experts fast3r mast3r spann3r",
    )
    args = parser.parse_args()

    result = build_oracle_expert_labels_eth3d(
        root=args.root,
        regime_labels=args.regime_labels,
        output=args.output,
        expert_order=args.experts,
        sequence_length=args.sequence_length,
        max_windows_per_scene=args.max_windows_per_scene,
        image_size=args.image_size,
        n_patches=args.n_patches,
        align_scale=args.align_scale,
        scenes=args.scenes,
    )
    print(json.dumps({
        "summary": result["summary"],
        "regime_top_sample": dict(list(result["regime_top"].items())[:5]),
        "oracle_expert_sample": dict(list(result["oracle_expert"].items())[:5]),
        "output": args.output,
    }, indent=2))


if __name__ == "__main__":
    main()
