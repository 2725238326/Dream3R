# 3R survey — handoff state

This file is the top-level handoff for the 3R survey project at `E:\kykt\Dream\3R-mix`.
It is updated after every substantive editing pass. For fine-grained history see `notes/work_log.md`.

## 当前目标

将 LaTeX 中文 3R / feed-forward 3D reconstruction 综述打磨成一篇结构清楚、证据可追溯、语言克制的综述论文。主稿为 `main.tex`，BibTeX 为 `references.bib`，PDF 输出 `build/main.pdf`。

## 当前稿件状态

- 框架：LaTeX（`ctexart`，`xelatex` 编译，`natbib`/`unsrtnat`）。已彻底放弃 Typst 路线，`main.typ` 仅作为历史快照保留，不再维护。
- 主稿：`main.tex`，最后更新 2026-05-14（在 2026-05-13 终稿再精炼基础上做了一次 wind-down 后质量优化：删 `fig:application` 与三处定义重述、统一表头为"适用条件与局限"、补 CroCo 与 MASt3R 机制段、加 §10 failure modes 段与 `fig:timeline`）。
- PDF：`build/main.pdf`，18 页，可正常打开。
- 阶段终稿输出：`deliverables/3r_survey_stage_final_2026-05-13.pdf`，17 页 A4，已按最终编译结果复制。
- 阶段终稿优化版：`deliverables/3r_survey_stage_final_2026-05-13_polished.pdf`，17 页 A4，已写入 PDF 元数据，LaTeX 日志清至 0 warnings / 0 underfull / 0 overfull。
- 图注与语言优化版：`deliverables/3r_survey_stage_final_2026-05-13_caption_polished.pdf`，16 页 A4，图注更短，正文去掉了偏过程汇报的“边界/不是/不把”式表述。
- 当前推荐交付版：`deliverables/3r_survey_stage_final_2026-05-15_natural.pdf`，18 页 A4，2026-05-15 prose naturalization 轮次产出（在 2026-05-14 quality 版基础上重写了 10 个段落，清掉编号列表式骨架、平行对仗、"X 的意义在于 / 综上所述"等 LLM 套话、以及"承接 / 消费 / 交付物"等工作流词汇）。
- 章节结构（共 10 节）：
  1. 引言
  2. 从传统几何流程到点图表示
  3. 基础谱系：DUSt3R、MASt3R 与 SfM 接口
  4. 多视角规模化与统一视觉几何
  5. 视频、动态场景与 4D 重建
  6. 长序列重建中的状态、记忆与缓存
  7. 测试时验证、修正与先验输入
  8. 从几何预测到可查看输出
  9. 应用证据、复现与失败样本记录
  10. 开放问题与结论
- 表格：5 张（`tab:foundation`, `tab:dynamic`, `tab:memory`, `tab:testtime`, `tab:application`），均使用 booktabs，最后一列统一为"适用条件与局限"。
- 图：6 张 figure 环境。其中 4 张 TikZ（`fig:lineage`、`fig:paradigm`、`fig:memory`、`fig:timeline`），2 张论文原图复合图（`fig:paper-core` 含 DUSt3R/VGGT Fig.1，`fig:paper-dynamic-stream` 含 MonST3R/CUT3R Fig.1）。论文图均在 caption 中以 `\citet{...}` 归属。原 `fig:application` 在 2026-05-14 质量优化轮次中删除（与 `tab:application` 信息重叠）。
- 参考文献：44 条，全部在正文中至少被引用一次，已移除 `\nocite{*}`；2026-05-14 加入 CroCo 后从 43 → 44。
- `figures/` 中四篇论文 Fig.1 裁切缓存（DUSt3R / VGGT / MonST3R / CUT3R）已嵌入 `main.tex`。嵌入 gate 根据用户 2026-05-13 的复用许可确认解除；详见“论文 Fig.1 嵌入与证据核对轮次”小节。

## 本轮已完成修改（2026-05-13）

按章节、图、表、参考文献分类：

- **章节**：
  - 移除作者行 "KYKT Dream 调研组"，改为空。
  - 将旧 §3（DUSt3R/MASt3R + 多视角）拆为 §3（DUSt3R/MASt3R/SfM 接口）和 §4（多视角规模化与统一视觉几何）。
  - 新增 §9（应用证据、复现边界与失败样本记录），并把应用图和应用矩阵表移入。
  - 把旧 "讨论" + "结论" 两节合并为 §10（开放问题与结论）。
