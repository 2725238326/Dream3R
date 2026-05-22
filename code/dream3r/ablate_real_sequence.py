"""Real-data ablation runner for Dream3R memory and recurrence variants."""

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List, Optional

from dream3r.evaluate_real_sequence import run_real_sequence_eval


REAL_SEQUENCE_VARIANTS = [
    {
        "name": "baseline_cross_attention",
        "state_recurrence_type": "cross_attention",
        "memory_use_nsa": True,
        "enable_stable_memory": True,
    },
    {
        "name": "mamba_hybrid",
        "state_recurrence_type": "mamba_hybrid",
        "memory_use_nsa": True,
        "enable_stable_memory": True,
    },
    {
        "name": "no_nsa",
        "state_recurrence_type": "mamba_hybrid",
        "memory_use_nsa": False,
        "enable_stable_memory": True,
    },
    {
        "name": "no_stable_memory",
        "state_recurrence_type": "mamba_hybrid",
        "memory_use_nsa": True,
        "enable_stable_memory": False,
    },
]


def _metric(result: Dict[str, Any], key: str) -> float:
    value = result.get("metrics", {}).get(key, 0.0)
    return float(value) if isinstance(value, (int, float)) else 0.0


def _window_metric(result: Dict[str, Any], key: str) -> float:
    values = [
        float(window[key])
        for window in result.get("windows", [])
        if isinstance(window.get(key), (int, float))
    ]
    return mean(values) if values else 0.0


def _branch_mean(result: Dict[str, Any], key: str) -> float:
    values = []
    for window in result.get("windows", []):
        branches = window.get("nsa_branch_mean", {})
        value = branches.get(key)
        if isinstance(value, (int, float)):
            values.append(float(value))
    return mean(values) if values else 0.0


def _summarize(result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "recurrence_backend": result.get("recurrence_backend", ""),
        "recurrence_backend_error": result.get("recurrence_backend_error", ""),
        "window_count": result.get("window_count", 0),
        "pointmap_l2": round(_metric(result, "pointmap_l2"), 6),
        "depth_rmse": round(_metric(result, "depth_rmse"), 6),
        "elapsed_ms_mean": round(_window_metric(result, "elapsed_ms"), 3),
        "bank_occupancy_mean": round(_window_metric(result, "bank_occupancy"), 6),
        "latent_drift_proxy_mean": round(_window_metric(result, "latent_drift_proxy"), 6),
        "stable_promotion_rate_mean": round(_window_metric(result, "stable_promotion_rate"), 6),
        "selected_anchor_3d_distance_mean": round(_window_metric(result, "selected_anchor_3d_distance"), 6),
        "conflict_score_mean": round(_window_metric(result, "conflict_score_mean"), 6),
        "nsa_branch_mean": {
            "compressed": round(_branch_mean(result, "compressed"), 6),
            "selected": round(_branch_mean(result, "selected"), 6),
            "sliding": round(_branch_mean(result, "sliding"), 6),
        },
    }


def run_real_sequence_ablation(
    data_root: str = "/hdd3/kykt26/data",
    max_windows: int = 2,
    max_sequences: int = 1,
    device_name: str = "auto",
    variants: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    variants = variants or REAL_SEQUENCE_VARIANTS
    result = {
        "dataset": "kitti_rectified",
        "data_root": data_root,
        "max_windows": max_windows,
        "max_sequences": max_sequences,
        "requested_device": device_name,
        "evidence_boundary": (
            "real-data integration ablation scaffold; not trained reconstruction quality"
        ),
        "variants": {},
    }

    for variant in variants:
        run = run_real_sequence_eval(
            data_root=data_root,
            max_windows=max_windows,
            max_sequences=max_sequences,
            recurrence=variant["state_recurrence_type"],
            device_name=device_name,
            config_overrides={
                "memory_use_nsa": variant["memory_use_nsa"],
                "enable_stable_memory": variant["enable_stable_memory"],
            },
        )
        result["variants"][variant["name"]] = {
            "config": {
                "state_recurrence_type": variant["state_recurrence_type"],
                "memory_use_nsa": variant["memory_use_nsa"],
                "enable_stable_memory": variant["enable_stable_memory"],
            },
            "summary": _summarize(run),
            "run": run,
        }

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", default="/hdd3/kykt26/data")
    parser.add_argument("--max-windows", type=int, default=2)
    parser.add_argument("--max-sequences", type=int, default=1)
    parser.add_argument("--device", default="auto")
    parser.add_argument(
        "--output",
        default="demo_artifacts/real_sequence/real_ablation.json",
    )
    args = parser.parse_args()

    result = run_real_sequence_ablation(
        data_root=args.data_root,
        max_windows=args.max_windows,
        max_sequences=args.max_sequences,
        device_name=args.device,
    )
    text = json.dumps(result, indent=2)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
