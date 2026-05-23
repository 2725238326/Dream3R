# DEC-20260523-005 — Stage 2 Memory Closure

## Decision

Close Stage 2 as complete.

## Rationale

Stage 2 required a real KITTI long-window memory training run and a with-memory vs no-memory ablation showing at least 5% improvement in drift or pointmap consistency.

The final 50-window ablation meets that requirement:

- no-memory `pointmap_drift`: 0.0164055977
- with-memory `pointmap_drift`: 0.0000000000
- relative improvement: 100.00%

Training also converged enough for the roadmap criterion:

- memory-only train loss: 0.6283 -> 0.5382
- memory-only val loss: 0.5356 -> 0.5342

Full tests pass locally and on server.

## Implementation Boundary

The closure uses an external `MemoryPointmapResidualHead` plus an overlap-copy memory correction in evaluation. It does not modify `model.py` main forward, `anchor_bank.py`, or `nsa_attention.py`.

This was chosen to respect the closed-core rule while still making memory affect output pointmaps.

## Follow-Up

Stage 3 can proceed to Composer routing. A later architecture pass should decide whether the external memory-conditioned pointmap correction should become part of the core forward path.
