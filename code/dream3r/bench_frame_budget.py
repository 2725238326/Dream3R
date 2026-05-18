"""
Frame budget profiler for Dream3R.

Measures per-module latency and reports p50/p95/p99 statistics.
Also tracks architecture metrics such as bank utilization, sparse branch
usage, routing entropy, geometry retrieval distance, state drift, and peak
memory usage.
Uses CUDA events for GPU timing, time.perf_counter for CPU.

Usage:
    python -m dream3r.bench_frame_budget --preset small --n-windows 50
"""

import argparse
import time
from typing import Dict, List

import torch
import torch.nn.functional as F
import numpy as np


SPECIAL_RESULT_KEYS = {"total", "architecture", "memory"}


def _summarize(values: List[float]) -> float:
    return float(np.array(values).mean()) if values else 0.0


def _append_metric(metrics: Dict[str, List[float]], name: str, value):
    if isinstance(value, torch.Tensor):
        value = value.detach().float()
        if value.numel() == 0:
            return
        finite = value[torch.isfinite(value)]
        if finite.numel() == 0:
            return
        value = finite.mean().item()
    metrics.setdefault(name, []).append(float(value))


def collect_architecture_metrics(out: Dict[str, torch.Tensor],
                                 metrics: Dict[str, List[float]]):
    """Collect scalar architecture metrics from one forward output."""
    if "bank_occupancy" in out:
        _append_metric(metrics, "bank_occupancy", out["bank_occupancy"])

    if "nsa_branch_weights" in out:
        branch = out["nsa_branch_weights"].detach().float().mean(dim=(0, 1))
        names = ["branch_compressed", "branch_selected", "branch_sliding"]
        for i, name in enumerate(names[:branch.numel()]):
            _append_metric(metrics, name, branch[i])
        entropy = -(branch * branch.clamp_min(1e-8).log()).sum()
        _append_metric(metrics, "branch_entropy", entropy)

    log = out.get("memory_retrieval_log", {})
    if isinstance(log, dict):
        if "selected_3d_distances" in log:
            _append_metric(metrics, "selected_anchor_3d_distance", log["selected_3d_distances"])
        if "geometry_bias_applied" in log:
            _append_metric(metrics, "geometry_bias_applied", log["geometry_bias_applied"])
        if "branch_active_mask" in log:
            active = log["branch_active_mask"].detach().float().sum(dim=-1)
            _append_metric(metrics, "active_branch_count", active)

    if "latent_drift_proxy" in out:
        _append_metric(metrics, "state_drift_magnitude", out["latent_drift_proxy"].abs())

    if "routing_logits" in out:
        probs = F.softmax(out["routing_logits"].detach().float(), dim=-1)
        avg_probs = probs.mean(dim=0)
        entropy = -(avg_probs * avg_probs.clamp_min(1e-8).log()).sum()
        _append_metric(metrics, "routing_entropy", entropy)


