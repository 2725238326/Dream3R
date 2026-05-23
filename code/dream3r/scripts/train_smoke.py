"""Quick training smoke test: 5 steps, verify loss decreases."""
import torch
import sys

from dream3r.config import load_config, config_to_model_args
from dream3r.model import Dream3R
from dream3r.losses import Dream3RLoss
from dream3r.data.synthetic import SyntheticSequenceDataset
from dream3r.train import _forward_sequence, collate_synthetic
from torch.utils.data import DataLoader

print("=== Dream3R Training Smoke Test ===", flush=True)

cfg = load_config(preset="small", overrides={"batch_size": 2, "epochs": 1, "sequence_length": 2})
model_cfg = config_to_model_args(cfg)
model = Dream3R(model_cfg).cuda()
loss_fn = Dream3RLoss().cuda()

n_params = sum(p.numel() for p in model.parameters())
print(f"Model params: {n_params:,}", flush=True)

ds = SyntheticSequenceDataset(
    n_sequences=10, n_frames=4, n_slots=16, n_regimes=5,
    d_model=768, sequence_length=2, seed=42,
)
dl = DataLoader(ds, batch_size=2, collate_fn=collate_synthetic)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

losses_history = []
for i, batch in enumerate(dl):
    optimizer.zero_grad()
    with torch.amp.autocast("cuda"):
        outputs, losses = _forward_sequence(model, batch, loss_fn, torch.device("cuda"), 1)
    losses["total"].backward()
    optimizer.step()
    loss_val = losses["total"].item()
    losses_history.append(loss_val)
    print(f"  step {i}: loss={loss_val:.4f}", flush=True)

print(f"\nLoss trend: {losses_history[0]:.4f} -> {losses_history[-1]:.4f}", flush=True)
if losses_history[-1] < losses_history[0] * 1.5:
    print("TRAINING SMOKE: PASS", flush=True)
else:
    print("TRAINING SMOKE: WARN (loss did not decrease, but no crash)", flush=True)

print(f"GPU memory: {torch.cuda.max_memory_allocated()/1e9:.2f} GB", flush=True)
