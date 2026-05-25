"""Generate hardcoded ETH3D regime labels + per-window stats for router input.

Mirrors `generate_regime_labels.py`'s output schema:
  - regime_order: 6 labels (same as KITTI)
  - labels[seq]: 6D probability vector (one-hot per scene per HANDOFF)
  - features[seq]: dict with STAT_FEATURE_KEYS values

Sequence names match those emitted by `ETH3DLongSequenceDataset`.
"""

import argparse
import json
from pathlib import Path
from typing import Dict, List

import numpy as np

from dream3r.composer_experts.method_profiles import REGIME_ORDER
from dream3r.data.eth3d_long import ETH3DLongSequenceDataset, SCENES


SCENE_REGIME = {
    "delivery_area": "indoor_static",
    "electro": "indoor_static",
    "forest": "outdoor_static",
    "playground": "outdoor_static",
    "terrains": "outdoor_static",
}


def _one_hot(regime_name: str) -> List[float]:
    probs = [0.0] * len(REGIME_ORDER)
    if regime_name in REGIME_ORDER:
        probs[REGIME_ORDER.index(regime_name)] = 1.0
    return probs


def _window_stats(sample: Dict[str, object]) -> Dict[str, float]:
    pointmap = sample["pointmap_gt"][0]   # [N, P, 3]
    mask = sample["pointmap_mask"][0]     # [N, P]
    depths_per_frame: List[float] = []
    valid_ratios: List[float] = []
    for i in range(pointmap.shape[0]):
        valid = mask[i].bool()
        if valid.any():
            depths_per_frame.append(float(pointmap[i][valid, 2].mean().item()))
            valid_ratios.append(float(valid.float().mean().item()))
        else:
            depths_per_frame.append(0.0)
            valid_ratios.append(0.0)
    depth_mean = float(np.mean(depths_per_frame)) if depths_per_frame else 0.0
    if len(depths_per_frame) > 1:
        denom = max(depth_mean, 1e-6)
        temporal_change = float(np.mean(np.abs(np.diff(depths_per_frame))) / denom)
    else:
        temporal_change = 0.0
    return {
        "frame_count": float(pointmap.shape[0]),
        "depth_mean": depth_mean,
        "valid_ratio": float(np.mean(valid_ratios)) if valid_ratios else 0.0,
        "depth_temporal_change": temporal_change,
        "oxts_available": 0.0,
        "mean_speed": 0.0,
        "speed_std": 0.0,
    }


def generate_eth3d_regime_labels(
    root: str,
    output: str,
    sequence_length: int = 4,
    max_windows_per_scene: int = 10,
    image_size: int = 224,
    n_patches: int = 196,
    scenes: List[str] = None,
) -> Dict[str, object]:
    dataset = ETH3DLongSequenceDataset(
        root=root,
        sequence_length=sequence_length,
        max_windows_per_scene=max_windows_per_scene,
        image_size=image_size,
        n_patches=n_patches,
        scenes=scenes or SCENES,
    )

    labels: Dict[str, List[float]] = {}
    features: Dict[str, Dict[str, float]] = {}
    sanity: List[Dict[str, object]] = []

    for idx in range(len(dataset)):
        sample = dataset[idx]
        seq = sample["sequence_name"]
        scene = sample["scene_name"]
        regime_name = SCENE_REGIME.get(scene, "outdoor_static")
        labels[seq] = _one_hot(regime_name)
        feats = _window_stats(sample)
        features[seq] = feats
        if len(sanity) < 10:
            sanity.append({
                "sequence": seq,
                "scene": scene,
                "top_regime": regime_name,
                "depth_mean": round(feats["depth_mean"], 4),
                "valid_ratio": round(feats["valid_ratio"], 4),
                "depth_temporal_change": round(feats["depth_temporal_change"], 6),
            })

    result = {
        "regime_order": REGIME_ORDER,
        "label_source": "eth3d_hardcoded_scene_one_hot_v1",
        "scene_regime_mapping": SCENE_REGIME,
        "labels": labels,
        "features": features,
        "sanity": sanity,
        "scenes": list(scenes or SCENES),
        "sequence_length": sequence_length,
        "image_size": image_size,
        "n_patches": n_patches,
        "max_windows_per_scene": max_windows_per_scene,
    }
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/hdd3/kykt26/data")
    parser.add_argument(
        "--output",
        default="/hdd3/kykt26/code/dream3r/runs/eth3d_cross_dataset_regime_labels/regime_labels.json",
    )
    parser.add_argument("--sequence-length", type=int, default=4)
    parser.add_argument("--max-windows-per-scene", type=int, default=10)
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--n-patches", type=int, default=196)
    parser.add_argument("--scenes", nargs="+", default=None)
    args = parser.parse_args()

    result = generate_eth3d_regime_labels(
        root=args.root,
        output=args.output,
        sequence_length=args.sequence_length,
        max_windows_per_scene=args.max_windows_per_scene,
        image_size=args.image_size,
        n_patches=args.n_patches,
        scenes=args.scenes,
    )
    print(json.dumps({
        "n_sequences": len(result["labels"]),
        "regime_order": result["regime_order"],
        "scene_regime_mapping": result["scene_regime_mapping"],
        "sanity": result["sanity"],
        "output": args.output,
    }, indent=2))


if __name__ == "__main__":
    main()
