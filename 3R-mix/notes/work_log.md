# Work log for 3R survey

Append-only log of substantive editing passes. Replaces verbal handoff for fine-grained history; `NEW_CHAT_HANDOFF.md` carries the latest top-level status.

## 2026-05-13 — Comprehensive optimization pass (LaTeX)

- **Files edited**: `main.tex`.
- **Files written**: `notes/work_log.md` (new), `NEW_CHAT_HANDOFF.md` (rewritten for LaTeX track).
- **Drivers**: `COMPREHENSIVE_OPTIMIZATION_PROMPT.md` (sections 1–12); `notes/fact_cards.md` and `notes/review_quality_audit.md` used as evidence-discipline references.

### Structural changes

- Author removed: `\author{KYKT Dream 调研组}` → `\author{}` to drop the internal project name from the title block. No other KYKT/Dream/Dream3R/agent/skill/workflow strings remain in `main.tex` (`Grep` verified).
- Section list aligned to the prompt's 10-section plan:
  1. 引言
  2. 从传统几何流程到点图表示
  3. 基础谱系：DUSt3R、MASt3R 与 SfM 接口  *(split from old §3.1)*
  4. 多视角规模化与统一视觉几何  *(split from old §3.2; now a section, not a subsection)*
  5. 视频、动态场景与 4D 重建
  6. 长序列重建中的状态、记忆与缓存
  7. 测试时验证、修正与先验输入  *(rewritten as three paragraphs covering Test3R/TTT3R/G-CUT3R/Pow3R/MASt3R-SfM and external priors)*
  8. 从几何预测到可查看输出
  9. 应用证据、复现边界与失败样本记录  *(new dedicated section; absorbs the application figure and matrix table)*
  10. 开放问题与结论  *(merged previous "讨论" four-point structure into the conclusion, dropping the standalone "结论" section)*

### Prose changes

- Abstract reworded to lead with the problem-branch organization principle (rather than the bare model list) and to make the three-tier evidence labeling (paper / official-code / local-smoke) explicit.
- Intro evidence-boundary paragraph rewritten to drop "本地流程跑通...质量领先" phrasing in favor of "可运行的本地复现只说明接口和依赖成立，不说明几何质量更优".
- Dynamic section: removed "通常被视为...重要代表" and "应更克制地理解"; replaced with direct mechanism descriptions for MonST3R/POMATO/D²USt3R/Easi3R/RayMap3R; added explicit "4D pointmap ≠ 4DGS asset" closing sentence.
- Long-sequence section: replaced the run-on model-listing paragraph with a four-class breakdown (spatial-pointer / causal-autoregressive / hybrid memory / budget-and-filter), each with one-sentence mechanism description and citation cluster.
- Test-time section: introduced three paragraphs covering (a) Test3R vs TTT3R consistency-vs-state distinction, (b) G-CUT3R/Pow3R/MASt3R-SfM differing prior-entry positions, (c) external auxiliary priors (Depth Pro / Metric3Dv2 / DINO / CoTracker / SpatialTracker / SAM2) framed as system-layer signals subject to prior conflicts.
- Output section: tightened Splatt3R/InstantSplat/NoPoSplat distinctions (uncalibrated pair vs. dense-stereo+GBA vs. canonical-frame unposed) and the rendering-vs-geometry caveat.
- New §9 prose explicitly defines the four evidence tiers (paper-proven, official-code, local-smoke-test, application-validated) plus "尚需确认", and ties them to figure / matrix table.
- Open-problems-and-conclusion section consolidates the previous four discussion points into one flowing paragraph plus a closing summary; both pieces avoid superlatives ("最强 / 领先 / 突破" — `Grep`-verified absent).

### New artifact

- Table 4: `tab:testtime` — "测试时机制与先验输入的进入位置和证据边界". Columns: 方法或先验 / 进入位置 / 修正约束信号 / 证据边界与风险. Rows cover Test3R, TTT3R, G-CUT3R, Pow3R, MASt3R-SfM, depth priors group, DINO group, tracking/segmentation group.

### Figure and table changes (summary)

- `fig:lineage` (Fig. 1) unchanged: DUSt3R-root taxonomy with six branches.
- `fig:memory` (Fig. 2 → still Fig. 2 by appearance order; in the new structure it appears in §6) unchanged: recurrent / spatial / hybrid / cache-policy quartet.
- `fig:application` (Fig. 4 by appearance) moved from §8 to new §9.
- `tab:foundation` rows tightened (replaced "领先" / "SOTA" wording with "更优" / "具体优劣需按实验表引用").
- `tab:dynamic` unchanged.
- `tab:memory` unchanged.
- `tab:testtime` added (new).
- `tab:application` moved to §9; "领先" cell text softened to "重建质量更优".

### Citation hygiene

- Removed `\nocite{*}`. All 43 bib keys in `references.bib` are now explicitly cited at least once (verified by comparing `grep` of `\citep{...}` against `@misc{...,}` entries).
- BibTeX style: `unsrtnat` (preserved).

### Build outcome

