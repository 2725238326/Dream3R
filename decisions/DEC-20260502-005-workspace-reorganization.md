# DEC-20260502-005 Workspace Reorganization

decision_id: DEC-20260502-005

date: 2026-05-02

scope: workspace

decision: Reorganize the Dream workspace into topical subdirectories with an archive/ directory for historical artifacts and a new INDEX.md as the human-and-agent navigation entry point.

status: accepted

## Context

The Dream root directory accumulated ~28 markdown files at a single level: paradigm rules, active planning, source maps, RU banks, scoring, demo plans, frontend handoff, Phase 1 historical artifacts, and an early prompt draft were all at the same depth. This made it hard for both humans and incoming agents to distinguish:

- entry points (always read) from supporting documents
- active artifacts from superseded ones
- planning artifacts from research-content artifacts

The user requested cleanup with the explicit choice "Stage A + B + C": archive obsolete files, group active files into topical subdirectories, and add a clean total index.

## Evidence

- root previously held 28 .md files; 4 of them were explicitly historical or superseded (`PHASE1_*`, `MASTER_RESEARCH_PROMPT_DRAFT.md`)
- `MASTER_RESEARCH_PROMPT_DRAFT.md` self-identifies as "historical draft" and points readers to `AGENT_MASTER_PROMPT.md`
- Phase 1 is closed; Phase 1.5 has been the active phase for several cycles
- the load protocol in `AGENT_MASTER_PROMPT.md` already implicitly expressed the topical grouping by ordering files; the reorganization makes this structure explicit on disk

## Options

A. Stage A only: archive historical files; keep ~24 root files.

B. Stage A + B: also group by topic into `paradigm/`, `planning/`, `sources/`, `units/`, `handoff/`, `logs/`.

C. Stage A + B + C: also create a clean `INDEX.md` for navigation.

D. Defer cleanup; continue research first.

## Recommendation

C accepted by the user.

## Decision

1. Create `archive/`, `paradigm/`, `planning/`, `sources/`, `units/`, `handoff/`, `logs/`.
2. Move 23 files from root into the new subdirectories per the published map (see `cycles/CYCLE-20260502-006.md` for the full move table).
3. Update all cross-references in remaining .md files using a deterministic batch rewrite (PowerShell regex with negative lookbehind to avoid double-prefixing).
4. Manually update the four entry-level files (`AGENT_MASTER_PROMPT.md`, `README.md`, `WORKFLOW_STATUS.md`, `RESEARCH_STATE.md`) to ensure the load protocol, file maps, and active workstreams reflect the new layout.
5. Create `INDEX.md` at the root as a topic-keyed navigation document.
6. Verify with grep that no stale references remain.

## Risks

- a missed reference would silently break human/agent navigation; mitigated by the final verification grep
- git rename detection depends on content-similarity threshold; PowerShell `Move-Item` does not directly invoke `git mv`, but file content is unchanged so git will still detect renames at commit time
- reusable Codex skill packaging (when it happens) will need to point to the new layout; tracked under the existing skill-packaging gate

## User Approval Required

User explicitly approved Stage A + B + C in the cycle 006 prompt.

## Next Action

- run a final `grep_search` for residual stale references
- close the cycle 006 log
- continue research from the shortlist decision (`planning/BRANCH_SHORTLIST_DECISION_SURFACE.md` -> A / B / C)
