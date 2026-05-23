"""Quick analysis of KITTI eval JSON for A6 evidence summary.

Supports both per-window evaluator output and aggregated sweep/ablation JSON.
"""
import json
import sys
from pathlib import Path

path = sys.argv[1] if len(sys.argv) > 1 else "runs/kitti_200win_a6_evidence.json"
data = json.loads(Path(path).read_text())

if "results" in data:
    results = data["results"]
    print("=== A6 KITTI Sweep / Ablation Summary ===")
    print(f"File: {path}")
    print(f"Configs: {data.get('n_configs', len(results))}")
    print(f"Elapsed: {data.get('sweep_elapsed_s', 0):.1f}s")
    print()

    header = (
        "config",
        "status",
        "backend",
        "win",
        "nsa",
        "slide_fire",
        "branch(c/s/sl)",
        "bank(first/last/max)",
        "drift",
        "route_regret",
        "l2",
    )
    print(
        f"{header[0]:<22} {header[1]:<6} {header[2]:<19} {header[3]:>4} "
        f"{header[4]:<5} {header[5]:>10} {header[6]:>19} "
        f"{header[7]:>20} {header[8]:>8} {header[9]:>12} {header[10]:>8}"
    )
    print("-" * 145)

    ok_count = 0
    nsa_count = 0
    nsa_slide_count = 0
    for name, result in results.items():
        status = result.get("status", "?")
        ok_count += status == "ok"
        metrics = result.get("metrics", {})
        nsa_enabled = bool(result.get("memory_use_nsa", False))
        nsa_count += nsa_enabled
        fire_rate = float(result.get("sliding_branch_fire_rate", 0.0) or 0.0)
        nsa_slide_count += nsa_enabled and fire_rate > 0
        branch = (
            f"{metrics.get('memory_branch_compressed', 0.0):.3f}/"
            f"{metrics.get('memory_branch_selected', 0.0):.3f}/"
            f"{metrics.get('memory_branch_sliding', 0.0):.3f}"
        )
        bank = (
            f"{result.get('bank_occupancy_first', 0):.0f}/"
            f"{result.get('bank_occupancy_last', 0):.0f}/"
            f"{result.get('bank_occupancy_max', 0):.0f}"
        )
        print(
            f"{name:<22} {status:<6} {str(result.get('recurrence_backend', '?')):<19} "
            f"{int(result.get('window_count', 0)):>4} {str(nsa_enabled):<5} "
            f"{fire_rate:>9.1%} {branch:>19} {bank:>20} "
            f"{metrics.get('state_drift_magnitude', 0.0):>8.3f} "
            f"{metrics.get('routing_mean_regret', 0.0):>12.4f} "
            f"{metrics.get('pointmap_l2', 0.0):>8.3f}"
        )

    print()
    print(f"OK configs: {ok_count}/{len(results)}")
    print(f"NSA configs with sliding fire: {nsa_slide_count}/{nsa_count}")
    print("Negative control: non-NSA config keeps sliding branch at 0 by construction.")
    saturated = [
        name
        for name, result in results.items()
        if result.get("bank_occupancy_max") == result.get("bank_occupancy_last") == 256.0
    ]
    print(f"Bank saturation at K=256: {len(saturated)}/{len(results)} configs")
    sys.exit(0)

ws = data["windows"]
print("=== A6 KITTI Evidence Summary ===")
print(f"File: {path}")
print(f"Recurrence: {data.get('recurrence_type', '?')}")
print(f"Backend: {data.get('recurrence_backend', '?')}")
print(f"NSA enabled: {data.get('memory_use_nsa', '?')}")
print(f"Windows: {len(ws)}")
print()

fire = [w["sliding_branch_fired"] for w in ws]
fire_rate = sum(fire) / len(fire) if fire else 0
print(f"Sliding branch fire rate: {sum(fire)}/{len(fire)} = {fire_rate:.1%}")

drifts = [w["latent_drift_proxy"] for w in ws]
print(f"Drift range: [{min(drifts):.3f}, {max(drifts):.3f}]")
print(f"Drift first->last: {drifts[0]:.3f} -> {drifts[-1]:.3f}")

banks = [w["bank_occupancy"] for w in ws]
print(f"Bank occupancy: min={min(banks):.0f}  max={max(banks):.0f}")

etk = [w.get("effective_top_k") for w in ws if w.get("effective_top_k") is not None]
if etk:
    print(f"Effective top-k: min={min(etk)}  max={max(etk)}  avg={sum(etk)/len(etk):.1f}")

branches = [w.get("nsa_branch_mean", {}) for w in ws]
if branches:
    c_avg = sum(b.get("compressed", 0) for b in branches) / len(branches)
    s_avg = sum(b.get("selected", 0) for b in branches) / len(branches)
    sl_avg = sum(b.get("sliding", 0) for b in branches) / len(branches)
    print(f"Branch means: compressed={c_avg:.4f}  selected={s_avg:.4f}  sliding={sl_avg:.4f}")

elapsed = [w.get("elapsed_ms", 0) for w in ws]
print(f"Elapsed per window: avg={sum(elapsed)/len(elapsed):.0f}ms  total={sum(elapsed)/1000:.1f}s")

# First 5 vs last 5 sliding
first5 = fire[:5]
last5 = fire[-5:]
print(f"\nSliding fire (first 5): {first5}")
print(f"Sliding fire (last 5):  {last5}")

# Drift trajectory (sample every 20th)
sample_idx = list(range(0, len(ws), max(1, len(ws)//10)))
print(f"\nDrift trajectory (sampled):")
for i in sample_idx:
    print(f"  win {i:3d}: drift={drifts[i]:.3f}  bank={banks[i]:.0f}  sliding={fire[i]}")