- Pipeline (manual, no `latexmk`):
  - `xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex`
  - `bibtex build/main`
  - `xelatex` × 2
- Final PDF: `build/main.pdf`, 13 pages, ~240 KB.
- Log status:
  - No `LaTeX Error`.
  - No `Undefined citation` or `Undefined reference`.
  - No `Overfull \hbox`.
  - 7 × `Underfull \hbox` warnings — all CJK column-wrap inside `tab:foundation` (line 130) and `tab:testtime` (line 233); accepted per the prompt's stated tolerance for table-induced underfulls.
- Environment noise: MiKTeX prints "running on an unsupported version of Windows" at every xelatex/bibtex invocation (Windows 11 Home China 10.0.29585). PDF generation is unaffected; recorded as environment warning, not a manuscript issue.

### Next-step candidates

- Per-paper benchmark reading: `notes/fact_cards.md` still flags benchmark numbers, license terms, and exact training-data details as "尚需确认". A targeted reading of 5–8 core PDFs would let us upgrade specific claims (e.g., MV-DUSt3R+ "2 seconds" hardware context, VGGT vs Fast3R quality comparison, TTT3R 20 FPS / 6 GB claims).
- 2026 preprints (LoGeR, Mem3R, OVGGT, PAS3R, FILT3R, RayMap3R, LongStream): code/checkpoint status not independently verified. Sentence-level claims are already kept neutral, but a targeted repository check before any external sharing remains warranted.
- D²USt3R bibliographic title contains `\textsuperscript{2}`; renders correctly under `unsrtnat`, but if the bib style is later changed (`acm`, `ieeetran`, etc.), revisit.
- Figure 1 (`fig:lineage`) currently lists all members per branch; once the survey is read by a third reviewer, consider compressing the long memory-branch list into a representative subset to avoid label crowding.

## 2026-05-13 — Figure optimization round (LaTeX)

- **Files edited**: `main.tex` (added `fig:paradigm` + small `fig:lineage` label tweak); `notes/figure_prompts.md` (full rewrite for current LaTeX state); `NEW_CHAT_HANDOFF.md` (figure-optimization subsection + updated未完成任务 + bumped timestamp).
- **New artifact**: `fig:paradigm` in §2 — TikZ two-row pipeline diagram. Top row: 特征提取与匹配 → 相机位姿估计 → 稀疏三角化 → 稠密 MVS/深度融合 → 全局 BA. Bottom row: 图像/图像对 → pointmap/深度/相机/置信度 → 对齐与一致性检查 → 点云/相机/匹配/Gaussian. Reused existing `arrows.meta`, `positioning`, `calc` libraries; no new package needed. Position: between the "三个直接后果" paragraph and the lineage paragraph; the consequences paragraph now opens with `这种变化的整体对照见图\,\ref{fig:paradigm}`.
- **Figure tweak**: `fig:lineage` streaming-branch label wraps to two lines (4+4 models) with trailing `等` to acknowledge §6 includes more models (PAS3R/FILT3R/LongStream) than fit the diagram.
- **Paper-figure embedding deferred**: `figures/` retains the DUSt3R/VGGT/MonST3R/CUT3R Fig.1 crops from the previous attempt, plus raw page-1 rasters. They are **not** referenced from `main.tex`. Reason: (1) prior crops were mixed quality — VGGT captured the title block, DUSt3R included caption tail, MonST3R/CUT3R were never visually verified; (2) per-paper reuse licenses for these arXiv preprints have not been independently confirmed; (3) the optimization prompt §0.4 defaults to "no embedded paper screenshots unless license confirmed". `notes/figure_prompts.md` records candidate re-crop coordinates (`crops_v2`) for any future attempt.
- **Compile**:
  - Same four-step pipeline as 2026-05-13 (xelatex / bibtex / xelatex / xelatex).
  - `build/main.pdf` is still 13 pages — `fig:paradigm` fit without page bloat.
  - Log: 0 errors, 0 undefined references/citations, 0 Overfull, 7 Underfull (same `tab:testtime` CJK column wraps as before; no new warning).
  - MiKTeX "unsupported Windows" message persists; PDF unaffected.
- **Caveat to user**: the chosen scope was "both new paradigm figure and embed paper figures"; only the first half landed in `main.tex`. The second half is staged in `figures/` but deferred pending license confirmation and crop re-verification. To proceed, follow `notes/figure_prompts.md` § "Paper-figure cache".

## 2026-05-13 — Paper-figure re-crop pass (not embedded)

- **Files edited**: none in `main.tex` this round. Only re-ran the PIL crop on the four cached page-1 rasters and overwrote `figures/<name>_fig1.png`.
- **Files written**: this `work_log.md` entry; `NEW_CHAT_HANDOFF.md` (timestamp + figure-cache subsection refreshed); `notes/figure_prompts.md` (cache table refreshed with new dimensions and visual-verification status).
- **Driver**: previous chat's handoff item "论文 Fig.1 嵌入决策" — re-crop with `crops_v2` coordinates, verify visually, then decide whether to embed.

### What changed on disk

