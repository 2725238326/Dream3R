# Dream3R-RC Method Figure

Date: 2026-06-06

## Figure Caption

Dream3R-RC uses real proposal teachers and a frozen StatePrior to produce a
state-conditioned bounded proposal fusion. The residual refinement is bounded
so it cannot freely overwrite the state prior. The candidate is accepted only
when the correct-state path beats shuffled-state controls.

## Mermaid Diagram

```mermaid
flowchart LR
  I["Input image window"] --> P["Real proposal teachers"]
  P --> F["Proposal feature/cache bank"]
  F --> B["Bounded convex fusion"]

  S["Dream state"] --> SP["StatePrior head"]
  SP --> FR["Frozen StatePrior"]
  FR --> B

  B --> R["Bounded residual refinement"]
  R --> O["Dream3R-RC output"]

  S --> SH["Shuffle-state control"]
  SH --> C["Causality gate"]
  O --> C
  C --> A["Accept only if correct-state beats shuffle"]

  Q["Qwen semantic labels"] -. "diagnostic only" .-> NQ["Not in RC model"]
  V["VGGT-Omega"] -. "optional teacher lane" .-> NV["Not in RC model"]
```

## Paper/Slide Version

```text
Input window
  -> real MASt3R/Fast3R/Spann3R proposal caches
  -> bounded convex fusion
  -> bounded residual refinement
  -> Dream3R-RC output

Dream state
  -> StatePrior head
  -> freeze prior
  -> state-conditioned fusion weights

Release gate
  -> compare correct-state against shuffled-state control
  -> accept only if state-causality survives
```

## Visual Claim Boundary

The diagram should not show Qwen or VGGT-Omega as part of the RC inference
path. They are shown only as diagnostic/teacher lanes outside the release
candidate.

