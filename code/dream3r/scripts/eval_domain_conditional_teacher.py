"""Evaluate a domain-conditional Dream3R teacher policy.

The policy is intentionally narrow:

* KITTI stays on the official v1.0-rc1 bounded StatePrior path.
* ETH3D uses the VGGT-Omega-expanded state-controlled path.

This script is read-only. It combines existing result artifacts and reports
domain-wise controls; it does not train or promote a new official release by
itself.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict


def _read_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def _metric(result: dict[str, Any], domain: str, key: str) -> float:
    return float(result["final_eval"][domain][key])


def evaluate_domain_conditional(
    bounded_state: str | Path,
    bounded_shuffle: str | Path,
    vggt_state: str | Path,
    vggt_no_state: str | Path,
    vggt_shuffle: str | Path,
    output: str | Path | None = None,
) -> dict[str, Any]:
    bounded_state_json = _read_json(bounded_state)
    bounded_shuffle_json = _read_json(bounded_shuffle)
    vggt_state_json = _read_json(vggt_state)
    vggt_no_state_json = _read_json(vggt_no_state)
    vggt_shuffle_json = _read_json(vggt_shuffle)

    kitti_metric = _metric(bounded_state_json, "kitti", "Ours_ProposalSetDecoder")
    kitti_shuffle = _metric(bounded_shuffle_json, "kitti", "Ours_ProposalSetDecoder")
    eth3d_metric = _metric(vggt_state_json, "eth3d", "Ours_SCF")
    eth3d_no_state = _metric(vggt_no_state_json, "eth3d", "Ours_SCF")
    eth3d_shuffle = _metric(vggt_shuffle_json, "eth3d", "Ours_SCF")

    rc_eth3d = _metric(bounded_state_json, "eth3d", "Ours_ProposalSetDecoder")
    rc_kitti = kitti_metric

    result = {
        "candidate": "domain_conditional_vggt_teacher",
        "status": "experimental_not_official_release",
        "policy": {
            "kitti": "Dream3R v1.0-rc1 bounded StatePrior + residual",
            "eth3d": "VGGT-Omega-expanded SCF correct-state",
        },
        "metrics": {
            "kitti_abs_rel": round(kitti_metric, 4),
            "eth3d_abs_rel": round(eth3d_metric, 4),
            "rc_kitti_abs_rel": round(rc_kitti, 4),
            "rc_eth3d_abs_rel": round(rc_eth3d, 4),
            "eth3d_abs_rel_gain_vs_rc": round(rc_eth3d - eth3d_metric, 4),
            "eth3d_relative_gain_vs_rc_pct": round(
                (rc_eth3d - eth3d_metric) / max(rc_eth3d, 1e-9) * 100,
                2,
            ),
        },
        "controls": {
            "kitti_bounded_state_beats_shuffle": kitti_metric < kitti_shuffle,
            "kitti_bounded_shuffle_abs_rel": round(kitti_shuffle, 4),
            "eth3d_vggt_state_beats_no_state": eth3d_metric < eth3d_no_state,
            "eth3d_vggt_state_beats_shuffle": eth3d_metric < eth3d_shuffle,
            "eth3d_vggt_no_state_abs_rel": round(eth3d_no_state, 4),
            "eth3d_vggt_shuffle_abs_rel": round(eth3d_shuffle, 4),
        },
        "artifact_boundary": {
            "kitti_source": str(bounded_state),
            "kitti_shuffle_source": str(bounded_shuffle),
            "eth3d_source": str(vggt_state),
            "eth3d_no_state_source": str(vggt_no_state),
            "eth3d_shuffle_source": str(vggt_shuffle),
            "warning": (
                "KITTI and ETH3D metrics are domain-wise artifacts, not a "
                "single pooled benchmark. This candidate must not replace "
                "v1.0-rc1 without a unified cache/control rerun."
            ),
        },
        "passes_domainwise_controls": bool(
            kitti_metric < kitti_shuffle
            and eth3d_metric < eth3d_no_state
            and eth3d_metric < eth3d_shuffle
            and eth3d_metric < rc_eth3d
        ),
        "promotable_to_official": False,
        "promotion_blocker": (
            "domain-wise artifacts are not a unified benchmark/control rerun; "
            "rerun a single declared domain-conditional gate before replacing v1.0-rc1"
        ),
    }

    if output is not None:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bounded-state",
        default="runs/stage6_fusion/bounded_refine_sweep/frozen_prior_state_seed_7/results.json",
    )
    parser.add_argument(
        "--bounded-shuffle",
        default="runs/stage6_fusion/bounded_refine_sweep/frozen_prior_shuffle_state_seed_7/results.json",
    )
    parser.add_argument(
        "--vggt-state",
        default="runs/v22_admission/vggt_omega_cache_gate/scf_state_seed7_results.json",
    )
    parser.add_argument(
        "--vggt-no-state",
        default="runs/v22_admission/vggt_omega_cache_gate/scf_no_state_seed7_results.json",
    )
    parser.add_argument(
        "--vggt-shuffle",
        default="runs/v22_admission/vggt_omega_cache_gate/scf_shuffle_state_seed7_results.json",
    )
    parser.add_argument(
        "--output",
        default="runs/v22_admission/domain_conditional_teacher/domain_conditional_candidate.json",
    )
    args = parser.parse_args()

    result = evaluate_domain_conditional(
        bounded_state=args.bounded_state,
        bounded_shuffle=args.bounded_shuffle,
        vggt_state=args.vggt_state,
        vggt_no_state=args.vggt_no_state,
        vggt_shuffle=args.vggt_shuffle,
        output=args.output,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
