# Dream3R Initial Recurrence Ablation Baseline

Status: synthetic smoke ablation, not a real-data quality result.

Date: 2026-05-10

## Purpose

This is the first lightweight ablation table for the memory and recurrence path. It compares:

- `baseline_cross_attention`: current CUT3R-style `StateTokenRecurrence` with NSA and stable memory enabled.
- `mamba_hybrid`: `MambaHybridRecurrence` using server `mamba_ssm`, with NSA and stable memory enabled.
- `no_nsa`: Mamba recurrence with NSA fusion bypassed.
- `no_stable_memory`: Mamba recurrence with AnchorBank write/recall/promote disabled.

The goal is to prove the ablation machinery and collect initial integration signals. It does not claim reconstruction quality superiority.

## Command

Run on server:

```bash
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -m dream3r.ablate_recurrence --windows 3 --seeds 33 34 35
```

## Summary

| Variant | Backend | Mean time, 3 windows | State delta | Latent drift | Stable promotion | NSA compressed | NSA selected | NSA sliding |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `baseline_cross_attention` | `StateTokenRecurrence` | 5349.631 ms | 0.528511 | 0.208999 | 1.0 | 0.062294 | 0.863726 | 0.073981 |
| `mamba_hybrid` | `mamba_ssm` | 4625.448 ms | 0.338021 | 0.077019 | 1.0 | 0.068841 | 0.872511 | 0.058648 |
| `no_nsa` | `mamba_ssm` | 4596.949 ms | 0.383781 | 0.287060 | 1.0 | 1.000000 | 0.000000 | 0.000000 |
| `no_stable_memory` | `mamba_ssm` | 4637.332 ms | 0.357718 | 0.089565 | 0.0 | 0.019207 | 0.874350 | 0.106443 |

## Interpretation

- All variants run through the same Dream3R control graph.
- `mamba_hybrid` uses the real server `mamba_ssm` backend.
- `no_nsa` forces branch usage to compressed-only, proving the NSA bypass switch is active.
- `no_stable_memory` has `stable_promotion_rate=0.0`, proving the AnchorBank write/recall/promote switch is active.
- `mamba_hybrid` shows lower synthetic state delta and lower mean runtime than the cross-attention baseline in this run, but this is not yet a quality claim.
- `no_stable_memory` still reports selected-branch gate mass because the learned NSA gate can weight the selected branch even when stable memory entries are masked. This is a useful diagnostic for future gate calibration.

## Caveats

- Inputs are synthetic random tensors.
- The demo sets `active_to_stable_threshold=0.0` so stable promotion is visible.
- Runtime includes full model forward, not isolated recurrence kernel profiling.
- Real reconstruction quality requires real image/depth/pose data and metrics. The first KITTI smoke path now exists in `evaluate_real_sequence.py`, so the next ablation table should reuse these variant names on real windows.

## Next Ablations

Minimum next table now that the KITTI real-data smoke path exists:

1. Repeat this table on KITTI real windows.
2. Add reconstruction metrics from `evaluate_real_sequence.py`, not just integration signals.
3. Compare NSA enabled vs disabled with learned gate calibration.
4. Geometric Critic repair enabled vs disabled.
5. Expert routing enabled vs fixed expert.
