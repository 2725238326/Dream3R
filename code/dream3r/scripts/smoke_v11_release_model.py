"""Smoke-test the Dream3R v1.1 effective release model.

This is a packaging/runtime check, not a benchmark. It proves the current
effective architecture entrypoint can execute both domain branches with the
documented proposal-bank contracts.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

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


def _branch_inputs(
    *,
    batch: int,
    experts: int,
    views: int,
    patches: int,
    d_memory: int,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    pointmaps = torch.randn(batch, experts, views, patches, 3)
    confidences = torch.rand(batch, experts, views, patches, 1)
    memory_context = torch.randn(batch, d_memory)
    conflict_score = torch.rand(batch, 1)
    return pointmaps, confidences, memory_context, conflict_score


def _summarize_branch(out: dict[str, Any]) -> dict[str, Any]:
    weights = out["expert_weights"]
    return {
        "domain_branch": out["domain_branch"],
        "final_pointmap_shape": list(out["final_pointmap"].shape),
        "final_confidence_shape": list(out["final_confidence"].shape),
        "expert_weights_shape": list(weights.shape),
        "expert_weight_sum_min": float(weights.sum(dim=1).min().item()),
        "expert_weight_sum_max": float(weights.sum(dim=1).max().item()),
    }


@torch.inference_mode()
def run_smoke(
    *,
    output: Path | None = None,
    seed: int = 7,
    batch: int = 2,
    views: int = 2,
    patches: int = 8,
    d_memory: int = 32,
) -> dict[str, Any]:
    torch.manual_seed(seed)
    model = build_dream3r_v11_release()
    model.eval()

    kitti_inputs = _branch_inputs(
        batch=batch,
        experts=len(KITTI_EXPERT_ORDER),
        views=views,
        patches=patches,
        d_memory=d_memory,
    )
    eth3d_inputs = _branch_inputs(
        batch=batch,
        experts=len(ETH3D_EXPERT_ORDER),
        views=views,
        patches=patches,
        d_memory=d_memory,
    )

    kitti_out = model(*kitti_inputs, domain="kitti")
    eth3d_out = model(*eth3d_inputs, domain="eth3d")

    report = {
        "status": "pass",
        "version": RELEASE_V11_VERSION,
        "candidate": RELEASE_V11_CANDIDATE,
        "seed": seed,
        "contract": {
            "input": "proposal_pointmaps + proposal_confidences + Dream state/context",
            "output": "final_pointmap + final_confidence + expert_weights",
            "not_claimed": "image-only proposal-free inference",
        },
        "branches": {
            "kitti": _summarize_branch(kitti_out),
            "eth3d": _summarize_branch(eth3d_out),
        },
        "metadata": model.release_metadata(),
    }

    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("runs/release/v11_smoke/smoke_v11_release_model.json"),
        help="where to write the smoke report",
    )
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    report = run_smoke(output=args.output, seed=args.seed)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
