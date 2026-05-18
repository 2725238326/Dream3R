# Phase 1 Decision Memo

Last updated: 2026-05-01

Status: preliminary. This memo records the current research posture after the first subagent-assisted survey. It is not a final project commitment.

## Current Field Read

The modern 3R field has moved beyond "pointmap regression works." The frontier is now about how spatial state is maintained and corrected over time:

- scale line: DUSt3R, MASt3R, Fast3R, MASt3R-SfM
- streaming/state line: CUT3R, Spann3R, Point3R, STream3R, TTT3R, LoGeR, Mem3R, PAS3R
- dynamic/4D line: MonST3R, POMATO, D^2USt3R, RayMap3R
- output/demo line: Splatt3R, InstantSplat, NoPoSplat, MV-DUSt3R+, 4DGS variants

The most valuable Dream question is therefore:

```text
What is the right computation graph for routing, writing, compressing, verifying, and adapting spatial state in streaming/dynamic 3R?
```

## Strongest Research Thesis Candidate

Working title:

```text
Dream3R: Geometry-Governed State and Test-Time Reasoning for Long-Context 3R
```

Core claim:

```text
Long-context 3R cannot be solved by simply using a bigger Transformer, a plain recurrent state, or a generic Mamba block.
It needs an explicit geometry-governed control system:
  route policy -> state write -> external spatial memory -> sparse global context -> geometry critic -> local revision / adaptation.
```

Why this is not just buzzword fusion:

- MambaOut warns that SSM is not automatically useful in vision.
- Point3R / LoGeR / Mem3R show that memory design is already central.
- Test3R / TTT3R show that test-time updates can matter.
- POMATO / D^2USt3R / RayMap3R show that dynamic scenes require motion-aware validity, not only static pointmaps.

## Near-Term Demo Stack Candidate

Do not build the full thesis first. The practical teacher-facing demo should be:

```text
Dream Research Lane
  + 3R Composer Controller
  + Geometry Critic-Revision Report
  + one Pose-Free Gaussian visual path
```

This gives:

- visible app progress
- source-backed research management
- a concrete "System-2 3R" story
- visually impressive output without overcommitting to heavy model training

## Important Decision Points For User Discussion

Before moving from survey to implementation, discuss:

1. Whether the umbrella thesis should emphasize memory/state, test-time reasoning, or a combined control graph.
2. Whether the first demo should prioritize app polish, local model reproduction, or architecture visualization.
3. Whether to spend setup effort on Splatt3R / DUSt3R / InstantSplat first.
4. Whether Dream should become a KYKT page immediately or remain markdown/data-driven until the first runner is proven.
5. Whether Phase 2 should build benchmark infrastructure or directly attempt a small prototype module.

## Recommended Phase 2 Plan

1. Build a `Dream Source Registry` data file from `sources/FRONTIER_SOURCE_MAP.md`.
2. Build a minimal `Research Unit` schema from `units/RESEARCH_UNIT_BANK.md`.
3. Add a KYKT Dream research lane that renders source, unit, score, and demo status.
4. Run one visual reproduction candidate:
   - first try DUSt3R as the stable foundational baseline
   - try Splatt3R as the first visual surprise path if CUDA/dependencies permit
   - keep InstantSplat as the permissive-license Gaussian fallback
   - keep MASt3R / Fast3R as app-composer baselines
5. Build a non-learned Geometry Critic report:
   - confidence conflict
   - view overlap / pose novelty
   - dynamic-risk flag
   - suggested retry/model switch/global context escalation

## Do Not Claim Yet

- Do not claim true infinite video reconstruction until the external memory story is formalized. At best, bounded GPU state plus growing sparse scene memory.
- Do not claim Event-DUSt3R novelty without positioning against EAG3R and Interp3R.
- Do not claim "Mamba beats Transformer" unless tested against STream3R / LoGeR-style causal and hybrid-memory baselines.
- Do not claim 4DGS asset generation until a local or reproducible pipeline is validated.

## Current Recommendation

Keep the research broad for one more batch, but let the first implementation path be narrow:

```text
Research breadth:
  memory/state + test-time reasoning + dynamic 4D comparators + GS demo enablers

Implementation narrow path:
  Dream lane + Composer + Critic report + DUSt3R/Splatt3R smoke test
```
