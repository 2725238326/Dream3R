"""Build proposal-free distillation caches.

The output cache keeps only fields needed by proposal-free training:

``image_tokens, Dream state, conflict score, GT pointmap, teacher_pointmap``.

Proposal tensors are used only inside this offline builder and are stripped
from the saved entries by default. That keeps the training/inference contract
proposal-free while still allowing teacher distillation.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Tuple

import torch

from dream3r.scripts.build_oracle_expert_labels import _pointmap_abs_rel


def _select_best_single_teacher(entry: Dict, expert_order: List[str]) -> Tuple[torch.Tensor, str, float]:
    proposals = entry.get("proposals") or {}
    gt = entry["gt_pointmap"].unsqueeze(0)
    mask = entry["gt_mask"].unsqueeze(0)
    best_name = ""
    best_metric = float("inf")
    best_pointmap = None
    for name in expert_order:
        if name not in proposals:
            continue
        pointmap = proposals[name]["pointmap"].unsqueeze(0)
        metric = _pointmap_abs_rel(pointmap, gt, mask, align_scale=True)
        if metric < best_metric:
            best_name = name
            best_metric = float(metric)
            best_pointmap = proposals[name]["pointmap"].detach().cpu()
    if best_pointmap is None:
        raise ValueError(f"{entry.get('seq', '<unknown>')} has no usable proposal teacher")
    return best_pointmap, best_name, best_metric


def build_proposal_free_teacher_cache(
    cache_paths: List[str],
    output: str,
    teacher_policy: str = "best_single",
    keep_proposals: bool = False,
) -> Dict:
    if teacher_policy != "best_single":
        raise ValueError(f"unsupported teacher_policy: {teacher_policy}")

    out_entries: List[Dict] = []
    d_image = None
    d_memory = None
    source_paths: List[str] = []
    for path in cache_paths:
        source_paths.append(path)
        blob = torch.load(path, map_location="cpu", weights_only=False)
        if blob.get("d_image") is None:
            raise ValueError(f"{path} has no d_image")
        expert_order = list(blob.get("expert_order", []))
        if not expert_order:
            raise ValueError(f"{path} has no expert_order")
        d_image = int(blob["d_image"]) if d_image is None else d_image
        d_memory = int(blob["d_memory"]) if d_memory is None else d_memory
        for entry in blob["entries"]:
            teacher, teacher_name, teacher_metric = _select_best_single_teacher(entry, expert_order)
            clean = {
                "seq": entry.get("seq", ""),
                "domain": entry["domain"],
                "image_tokens": entry["image_tokens"].detach().cpu(),
                "memory_context": entry.get("memory_context"),
                "conflict_score": float(entry.get("conflict_score", 0.0)),
                "gt_pointmap": entry["gt_pointmap"].detach().cpu(),
                "gt_mask": entry["gt_mask"].detach().cpu(),
                "teacher_pointmap": teacher,
                "teacher_name": teacher_name,
                "teacher_abs_rel": teacher_metric,
                "teacher_policy": teacher_policy,
            }
            if keep_proposals:
                clean["proposals"] = entry.get("proposals")
            out_entries.append(clean)

    result = {
        "cache_type": "proposal_free_teacher",
        "teacher_policy": teacher_policy,
        "source_paths": source_paths,
        "n_windows": len(out_entries),
        "d_image": d_image,
        "d_memory": d_memory,
        "proposal_fields_stripped": not keep_proposals,
        "entries": out_entries,
    }
    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(result, out_path)
    print(
        f"Saved proposal-free teacher cache to {out_path} "
        f"(n={len(out_entries)}, teacher_policy={teacher_policy}, "
        f"proposal_fields_stripped={not keep_proposals})",
        flush=True,
    )
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", nargs="+", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--teacher-policy", default="best_single", choices=["best_single"])
    ap.add_argument("--keep-proposals", action="store_true")
    args = ap.parse_args()
    build_proposal_free_teacher_cache(
        args.cache,
        args.output,
        teacher_policy=args.teacher_policy,
        keep_proposals=args.keep_proposals,
    )


if __name__ == "__main__":
    main()
