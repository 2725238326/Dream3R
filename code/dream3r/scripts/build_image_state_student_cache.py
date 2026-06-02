"""Build Dream3R-U1 image/state native student cache.

The existing SCF cache does not store image tokens, so it cannot train a
usable image-conditioned native decoder. This builder mirrors
``build_scf_cache`` but additionally stores frozen Perceiver image tokens.
It remains non-core and preserves the real-backend proposal guardrail.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Dict, List, Optional

import torch

from dream3r.model import build_dream3r
from dream3r.orchestrator import build_v04_pipeline
from dream3r.scripts.build_oracle_expert_labels import _resize_images
from dream3r.scripts.train_fusion_head import (
    REAL_EXPERTS,
    _iter_eth3d_windows,
    _iter_kitti_windows,
    ensure_real_backends,
)


def build_image_state_student_cache(
    dataset_name: str,
    root: str,
    regime_labels: str,
    output: str,
    preset: str = "small_real",
    window_frames: int = 4,
    image_size: int = 224,
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"=== Image-state student cache ({dataset_name}, preset={preset}) ===", flush=True)
    print(f"  device: {device}", flush=True)

    model = build_dream3r(preset).to(device)
    model.eval()
    ensure_real_backends(model)
    registry = model.composer.registry
    adapters = {name: registry.get(name) for name in REAL_EXPERTS}
    pipeline = build_v04_pipeline(model, max_repair_attempts=1).to(device)
    print(f"  real-backend guardrail: {list(REAL_EXPERTS)} all loaded", flush=True)

    if dataset_name == "kitti_long":
        iterator = _iter_kitti_windows(root, regime_labels, window_frames)
    elif dataset_name == "eth3d_long":
        iterator = _iter_eth3d_windows(root, regime_labels, window_frames)
    else:
        raise ValueError(f"unknown dataset: {dataset_name}")

    entries: List[Dict] = []
    d_memory: Optional[int] = None
    d_image: Optional[int] = None
    t_start = time.time()
    for idx, (seq, sample) in enumerate(iterator):
        images = sample["images"][0].unsqueeze(0).to(device)
        images = _resize_images(images, image_size)
        target = sample["pointmap_gt"][0].unsqueeze(0)
        mask = sample["pointmap_mask"][0].unsqueeze(0)

        with torch.no_grad():
            out = pipeline(images=images, timestep=0)
            image_tokens = model.perceiver.encode_images(images).detach().cpu().squeeze(0)
            proposals: Dict[str, Dict[str, torch.Tensor]] = {}
            backends: Dict[str, bool] = {}
            for name in REAL_EXPERTS:
                eo = adapters[name].forward(images)
                proposals[name] = {
                    "pointmap": eo.pointmap.detach().cpu().squeeze(0),
                    "confidence": eo.confidence.detach().cpu().squeeze(0),
                }
                backends[name] = bool(adapters[name].is_loaded)

        if not all(backends.values()):
            raise RuntimeError(f"{seq}: not all real experts loaded: {backends}")

        memory = out.memory
        critic = out.critic
        mc = memory.fused_context.detach().cpu().squeeze(0) \
            if (memory is not None and memory.fused_context is not None) else None
        if mc is not None and d_memory is None:
            d_memory = int(mc.shape[-1])
        if d_image is None:
            d_image = int(image_tokens.shape[-1])

        entries.append({
            "seq": seq,
            "domain": "kitti" if dataset_name == "kitti_long" else "eth3d",
            "image_tokens": image_tokens,
            "proposals": proposals,
            "expert_order": list(REAL_EXPERTS),
            "expert_backends": backends,
            "memory_context": mc,
            "conflict_score": float(critic.conflict_score.flatten()[0].item())
            if critic is not None else 0.0,
            "gt_pointmap": target.squeeze(0).cpu(),
            "gt_mask": mask.squeeze(0).cpu(),
        })
        print(f"  [{idx+1}] {seq}: ok (elapsed={time.time()-t_start:.1f}s)", flush=True)

    blob = {
        "dataset": dataset_name,
        "preset": preset,
        "n_windows": len(entries),
        "d_memory": d_memory,
        "d_image": d_image,
        "expert_order": list(REAL_EXPERTS),
        "entries": entries,
    }
    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(blob, out_path)
    print(f"\nSaved image-state student cache to {out_path}", flush=True)
    print(
        f"  n_windows: {len(entries)}, d_memory: {d_memory}, "
        f"d_image: {d_image}, experts: {list(REAL_EXPERTS)}",
        flush=True,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=["kitti_long", "eth3d_long"], required=True)
    ap.add_argument("--root", default="/hdd3/kykt26/data")
    ap.add_argument("--regime-labels", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--preset", default="small_real")
    ap.add_argument("--window-frames", type=int, default=4)
    ap.add_argument("--image-size", type=int, default=224)
    args = ap.parse_args()
    build_image_state_student_cache(
        args.dataset,
        args.root,
        args.regime_labels,
        args.output,
        args.preset,
        args.window_frames,
        args.image_size,
    )


if __name__ == "__main__":
    main()
