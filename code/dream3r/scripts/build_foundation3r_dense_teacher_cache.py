"""Build dense teacher caches for the Foundation3R proposal-free line.

The saved cache is for training only. It stores RGB window identifiers and
offline dense teacher targets, but never stores proposal-bank fields.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import torch
import torch.nn.functional as F

from dream3r.scripts.eval_vggt_omega_oracle_admission import (
    DEFAULT_CHECKPOINT,
    DEFAULT_REPO,
    _dense_conf_to_patch_confidence,
    _dense_depth_to_patch_pointmap,
)
from dream3r.scripts.smoke_vggt_omega_adapter import _load_upstream, _normalize_depth


SCHEMA_VERSION = "dream3r_foundation3r_dense_teacher_cache_v1"
FORBIDDEN_ENTRY_KEYS = {
    "proposals",
    "proposal_pointmaps",
    "proposal_confidences",
    "expert_confidences",
    "expert_order",
    "teacher_model",
}


def _load_manifest(path: str, max_windows: int = 0) -> List[Dict[str, Any]]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    windows = (
        data
        if isinstance(data, list)
        else data.get("windows", data.get("records")) if isinstance(data, dict)
        else None
    )
    if not isinstance(windows, list):
        raise ValueError("manifest must contain a windows/records list or be a JSON list")
    out: List[Dict[str, Any]] = []
    for idx, row in enumerate(windows):
        if max_windows > 0 and len(out) >= max_windows:
            break
        if not isinstance(row, dict):
            raise ValueError(f"manifest row {idx} is not an object")
        window_id = str(row.get("window_id") or row.get("sequence") or "")
        frames = [str(x) for x in row.get("frames", [])]
        domain = str(row.get("dataset") or row.get("domain") or "")
        if not window_id:
            raise ValueError(f"manifest row {idx} missing window_id/sequence")
        if not domain:
            raise ValueError(f"manifest row {idx} missing dataset/domain")
        if not frames:
            raise ValueError(f"manifest row {idx} missing frames")
        out.append({**row, "window_id": window_id, "frames": frames, "domain": domain})
    return out


def _load_state_index(cache_paths: Iterable[str]) -> Dict[str, Dict[str, Any]]:
    index: Dict[str, Dict[str, Any]] = {}
    for path in cache_paths:
        if not path:
            continue
        blob = torch.load(path, map_location="cpu", weights_only=False)
        for entry in blob.get("entries", []):
            seq = str(entry.get("seq") or entry.get("window_id") or "")
            if not seq:
                continue
            clean = {
                "memory_context": entry.get("memory_context"),
                "conflict_score": float(entry.get("conflict_score", 0.0)),
                "gt_pointmap": entry.get("gt_pointmap"),
                "gt_mask": entry.get("gt_mask"),
            }
            index[seq] = clean
            index[f"{entry.get('domain', '')}/{seq}"] = clean
    return index


def _state_for_window(window: Dict[str, Any], state_index: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    keys = [
        str(window.get("sequence", "")),
        str(window.get("window_id", "")),
        f"{window.get('domain', '')}/{window.get('sequence', '')}",
        f"{window.get('domain', '')}/{window.get('window_id', '')}",
    ]
    for key in keys:
        if key in state_index:
            return state_index[key]
    return {}


def _seed_from_window(window: Dict[str, Any]) -> int:
    text = json.dumps({
        "window_id": window.get("window_id"),
        "frames": window.get("frames"),
        "domain": window.get("domain"),
    }, sort_keys=True)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def _mock_teacher(window: Dict[str, Any], n_patches: int) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    n = len(window["frames"])
    gen = torch.Generator().manual_seed(_seed_from_window(window))
    z = torch.rand(n, n_patches, generator=gen).clamp_min(0.05)
    pointmap = torch.zeros(n, n_patches, 3)
    pointmap[..., 2] = z
    confidence = torch.rand(n, n_patches, 1, generator=gen) * 0.5 + 0.5
    valid = torch.ones(n, n_patches, dtype=torch.bool)
    return pointmap, confidence, valid


def _mock_vggt_features(window: Dict[str, Any], n_patches: int, feature_dim: int) -> torch.Tensor:
    n = len(window["frames"])
    gen = torch.Generator().manual_seed(_seed_from_window(window) + 17)
    return torch.randn(n, n_patches, feature_dim, generator=gen) * 0.02


def _compact_vggt_patch_features(patch_tokens: torch.Tensor, feature_dim: int) -> torch.Tensor:
    """Deterministically compress VGGT patch tokens without adding trainable state."""
    n, p, c = patch_tokens.shape
    if feature_dim <= 0:
        raise ValueError("feature_dim must be positive")
    if c < feature_dim:
        raise ValueError(f"cannot compact {c} channels to {feature_dim}")
    usable = (c // feature_dim) * feature_dim
    compact = patch_tokens[..., :usable].float().reshape(n, p, feature_dim, usable // feature_dim)
    return compact.mean(dim=-1)


def _downsample_patch_tokens(
    patch_tokens: torch.Tensor,
    n_patches: int,
    source_grid: Optional[tuple[int, int]] = None,
) -> torch.Tensor:
    n, p, c = patch_tokens.shape
    if source_grid is None:
        source_side = int(math.sqrt(p))
        source_grid = (source_side, source_side)
    source_h, source_w = source_grid
    target_side = int(math.sqrt(n_patches))
    if source_h * source_w != p:
        raise ValueError(f"VGGT patch token count {p} does not match source grid {source_grid}")
    if target_side * target_side != n_patches:
        raise ValueError(f"target patch count is not square: {n_patches}")
    grid = patch_tokens.transpose(1, 2).reshape(n, c, source_h, source_w)
    pooled = F.adaptive_avg_pool2d(grid, (target_side, target_side))
    return pooled.flatten(2).transpose(1, 2)


def _build_vggt_backend(repo: str, checkpoint: str, device_name: str, image_resolution: int, resize_mode: str):
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
    return {
        "device": device,
        "model": model,
        "load_and_preprocess_images": load_and_preprocess_images,
        "image_resolution": image_resolution,
        "resize_mode": resize_mode,
    }


@torch.inference_mode()
def _vggt_teacher(
    backend: Dict[str, Any],
    frames: List[str],
    n_patches: int,
    include_vggt_features: bool = False,
    vggt_feature_dim: int = 128,
):
    missing = [frame for frame in frames if not Path(frame).expanduser().exists()]
    if missing:
        raise FileNotFoundError(f"missing image frames: {missing[:3]}")
    images = backend["load_and_preprocess_images"](
        frames,
        image_resolution=backend["image_resolution"],
        mode=backend["resize_mode"],
    ).to(backend["device"])
    pred = backend["model"](images)
    depth = _normalize_depth(pred["depth"]).detach().cpu()
    conf = pred["depth_conf"].detach().cpu()
    pointmap = _dense_depth_to_patch_pointmap(depth, n_patches)
    confidence = _dense_conf_to_patch_confidence(conf, n_patches)
    valid = torch.isfinite(pointmap[..., 2]) & (pointmap[..., 2] > 0)
    features = None
    if include_vggt_features:
        image_batch = images.unsqueeze(0) if images.dim() == 4 else images
        amp_enabled = backend["device"].type == "cuda"
        amp_dtype = torch.bfloat16 if amp_enabled and torch.cuda.is_bf16_supported() else torch.float16
        with torch.autocast(device_type="cuda", dtype=amp_dtype, enabled=amp_enabled):
            aggregated_tokens_list, patch_token_start = backend["model"].aggregator(image_batch)
        final_tokens = aggregated_tokens_list[-1]
        patch_tokens = final_tokens[0, :, patch_token_start:].detach().cpu()
        patch_size = int(getattr(backend["model"].aggregator, "patch_size", 16))
        source_grid = (int(image_batch.shape[-2]) // patch_size, int(image_batch.shape[-1]) // patch_size)
        patch_tokens = _downsample_patch_tokens(patch_tokens, n_patches, source_grid=source_grid)
        features = _compact_vggt_patch_features(patch_tokens, vggt_feature_dim).to(torch.float16)
    return pointmap, confidence, valid, features


def _clean_state_tensor(value: Optional[torch.Tensor]) -> Optional[torch.Tensor]:
    if value is None:
        return None
    return value.detach().cpu()


def _assert_no_forbidden_fields(entry: Dict[str, Any]) -> None:
    leaked = sorted(FORBIDDEN_ENTRY_KEYS.intersection(entry))
    if leaked:
        raise ValueError(f"foundation cache entry leaks forbidden proposal fields: {leaked}")


def build_foundation3r_dense_teacher_cache(
    window_manifest: str,
    output: str,
    backend: str = "mock",
    state_caches: Optional[List[str]] = None,
    max_windows: int = 0,
    n_patches: int = 196,
    repo: str = DEFAULT_REPO,
    checkpoint: str = DEFAULT_CHECKPOINT,
    image_resolution: int = 512,
    resize_mode: str = "balanced",
    device: str = "auto",
    include_vggt_features: bool = False,
    vggt_feature_dim: int = 128,
) -> Dict[str, Any]:
    if backend not in {"mock", "vggt_omega"}:
        raise ValueError(f"unsupported backend: {backend}")
    windows = _load_manifest(window_manifest, max_windows=max_windows)
    state_index = _load_state_index(state_caches or [])
    vggt_backend = (
        _build_vggt_backend(repo, checkpoint, device, image_resolution, resize_mode)
        if backend == "vggt_omega"
        else None
    )

    entries: List[Dict[str, Any]] = []
    failures: List[str] = []
    start = time.perf_counter()
    for window in windows:
        try:
            state = _state_for_window(window, state_index)
            gt = state.get("gt_pointmap")
            patch_count = int(gt.shape[-2]) if isinstance(gt, torch.Tensor) else int(n_patches)
            if backend == "mock":
                teacher_pointmap, teacher_confidence, teacher_valid_mask = _mock_teacher(
                    window,
                    patch_count,
                )
                vggt_patch_features = (
                    _mock_vggt_features(window, patch_count, vggt_feature_dim).to(torch.float16)
                    if include_vggt_features
                    else None
                )
            else:
                teacher_pointmap, teacher_confidence, teacher_valid_mask, vggt_patch_features = _vggt_teacher(
                    vggt_backend,
                    window["frames"],
                    patch_count,
                    include_vggt_features=include_vggt_features,
                    vggt_feature_dim=vggt_feature_dim,
                )
            entry = {
                "window_id": str(window["window_id"]),
                "seq": str(window.get("sequence") or window["window_id"]),
                "domain": str(window["domain"]),
                "frames": list(window["frames"]),
                "teacher_backend": backend,
                "teacher_pointmap": teacher_pointmap.detach().cpu(),
                "teacher_confidence": teacher_confidence.detach().cpu(),
                "teacher_valid_mask": teacher_valid_mask.detach().cpu().bool(),
                "memory_context": _clean_state_tensor(state.get("memory_context")),
                "conflict_score": float(state.get("conflict_score", 0.0)),
                "gt_pointmap": _clean_state_tensor(state.get("gt_pointmap")),
                "gt_mask": _clean_state_tensor(state.get("gt_mask")),
            }
            if vggt_patch_features is not None:
                entry["vggt_patch_features"] = vggt_patch_features.detach().cpu()
                entry["vggt_feature_source"] = "vggt_omega_aggregator_final_patch_tokens_chunkmean"
            _assert_no_forbidden_fields(entry)
            entries.append(entry)
        except Exception as exc:
            failures.append(f"{window.get('window_id', '<unknown>')}:{type(exc).__name__}:{exc}")

    result = {
        "schema_version": SCHEMA_VERSION,
        "cache_type": "foundation3r_dense_teacher",
        "teacher_backend": backend,
        "window_manifest": window_manifest,
        "n_windows": len(entries),
        "n_failures": len(failures),
        "fallback_contamination_count": 0 if backend == "vggt_omega" else None,
        "proposal_fields_stripped": True,
        "teacher_used_at_inference": False,
        "proposal_inputs_used": False,
        "vggt_features_included": bool(include_vggt_features),
        "vggt_feature_dim": int(vggt_feature_dim) if include_vggt_features else None,
        "forbidden_entry_keys": sorted(FORBIDDEN_ENTRY_KEYS),
        "runtime_ms": (time.perf_counter() - start) * 1000.0,
        "failure_flags": failures,
        "entries": entries,
    }
    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(result, out_path)
    report = {
        key: value for key, value in result.items()
        if key != "entries"
    }
    report["output"] = str(out_path)
    report["entry_shapes"] = [
        {
            "window_id": entry["window_id"],
            "teacher_pointmap": list(entry["teacher_pointmap"].shape),
            "teacher_confidence": list(entry["teacher_confidence"].shape),
            "teacher_valid_mask": list(entry["teacher_valid_mask"].shape),
            "vggt_patch_features": (
                list(entry["vggt_patch_features"].shape)
                if "vggt_patch_features" in entry
                else None
            ),
            "has_gt": entry["gt_pointmap"] is not None,
            "has_state": entry["memory_context"] is not None,
        }
        for entry in entries[:10]
    ]
    report_path = out_path.with_suffix(".json")
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2), flush=True)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--window-manifest", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--backend", choices=["mock", "vggt_omega"], default="mock")
    parser.add_argument("--state-cache", nargs="*", default=[])
    parser.add_argument("--max-windows", type=int, default=0)
    parser.add_argument("--n-patches", type=int, default=196)
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--checkpoint", default=DEFAULT_CHECKPOINT)
    parser.add_argument("--image-resolution", type=int, default=512)
    parser.add_argument("--resize-mode", default="balanced")
    parser.add_argument("--device", default="auto")
    parser.add_argument("--include-vggt-features", action="store_true")
    parser.add_argument("--vggt-feature-dim", type=int, default=128)
    args = parser.parse_args()
    build_foundation3r_dense_teacher_cache(
        window_manifest=args.window_manifest,
        output=args.output,
        backend=args.backend,
        state_caches=args.state_cache,
        max_windows=args.max_windows,
        n_patches=args.n_patches,
        repo=args.repo,
        checkpoint=args.checkpoint,
        image_resolution=args.image_resolution,
        resize_mode=args.resize_mode,
        device=args.device,
        include_vggt_features=args.include_vggt_features,
        vggt_feature_dim=args.vggt_feature_dim,
    )


if __name__ == "__main__":
    main()
