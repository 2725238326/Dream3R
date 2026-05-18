"""
Extended smoke test for Dream3R v0.3.

Validates:
  1. v0.3 forward + backward + bus signals (SpatialMemory + ComposerRouter)
  2. v0.1 backward compatibility
  3. AnchorBank lifecycle (write/read/prune/quarantine)
  4. NSA attention correctness
  5. ComposerRouter expert dispatch
  6. Multi-window streaming with state carry-over
  7. New loss terms (retrieval, routing, drift_consistency)

Usage: python -m dream3r.smoke_test
"""

import torch
import sys
import traceback


def section(name: str):
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")


def smoke_test_v03():
    from dream3r.model import build_dream3r
    from dream3r.losses import Dream3RLoss

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    errors = []

    # ----------------------------------------------------------------
    section("1. v0.3 Forward Pass")
    # ----------------------------------------------------------------
    model = build_dream3r("small").to(device)
    loss_fn = Dream3RLoss().to(device)

    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Parameters: {total:,} total, {trainable:,} trainable")
    print(f"Version: {model.version}")

    B, N, P, D = 2, 4, 196, 768
    x = torch.randn(B, N, P, D, device=device)
    regime = torch.softmax(torch.randn(B, 5, device=device), dim=-1)

    out1 = model(x, regime, timestep=0)
    print(f"Output keys: {len(out1)} entries")
    for k, v in sorted(out1.items()):
        if isinstance(v, torch.Tensor):
            print(f"  {k}: {list(v.shape)}")

    assert "nsa_branch_weights" in out1, "Missing NSA branch weights"
    assert "bank_occupancy" in out1, "Missing bank occupancy"
    assert "selected_expert" in out1, "Missing selected expert"
    print("  v0.3-specific outputs present: OK")

    # ----------------------------------------------------------------
    section("2. Bus Contract Log")
    # ----------------------------------------------------------------
    log = out1["contract_log"]
    print(f"Bus contract log: {len(log)} entries")
    readers = set(e["consumer"] for e in log)
    signals = set(e["signal"] for e in log)
    print(f"  Consumers: {readers}")
    print(f"  Signals read: {signals}")
    assert "memory" in readers, "Memory not reading from bus"
    assert "critic" in readers, "Critic not reading from bus"

    # ----------------------------------------------------------------
    section("3. Loss + Backward")
    # ----------------------------------------------------------------
    targets = {
        "pointmap": torch.randn(B, N, P, 3, device=device),
        "pointmap_mask": torch.ones(B, N, P, device=device),
        "conflict_label": torch.randint(0, 2, (B,), device=device).float(),
        "repair_label": torch.randint(0, 6, (B,), device=device),
        "region_label": torch.randint(0, 3, (B, 16), device=device),
        "pointmap_change": torch.rand(B, device=device),
    }
    losses = loss_fn(out1, targets)
    print("Losses:")
    for k, v in losses.items():
        if isinstance(v, torch.Tensor):
            print(f"  {k}: {v.item():.4f}")

    assert "retrieval" in losses, "Missing retrieval loss"
    assert "routing" in losses, "Missing routing loss"
    print("  v0.3 loss terms present: OK")

    losses["total"].backward()
    bad = sum(1 for p in model.parameters()
              if p.requires_grad and p.grad is not None and torch.isnan(p.grad).any())
    print(f"  NaN gradients: {bad}")
    if bad > 0:
        errors.append("NaN gradients in v0.3 backward")

    # ----------------------------------------------------------------
    section("4. Multi-Window Streaming")
    # ----------------------------------------------------------------
    model.zero_grad()

    if "latent_state_tokens" in out1:
        prev_mem = out1["latent_state_tokens"].detach()
    else:
        prev_mem = out1["latent_state"].detach()
    prev_slots = out1["object_track_set"].detach()

    out2 = model(x, regime,
                 prev_memory_state=prev_mem,
                 prev_object_slots=prev_slots,
                 timestep=1)

    state_key = "latent_state_tokens" if "latent_state_tokens" in out1 else "latent_state"
    same = torch.allclose(out1[state_key], out2[state_key])
    print(f"  States differ across windows: {not same}")
    if same:
        errors.append("States identical across windows")

    # ----------------------------------------------------------------
    section("5. NSA Branch Weights")
    # ----------------------------------------------------------------
    bw = out1["nsa_branch_weights"].mean(dim=(0, 1))
    branch_names = ["compressed", "selected", "sliding"]
    for i, name in enumerate(branch_names):
        print(f"  {name}: {bw[i].item():.3f}")
    assert bw.sum().item() > 0.99, "Branch weights don't sum to 1"
    print("  Branch weights sum check: OK")

    # ----------------------------------------------------------------
    section("6. AnchorBank Lifecycle")
    # ----------------------------------------------------------------
    from dream3r.anchor_bank import AnchorBank

    bank = AnchorBank(capacity=16, d_key=32, d_value=32)
    bank.reset(batch_size=1)

    keys = torch.randn(1, 5, 32)
    values = torch.randn(1, 5, 32)
    wr = bank.write(keys, values)
    print(f"  Write: {wr.n_written} written, {wr.n_suppressed} suppressed")
    assert wr.n_written == 5

    queries = torch.randn(1, 3, 32)
    rr = bank.read(queries, top_k=3)
    print(f"  Read: values shape {list(rr.values.shape)}, scores shape {list(rr.scores.shape)}")
    assert rr.values.shape == (1, 3, 3, 32)

    wr2 = bank.write(
        torch.randn(1, 4, 32), torch.randn(1, 4, 32),
        bus_dynamic_ratio=torch.tensor([[0.9]]),
    )
    print(f"  Gated write (high dynamic): {wr2.n_written} written, {wr2.n_suppressed} suppressed")
    assert wr2.n_suppressed > 0, "Dynamic gating didn't suppress"

    bank.quarantine(torch.tensor([[0, 1]]))
    assert bank.quarantined[0, 0].item() and bank.quarantined[0, 1].item()
    print("  Quarantine: OK")

    bank.unquarantine(torch.tensor([[0]]))
    assert not bank.quarantined[0, 0].item()
    print("  Unquarantine: OK")

    for _ in range(12):
        bank.write(torch.randn(1, 2, 32), torch.randn(1, 2, 32))
        bank.tick()
    pr = bank.prune(keep_ratio=0.5)
    print(f"  Prune: {pr.n_pruned} pruned, lowest utility {pr.lowest_utility:.3f}")
    print("  AnchorBank lifecycle: OK")

    # ----------------------------------------------------------------
    section("7. ComposerRouter Expert Dispatch")
    # ----------------------------------------------------------------
    from dream3r.composer_experts import ExpertRegistry

    reg = ExpertRegistry()
    reg.register_all_defaults()
    print(f"  Registered experts: {reg.names}")
    assert len(reg.names) == 7

    cap_matrix = reg.capability_matrix()
    print(f"  Capability matrix: {list(cap_matrix.shape)}")
    assert cap_matrix.shape == (7, 5)

    latency = reg.latency_vector()
    print(f"  Latency vector: {[f'{l:.0f}ms' for l in latency.tolist()]}")

    adapter = reg.get("fast3r")
    dummy_img = torch.randn(1, 2, 3, 224, 224)
    expert_out = adapter.forward(dummy_img)
    print(f"  Fast3R output: pointmap {list(expert_out.pointmap.shape)}, "
          f"conf {list(expert_out.confidence.shape)}")

    # ----------------------------------------------------------------
    section("8. v0.1 Backward Compatibility")
    # ----------------------------------------------------------------
    from dream3r.model import CONFIGS
    model_v01 = build_dream3r("small_v01").to(device)
    out_v01 = model_v01(x, regime, timestep=0)
    print(f"  v0.1 forward: {len(out_v01)} output keys")
    assert "latent_state" in out_v01
    assert "capability_match" in out_v01
    print("  v0.1 compatibility: OK")

    # ----------------------------------------------------------------
    section("9. Synthetic Dataset")
    # ----------------------------------------------------------------
    from dream3r.data.synthetic import SyntheticSequenceDataset

    ds = SyntheticSequenceDataset(n_sequences=10, n_frames=4, d_model=768, seed=42)
    sample = ds[0]
    print(f"  Sample keys: {list(sample.keys())}")
    print(f"  features: {list(sample['features'].shape)}")
    print(f"  pointmap_gt: {list(sample['pointmap_gt'].shape)}")
    print(f"  regime: {list(sample['regime'].shape)}")
    print(f"  Deterministic: {torch.allclose(ds[0]['features'], ds[0]['features'])}")

    # ----------------------------------------------------------------
    section("RESULT")
    # ----------------------------------------------------------------
    if errors:
        print(f"\nFAILED with {len(errors)} error(s):")
        for e in errors:
            print(f"  - {e}")
        return False

    print("\n=== ALL SMOKE TESTS PASSED ===")
    return True


if __name__ == "__main__":
    try:
        ok = smoke_test_v03()
        sys.exit(0 if ok else 1)
    except Exception as e:
        print(f"\n=== SMOKE TEST CRASHED: {e} ===")
        traceback.print_exc()
        sys.exit(1)
