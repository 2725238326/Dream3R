"""Evaluate Qwen/VLM semantics as a gated Critic prior, not a router.

This diagnostic asks a narrower question than expert routing: can semantic risk
labels improve hard-window verification triggers when they only modulate a
geometry/disagreement proxy? It does not run geometry, does not train a Critic,
and does not treat VLM output as depth/pose/pointmap evidence.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple


SCHEMA_VERSION = "dream3r_vlm_semantic_critic_gate_v1"
DEFAULT_HARD_WINDOW_GAP = 0.05
DEFAULT_SEMANTIC_WEIGHT = 0.5


def _load_json(path: str) -> Dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _feature_dict(feature_order: Sequence[str], vector: Sequence[float]) -> Dict[str, float]:
    if len(feature_order) != len(vector):
        raise ValueError("feature vector length does not match feature_order")
    return {str(key): float(value) for key, value in zip(feature_order, vector)}


def _hard_window_ids(
    metrics: Mapping[str, Mapping[str, float]],
    labels: Mapping[str, int],
    expert_order: Sequence[str],
    window_ids: Sequence[str],
    default_expert: str,
    gap_threshold: float,
) -> Set[str]:
    hard: Set[str] = set()
    for window_id in window_ids:
        oracle_expert = expert_order[int(labels[window_id])]
        default_value = float(metrics[window_id][default_expert])
        oracle_value = float(metrics[window_id][oracle_expert])
        if default_value - oracle_value >= gap_threshold:
            hard.add(window_id)
    return hard


def _precision_recall_f1(predicted: Set[str], target: Set[str]) -> Dict[str, float]:
    tp = len(predicted & target)
    fp = len(predicted - target)
    fn = len(target - predicted)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "true_positive": tp,
        "false_positive": fp,
        "false_negative": fn,
    }


def _geometry_disagreement_scores(
    metrics: Mapping[str, Mapping[str, float]],
    expert_order: Sequence[str],
    window_ids: Sequence[str],
) -> Dict[str, float]:
    scores: Dict[str, float] = {}
    for window_id in window_ids:
        values = [float(metrics[window_id][expert]) for expert in expert_order]
        scores[window_id] = max(values) - min(values)
    return scores


def _semantic_risk_score(features: Mapping[str, float]) -> float:
    risk_values = [
        value for key, value in features.items()
        if key.startswith("risk_")
    ]
    risk = max(risk_values) if risk_values else 0.0
    if features.get("suggest_verify_geometry", 0.0) >= 0.5:
        risk = max(risk, 0.5)
    return float(risk)


def _semantic_scores(
    feature_order: Sequence[str],
    feature_map: Mapping[str, Sequence[float]],
    window_ids: Sequence[str],
) -> Dict[str, float]:
    return {
        window_id: _semantic_risk_score(_feature_dict(feature_order, feature_map[window_id]))
        for window_id in window_ids
    }


def _top_budget(scores: Mapping[str, float], budget: int) -> Set[str]:
    ordered = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    return {window_id for window_id, _ in ordered[:budget]}


def _evaluate_scores(
    name: str,
    scores: Mapping[str, float],
    hard_windows: Set[str],
    trigger_budget: int,
) -> Dict[str, Any]:
    triggered = _top_budget(scores, trigger_budget)
    return {
        "variant": name,
        "trigger_budget": trigger_budget,
        "triggered_windows": sorted(triggered),
        "score_summary": {
            "min": min(scores.values()) if scores else 0.0,
            "max": max(scores.values()) if scores else 0.0,
            "mean": sum(scores.values()) / max(len(scores), 1),
        },
        "hard_window": _precision_recall_f1(triggered, hard_windows),
    }


def _validate_controls(
    window_ids: Sequence[str],
    feature_order: Sequence[str],
    feature_maps: Mapping[str, Mapping[str, Sequence[float]]],
) -> None:
    if not feature_order:
        raise ValueError("VLM cache is missing controls.feature_order")
    for variant_name, feature_map in feature_maps.items():
        missing = [window_id for window_id in window_ids if window_id not in feature_map]
        if missing:
            raise ValueError(f"{variant_name} missing features for {missing[:3]}")
        bad = [
            window_id for window_id in window_ids
            if len(feature_map[window_id]) != len(feature_order)
        ]
        if bad:
            raise ValueError(f"{variant_name} feature length mismatch for {bad[:3]}")


def evaluate_vlm_semantic_critic_gate(
    vlm_cache: str,
    oracle_labels: str,
    output: str,
    hard_window_gap: float = DEFAULT_HARD_WINDOW_GAP,
    semantic_weight: float = DEFAULT_SEMANTIC_WEIGHT,
    trigger_rate: Optional[float] = None,
    window_filter: Optional[List[str]] = None,
) -> Dict[str, Any]:
    cache = _load_json(vlm_cache)
    oracle = _load_json(oracle_labels)
    controls = cache.get("controls") or {}
    feature_order = list(controls.get("feature_order") or cache.get("schema_report", {}).get("feature_order") or [])
    features = cache.get("features") or {}
    shuffled = controls.get("shuffled_features") or {}
    disabled = controls.get("disabled_features") or {}
    metrics = oracle["metrics"]
    labels = oracle["labels"]
    expert_order = list(oracle["expert_order"])
    default_expert = expert_order[0]

    window_ids = sorted(
        window_id for window_id in features
        if window_id in metrics and window_id in labels
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
    _validate_controls(window_ids, feature_order, feature_maps)

    hard_windows = _hard_window_ids(
        metrics, labels, expert_order, window_ids, default_expert, hard_window_gap,
    )
    if trigger_rate is None:
        trigger_budget = max(1, len(hard_windows))
    else:
        trigger_budget = max(1, min(len(window_ids), round(float(trigger_rate) * len(window_ids))))

    geometry_scores = _geometry_disagreement_scores(metrics, expert_order, window_ids)
    semantic_by_variant = {
        name: _semantic_scores(feature_order, feature_map, window_ids)
        for name, feature_map in feature_maps.items()
    }
    variants: Dict[str, Any] = {
        "geometry_only": _evaluate_scores(
            "geometry_only", geometry_scores, hard_windows, trigger_budget,
        ),
    }
    for name, semantic_scores in semantic_by_variant.items():
        variants[f"{name}_qwen_only"] = _evaluate_scores(
            f"{name}_qwen_only", semantic_scores, hard_windows, trigger_budget,
        )
        combined = {
            window_id: geometry_scores[window_id] + semantic_weight * semantic_scores[window_id]
            for window_id in window_ids
        }
        variants[f"{name}_plus_geometry"] = _evaluate_scores(
            f"{name}_plus_geometry", combined, hard_windows, trigger_budget,
        )

    real_plus = variants["vlm_real_plus_geometry"]["hard_window"]["f1"]
    geom_only = variants["geometry_only"]["hard_window"]["f1"]
    shuffle_plus = variants["vlm_shuffle_plus_geometry"]["hard_window"]["f1"]
    disabled_plus = variants["vlm_disabled_plus_geometry"]["hard_window"]["f1"]
    result = {
        "schema_version": SCHEMA_VERSION,
        "metric": oracle.get("summary", {}).get("metric", "abs_rel"),
        "vlm_cache": vlm_cache,
        "oracle_labels": oracle_labels,
        "n_windows": len(window_ids),
        "hard_window_gap": hard_window_gap,
        "hard_window_count": len(hard_windows),
        "trigger_budget": trigger_budget,
        "trigger_rate": trigger_budget / max(len(window_ids), 1),
        "semantic_weight": semantic_weight,
        "expert_order": expert_order,
        "feature_order": feature_order,
        "hard_windows": sorted(hard_windows),
        "variants": variants,
        "diagnostic": {
            "real_plus_beats_geometry_only": real_plus > geom_only,
            "real_plus_beats_shuffle_plus": real_plus > shuffle_plus,
            "real_plus_beats_disabled_plus": real_plus > disabled_plus,
            "promotable": False,
            "promotion_note": (
                "Semantic-assisted Critic diagnostic only. Promotion requires "
                "a real Critic/proposal-disagreement cache and held-out "
                "real > shuffle > disabled controls."
            ),
        },
        "state_causality_controls": {
            "vlm_geometry_access": False,
            "dream3r_core_mutation": False,
            "oracle_used_for": "hard_window_target_and_offline_metric_disagreement_proxy",
            "control_variants": [
                "geometry_only",
                "vlm_real_qwen_only",
                "vlm_shuffle_qwen_only",
                "vlm_disabled_qwen_only",
                "vlm_real_plus_geometry",
                "vlm_shuffle_plus_geometry",
                "vlm_disabled_plus_geometry",
            ],
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
    parser.add_argument("--semantic-weight", type=float, default=DEFAULT_SEMANTIC_WEIGHT)
    parser.add_argument("--trigger-rate", type=float, default=None)
    args = parser.parse_args()
    result = evaluate_vlm_semantic_critic_gate(
        vlm_cache=args.vlm_cache,
        oracle_labels=args.oracle_labels,
        output=args.output,
        hard_window_gap=args.hard_window_gap,
        semantic_weight=args.semantic_weight,
        trigger_rate=args.trigger_rate,
    )
    print(json.dumps({
        "schema_version": result["schema_version"],
        "n_windows": result["n_windows"],
        "hard_window_count": result["hard_window_count"],
        "trigger_budget": result["trigger_budget"],
        "variant_f1": {
            name: data["hard_window"]["f1"]
            for name, data in result["variants"].items()
        },
        "variant_precision": {
            name: data["hard_window"]["precision"]
            for name, data in result["variants"].items()
        },
        "diagnostic": result["diagnostic"],
        "output": args.output,
    }, indent=2))


if __name__ == "__main__":
    main()