- Re-applied `crops_v2` (plus minor manual tweaks) to the four `figures/<name>_p1-01.png` rasters. New dimensions on disk:
  - `dust3r_fig1.png` — 1365 × 630
  - `vggt_fig1.png` — 1380 × 465
  - `monst3r_fig1.png` — 1310 × 435
  - `cut3r_fig1.png` — 1385 × 360
- Raw page-1 rasters (`*_p1-01.png`, 1530 × 1980) are unchanged and remain alongside.

### Visual verification status

Read each cropped PNG one at a time (the previous attempt at multi-image Read hit a 32 MB request cap):

- `dust3r_fig1.png` — verified clean. Captures DUSt3R Fig.1 with pointmap outputs and rendered point clouds; no caption tail; no title-block fragment.
- `vggt_fig1.png` — verified clean. Captures the house/garden reconstruction with camera frusta and depth map; prior title-block issue is resolved.
- `monst3r_fig1.png` — verified clean. Captures the video-input strip, dynamic point cloud, and output labels (Video Depth / Camera Intrinsics / Dynamic & Static Masks).
- `cut3r_fig1.png` — **not yet visually verified**. The Read call returned `(media removed — rejected by API)` despite the file being only 623 KB on disk; cause unclear. Dimensions on disk look plausible (1385 × 360 — wide-and-short, consistent with a horizontal pipeline figure). Re-verification deferred.

### Not done this round (intentional)

- No `\includegraphics` blocks inserted into `main.tex`. Per `notes/figure_prompts.md` § "Figure policy", embedding is gated on independent license/reuse confirmation per paper. That check has not been performed.
- No xelatex/bibtex recompile. `build/main.pdf` is unchanged from the 2026-05-13 figure-optimization round (still 13 pages, same TikZ-only figure set).
- CUT3R crop visual confirmation still pending; if a future round wants to embed it, redo the Read in a clean context or open it in a viewer.

### Next-step candidates (unchanged in priority from prior entry)

1. Per-paper license/reuse confirmation for DUSt3R / VGGT / MonST3R / CUT3R before any `\includegraphics` embedding.
2. Visually re-verify `cut3r_fig1.png`.
3. If license cleared, insert four `\figure` blocks with attribution captions: 「图 X. 摘自 \citet{KEY}，仅用于综述说明，版权归原作者。」 — likely positions: DUSt3R/VGGT in §3–§4, MonST3R in §5, CUT3R in §6. Then xelatex × 3 + bibtex.

## 2026-05-13 — Paper figures embedded and evidence gates advanced

- **Files edited**: `main.tex`, `figures/cut3r_fig1.png`, `notes/figure_prompts.md`, `notes/paper_inventory.md`, `notes/model_inventory.md`, `notes/work_log.md`, `NEW_CHAT_HANDOFF.md`.
- **Driver**: user requested full continuation and explicitly confirmed that the paper-figure reuse/license gate is cleared. `$imagegen` skill was read; no generated image was needed because the paper crops were already available and more appropriate than synthetic replacements.

### Figure embedding

- Re-verified `figures/cut3r_fig1.png` visually. It was readable in the clean context; it showed three CUT3R examples but retained a left page-edge/date residue.
- Cropped `cut3r_fig1.png` from 1385 × 360 to 1340 × 360 to remove the page-edge residue while preserving all three example panels.
- Inserted two composite paper-figure floats in `main.tex`:
  - `fig:paper-core`: `dust3r_fig1.png` + `vggt_fig1.png`, caption attributed to `\citet{dust3r}` and `\citet{vggt}`.
  - `fig:paper-dynamic-stream`: `monst3r_fig1.png` + `cut3r_fig1.png`, caption attributed to `\citet{monst3r}` and `\citet{cut3r}`.
- Added `placeins` and `\FloatBarrier` so the paper figures remain near their relevant sections instead of floating past the bibliography.

### Evidence and wording updates

- §4 now states that MV-DUSt3R+, Fast3R, and VGGT experimental numbers must be read under their paper-specific input/hardware settings.
- `tab:foundation` now records:
  - Fast3R: 1000+ view expansion, with single-A100 and resolution caveats.
  - MV-DUSt3R+: 12/20-view second-level examples and official demo/checkpoint repository.
  - VGGT: paper and repository are public, but code/checkpoint license terms differ by version.
- §5 and `tab:dynamic` now distinguish RayMap3R's project-page/code-entry signal from application-quality validation.
- §6 now records 2026 project/code status from primary pages:
  - LoGeR: project page and code entry; hybrid SWA + TTT memory.
  - Mem3R: project page; decoupled camera-tracking fast-weight memory and mapping token state.
  - OVGGT: arXiv page lists project and code links; fixed-budget cache governance.
  - RayMap3R: project page lists arXiv and code links; dynamic suppression via RayMap/image dual branch.
  - LongStream: arXiv lists a project page; code maturity not upgraded beyond that.
  - FILT3R: arXiv says code will be released.
  - PAS3R: arXiv page verified; no stronger code claim written.
- `tab:testtime` now keeps TTT3R's `20 FPS / 6 GB` as a paper/project-page reported value, tied to hardware and sequence conditions rather than generalized throughput.

