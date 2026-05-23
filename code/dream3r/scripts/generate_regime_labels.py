"""Generate heuristic KITTI regime labels for Stage 3 router training."""

import argparse
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

from dream3r.composer_experts.method_profiles import REGIME_ORDER


def _resolve_rectified_root(root: str) -> Path:
    path = Path(root)
    nested = path / "kitti" / "rectified"
    return nested if nested.exists() else path


def _raw_oxts_dir(kitti_root: Path, sequence_name: str) -> Path:
    raw_name = sequence_name.rsplit("_", 1)[0]
    date = "_".join(raw_name.split("_")[:3])
    return kitti_root / date / raw_name / "oxts" / "data"


def _sequence_stems(seq_dir: Path) -> List[str]:
    return sorted(
        path.stem for path in seq_dir.glob("*.jpg")
        if (seq_dir / f"{path.stem}.npy").exists()
    )


def _sample_indices(n_items: int, n_samples: int) -> List[int]:
    if n_items <= 0:
        return []
    count = min(n_items, n_samples)
    return sorted(set(np.linspace(0, n_items - 1, count, dtype=np.int64).tolist()))


def _depth_features(seq_dir: Path, stems: List[str], n_samples: int) -> Dict[str, float]:
    means = []
    valid_ratios = []
    for idx in _sample_indices(len(stems), n_samples):
        depth = np.load(seq_dir / f"{stems[idx]}.npy").astype(np.float32)
        valid = np.isfinite(depth) & (depth > 0)
        valid_ratios.append(float(valid.mean()))
        means.append(float(depth[valid].mean()) if valid.any() else 0.0)
    if len(means) > 1:
        denom = max(float(np.mean(means)), 1e-6)
        temporal_change = float(np.mean(np.abs(np.diff(means))) / denom)
    else:
        temporal_change = 0.0
    return {
        "depth_mean": float(np.mean(means)) if means else 0.0,
        "valid_ratio": float(np.mean(valid_ratios)) if valid_ratios else 0.0,
        "depth_temporal_change": temporal_change,
    }


def _oxts_motion_features(kitti_root: Path, sequence_name: str,
                          stems: List[str], n_samples: int) -> Dict[str, float]:
    oxts_dir = _raw_oxts_dir(kitti_root, sequence_name)
    if not oxts_dir.exists():
        return {"oxts_available": 0.0, "mean_speed": 0.0, "speed_std": 0.0}
    speeds = []
    for idx in _sample_indices(len(stems), n_samples):
        path = oxts_dir / f"{stems[idx]}.txt"
        if not path.exists():
            continue
        values = np.loadtxt(path, dtype=np.float64)
        if values.size >= 11:
            vf, vl, vu = values[8], values[9], values[10]
            speeds.append(math.sqrt(vf * vf + vl * vl + vu * vu))
    return {
        "oxts_available": 1.0 if speeds else 0.0,
        "mean_speed": float(np.mean(speeds)) if speeds else 0.0,
        "speed_std": float(np.std(speeds)) if speeds else 0.0,
    }


def _softmax(scores: List[float]) -> List[float]:
    arr = np.asarray(scores, dtype=np.float64)
    arr = arr - arr.max()
    exp = np.exp(arr)
    probs = exp / exp.sum()
    return [round(float(x), 6) for x in probs]


def _score_regimes(features: Dict[str, float]) -> List[float]:
    frame_count = features["frame_count"]
    dense = min(1.0, max(0.0, (frame_count - 50.0) / 70.0))
    feed_forward = min(1.0, max(0.0, (frame_count - 70.0) / 90.0))
    sparse = 1.0 - min(1.0, frame_count / 80.0)
    dynamic = min(
        1.0,
        0.6 * min(1.0, features["depth_temporal_change"] * 8.0)
        + 0.4 * min(1.0, features["speed_std"] / 4.0),
    )
    outdoor = 0.85 - 0.15 * dynamic
    indoor = 0.02
    scores = {
        "indoor_static": indoor,
        "outdoor_static": outdoor,
        "dynamic_scene": 0.1 + 0.9 * dynamic,
        "sparse_view": 0.1 + 0.9 * sparse,
        "dense_sequential": 0.1 + 0.9 * dense,
        "feed_forward_manyview": 0.1 + 0.9 * feed_forward,
    }
    return _softmax([scores[name] for name in REGIME_ORDER])


def label_sequence(kitti_root: Path, seq_dir: Path,
                   sample_frames: int = 5) -> Tuple[List[float], Dict[str, float]]:
    stems = _sequence_stems(seq_dir)
    features = {
        "frame_count": float(len(stems)),
        **_depth_features(seq_dir, stems, sample_frames),
        **_oxts_motion_features(kitti_root, seq_dir.name, stems, sample_frames),
    }
    return _score_regimes(features), features


def generate_regime_labels(
    root: str = "/hdd3/kykt26/data",
    output: str = "/hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json",
    sample_frames: int = 5,
    max_sequences: int = 0,
) -> Dict[str, object]:
    rectified_root = _resolve_rectified_root(root)
    kitti_root = rectified_root.parent
    sequence_dirs = sorted(path for path in rectified_root.iterdir() if path.is_dir())
    if max_sequences > 0:
        sequence_dirs = sequence_dirs[:max_sequences]

    labels = {}
    features = {}
    sanity = []
    skipped_empty = []
    for seq_dir in sequence_dirs:
        probs, feats = label_sequence(kitti_root, seq_dir, sample_frames=sample_frames)
        if feats["frame_count"] <= 0:
            skipped_empty.append(seq_dir.name)
            continue
        labels[seq_dir.name] = probs
        features[seq_dir.name] = feats
        top_idx = int(np.argmax(probs))
        if len(sanity) < 10:
            sanity.append({
                "sequence": seq_dir.name,
                "top_regime": REGIME_ORDER[top_idx],
                "probability": probs[top_idx],
                "frame_count": int(feats["frame_count"]),
                "depth_temporal_change": round(feats["depth_temporal_change"], 6),
                "mean_speed": round(feats["mean_speed"], 6),
                "speed_std": round(feats["speed_std"], 6),
            })

    result = {
        "regime_order": REGIME_ORDER,
        "label_source": "heuristic_kitti_rectified_depth_oxts_v1",
        "labels": labels,
        "features": features,
        "sanity": sanity,
        "skipped_empty": skipped_empty,
    }
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/hdd3/kykt26/data")
    parser.add_argument("--output", default="/hdd3/kykt26/code/dream3r/runs/stage3_regime_labels/regime_labels.json")
    parser.add_argument("--sample-frames", type=int, default=5)
    parser.add_argument("--max-sequences", type=int, default=0)
    args = parser.parse_args()

    result = generate_regime_labels(
        root=args.root,
        output=args.output,
        sample_frames=args.sample_frames,
        max_sequences=args.max_sequences,
    )
    print(json.dumps({
        "n_sequences": len(result["labels"]),
        "regime_order": result["regime_order"],
        "sanity": result["sanity"],
        "output": args.output,
    }, indent=2))


if __name__ == "__main__":
    main()
