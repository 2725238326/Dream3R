# DEC-20260502-002: Architecture Mechanism Intake Map

Date: 2026-05-02

Status:

```text
accepted workflow decision
```

## Decision

Dream should track broad architecture and visual methods through a branch-neutral intake map before promoting any method to a research branch or thesis.

New active artifact:

```text
planning/ARCHITECTURE_MECHANISM_INTAKE.md
```

## Reason

The user emphasized that sparse attention, reinforcement learning, continual learning, attention residuals, new visual methods, and combinations of multiple new 3R models are important to the research program.

However, these mechanisms should not be added as buzzwords. They must be translated through:

```text
Failure mode -> Mechanism -> Action -> Proxy metric -> Comparator -> Evidence level
```

## Scope

This decision covers research preparation and mechanism intake only.

It does not approve:

- model reproduction
- checkpoint downloads
- model training or fine-tuning
- KYKT app navigation changes
- frontend implementation
- final thesis selection
- discarding any major branch

## Expected Use

Future Dream research passes should use `planning/ARCHITECTURE_MECHANISM_INTAKE.md` when:

- adding sparse / linear attention mechanisms
- comparing SSM/Mamba-like state models
- evaluating attention residuals or hidden-state reuse
- considering RL / active perception
- considering continual learning or adapter updates
- integrating segmentation, tracking, flow, VOS, or new visual backbones
- using event, depth, IMU, LiDAR, or guided priors
- distinguishing 3R Composer L1 system routing from L2 mechanism distillation