### Sources checked

- Local PDFs: `papers/mvdust3rplus_2412.06974.pdf`, `papers/fast3r_2501.13928.pdf`, `papers/vggt_2503.11651.pdf`, `papers/ttt3r_2509.26645.pdf`.
- Primary web pages: `https://github.com/facebookresearch/mvdust3r`, `https://github.com/facebookresearch/fast3r`, `https://github.com/facebookresearch/vggt`, `https://rover-xingyu.github.io/TTT3R/`, `https://loger-project.github.io/`, `https://lck666666.github.io/Mem3R/`, `https://raymap3r.github.io/`, `https://arxiv.org/abs/2603.05959`, `https://arxiv.org/abs/2603.21436`, `https://arxiv.org/abs/2603.18493`, `https://arxiv.org/abs/2602.13172`.

### Compile and visual QA

- Pipeline:
  - `xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex`
  - `bibtex build/main`
  - `xelatex` × 2
- Final PDF: `build/main.pdf`, 17 pages.
- Log status:
  - 0 LaTeX errors.
  - 0 undefined references/citations after final pass.
  - 0 Overfull hbox.
  - 7 Underfull hbox warnings, still confined to CJK table wrapping (`tab:foundation`, `tab:testtime`).
  - MiKTeX unsupported-Windows warning persists and remains an environment warning.
- Visual spot check rendered pages 5 and 8: `fig:paper-core` and `fig:paper-dynamic-stream` are visible, attributed, and no longer float after the bibliography.

### Remaining work

- The figure-embedding task is complete for the four approved Fig.1 crops.
- Core experiment-table checking is advanced but not a full benchmark meta-analysis; no new ranking claims were introduced.
- 2026 preprint project/code status is advanced from unknown to source-scoped status, but licenses for code/checkpoints should still be read from each repository before any software redistribution or reuse.
- Style-template compatibility remains unchanged and should be checked only if a target venue/template is chosen.

## 2026-05-13 — Narrative structure and figure-relation polish

- **Files edited**: `main.tex`, `notes/figure_prompts.md`, `notes/work_log.md`, `NEW_CHAT_HANDOFF.md`.
- Added an introduction roadmap that frames the paper as "representation basis -> input expansion -> temporal mechanisms -> test-time correction -> output and evidence" rather than a model list.
- Added an explicit §2 figure-reading paragraph:
  - `fig:paradigm` and `fig:lineage` are conceptual frames.
  - `fig:paper-core` and `fig:paper-dynamic-stream` are paper-figure visual anchors, not performance evidence.
  - `fig:memory` and `fig:application` are author-redrawn system abstractions.
- Added `\FloatBarrier` after `fig:lineage` so the reading-order paragraph appears after the taxonomy figure instead of being split by the float.
- Refined §4 prose around `fig:paper-core`: DUSt3R is described as pointmap intermediate language; VGGT as unified prediction of camera/depth/pointmap/tracks. The figure is explicitly scoped to problem statement/output form, not performance comparison.
- Added a transition sentence before `tab:foundation` to connect the paper figure to the evidence-boundary table.
- Refined §6 prose around `fig:paper-dynamic-stream`: MonST3R is framed as dynamic geometry estimation; CUT3R as continuous-input state update. The following paragraph now returns from paper visual anchors to mechanism-level taxonomy before `fig:memory`.

### Verification

- Recompiled with the required 4-step pipeline: `xelatex`, `bibtex`, `xelatex`, `xelatex`.
- Final PDF remains `build/main.pdf`, 17 pages.
- Log check: 0 LaTeX errors, 0 undefined references/citations, 0 Overfull hbox; 7 existing Underfull hbox warnings remain in `tab:foundation` and `tab:testtime`.
- Forbidden internal terms check against `main.tex` returned no matches for `KYKT`, `Dream`, `Dream3R`, `agent`, `skill`, `workflow`, or `本地项目`.
- Rendered pages 2--8 for visual QA; confirmed the figure-reading paragraph now follows `fig:lineage`, and both paper composite figures remain visible and attributed.

## 2026-05-13 — Stage-final output

- **Files edited/output**: `main.tex`, `notes/work_log.md`, `NEW_CHAT_HANDOFF.md`, `deliverables/3r_survey_stage_final_2026-05-13.pdf`.
- Per final-stage request, performed a light terminal polish:
  - Abstract evidence wording changed from "local record" style to "论文机制、官方仓库与复现记录".
  - §9 evidence tiers rewritten as Chinese paper prose: 论文可证 / 官方代码 / 复现烟测 / 应用验证.
  - `tab:application` final row now says not to write "可运行" as "质量已验证".
- Recompiled with the required 4-step pipeline. Output remains 17 A4 pages.
- Final checks:
  - 0 LaTeX errors.
  - 0 undefined references/citations.
  - 0 Overfull hbox.
  - 7 known Underfull hbox warnings in tables only.
  - Forbidden internal-term scan on `main.tex` returned no matches.
  - Rendered page 1 for visual QA; title, abstract, keywords, and start of §1 render normally.
