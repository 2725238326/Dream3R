"""Held-out calibration gate for cached VLM semantic controller signals.

This evaluator treats Qwen/VLM outputs as an offline semantic signal only. It
does not run geometry, does not train Dream3R modules, and does not touch the
Router/Critic path. Oracle labels are used only inside each train fold to fit a
small nearest-centroid controller, then real/shuffle/disabled VLM feature
variants are evaluated on held-out windows.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple


SCHEMA_VERSION = "dream3r_vlm_calibrated_controller_v1"
DEFAULT_FOLDS = 5


def _load_json(path: str) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _mean_metric(metrics: Mapping[str, Mapping[str, float]], routes: Mapping[str, str]) -> float:
    values = [float(metrics[window_id][expert]) for window_id, expert in routes.items()]
    return sum(values) / max(len(values), 1)


def _oracle_routes(oracle_data: Mapping[str, Any], window_ids: Sequence[str]) -> Dict[str, str]:
    expert_order = list(oracle_data["expert_order"])
    return {
        window_id: expert_order[int(oracle_data["labels"][window_id])]
        for window_id in window_ids
    }


def _window_group(window_id: str) -> str:
    """Return a causality-preserving split group for a window id.

    KITTI sequence ids use ``*_sync_02`` camera suffixes. Grouping by drive
    prevents neighboring windows from the same drive leaking between train and
    held-out folds. Non-KITTI slash paths fall back to their first two path
    components, otherwise the full id is its own group.
    """
    match = re.match(r"^(.+?_drive_\d{4})_sync(?:_\d+)?(?:/.*)?$", window_id)
    if match:
        return match.group(1)
    parts = window_id.split("/")
    if len(parts) >= 2:
        return "/".join(parts[:2])
    return window_id


def _build_folds(window_ids: Sequence[str]) -> Tuple[str, List[Dict[str, List[str]]]]:
    groups: Dict[str, List[str]] = {}
    for window_id in window_ids:
        groups.setdefault(_window_group(window_id), []).append(window_id)
    sorted_groups = sorted(groups)
    if len(sorted_groups) >= 2:
        folds = []
        for group in sorted_groups:
            test_ids = sorted(groups[group])
            train_ids = [
                window_id
                for other_group in sorted_groups
                if other_group != group
                for window_id in sorted(groups[other_group])
            ]
            folds.append({
                "fold_id": group,
                "heldout_groups": [group],
                "train_window_ids": train_ids,
                "test_window_ids": test_ids,
            })
        return "leave_one_group_out", folds

    n_folds = min(DEFAULT_FOLDS, max(1, len(window_ids)))
    folds = []
    sorted_ids = sorted(window_ids)
    for fold_idx in range(n_folds):
        test_ids = [window_id for idx, window_id in enumerate(sorted_ids) if idx % n_folds == fold_idx]
        train_ids = [window_id for window_id in sorted_ids if window_id not in set(test_ids)]
        folds.append({
            "fold_id": f"kfold_{fold_idx}",
            "heldout_groups": ["fallback_single_group"],
            "train_window_ids": train_ids,
            "test_window_ids": test_ids,
        })
    return "deterministic_kfold_fallback", folds


def _centroids(
    feature_map: Mapping[str, Sequence[float]],
    train_ids: Sequence[str],
    oracle_routes: Mapping[str, str],
    expert_order: Sequence[str],
) -> Dict[str, List[float]]:
    sums: Dict[str, List[float]] = {}
    counts: Counter[str] = Counter()
    for window_id in train_ids:
        expert = oracle_routes[window_id]
        vector = [float(value) for value in feature_map[window_id]]
        if expert not in sums:
            sums[expert] = [0.0] * len(vector)
        if len(sums[expert]) != len(vector):
            raise ValueError("feature vector length changed inside a variant")
        for idx, value in enumerate(vector):
            sums[expert][idx] += value
        counts[expert] += 1
    return {
        expert: [value / counts[expert] for value in sums[expert]]
        for expert in expert_order
        if counts[expert] > 0
    }


def _distance(left: Sequence[float], right: Sequence[float]) -> float:
    return math.sqrt(sum((float(a) - float(b)) ** 2 for a, b in zip(left, right)))


def _predict(
    vector: Sequence[float],
    centroids: Mapping[str, Sequence[float]],
    expert_order: Sequence[str],
) -> str:
    if not centroids:
        return expert_order[0]
    best_expert = None
    best_distance = None
    for expert in expert_order:
        if expert not in centroids:
            continue
        distance = _distance(vector, centroids[expert])
        if best_distance is None or distance < best_distance:
            best_expert = expert
            best_distance = distance
    return str(best_expert or expert_order[0])


def _evaluate_variant(
    name: str,
    feature_map: Mapping[str, Sequence[float]],
    folds: Sequence[Mapping[str, List[str]]],
    oracle_routes: Mapping[str, str],
    expert_order: Sequence[str],
    metrics: Mapping[str, Mapping[str, float]],
    oracle_mean: float,
) -> Dict[str, Any]:
    routes: Dict[str, str] = {}
    fold_reports: List[Dict[str, Any]] = []
    for fold in folds:
        train_ids = list(fold["train_window_ids"])
        test_ids = list(fold["test_window_ids"])
        fitted = _centroids(feature_map, train_ids, oracle_routes, expert_order)
        fold_routes = {
            window_id: _predict(feature_map[window_id], fitted, expert_order)
            for window_id in test_ids
        }
        routes.update(fold_routes)
        fold_reports.append({
            "fold_id": fold["fold_id"],
            "heldout_groups": fold["heldout_groups"],
            "n_train": len(train_ids),
            "n_test": len(test_ids),
            "train_expert_counts": {
                expert: sum(1 for window_id in train_ids if oracle_routes[window_id] == expert)
                for expert in expert_order
            },
            "test_mean_metric": _mean_metric(metrics, fold_routes),
            "routes": fold_routes,
        })
    mean_metric = _mean_metric(metrics, routes)
    return {
        "variant": name,
        "mean_metric": mean_metric,
        "route_regret_vs_oracle": mean_metric - oracle_mean,
        "expert_counts": {
            expert: sum(1 for route in routes.values() if route == expert)
            for expert in expert_order
        },
        "route_accuracy_vs_oracle": (
            sum(1 for window_id, route in routes.items() if route == oracle_routes[window_id])
            / max(len(routes), 1)
        ),
        "routes": dict(sorted(routes.items())),
        "folds": fold_reports,
    }


def _validate_feature_controls(
    window_ids: Sequence[str],
    feature_order: Sequence[str],
    feature_maps: Mapping[str, Mapping[str, Sequence[float]]],
) -> None:
    if not feature_order:
        raise ValueError("VLM cache is missing controls.feature_order")
    for variant_name, feature_map in feature_maps.items():
        missing = [window_id for window_id in window_ids if window_id not in feature_map]
        if missing:
            raise ValueError(f"{variant_name} is missing features for {missing[:3]}")
        bad_length = [
            window_id for window_id in window_ids
            if len(feature_map[window_id]) != len(feature_order)
        ]
        if bad_length:
            raise ValueError(f"{variant_name} feature length mismatch for {bad_length[:3]}")


def evaluate_vlm_calibrated_controller(
    vlm_cache: str,
    oracle_labels: str,
    output: str,
    window_filter: Optional[List[str]] = None,
) -> Dict[str, Any]:
    cache = _load_json(vlm_cache)
    oracle_data = _load_json(oracle_labels)
    controls = cache.get("controls") or {}
    feature_order = list(controls.get("feature_order") or cache.get("schema_report", {}).get("feature_order") or [])
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

    feature_maps = {
        "vlm_real": features,
        "vlm_shuffle": shuffled,
        "vlm_disabled": disabled,
    }
    _validate_feature_controls(window_ids, feature_order, feature_maps)

    split_strategy, folds = _build_folds(window_ids)
    oracle = _oracle_routes(oracle_data, window_ids)
    oracle_mean = _mean_metric(metrics, oracle)
    default_routes = {window_id: expert_order[0] for window_id in window_ids}
    default_mean = _mean_metric(metrics, default_routes)
    variants = {
        name: _evaluate_variant(
            name, feature_map, folds, oracle, expert_order, metrics, oracle_mean,
        )
        for name, feature_map in feature_maps.items()
    }
    result = {
        "schema_version": SCHEMA_VERSION,
        "metric": oracle_data.get("summary", {}).get("metric", "abs_rel"),
        "vlm_cache": vlm_cache,
        "oracle_labels": oracle_labels,
        "n_windows": len(window_ids),
        "n_groups": len({_window_group(window_id) for window_id in window_ids}),
        "split_strategy": split_strategy,
        "expert_order": expert_order,
        "feature_order": feature_order,
        "oracle_mean": oracle_mean,
        "default_expert": expert_order[0],
        "default_expert_mean": default_mean,
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
            "real_gap_vs_disabled": (
                variants["vlm_disabled"]["mean_metric"]
                - variants["vlm_real"]["mean_metric"]
            ),
            "real_gap_vs_shuffle": (
                variants["vlm_shuffle"]["mean_metric"]
                - variants["vlm_real"]["mean_metric"]
            ),
            "promotable": False,
            "promotion_note": (
                "Held-out semantic-only diagnostic. Promotion still requires a "
                "pre-registered threshold, broader split coverage, and Router/Critic "
                "state-causality evaluation with shuffle/disabled controls."
            ),
        },
        "state_causality_controls": {
            "oracle_used_for": "train_fold_centroid_calibration_only",
            "heldout_oracle_leakage": False,
            "vlm_geometry_access": False,
            "dream3r_core_mutation": False,
            "control_variants": ["vlm_real", "vlm_shuffle", "vlm_disabled"],
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
    args = parser.parse_args()
    result = evaluate_vlm_calibrated_controller(
        vlm_cache=args.vlm_cache,
        oracle_labels=args.oracle_labels,
        output=args.output,
    )
    print(json.dumps({
        "schema_version": result["schema_version"],
        "n_windows": result["n_windows"],
        "n_groups": result["n_groups"],
        "split_strategy": result["split_strategy"],
        "oracle_mean": result["oracle_mean"],
        "default_expert_mean": result["default_expert_mean"],
        "variant_metrics": {
            name: data["mean_metric"]
            for name, data in result["variants"].items()
        },
        "diagnostic": result["diagnostic"],
        "output": args.output,
    }, indent=2))


if __name__ == "__main__":
    main()
