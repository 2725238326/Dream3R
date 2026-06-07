"""Unified gate for the domain-conditional Dream3R candidate.

This gate is stricter than ``eval_domain_conditional_teacher``. It asks whether
the experimental policy can replace v1.0-rc1:

* KITTI uses the bounded v1.0-rc1 ProposalSetDecoder path.
* ETH3D uses the VGGT-Omega-expanded SCF path.
* both domains must have state/no-state/shuffle controls.

The script is read-only and reports blockers instead of silently promoting.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Optional


def _read_json(path: str | Path | None) -> Optional[dict[str, Any]]:
    if not path:
        return None
    p = Path(path)
    if not p.exists() and p.name == "results.json":
        flat_mirror = p.parent.parent / f"{p.parent.name}_results.json"
        if flat_mirror.exists():
            p = flat_mirror
    if not p.exists():
        return None
    with p.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def _metric(result: dict[str, Any], domain: str, key: str) -> float:
    return float(result["final_eval"][domain][key])


def _maybe_metric(result: Optional[dict[str, Any]], domain: str, key: str) -> Optional[float]:
    if result is None:
        return None
    return _metric(result, domain, key)


def evaluate_unified_domain_conditional_gate(
    *,
    kitti_state: str | Path,
    kitti_shuffle: str | Path,
    eth3d_state: str | Path,
    eth3d_no_state: str | Path,
    eth3d_shuffle: str | Path,
    kitti_no_state: str | Path | None = None,
    output: str | Path | None = None,
) -> dict[str, Any]:
    k_state = _read_json(kitti_state)
    k_no = _read_json(kitti_no_state)
    k_shuffle = _read_json(kitti_shuffle)
    e_state = _read_json(eth3d_state)
    e_no = _read_json(eth3d_no_state)
    e_shuffle = _read_json(eth3d_shuffle)

    missing = []
    for label, value in {
        "kitti_state": k_state,
        "kitti_no_state": k_no,
        "kitti_shuffle": k_shuffle,
        "eth3d_state": e_state,
        "eth3d_no_state": e_no,
        "eth3d_shuffle": e_shuffle,
    }.items():
        if value is None:
            missing.append(label)

    k_state_metric = _maybe_metric(k_state, "kitti", "Ours_ProposalSetDecoder")
    k_no_metric = _maybe_metric(k_no, "kitti", "Ours_ProposalSetDecoder")
    k_shuffle_metric = _maybe_metric(k_shuffle, "kitti", "Ours_ProposalSetDecoder")
    e_state_metric = _maybe_metric(e_state, "eth3d", "Ours_SCF")
    e_no_metric = _maybe_metric(e_no, "eth3d", "Ours_SCF")
    e_shuffle_metric = _maybe_metric(e_shuffle, "eth3d", "Ours_SCF")

    controls = {
        "kitti_state_beats_no_state": (
            k_state_metric is not None
            and k_no_metric is not None
            and k_state_metric < k_no_metric
        ),
        "kitti_state_beats_shuffle": (
            k_state_metric is not None
            and k_shuffle_metric is not None
            and k_state_metric < k_shuffle_metric
        ),
        "eth3d_state_beats_no_state": (
            e_state_metric is not None
            and e_no_metric is not None
            and e_state_metric < e_no_metric
        ),
        "eth3d_state_beats_shuffle": (
            e_state_metric is not None
            and e_shuffle_metric is not None
            and e_state_metric < e_shuffle_metric
        ),
    }
    blockers = list(missing)
    for name, passed in controls.items():
        if not passed:
            blockers.append(name)

    result = {
        "candidate": "unified_domain_conditional_vggt_teacher",
        "status": "pass" if not blockers else "blocked",
        "policy": {
            "kitti": "Dream3R v1.0-rc1 bounded StatePrior + residual",
            "eth3d": "VGGT-Omega-expanded SCF correct-state",
        },
        "metrics": {
            "kitti_state_abs_rel": k_state_metric,
            "kitti_no_state_abs_rel": k_no_metric,
            "kitti_shuffle_abs_rel": k_shuffle_metric,
            "eth3d_state_abs_rel": e_state_metric,
            "eth3d_no_state_abs_rel": e_no_metric,
            "eth3d_shuffle_abs_rel": e_shuffle_metric,
        },
        "controls": controls,
        "promotion_blockers": blockers,
        "promotable_to_official": not blockers,
        "artifact_paths": {
            "kitti_state": str(kitti_state),
            "kitti_no_state": str(kitti_no_state) if kitti_no_state else "",
            "kitti_shuffle": str(kitti_shuffle),
            "eth3d_state": str(eth3d_state),
            "eth3d_no_state": str(eth3d_no_state),
            "eth3d_shuffle": str(eth3d_shuffle),
        },
    }

    if output is not None:
        out = Path(output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--kitti-state",
        default="runs/stage6_fusion/bounded_refine_sweep/frozen_prior_state_seed_7/results.json",
    )
    parser.add_argument("--kitti-no-state", default="")
    parser.add_argument(
        "--kitti-shuffle",
        default="runs/stage6_fusion/bounded_refine_sweep/frozen_prior_shuffle_state_seed_7/results.json",
    )
    parser.add_argument(
        "--eth3d-state",
        default="runs/v22_admission/vggt_omega_cache_gate/scf_state_seed7/results.json",
    )
    parser.add_argument(
        "--eth3d-no-state",
        default="runs/v22_admission/vggt_omega_cache_gate/scf_no_state_seed7/results.json",
    )
    parser.add_argument(
        "--eth3d-shuffle",
        default="runs/v22_admission/vggt_omega_cache_gate/scf_shuffle_state_seed7/results.json",
    )
    parser.add_argument(
        "--output",
        default="runs/v22_admission/domain_conditional_teacher/unified_gate_candidate.json",
    )
    args = parser.parse_args()

    result = evaluate_unified_domain_conditional_gate(
        kitti_state=args.kitti_state,
        kitti_no_state=args.kitti_no_state,
        kitti_shuffle=args.kitti_shuffle,
        eth3d_state=args.eth3d_state,
        eth3d_no_state=args.eth3d_no_state,
        eth3d_shuffle=args.eth3d_shuffle,
        output=args.output,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