- **正文**：
  - 重写摘要，使其先讲问题分支组织线索，再列代表模型；显式提出三类证据（论文 / 官方仓库 / 本地复现）。
  - 引言"证据边界"段去掉"流程跑通 ≈ 质量领先"的措辞，改为"接口和依赖成立 ≠ 几何质量更优"。
  - 动态场景段去掉"通常被视为...重要代表"、"应更克制地理解"等评议化措辞，改为机制直述；末句明确"4D pointmap / dynamic mask / 4DGS asset"不是同一输出。
  - 长序列段从单段堆名改为四类（空间指针 / causal-autoregressive / hybrid memory / 预算治理与滤波），每类一句机制描述。
  - 测试时段拆为三段：Test3R vs TTT3R 区分、G-CUT3R vs Pow3R vs MASt3R-SfM 的先验进入位置、外部先验（Depth Pro / Metric3Dv2 / DINO / CoTracker / SpatialTracker / SAM2）的辅助角色与冲突风险。
  - 输出段（§8）梳理 Splatt3R / InstantSplat / NoPoSplat 的具体差异。
  - §9 显式定义"paper-proven / official-code / local-smoke-test / application-validated / 尚需确认"四级证据，并与 `fig:application` 和 `tab:application` 对齐。
  - §10 把原讨论的四点合并为一段开放问题，再以一段收束。
- **图**：仅 `fig:application` 因章节移位换位；TikZ 内容未改。
- **表**：
  - `tab:foundation` 内"领先"/"SOTA"措辞替换为"更优"/"按实验表引用"。
  - `tab:application` 同样把"领先"替换为"更优"，并把"系统报告"行的过度表述改为"质量已验证"。
  - **新增** `tab:testtime`（测试时机制与先验输入的进入位置和证据边界，9 行）。
- **参考文献**：删除 `\nocite{*}`；确认 43 个 bib key 都在正文显式引用，BibTeX 0 warning。

## 图像优化轮次（2026-05-13 续编）

- **新增** `fig:paradigm`（TikZ，§2 内）：两行对照——上排为传统 SfM/MVS 五阶段，下排为 3R 前馈四阶段。位置在"三个直接后果"段与谱系段之间，§2 末段加了 `\,\ref{fig:paradigm}` 引用。配色与既有 TikZ 图一致（细线、白底、灰蓝弱填充）。
- **微调** `fig:lineage` 中长序列分支标签：原 `CUT3R；Spann3R；Point3R；STream3R；LONG3R；LoGeR；Mem3R；OVGGT` 单行，改为两行（每行四个），并补 `等` 字以反映 §6 正文实际覆盖（含 PAS3R/FILT3R/LongStream）。
- **重写** `notes/figure_prompts.md`：清除残留的 Typst 路线、KYKT 字眼与已过时的 Figure 6 计划；补当前 TikZ 图/booktabs 表清单，补 `figures/` 缓存说明与可选再裁切坐标。
- **暂不嵌入论文原图**：`figures/` 中保留 DUSt3R / VGGT / MonST3R / CUT3R 各自 Fig.1 的 PNG 缓存（外加 `*_p1-01.png` 原始页面位图），未在 `main.tex` 中插入 `\includegraphics`。理由：上一轮裁切质量混合（VGGT 截到了标题栏，DUSt3R 含一截 caption 文本，MonST3R/CUT3R 未视觉复核），且各论文复用许可证未独立核对，按优化提示词 §0.4 默认保守处理。再裁切坐标参考已写入 `notes/figure_prompts.md`。

## 论文 Fig.1 重新裁切轮次（2026-05-13 再续编）

- 用 `notes/figure_prompts.md` 中的 `crops_v2` 重跑了一遍 PIL 裁切，覆盖了 `figures/` 内四张 `*_fig1.png`。当前文件状态：
  - `dust3r_fig1.png` —— 1365 × 630，视觉复核通过（pointmap 输出+点云渲染，无 caption 残留）。
  - `vggt_fig1.png` —— 1380 × 465，视觉复核通过（房屋/花园重建+相机锥+深度图，已无标题栏）。
  - `monst3r_fig1.png` —— 1310 × 435，视觉复核通过（视频帧条+动态点云+输出标签 Video Depth / Camera Intrinsics / Dynamic & Static Mask）。
  - `cut3r_fig1.png` —— 1385 × 360，**未视觉复核**：Read 返回 `(media removed — rejected by API)`，原因未明（文件仅 623 KB）。下次在干净上下文里重试，或外部打开核对。