def profile_model(model, x, regime, n_windows: int = 50,
                  device: torch.device = torch.device("cpu"),
                  warmup: int = 5) -> Dict[str, Dict[str, float]]:
    """
    Profile Dream3R forward pass timing.

    Returns dict of module_name -> {p50, p95, p99, mean, min, max} in ms.
    """
    model.eval()
    model.profile = True

    use_cuda = device.type == "cuda"
    all_timings: Dict[str, List[float]] = {}
    arch_metrics: Dict[str, List[float]] = {}
    total_times: List[float] = []

    with torch.no_grad():
        prev_mem = None
        prev_slots = None
        if use_cuda:
            torch.cuda.reset_peak_memory_stats(device)

        for i in range(warmup + n_windows):
            if use_cuda:
                torch.cuda.synchronize()

            t0 = time.perf_counter()

            if use_cuda:
                start_event = torch.cuda.Event(enable_timing=True)
                end_event = torch.cuda.Event(enable_timing=True)
                start_event.record()

            out = model(x, regime,
                        prev_memory_state=prev_mem,
                        prev_object_slots=prev_slots,
                        timestep=i)

            if use_cuda:
                end_event.record()
                torch.cuda.synchronize()
                total_ms = start_event.elapsed_time(end_event)
            else:
                total_ms = (time.perf_counter() - t0) * 1000

            if i >= warmup:
                total_times.append(total_ms)
                if "timings" in out:
                    for k, v in out["timings"].items():
                        if k not in all_timings:
                            all_timings[k] = []
                        all_timings[k].append(v)
                collect_architecture_metrics(out, arch_metrics)

            if "latent_state_tokens" in out:
                prev_mem = out["latent_state_tokens"].detach()
            elif "latent_state" in out:
                prev_mem = out["latent_state"].detach()
            if "object_track_set" in out:
                prev_slots = out["object_track_set"].detach()

    model.profile = False

    results = {}
    for name, times in all_timings.items():
        arr = np.array(times)
        results[name] = {
            "p50": float(np.percentile(arr, 50)),
            "p95": float(np.percentile(arr, 95)),
            "p99": float(np.percentile(arr, 99)),
            "mean": float(arr.mean()),
            "min": float(arr.min()),
            "max": float(arr.max()),
        }

    total_arr = np.array(total_times)
    results["total"] = {
        "p50": float(np.percentile(total_arr, 50)),
        "p95": float(np.percentile(total_arr, 95)),
        "p99": float(np.percentile(total_arr, 99)),
        "mean": float(total_arr.mean()),
        "min": float(total_arr.min()),
        "max": float(total_arr.max()),
    }
    results["architecture"] = {
        name: _summarize(values)
        for name, values in sorted(arch_metrics.items())
    }
    if use_cuda:
        results["memory"] = {
            "peak_allocated_mb": float(torch.cuda.max_memory_allocated(device) / 1024 ** 2),
            "peak_reserved_mb": float(torch.cuda.max_memory_reserved(device) / 1024 ** 2),
        }
    else:
        results["memory"] = {
            "peak_allocated_mb": 0.0,
            "peak_reserved_mb": 0.0,
        }

    return results


def print_report(results: Dict[str, Dict[str, float]], target_ms: float = 50.0):
    print(f"\n{'Module':<20} {'p50':>8} {'p95':>8} {'p99':>8} {'mean':>8} {'budget':>8}")
    print("-" * 72)

    total = results.get("total", {})
    for name, stats in sorted(results.items()):
        if name in SPECIAL_RESULT_KEYS:
            continue
        pct = stats["mean"] / total.get("mean", 1) * 100
        print(f"  {name:<18} {stats['p50']:>7.2f} {stats['p95']:>7.2f} "
              f"{stats['p99']:>7.2f} {stats['mean']:>7.2f} {pct:>6.1f}%")

    print("-" * 72)
    if total:
        status = "OK" if total["p95"] <= target_ms else "OVER"
        print(f"  {'TOTAL':<18} {total['p50']:>7.2f} {total['p95']:>7.2f} "
              f"{total['p99']:>7.2f} {total['mean']:>7.2f}  [{status}]")
        print(f"\n  Target: {target_ms:.0f} ms/frame | p95: {total['p95']:.2f} ms")

    arch = results.get("architecture", {})
    if arch:
        print("\nArchitecture metrics:")
        for name, value in sorted(arch.items()):
            print(f"  {name:<30} {value:>10.4f}")

    memory = results.get("memory", {})
    if memory:
        print("\nMemory:")
        print(f"  peak_allocated_mb             {memory.get('peak_allocated_mb', 0.0):>10.2f}")
        print(f"  peak_reserved_mb              {memory.get('peak_reserved_mb', 0.0):>10.2f}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preset", default="small")
    parser.add_argument("--n-windows", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--target-ms", type=float, default=50.0)
    args = parser.parse_args()

    from dream3r.model import build_dream3r

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Profiling Dream3R [{args.preset}] on {device}")

    model = build_dream3r(args.preset).to(device)
    model.profile = True

    B, N, P, D = args.batch_size, 4, 196, 768
    x = torch.randn(B, N, P, D, device=device)
    regime = torch.softmax(torch.randn(B, 5, device=device), dim=-1)

    n_params = sum(p.numel() for p in model.parameters())
    print(f"  Parameters: {n_params:,}")

    results = profile_model(model, x, regime, n_windows=args.n_windows,
                            device=device)
    print_report(results, target_ms=args.target_ms)


if __name__ == "__main__":
    main()
