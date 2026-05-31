"""Train Dream3R-PD ProposalSetDecoder from cached proposal banks.

This script is the non-core execution lane for DEC-20260530-015. It reuses
existing SCF caches, keeps fallback-stub proposals out by relying on the cache
guardrail, and compares the proposal-set decoder against per-expert/oracle
diagnostics with the same metrics used by ``train_scf_head``.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Dict, List

import torch
import torch.nn.functional as F

from dream3r.proposal_set_decoder import ProposalSetDecoder
from dream3r.scripts.build_oracle_expert_labels import _pointmap_abs_rel
from dream3r.scripts.train_fusion_head import _abs_rel_loss, _stratified_split
from dream3r.scripts.train_scf_head import (
    _build_state_source,
    _load_caches,
    _per_patch_oracle_abs_rel,
    _scale_drift_proxy,
    _stack,
    _temporal_delta_abs_rel,
)


def _load_state_prior_checkpoint(
    decoder: ProposalSetDecoder,
    checkpoint_path: str,
    device: torch.device,
    freeze: bool = False,
) -> None:
    ckpt = torch.load(checkpoint_path, map_location=device)
    state_dict = ckpt["state_dict"]
    decoder.context_proj.weight.data.copy_(state_dict["context_proj.weight"])
    decoder.context_proj.bias.data.copy_(state_dict["context_proj.bias"])
    decoder.state_prior_mlp[0].weight.data.copy_(state_dict["prior_mlp.0.weight"])
    decoder.state_prior_mlp[0].bias.data.copy_(state_dict["prior_mlp.0.bias"])
    decoder.state_prior_mlp[2].weight.data.copy_(state_dict["prior_mlp.2.weight"])
    decoder.state_prior_mlp[2].bias.data.copy_(state_dict["prior_mlp.2.bias"])

    if freeze:
        for p in decoder.context_proj.parameters():
            p.requires_grad = False
        for p in decoder.state_prior_mlp.parameters():
            p.requires_grad = False
        for p in decoder.state_bias_head.parameters():
            p.requires_grad = False


def _prior_kl_loss(out: Dict[str, torch.Tensor]) -> torch.Tensor:
    weights = out["expert_weights"].clamp_min(1e-8)
    prior = out["state_prior_weights"].view(
        weights.shape[0], weights.shape[1], 1, 1
    ).expand_as(weights).clamp_min(1e-8)
    return F.kl_div(weights.log(), prior.detach(), reduction="batchmean")


def _eval(
    entries: List[Dict],
    idxs: List[int],
    decoder: ProposalSetDecoder,
    state_entries: List[Dict],
    expert_order: List[str],
    device: torch.device,
) -> Dict[str, Dict[str, float]]:
    decoder.eval()
    n_exp = len(expert_order)
    sums: Dict[str, Dict] = {}
    with torch.no_grad():
        for i in idxs:
            e = entries[i]
            dom = e["domain"]
            pms, cfs, mc, cs, gt, mask = _stack(e, expert_order, device, state_entries[i])
            per_expert = [
                _pointmap_abs_rel(pms[:, k], gt, mask, align_scale=True)
                for k in range(n_exp)
            ]
            oracle = min(per_expert)
            patch_oracle = _per_patch_oracle_abs_rel(pms, gt, mask)
            out = decoder(pms, cfs, mc, cs)
            ours = _pointmap_abs_rel(out["final_pointmap"], gt, mask, align_scale=True)
            temporal = _temporal_delta_abs_rel(out["final_pointmap"], gt, mask)
            scale_drift = _scale_drift_proxy(out["final_pointmap"], gt, mask)
            uncertainty = float(out["uncertainty"].mean().item())
            entropy = float(
                -(
                    out["expert_weights"].clamp_min(1e-8)
                    * out["expert_weights"].clamp_min(1e-8).log()
                ).sum(dim=1).mean().item()
            )
            prior_entropy = float(
                -(
                    out["state_prior_weights"].clamp_min(1e-8)
                    * out["state_prior_weights"].clamp_min(1e-8).log()
                ).sum(dim=1).mean().item()
            )

            s = sums.setdefault(dom, {
                "per_expert": [0.0] * n_exp,
                "oracle": 0.0,
                "patch_oracle": 0.0,
                "ours": 0.0,
                "temporal": 0.0,
                "scale_drift": 0.0,
                "uncertainty": 0.0,
                "entropy": 0.0,
                "prior_entropy": 0.0,
                "n": 0,
            })
            for k in range(n_exp):
                s["per_expert"][k] += per_expert[k]
            s["oracle"] += oracle
            s["patch_oracle"] += patch_oracle
            s["ours"] += ours
            s["temporal"] += temporal
            s["scale_drift"] += scale_drift
            s["uncertainty"] += uncertainty
            s["entropy"] += entropy
            s["prior_entropy"] += prior_entropy
            s["n"] += 1

    decoder.train()
    res: Dict[str, Dict[str, float]] = {}
    for dom, s in sums.items():
        n = max(1, s["n"])
        pe = [v / n for v in s["per_expert"]]
        oracle = s["oracle"] / n
        patch_oracle = s["patch_oracle"] / n
        ours = s["ours"] / n
        best_single = min(pe)
        res[dom] = {
            "n": s["n"],
            **{f"B_{expert_order[k]}": round(pe[k], 4) for k in range(n_exp)},
            "B_oracle": round(oracle, 4),
            "B_patch_oracle": round(patch_oracle, 4),
            "Ours_ProposalSetDecoder": round(ours, 4),
            "best_single": round(best_single, 4),
            "rel_imp_vs_best_single_pp": round((best_single - ours) / max(best_single, 1e-9) * 100, 2),
            "oracle_gap_pp": round((ours - oracle) / max(oracle, 1e-9) * 100, 2),
            "patch_oracle_gap_pp": round((ours - patch_oracle) / max(patch_oracle, 1e-9) * 100, 2),
            "temporal_delta_abs_rel": round(s["temporal"] / n, 4),
            "scale_drift_proxy": round(s["scale_drift"] / n, 4),
            "mean_uncertainty": round(s["uncertainty"] / n, 4),
            "mean_weight_entropy": round(s["entropy"] / n, 4),
            "mean_prior_entropy": round(s["prior_entropy"] / n, 4),
        }
    return res


def train(
    cache_paths: List[str],
    output_dir: str,
    seed: int = 7,
    epochs: int = 300,
    lr: float = 1e-3,
    token_dim: int = 64,
    state_dim: int = 64,
    hidden: int = 128,
    num_layers: int = 2,
    num_heads: int = 4,
    use_state_prior: bool = True,
    prior_hidden: int = 128,
    prior_logit_scale: float = 1.0,
    residual_refine_scale: float = 0.0,
    state_prior_checkpoint: str = "",
    freeze_state_prior: bool = False,
    prior_kl_weight: float = 0.0,
    holdout_frac: float = 0.2,
    use_state: bool = True,
    shuffle_state: bool = False,
):
    torch.manual_seed(seed)
    random.seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    entries, d_memory, expert_order = _load_caches(cache_paths)
    state_entries = _build_state_source(entries, seed, shuffle_state)
    n_exp = len(expert_order)
    print(f"loaded {len(entries)} entries, d_memory={d_memory}, experts={expert_order}", flush=True)

    decoder = ProposalSetDecoder(
        n_experts=n_exp,
        d_memory=d_memory,
        token_dim=token_dim,
        state_dim=state_dim,
        hidden=hidden,
        num_layers=num_layers,
        num_heads=num_heads,
        use_state=use_state,
        use_state_prior=use_state_prior,
        prior_hidden=prior_hidden,
        prior_logit_scale=prior_logit_scale,
        residual_refine_scale=residual_refine_scale,
    ).to(device)
    if state_prior_checkpoint:
        _load_state_prior_checkpoint(
            decoder,
            state_prior_checkpoint,
            device,
            freeze=freeze_state_prior,
        )
        print(
            f"loaded state prior checkpoint={state_prior_checkpoint} "
            f"freeze_state_prior={freeze_state_prior} prior_kl_weight={prior_kl_weight}",
            flush=True,
        )
    opt = torch.optim.Adam((p for p in decoder.parameters() if p.requires_grad), lr=lr)

    train_idx, test_idx = _stratified_split(entries, seed, holdout_frac)
    print(
        f"split: train={len(train_idx)} test={len(test_idx)} "
        f"use_state={use_state} shuffle_state={shuffle_state} seed={seed}",
        flush=True,
    )

    losses: List[float] = []
    for epoch in range(epochs):
        order = list(train_idx)
        random.shuffle(order)
        epoch_loss, nb = 0.0, 0
        for i in order:
            pms, cfs, mc, cs, gt, mask = _stack(entries[i], expert_order, device, state_entries[i])
            out = decoder(pms, cfs, mc, cs)
            loss = _abs_rel_loss(out["final_pointmap"], gt, mask, align_scale=True)
            if prior_kl_weight > 0:
                loss = loss + prior_kl_weight * _prior_kl_loss(out)
            opt.zero_grad()
            loss.backward()
            opt.step()
            epoch_loss += float(loss)
            nb += 1
        losses.append(epoch_loss / max(1, nb))
        if (epoch + 1) % 50 == 0 or epoch == 0:
            ev = _eval(entries, test_idx, decoder, state_entries, expert_order, device)
            print(f"epoch {epoch+1:4d}  loss={losses[-1]:.5f}  eval={json.dumps(ev)}", flush=True)

    final_eval = _eval(entries, test_idx, decoder, state_entries, expert_order, device)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    torch.save({
        "decoder_state_dict": decoder.state_dict(),
        "config": {
            "n_experts": n_exp,
            "d_memory": d_memory,
            "token_dim": token_dim,
            "state_dim": state_dim,
            "hidden": hidden,
            "num_layers": num_layers,
            "num_heads": num_heads,
            "use_state": use_state,
            "shuffle_state": shuffle_state,
            "use_state_prior": use_state_prior,
            "prior_hidden": prior_hidden,
            "prior_logit_scale": prior_logit_scale,
            "residual_refine_scale": residual_refine_scale,
            "state_prior_checkpoint": state_prior_checkpoint,
            "freeze_state_prior": freeze_state_prior,
            "prior_kl_weight": prior_kl_weight,
        },
        "seed": seed,
        "final_eval": final_eval,
        "loss_curve": losses,
    }, out_path / "latest.pt")

    result = {
        "seed": seed,
        "epochs": epochs,
        "n_train": len(train_idx),
        "n_test": len(test_idx),
        "expert_order": expert_order,
        "use_state": use_state,
        "shuffle_state": shuffle_state,
        "use_state_prior": use_state_prior,
        "prior_hidden": prior_hidden,
        "prior_logit_scale": prior_logit_scale,
        "residual_refine_scale": residual_refine_scale,
        "state_prior_checkpoint": state_prior_checkpoint,
        "freeze_state_prior": freeze_state_prior,
        "prior_kl_weight": prior_kl_weight,
        "final_train_loss": losses[-1] if losses else None,
        "loss_decrease_pct": (losses[0] - losses[-1]) / max(losses[0], 1e-9) * 100
        if len(losses) >= 2 else 0.0,
        "final_eval": final_eval,
    }
    (out_path / "results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nSaved ProposalSetDecoder + results to {out_path}", flush=True)
    print(json.dumps(result, indent=2), flush=True)
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", nargs="+", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--epochs", type=int, default=300)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--token-dim", type=int, default=64)
    ap.add_argument("--state-dim", type=int, default=64)
    ap.add_argument("--hidden", type=int, default=128)
    ap.add_argument("--num-layers", type=int, default=2)
    ap.add_argument("--num-heads", type=int, default=4)
    ap.add_argument("--disable-state-prior", action="store_true")
    ap.add_argument("--prior-hidden", type=int, default=128)
    ap.add_argument("--prior-logit-scale", type=float, default=1.0)
    ap.add_argument("--residual-refine-scale", type=float, default=0.0)
    ap.add_argument("--state-prior-checkpoint", default="")
    ap.add_argument("--freeze-state-prior", action="store_true")
    ap.add_argument("--prior-kl-weight", type=float, default=0.0)
    ap.add_argument("--holdout-frac", type=float, default=0.2)
    ap.add_argument("--no-state", action="store_true")
    ap.add_argument("--shuffle-state", action="store_true")
    a = ap.parse_args()
    train(
        a.cache,
        a.output_dir,
        seed=a.seed,
        epochs=a.epochs,
        lr=a.lr,
        token_dim=a.token_dim,
        state_dim=a.state_dim,
        hidden=a.hidden,
        num_layers=a.num_layers,
        num_heads=a.num_heads,
        use_state_prior=not a.disable_state_prior,
        prior_hidden=a.prior_hidden,
        prior_logit_scale=a.prior_logit_scale,
        residual_refine_scale=a.residual_refine_scale,
        state_prior_checkpoint=a.state_prior_checkpoint,
        freeze_state_prior=a.freeze_state_prior,
        prior_kl_weight=a.prior_kl_weight,
        holdout_frac=a.holdout_frac,
        use_state=not a.no_state,
        shuffle_state=a.shuffle_state,
    )


if __name__ == "__main__":
    main()