- **本轮没改 `main.tex`、没重新编译**：四张图仍然没有以 `\includegraphics` 形式嵌入。按 `notes/figure_prompts.md` § "Figure policy"，嵌入需先逐篇核对复用许可证。该核对未做。
- `build/main.pdf` 仍为上一轮的 13 页版本，未变。

## 论文 Fig.1 嵌入与证据核对轮次（2026-05-13 续编）

- 用户明确确认 DUSt3R / VGGT / MonST3R / CUT3R 四张论文 Fig.1 的复用许可没问题；据此解除嵌入 gate。
- `cut3r_fig1.png` 已在干净上下文视觉复核通过，并裁掉左侧页边残留；当前尺寸 1340 × 360。
- `main.tex` 新增 `\usepackage{placeins}`，用 `\FloatBarrier` 避免论文图漂到参考文献后。
- 新增两组论文图：
  - `fig:paper-core`：DUSt3R + VGGT 原论文 Fig.1。
  - `fig:paper-dynamic-stream`：MonST3R + CUT3R 原论文 Fig.1。
- 逐项推进了核心实验与项目状态核对：
  - MV-DUSt3R+：本地 PDF + 官方 GitHub 核对；正文只写 12/20 视角秒级示例、demo/权重存在，并保留实验条件边界。
  - Fast3R：本地 PDF + 官方 GitHub 核对；正文只写 1000+ 视角扩展和单 A100/分辨率条件，不写泛化排名。
  - VGGT：本地 PDF + 官方 GitHub 核对；正文写统一输出 camera/depth/pointmap/tracks，并指出代码/权重许可按版本区分。
  - TTT3R：本地 PDF + 项目页核对；`20 FPS / 6 GB` 已写成论文/项目页报告值，绑定硬件与序列设置。
  - 2026 预印本：LoGeR、Mem3R、OVGGT、RayMap3R 有项目/代码入口信号；LongStream 有项目页；FILT3R 标注 code will be released；PAS3R 仅稳定核到 arXiv 论文页。正文保持“机制已核对、代码与应用质量另行验证”的边界。
- `$imagegen` 技能已读取；本轮没有生成新图，因为论文来源图已满足需求，合成图会弱化论文证据链。

## 叙述结构与图文关系优化轮次（2026-05-13 再续编）

- `main.tex` 引言新增全文路线图：按“表示基础—输入扩展—时间机制—测试时校正—输出与证据”组织，而不是把模型排列成独立清单。
- §2 新增“图像材料三层使用”段落：
  - `fig:paradigm` + `fig:lineage`：综述重绘的概念框架。
  - `fig:paper-core` + `fig:paper-dynamic-stream`：原论文方法图的视觉锚点，只说明输入/几何中间量/输出形态，不作为性能或工程成熟度证据。
  - `fig:memory` + `fig:application`：本文重绘的系统抽象，分别对应长序列状态机制和应用证据路径。
- `fig:lineage` 后新增 `\FloatBarrier`，避免新增读图段落被谱系图浮动切开。
- §4 围绕 `fig:paper-core` 改写过渡：DUSt3R 对应 pointmap 中间语言，VGGT 对应 camera/depth/pointmap/tracks 统一预测；随后用 `tab:foundation` 汇总输入情形、主要输出、机制定位和证据边界。
- §6 围绕 `fig:paper-dynamic-stream` 改写过渡：MonST3R 对应动态几何估计，CUT3R 对应连续输入状态更新；原论文视觉锚点之后再回到四类状态/记忆机制。
- `notes/figure_prompts.md` 已补 Figure reading order 小节，并修正当前图清单顺序。

## 阶段终稿输出轮次（2026-05-13 最终收口）

- 按用户要求输出本阶段成果终稿。
- `main.tex` 做了最后一轮轻量论文语言收口：
  - 摘要中的证据口径改为“论文机制、官方仓库与复现记录”。
  - §9 的 evidence tier 从英文工作流标签改为中文论文表述：论文可证、官方代码、复现烟测、应用验证。
  - `tab:application` 的系统报告行改为“不把‘可运行’写为‘质量已验证’”。
