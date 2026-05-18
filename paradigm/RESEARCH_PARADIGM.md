# Dream Research Paradigm

Last updated: 2026-05-01

## Core Paradigm

Dream uses a **two-track research paradigm**:

```text
Track 1: Breadth Map
  Broadly mine papers, GitHub projects, and architecture ideas.
  Convert them into structured 3R hypotheses.

Track 2: Minimal Demo
  Keep one small teacher-facing demo path alive.
  Use the demo to force ideas into concrete artifacts, not only prose.
```

The two tracks must stay connected. Breadth Map without demo becomes empty literature collection. Minimal Demo without breadth becomes ordinary engineering.

## First-Phase Objective

The first phase should not pick a final paper topic.

It should produce:

1. a research map of candidate architecture mechanisms
2. a ranked idea pool
3. one small demo/prototype path
4. one initial KYKT app integration concept
5. a decision memo for which idea deserves deeper implementation

## Research Unit

Every idea must be converted into a **Dream Research Unit**:

```text
Idea name:
Source:
Borrowed mechanism:
3R bottleneck:
Architecture hypothesis:
Smallest experiment:
Teacher demo form:
KYKT integration surface:
Evidence level:
Engineering cost:
Risks:
Decision:
```

If an idea cannot be written in this format, it is not ready.

## Dual-Track Weekly Loop

Use this loop for each research cycle.

### Step 1: Intake

Collect 5-15 sources from:

- 3R / visual geometry
- Mamba / SSM / memory models
- efficient or residual attention
- test-time compute / self-correction
- continual learning
- RL / active perception
- 4DGS / dynamic scene representations
- event camera / cross-modal sensing

### Step 2: Mechanism Extraction

For each source, extract the mechanism:

- What state is stored?
- What computation is avoided?
- What prior is introduced?
- What signal is added?
- What error mode is corrected?
- What does the method know at train time vs test time?

### Step 3: 3R Translation

Translate the mechanism into a 3R hypothesis.

Bad:

```text
Use Mamba in 3R.
```

Good:

```text
Use geometry-gated selective state updates to replace temporal attention for streaming pointmap fusion. Gates depend on reprojection residual, confidence, dynamic mask, and baseline.
```

### Step 4: Scoring

Score every unit from 1 to 5:

- architecture novelty
- 3R relevance
- bottleneck severity
- demo surprise value
- engineering feasibility
- KYKT integration fit
- paper narrative strength
- available code/data
- risk of shallow combination

### Step 5: Two-Track Selection

At the end of each cycle, choose:

- 1 **architecture candidate** for deeper thinking
- 1 **demo candidate** for visible proof
- 1 **long-term speculative candidate**
- several deferred/rejected ideas with reasons

### Step 6: Decision Memo

Write a short memo before implementation:

```text
What we learned:
Best candidate:
Why now:
Minimal demo:
What must be discussed with the user:
Next action:
```

## Evidence Ladder

Use the cheapest evidence that can honestly support the claim.

### Level 1: Concept Evidence

- architecture diagram
- pseudo-code
- small mock workflow
- expected failure mode analysis

Use when the idea is very new or no code path is ready.

### Level 2: Existing-Model Evidence

- run existing 3R models on shared KYKT samples
- compare qualitative outputs
- identify concrete failure cases

Use when we can show why a new architecture is needed.

### Level 3: Prototype Evidence

- modify a pipeline
- add a controller, fusion layer, state module, or evaluation loop
- produce a visible output

Use when the idea has survived initial scoring.

### Level 4: Quantitative Evidence

- metric table
- ablation
- runtime/memory curve
- robustness comparison

Use only after the idea is worth the engineering cost.

## Decision Points That Require User Discussion

Pause and discuss with the user before:

1. choosing a primary research thesis
2. committing to one architecture family as the main direction
3. starting heavy training or large data construction
4. adding a major new dependency or large model download
5. changing KYKT app information architecture
6. creating a reusable Codex skill from the draft rules
7. spending significant time on a speculative repo with weak code availability
8. shifting from architecture-first work to application-first work
9. claiming teacher-demo readiness
10. discarding one of the major candidate tracks

The agent may proceed without asking for small edits, note-taking, document refinement, lightweight searches, and small local mockups.

## Candidate Track Definitions

### Track A: Memory / State 3R

Goal:

```text
Make 3R behave like a streaming geometric state machine.
```

Typical mechanisms:

- SSM / Mamba
- recurrent spatial memory
- map state compression
- geometry-gated updates
- loop-consistent memory consolidation

### Track B: 3R Composer

Goal:

```text
Combine the strengths of existing 3R models into a controlled research system.
```

Typical mechanisms:

- route samples to MASt3R / MonST3R / Fast3R / Spann3R / CUT3R
- fuse outputs
- compare failure modes
- distill or imitate best behavior
- produce unified output contracts

### Track C: Reasoning / Test-Time Compute 3R

Goal:

```text
Let 3R spend more compute on geometrically hard cases.
```

Typical mechanisms:

- uncertainty-gated refinement
- geometry self-check loops
- pose/depth hypothesis testing
- internal critique and repair
- adaptive iteration budget

### Track D: Continual / Lifelong 3R

Goal:

```text
Build spatial memory over time without catastrophic forgetting.
```

Typical mechanisms:

- replay
- confidence-preserving updates
- memory consolidation
- online adaptation
- drift detection

## Demo Philosophy

The first teacher demo does not need to prove the final paper.

It should prove:

```text
We are building a new research direction, and it already has a visible working surface.
```

Good first demo forms:

- KYKT app research lane showing ranked ideas and evidence
- side-by-side model failure map across shared samples
- mock streaming memory visualization
- prototype controller selecting among 3R model families
- test-time geometry self-check report on hard cases

Avoid demos that require weeks of training before any visual output exists.

## KYKT Integration Philosophy

KYKT should become the workbench where Dream ideas become observable.

Candidate integration surfaces:

- Overview research lane
- Sample Matrix evidence grid
- new prototype runner
- Advisor/report proposal generator
- System readiness for experimental repos
- long-running research management area

Do not force all research into model runners. Some ideas should first appear as reports, comparison tools, or analysis panels.

## Stop Conditions

Stop or defer an idea when:

- it cannot name a concrete 3R bottleneck
- it needs heavy training before any minimal evidence is possible
- it is only a buzzword combination
- it has no credible demo form
- it has no KYKT integration surface
- it duplicates an existing 3R model without a new mechanism

## First Operating Mode

Current operating mode:

```text
Balanced two-track plan:
  Breadth Map + Minimal Demo
```

The next research cycle should establish:

1. the first candidate source list
2. the first scoring table schema
3. the first minimal teacher-demo candidate
4. the first KYKT app management-area concept

