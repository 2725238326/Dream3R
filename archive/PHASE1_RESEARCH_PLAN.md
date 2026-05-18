# Dream Phase 1 Research Plan

Last updated: 2026-05-01

## Mission

Phase 1 prepares the ground for a future architecture-first 3R research direction while keeping a minimal teacher-facing demo path alive.

This phase is not supposed to choose the final paper topic immediately. It should create a reliable research base:

1. a current frontier map
2. a structured idea pool
3. mechanism-level translations into 3R hypotheses
4. one or more minimal demo candidates
5. a decision memo for which route deserves deeper implementation

## Operating Mode

Use the Dream two-track paradigm:

```text
Breadth Map + Minimal Demo
```

Breadth Map:

- survey 3R and adjacent architecture work
- extract mechanisms rather than just paper summaries
- score and cluster ideas

Minimal Demo:

- preserve a small teacher-facing proof path
- prefer a visible workbench artifact over a heavy training project
- connect the demo to KYKT app surfaces

## Scope

### Core 3R / Visual Geometry

Survey:

- DUSt3R-family pointmap models
- MASt3R / MonST3R / Spann3R / Fast3R / CUT3R
- streaming / stateful 3R models
- dynamic reconstruction, video depth consistency, and 4D reconstruction
- model output contracts: pointmaps, camera poses, confidence, dynamic masks, GLB/PLY, 4D assets

Key question:

```text
What bottleneck does each model solve, and what does it still fail to solve?
```

### Architecture Mechanisms

Survey mechanisms that can plausibly change 3R architecture:

- SSM / Mamba / state-space sequence modeling
- memory compression and persistent state
- residual attention / efficient attention / long-context vision architectures
- test-time compute and iterative self-correction
- continual learning and online adaptation
- RL / active perception and next-best-view
- mixture-of-experts, routing, controllers, and model composition

Key question:

```text
What architecture mechanism can be translated into a 3R module?
```

### Adjacent Systems and Sensors

Survey only when they strengthen a 3R mechanism:

- 4D Gaussian Splatting and dynamic scene assets
- event cameras and high-speed sensing
- IMU/depth/LiDAR priors
- physical priors and continuous-time motion fields

Key question:

```text
Does this solve a real 3R failure mode cheaply enough to matter?
```

### GitHub Project Mining

Survey GitHub projects in three tiers:

1. direct 3R / reconstruction repos
2. adjacent 3D / 4D / dynamic scene repos
3. architecture repos that can become 3R mechanisms

For each repo record:

- repository URL
- paper/source if any
- license if visible
- last update / active status
- installation difficulty
- model/data/checkpoint availability
- minimal smoke-test feasibility
- possible KYKT integration surface

Important: during actual execution, verify this information online because project status changes.

## Phase 1 Deliverables

### 1. Frontier Source Map

File:

```text
E:\kykt\Dream\sources\FRONTIER_SOURCE_MAP.md
```

Required sections:

- 3R model family map
- architecture mechanism map
- dynamic/4D/sensor map
- GitHub candidate map
- source confidence and recency notes

Each source should be tagged:

```text
direct_3r | architecture_transfer | demo_enabler | background | defer
```

### 2. Research Unit Bank

File:

```text
E:\kykt\Dream\units\RESEARCH_UNIT_BANK.md
```

Each unit follows:

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

Target count for first pass:

- 12-20 research units
- at least 3 memory/state units
- at least 3 composer/controller units
- at least 2 reasoning/test-time compute units
- at least 2 continual/lifelong units
- at least 2 demo-enabler units

### 3. Scoring Matrix

File:

```text
E:\kykt\Dream\units\IDEA_SCOREBOARD.md
```

Columns:

- idea id
- track
- architecture novelty
- 3R relevance
- bottleneck severity
- demo surprise value
- engineering feasibility
- KYKT integration fit
- paper narrative strength
- code/data availability
- shallow-combination risk
- total / weighted score
- decision

Initial scoring rule:

```text
Priority = high novelty + high 3R relevance + feasible minimal evidence + visible demo path.
```

Do not let pure novelty outrank feasibility unless the idea is kept explicitly as long-term speculative.

### 4. Minimal Demo Candidate Memo

File:

```text
E:\kykt\Dream\planning\MINIMAL_DEMO_CANDIDATES.md
```

Evaluate at least five possible teacher-demo forms:

