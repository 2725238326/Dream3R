# EXP-20260501-001: DUSt3R / Splatt3R Smoke-Test Plan

Last updated: 2026-05-01

Status:

```text
planned only; do not run until user confirms
```

## Goal

Prepare the first reproducibility path without starting installation.

## Linked Research Units

- RU-002 3R Composer Controller
- RU-008 Pose-Free Gaussian Demo Bridge
- RU-011 Geometry Critic-Revision Loop

## Candidate Lane A: Stable 3R Baseline

Candidate:

```text
DUSt3R
```

Why:

- mature baseline
- official demo and Docker path
- clear teacher explanation of pointmap-based 3R

Expected artifact:

- reconstruction output from a small shared image set
- baseline record for KYKT Composer

Approval required:

```text
yes, before cloning/downloading/running
```

## Candidate Lane B: Visual Surprise

Candidate:

```text
Splatt3R
```

Why:

- uncalibrated image pair to Gaussian asset
- Gradio demo and pretrained checkpoint
- strongest quick visual story

Expected artifact:

- PLY / Gaussian output from a small image pair
- visual demo note for teacher-facing workflow

Approval required:

```text
yes, before cloning/downloading/running
```

## Fallback Candidate

Candidate:

```text
InstantSplat
```

Why:

- strong sparse-view Gaussian story
- permissive license indicated by subagent, but verify license file before use
- heavier setup than Splatt3R

## Success Criteria

- one repo reaches a visible output
- command, runtime, environment, and artifact are logged
- failure mode is documented if setup fails
- no claim of final research result is made

## Stop Conditions

Stop if:

- dependency setup exceeds expected effort
- GPU/CUDA mismatch blocks clean progress
- checkpoint access fails
- license terms are unclear for intended use

## Current Decision

Do not run yet. This plan exists so the future reproduction step starts deliberately.

