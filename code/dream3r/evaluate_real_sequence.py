"""Run Dream3R on a small real RGB/depth sequence subset."""

import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict, Optional

import torch

from dream3r.config import config_to_model_args, load_config
from dream3r.data_kitti import KITTIRectifiedSequenceDataset
from dream3r.evaluate import Evaluator
from dream3r.model import Dream3R


def _tensor_mean(value: Any) -> float:
    if isinstance(value, torch.Tensor):
        finite = value.detach().float()
        finite = finite[torch.isfinite(finite)]
        return float(finite.mean().item()) if finite.numel() > 0 else 0.0
    return 0.0


def _summarize_window(index: int, sample: Dict[str, Any],
                      outputs: Dict[str, Any], elapsed_ms: float) -> Dict[str, Any]:
    branch = outputs.get("nsa_branch_weights")
    branch_summary = {}
    if isinstance(branch, torch.Tensor):
        weights = branch.detach().float().mean(dim=(0, 1)).cpu()
        branch_summary = {
            "compressed": round(float(weights[0].item()), 6),
            "selected": round(float(weights[1].item()), 6),
            "sliding": round(float(weights[2].item()), 6),
        }

    retrieval_log = outputs.get("memory_retrieval_log", {})
    promoted = 0.0
    selected_distance = 0.0
    if isinstance(retrieval_log, dict):
        promoted = _tensor_mean(retrieval_log.get("promoted_to_stable"))
        selected_distance = _tensor_mean(retrieval_log.get("selected_3d_distances"))

    effective_top_k = None
    sliding_branch_fired = False
    if isinstance(retrieval_log, dict):
        effective_top_k = retrieval_log.get("effective_top_k")
        active_mask = retrieval_log.get("branch_active_mask")
        if isinstance(active_mask, torch.Tensor) and active_mask.dim() >= 2:
            sliding_branch_fired = bool(active_mask[..., 2].any().item())

    return {
        "index": index,
        "sequence_name": sample["sequence_name"],
        "frame_ids": list(sample["frame_ids"]),
        "elapsed_ms": round(elapsed_ms, 3),
        "bank_occupancy": round(_tensor_mean(outputs.get("bank_occupancy")), 6),
        "latent_drift_proxy": round(_tensor_mean(outputs.get("latent_drift_proxy")), 6),
        "stable_promotion_rate": round(promoted, 6),
        "selected_anchor_3d_distance": round(selected_distance, 6),
        "conflict_score_mean": round(_tensor_mean(outputs.get("conflict_score")), 6),
        "recommended_action": outputs["recommended_action"].detach().cpu().tolist(),
        "nsa_branch_mean": branch_summary,
        "effective_top_k": effective_top_k,
        "sliding_branch_fired": sliding_branch_fired,
    }


@torch.no_grad()
def run_real_sequence_eval(
    data_root: str = "/hdd3/kykt26/data",
    max_windows: int = 2,
    max_sequences: int = 1,
    recurrence: str = "mamba_hybrid",
    device_name: str = "auto",
    config_overrides: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    device = torch.device(
        "cuda" if device_name == "auto" and torch.cuda.is_available()
        else "cpu" if device_name == "auto"
        else device_name
    )
    overrides = {
        "use_backbone": False,
        "state_recurrence_type": recurrence,
        "active_to_stable_threshold": 0.0,
    }
    if config_overrides:
        overrides.update(config_overrides)
    cfg = load_config(overrides=overrides)
    dataset = KITTIRectifiedSequenceDataset(
        data_root=data_root,
        n_frames=cfg["n_frames_per_window"],
        n_patches=196,
        d_model=cfg["d_model"],
        max_sequences=max_sequences,
    )
    if len(dataset) == 0:
        raise RuntimeError(f"No KITTI windows found under {data_root}/kitti/rectified")

    model = Dream3R(config_to_model_args(cfg)).to(device)
    model.eval()
    evaluator = Evaluator()
    prev_memory = None
    prev_slots = None
    prev_slot_poses = None
    windows = []

    limit = min(max_windows, len(dataset))
    for i in range(limit):
        sample = dataset[i]
        x = sample["features"].unsqueeze(0).to(device)
        targets = {
            "pointmap": sample["pointmap_gt"].unsqueeze(0).to(device),
            "pointmap_mask": sample["pointmap_mask"].unsqueeze(0).to(device),
            "conflict_label": sample["conflict_label"].view(1).to(device),
        }
        start = time.perf_counter()
        outputs = model(
            x,
            prev_memory_state=prev_memory,
            prev_object_slots=prev_slots,
            prev_object_slot_poses=prev_slot_poses,
            timestep=i,
        )
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        evaluator.update(outputs, targets)
        windows.append(_summarize_window(i, sample, outputs, elapsed_ms))
        prev_memory = outputs.get("latent_state_tokens")
        prev_slots = outputs.get("object_track_set")
        prev_slot_poses = outputs.get("object_slot_poses")

    recurrence_module = model.memory.state_recurrence
    return {
        "dataset": "kitti_rectified",
        "data_root": data_root,
        "device": str(device),
        "recurrence_type": recurrence,
        "recurrence_backend": getattr(
            recurrence_module, "backend", recurrence_module.__class__.__name__
        ),
        "recurrence_backend_error": getattr(recurrence_module, "backend_error", ""),
        "memory_use_nsa": bool(cfg.get("memory_use_nsa", True)),
        "enable_stable_memory": bool(cfg.get("enable_stable_memory", True)),
        "window_count": limit,
        "metrics": evaluator.compute().to_dict(),
        "windows": windows,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", default="/hdd3/kykt26/data")
    parser.add_argument("--max-windows", type=int, default=2)
    parser.add_argument("--max-sequences", type=int, default=1)
    parser.add_argument(
        "--recurrence",
        choices=["cross_attention", "mamba_hybrid"],
        default="mamba_hybrid",
    )
    parser.add_argument("--disable-nsa", action="store_true")
    parser.add_argument("--disable-stable-memory", action="store_true")
    parser.add_argument("--device", default="auto")
    parser.add_argument(
        "--output",
        default="demo_artifacts/real_sequence/kitti_metrics.json",
    )
    args = parser.parse_args()

    result = run_real_sequence_eval(
        data_root=args.data_root,
        max_windows=args.max_windows,
        max_sequences=args.max_sequences,
        recurrence=args.recurrence,
        device_name=args.device,
        config_overrides={
            "memory_use_nsa": not args.disable_nsa,
            "enable_stable_memory": not args.disable_stable_memory,
        },
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
