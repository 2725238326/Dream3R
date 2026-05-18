# Planning addendum v0.3 — Per-component latency pass/fail thresholds

addendum_id:    PLANNING_ADDENDUM_V03_LATENCY_THRESHOLDS
date:           2026-05-07
cycle:          023 (S2 deliverable; per DEC-20260507-003)
addresses:      RA-01 [HIGH] from Path C Agent A review (cycle 022)
parent_artifact: planning/DREAM3R_V02_CODE_STRUCTURE.md (cycle 020; NOT modified)
rule:           B-roadmap-F (no in-place modification; NEW addendum file)
source:         SPEC-20260506-004 Delta 1 per-frame component budget table

---

## Problem statement

Path C Agent A (cycle 022) identified that `bench_frame_budget.py` references Delta 1's
30–50 ms/frame budget but does not specify per-component latency pass/fail thresholds.
A code author implementing T-v02-A has no numeric criteria to validate against.

## Per-component latency pass/fail thresholds

Source: SPEC-20260506-004 Delta 1 per-frame component budget allocation.

| Component | Target latency | PASS threshold (p95) | FAIL threshold (p95) | Notes |
|---|---|---|---|---|
| C1 Perceiver (DINOv3-S forward) | 10–15 ms | ≤ 18 ms | > 25 ms | Frozen backbone; stable post-warmup; p95 accounts for CUDA scheduling jitter |
| C2 Memory NSA retrieve | few ms | ≤ 5 ms | > 8 ms | Sparse top-k; bounded by K=256 anchor bank size |
| C3 Permanence slot | few ms | ≤ 5 ms | > 8 ms | Bounded slot set (slot_count ≤ 32 proposed) |
| C4 Critic head | few ms | ≤ 5 ms | > 8 ms | Small transformer; only fires when evidence tokens indicate uncertainty |
| C5 Composer route | < 1 ms | ≤ 1 ms | > 2 ms | Parameter-free table join; CPU-feasible |
| C6 Bus tick + handoff | < 1 ms | ≤ 1 ms | > 2 ms | Dataflow bookkeeping; no compute |
| **End-to-end (C1–C6)** | **20–25 ms** | **≤ 33 ms** | **> 50 ms** | 30 FPS = 33.3 ms hard ceiling; FAIL at > 50 ms means sub-20 FPS |
| EXPERT-07 Test3R (lazy path) | OFF streaming | ≤ 500 ms per invocation | > 1000 ms | Not in streaming budget; measured separately per Critic-trigger event |

Evidence label: inferred. All thresholds are engineering-judgment targets on TITAN RTX 24GB;
promotion to `measured` requires ABL-v02-8 execution (frame-budget benchmark) under a
separate DEC.

## Threshold interpretation rules

```text
1. PASS threshold = p95 per-component latency over a 10-second streaming
   window (300 frames at 30 FPS). Component latency includes CUDA sync.

2. FAIL threshold = any component exceeding this value at p95 triggers
   an investigation flag. The component is not automatically removed
   from v0.2; the flag feeds into ABL-v02-8 analysis.

3. End-to-end PASS = sum of per-component p95 values ≤ 33 ms. This is
   the 30 FPS hard ceiling. A system running at 25 FPS (40 ms) is in
   the "yellow zone" — acceptable for development but FAIL for
   streaming-first deployment claim.

4. EXPERT-07 Test3R lazy-path latency is measured per invocation, NOT
   per frame. Expected invocation frequency: < 5% of frames (Critic
   flags only on uncertainty). If invocation frequency exceeds 10%
   of frames in B3 (long dynamic video), the Critic threshold is
   too sensitive — adjust Critic confidence threshold, not Test3R.

5. All thresholds assume TITAN RTX 24GB with CUDA 12.1, fp16 inference,
   batch_size=1 (streaming). A100/H100 numbers are NOT applicable
   and must NOT be reported as dream3r-server performance.
```

## Integration with bench_frame_budget.py

The file `code/dream3r/bench_frame_budget.py` (NEW per CODE_STRUCTURE §"bench_frame_budget")
should implement:

```text
- per_component_thresholds dict: maps component_id -> (pass_ms, fail_ms)
  populated from the table above.
- end_to_end_threshold: (pass_ms=33, fail_ms=50).
- lazy_path_threshold: (pass_ms=500, fail_ms=1000).
- report_verdict(results) -> {"overall": PASS|FAIL|YELLOW, "per_component": {...}}
  where YELLOW = between pass and fail on any component.
```

## Version history

```text
v1  2026-05-07  cycle 023. Addresses RA-01 from Path C Agent A.
                Per-component latency thresholds for bench_frame_budget.py.
                Source: SPEC-004 Delta 1.
```
