# CYCLE-20260530 — Dream3R model-first milestone reorganization

date: 2026-05-30
status: closed as planning/route milestone
linked_decision: `decisions/DEC-20260530-013-milestone-reorg-proposal-bank-native-roadmap.md`
linked_spec: `specs/SPEC-20260530-003-dream3r-reconstruction-decoder-roadmap.md`
linked_plan: `planning/DREAM3R_MILESTONE_REORG_20260530.md`

## Objective

Prevent the post-midterm route from drifting into blind expert search or a
loose ensemble story. Reorganize Dream3R as a real staged 3R model:

```text
proposal encoders + Dream state + reconstruction decoder
```

## Work completed

- Re-read the current SCF/ver2.1 project state.
- Checked current external source surfaces for VGGT, CUT3R, Fast3R, Spann3R,
  MonST3R, STream3R, and InfiniteVGGT.
- Wrote DEC-013 to lock:
  - Dream3R is not a hard router;
  - external 3R models are proposal encoders / teachers;
  - Dream3R-owned work is state + reconstruction decoder;
  - next candidate experts are VGGT, CUT3R, MonST3R only.
- Wrote SPEC-003 to define the reconstruction-decoder roadmap:
  - Decoder v0 = SCFHead;
  - Decoder v1 = frozen-state projection;
  - Decoder v2 = proposal-set transformer;
  - Decoder v3 = native Dream3R distillation.
- Wrote the milestone plan and next-agent prompt.

## Key conclusion

The best route is not to ask "which one expert wins?" The route is:

```text
Which proposal bank raises the oracle ceiling,
and which Dream3R decoder turns that ceiling into final pointmap quality?
```

Current bank stays MASt3R / Fast3R / Spann3R. The next admission candidates
are VGGT, CUT3R, and MonST3R because they cover different missing regimes:
global feed-forward geometry, persistent state, and dynamic geometry.

## Boundary

No code was changed. No checkpoint download, server run, core edit, or new
model claim was authorized.
