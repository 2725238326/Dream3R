"""Evaluate VGGT-Omega as a proposal-bank admission candidate.

This script consumes existing SCF caches for the current real proposal bank
(Fast3R / MASt3R / Spann3R), runs VGGT-Omega on matching image windows, and
reports whether adding VGGT-Omega improves the per-window oracle ceiling.

It is an admission gate, not training. It never accepts fallback outputs.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import torch
import torch.nn.functional as F

from dream3r.data.eth3d_long import ETH3DLongSequenceDataset, SCENES
from dream3r.data.kitti_long import KITTILongSequenceDataset, _resolve_roots
from dream3r.scripts.build_oracle_expert_labels import _pointmap_abs_rel
from dream3r.scripts.smoke_vggt_omega_adapter import _load_upstream, _normalize_depth


DEFAULT_REPO = "/hdd3/kykt26/externals/vggt-omega"
DEFAULT_CHECKPOINT = "/hdd3/kykt26/checkpoints/vggt_omega/VGGT-Omega-1B-512/model.pt"


def _load_json(path: str) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _load_cache(path: str) -> Dict[str, Any]:
    return torch.load(path, map_location="cpu", weights_only=False)


def _select_entries(blob: Dict[str, Any], max_windows: int) -> List[Dict[str, Any]]:
    entries = list(blob["entries"])
    if max_windows > 0:
        entries = entries[:max_windows]
    return entries


def _kitti_image_paths(root: str, seq: str, window_frames: int) -> List[str]:
    rectified_root, _ = _resolve_roots(root)
    dataset = KITTILongSequenceDataset(
        root=root,
        sequence=seq,
        sequence_length=window_frames,
        overlap=max(0, window_frames - 1),
        windows_per_sample=1,
        min_sequence_frames=window_frames,
        max_frames_per_sequence=32,
        max_sequences=0,
        n_patches=196,
        d_model=8,
    )
    if len(dataset) == 0:
        raise ValueError(f"KITTI sequence has no matching window: {seq}")
    sample = dataset[0]
    stems = sample["frame_ids"][0]
    return [str(rectified_root / seq / f"{stem}.jpg") for stem in stems]


def _eth3d_dataset_from_regime(root: str, regime_labels: str, window_frames: int):
    regime_data = _load_json(regime_labels)
    scenes = list(regime_data.get("scenes") or SCENES)
    sequence_length = int(regime_data.get("sequence_length", window_frames))
    image_size = int(regime_data.get("image_size", 224))
    n_patches = int(regime_data.get("n_patches", 196))
    max_per_scene = int(regime_data.get("max_windows_per_scene", 10))
    return ETH3DLongSequenceDataset(
        root=root,
        sequence_length=sequence_length,
        max_windows_per_scene=max_per_scene,
        image_size=image_size,
        n_patches=n_patches,
        scenes=scenes,
        dense_gt=True,
    )


def _eth3d_image_paths(dataset: ETH3DLongSequenceDataset, seq: str) -> List[str]:
    sample_index = {s["sequence_name"]: idx for idx, s in enumerate(dataset.samples)}
    idx = sample_index.get(seq)
    if idx is None:
        raise ValueError(f"ETH3D sequence has no matching window: {seq}")
    meta = dataset.samples[idx]
    scene = dataset._scene_cache[meta["scene_name"]]
    scene_dir = Path(scene["scene_dir"])
    return [str(scene_dir / "images" / img["name"]) for img in meta["images"]]


def _dense_depth_to_patch_pointmap(depth: torch.Tensor, n_patches: int) -> torch.Tensor:
    depth = _normalize_depth(depth)
    grid = int(round(n_patches ** 0.5))
    if grid * grid != n_patches:
        raise ValueError(f"n_patches must be square, got {n_patches}")
    patch_depth = F.interpolate(
        depth.unsqueeze(1),
        size=(grid, grid),
        mode="bilinear",
        align_corners=False,
    ).squeeze(1).reshape(depth.shape[0], n_patches)
    pointmap = torch.zeros(depth.shape[0], n_patches, 3, dtype=patch_depth.dtype)
    pointmap[..., 2] = patch_depth
    return pointmap


def _dense_conf_to_patch_confidence(confidence: torch.Tensor, n_patches: int) -> torch.Tensor:
    conf = confidence.detach().float()
    if conf.ndim == 4 and conf.shape[0] == 1:
        conf = conf.squeeze(0)
    if conf.ndim == 5 and conf.shape[0] == 1:
        conf = conf.squeeze(0)
    if conf.ndim == 4 and conf.shape[-1] == 1:
        conf = conf.squeeze(-1)
    if conf.ndim != 3:
        raise ValueError(f"expected confidence shaped [N,H,W], got {tuple(conf.shape)}")
    grid = int(round(n_patches ** 0.5))
    if grid * grid != n_patches:
        raise ValueError(f"n_patches must be square, got {n_patches}")
    patch_conf = F.interpolate(
        conf.unsqueeze(1),
        size=(grid, grid),
        mode="bilinear",
        align_corners=False,
    ).squeeze(1).reshape(conf.shape[0], n_patches, 1)
    return patch_conf


def _expanded_entry(
    entry: Dict[str, Any],
    expert_order: List[str],
    vggt_pointmap: torch.Tensor,
    vggt_confidence: torch.Tensor,
) -> Dict[str, Any]:
    proposals = {
        name: {
            "pointmap": entry["proposals"][name]["pointmap"],
            "confidence": entry["proposals"][name]["confidence"],
        }
        for name in expert_order
    }
    proposals["vggt_omega"] = {
        "pointmap": vggt_pointmap.squeeze(0).detach().cpu(),
        "confidence": vggt_confidence.squeeze(0).detach().cpu(),
    }
    backends = dict(entry.get("expert_backends", {}))
    backends["vggt_omega"] = True
    return {
        "seq": entry["seq"],
        "domain": entry["domain"],
        "proposals": proposals,
        "expert_order": expert_order + ["vggt_omega"],
        "expert_backends": backends,
        "memory_context": entry.get("memory_context"),
        "conflict_score": float(entry.get("conflict_score", 0.0)),
        "composer_prior": entry.get("composer_prior"),
        "gt_pointmap": entry["gt_pointmap"],
        "gt_mask": entry["gt_mask"],
    }


def _summarize_rows(rows: List[Dict[str, Any]], expert_order: List[str]) -> Dict[str, Any]:
    if not rows:
        return {
            "n": 0,
            "expert_order": expert_order + ["vggt_omega"],
            "failure_flags": ["no_rows"],
        }
    old_oracle = sum(float(r["old_oracle"]) for r in rows) / len(rows)
    new_oracle = sum(float(r["new_oracle"]) for r in rows) / len(rows)
    vggt_mean = sum(float(r["metrics"]["vggt_omega"]) for r in rows) / len(rows)
    old_best_counts: Dict[str, int] = {}
    new_best_counts: Dict[str, int] = {}
    vggt_wins = 0
    for row in rows:
        old_best_counts[row["old_best_expert"]] = old_best_counts.get(row["old_best_expert"], 0) + 1
        new_best_counts[row["new_best_expert"]] = new_best_counts.get(row["new_best_expert"], 0) + 1
        if row["new_best_expert"] == "vggt_omega":
            vggt_wins += 1
    gain = old_oracle - new_oracle
    return {
        "n": len(rows),
        "expert_order": expert_order + ["vggt_omega"],
        "old_oracle_mean": old_oracle,
        "new_oracle_mean": new_oracle,
        "oracle_gain_abs_rel": gain,
        "oracle_gain_pct": gain / max(old_oracle, 1e-9) * 100.0,
        "vggt_omega_mean": vggt_mean,
        "vggt_omega_wins": vggt_wins,
        "old_best_counts": old_best_counts,
        "new_best_counts": new_best_counts,
    }


@torch.inference_mode()
def evaluate_vggt_omega_admission(
    kitti_cache: str,
    eth3d_cache: str,
    kitti_regime_labels: str,
    eth3d_regime_labels: str,
    output: str,
    root: str = "/hdd3/kykt26/data",
    repo: str = DEFAULT_REPO,
    checkpoint: str = DEFAULT_CHECKPOINT,
    max_windows_per_domain: int = 5,
    image_resolution: int = 512,
    resize_mode: str = "balanced",
    device_name: str = "auto",
    output_cache_dir: str = "",
) -> Dict[str, Any]:
    repo_path = Path(repo)
    checkpoint_path = Path(checkpoint)
    if not repo_path.exists():
        raise FileNotFoundError(f"VGGT-Omega repo not found: {repo_path}")
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"VGGT-Omega checkpoint not found: {checkpoint_path}")

    device = torch.device(
        "cuda" if device_name == "auto" and torch.cuda.is_available()
        else "cpu" if device_name == "auto"
        else device_name
    )
    VGGTOmega, load_and_preprocess_images, _ = _load_upstream(repo_path)
    model = VGGTOmega().to(device).eval()
    state = torch.load(checkpoint_path, map_location="cpu")
    model.load_state_dict(state)
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)

    blobs = {
        "kitti": _load_cache(kitti_cache),
        "eth3d": _load_cache(eth3d_cache),
    }
    expert_order = list(blobs["kitti"]["expert_order"])
    if list(blobs["eth3d"]["expert_order"]) != expert_order:
        raise ValueError("KITTI/ETH3D expert_order mismatch")

    eth3d_ds = _eth3d_dataset_from_regime(root, eth3d_regime_labels, window_frames=4)
    rows_by_domain: Dict[str, List[Dict[str, Any]]] = {"kitti": [], "eth3d": []}
    expanded_entries: Dict[str, List[Dict[str, Any]]] = {"kitti": [], "eth3d": []}
    failures: List[str] = []
    start = time.perf_counter()
    for domain, blob in blobs.items():
        for entry in _select_entries(blob, max_windows_per_domain):
            seq = entry["seq"]
            try:
                image_paths = (
                    _kitti_image_paths(root, seq, window_frames=4)
                    if domain == "kitti"
                    else _eth3d_image_paths(eth3d_ds, seq)
                )
                images = load_and_preprocess_images(
                    image_paths,
                    image_resolution=image_resolution,
                    mode=resize_mode,
                ).to(device)
                predictions = model(images)
                depth = _normalize_depth(predictions["depth"]).detach().cpu()
                depth_conf = predictions["depth_conf"].detach().cpu()
                gt = entry["gt_pointmap"].unsqueeze(0)
                mask = entry["gt_mask"].unsqueeze(0)
                n_patches = int(gt.shape[-2])
                vggt_pointmap = _dense_depth_to_patch_pointmap(depth, n_patches).unsqueeze(0)
                vggt_confidence = _dense_conf_to_patch_confidence(depth_conf, n_patches).unsqueeze(0)
                metrics = {
                    name: _pointmap_abs_rel(
                        entry["proposals"][name]["pointmap"].unsqueeze(0),
                        gt,
                        mask,
                        align_scale=True,
                    )
                    for name in expert_order
                }
                metrics["vggt_omega"] = _pointmap_abs_rel(
                    vggt_pointmap,
                    gt,
                    mask,
                    align_scale=True,
                )
                old_best = min(expert_order, key=lambda name: metrics[name])
                new_order = expert_order + ["vggt_omega"]
                new_best = min(new_order, key=lambda name: metrics[name])
                rows_by_domain[domain].append({
                    "seq": seq,
                    "domain": domain,
                    "image_paths": image_paths,
                    "metrics": metrics,
                    "old_best_expert": old_best,
                    "new_best_expert": new_best,
                    "old_oracle": metrics[old_best],
                    "new_oracle": metrics[new_best],
                    "vggt_depth_shape": list(depth.shape),
                })
                expanded_entries[domain].append(
                    _expanded_entry(entry, expert_order, vggt_pointmap, vggt_confidence)
                )
                print(
                    f"{domain} {len(rows_by_domain[domain])}: {seq} "
                    f"old={metrics[old_best]:.4f}({old_best}) "
                    f"new={metrics[new_best]:.4f}({new_best}) "
                    f"vggt={metrics['vggt_omega']:.4f}",
                    flush=True,
                )
            except Exception as exc:
                failures.append(f"{domain}:{seq}:{type(exc).__name__}:{exc}")
                print(f"FAIL {domain}:{seq}: {type(exc).__name__}: {exc}", flush=True)

    runtime_ms = (time.perf_counter() - start) * 1000.0
    vram_mb = torch.cuda.max_memory_allocated(device) / (1024.0 * 1024.0) if device.type == "cuda" else None
    cache_outputs: Dict[str, str] = {}
    if output_cache_dir:
        cache_dir = Path(output_cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)
        for domain, entries in expanded_entries.items():
            if not entries:
                continue
            source_blob = blobs[domain]
            cache_path = cache_dir / f"scf_{domain}_vggt_omega_cache.pt"
            torch.save({
                "dataset": source_blob["dataset"],
                "preset": source_blob.get("preset", "vggt_omega_expanded"),
                "n_windows": len(entries),
                "d_memory": source_blob.get("d_memory"),
                "expert_order": expert_order + ["vggt_omega"],
                "entries": entries,
            }, cache_path)
            cache_outputs[domain] = str(cache_path)
    result = {
        "schema_version": "dream3r_vggt_omega_oracle_admission_v1",
        "adapter": "vggt_omega",
        "backend": "real",
        "fallback_contamination_count": 0,
        "failure_flags": failures,
        "repo": str(repo_path),
        "checkpoint": str(checkpoint_path),
        "root": root,
        "image_resolution": image_resolution,
        "resize_mode": resize_mode,
        "device": str(device),
        "runtime_ms": runtime_ms,
        "vram_mb": vram_mb,
        "expert_order": expert_order + ["vggt_omega"],
        "summary": {
            domain: _summarize_rows(rows, expert_order)
            for domain, rows in rows_by_domain.items()
        },
        "cache_outputs": cache_outputs,
        "rows": rows_by_domain,
        "promotable_to_tiny_cache": all(rows_by_domain.values())
        and any(
            result_summary["oracle_gain_abs_rel"] > 0
            for result_summary in [
                _summarize_rows(rows_by_domain["kitti"], expert_order),
                _summarize_rows(rows_by_domain["eth3d"], expert_order),
            ]
        ),
    }
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "output": str(output_path),
        "summary": result["summary"],
        "failure_flags": failures,
        "promotable_to_tiny_cache": result["promotable_to_tiny_cache"],
        "cache_outputs": cache_outputs,
    }, indent=2, sort_keys=True), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--kitti-cache", default="runs/stage6_fusion/scf_kitti_cache.pt")
    parser.add_argument("--eth3d-cache", default="runs/stage6_fusion/scf_eth3d_cache.pt")
    parser.add_argument("--kitti-regime-labels", default="runs/stage3_regime_labels/regime_labels.json")
    parser.add_argument("--eth3d-regime-labels", default="runs/eth3d_cross_dataset_regime_labels/regime_labels.json")
    parser.add_argument("--output", default="runs/v22_admission/vggt_omega_oracle/tiny_oracle_admission.json")
    parser.add_argument("--root", default="/hdd3/kykt26/data")
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--checkpoint", default=DEFAULT_CHECKPOINT)
    parser.add_argument("--max-windows-per-domain", type=int, default=5)
    parser.add_argument("--image-resolution", type=int, default=512)
    parser.add_argument("--resize-mode", default="balanced")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--output-cache-dir", default="")
    args = parser.parse_args()
    evaluate_vggt_omega_admission(
        kitti_cache=args.kitti_cache,
        eth3d_cache=args.eth3d_cache,
        kitti_regime_labels=args.kitti_regime_labels,
        eth3d_regime_labels=args.eth3d_regime_labels,
        output=args.output,
        root=args.root,
        repo=args.repo,
        checkpoint=args.checkpoint,
        max_windows_per_domain=args.max_windows_per_domain,
        image_resolution=args.image_resolution,
        resize_mode=args.resize_mode,
        device_name=args.device,
        output_cache_dir=args.output_cache_dir,
    )


if __name__ == "__main__":
    main()
