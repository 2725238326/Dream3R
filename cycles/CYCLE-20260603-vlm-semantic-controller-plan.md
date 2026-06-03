# CYCLE-20260603: VLM semantic-controller research plan

Date: 2026-06-03
Status: documentation pass complete
Decision: `decisions/DEC-20260603-027-vlm-semantic-controller-plan.md`

## Trigger

The user asked for a comprehensive research plan, project document updates, and
a prompt that a new agent can use to start fresh research toward better Dream3R
ideas and execution plans. The immediate research question was whether
Qwen3-VL-2B-Instruct or similar compact open VLMs can optimize Dream3R.

## Work completed

Added:

```text
planning/DREAM3R_V11_VLM_SEMANTIC_CONTROLLER_RESEARCH_PLAN.md
decisions/DEC-20260603-027-vlm-semantic-controller-plan.md
cycles/CYCLE-20260603-vlm-semantic-controller-plan.md
handoff/ARCHITECTURE_V11_VLM_SEMANTIC_CONTROLLER_AGENT_PROMPT.md
```

Updated the project guidance chain:

```text
TASK_SNAPSHOT.md
WORKFLOW_STATUS.md
INDEX.md
mainwork.md
registry/decision_registry.md
README.md
RESEARCH_STATE.md
AGENT_MASTER_PROMPT.md
```

## Findings

The plan keeps Qwen3-VL-2B-Instruct in the controller layer:

- semantic risk labeling;
- Router feature augmentation;
- Critic trigger priors;
- compute scheduler for expensive teacher admission;
- optional state auxiliary supervision after label-cache quality is proven.

The plan explicitly rejects using VLM output as depth, camera, pointmap, or
ground-truth geometry.

## Evidence used

Official Qwen sources checked:

```text
https://github.com/QwenLM/Qwen3-VL
https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct
```

Repository-local evidence checked:

- current bounded baseline and negative U1 result from `TASK_SNAPSHOT.md`;
- VLM mechanism slot from `planning/ARCHITECTURE_MECHANISM_INTAKE.md`;
- Composer/Router surfaces from local search over `code/dream3r`.

## Next executable gate

Implement the offline label-cache builder with mock and Qwen backends:

```text
code/dream3r/scripts/build_vlm_semantic_labels.py
code/dream3r/tests/test_vlm_semantic_labels.py
```

First pass should run locally with a mock backend and schema tests only. Qwen
inference on BUAA-Server GPU1 should be attempted only if model weights and
dependencies are available or explicitly approved.

## Boundaries preserved

- no frozen-core edit;
- no model training;
- no checkpoint download;
- no server environment mutation;
- no claim that Dream3R is usable beyond the locked 0.1448/0.1475 bounded
  baseline.