1. KYKT research lane showing ranked Dream ideas and evidence.
2. Side-by-side failure/comparison map across shared KYKT samples.
3. Mock streaming memory visualization for Memory/State 3R.
4. Prototype 3R composer/controller selecting among model families.
5. Test-time geometry self-check report on hard cases.

For each demo:

- what the teacher sees
- what claim it supports
- what is real vs mock
- smallest implementation path
- risk
- whether it changes KYKT app architecture

### 5. Decision Memo

File:

```text
E:\kykt\Dream\archive\PHASE1_DECISION_MEMO.md
```

This is written after the first source map and scoring pass.

Required answer:

```text
What did we learn?
Which architecture track is strongest now?
Which demo path is cheapest and most impressive?
Which idea should be prototyped first?
Which decisions require user approval?
What should be done next?
```

## Batch Plan

### Batch 0: Setup and Query Design

Goal:

- define search queries
- define source inclusion rules
- prepare files for source map, unit bank, and scoreboard

Output:

- query list
- empty tables/templates

Decision gate:

- none unless scope changes significantly

### Batch 1: Direct 3R Frontier

Goal:

- map DUSt3R-family and newer 3R directions
- identify bottlenecks, outputs, and available code

Must cover:

- pointmap regression
- dynamic 3R
- streaming/stateful 3R
- fast many-image reconstruction
- video/depth consistency

Output:

- 3R source map
- at least 6 research units

Decision gate:

- discuss if one 3R family appears dominant enough to anchor the entire project

### Batch 2: Architecture Transfer

Goal:

- mine Mamba/SSM, memory, attention, test-time compute, continual learning, and RL mechanisms
- translate them into 3R hypotheses

Output:

- architecture mechanism map
- at least 8 research units

Decision gate:

- discuss before choosing Memory/State, Composer, Reasoning, or Continual as the primary architecture thesis

### Batch 3: Demo Enabler and KYKT Integration

Goal:

- identify demos that can be shown without heavy training
- map each to KYKT surfaces

Output:

- demo candidate memo
- KYKT integration concept

Decision gate:

- discuss before changing KYKT app information architecture

### Batch 4: Scoring and Convergence

Goal:

- score all research units
- select first architecture candidate, demo candidate, and speculative candidate

Output:

- scoreboard
- decision memo

Decision gate:

- user approval before implementation beyond lightweight mockups

## Search and Verification Rules

Because this is a frontier topic, execution must verify current sources online.

Use primary sources when possible:

- arXiv / OpenReview / conference pages
- official GitHub repos
- project pages from authors/labs
- official documentation for architecture libraries

Avoid relying on:

- unsourced blog summaries
- reposted code without paper links
- stale README claims without recent commits/releases

For each source, record:

- title
- URL
- date/year
- authors/lab if relevant
- code URL
- checkpoint/data availability if relevant
- one-sentence mechanism
- evidence status: paper, code, demo, speculation

## Research Quality Controls

### Anti-Hype Filter

Reject ideas that only combine buzzwords.

Every idea must answer:

```text
What changes in the 3R computation graph or system loop?
```

### Cost Filter

Every idea must state:

- can it be shown with no training?
- can it be shown by running existing models?
- does it need small code modification?
- does it require heavy training?

### Demo Filter

Every idea must state:

- what would the teacher actually see?
- what would be surprising?
- what is proven vs suggested?

### KYKT Filter

Every idea must map to:

- research lane
- model runner
- Sample Matrix
- Advisor/report
- System readiness
- long-term management area
- or be explicitly classified as background-only

## Important User-Discussion Points

Discuss with the user before:

1. declaring the main thesis
2. discarding a major track
3. committing to a heavy repo reproduction
4. starting training/fine-tuning
5. redesigning KYKT app navigation
6. deciding a teacher demo is ready
7. packaging the rules as a reusable Codex skill

Proceed without asking for:

- source collection
- note formatting
- lightweight score table updates
- prompt/rule refinement
- mock-only planning

## Suggested First Research Questions

Use these as the first query cluster:

1. What is the current DUSt3R-family frontier after DUSt3R, MASt3R, MonST3R, Spann3R, Fast3R, and CUT3R?
2. Which newer models explicitly address streaming, state, or long-sequence 3D reconstruction?
3. Which Mamba/SSM or memory architectures have visual/spatial variants that could transfer to 3R?
4. Which test-time compute or self-correction methods can be expressed as geometry consistency loops?
5. Which continual learning methods are lightweight enough to apply to spatial memory?
6. Which GitHub repos can produce a visible 3D/dynamic demo with minimal setup?

