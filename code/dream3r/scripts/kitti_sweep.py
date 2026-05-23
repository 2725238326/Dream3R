"""KITTI sweep: run evaluate_real_sequence over multiple configs,
producing a comparison matrix for v0.5 A6 axis verification.

Configs swept:
  - recurrence: cross_attention | mamba_hybrid
  - max_windows: 10 | 30 | 60
  - disable_nsa: False | True (when False, also probe sliding window utility)

Output: a single JSON aggregating all runs with key fields:
  - nsa_branch_mean per window
  - bank_occupancy trajectory
  - sliding_branch_fired rate
  - effective_top_k stats
  - latent_drift_proxy trajectory
"""
import argparse
import json
import time
from pathlib import Path

try:
    from tqdm.auto import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

from dream3r.evaluate_real_sequence import run_real_sequence_eval


SWEEP_CONFIGS = [
    # (name, recurrence, max_windows, disable_nsa, disable_stable_memory)
    ("cross_attn_10w_nsa",  "cross_attention", 10, False, False),
    ("cross_attn_30w_nsa",  "cross_attention", 30, False, False),
    ("mamba_10w_nsa",       "mamba_hybrid",    10, False, False),
    ("mamba_30w_nsa",       "mamba_hybrid",    30, False, False),
    ("cross_attn_30w_nonsa","cross_attention", 30, True,  False),
    ("mamba_60w_nsa",       "mamba_hybrid",    60, False, False),
]


def _slim_summary(result):
    """Pull out only the diagnostic fields needed for the comparison matrix."""
    windows = result.get("windows", [])
    sliding_fired = [w.get("sliding_branch_fired", False) for w in windows]
    bank_occ = [w.get("bank_occupancy", 0.0) for w in windows]
    drift = [w.get("latent_drift_proxy", 0.0) for w in windows]
    promo = [w.get("stable_promotion_rate", 0.0) for w in windows]
    branches = [w.get("nsa_branch_mean", {}) for w in windows]
    elapsed = [w.get("elapsed_ms", 0.0) for w in windows]

    def _avg(xs):
        xs = [x for x in xs if x is not None]
        return sum(xs) / max(len(xs), 1)

    def _branch_avg(key):
        vals = [b.get(key, 0.0) for b in branches if isinstance(b, dict)]
        return _avg(vals)

    return {
        "recurrence_type": result.get("recurrence_type"),
        "recurrence_backend": result.get("recurrence_backend"),
        "memory_use_nsa": result.get("memory_use_nsa"),
        "enable_stable_memory": result.get("enable_stable_memory"),
        "window_count": result.get("window_count"),
        "metrics": result.get("metrics", {}),
        "sliding_branch_fire_rate": sum(sliding_fired) / max(len(sliding_fired), 1),
        "bank_occupancy_first": bank_occ[0] if bank_occ else 0.0,
        "bank_occupancy_last": bank_occ[-1] if bank_occ else 0.0,
        "bank_occupancy_max": max(bank_occ) if bank_occ else 0.0,
        "latent_drift_first": drift[0] if drift else 0.0,
        "latent_drift_last": drift[-1] if drift else 0.0,
        "stable_promotion_avg": _avg(promo),
        "branch_mean": {
            "compressed": _branch_avg("compressed"),
            "selected": _branch_avg("selected"),
            "sliding": _branch_avg("sliding"),
        },
        "elapsed_ms_avg": _avg(elapsed),
        "elapsed_ms_total": sum(elapsed),
        "first_window_recommended_action": windows[0]["recommended_action"] if windows else None,
        "last_window_recommended_action": windows[-1]["recommended_action"] if windows else None,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", default="/hdd3/kykt26/data")
    parser.add_argument("--output", default="runs/kitti_sweep.json")
    parser.add_argument("--max-sequences", type=int, default=2)
    parser.add_argument("--device", default="auto")
    args = parser.parse_args()

    iterator = SWEEP_CONFIGS
    if HAS_TQDM:
        iterator = tqdm(SWEEP_CONFIGS, desc="KITTI sweep", unit="cfg",
                        dynamic_ncols=True)

    all_results = {}
    started = time.time()

    for cfg in iterator:
        name, recurrence, max_windows, disable_nsa, disable_stable = cfg
        if HAS_TQDM:
            iterator.set_description(f"KITTI sweep [{name}]")

        try:
            result = run_real_sequence_eval(
                data_root=args.data_root,
                max_windows=max_windows,
                max_sequences=args.max_sequences,
                recurrence=recurrence,
                device_name=args.device,
                config_overrides={
                    "memory_use_nsa": not disable_nsa,
                    "enable_stable_memory": not disable_stable,
                },
            )
            slim = _slim_summary(result)
            slim["status"] = "ok"
        except Exception as exc:
            slim = {"status": "error", "error": str(exc)}

        all_results[name] = slim
        if HAS_TQDM:
            sfr = slim.get("sliding_branch_fire_rate", 0.0)
            iterator.set_postfix({
                "sliding": f"{sfr:.2f}",
                "drift": f"{slim.get('latent_drift_last', 0.0):.3f}",
                "ms": f"{slim.get('elapsed_ms_avg', 0.0):.0f}",
            })

    elapsed = time.time() - started
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary = {
        "sweep_elapsed_s": round(elapsed, 1),
        "n_configs": len(SWEEP_CONFIGS),
        "results": all_results,
    }
    output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"\nSweep complete in {elapsed:.1f}s")
    print(f"Output: {output_path}")
    print(f"\n=== Quick summary ===")
    print(f"{'config':<30} {'sliding_fire':>13} {'bank_max':>10} {'drift_last':>12} {'avg_ms':>8}")
    for name, r in all_results.items():
        if r.get("status") == "ok":
            print(f"{name:<30} {r['sliding_branch_fire_rate']:>13.3f} "
                  f"{r['bank_occupancy_max']:>10.2f} {r['latent_drift_last']:>12.3f} "
                  f"{r['elapsed_ms_avg']:>8.0f}")
        else:
            print(f"{name:<30}   ERROR: {r.get('error','')[:50]}")


if __name__ == "__main__":
    main()
