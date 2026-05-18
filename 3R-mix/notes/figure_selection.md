# Figure selection notes

Date: 2026-05-12.

Purpose: choose paper figures and survey-native diagrams for the 3R review. This file separates three roles:

- `paper-source candidate`: a figure in a paper that can be inspected and possibly cited or redrawn.
- `redraw recommended`: use the paper figure as conceptual evidence, but redraw in Typst/Mermaid to avoid copyright and visual-style mismatch.
- `survey-native`: a new diagram/table made by us because no single paper figure can represent the review-level relation.

## Policy

- Do not directly embed paper figures in the final public version until license/venue reuse policy is checked.
- For internal drafts, paper figures may be used as visual references, but captions must identify the source paper and figure number.
- For final review diagrams, prefer Typst-native or Mermaid-rendered schematics for route maps, taxonomies, and application pipelines.
- Avoid image generation for text-heavy diagrams. Generated images are only suitable for non-critical conceptual visuals; exact labels should be added by Typst, not by the image model.

## Paper figure candidates inspected

A contact sheet was rendered at `build/paper_figure_scout/core_paper_first_pages_contact_sheet.png` from the first two pages of selected PDFs.

| candidate | local PDF | likely figure | role in review | action |
|---|---|---:|---|---|
| DUSt3R | `papers/dust3r_2312.14132.pdf` | Fig. 1 | Shows the pointmap paradigm and pose-free dense reconstruction setup. | Redraw recommended as the "traditional pipeline vs pointmap" explanation; cite DUSt3R. |
| MASt3R | `papers/mast3r_2406.09756.pdf` | Fig. 1 | Shows dense 3D-grounded correspondences. | Optional paper-source candidate for matching section; redraw if used. |
| Fast3R | `papers/fast3r_2501.13928.pdf` | Fig. 1 | Shows many-view one-forward-pass motivation. | Use as reference for many-view branch in lineage/taxonomy diagram. |
| VGGT | `papers/vggt_2503.11651.pdf` | Fig. 1 | Shows unified prediction of camera/depth/pointmap/tracks. | Strong candidate for unified geometry section; redraw compactly. |
| CUT3R | `papers/cut3r_2501.12387.pdf` | Fig. 1 | Shows persistent-state continuous 3D perception on static/dynamic scenes. | Candidate for long-sequence section; compare with Spann3R rather than using alone. |
| Spann3R | `papers/spann3r_2408.16061.pdf` | Fig. 1 | Shows spatial memory and global pointmap reconstruction. | Use as reference for memory primitive diagram. |
| MonST3R | `papers/monst3r_2410.03825.pdf` | Fig. 1 | Shows dynamic-scene geometry pipeline and outputs. | Candidate for dynamic section; avoid overloading with Easi3R. |
| Easi3R | `papers/easi3r_2503.24391.pdf` | Fig. 1 | Shows training-free attention adaptation and dynamic motion disentanglement. | Mention as mechanism reference; not a central figure. |
| RayMap3R | `papers/raymap3r_2603.20588.pdf` | Fig. 1 | Shows RayMap/image branch contrast and dynamic suppression. | Use as reference in dynamic mechanism table/figure, not necessarily direct image. |
| Test3R | `papers/test3r_2506.13750.pdf` | Fig. 1 | Shows triplet consistency / test-time prompt tuning. | Good candidate for test-time mechanism figure; redraw to avoid confusing it with TTT3R. |
| OVGGT | `papers/ovggt_2603.05959.pdf` | Fig. 1 | Shows cache/budget and streaming visual geometry behavior. | Use as evidence for cache-governance subsection. |
| Splatt3R | `papers/splatt3r_2408.13912.pdf` | Fig. 1 | Shows uncalibrated pair -> 3D Gaussian splat -> novel renderings. | Candidate for output-representation section; license-sensitive. |

## Figures to include in the review

### Figure A: Survey lineage map

Type: survey-native.

Content: DUSt3R root with six branches:

- pointmap/matching: MASt3R, MASt3R-SfM
- many-view/unified geometry: Fast3R, MV-DUSt3R+, VGGT, MapAnything, Pow3R
- streaming/memory: CUT3R, Spann3R, Point3R, STream3R, LONG3R, LoGeR, Mem3R, OVGGT, PAS3R, FILT3R, LongStream
- dynamic/4D: MonST3R, POMATO, D^2USt3R, Easi3R, RayMap3R
- test-time/prior-guided: Test3R, TTT3R, G-CUT3R, MASt3R-SfM
- renderable output: Splatt3R, InstantSplat, NoPoSplat, 3DGS, 4DGS

Implementation: Typst or Mermaid, not AI-generated text.

### Figure B: Mechanism examples from papers

Type: source-aware paper figure panel or redraw panel.

Recommended panel entries:

1. DUSt3R Fig. 1 concept: pointmap reconstruction.
2. VGGT Fig. 1 concept: unified camera/depth/pointmap/tracks.
3. CUT3R or Spann3R Fig. 1 concept: state or spatial memory.
4. MonST3R or Test3R Fig. 1 concept: dynamic geometry or test-time consistency.

Implementation: redraw as schematic boxes unless reuse permission is confirmed.

### Figure C: Long-sequence memory primitives

Type: survey-native.

Content:

- recurrent state: CUT3R, STream3R
- spatial/pointer memory: Spann3R, Point3R
- hybrid memory: LONG3R, LoGeR, Mem3R
- cache/update/filtering: OVGGT, PAS3R, FILT3R, LongStream

Implementation: Typst table/diagram.

### Figure D: Application and evidence path

Type: survey-native.

Content: input regime -> model family -> geometry output -> quality evidence -> output artifact -> report/log.

Implementation: Typst/Mermaid flowchart. Dream/KYKT may appear only as terminal evidence logging, not as a model.

## Tables to keep or add

| table | status | role |
|---|---|---|
| Literature relevance tiers | present | explains inclusion scope. |
| Prior roles | present | keeps Depth/DINO/CoTracker/SAM2 out of main-model ranking. |
| Dynamic 3R mechanism table | present | includes Easi3R without over-centering it. |
| Foundation/many-view model comparison | present | core model taxonomy. |
| Video/dynamic/long-sequence comparison | present | capability classification. |
| Test-time/adaptation/output comparison | present | separates Test3R, TTT3R, G-CUT3R, Gaussian outputs. |
| Application evidence matrix | planned | should list output artifact, quality signal, code/license status, and evidence label. |

## Image generation usage

No generated image is necessary for exact scientific diagrams because text-heavy labels should be deterministic. If a generated bitmap is later used, it should only serve as a non-authoritative visual base and all labels should be overlaid in Typst.

Candidate imagegen prompt for a non-textual background-free route-map base:

```text
Use case: scientific-educational
Asset type: academic review diagram base
Primary request: Create a clean, text-free academic schematic base for a survey figure about feed-forward 3D reconstruction model families. Use a white background, thin muted blue and gray branching lines, six grouped lanes, and small empty rounded rectangles as label placeholders. The layout should suggest a root method branching into matching, multi-view, streaming memory, dynamic 4D, test-time mechanisms, and renderable output. No readable text, no logos, no icons, no 3D renderings, no gradients, no decorative effects. Leave enough blank space inside placeholders for labels to be added later in Typst.
```