- Stage-final PDF copied to `deliverables/3r_survey_stage_final_2026-05-13.pdf` (2,849,136 bytes).

## 2026-05-13 — Post-final polish pass

- **Files edited/output**: `main.tex`, `notes/work_log.md`, `NEW_CHAT_HANDOFF.md`, `deliverables/3r_survey_stage_final_2026-05-13_polished.pdf`.
- Implemented the four optional polish items requested after the stage-final review:
  - Cleaned table typography by using explicit `\makecell` line breaks in `tab:foundation` and `tab:testtime`.
  - Unified the evidence tier wording around "接口烟测" / "应用验证" in §9, `fig:application`, `tab:application`, and the conclusion.
  - Compressed the final conclusion paragraph to reduce repeated model-name enumeration and foreground the paper's main judgment.
  - Added PDF metadata through `\hypersetup` (`Title`, `Subject`, `Keywords`).
- Recompiled with the required 4-step pipeline.
- Final log check after this pass:
  - 0 LaTeX errors.
  - 0 undefined references/citations.
  - 0 Overfull hbox.
  - 0 Underfull hbox.
  - 0 LaTeX warnings matched by the final `rg` log scan.
  - Forbidden internal-term scan on `main.tex` returned no matches.
- `pdfinfo` confirms metadata and 17 A4 pages.
- Rendered pages 6--9 for visual QA; table/section flow remained normal.
- Could not overwrite `deliverables/3r_survey_stage_final_2026-05-13.pdf` because it was open/locked by another process. Wrote the polished deliverable as `deliverables/3r_survey_stage_final_2026-05-13_polished.pdf` instead.

## 2026-05-13 — Caption and prose naturalization pass

- **Files edited/output**: `main.tex`, `notes/work_log.md`, `NEW_CHAT_HANDOFF.md`, `notes/figure_prompts.md`, `deliverables/3r_survey_stage_final_2026-05-13_caption_polished.pdf`.
- Shortened the main figure/table captions:
  - `fig:paradigm`, `fig:lineage`, `fig:paper-core`, `fig:paper-dynamic-stream`, `fig:memory`, `fig:application`.
  - `tab:foundation`, `tab:dynamic`, `tab:testtime`, `tab:application`.
- Reworked prose that sounded like process reporting:
  - Replaced "证据边界" framing in the manuscript with source-based judgment / evidence wording.
  - Removed old "不是 / 而非 / 不把 / 不写 / 接口烟测" style phrases from `main.tex`.
  - Made the abstract, DUSt3R/MASt3R discussion, test-time section, external-prior paragraph, and conclusion more natural.
- Kept paper-figure source attribution in captions while removing redundant explanation.
- Recompiled with the required 4-step pipeline. Final PDF: `build/main.pdf`, 16 A4 pages.
- Final checks:
  - 0 LaTeX errors.
  - 0 undefined references/citations.
  - 0 Overfull hbox.
  - 0 Underfull hbox.
  - 0 matched LaTeX warnings in the final log scan.
  - Forbidden internal-term scan on `main.tex` returned no matches.
  - Old phrasing scan on `main.tex` returned no matches for `证据边界`, `应用边界`, `不是`, `而非`, `不把`, `不写`, `接口烟测`, `质量已验证`, or `流程可运行`.
- Rendered pages 5, 8, and 10 for visual QA; paper composite figures and the application/long-sequence pages remain readable, with shorter captions.

## 2026-05-13 — Final refinement pass

- **Files edited/output**: `main.tex`, `notes/work_log.md`, `NEW_CHAT_HANDOFF.md`, `notes/figure_prompts.md`, `deliverables/3r_survey_stage_final_2026-05-13_refined.pdf`.
- Reworked the abstract into a tighter paper-style structure:
  - 3R background and central representation shift.
  - Main branches and representative models.
  - Evidence sources used for claims.
  - Core judgment about intermediate representations, state, priors, and visible outputs.
- Refined paper-figure captions:
  - `fig:paper-core` now names DUSt3R and VGGT sources directly.
  - `fig:paper-dynamic-stream` now names MonST3R and CUT3R sources directly.
  - Captions remain short and keep explicit attribution.
- Unified table language:
  - Last columns in `tab:foundation`, `tab:dynamic`, `tab:testtime`, and `tab:application` now use "记录要点".
  - `tab:memory` uses "典型风险" instead of "潜在失败点".
- Added a compact six-item reproduction-record template in §9: input source/scale, model and weight version, runtime environment, outputs, failure samples, license plus runtime/memory.
- Strengthened the final conclusion around the main claim: 3R reorganizes intermediate representations, state updates, priors, and visible assets, not just model rankings.
- Recompiled with the required 4-step pipeline. Final PDF: `build/main.pdf`, 16 A4 pages.
- Final checks:
  - 0 LaTeX errors.
  - 0 undefined references/citations.
  - 0 Overfull hbox.
  - 0 Underfull hbox.
  - 0 matched LaTeX warnings in the final log scan.
  - Forbidden internal-term scan on `main.tex` returned no matches.
  - Old phrasing scan on `main.tex` returned no matches for `证据边界`, `应用边界`, `不是`, `而非`, `不把`, `不写`, `接口烟测`, `质量已验证`, `流程可运行`, `使用口径`, `使用提示`, or `潜在失败点`.
