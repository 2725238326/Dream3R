# Dream3R-RC Presentation Outline

Date: 2026-06-06

## Slide 1: Problem

Long-sequence 3R needs more than a single-frame proposal model. Dream3R tests
whether a learned state can improve proposal fusion without collapsing into
spurious state dependence.

## Slide 2: Release Candidate

```text
frozen StatePrior + bounded residual refinement
```

Key metrics:

```text
KITTI / ETH3D: 0.1448 / 0.1475
```

## Slide 3: Method Figure

Use `release/METHOD_FIGURE.md`.

Main message:

```text
proposal teachers + frozen StatePrior + bounded residual + shuffle-state gate
```

## Slide 4: Main Result Table

Use the selected RC table from `release/RESULT_TABLE.md`.

Emphasize:

```text
beats best single expert
does not claim oracle-level performance
correct-state beats shuffled-state control
```

## Slide 5: Why VGGT-Omega Is Not The RC

Use the VGGT-Omega oracle and control tables.

Message:

```text
real teacher, strong ETH3D evidence, not robust mixed-domain release path
```

## Slide 6: Why Qwen Is Not The RC

Use the Qwen/VLM semantic gate table.

Message:

```text
semantic labels are diagnostic, not geometry control
```

## Slide 7: Honest Claim

Claim:

```text
controlled state-conditioned proposal fusion
```

Do not claim:

```text
SOTA
VGGT-Omega final model
Qwen-guided geometry
proposal-free native decoder
```

## Slide 8: Next Step

Next research lane:

```text
domain-conditional VGGT-Omega teacher integration with KITTI/state-causality
controls preserved as hard gates
```

