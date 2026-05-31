"""Summarize Dream3R-PD ProposalSetDecoder cached-proposal sweeps."""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path


DOMAINS = ("kitti", "eth3d")
STATE_METRICS = (
    "Ours_ProposalSetDecoder",
    "best_single",
    "rel_imp_vs_best_single_pp",
    "B_oracle",
    "B_patch_oracle",
    "oracle_gap_pp",
    "patch_oracle_gap_pp",
    "temporal_delta_abs_rel",
    "scale_drift_proxy",
)
CONTROL_METRICS = (
    "Ours_ProposalSetDecoder",
    "rel_imp_vs_best_single_pp",
    "oracle_gap_pp",
    "patch_oracle_gap_pp",
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _mean_std(values: list[float]) -> dict[str, float]:
    return {
        "mean": round(statistics.fmean(values), 4),
        "std": round(statistics.stdev(values), 4) if len(values) > 1 else 0.0,
    }


def _load_many(root: Path, prefix: str, seeds: list[int]) -> list[dict]:
    results = []
    for seed in seeds:
        path = root / f"{prefix}_seed_{seed}" / "results.json"
        if path.exists():
            results.append(_load(path))
    return results


def _summarize_results(results: list[dict], metrics: tuple[str, ...]) -> dict:
    return {
        domain: {
            metric: _mean_std(
                [float(item["final_eval"][domain][metric]) for item in results]
            )
            for metric in metrics
        }
        for domain in DOMAINS
    }


def summarize(root: Path, state_seeds: list[int], control_seed: int) -> dict:
    state_results = _load_many(root, "state", state_seeds)
    control_results = {
        "no_state": _load_many(root, "no_state", state_seeds),
        "shuffle_state": _load_many(root, "shuffle_state", state_seeds),
    }
    for seed in state_seeds:
        path = root / f"state_seed_{seed}" / "results.json"
        if path.exists():
            continue

    controls = {}
    for name in ("no_state", "shuffle_state"):
        path = root / f"{name}_seed_{control_seed}" / "results.json"
        if path.exists():
            controls[name] = _load(path)

    summary: dict[str, object] = {
        "root": str(root),
        "state_seeds_requested": state_seeds,
        "state_seeds_found": [int(item["seed"]) for item in state_results],
        "control_seed": control_seed,
        "state": {},
        "controls": {},
        "control_aggregates": {},
    }

    summary["state"] = _summarize_results(state_results, STATE_METRICS)

    controls_summary = summary["controls"]
    assert isinstance(controls_summary, dict)
    for name, item in controls.items():
        controls_summary[name] = {
            domain: {
                metric: float(item["final_eval"][domain][metric])
                for metric in CONTROL_METRICS
            }
            for domain in DOMAINS
        }

    control_aggregates = summary["control_aggregates"]
    assert isinstance(control_aggregates, dict)
    for name, results in control_results.items():
        if results:
            control_aggregates[name] = {
                "seeds_found": [int(item["seed"]) for item in results],
                "domains": _summarize_results(results, CONTROL_METRICS),
            }

    return summary


def _fmt_stat(summary: dict, domain: str, metric: str) -> str:
    stat = summary["state"][domain][metric]
    return f"{stat['mean']:.4f} +/- {stat['std']:.4f}"


def _fmt_control(summary: dict, variant: str, domain: str, metric: str) -> str:
    controls = summary["controls"]
    if variant not in controls:
        return "missing"
    return f"{controls[variant][domain][metric]:.4f}"


def _fmt_control_stat(summary: dict, variant: str, domain: str, metric: str) -> str:
    aggregate = summary["control_aggregates"].get(variant)
    if not aggregate:
        return "missing"
    stat = aggregate["domains"][domain][metric]
    return f"{stat['mean']:.4f} +/- {stat['std']:.4f}"


def render_markdown(summary: dict) -> str:
    seeds = ", ".join(str(seed) for seed in summary["state_seeds_found"])
    lines = [
        "# ProposalSetDecoder Sweep Summary",
        "",
        f"State seeds: {seeds}",
        f"Control seed: {summary['control_seed']}",
        "",
        "## State Seeds",
        "",
        "| domain | ours | best_single | rel_imp_pp | oracle | patch_oracle | oracle_gap_pp | patch_gap_pp | temporal | scale |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for domain in DOMAINS:
        lines.append(
            "| "
            + " | ".join(
                [
                    domain,
                    _fmt_stat(summary, domain, "Ours_ProposalSetDecoder"),
                    _fmt_stat(summary, domain, "best_single"),
                    _fmt_stat(summary, domain, "rel_imp_vs_best_single_pp"),
                    _fmt_stat(summary, domain, "B_oracle"),
                    _fmt_stat(summary, domain, "B_patch_oracle"),
                    _fmt_stat(summary, domain, "oracle_gap_pp"),
                    _fmt_stat(summary, domain, "patch_oracle_gap_pp"),
                    _fmt_stat(summary, domain, "temporal_delta_abs_rel"),
                    _fmt_stat(summary, domain, "scale_drift_proxy"),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Control Aggregates",
            "",
            "| variant | seeds | domain | ours | rel_imp_pp | oracle_gap_pp | patch_gap_pp |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for variant in ("no_state", "shuffle_state"):
        aggregate = summary["control_aggregates"].get(variant)
        seeds = ", ".join(str(seed) for seed in aggregate["seeds_found"]) if aggregate else "missing"
        for domain in DOMAINS:
            lines.append(
                "| "
                + " | ".join(
                    [
                        variant,
                        seeds,
                        domain,
                        _fmt_control_stat(summary, variant, domain, "Ours_ProposalSetDecoder"),
                        _fmt_control_stat(summary, variant, domain, "rel_imp_vs_best_single_pp"),
                        _fmt_control_stat(summary, variant, domain, "oracle_gap_pp"),
                        _fmt_control_stat(summary, variant, domain, "patch_oracle_gap_pp"),
                    ]
                )
                + " |"
            )

    lines.extend(
        [
            "",
            "## Seed-7 Controls",
            "",
            "| variant | domain | ours | rel_imp_pp | oracle_gap_pp | patch_gap_pp |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for variant in ("no_state", "shuffle_state"):
        for domain in DOMAINS:
            lines.append(
                "| "
                + " | ".join(
                    [
                        variant,
                        domain,
                        _fmt_control(summary, variant, domain, "Ours_ProposalSetDecoder"),
                        _fmt_control(summary, variant, domain, "rel_imp_vs_best_single_pp"),
                        _fmt_control(summary, variant, domain, "oracle_gap_pp"),
                        _fmt_control(summary, variant, domain, "patch_oracle_gap_pp"),
                    ]
                )
                + " |"
            )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Positive claim is narrow: KITTI improves over best single by about 3 pp relative across state seeds.",
            "- ETH3D remains negative versus best single, so the current decoder does not support a broad cross-domain claim.",
            "- Correct-state and shuffled-state are effectively tied in this v0 decoder; the KITTI gain is proposal mixing, not proven Dream-state causality.",
            "- No-state is unstable across seeds, so seed-7 no-state improvement should be treated as an outlier.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("runs/stage6_fusion/proposal_set_decoder_sweep"),
    )
    parser.add_argument("--state-seeds", type=int, nargs="+", default=[7, 11, 13])
    parser.add_argument("--control-seed", type=int, default=7)
    args = parser.parse_args()

    summary = summarize(args.root, args.state_seeds, args.control_seed)
    args.root.mkdir(parents=True, exist_ok=True)
    (args.root / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    markdown = render_markdown(summary)
    (args.root / "summary.md").write_text(markdown, encoding="utf-8")
    print(markdown)


if __name__ == "__main__":
    main()
