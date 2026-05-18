# Dream Research Data Model

Last updated: 2026-05-01

Status: active schema for markdown-first research operations.

## Core Entities

Dream uses five core entities:

```text
Source
Mechanism
Research Unit
Decision
Experiment Plan
```

## Source

A source is a paper, project page, GitHub repository, dataset, benchmark, or official technical report.

Required fields:

```text
source_id:
title:
url:
year:
source_type: paper | repo | project_page | dataset | benchmark | report
evidence_type: paper | code | checkpoint | demo | dataset | speculation
track: direct_3r | architecture_transfer | demo_enabler | sensor | background | defer
mechanism_one_liner:
code_url:
license:
checkpoint_status:
demo_status:
reproduction_risk: low | medium | high | unknown
notes:
```

Rules:

- Do not put a source into the unit bank until the mechanism is clear.
- If license/checkpoint/demo status is uncertain, say `unknown`, not `available`.

## Mechanism

A mechanism is the transferable idea extracted from a source.

Required fields:

```text
mechanism_id:
source_ids:
name:
what_changes:
state_carrier:
compute_saved:
error_mode_addressed:
train_time_signal:
test_time_signal:
3r_translation:
evidence_boundary:
```

Rules:

- `what_changes` must describe a computation graph, system loop, state update, memory, sensing, or optimization change.
- Reject mechanisms that are only naming-level analogies.

## Research Unit

A Research Unit is a candidate Dream idea.

Required fields:

```text
ru_id:
idea_name:
track:
source_ids:
borrowed_mechanism:
3r_bottleneck:
architecture_hypothesis:
smallest_experiment:
teacher_demo_form:
kykt_integration_surface:
evidence_level: 1 | 2 | 3 | 4
engineering_cost: low | medium | high
risks:
decision:
```

Allowed decisions:

```text
explore_next
prototype_next
demo_next
defer
reject
needs_user_decision
```

## Score

Scores use 1-5 integers.

Required fields:

```text
architecture_novelty:
3r_relevance:
bottleneck_severity:
demo_surprise_value:
engineering_feasibility:
kykt_integration_fit:
paper_narrative_strength:
code_data_availability:
shallow_combination_risk:
```

Interpretation:

- high `shallow_combination_risk` is bad
- high values are otherwise good
- do not use a total score blindly; decisions should include judgment

## Decision

A decision records commitment, deferral, or a required user discussion.

Required fields:

```text
decision_id:
date:
scope:
decision:
status:
why:
evidence:
risks:
requires_user_approval: yes | no
next_action:
```

Rules:

- Major research direction choices require user approval.
- Heavy reproduction and KYKT app architecture changes require user approval.

## Experiment Plan

An experiment plan does not mean we will run it immediately.

Required fields:

```text
experiment_id:
name:
linked_ru_ids:
goal:
inputs:
method:
commands_or_files:
expected_artifact:
success_criteria:
stop_conditions:
estimated_cost:
approval_required: yes | no
status:
```

Rules:

- Any large model download, heavy repo install, training, or app navigation change must have `approval_required: yes`.
- A mock or report-only experiment can usually be planned without approval.

## ID Conventions

Use stable IDs:

```text
SRC-YYYY-NNN
MECH-YYYY-NNN
RU-001
DEC-YYYYMMDD-NNN
EXP-YYYYMMDD-NNN
CYCLE-YYYYMMDD-NNN
```

Do not renumber existing IDs unless a file is explicitly marked as draft-only.

