"""Temporary debug script for router conf-gate training."""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import torch

from dream3r.scripts.train_router_only import train_router_only

tmp = Path(tempfile.mkdtemp())
regime_path = tmp / "r.json"
oracle_path = tmp / "o.json"
out_dir = tmp / "router"

regime_path.write_text(json.dumps({
    "regime_order": ["a", "b", "c", "d", "e", "f"],
    "labels": {
        "dense_a": [0.02, 0.12, 0.05, 0.05, 0.7, 0.06],
        "dense_b": [0.02, 0.12, 0.05, 0.05, 0.68, 0.08],
        "sparse_a": [0.02, 0.15, 0.05, 0.68, 0.05, 0.05],
        "sparse_b": [0.02, 0.15, 0.05, 0.66, 0.07, 0.05],
    },
}))
oracle_path.write_text(json.dumps({
    "expert_order": ["fast3r", "mast3r"],
    "labels": {"dense_a": 0, "dense_b": 0, "sparse_a": 1, "sparse_b": 1},
    "metrics": {
        "dense_a": {"fast3r": 0.12, "mast3r": 0.30},
        "dense_b": {"fast3r": 0.13, "mast3r": 0.28},
        "sparse_a": {"fast3r": 0.32, "mast3r": 0.14},
        "sparse_b": {"fast3r": 0.30, "mast3r": 0.15},
    },
    "summary": {"metric": "scale_aligned_abs_rel"},
}))

s = train_router_only(
    str(regime_path), str(oracle_path), str(out_dir),
    epochs=500, lr=0.05, batch_size=4, d_routing=16,
)
print(json.dumps(s, indent=2))

ckpt = torch.load(out_dir / "latest.pt", map_location="cpu", weights_only=False)
sd = ckpt["router_state_dict"]
print("W norm:", sd["confidence_gate.weight"].norm().item())
print("b norm:", sd["confidence_gate.bias"].norm().item())
print("regime_encoder.0.weight norm:", sd["regime_encoder.0.weight"].norm().item())
print("regime_encoder.2.weight norm:", sd["regime_encoder.2.weight"].norm().item())
print("routing_head.weight norm:", sd["routing_head.weight"].norm().item())

# Project W and b onto (R_y - R_alt) direction
R = sd["routing_head.weight"]  # (n_classes=2, d_routing=16)
R_diff = R[0] - R[1]  # (d_routing,)
R_diff_norm = R_diff.norm().item()
W = sd["confidence_gate.weight"].squeeze(-1)  # (d_routing,)
b = sd["confidence_gate.bias"]  # (d_routing,)
proj_W = (W @ R_diff).item() / max(R_diff_norm, 1e-8)
proj_b = (b @ R_diff).item() / max(R_diff_norm, 1e-8)
proj_W_orth_norm = (W - (W @ R_diff / R_diff_norm**2) * R_diff).norm().item()
proj_b_orth_norm = (b - (b @ R_diff / R_diff_norm**2) * R_diff).norm().item()
print(f"||R_y - R_alt|| = {R_diff_norm:.4f}")
print(f"proj_W on (R_y - R_alt) = {proj_W:.4f} (positive ⇒ W aligned with y-alt direction)")
print(f"proj_b on (R_y - R_alt) = {proj_b:.4f}")
print(f"||W_perp|| = {proj_W_orth_norm:.4f} (orthogonal component norm)")
print(f"||b_perp|| = {proj_b_orth_norm:.4f}")
# What conf_mod looks like at eval, projected onto (R_y - R_alt):
for c in [0.42, 0.45, 0.47]:
    cm = W * c + b
    proj_cm = (cm @ R_diff).item() / max(R_diff_norm, 1e-8)
    print(f"  conf={c:.2f}: proj(conf_mod) on (R_y-R_alt) = {proj_cm:.4f}")

# Simulate inference
from dream3r.composer_experts import ExpertRegistry
from dream3r.composer_experts.fast3r_adapter import Fast3RAdapter
from dream3r.composer_experts.mast3r_adapter import MASt3RAdapter
from dream3r.modules import ComposerRouter

reg = ExpertRegistry()
reg.register_class("fast3r", Fast3RAdapter)
reg.register_class("mast3r", MASt3RAdapter)
router = ComposerRouter(n_regimes=6, d_routing=16, cost_alpha=0.0, expert_registry=reg)
router.load_state_dict(sd)
router.eval()

regime_data = json.loads(regime_path.read_text())
oracle_data = json.loads(oracle_path.read_text())
seqs = sorted(oracle_data["labels"])
x = torch.tensor([regime_data["labels"][q] for q in seqs], dtype=torch.float32)

with torch.no_grad():
    logits_n = router(x)["routing_logits"]
    pred_n = logits_n.argmax(dim=-1)
    conf_h = torch.full((4, 1), float(s["conf_high_val"]))
    conf_l = torch.full((4, 1), float(s["conf_low_val"]))
    logits_h = router(x, critic_confidence=conf_h)["routing_logits"]
    logits_l = router(x, critic_confidence=conf_l)["routing_logits"]
    pred_h = logits_h.argmax(dim=-1)
    pred_l = logits_l.argmax(dim=-1)

    print("seqs:", seqs)
    print("conf_high:", s["conf_high_val"], "conf_low:", s["conf_low_val"])
    print("pred no-conf:", pred_n.tolist())
    print("pred conf-high:", pred_h.tolist())
    print("pred conf-low:", pred_l.tolist())
    print("logits no-conf:", logits_n)
    print("logits conf-high:", logits_h)
    print("logits conf-low:", logits_l)

    # Probe: what does router predict at conf=0.0 vs conf=1.0?
    conf_0 = torch.zeros(4, 1)
    conf_1 = torch.ones(4, 1)
    pred_0 = router(x, critic_confidence=conf_0)["routing_logits"].argmax(dim=-1)
    pred_1 = router(x, critic_confidence=conf_1)["routing_logits"].argmax(dim=-1)
    print("pred conf=0:", pred_0.tolist())
    print("pred conf=1:", pred_1.tolist())