- 最终 PDF 复制到 `deliverables/3r_survey_stage_final_2026-05-13.pdf`。

## 阶段终稿后优化轮次（2026-05-13 再收口）

- 用户确认继续推进四项优化：表格排版、证据术语统一、结论压缩、PDF 元数据。
- `main.tex` 改动：
  - 在 `hyperref` 后补 `\hypersetup`，写入 PDF Title / Subject / Keywords。
  - `tab:foundation` 与 `tab:testtime` 使用显式 `\makecell` 换行，解决中英文混排窄列拉伸。
  - §9、`fig:application`、`tab:application` 与结论统一使用“接口烟测 / 应用验证”口径。
  - 结论末段压缩模型名枚举，保留核心判断：3R 的问题是组织几何中间量与证据链，而不是端到端替代所有几何流程。
- 重新编译后，`build/main.pdf` 仍为 17 页 A4。
- 最终日志扫描结果：0 LaTeX errors，0 undefined refs/cites，0 Overfull，0 Underfull，0 matched LaTeX warnings。
- `pdfinfo` 已确认 PDF metadata 生效。
- `deliverables/3r_survey_stage_final_2026-05-13.pdf` 被其他进程占用，未能覆盖；优化版另存为 `deliverables/3r_survey_stage_final_2026-05-13_polished.pdf`。

## 图注与语言自然化轮次（2026-05-13 再再收口）

- 按用户反馈压缩所有主要 figure/table caption，尤其是 `fig:paradigm`、`fig:lineage`、`fig:paper-core`、`fig:paper-dynamic-stream`、`fig:memory`、`fig:application` 与 `tab:application`。
- 正文进一步去掉偏过程汇报的写法：将“证据边界”“不是/而非/不把/不写”等框架化句式改为更自然的论文叙述。
- `tab:foundation`、`tab:dynamic`、`tab:testtime`、`tab:application` 的最后一列统一为“使用口径/使用提示”一类表达，减少告诫式措辞。
- 第 9 节标题固定为“应用证据、复现与失败样本记录”，正文使用“论文可证 / 官方代码 / 跑通记录 / 应用验证”四类材料组织判断。
- 重新编译后 `build/main.pdf` 为 16 页 A4，另存为 `deliverables/3r_survey_stage_final_2026-05-13_caption_polished.pdf`。
- 最终日志扫描：0 LaTeX errors，0 undefined refs/cites，0 Overfull，0 Underfull，0 matched LaTeX warnings。内部语境词扫描和“证据边界/不是/而非/不把/接口烟测”等旧表述扫描均无命中。
- 视觉抽查渲染 pages 5、8、10：两组论文图、长序列图和应用证据段落排版正常，图注已明显缩短。

## 终稿再精炼轮次（2026-05-13 最后优化）

- 摘要重写为更标准的论文摘要结构：问题背景、分支谱系、证据来源、核心判断。
- 图 3 / 图 4 caption 继续缩短，但保留明确来源归属：
  - `DUSt3R 与 VGGT 方法图对照。来源：DUSt3R \citet{dust3r}，VGGT \citet{vggt}。`
  - `MonST3R 与 CUT3R 方法图对照。来源：MonST3R \citet{monst3r}，CUT3R \citet{cut3r}。`
- 表格最后一列统一为更自然的“记录要点”；`tab:memory` 的最后一列改为“典型风险”。
- 第 9 节新增一条六项复现记录模板：输入来源与规模、模型和权重版本、运行环境、主要输出、失败样本、许可证与耗时/显存。
- 结论末段强化核心判断：3R 的主要贡献既来自模型指标提升，也来自对中间表示、状态更新、外部先验和可查看资产的重新编排。
- 重新编译后 `build/main.pdf` 仍为 16 页 A4，另存为 `deliverables/3r_survey_stage_final_2026-05-13_refined.pdf`。
- 最终日志扫描：0 LaTeX errors，0 undefined refs/cites，0 Overfull，0 Underfull，0 matched LaTeX warnings。内部语境词和旧式汇报词扫描均无命中。
- 视觉抽查 pages 1、5、8、10：摘要、两组论文图和应用段落排版正常。

## 项目收口 / Release Closeout（2026-05-14）

用户确认综述以 arXiv-only 自存档为终点，不再投递期刊或会议（route C）。本轮按"尽快收口"原则做卫生项与历史标记：

