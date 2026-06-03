"""Evaluate cached VLM semantic features as Dream3R controller signals.

This dry-run does not train a router and does not run geometry. It tests whether
the cached semantic labels create a measurable control signal surface by
comparing three deterministic policies:

- real VLM features;
- shuffled VLM features;
- disabled zero features.

The output is a Router/Critic-ready diagnostic, not a promotion claim.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple


DEFAULT_ROUTE_THRESHOLD = 0.5
DEFAULT_HARD_WINDOW_GAP = 0.05


def _load_json(path: str) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _feature_dict(feature_order: Sequence[str], vector: Sequence[float]) -> Dict[str, float]:
    if len(feature_order) != len(vector):
        raise ValueError("feature vector length does not match feature_order")
    return {str(key): float(value) for key, value in zip(feature_order, vector)}


def _choose_expert(features: Mapping[str, float], expert_order: Sequence[str]) -> str:
    """Small deterministic semantic controller policy.

    The policy is intentionally simple so it is auditable:
    dynamic scenes prefer the dynamic/memory-friendly expert if available;
    low-texture/repeated/reflection/occlusion risk prefers MASt3R if available;
    large-baseline or road-like scenes prefer Fast3R if available;
    otherwise it falls back to the first expert.
    """
    experts = list(expert_order)
    if not experts:
        raise ValueError("expert_order is empty")
    if features.get("risk_dynamic", 0.0) >= DEFAULT_ROUTE_THRESHOLD and "spann3r" in experts:
        return "spann3r"
    if (
        max(
            features.get("risk_low_texture", 0.0),
            features.get("risk_repeated_structure", 0.0),
            features.get("risk_reflection", 0.0),
            features.get("risk_occlusion", 0.0),
        ) >= DEFAULT_ROUTE_THRESHOLD
        and "mast3r" in experts
    ):
        return "mast3r"
    if (
        features.get("risk_large_baseline", 0.0) >= DEFAULT_ROUTE_THRESHOLD
        or features.get("scene_road", 0.0) >= 0.5
    ) and "fast3r" in experts:
        return "fast3r"
    return experts[0]


def _trigger_scores(features: Mapping[str, float]) -> Tuple[bool, bool]:
    verify = bool(
        features.get("suggest_verify_geometry", 0.0) >= 0.5
        or max(
            features.get("risk_dynamic", 0.0),
            features.get("risk_low_texture", 0.0),
            features.get("risk_reflection", 0.0),
            features.get("risk_occlusion", 0.0),
            features.get("risk_large_baseline", 0.0),
            features.get("risk_scale_drift", 0.0),
            features.get("risk_repeated_structure", 0.0),
        ) >= DEFAULT_ROUTE_THRESHOLD
    )
    expensive = bool(
        features.get("suggest_expensive_teacher", 0.0) >= 0.5
        or features.get("risk_large_baseline", 0.0) >= 0.7
        or features.get("risk_reflection", 0.0) >= 0.7
    )
    return verify, expensive


def _mean_metric(metrics: Mapping[str, Mapping[str, float]], routes: Mapping[str, str]) -> float:
    values = [float(metrics[window_id][expert]) for window_id, expert in routes.items()]
    return sum(values) / max(len(values), 1)


def _oracle_routes(oracle_data: Mapping[str, Any], window_ids: Sequence[str]) -> Dict[str, str]:
    expert_order = list(oracle_data["expert_order"])
    return {
        window_id: expert_order[int(oracle_data["labels"][window_id])]
        for window_id in window_ids
    }


def _hard_window_ids(
    metrics: Mapping[str, Mapping[str, float]],
    oracle_routes: Mapping[str, str],
    default_expert: str,
    gap_threshold: float,
) -> set[str]:
    hard = set()
    for window_id, oracle_expert in oracle_routes.items():
        default_value = float(metrics[window_id][default_expert])
        oracle_value = float(metrics[window_id][oracle_expert])
        if default_value - oracle_value >= gap_threshold:
            hard.add(window_id)
    return hard


def _precision_recall(predicted: set[str], target: set[str]) -> Dict[str, float]:
    tp = len(predicted & target)
    fp = len(predicted - target)
    fn = len(target - predicted)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    return {
        "precision": precision,
        "recall": recall,
        "true_positive": tp,
        "false_positive": fp,
        "false_negative": fn,
    }


def _evaluate_variant(
    name: str,
    feature_order: Sequence[str],
    feature_map: Mapping[str, Sequence[float]],
    window_ids: Sequence[str],
    expert_order: Sequence[str],
    metrics: Mapping[str, Mapping[str, float]],
    oracle_mean: float,
    hard_windows: set[str],
) -> Dict[str, Any]:
    routes: Dict[str, str] = {}
    verify_triggers: set[str] = set()
    expensive_triggers: set[str] = set()
    for window_id in window_ids:
        features = _feature_dict(feature_order, feature_map[window_id])
        routes[window_id] = _choose_expert(features, expert_order)
        verify, expensive = _trigger_scores(features)
        if verify:
            verify_triggers.add(window_id)
        if expensive:
            expensive_triggers.add(window_id)
    mean_metric = _mean_metric(metrics, routes)
    return {
        "variant": name,
        "routes": routes,
        "mean_metric": mean_metric,
        "route_regret_vs_oracle": mean_metric - oracle_mean,
        "expert_counts": {
            expert: sum(1 for value in routes.values() if value == expert)
            for expert in expert_order
        },
        "verify_geometry_trigger_rate": len(verify_triggers) / max(len(window_ids), 1),
        "expensive_teacher_trigger_rate": len(expensive_triggers) / max(len(window_ids), 1),
        "verify_geometry_hard_window": _precision_recall(verify_triggers, hard_windows),
        "triggered_verify_geometry": sorted(verify_triggers),
        "triggered_expensive_teacher": sorted(expensive_triggers),
    }


def evaluate_vlm_controller_dryrun(
    vlm_cache: str,
    oracle_labels: str,
    output: str,
    hard_window_gap: float = DEFAULT_HARD_WINDOW_GAP,
    window_filter: Optional[List[str]] = None,
) -> Dict[str, Any]:
    cache = _load_json(vlm_cache)
    oracle_data = _load_json(oracle_labels)
    feature_order = list(cache.get("controls", {}).get("feature_order") or cache.get("schema_report", {}).get("feature_order") or [])
    if not feature_order:
        raise ValueError("VLM cache is missing controls.feature_order")
    controls = cache.get("controls") or {}
    features = cache.get("features") or {}
    shuffled = controls.get("shuffled_features") or {}
    disabled = controls.get("disabled_features") or {}
    metrics = oracle_data["metrics"]
    expert_order = list(oracle_data["expert_order"])

    window_ids = sorted(
        window_id for window_id in features
        if window_id in metrics and window_id in oracle_data["labels"]
    )
    if window_filter is not None:
        allowed = set(window_filter)
        window_ids = [window_id for window_id in window_ids if window_id in allowed]
    if not window_ids:
        raise ValueError("no overlapping VLM cache / oracle windows")
    missing_controls = [
        window_id for window_id in window_ids
        if window_id not in shuffled or window_id not in disabled
    ]
    if missing_controls:
        raise ValueError(f"missing shuffled/disabled controls for {missing_controls[:3]}")

    oracle_routes = _oracle_routes(oracle_data, window_ids)
    oracle_mean = _mean_metric(metrics, oracle_routes)
    default_expert = expert_order[0]
    hard_windows = _hard_window_ids(
        metrics, oracle_routes, default_expert, hard_window_gap,
    )
    variants = {
        "vlm_real": _evaluate_variant(
            "vlm_real", feature_order, features, window_ids, expert_order,
            metrics, oracle_mean, hard_windows,
        ),
        "vlm_shuffle": _evaluate_variant(
            "vlm_shuffle", feature_order, shuffled, window_ids, expert_order,
            metrics, oracle_mean, hard_windows,
        ),
        "vlm_disabled": _evaluate_variant(
            "vlm_disabled", feature_order, disabled, window_ids, expert_order,
            metrics, oracle_mean, hard_windows,
        ),
    }
    result = {
        "schema_version": "dream3r_vlm_controller_dryrun_v1",
        "metric": oracle_data.get("summary", {}).get("metric", "abs_rel"),
        "vlm_cache": vlm_cache,
        "oracle_labels": oracle_labels,
        "n_windows": len(window_ids),
        "expert_order": expert_order,
        "feature_order": feature_order,
        "hard_window_gap": hard_window_gap,
        "hard_windows": sorted(hard_windows),
        "oracle_mean": oracle_mean,
        "variants": variants,
        "diagnostic": {
            "real_beats_disabled": (
                variants["vlm_real"]["mean_metric"]
                < variants["vlm_disabled"]["mean_metric"]
            ),
            "real_beats_shuffle": (
                variants["vlm_real"]["mean_metric"]
                < variants["vlm_shuffle"]["mean_metric"]
            ),
            "promotable": False,
            "promotion_note": (
                "Dry-run only. Promotion requires real Qwen labels and held-out "
                "Router/Critic evaluation with shuffled and disabled controls worse."
            ),
        },
    }
    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vlm-cache", required=True)
    parser.add_argument("--oracle-labels", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--hard-window-gap", type=float, default=DEFAULT_HARD_WINDOW_GAP)
    args = parser.parse_args()
    result = evaluate_vlm_controller_dryrun(
        vlm_cache=args.vlm_cache,
        oracle_labels=args.oracle_labels,
        output=args.output,
        hard_window_gap=args.hard_window_gap,
    )
    print(json.dumps({
        "schema_version": result["schema_version"],
        "n_windows": result["n_windows"],
        "oracle_mean": result["oracle_mean"],
        "variant_metrics": {
            name: data["mean_metric"]
            for name, data in result["variants"].items()
        },
        "diagnostic": result["diagnostic"],
        "output": args.output,
    }, indent=2))


if __name__ == "__main__":
    main()
