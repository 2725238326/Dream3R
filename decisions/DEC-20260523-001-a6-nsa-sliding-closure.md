# DEC-20260523-001: Close v0.5 Axis A6 — NSA sliding branch utility verified

decision_id: DEC-20260523-001
date: 2026-05-23
axis: A6
parent_spec: SPEC-20260522-001-dream3r-v05-axes.md
evidence_cycle: CYCLE-20260523-001
status: proposed (pending user ratification)

---

## Decision

**Close Axis A6 (NSA sliding branch utility verification).**

The sliding branch was observed at 0% weight on a 2-window KITTI smoke test. After a systematic 128-window long-sequence evaluation plus a 6-config sweep, the evidence conclusively shows:

1. The sliding branch **consistently fires** (weight ~28%, fire rate 100%) once bank occupancy saturates (K=256, achieved by window 12).
2. The 2-window zero was **correct routing** — insufficient bank context makes sliding uninformative; the learned gate correctly suppresses it.
3. **No code change is needed** to the NSA three-branch routing logic.
4. Drift remains bounded ([-0.08, 0.59]) over 128 windows — no divergence.

## closes_iff satisfaction

Per SPEC-20260522-001 §A6:

| Criterion | Satisfied | Evidence |
|---|---|---|
| KITTI rerun ≥ 8 windows | ✅ | 128 windows (kitti_200win_a6_evidence.json) |
| Per-window branch weights reported | ✅ | JSON + cycle log |
| Sliding branch fires or investigation recorded | ✅ | 100% fire rate post-saturation |
| Result folded into SOTA_FEATURE_MATRIX.md | ✅ | Updated Section 6 NSA row |

## Waived sub-conditions

None. All four sub-conditions fully satisfied.

## Consequence

- A6 status in SPEC-20260522-001 promoted from `axis-draft` to `axis-closed`.
- `ARCHITECTURE_V04_STATUS.md` "Behavioral observation needing follow-up" for NSA sliding branch is resolved.
- No v0.3 code change authorized by this DEC. The observation confirms current routing is correct.
- `SOTA_FEATURE_MATRIX.md` Section 6 NSA "Remaining gap" cell updated from "sliding weight 0 on KITTI smoke" to "resolved — fires at 28% on long sequences; 2-window zero is expected under low bank occupancy."

## Linked artifacts

- `cycles/CYCLE-20260523-001.md`
- `runs/kitti_sweep_v05.json`
- `runs/kitti_200win_a6_evidence.json`
- `runs/pytest_v05.log` (153 passed, no regression)