- **README.md** 重写为 LaTeX-only 入口，明确当前交付、编译命令、目录约定与 Typst 时代历史快照说明。
- **GENERATION_PROMPT.md** 缩为一句话历史指针，原 Typst-era 生成提示词不再作为活动指引。
- **顶层 Typst legacy**（`main.typ`、`bib.yaml`）添加 DEPRECATED 头注，`review-template.typ` 作为 `main.typ` 的从属模板未单独标注。
- **`.gitignore`** 复核通过：`/papers/`、`/build/`、`/guidance_skills/` 三项排除条目齐全。
- **`references.bib`** 复核：43 个唯一 bib key，无重复。

### 发布前检查清单（Release checklist）

任何打算公开（含 arXiv 上传）的版本，按下面流程过一遍：

1. **重新编译**：`xelatex` → `bibtex build/main` → `xelatex` → `xelatex`，确认 0 errors / 0 undefined refs/cites / 0 Overfull / 0 Underfull / 0 warnings。
2. **禁用词扫描**（`Grep` `main.tex`）：`KYKT`、`Dream`、`Dream3R`、`agent`、`skill`、`workflow`、`本地项目` 不应出现。
3. **页数与文件大小**：`build/main.pdf` 当前为 18 A4 页，约 2.85 MB；与 `deliverables/3r_survey_stage_final_2026-05-14_quality.pdf` 对齐。
4. **图引用检查**：6 张 figure（4 张 TikZ + 2 张论文 Fig.1 复合）的 caption 均保留来源 `\citet{...}`。
5. **PDF metadata**：`pdfinfo` 应显示 Title / Subject / Keywords。
6. **论文截图许可证**：当前嵌入的 DUSt3R / VGGT / MonST3R / CUT3R 已确认复用许可。若新增任何论文截图，须逐篇重新确认。

## 关键决策

- 继续使用 LaTeX，不回到 Typst。
- Easi3R 仅在动态 3R / training-free motion disentanglement 机制中讨论；不放在主线中心。
- 论文 Fig.1 可在复用许可确认后嵌入；当前四张已嵌入并在 caption 中保留来源归属。其他新增论文截图仍需逐项确认许可。
- 应用证据矩阵明确标注"系统报告"行，把"流程跑通≠质量已验证"作为系统层规则写入正文。
- 正文中不出现 KYKT / Dream / Dream3R / agent / skill / workflow / 本地项目 等内部语境词（已 `Grep` 校验）。

## 证据口径

正文按四类材料组织判断：

- **论文可证**：DUSt3R / MASt3R / Fast3R / VGGT / CUT3R / Spann3R / MonST3R / Test3R 等核心模型的机制描述来自论文摘要、正文或方法图。
- **官方代码 / 项目页**：说明仓库、项目页、权重或 demo 入口存在；具体许可证、显存、依赖按仓库版本另行核对。
- **跑通记录**：记录特定环境下接口、依赖和默认输入是否成立，不直接扩展为质量判断。
- **来源级核对**：MV-DUSt3R+、Fast3R、VGGT、TTT3R 的关键数字已按论文/项目页条件写入正文；LoGeR、Mem3R、OVGGT、RayMap3R、LongStream、FILT3R、PAS3R 已推进到来源状态描述。

## 编译命令与结果

最近一次（2026-05-13，终稿再精炼后）：

```bash
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
bibtex  build/main
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
```

结果：

- 16 页 PDF 正常输出至 `build/main.pdf`。
- 0 × undefined citation / undefined reference。
- 0 × LaTeX Error。
- 0 × `Overfull \hbox`。
- 0 × `Underfull \hbox`（阶段终稿后优化轮次已清理表格窄列拉伸）。
- MiKTeX 在 Windows 11 Home China 10.0.29585 上仍打印 "running on an unsupported version of Windows"。PDF 正常生成，记录为环境警告，不视为稿件失败。
- 视觉 QA：渲染 pages 1、5、8、10，确认摘要、两组论文复合图、长序列图和应用证据段落排版正常，caption 已压缩且来源归属仍保留。

## 未完成任务（按优先级）

> **注**：项目已按 route C（arXiv-only）收口于 2026-05-14。以下三项均为"如未来想再展开"的可选工作，不在当前推进清单中。