- Rendered pages 1, 5, 8, and 10 for visual QA; abstract, paper composite figures, and application/long-sequence pages remained readable.
- Wrote current recommended deliverable to `deliverables/3r_survey_stage_final_2026-05-13_refined.pdf` (2,838,654 bytes).

## 2026-05-14 — Project closeout to arXiv-only route

- **Files edited/output**: `README.md` (rewritten), `GENERATION_PROMPT.md` (shrunk to historical pointer), `main.typ` (DEPRECATED header), `bib.yaml` (DEPRECATED header), `NEW_CHAT_HANDOFF.md` (added 项目收口 section + release checklist + 未完成任务 closeout note + 最后更新时间), `notes/work_log.md` (this entry).
- User confirmed wind-down route: arXiv-only, no venue submission (route C). Phase 1 hygiene items also requested in same turn.
- README.md rewritten as canonical entry: declares LaTeX-only canonical pipeline, current deliverable PDF, 4-step xelatex/bibtex compile, `.gitignore` policy, paper Fig.1 license note (DUSt3R / VGGT / MonST3R / CUT3R), Typst legacy snapshot status.
- GENERATION_PROMPT.md shrunk to a short historical-note paragraph pointing to NEW_CHAT_HANDOFF.md and README.md.
- Top-level Typst legacy files (`main.typ`, `bib.yaml`) received DEPRECATED comment headers; `review-template.typ` left intact as it is template machinery subordinate to `main.typ`.
- `.gitignore` reverified: `/papers/`, `/build/`, `/guidance_skills/` — all three exclusions in place.
- `references.bib` quick dedup pass: 43 unique bib keys confirmed (foundation 7 + long-seq 7 + 2026 preprints 6 + dynamic 5 + test-time 3 + gaussian-splatting outputs 3 + base 3DGS/4DGS 3 + backbone/depth 4 + tracking 3 + metric depth 2 = 43).
- NEW_CHAT_HANDOFF.md additions:
  - New 项目收口 / Release Closeout section dated 2026-05-14.
  - New 发布前检查清单 (release checklist) — recompile / forbidden-term grep / page-count + file-size / figure citation / PDF metadata / paper-image license.
  - Note above 未完成任务 indicating all 3 items are post-closeout optional under route C.
  - Updated 最后更新时间 to 2026-05-14.
- No LaTeX recompile or PDF change this pass. Current deliverable `deliverables/3r_survey_stage_final_2026-05-13_refined.pdf` remains canonical.
- Forbidden internal-term scan not re-run because `main.tex` was not edited; last clean scan stands.

## 2026-05-14 — Quality pass after wind-down

- **Files edited/output**: `main.tex`, `references.bib`, `notes/work_log.md`, `NEW_CHAT_HANDOFF.md`, `deliverables/3r_survey_stage_final_2026-05-14_quality.pdf`; sync edits to `Dream/WORKFLOW_STATUS.md` and the Track B memory file (`project_track_b_3r_mix_survey.md`).
- **Driver**: after the 2026-05-14 wind-down (route C, arXiv-only) the user requested a final quality pass without restarting Track B. Plan file: `C:\Users\27252\.claude\plans\greedy-petting-lemur.md` (17 items grouped A/B/C; Tier-C content like evaluation/dataset sections, critical-evaluation column, narrative restructuring deliberately deferred).

### A 组 — 去重与删除（5 项）

- **A1**: removed `fig:application` TikZ flow diagram (24 lines) since it duplicated `tab:application`. Added one-sentence transition before the table: "在这一框架下，3R 模型是中间环节：输入经过几何预测，输出之前需要一致性与置信度检查，并伴随来源、失败样本与许可证记录。"
- **A2**: removed the §1 末段 "四类证据材料" re-definition. The abstract still flags four evidence tiers; the canonical definition stays in §9.
- **A3**: removed §2 末段 "本文的图像材料分三层使用..." which duplicated §1 末段 roadmap function.
- **A4**: dropped "应用质量另行复验" / "代码许可需按版本区分" cautionary tails from `tab:foundation` (VGGT row), `tab:dynamic` (RayMap3R row), and §6 closing line. Kept §9 as the single normative place where evidence-validation language lives.
- **A5**: merged the two-paragraph §10 conclusion into a single paragraph whose closing sentence carries the central judgment about intermediate representations / state / priors / visible assets and the failure-sample-and-license caveat.

### B 组 — 语言精修与表头统一（8 项）

