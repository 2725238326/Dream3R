"""Run the Dream3R v1.1.0 release model on proposal-cache entries.

This is the real-cache companion to ``run_dream3r_v11_demo.py``. It consumes
SCF/proposal-bank cache files produced by the existing pipeline, validates the
expert order for the selected v1.1 domain branch, runs the official release
API, and writes a compact JSON report.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List

import torch

_CODE_ROOT = Path(__file__).resolve().parents[2]
if str(_CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(_CODE_ROOT))

from dream3r.release_v11 import (  # noqa: E402
    ETH3D_EXPERT_ORDER,
    KITTI_EXPERT_ORDER,
    RELEASE_V11_CANDIDATE,
    RELEASE_V11_VERSION,
    build_dream3r_v11_release,
)
from dream3r.scripts.build_oracle_expert_labels import _pointmap_abs_rel  # noqa: E402
from dream3r.scripts.train_scf_head import _load_caches  # noqa: E402


DEFAULT_CACHE_BY_DOMAIN = {
    "kitti": Path("runs/stage6_fusion/scf_kitti_cache.pt"),
    "eth3d": Path("runs/v22_admission/vggt_omega_cache_gate/scf_eth3d_vggt_omega_cache.pt"),
}

EXPECTED_EXPERT_ORDER = {
    "kitti": list(KITTI_EXPERT_ORDER),
    "eth3d": list(ETH3D_EXPERT_ORDER),
}


def _device(name: str) -> torch.device:
    if name == "auto":
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return torch.device(name)


def _shape(tensor: torch.Tensor | None) -> list[int] | None:
    if tensor is None:
        return None
    return list(tensor.shape)


def _entry_label(entry: Dict[str, Any], fallback_index: int) -> Dict[str, Any]:
    keys = ("domain", "sequence", "seq", "window_id", "window", "index", "sample_id")
    label = {key: entry[key] for key in keys if key in entry}
    label.setdefault("cache_entry_index", fallback_index)
    return label


def _stack_entry(
    entry: Dict[str, Any],
    *,
    expert_order: Iterable[str],
    device: torch.device,
) -> Dict[str, torch.Tensor | None]:
    pointmaps = torch.stack(
        [entry["proposals"][name]["pointmap"] for name in expert_order], dim=0
    ).unsqueeze(0).to(device)
    confidences = torch.stack(
        [entry["proposals"][name]["confidence"] for name in expert_order], dim=0
    ).unsqueeze(0).to(device)
    memory_context = entry.get("memory_context")
    if memory_context is not None:
        memory_context = memory_context.unsqueeze(0).to(device)
    conflict_score = torch.tensor([[float(entry.get("conflict_score", 0.0))]], device=device)
    gt_pointmap = entry.get("gt_pointmap")
    gt_mask = entry.get("gt_mask")
    if gt_pointmap is not None:
        gt_pointmap = gt_pointmap.unsqueeze(0).to(device)
    if gt_mask is not None:
        gt_mask = gt_mask.unsqueeze(0).to(device)
    return {
        "proposal_pointmaps": pointmaps,
        "proposal_confidences": confidences,
        "memory_context": memory_context,
        "conflict_score": conflict_score,
        "gt_pointmap": gt_pointmap,
        "gt_mask": gt_mask,
    }


def _summarize_output(
    *,
    out: Dict[str, Any],
    tensors: Dict[str, torch.Tensor | None],
) -> Dict[str, Any]:
    weights = out["expert_weights"].detach().cpu()
    summary: Dict[str, Any] = {
        "domain_branch": out["domain_branch"],
        "final_pointmap_shape": _shape(out["final_pointmap"]),
        "final_confidence_shape": _shape(out["final_confidence"]),
        "expert_weights_shape": _shape(weights),
        "expert_weight_sum_min": float(weights.sum(dim=1).min().item()),
        "expert_weight_sum_max": float(weights.sum(dim=1).max().item()),
    }
    if tensors["gt_pointmap"] is not None and tensors["gt_mask"] is not None:
        summary["abs_rel_vs_cache_gt"] = _pointmap_abs_rel(
            out["final_pointmap"],
            tensors["gt_pointmap"],
            tensors["gt_mask"],
            align_scale=True,
        )
    return summary


@torch.inference_mode()
def run_cache_demo(
    *,
    domain: str,
    cache_paths: List[Path],
    output: Path | None = None,
    max_entries: int = 1,
    device_name: str = "auto",
) -> Dict[str, Any]:
    domain_key = domain.lower()
    if domain_key not in EXPECTED_EXPERT_ORDER:
        raise ValueError(f"unsupported cache-demo domain: {domain}")
    if max_entries < 1:
        raise ValueError("max_entries must be >= 1")
    if not cache_paths:
        raise ValueError("at least one cache path is required")

    missing = [str(path) for path in cache_paths if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing cache path(s): {missing}")

    entries, d_memory, expert_order = _load_caches([str(path) for path in cache_paths])
    expected_order = EXPECTED_EXPERT_ORDER[domain_key]
    if list(expert_order) != expected_order:
        raise ValueError(
            f"{domain_key} v1.1 branch requires expert_order={expected_order}, got {expert_order}"
        )

    matched = [(i, entry) for i, entry in enumerate(entries) if entry.get("domain") == domain_key]
    if not matched:
        raise ValueError(f"cache has no entries for domain={domain_key}")

    device = _device(device_name)
    model = build_dream3r_v11_release(d_memory=d_memory).to(device)
    model.eval()

    item_reports: list[Dict[str, Any]] = []
    abs_rel_values: list[float] = []
    for original_index, entry in matched[:max_entries]:
        tensors = _stack_entry(entry, expert_order=expert_order, device=device)
        out = model(
            tensors["proposal_pointmaps"],
            tensors["proposal_confidences"],
            tensors["memory_context"],
            tensors["conflict_score"],
            domain=domain_key,
        )
        item = {
            "entry": _entry_label(entry, original_index),
            "input_shapes": {
                "proposal_pointmaps": _shape(tensors["proposal_pointmaps"]),
                "proposal_confidences": _shape(tensors["proposal_confidences"]),
                "memory_context": _shape(tensors["memory_context"]),
                "conflict_score": _shape(tensors["conflict_score"]),
                "gt_pointmap": _shape(tensors["gt_pointmap"]),
                "gt_mask": _shape(tensors["gt_mask"]),
            },
            "output": _summarize_output(out=out, tensors=tensors),
        }
        if "abs_rel_vs_cache_gt" in item["output"]:
            abs_rel_values.append(float(item["output"]["abs_rel_vs_cache_gt"]))
        item_reports.append(item)

    report: Dict[str, Any] = {
        "status": "pass",
        "demo_mode": "proposal_cache_runtime",
        "version": RELEASE_V11_VERSION,
        "candidate": RELEASE_V11_CANDIDATE,
        "official_api": "dream3r.release_v11.build_dream3r_v11_release",
        "domain": domain_key,
        "device": str(device),
        "cache_paths": [str(path) for path in cache_paths],
        "cache_entries_total": len(entries),
        "cache_entries_matched_domain": len(matched),
        "entries_ran": len(item_reports),
        "d_memory": d_memory,
        "model_config_source": "cache d_memory override on v1.1 release policy",
        "expert_order": list(expert_order),
        "items": item_reports,
        "aggregate": {
            "mean_abs_rel_vs_cache_gt": (
                sum(abs_rel_values) / len(abs_rel_values) if abs_rel_values else None
            ),
            "metric_direction": "lower_is_better",
        },
        "claim_boundary": {
            "safe_claim": "v1.1 official release consumes proposal-cache entries",
            "not_claimed": [
                "benchmark rerun",
                "proposal-free foundation 3R",
                "image-only inference",
            ],
        },
    }

    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", choices=sorted(EXPECTED_EXPERT_ORDER), required=True)
    parser.add_argument(
        "--cache",
        type=Path,
        nargs="+",
        default=None,
        help="SCF/proposal cache path(s); defaults to the known server cache for the domain",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="where to write the cache-demo report; defaults to runs/release/v11_cache_demo/cache_demo_<domain>.json",
    )
    parser.add_argument("--max-entries", type=int, default=1)
    parser.add_argument("--device", default="auto", help="auto, cpu, cuda, or cuda:<idx>")
    args = parser.parse_args()

    cache_paths = args.cache or [DEFAULT_CACHE_BY_DOMAIN[args.domain]]
    output = args.output or Path(f"runs/release/v11_cache_demo/cache_demo_{args.domain}.json")
    report = run_cache_demo(
        domain=args.domain,
        cache_paths=cache_paths,
        output=output,
        max_entries=args.max_entries,
        device_name=args.device,
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