1. **更深的 benchmark meta-analysis（可选）**：MV-DUSt3R+ / Fast3R / VGGT / TTT3R 已做来源级核对；若要写更强结论，需要逐表抽取数据集、视角数、分辨率、硬件、指标口径并做横向表。
2. **2026 预印本软件许可细读**：LoGeR、Mem3R、OVGGT、RayMap3R、LongStream、FILT3R、PAS3R 已推进到项目/论文来源状态；若要复用代码、权重或截图，需要逐仓库读 LICENSE / checkpoint terms。
3. **样式备份**：如计划改投，提前确认 `unsrtnat` 与 `ctex` 是否在目标期刊/会议模板兼容。

## 风险与注意事项

- D²USt3R 标题在 `references.bib` 中使用 `\textsuperscript{2}`；当前 `unsrtnat` 风格下渲染正常，更换风格时应复检。
- `MiKTeX` 在当前 Windows 系统会持续打印 "unsupported Windows" 警告，但不影响输出。如换为 TeXLive 可消除该警告。
- `papers/`、`build/`、`guidance_skills/` 仍按 `.gitignore` 排除；不要无意中把生成 PDF 或第三方 PDF 提交进版本控制。
- 原 Typst 稿（`main.typ`、`review-template.typ`、`bib.yaml` 等）保留为历史快照，不再维护；如未来仍需 Typst 版本，应在 handoff 中重新声明。

## 质量优化轮次（2026-05-14 wind-down 后）

用户在 wind-down 后追加要求做一轮批判性质量复审。我识别了三档问题，按 Tier A 全部 + Tier B 高杠杆部分执行（计划文件 `C:\Users\27252\.claude\plans\greedy-petting-lemur.md`，17 项归 A/B/C 三组）；Tier C（评测/数据集章节、critical evaluation、narrative restructuring）按 wind-down 节奏跳过。

- **A 组（去重 5 项）**：删 `fig:application`（与 `tab:application` 重叠）；删 §1 末段四类材料重述与 §2 末段"图像材料三层使用"段（与摘要 / §1 / §9 重复）；剥离 `tab:foundation` / `tab:dynamic` / §6 末段三处"应用质量另行复验"变体（§9 保留唯一权威说明）；§10 两段合并为一段，把核心判断与失败/许可证注脚收束在一起。
- **B 组（语言精修与表头统一 8 项）**：摘要"三类依据 / 工程成熟度"改为"四类依据 / 实现状态"；§3 删生造词"接口转向"改为"几何中间层"；表格里删法律语言"代码/权重许可需按版本区分"；§7 与 `tab:testtime` 中的 "prompt tuning" 改为"一致性优化"（避免与 prompt learning 混淆）；§9 开头由列表式定义改写为一段散文；5 张表最后一列统一为**"适用条件与局限"**，正文从告诫语气改为机制语气。
- **C 组（内容补充 4 项）**：补 CroCo 引用（`@misc{croco}` + §3 一句话），bib 43 → 44；§3 加一段 MASt3R 机制说明（dense local feature head + descriptor 对比损失 + 互最近邻 + Sinkhorn）；§10 首段加 6 类典型失败 modes（弱纹理 / 镜面玻璃 / 快速运动 / 长基线 / 尺度漂移 / 域外场景）；§2 `fig:lineage` 之后新增 `fig:timeline`（TikZ，2023–2026 横轴 × 5 track，覆盖所有引用模型）。

**编译结果**：18 页 A4，2.85 MB；0 errors / 0 undefined / 0 Overfull / 0 Underfull / 0 warnings；禁用词与旧式工作流措辞扫描均 0 命中。

**新交付**：`deliverables/3r_survey_stage_final_2026-05-14_quality.pdf`（2,847,531 bytes）。supersedes 2026-05-13 refined 版。页数从 16 → 18 的增量来自新增 §3 MASt3R 段、§10 failure modes 段与 `fig:timeline`；非冗余增长，按 wind-down 节奏接受。

## 最后更新时间

2026-05-15（在 2026-05-14 quality 版基础上做 prose naturalization 轮次：重写摘要 / §1 / §2 / §3 / §4 / §5 / §6 / §7 / §8 / §9 / §10 共 10 个段落，删 LLM 套话、平行对仗、编号列表骨架、工作流词汇；编译 0 errors / 0 warnings；PDF 仍 18 页 2.85 MB；新推荐交付版 `deliverables/3r_survey_stage_final_2026-05-15_natural.pdf`）。
