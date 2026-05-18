# 新对话续作提示词（直接复制给 agent）

> 把下面这段整段贴给新对话里的 agent；它就能从当前状态接着干。

---

你接手一篇中文 LaTeX 3R / feed-forward 3D reconstruction 综述，工作目录 `E:\kykt\Dream\3R-mix`。

**强制先读**（按顺序）：

1. `NEW_CHAT_HANDOFF.md` —— 项目顶层状态、决策、未完成任务列表。
2. `notes/work_log.md` —— 按日期顺序的细粒度编辑记录；最近三条 2026-05-13 的条目尤其重要。
3. `notes/figure_prompts.md` —— 图/表清单和 `figures/` 缓存状态表。
4. `main.tex` 全文（约 13 页 PDF 量级，可一次读完）。

**当前状态摘要**（读完上面后应当与你看到的一致；不一致以文件为准）：

- 主稿 `main.tex` 共 10 节、5 张 booktabs 表、4 张 TikZ 图（`fig:lineage` / `fig:paradigm` / `fig:memory` / `fig:application`），43 条参考文献全部显式引用，`build/main.pdf` 为 13 页可正常打开。
- `figures/` 下有四张已重新裁切的论文 Fig.1：
  - `dust3r_fig1.png` 1365×630（已视觉复核通过）
  - `vggt_fig1.png` 1380×465（已视觉复核通过）
  - `monst3r_fig1.png` 1310×435（已视觉复核通过）
  - `cut3r_fig1.png` 1385×360（**未视觉复核**，上次 Read 被 API 拒绝）
  - 这些图**没有**嵌入 `main.tex`。
- 上一轮没改 `main.tex`、没重新编译；PDF 与 2026-05-13 图像优化轮次的版本一致。

**顶部未完成任务**（用户未指定优先级时按这个顺序处理；用户指定就听用户的）：

1. 论文 Fig.1 嵌入决策（前置：CUT3R 视觉复核 + 逐篇许可证确认）。
2. 逐篇核对核心论文实验表（MV-DUSt3R+ / VGGT / Fast3R / TTT3R）。
3. 2026 预印本代码与许可证核对（LoGeR / Mem3R / OVGGT / PAS3R / FILT3R / RayMap3R / LongStream）。
4. 样式备份（改投时复检 `unsrtnat` + `ctex` 兼容性）。

**硬约束（不要违反）**：

- 不在 `main.tex` 中出现 KYKT / Dream / Dream3R / agent / skill / workflow / 本地项目 等内部语境词（用 Grep 校验）。
- 不在没有逐篇核对复用许可证的情况下，往 `main.tex` 插入 `\includegraphics` 引用 `figures/<name>_fig1.png`。要嵌入先和用户确认许可证。
- 不引入未在 `references.bib` 出现的新 bib key 而不补条目；新增条目时保持 `unsrtnat` 兼容。
- 不复活 Typst 路线；`main.typ` 是历史快照，不维护。
- 不在 Windows 本地装 PyTorch / conda env / 跑 3R 模型。模型推理在远程 `/hdd3/kykt26/`，本地仅做综述写作和图像裁切等编排工作。
- 默认 bash 工具；需要 Windows 原生语义时用 `pwsh -NoProfile -Command "..."`（不要用 `cmd /c`）。
- 不写带 emoji 的文档（除非用户要）。

**编译命令**（任何改完 `main.tex` 后跑一遍；4 步顺序固定）：

```bash
cd e:/kykt/Dream/3R-mix
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
bibtex  build/main
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
```

预期：13 页、0 error / 0 undefined / 0 Overfull、7 Underfull（CJK 表格列宽，已容忍）、MiKTeX 的 "unsupported Windows" 警告可忽略。

**汇报方式**：

- 实质性改完后追加一条 `## YYYY-MM-DD — <主题>` 到 `notes/work_log.md`，写清改了哪些文件、为什么、build 结果。
- 顶层状态变化（章节增删、未完成任务推进、新决策）同步更新 `NEW_CHAT_HANDOFF.md` 的对应小节和 "最后更新时间"。
- 不要再写新的 markdown 文件（如 NEW_CHAT_HANDOFF_v2.md 之类）；就维护现有这两个加 `notes/figure_prompts.md`。

**第一步建议**：先问用户本轮要推进上面四项里的哪一项；不要替用户决定走嵌入图像那条（因为它被许可证 gate 住）。如果用户没说，默认问"想接着上轮的图像嵌入决策（需要先和你确认四篇论文的复用许可），还是改成做实验表/预印本核对？"。