- **B-Abstract**: "三类依据，用于说明性能结论、工程成熟度和应用可行性的来源" → "四类依据，便于追溯性能结论、实现状态与失败样本的来源".
- **B2**: §3 sentence "DUSt3R 打开的是一种接口转向" → "DUSt3R 引入了一种新的几何中间层"。Removed the manufactured term "接口转向".
- **B3**: dropped legal-style "代码/权重许可需按版本区分" from the `tab:foundation` VGGT row body (replaced with mechanism-level description; license framing kept only in §9).
- **B5 + B5b**: §7 "测试时 prompt tuning" → "测试时一致性优化", with the same change in the `tab:testtime` Test3R row. Avoids the prompt-learning misnomer.
- **B6 + B7**: §9 opening rewritten from a meta sentence + numbered list of four evidence tiers into a single prose paragraph: "将 3R 模型转化为可交付系统时，证据来源至少分布在四个层面：论文方法图与章节描述支撑公开机制，官方仓库说明代码、权重与 demo 状态，复现记录验证依赖与默认输入，跨场景实验表、失败样本与许可证则用于支撑应用判断。" Followed by paper-figure attribution sentence.
- **B8**: unified the last-column header of all 5 booktabs tables (`tab:foundation`, `tab:dynamic`, `tab:memory`, `tab:testtime`, `tab:application`) to "适用条件与局限". Body cells reworded from caution-style ("应配合 X / 需另行验证") to mechanism-style ("适合 Y 输入条件下使用 / 对 Z 域分布敏感").

### C 组 — 内容补充（4 项）

- **C1**: added `croco` entry to `references.bib`. `references.bib` total entries now 44 (one of the prior count discrepancies surfaced too — the handoff said 43 but the actual file had pre-existing 43; +1 CroCo → 44). §3 opens with one CroCo citation sentence: "DUSt3R 在此之前由 CroCo 的跨视角补全自监督预训练奠定基础，把 cross-view 视觉对应能力迁移到稠密 pointmap 预测上\citep{croco}。"
- **C2**: §3 expanded with one MASt3R mechanism paragraph (~5 lines): dense local feature head + contrastive descriptor loss + mutual-nearest-neighbor correspondence at inference + Sinkhorn refinement; explains why a feature head was added on top of the DUSt3R pointmap head.
- **C3**: added a 6-category failure-modes paragraph at the head of §10 (before the consolidated conclusion paragraph): 弱纹理/纯色区域 / 镜面与玻璃 / 快速运动与严重遮挡 / 长基线大视差 / 长序列尺度漂移 / 域外场景。 Each category one sentence; provides concrete cautions before the abstract "tension" framing.
- **C4**: added `fig:timeline` (TikZ) after `fig:lineage` in §2. Horizontal axis 2023–2026 × 5 tracks (基础 / 多视角 / 动态 / 长序列 / 测试时与输出). Nodes cover all 32 models cited in the paper, each in its publication year. §2 sentence updated: "图 \ref{fig:lineage} 给出本文采用的综述性谱系，图 \ref{fig:timeline} 进一步给出其时间分布。" `\resizebox{\textwidth}{!}{...}` keeps the figure inside the text width; track y-spacing tightened to `{0, -1.3, -2.6, -4.3, -6.0}` cm to limit page bloat.

### Build outcome

- Pipeline: `xelatex` → `bibtex build/main` → `xelatex` × 2 (4-step manual sequence).
- Final `build/main.pdf`: 18 A4 pages, 2,847,531 bytes (≈ 2.85 MB).
- LaTeX log:
  - 0 LaTeX errors.
  - 0 undefined references / undefined citations (CroCo entry resolved after the bibtex pass).
  - 0 Overfull hbox.
  - 0 Underfull hbox.
  - 0 LaTeX warnings matched by final log scan.
  - MiKTeX "unsupported Windows" environment warning persists as before; not a manuscript issue.
- Forbidden internal-term scan on `main.tex`: 0 hits for `KYKT`, `Dream`, `Dream3R`, `agent`, `skill`, `workflow`, `本地项目`. Old workflow-style phrasing scan: 0 hits for `工程成熟度`, `接口转向`, `代码/权重许可`, `prompt tuning`, `证据组织本身`, `应用质量另行验证`.
- `pdfinfo` confirms PDF metadata (Title / Subject / Keywords) is intact.
- Page count: 18 pages, +1 over the prior 16/17-page versions. The added page comes from §10 failure-modes paragraph, §3 MASt3R mechanism paragraph, and `fig:timeline` figure; the new content is plan-internal additions, not redundancy, so 18 pages is accepted.

### Deliverable

- `deliverables/3r_survey_stage_final_2026-05-14_quality.pdf` (2,847,531 bytes) is the new recommended deliverable. Prior 2026-05-13 versions are preserved alongside.

## 2026-05-15 — Prose naturalization pass

- **Files edited/output**: `main.tex` (10 paragraph rewrites), `deliverables/3r_survey_stage_final_2026-05-15_natural.pdf`; sync edits to `NEW_CHAT_HANDOFF.md`, `README.md`, `notes/work_log.md` (this entry), and the Track B memory + Dream top-level docs (`Dream/INDEX.md`, `Dream/TASK_SNAPSHOT.md`, `Dream/WORKFLOW_STATUS.md`).
- **Driver**: user feedback "内容还是没那么自然，此外一些 AI 风格的语言表述还是有点严重，不像人写的". The 2026-05-14 quality pass had cleared workflow-style vocabulary but the prose still had visible LLM tells. Scope confirmed via single-question prompt: "按示范力度全文改".

