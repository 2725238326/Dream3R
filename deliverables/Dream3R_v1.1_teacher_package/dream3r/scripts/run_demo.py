"""Run the Dream3R v1.1.0 release demo.

This is a proposal-bank runtime demo, not an image-only benchmark. It proves
the official v1.1 API can consume proposal tensors plus Dream state/context and
emit the fused 3R pointmap outputs for either release branch.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict

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


DOMAIN_EXPERT_ORDER = {
    "kitti": KITTI_EXPERT_ORDER,
    "eth3d": ETH3D_EXPERT_ORDER,
}

SELECTED_METRICS = {
    "metric": "AbsRel",
    "metric_direction": "lower_is_better",
    "kitti_abs_rel": 0.1448,
    "eth3d_abs_rel": 0.0570,
    "controls": {
        "kitti_state_no_state_shuffle": [0.1448, 0.1553, 0.1521],
        "eth3d_state_no_state_shuffle": [0.0570, 0.0583, 0.0598],
    },
}


def _make_inputs(
    *,
    domain: str,
    seed: int,
    batch: int,
    views: int,
    patches: int,
    d_memory: int,
) -> Dict[str, torch.Tensor]:
    expert_order = DOMAIN_EXPERT_ORDER[domain]
    generator = torch.Generator(device="cpu")
    generator.manual_seed(seed)
    n_experts = len(expert_order)
    return {
        "proposal_pointmaps": torch.randn(
            batch, n_experts, views, patches, 3, generator=generator
        ),
        "proposal_confidences": torch.sigmoid(
            torch.randn(batch, n_experts, views, patches, 1, generator=generator)
        ),
        "memory_context": torch.randn(batch, d_memory, generator=generator),
        "conflict_score": torch.rand(batch, 1, generator=generator),
    }


def _shape(tensor: torch.Tensor) -> list[int]:
    return list(tensor.shape)


@torch.inference_mode()
def run_demo(
    *,
    domain: str,
    output: Path | None = None,
    seed: int = 7,
    batch: int = 2,
    views: int = 2,
    patches: int = 8,
    d_memory: int = 32,
) -> dict[str, Any]:
    domain_key = domain.lower()
    if domain_key not in DOMAIN_EXPERT_ORDER:
        raise ValueError(f"unsupported demo domain: {domain}")

    model = build_dream3r_v11_release()
    model.eval()
    inputs = _make_inputs(
        domain=domain_key,
        seed=seed,
        batch=batch,
        views=views,
        patches=patches,
        d_memory=d_memory,
    )
    output_tensors = model(**inputs, domain=domain_key)
    weights = output_tensors["expert_weights"].detach().cpu()

    report = {
        "status": "pass",
        "demo_mode": "synthetic_proposal_bank_runtime",
        "version": RELEASE_V11_VERSION,
        "candidate": RELEASE_V11_CANDIDATE,
        "official_api": "dream3r.release_v11.build_dream3r_v11_release",
        "domain": domain_key,
        "domain_branch": output_tensors["domain_branch"],
        "seed": seed,
        "input_contract": {
            "proposal_bank_provider": "synthetic fixture for release demo",
            "expert_order": list(DOMAIN_EXPERT_ORDER[domain_key]),
            "proposal_pointmaps_shape": _shape(inputs["proposal_pointmaps"]),
            "proposal_confidences_shape": _shape(inputs["proposal_confidences"]),
            "memory_context_shape": _shape(inputs["memory_context"]),
            "conflict_score_shape": _shape(inputs["conflict_score"]),
        },
        "output_contract": {
            "final_pointmap_shape": _shape(output_tensors["final_pointmap"]),
            "final_confidence_shape": _shape(output_tensors["final_confidence"]),
            "expert_weight_normalization_axis": "expert dimension, per batch/view/patch",
            "expert_weights_shape": _shape(weights),
            "expert_weight_sum_min": float(weights.sum(dim=1).min().item()),
            "expert_weight_sum_max": float(weights.sum(dim=1).max().item()),
        },
        "selected_metrics": SELECTED_METRICS,
        "stable_fallback": {
            "version": "v1.0-rc1",
            "api": "dream3r.release_candidate.build_dream3r_release_candidate",
            "kitti_abs_rel": 0.1448,
            "eth3d_abs_rel": 0.1475,
        },
        "claim_boundary": {
            "safe_claim": "state-conditioned proposal-fusion 3R release package",
            "not_claimed": [
                "proposal-free foundation 3R",
                "image-only inference",
                "Qwen geometry backend",
                "universal SOTA",
            ],
        },
        "v12_experimental_note": (
            "v1.2-exp0 is a core-bridge scaffold only; it is not the official "
            "release until real-cache metrics and state/no-state/shuffle "
            "controls pass."
        ),
        "metadata": model.release_metadata(),
    }

    if output is not None:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--domain", choices=sorted(DOMAIN_EXPERT_ORDER), required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="where to write the demo report; defaults to runs/release/v11_demo/demo_<domain>.json",
    )
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--batch", type=int, default=2)
    parser.add_argument("--views", type=int, default=2)
    parser.add_argument("--patches", type=int, default=8)
    parser.add_argument("--d-memory", type=int, default=32)
    args = parser.parse_args()

    output = args.output or Path(f"runs/release/v11_demo/demo_{args.domain}.json")
    report = run_demo(
        domain=args.domain,
        output=output,
        seed=args.seed,
        batch=args.batch,
        views=args.views,
        patches=args.patches,
        d_memory=args.d_memory,
    )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
