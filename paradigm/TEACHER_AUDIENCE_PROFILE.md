# Teacher Audience Profile

Last updated: 2026-05-04 (populated by user input; D3' unblocked for profile-population purposes; D3 demo-target choice itself still deferred per DEC-20260504-002)

Status: **populated (user input 2026-05-04)**. Substantive priority fields filled from user statement. Logistical fields recorded as "no constraints stated by user". Agent-inferred fields are explicitly labeled as such; user can correct any.

## Purpose

The four finalist specs (Critic / Memory / Permanence / Composer) each describe a possible teacher demo. Picking which one to show first depends on the teacher's research taste, prior expectations, and demo precedent. None of those are knowable to the agent.

This file is the user's input surface. When populated, it gates D3 (first teacher demo target). Until then, D3 is deferred per `decisions/DEC-20260504-002-no-all-in-on-single-finalist.md`.

## How To Use This File

1. The user fills the fields below.
2. The agent reads them when next asked to plan a demo or storyboard.
3. The agent does NOT invent values for blank fields.
4. If the agent must reason about a demo path before this file is populated, the agent surfaces a question to the user instead of inferring.
5. When the file changes substantively, append a dated note to the change log at the end rather than silently overwriting.

## Fields For The User To Populate

### Research Taste

```text
[user input 2026-05-04, verbatim paraphrase]
"老师主要希望我们能有科研的训练以及写作方面的技巧以及创新范式，
 同时也能讲好故事这样"

Decomposed (user-stated priorities, not agent-invented):
- 科研的训练 -> research methodology / training as a value in itself
- 写作技巧   -> academic writing craft as a visible skill
- 创新范式   -> paradigm-level novelty (not incremental tweaks)
- 讲好故事   -> narrative quality; the work must be tellable

[agent reading, user can correct]
Closest mapping onto the example axes: the teacher cares about
research-as-craft - process + framing + narration - more than a clean
theory-vs-system axis. Novelty (创新范式) and narrative (讲好故事)
both carry strong weight; principled formulation (writing + research
methodology) carries strong weight. Pure "module-stacking" or pure
"benchmark-chasing" demos are unlikely to land well; framing-first
demos with a clear story arc are.
```

Examples of what to capture (the user picks the framing that fits):

- theory-leaning: prefers principled formulations and crisp claims
- system-leaning: prefers measurable engineering and end-to-end demos
- visual-leaning: prefers visible artifacts, pictures, timelines

A teacher may be more than one. Order them by weight if so.

### Prior Expectations On This Work

```text
[user input 2026-05-04, verbatim paraphrase]
"老师不知道我们要做Dream"

Recorded as: cold start. The teacher has not seen Dream framing or
Dream content; first impression of the Dream line will be whatever
demo lands first.
```

Examples:

- cold start: teacher has not seen Dream content; first impression matters most
- known direction: teacher has seen prior framing (e.g. Dream3R / GEM-3R) and expects continuation
- skeptical baseline: teacher has expressed concern about a specific axis

### Demo Precedent

```text
[user input 2026-05-04, implied by Prior Expectations statement]
"老师不知道我们要做Dream" -> first impression.

Recorded as: first impression. Whatever demo lands first defines the
teacher's baseline for the Dream line. Sequencing per cycle 008 D1
(Critic-first technically) still applies; that is execution order,
not demo precedence — D3 (which finalist to actually demo first)
remains deferred per DEC-20260504-002.
```

Examples:

- first impression: this is the first demo of Dream the teacher will see
- reinforcement: teacher has seen earlier work; this demo continues a thread
- comparison: teacher will see this demo alongside another lab's work

### What The Teacher Has Previously Praised In Similar Work

```text
[user input 2026-05-04, verbatim paraphrase]
"老师是对3R方向都没啥具体贬褒"

Recorded as: no specific praise stated on the 3R direction. Teacher
has not, to user's knowledge, named specific 3R-line papers / demos /
phrases approvingly. The Research Taste field above remains the only
positive signal to design against.

[Earlier agent inference about "novel framing + story arc + writing
craft" is superseded by this explicit user statement and removed.]
```

Examples (the user fills with specifics, not categories):

- particular paper claims the teacher cited approvingly
- particular demo styles the teacher found compelling
- particular comparators the teacher views as benchmarks

### What The Teacher Has Previously Criticized In Similar Work

```text
[user input 2026-05-04, verbatim paraphrase]
"老师是对3R方向都没啥具体贬褒"

Recorded as: no specific criticism stated on the 3R direction.
Teacher has not, to user's knowledge, named specific 3R-line research
moves rejectionally. No concrete failure modes to design away from.
```

Examples:

- common research moves the teacher rejects (e.g. "module-stacking", "buzzword combinations")
- positioning failures the teacher cites
- demo failures the teacher would notice

### Hard Constraints

```text
[user input 2026-05-04, verbatim paraphrase]
"老师没啥要求的" (with respect to logistical constraints).

Recorded as: no hard limits stated by user on
- timing
- presentation surface (laptop / projector / shared notebook)
- live vs offline
- demo length

Confirm with user before any actual demo step; "no constraints stated"
is not the same as "infinite latitude".
```

Examples:

- timing: how long the demo is allowed to run
- presentation surface: laptop screen, projector, shared notebook, etc.
- live vs offline: must everything run offline; can the demo include live inference

## Agent Behavior While This File Is Empty

- Do NOT pick a demo target.
- Do NOT fill demo storyboard audience fields by inference.
- Do NOT recommend "Critic first" / "Memory first" / "Permanence first" / "Composer first" in user-facing summaries based on demo impact (technical sequencing per cycle 008 D1 still applies; that is execution order, not demo precedence).
- DO surface this file as an open dependency when the user asks about demo planning.
- DO continue with case cards in cycle 009 regardless; case cards are independent of demo authorization.

## Change Log

- 2026-05-04 (cycle 008.5): file created as placeholder per `handoff/SESSION-HANDOFF-20260504-001-cycle-008-closeout-and-cycle-009-prep.md` Task 11. No content. Awaiting user input.
- 2026-05-04 (cycle 009 activation): populated by user input within the cycle 009 activation pass.
  - User stated Research Taste priorities verbatim: 科研的训练 / 写作技巧 / 创新范式 / 讲好故事. Recorded verbatim + decomposed; agent reading flagged separately.
  - User stated no hard logistical constraints ("老师没啥要求的"). Recorded as such.
  - Three fields (Prior Expectations, Demo Precedent, Previously Criticized) remain empty by user. Agent did NOT invert priority statements into criticism claims (Honesty Override).
  - Previously Praised contains agent inference flagged for user correction.
- 2026-05-04 (cycle 009 activation, follow-up): remaining four fields resolved by user input.
  - "老师不知道我们要做Dream" -> Prior Expectations = cold start; Demo Precedent = first impression.
  - "老师是对3R方向都没啥具体贬褒" -> Previously Praised = no specific signal on 3R; Previously Criticized = no specific signal on 3R.
  - Earlier agent-inference block under Previously Praised is superseded and removed; user explicitly stated no specifics, so inference is no longer the right framing.
  - Profile is now fully populated. Remaining open item is D3 (which finalist to demo first), still deferred per DEC-20260504-002 until case cards land.

## Companion Files

- `decisions/DEC-20260504-002-no-all-in-on-single-finalist.md` — the decision deferring D3 until this file is populated and case-card data lands
- `templates/demo_storyboard.md` — references this file as the audience profile pointer
- `WORKFLOW_STATUS.md` — Recommended Next User Decision lists population of this file as a still-open user task