### What was rewritten

Targeting six recurring AI-tell patterns: enumerated "第一类/第二类/..." paragraphs, "前者...后者..." / "既...也..." parallel constructions, "X 的意义在于" / "关键在于" / "综上所述" cliché openings, meta-commentary like "本文按..." / "这样的安排...", workflow vocabulary ("承接", "消费", "交付物"), and "扮演...角色" / "起到...作用" stock phrasing.

- **Abstract**: dropped "本文的核心判断是：" + "既在于...也在于..." structure; rewrote around a single narrative claim about evidence sources and what really decides deployment.
- **§1 intro**: rewrote the Depth Anything / DINOv2 / SAM2 / 3DGS framing sentence to remove "在本文中作为支撑先验或辅助模块讨论" / "作为输出表示和可视化层来讨论" parallel; dropped the trailing meta-commentary sentence "这样的安排把模型谱系和应用约束放在同一条叙述线上...".
- **§2**: replaced "前馈式三维重建的核心变化在于..." with "差别集中在..."; killed the "它带来三个直接后果。第一... 第二... 第三..." enumerated paragraph and merged into one continuous paragraph that describes the same three consequences in prose.
- **§3 DUSt3R/MASt3R**: replaced "DUSt3R 的意义在于..." and "从综述角度看..." openings; rewrote MASt3R paragraph to drop "这一支线也说明..." meta-commentary; phrased the "traditional geometry returning via new interface" point as a noted phenomenon rather than a moral.
- **§4 multi-view**: rewrote two paragraphs to drop "这一组工作的共同启示是..." + "前者强调... 后者强调..." patterns; kept the concrete content (Fast3R many-view / MV-DUSt3R+ sparse-view / VGGT / MapAnything / Pow3R).
- **§6 long-sequence categories paragraph**: this was the most LLM-shaped paragraph in the manuscript ("进入近一年的工作可分为四类。第一类是...第二类是...第三类是...第四类是..."). Rewrote as continuous narrative with "一条延续... 另一条... 再有一类... 还有一条线..." flow; preserved every model citation.
- **§7 test-time**: rewrote three paragraphs; dropped "两者机制相近但侧重不同：Test3R 更靠近... TTT3R 更靠近..." and "前者偏向... 后者偏向..." parallels; replaced "外部先验在 3R 系统中扮演辅助角色" + "当先验与模型预测冲突时，系统层需要给出取舍规则" with a more direct phrasing.
- **§8 output**: replaced "实际应用很少直接消费模型内部的 pointmap" ("消费" calque) with "很少直接面向"; rewrote "这些方法属于输出与资产层，承接 3R 几何结果" to drop the workflow framing; killed "应用时还需要看两类信号：一是... 二是..." enumeration.
- **§9 application evidence**: rewrote three paragraphs to drop "证据来源至少分布在四个层面" framing, "这个模板用于追踪来源，使应用判断更容易复核" workflow sentence, and "在这一框架下，3R 模型是中间环节" / "可作为写作和复现记录的核对清单" meta-commentary.
- **§5 dynamic** (small): replaced "这里需要区分三类输出：4D pointmap 和 dynamic mask 属于几何中间量，4DGS 属于可渲染表示" with em-dash phrasing.
- **§10 conclusion** (largest): the original §10 had two enumerated paragraphs back-to-back ("第一类是... 第六类是..." for failure modes, then "第一... 第二... 第三... 第四..." for structural tensions, plus a "综上所述..." closing sentence). Rewrote as three flowing paragraphs — six failure modes as a narrative sweep using em-dashes and rhythm variation, four tensions as a continuous "更高一层" paragraph using different connective phrasing per item ("但 / 一个... 一个... / 也让 / 但要避免"), and a separate closing paragraph that drops "综上所述" entirely and ends on "失败样本与许可证往往比 benchmark 数字更先暴露问题".

### Build outcome

- Pipeline: `xelatex` → `bibtex build/main` → `xelatex` × 2.
- Final `build/main.pdf`: 18 A4 pages, 2,854,049 bytes (≈ 2.85 MB; same page count as 2026-05-14 quality version; the prose rewrites compensated for each other in length).
- LaTeX log: 0 errors, 0 undefined references/citations, 0 Overfull, 0 Underfull, 0 LaTeX warnings.
- AI-tell residue scan (`Grep` `main.tex` for patterns `综上所述|意义在于|关键在于|核心变化在于|核心判断|前者.{1,15}后者|第[一二三四五六]类|继续处理|工程成熟度|这一组工作的共同|消费.*pointmap`): 0 hits for all targeted patterns.
- Forbidden internal-term scan (`KYKT|Dream|Dream3R|agent|skill|workflow|本地项目`): 0 hits, unchanged from prior passes.

### Deliverable

- `deliverables/3r_survey_stage_final_2026-05-15_natural.pdf` (2,854,049 bytes) is the new recommended deliverable. The 2026-05-14 quality version and the 2026-05-13 trio remain in place as earlier snapshots.
