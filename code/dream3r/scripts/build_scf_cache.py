"""Dream3R-v0.6 SCF -- all-expert proposal-bank cache builder (SPEC A10).

Per window this runs ALL real experts (fast3r / mast3r / spann3r) forward to
store their proposal pointmaps + confidences, and one ``V04Pipeline.forward``
to capture persistent state (``memory.fused_context``,
``critic.conflict_score``, composer routing prior). This is the multi-expert
proposal bank that ``SCFHead`` fuses, and it directly yields the B0-B4
baselines (per-expert + oracle).

The real-backend guardrail (SPEC-20260527-001 Axis A9) is enforced via
``ensure_real_backends`` so no fallback-stub proposal can enter the cache.

This script never touches v0.3/v0.5 core. It reuses the proven dataset
iterators and guardrail from ``train_fusion_head`` and the metric / resize
helpers from ``build_oracle_expert_labels``.
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
    ensure_real_backends,
    _iter_kitti_windows,
    _iter_eth3d_windows,
)


def build_scf_cache(dataset_name: str, root: str, regime_labels: str, output: str,
                    preset: str = "small_real", window_frames: int = 4,
                    image_size: int = 224):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"=== SCF all-expert cache ({dataset_name}, preset={preset}) ===", flush=True)
    print(f"  device: {device}", flush=True)

    model = build_dream3r(preset)
    model.eval()
    ensure_real_backends(model)  # A9 guardrail: load + assert fast3r/mast3r/spann3r
    registry = model.composer.registry
    adapters = {name: registry.get(name) for name in REAL_EXPERTS}
    pipeline = build_v04_pipeline(model, max_repair_attempts=1).to(device)
    print(f"  real-backend guardrail: {list(REAL_EXPERTS)} all loaded", flush=True)

    sorted_names = sorted(registry.names)
    real_idx = [sorted_names.index(n) for n in REAL_EXPERTS]  # composer logit indices

    if dataset_name == "kitti_long":
        iterator = _iter_kitti_windows(root, regime_labels, window_frames)
    elif dataset_name == "eth3d_long":
        iterator = _iter_eth3d_windows(root, regime_labels, window_frames)
    else:
        raise ValueError(f"unknown dataset: {dataset_name}")

    entries: List[Dict] = []
    d_memory: Optional[int] = None
    t_start = time.time()
    for idx, (seq, sample) in enumerate(iterator):
        images = sample["images"][0].unsqueeze(0).to(device)
        images = _resize_images(images, image_size)
        target = sample["pointmap_gt"][0].unsqueeze(0)         # [1, N, P, 3]
        mask = sample["pointmap_mask"][0].unsqueeze(0)         # [1, N, P]

        with torch.no_grad():
            out = pipeline(images=images, timestep=0)
            proposals: Dict[str, Dict[str, torch.Tensor]] = {}
            backends: Dict[str, bool] = {}
            for name in REAL_EXPERTS:
                eo = adapters[name].forward(images)
                proposals[name] = {
                    "pointmap": eo.pointmap.detach().cpu().squeeze(0),       # [N, P, 3]
                    "confidence": eo.confidence.detach().cpu().squeeze(0),   # [N, P, 1]
                }
                backends[name] = bool(adapters[name].is_loaded)

        if not all(backends.values()):
            raise RuntimeError(f"{seq}: not all real experts loaded: {backends}")

        memory = out.memory
        critic = out.critic
        composer = out.composer
        mc = memory.fused_context.detach().cpu().squeeze(0) \
            if (memory is not None and memory.fused_context is not None) else None
        if mc is not None and d_memory is None:
            d_memory = int(mc.shape[-1])
        prior = None
        if composer is not None and composer.routing_logits is not None:
            rl = composer.routing_logits.detach().cpu().squeeze(0)  # [n_experts]
            prior = rl[real_idx].clone()                            # [E]

        entry = {
            "seq": seq,
            "domain": "kitti" if dataset_name == "kitti_long" else "eth3d",
            "proposals": proposals,
            "expert_order": list(REAL_EXPERTS),
            "expert_backends": backends,
            "memory_context": mc,                                  # [D_mem] or None
            "conflict_score": float(critic.conflict_score.flatten()[0].item())
            if critic is not None else 0.0,
            "composer_prior": prior,                               # [E] or None
            "gt_pointmap": target.squeeze(0).cpu(),                # [N, P, 3]
            "gt_mask": mask.squeeze(0).cpu(),                      # [N, P]
        }
        entries.append(entry)
        print(f"  [{idx+1}] {seq}: ok (elapsed={time.time()-t_start:.1f}s)", flush=True)

    blob = {
        "dataset": dataset_name,
        "preset": preset,
        "n_windows": len(entries),
        "d_memory": d_memory,
        "expert_order": list(REAL_EXPERTS),
        "entries": entries,
    }
    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(blob, out_path)
    print(f"\nSaved SCF cache to {out_path}", flush=True)
    print(f"  n_windows: {len(entries)}, d_memory: {d_memory}, experts: {list(REAL_EXPERTS)}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", choices=["kitti_long", "eth3d_long"], required=True)
    ap.add_argument("--root", default="/hdd3/kykt26/data")
    ap.add_argument("--regime-labels", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--preset", default="small_real")
    ap.add_argument("--window-frames", type=int, default=4)
    ap.add_argument("--image-size", type=int, default=224)
    a = ap.parse_args()
    build_scf_cache(a.dataset, a.root, a.regime_labels, a.output,
                    a.preset, a.window_frames, a.image_size)


if __name__ == "__main__":
    main()
