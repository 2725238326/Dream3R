"""Build image-window manifests for VLM semantic labeling.

The manifest is the bridge between existing Dream3R cache windows and the
offline VLM labeler. It stores only identifiers and image paths; it does not
run geometry models, build pointmaps, or touch frozen core modules.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from dream3r.data.eth3d_long import ETH3DLongSequenceDataset, SCENES
from dream3r.data.kitti_long import KITTILongSequenceDataset


def _load_regime_sequences(regime_labels: str) -> List[str]:
    data = json.loads(Path(regime_labels).read_text(encoding="utf-8"))
    labels = data.get("labels")
    if not isinstance(labels, dict):
        raise ValueError("regime labels must contain a labels object")
    return sorted(str(key) for key in labels)


def _resolve_kitti_roots(root: str) -> tuple[Path, Path]:
    path = Path(root)
    nested = path / "kitti" / "rectified"
    rectified_root = nested if nested.exists() else path
    kitti_root = rectified_root.parent
    return rectified_root, kitti_root


def build_kitti_manifest(
    root: str,
    regime_labels: str,
    output: str,
    window_frames: int = 4,
    max_windows: int = 0,
    max_frames_per_sequence: int = 32,
    window_id_mode: str = "prefixed",
) -> Dict[str, Any]:
    rectified_root, _ = _resolve_kitti_roots(root)
    windows: List[Dict[str, Any]] = []
    for seq in _load_regime_sequences(regime_labels):
        if max_windows > 0 and len(windows) >= max_windows:
            break
        ds = KITTILongSequenceDataset(
            root=root,
            sequence=seq,
            sequence_length=window_frames,
            overlap=max(0, window_frames - 1),
            windows_per_sample=1,
            min_sequence_frames=window_frames,
            max_frames_per_sequence=max_frames_per_sequence,
            max_sequences=0,
            n_patches=196,
            d_model=8,
        )
        if len(ds) == 0:
            continue
        _, stems = ds.samples[0]
        frame_stems = stems[:window_frames]
        seq_dir = rectified_root / seq
        window_id = seq if window_id_mode == "sequence" else f"kitti/{seq}/{frame_stems[0]}"
        windows.append({
            "window_id": window_id,
            "dataset": "kitti",
            "sequence": seq,
            "frame_ids": list(frame_stems),
            "frames": [str(seq_dir / f"{stem}.jpg") for stem in frame_stems],
        })
    return _write_manifest(output, windows, "kitti", root, regime_labels)


def build_eth3d_manifest(
    root: str,
    regime_labels: str,
    output: str,
    window_frames: int = 4,
    max_windows: int = 0,
    window_id_mode: str = "prefixed",
) -> Dict[str, Any]:
    regime_data = json.loads(Path(regime_labels).read_text(encoding="utf-8"))
    regime_sequences = [str(key) for key in regime_data.get("labels", {})]
    scenes = list(regime_data.get("scenes") or SCENES)
    sequence_length = int(regime_data.get("sequence_length", window_frames))
    image_size = int(regime_data.get("image_size", 224))
    n_patches = int(regime_data.get("n_patches", 196))
    max_per_scene = int(regime_data.get("max_windows_per_scene", 10))
    dataset = ETH3DLongSequenceDataset(
        root=root,
        sequence_length=sequence_length,
        max_windows_per_scene=max_per_scene,
        image_size=image_size,
        n_patches=n_patches,
        scenes=scenes,
        dense_gt=True,
    )
    sample_index = {str(sample["sequence_name"]): sample for sample in dataset.samples}
    windows: List[Dict[str, Any]] = []
    for seq in regime_sequences:
        if max_windows > 0 and len(windows) >= max_windows:
            break
        sample = sample_index.get(seq)
        if sample is None:
            continue
        scene_name = str(sample["scene_name"])
        scene_dir = dataset.root / scene_name
        image_infos = list(sample["images"])[:window_frames]
        frames = [str(scene_dir / "images" / str(info["name"])) for info in image_infos]
        window_id = seq if window_id_mode == "sequence" else f"eth3d/{seq}"
        windows.append({
            "window_id": window_id,
            "dataset": "eth3d",
            "sequence": seq,
            "scene": scene_name,
            "frame_ids": [str(info["name"]) for info in image_infos],
            "frames": frames,
        })
    return _write_manifest(output, windows, "eth3d", root, regime_labels)


def _write_manifest(
    output: str,
    windows: List[Dict[str, Any]],
    dataset: str,
    root: str,
    regime_labels: Optional[str],
) -> Dict[str, Any]:
    result = {
        "schema_version": "dream3r_vlm_window_manifest_v1",
        "dataset": dataset,
        "root": root,
        "regime_labels": regime_labels,
        "n_windows": len(windows),
        "windows": windows,
    }
    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def build_vlm_window_manifest(
    dataset: str,
    root: str,
    output: str,
    regime_labels: str,
    window_frames: int = 4,
    max_windows: int = 0,
    window_id_mode: str = "prefixed",
) -> Dict[str, Any]:
    if window_id_mode not in {"prefixed", "sequence"}:
        raise ValueError(f"unsupported window_id_mode: {window_id_mode}")
    if dataset == "kitti_long":
        return build_kitti_manifest(
            root=root,
            regime_labels=regime_labels,
            output=output,
            window_frames=window_frames,
            max_windows=max_windows,
            window_id_mode=window_id_mode,
        )
    if dataset == "eth3d_long":
        return build_eth3d_manifest(
            root=root,
            regime_labels=regime_labels,
            output=output,
            window_frames=window_frames,
            max_windows=max_windows,
            window_id_mode=window_id_mode,
        )
    raise ValueError(f"unsupported dataset: {dataset}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["kitti_long", "eth3d_long"], required=True)
    parser.add_argument("--root", default="/hdd3/kykt26/data")
    parser.add_argument("--regime-labels", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--window-frames", type=int, default=4)
    parser.add_argument("--max-windows", type=int, default=0)
    parser.add_argument("--window-id-mode", choices=["prefixed", "sequence"], default="prefixed")
    args = parser.parse_args()

    result = build_vlm_window_manifest(
        dataset=args.dataset,
        root=args.root,
        output=args.output,
        regime_labels=args.regime_labels,
        window_frames=args.window_frames,
        max_windows=args.max_windows,
        window_id_mode=args.window_id_mode,
    )
    print(json.dumps({
        "schema_version": result["schema_version"],
        "dataset": result["dataset"],
        "n_windows": result["n_windows"],
        "output": args.output,
    }, indent=2))


if __name__ == "__main__":
    main()
