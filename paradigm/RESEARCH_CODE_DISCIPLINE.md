# Research & Code Discipline

Last updated: 2026-05-03

Status: active discipline rulebook for Dream research synthesis and any code work driven from Dream context.

## Provenance

These four spine principles are adapted from Andrej Karpathy's observations on LLM coding pitfalls, distilled by the community at:

```text
https://github.com/forrestchang/andrej-karpathy-skills
```

Karpathy's original framing applies to general LLM coding. This file translates each principle into Dream's specific context:

- research synthesis (mechanism intake, branch comparison, RU drafting)
- markdown-first artifacts (cycle logs, decision memos, registries, specs)
- code work in `Coding/4.06/vision_ui` that is *driven by* a Dream decision

A fifth Dream-native rule (`5. Honesty Override`) is added because research artifacts have a stronger truth-tracking requirement than typical product code.

## Scope

Apply this discipline to every Dream-side action that produces a durable artifact. That includes:

- writing or editing files under `E:\kykt\Dream\` (paradigm, planning, sources, units, registries, cycles, decisions, experiments, handoff, templates)
- drafting RU entries, mechanism specs, proxy case cards, decision memos
- writing prompts, skill drafts, and handoff briefs
- code that Dream explicitly asks Codex to write inside `Coding/4.06/vision_ui` (e.g. a research-prototype runner, an Advisor schema change, a Sample Matrix scoring helper)

This file is **not** the operating workflow (`paradigm/RESEARCH_WORKFLOW.md` is). It is the *behavior* layer that sits underneath any workflow stage.

## How To Use This File

Before producing a durable artifact, do a quick mental pass through the five rules below. They are ordered by frequency of relevance:

1. Think Before Synthesizing
2. Minimum Viable Mechanism
3. Surgical Edits
4. Falsifiable Research Goals
5. Honesty Override

When you skip a rule on purpose (because the task is genuinely trivial), say so in one line in the cycle log so the next agent knows it was a deliberate choice, not an oversight.

## 1. Think Before Synthesizing

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Karpathy's "Think Before Coding" maps directly: research synthesis is even more vulnerable to silent assumptions because evidence is often inferred or speculative.

Rules:

- Every claim must carry an evidence label: `paper-proven`, `code-observed`, `demo-observed`, `inferred`, `speculative`, or `unknown`. The `RESEARCH_DATA_MODEL.md` schema already requires this; this rule promotes it from "schema field" to "default behavior."
- If a paper / repo / mechanism has multiple plausible 3R translations, list all of them in the cycle log first, then pick. Never silently pick.
- If a candidate mechanism overlaps with an existing comparator (e.g. Spann3R / OVGGT / LoGeR / FILT3R / PAS3R / Mem3R), name the overlap explicitly *before* claiming novelty.
- If you do not know whether a source has running code or a usable checkpoint, say `unknown`, not `available`.
- When confused, stop. Name what is unclear in `logs/QUESTION_LOG.md` and ask the user. Do not synthesize through fog.

Apply when:

- promoting a `Mechanism` from intake to a `Research Unit`
- writing a finalist mechanism spec (`templates/finalist_mechanism_spec.md`)
- updating `BRANCH_COMPARISON_MATRIX.md` scores
- adding a row to `registry/source_registry.md`

Don't:

- silently rewrite an evidence label without a cycle-log entry justifying the change
- combine two sources into one mechanism without listing the borrowed parts of each
- claim a source supports a Dream mechanism when only the failure mode is shared

## 2. Minimum Viable Mechanism

**Smallest mechanism that addresses the failure mode. Nothing speculative.**

Karpathy's "Simplicity First" maps to mechanism design: 3R already has many partial solutions; the easy mistake is to stack 4–5 fashionable ideas and call it a thesis.

Rules:

- A mechanism spec must name **the smallest A1–A8 action subset** it owns. If the spec claims more than 3 owned actions, prune.
- A composition edge (`C1`–`C16` in `RESEARCH_GRAPH_AND_PAPER_START.md`) is allowed only after both endpoint mechanisms have at least `inferred` evidence labels.
- An RU description with more than 3 architecture buzzwords (`Mamba` + `RL` + `world model` + `4DGS` + ...) without a stated 3R bottleneck is rejected. See `RESEARCH_SKILL_RULES_DRAFT.md` Anti-Slop Rules.
- Choose the cheapest proxy metric from `P1`–`P8` that can *falsify* the mechanism. Do not pick the most comprehensive proxy by default.
- For prototype code (when a Dream decision authorizes it): the runner / report / tool should solve only the failure mode named in the spec. No speculative configurability.

The 200-vs-50 lines test, in Dream form:

```text
Would a senior 3R researcher say this RU / spec / runner is overcomplicated?
If yes, simplify.
```

Apply when:

- drafting an RU body in `RESEARCH_UNIT_BANK.md`
- filling `templates/finalist_mechanism_spec.md`
- writing a runner in `Coding/4.06/vision_ui/runners/` for a research prototype
- adding a new entry to `model_catalog`

Don't:

- inflate an RU to look impressive ("we combine Mamba + critic + 4DGS + active perception")
- attach a proxy metric that requires reproduction when an L2 metric works
- ship configurable knobs the spec does not justify

## 3. Surgical Edits

**Touch only what you must. The cross-link graph is fragile.**

Dream has a thick web of cross-references between paradigm/, planning/, registries/, and cycles/. A single "while I'm here, let me also tidy..." edit can desync four files.

Rules:

- When updating one Dream file, update only the files explicitly required by the **Guidance File Sync Rule** (`AGENT_MASTER_PROMPT.md`, `README.md`, `WORKFLOW_STATUS.md`, `RESEARCH_STATE.md`, current cycle log). Do not "improve" sibling files in the same pass.
- Match the existing voice and structure of each file. `RESEARCH_PARADIGM.md` is conceptual; `RESEARCH_WORKFLOW.md` is procedural; `RESEARCH_SKILL_RULES_DRAFT.md` is ruleset. Do not collapse styles.
- If you spot a stale claim outside the current task, log it in `logs/QUESTION_LOG.md` instead of silently fixing it. The fix can ride its own cycle.
- Preserve existing IDs (`SRC-…`, `RU-…`, `MECH-…`, `DEC-…`, `EXP-…`, `CYCLE-…`). Renumbering breaks links across files.
- For prototype code: do not refactor adjacent functions that aren't broken. The diff should explain itself.

The trace-test:

```text
Every changed line must trace to either:
  - a user request,
  - a decision memo entry, or
  - a Guidance File Sync Rule trigger.
