# Reproduction Readiness Matrix

Last updated: 2026-05-04 (cycle 008.5 sync: dormancy status note added; cycle 008 source-mining additions appended at P3 research-background tier; cycle 008.5 finalist-to-candidate mapping appended)

Status: first pass with subagent merge (Phase 1; cycle 002). **Dormant during Phase 1.5 + cycle 008.5**: no reproduction is authorized; cycle 009 case cards are L2 proxy evidence over existing KYKT outputs and require no new smoke tests. The matrix wakes up if and when the user gates a Phase 2 smoke test. Some license/checkpoint fields still require direct file-level verification before any public/commercial use.

Purpose:

```text
Choose the first Phase 2 smoke test without confusing visual appeal, paper novelty, and engineering risk.
```

## Readiness Labels

- `P0`: first smoke-test candidate
- `P1`: good after one P0 path succeeds
- `P2`: keep as comparator / later integration
- `P3`: research background only for now

## Candidate Matrix

| Candidate | Official source | License / use note | Code / checkpoint / demo | Dependency risk | KYKT fit | Current rank |
|---|---|---|---|---|---|---|
| Splatt3R | [GitHub](https://github.com/btsmart/splatt3r) | CC BY-NC 4.0 | Gradio demo, pretrained model on Hugging Face, example PLY outputs | High; custom CUDA / modified Gaussian rasterization / MASt3R dependency | Strongest pose-free Gaussian visual surprise path, research/demo only | P0 |
| DUSt3R | [GitHub](https://github.com/naver/dust3r) | CC BY-NC-SA 4.0 non-commercial | interactive demo, Docker path, checkpoints | Medium-high; mature, but CUDA/RoPE/Docker choices matter | Foundational baseline and teaching reference | P0 |
| InstantSplat | [GitHub](https://github.com/NVlabs/InstantSplat) | Apache 2.0 per subagent license check; verify file before use | code, Docker option, MASt3R checkpoint dependency, sample scripts | High; submodules, 3DGS dependencies, CUDA kernels, data prep | Strong asset lane, heavier than Splatt3R | P0/P1 |
| MASt3R | [GitHub](https://github.com/naver/mast3r) | CC BY-NC-SA 4.0, dataset/checkpoint notices apply | HF/local demo, checkpoint downloads, MASt3R-SfM path | High; ASMK/retrieval optional complexity and DUSt3R inheritance | Excellent static baseline and matching/composer path | P1 |
| MV-DUSt3R+ | [GitHub](https://github.com/facebookresearch/mvdust3r) | License file present; verify exact terms before use | Gradio demo, all checkpoints, data/eval code released | Medium-high; authors only tested Linux + CUDA 12.4 | Strong multi-view pose-free geometry demo | P1 |
| Fast3R | [GitHub](https://github.com/facebookresearch/fast3r) | FAIR NC Research License | Gradio demo, HF auto-download weights, example inference API | Medium-high; CUDA 12.4 path, network-dependent HF download, do not install cuROPE | Excellent for Composer and high-image-count baseline runner | P1 |
| MonST3R | [GitHub](https://github.com/Junyi42/monst3r) | License file present; verify exact terms | demo.py, demo_data, Gradio/demo notes, real-time/window-wise modes | Medium; dynamic video path can be sensitive | Best dynamic 3R demo and comparator | P1 |
| NoPoSplat | [GitHub](https://github.com/cvg/NoPoSplat) | MIT | pretrained checkpoints on Hugging Face, eval scripts | Medium-high for training; inference/eval easier than training | Good open-license comparator, less immediate Gradio | P2 |
| CUT3R | [GitHub](https://github.com/CUT3R/CUT3R) | License file present; verify exact terms | Google Drive checkpoints, demo.py, demo_ga.py, examples | Medium-high; CUDA 12.1, RoPE compile, viser, linear memory note | Important architecture baseline | P2 |
| Point3R | [GitHub](https://github.com/YkiWu/Point3R) | License file present; verify exact terms | training/finetuning/eval code, Google Drive checkpoint for finetuning | Medium-high; training commands use 8 processes, no simple Gradio found | Explicit spatial memory comparator | P2 |
| STream3R | [GitHub](https://github.com/NIRVANALAN/STream3R) | NTU S-Lab License 1.0 per subagent; verify file before use | README shows inference code, app.py, HF auto-download, StreamSession; subagent flagged release-surface uncertainty | Medium-high; fresh repo and CUDA-dependent, but API is clear | Causal streaming comparator and KV-cache baseline | P2 |
| TTT3R | [GitHub](https://github.com/Inception3D/TTT3R) | License file present; verify exact terms | demo.py, examples, depends on CUT3R checkpoint | Medium-high; CUT3R/RoPE/evo/open3d dependencies | Test-time update comparator | P2 |
| RayMap3R | [Project](https://raymap3r.github.io/) | Code link claimed; verify repo maturity | project page and code link claimed | Unknown | Dynamic/static inference-time branch | P2/P3 |
| LoGeR | [Project](https://loger-project.github.io/) | GitHub link indicated on source pages; verify repo maturity | project/paper; code availability needs direct check | Unknown | Long-context hybrid memory evidence | P3 until code smoke path is clear |
| Mem3R | [Project](https://lck666666.github.io/Mem3R/) | Verify exact terms | project/paper; code state needs direct check | Unknown | Hybrid memory + TTT evidence | P3 until code smoke path is clear |

## Current Phase 2 Smoke-Test Recommendation

Use a two-lane smoke-test strategy:

```text
Lane A: stable geometry baseline
  DUSt3R first, then MASt3R or Fast3R

Lane B: visual surprise
  Splatt3R first, InstantSplat second, MV-DUSt3R+ third
```

Reasoning:

- DUSt3R is the safest foundational demo and gives the teacher a clean reference point for the 3R jump.
- Splatt3R is the fastest route to a visually impressive pose-free Gaussian artifact, but its non-commercial license means it should be framed as research/demo only.
- InstantSplat appears permissively licensed and visually strong, but has more moving parts than Splatt3R.
- MASt3R and Fast3R should anchor the Composer lane after one baseline works.
- MV-DUSt3R+ is strong but more environment-constrained because its README notes Linux/CUDA 12.4 testing.

## Do Before Any Local Clone

1. Confirm exact license if the result may be shown beyond classroom/research.
2. Confirm GPU/CUDA availability and whether Docker is acceptable.
3. Prefer one clean smoke test over installing several heavy repos at once.
4. Record command, input, output artifact, runtime, and failure mode in this file after each attempt.

## Evidence Notes

- Splatt3R README states it has a Gradio demo, Hugging Face pretrained model, downloadable example images/PLY files, and CC BY-NC 4.0 license.
- MV-DUSt3R+ README states all checkpoints and a Gradio demo were released, and notes Linux/CUDA 12.4 testing.
- Fast3R README states `python fast3r/viz/demo.py` auto-downloads pretrained weights from Hugging Face and provides a Gradio interface.
- DUSt3R and MASt3R both provide interactive demo paths and Docker instructions.
- NoPoSplat provides MIT license and Hugging Face checkpoints, but no first-pass Gradio path was found.
- CUT3R provides Google Drive checkpoints and demo scripts, but notes linear memory growth in its current parallel encoder acceleration path.
- Point3R provides training/finetuning/evaluation code and an explicit spatial pointer memory design; first-pass local demo path is less direct than Fast3R/Splatt3R.
- STream3R provides released inference code/weights and `StreamSession` for sequential input, making it the clearest causal-streaming comparator after the first visual demo.
- TTT3R provides demo commands around CUT3R checkpoints and is a good test-time update comparator, but it inherits CUT3R setup cost.

## Subagent Merge Notes

The reproduction-readiness subagent ranked:

```text
Splatt3R -> DUSt3R -> InstantSplat -> MASt3R -> MV-DUSt3R+ -> Fast3R -> CUT3R
```

This matrix adopts that ordering for first smoke-test planning, with two corrections:

- STream3R is not treated as first-wave ready, but its README does show HF auto-download inference and `StreamSession`; keep it as a causal-streaming comparator, not as a teacher-demo target.
- TTT3R has an official GitHub repo with CUT3R-based demo commands, but it remains an add-on path because it inherits CUT3R setup and checkpoint cost.

## Cycle 008.5 Finalist-To-Candidate Mapping

Status: navigation overlay, not a re-ranking. Added in cycle 008.5 so a reader of this matrix can see which existing P0/P1/P2 candidate would be the natural Phase 2 smoke-test target *if* the corresponding finalist's L2 case-card data later motivates reproduction. This does NOT authorize reproduction. Reproduction remains blocked until the user gates Phase 2.

| Finalist | Linked spec | Natural smoke-test candidate(s) | Current rank above | Why this candidate |
|---|---|---|---|---|
| Geometry Critic | `specs/SPEC-20260503-001-geometry-critic.md` | DUSt3R or MASt3R | P0 / P1 | Critic verifies on per-window output of an existing 3R model; DUSt3R/MASt3R are the lowest-risk hosts for a verify-then-act loop |
| Executive Memory | `specs/SPEC-20260503-002-executive-memory.md` | CUT3R (when env unblocks) | P2 | CUT3R's persistent-state architecture is the canonical host for memory-policy experiments |
| Dynamic Object Permanence | `specs/SPEC-20260503-003-dynamic-object-permanence.md` | MonST3R | P1 | MonST3R already produces per-frame dynamic masks + confidence + flow that the Permanence pipeline consumes |
| 3R Composer | `specs/SPEC-20260504-001-3r-composer.md` | DUSt3R + MASt3R + Fast3R + Spann3R | P0 / P0 / P1 / (in source map only; not yet reproduced) | Composer needs at least three different-regime models to exercise route_regret; all four are candidates rather than a single one |

This mapping is read-only against the candidate matrix above; it does NOT change Current rank, License, or Dependency risk for any candidate. If Phase 2 is later authorized, the user picks the actual smoke-test target; this table only narrates which finalist would benefit.

## Cycle 008 Source-Mining Additions (Research Background, P3)

Status: appended in cycle 008.5 to keep the readiness matrix in sync with the source map. These sources entered the inventory in cycle 008's source mining pass; none have been reproduced; none are first-wave smoke-test candidates. They are listed here as P3 research background only so a reader does not get the impression they are reproduction-ready.

| Candidate | Official source | License / use note | Code / checkpoint / demo | Dependency risk | KYKT fit | Current rank |
|---|---|---|---|---|---|---|
| LONG3R | [arXiv](https://arxiv.org/abs/2507.18255) | Verify project page before any use | project page; code state needs direct check | Unknown | Long-sequence memory comparator for SPINE_MEMORY required reading | P3 |
| LoGeR | [Project](https://loger-project.github.io/) | Verify project page before any use | project / paper; code state needs direct check | Unknown | Hybrid memory (TTT global + sliding-window local) comparator for SPINE_MEMORY required reading | P3 |
| Mem3R | [Project](https://lck666666.github.io/Mem3R/) | Verify project page before any use | project / paper; code state needs direct check | Unknown | Decoupled tracking / mapping memory comparator for SPINE_MEMORY required reading | P3 |
| PAS3R | [arXiv](https://arxiv.org/abs/2603.21436) | Paper-only; verify code claim | paper; code state unknown | Unknown | Pose-adaptive streaming state update comparator (advanced reading for SPINE_MEMORY) | P3 |
| FILT3R | [arXiv](https://arxiv.org/abs/2603.18493) | Code promised; verify before any use | paper; code state unknown | Unknown | Kalman-style latent filtering comparator (advanced reading for SPINE_MEMORY) | P3 |
| LongStream | [arXiv](https://arxiv.org/abs/2602.13172) | Verify project page before any use | project / paper; code state needs direct check | Unknown | Gauge-decoupled streaming + cache refresh comparator (advanced reading for SPINE_MEMORY) | P3 |
| OVGGT | [arXiv](https://arxiv.org/abs/2603.05959) | Verify before any use | paper, project, code claimed | Unknown | Constant-budget cache compression and dynamic anchor protection comparator (required reading for SPINE_MEMORY; advanced reading for SPINE_COMPOSER) | P3 |
| POMATO | [arXiv](https://arxiv.org/abs/2504.05692) | Verify before any use | paper, code location claimed | Unknown | Dynamic-aware token routing comparator for SPINE_PERMANENCE required reading | P3 |
| D^2USt3R | [arXiv](https://arxiv.org/abs/2504.06264) | Verify before any use | paper; code state needs direct check | Unknown | 4D pointmap comparator for SPINE_PERMANENCE required reading | P3 |
| Easi3R | [arXiv](https://arxiv.org/abs/2503.24391) | Verify before any use | paper, project | Unknown | Training-free dynamic adaptation comparator for SPINE_PERMANENCE required reading | P3 |
| RayMap3R | [Project](https://raymap3r.github.io/) | Code link claimed; verify repo maturity | project / paper; code state needs direct check | Unknown | Ray-based dynamic streaming comparator for SPINE_PERMANENCE required reading | P3 |
| SLAM3R | [arXiv](https://arxiv.org/abs/2412.09401) | Verify before any use | paper, code | Unknown | Sliding-window dense SLAM comparator (cycle 008 mining; not currently SPINE-anchored but kept for SPINE_COMPOSER advanced reading consideration) | P3 |
| Easi3R / RayMap3R / SLAM3R rationale | — | — | — | — | These three entered the inventory in cycle 008 mining but are not first-wave smoke-test ready; license / code maturity must be re-verified before any reproduction. | P3 |
| Test3R | [GitHub](https://github.com/nopQAQ/Test3R) | License file present; verify exact terms | paper, code | Unknown | Test-time geometric consistency comparator for SPINE_CRITIC required reading | P3 |
| MASt3R-SfM | [arXiv](https://arxiv.org/abs/2409.19152) | Verify exact terms | paper, code via MASt3R ecosystem | Unknown | Classical SfM-stage refinement comparator for SPINE_CRITIC required reading | P3 |
| G-CUT3R | [arXiv](https://arxiv.org/abs/2508.11379) | Verify before any use | paper | Unknown | Guided CUT3R comparator for SPINE_CRITIC advanced reading | P3 |
| CTRL | [arXiv](https://arxiv.org/abs/2502.03492) | Verify before any use | paper, code | Unknown | Cross-domain critic-revision pattern (LM domain) cited as `inferred` for 3R use in SPINE_CRITIC | P3 |
| SEAL | [arXiv](https://arxiv.org/abs/2506.10943) | Verify before any use | paper, code | Unknown | Self-edit driven adaptation pattern; held in source map; not currently a SPINE required-reading anchor | P3 |
| DINOv2 | [arXiv](https://arxiv.org/abs/2304.07193) | Apache-style; verify before commercial use | paper, code, checkpoints | Medium for inference; high for training | Visual prior for SPINE_PERMANENCE pipeline inputs (advanced reading) | P3 |
| CoTracker | [arXiv](https://arxiv.org/abs/2307.07635) | Verify before use | paper, code, checkpoints | Medium | 2D tracking prior for SPINE_PERMANENCE pipeline inputs (advanced reading) | P3 |
| SAM 2 | [arXiv](https://arxiv.org/abs/2408.00714) | Verify before use | paper, code, checkpoints, demo | Medium | Mask prior for SPINE_PERMANENCE pipeline inputs (advanced reading) | P3 |
| SpatialTracker | [arXiv](https://arxiv.org/abs/2404.04319) | Verify before use | paper, code | Medium-high | 3D-aware track prior for SPINE_PERMANENCE pipeline inputs (advanced reading) | P3 |
| Depth Anything V2 | [arXiv](https://arxiv.org/abs/2406.09414) | Verify before use | paper, code, checkpoints | Medium | Depth prior for cross-modal / Memory work; not currently a SPINE required-reading anchor | P3 |
| Depth Pro | [arXiv](https://arxiv.org/abs/2410.02073) | Verify before use | paper, code, checkpoints | Medium | Metric-scale depth prior; not currently a SPINE required-reading anchor | P3 |
| Metric3D v2 | [arXiv](https://arxiv.org/abs/2404.15506) | Verify before use | paper, code | Medium | Joint depth/normal prior; not currently a SPINE required-reading anchor | P3 |
| ActiveNeRF | [arXiv](https://arxiv.org/abs/2209.08546) | Verify before use | paper, ECCV | Medium-high | A8 active-perception comparator; not currently a SPINE required-reading anchor (Active Perception remains alive at lower priority) | P3 |
| FisherRF | [arXiv](https://arxiv.org/abs/2311.17874) | Verify before use | paper, code, ECCV | Medium-high | A8 active-perception comparator; not currently SPINE-anchored | P3 |
| ActiveSplat | [arXiv](https://arxiv.org/abs/2410.21955) | Verify before use | paper, project, RA-L | High | A8 active-3DGS anchor; not currently SPINE-anchored | P3 |
| ActiveGS | [arXiv](https://arxiv.org/abs/2412.17769) | Verify before use | paper | Unknown | A8 comparator; not currently SPINE-anchored | P3 |
| DEVO | [arXiv](https://arxiv.org/abs/2312.09800) | Verify before use | paper, RA-L | Medium-high | Event-only VO baseline; cross-modal branch (lower priority) | P3 |

Why these are P3 not P0-P2:

- None has been reproduced or environment-verified by Dream.
- License / code / checkpoint fields are inventory-only; direct file-level verification is required before any reproduction.
- Cycle 008.5 explicitly defers reproduction; cycle 009 case cards generate L2 proxy evidence over existing KYKT outputs only.

When Phase 2 reproduction is authorized in a future cycle, candidates from this P3 list may move up to P0-P2 with one of:

1. successful local smoke test (DUSt3R-style first-wave) followed by the corresponding finalist's case-card data motivating the reproduction; or
2. user gating a specific candidate as the Phase 2 target.

Until then, the rank "P3 research background" is the correct label.

## Wake-Up Conditions

This matrix is dormant. It wakes up when:

1. The user explicitly authorizes a Phase 2 smoke test (overrides "no reproduction" in `WORKFLOW_STATUS.md`).
2. Cycle 009 (or later) case-card data shows that L2 proxy evidence cannot decide between finalist mechanism choices, and the user agrees that L3 prototype evidence is required.
3. A teacher-demo target is set per `paradigm/TEACHER_AUDIENCE_PROFILE.md` and a reproducible artifact is needed.

If condition 1, 2, or 3 fires, the agent re-reads the candidate matrix above, the cycle 008 mining additions, and the cycle 008.5 finalist mapping, and proposes a single first smoke-test target for user approval. No prior rank is auto-promoted.
