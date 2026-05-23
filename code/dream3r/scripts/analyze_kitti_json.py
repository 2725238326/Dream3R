"""Quick analysis of KITTI eval JSON for A6 evidence summary."""
import json
import sys
from pathlib import Path

path = sys.argv[1] if len(sys.argv) > 1 else "runs/kitti_200win_a6_evidence.json"
data = json.loads(Path(path).read_text())

ws = data["windows"]
print(f"=== A6 KITTI Evidence Summary ===")
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
print(f"Drift first→last: {drifts[0]:.3f} → {drifts[-1]:.3f}")

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