If it traces to none of those, revert it or move it into a new task.
```

Apply when:

- patching a single registry row
- correcting a typo in a paradigm file
- updating a status table
- adding a runner without rewriting the SSH layer

Don't:

- "while I'm here" tidy other files in the same commit
- rename existing IDs to fit a new naming pattern
- mass-format or mass-rephrase prose unrelated to the task
- delete pre-existing entries from registries because they look stale (defer with a Q in `QUESTION_LOG.md`)

## 4. Falsifiable Research Goals

**Define what would falsify the claim. Loop until verified.**

Karpathy's "Goal-Driven Execution" maps to research success criteria. Dream already has `evidence_level`, `success_criteria`, and `stop_conditions` in the schema; this rule promotes them from "schema fields" to "non-skippable."

Rules:

- Every cycle declares, in the cycle log header:
  - in-scope failure mode (one of `F1`–`F6`)
  - owned actions (subset of `A1`–`A8`)
  - first proxy metric (one of `P1`–`P8`)
  - fail-fast condition (one short sentence)
- Every RU must have a `smallest_experiment` that produces a yes/no outcome at evidence level L1 or L2. No checkpoints, no training, no heavy install required.
- Every mechanism spec must include a "what would make us reject this within one cycle" line. If you cannot write that line, the spec is not ready.
- Transform vague verbs into verifiable goals:

| Avoid | Use |
|---|---|
| explore Executive Memory | does an evidence-triggered cache policy beat fixed-window on `P2 anchor retention` over 3 case cards? if no, defer |
| study active perception | does a mock uncertainty map yield `P7 view gain > 0` on 2 design cards? if no, defer |
| improve composer | does the L1 capability matrix reduce `P5 route regret` on the `static_collection_medium` sample? if no, escalate to L2 |
| make it work (curope) | the in-place build emits a `.so` that loads under `conda run -n <env> python` and `cuRoPE2D(...)` reaches the CUDA kernel |

- For Dream-authorized prototype code: write the success-test before the implementation. A research prototype without a falsification path is not a prototype, it is a sketch.

Apply when:

- opening a new cycle file
- moving an RU decision from `needs_user_decision` to `explore_next` / `prototype_next`
- writing an experiment plan in `experiments/`
- accepting a code task spawned by a Dream decision

Don't:

- write "explore X" without naming the failure mode and the proxy
- use total scoreboard sums as decisions; scores are *signals*, not approvals
- declare success when the test you set has not actually been run

## 5. Honesty Override

**Truth-tracking beats narrative neatness.**

This rule is Dream-native and overrides all four above when they conflict. Karpathy's framing assumes engineers tracking working code; Dream tracks claims about an unsettled research field, where it is far easier to drift into wishful taxonomy.

Rules:

- Never present a `speculative` claim with the language of a `paper-proven` one. Tone must follow the evidence label.
- When a previous decision proves wrong (example: "Align3R blocked by CUDA 11.3 vs cu121 mismatch" was wrong; the actual blocker was a GLIBC mismatch in a prebuilt `.so`), update the cycle log explicitly with the correction. Do not retroactively edit the original claim into looking right.
- Do not quietly retire a candidate branch. Dropping a branch requires a decision memo with a `defer` or `reject` status and a reason.
- Do not claim an experiment was run unless the artifact (file, log, plot) exists and is referenced by path.
- Do not claim user approval was given unless the user said so in this conversation. The decision registry must reflect actual user gates.
- If you realize mid-task that the framing is wrong, stop and write what you learned in `logs/QUESTION_LOG.md`. Re-plan in the next message.

Apply when:

- closing a cycle log
- writing a decision memo
- summarizing results back to the user
- responding to questions about whether a result is real

Don't:

- soften a `speculative` mechanism into "promising" without label correction
- describe planned experiments as if they were performed
- conflate "the env can run the model" with "the model produces good results"
- pretend a decision gate was passed when it wasn't

## Indicators That The Discipline Is Working

These are the equivalents of the Karpathy README's "How to know it's working" list, in Dream's terms:

- **Fewer silent overwrites in registries.** Evidence-label changes always come with a cycle-log line.
- **Smaller mechanism specs.** Owned actions ≤ 3, support actions ≤ 3, no buzzword stacking.
- **Cleaner diffs across paradigm/planning/registry files.** Each pull touches only the files the Sync Rule requires.
- **Cycle logs end with a falsification result, not a narrative.** "Did P_k fall below threshold? yes/no/deferred."
- **Wrong assumptions get retracted explicitly.** Old claims do not silently disappear.

## Tradeoff Note

This discipline biases toward **rigor over speed of synthesis**. For trivial edits (typo, single-row registry update, link fix), use judgment — the full five-rule pass is overhead.

The goal is reducing costly mistakes on durable research claims and on code that future cycles will rely on, not slowing down small fixes.

## Companion Files

- `AGENT_MASTER_PROMPT.md` — entry prompt; this discipline file is in its mandatory load protocol.
- `paradigm/RESEARCH_PARADIGM.md` — research philosophy (the "what for").
- `paradigm/RESEARCH_WORKFLOW.md` — operational stages (the "how").
- `paradigm/RESEARCH_DATA_MODEL.md` — schema for the entities this discipline governs.
- `paradigm/RESEARCH_SKILL_RULES_DRAFT.md` — long-form ruleset that may eventually package as a Codex skill; this discipline file is the lighter behavior layer that sits below it.
- `planning/ACTION_TAXONOMY_AND_PROXY_METRICS.md` — the A1–A8 actions and P1–P8 proxies referenced in rule 4.
- `planning/RESEARCH_GRAPH_AND_PAPER_START.md` — the F1–F6 failure modes and C1–C16 composition edges referenced in rules 2 and 4.
