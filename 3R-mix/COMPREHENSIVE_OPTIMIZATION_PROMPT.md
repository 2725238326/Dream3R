# 3R 综述全面优化提示词

使用对象：继续优化 `E:\kykt\Dream\3R-mix` 中中文 3R / feed-forward 3D reconstruction 综述的后续对话或 agent。

当前项目已经从 Typst 切换到 LaTeX。主稿为 `E:\kykt\Dream\3R-mix\main.tex`，参考文献为 `E:\kykt\Dream\3R-mix\references.bib`，编译产物应输出到 `E:\kykt\Dream\3R-mix\build\main.pdf`。请以“正式中文学术综述”为目标，而不是继续做模板调参、模型清单堆叠或项目汇报稿。正文主题只讨论 3R / feed-forward 3D reconstruction 研究，不要把 KYKT、Dream、Dream3R 或本地项目经验写进主线。

## 0. 工作目录与状态管理

本项目需要能被其他对话和 agent 无缝接手。开始工作前、阶段切换时、结束前都要维护清楚的工作状态。

### 0.1 工作范围

- 工作目录固定为 `E:\kykt\Dream\3R-mix`。
- 不要修改 Dream 其他目录，除非只是读取资料。
- 不要删除或重置用户已有文件。
- `papers/`、`build/`、`guidance_skills/` 是大文件或生成目录，应保持忽略状态。
- 原 Typst 文件可以保留作为历史版本，但新的正式稿以 LaTeX 为准。

### 0.2 启动时必须读取

先读取以下文件，再决定修改策略：

- `E:\kykt\Dream\3R-mix\main.tex`
- `E:\kykt\Dream\3R-mix\references.bib`
- `E:\kykt\Dream\3R-mix\COMPREHENSIVE_OPTIMIZATION_PROMPT.md`
- `E:\kykt\Dream\3R-mix\NEW_CHAT_HANDOFF.md`（如存在）
- `E:\kykt\Dream\3R-mix\notes\model_inventory.md`
- `E:\kykt\Dream\3R-mix\notes\paper_inventory.md`
- `E:\kykt\Dream\3R-mix\notes\chapter_structure.md`
- `E:\kykt\Dream\3R-mix\notes\figure_selection.md`
- `E:\kykt\Dream\3R-mix\GENERATION_PROMPT.md`

不要主动引入工作目录外的内部项目资料。本文目标是 3R 综述，不是本地项目经验总结。除非用户明确要求，否则不要读取或引用 Dream3R、KYKT 路线图、内部 SOTA 矩阵、内部 registry 等资料。

### 0.3 交接状态文件

请维护 `E:\kykt\Dream\3R-mix\NEW_CHAT_HANDOFF.md`，用于下一轮对话或 agent 接续。每次完成一个实质阶段后更新一次，结束前必须更新。

`NEW_CHAT_HANDOFF.md` 至少包含：

- 当前目标：一句话说明本轮在优化什么。
- 当前稿件状态：`main.tex` 是否已更新，`build/main.pdf` 是否可编译。
- 已完成修改：按章节、图、表、参考文献列出。
- 关键决策：例如“继续使用 LaTeX，不回到 Typst”“Easi3R 只放在动态机制表中”“不直接嵌入论文截图”。
- 证据边界：哪些结论来自论文，哪些来自官方仓库，哪些只是本地 smoke test，哪些尚需确认。
- 编译命令和结果：最近一次命令、是否成功、日志中是否有 undefined citation / overfull hbox。
- 未完成任务：按优先级列出下一步。
- 风险与注意事项：例如 2026 预印本代码状态、许可证、实验表未逐项核对等。
- 最后更新时间：使用绝对日期和时间。

请同时维护 `E:\kykt\Dream\3R-mix\notes\work_log.md`。它是追加式日志，不替代 handoff。每次较大修改后追加：

- 时间。
- 修改文件。
- 修改原因。
- 验证结果。
- 下一步。

### 0.4 文件管理规则

- 主稿只改 `main.tex`，不要另起一个主文件，除非用户明确要求。
- BibTeX 统一放在 `references.bib`。
- 图如果是 TikZ 概念图，优先内嵌在 `main.tex`；如果以后拆分，放入 `figures/` 并在 handoff 中记录。
- 不要直接嵌入论文 PDF 截图，除非确认版权和引用许可。
- 如果使用 AI 生成图，必须把提示词写入 `notes/figure_prompts.md`，并且生成图只做非文本背景或概念插图，精确标签必须由 LaTeX/TikZ 添加。
- 新下载 PDF 放入 `papers/`，并更新 `notes/paper_inventory.md`。
- 大文件和生成文件不要纳入 git 跟踪。

## 0.5 Skill 使用要求

如果当前环境可用相关 skill，请按以下优先级使用；如果 skill 不可用，则采用同等方法论手动执行，不要因为缺 skill 停止工作。

### 首选研究流程 skill

- 优先使用 `kthorn/research-superpower` 或等价的系统性文献检索/综述 skill。
- 如同时可用 `academic-research-skills`、`deep-research`、`academic-paper`、`academic-paper-reviewer`、`academic-pipeline` 等 skill，可组合使用。
- 使用 skill 的目标是改进文献筛选、证据分层、论证组织、语言正式性和质量检查，而不是引入复杂流程空转。

### Skill 应落实到这些动作

1. 把研究问题写清楚：3R 范式、pointmap 表示、多视角统一几何、动态场景、长序列记忆、测试时修正、Gaussian 输出。
2. 对文献做相关性分层：核心文献、机制补充、支撑先验、输出表示背景、尚需确认。
3. 对每个模型抽取固定字段：问题设置、输入假设、输出表示、核心机制、与 DUSt3R/VGGT/CUT3R 等主线的关系、局限、证据来源。
4. 检查叙述是否有证据：论文机制、官方仓库、本地复现、应用验证必须分开。
5. 做反向审稿：删除无证据排行、宣传口吻、机械堆名、AI 腔段落。
6. 形成最终 handoff：记录已完成、未完成、编译状态和事实风险。

### Skill 使用边界

- 不要把 skill 的工作流术语写进论文正文。
- 不要在正文中提到 “research-superpower”“agent”“pipeline”“skill”。
- 不要为了展示流程而制造过多中间文件；必要状态写入 `NEW_CHAT_HANDOFF.md` 和 `notes/work_log.md` 即可。
- 不要把任何本地调研框架写成 3R 领域贡献。

## 1. 总目标

将现有稿件打磨成一篇结构清楚、论证连贯、图表克制、引用可追溯的中文综述论文。主题是近期 3R / feed-forward 3D reconstruction 模型谱系，重点解释这些方法如何从 DUSt3R 式 pointmap 表示扩展到匹配、多视角统一几何、动态场景、长序列记忆、测试时修正和可渲染输出。

正文不要讨论 KYKT、Dream、Dream3R、本地路线图或内部项目经验。它们只属于工作目录背景和交接信息，不属于论文内容。若确需在“复现边界”中提到本地验证，也只能写成匿名、方法论式表述，例如“本地 smoke test 只能说明接口可运行，不代表质量已验证”，不要出现项目名。

## 2. 必须遵守的写作原则

1. 使用 LaTeX，不要回到 Typst。
2. 继续使用 `main.tex` 作为主文件，`references.bib` 作为 BibTeX 文献库。
3. 中文学术综述风格，语言自然、正式、克制。
4. 删除宣传腔、口号式总结和明显 AI 味表达，例如“颠覆、赋能、突破性、全流程闭环、空间智能、端到端解决一切”等。
5. 不做未验证性能排行，不写“全面领先”“SOTA 最强”“工程可用性最好”等无证据判断。
6. “代码可用、demo 可跑、流程跑通、项目页效果好”只能作为工程状态，不等同于重建质量领先。
7. 所有性能、SOTA、代码状态、权重可用性、应用可行性判断都必须有来源；无法确认时写“尚需确认”或降级为保守表述。
8. 论文图如果直接使用，必须确认许可；否则只可作为参考进行综述性重绘。
9. Easi3R 要讲到，但只放在动态 3R / training-free motion disentanglement 机制中，不要写成主线中心。
10. 图表必须像文献综述：booktabs 横线表、细线 TikZ 图、白底、克制，不要粗线海报风，不要信息墙。

## 2.1 语言风格与正式性要求

全文要像中文学术综述，而不是技术博客、项目报告、PRD、路演稿或 agent 生成笔记。

### 推荐风格

- 句子应清楚、平实、有判断边界。
- 段落应围绕一个技术问题展开：问题设置、机制、与相关方法关系、局限。
- 比较应落在输入假设、输出表示、几何约束、时间建模、测试时机制和证据类型上。
- 对新近预印本保持克制语气，避免下结论过满。
- 中文为主，必要技术名保留英文，如 pointmap、confidence、test-time training、Gaussian Splatting。
- 模型名第一次出现时说明它在谱系中的位置，后文避免反复介绍。

### 禁止风格

- 不要使用宣传词：颠覆、赋能、突破性、革命性、全流程闭环、空间智能、工业级、极致、领先、最强。
- 不要使用空泛套话：具有广阔前景、意义重大、效果显著、表现优异、充分证明。
- 不要使用 AI 腔连接：值得注意的是、与此同时、进一步地、综上所述地推进、从某种意义上说。
- 不要把模型名称堆成清单式段落。
- 不要把“可以”“能够”“支持”连续堆叠；需要说明在什么输入、什么约束、什么证据下成立。
- 不要在正文中出现“我们这个项目”“本地 Dream”“KYKT 集成”“agent”“skill”“工作流”等内部语境。

### 建议改写方式

- 把“该方法显著提升重建质量”改为“论文在若干基准上报告了改进；具体适用范围仍取决于输入视角、相机条件和动态干扰”。
- 把“该模型可直接落地”改为“官方仓库提供代码或 demo；实际应用仍需核对权重许可证、显存需求、失败样本和质量指标”。
- 把“实现端到端 3D 重建闭环”改为“将若干几何中间量放入同一前馈预测框架，但全局一致性和测试时质量检查仍需额外处理”。
- 把“Easi3R 是重要突破”改为“Easi3R 可作为 training-free 动态修正机制的例子，用于说明从既有 DUSt3R 表征中分离运动的可能性”。

## 3. 先诊断当前稿件

先做内部诊断，再修改。诊断不必单独交付，但必须据此行动。

诊断重点：

1. 当前文章是否像正式综述，还是像模型清单。
2. 章节之间是否有论证递进，而不是简单分类罗列。
3. 摘要和引言是否清楚提出综述对象、问题背景、范围边界和证据标准。
4. 每个模型是否服务于机制分类，而不是为了覆盖名单硬塞进去。
5. 图表是否帮助读者理解谱系、机制和应用证据。
6. 是否存在夸大、无来源、AI 腔或项目宣传口吻。
7. 是否有表格太宽、图太密、标题过大、图文不协调等排版问题。
8. `NEW_CHAT_HANDOFF.md` 是否足够让下一轮 agent 接续；不足则先补齐。

## 4. 重新确定综述问题

请围绕以下研究问题重写文章主线：

1. DUSt3R 式 pointmap 表示相对于传统 SfM/MVS 改变了什么？
2. 后续 3R 模型分别在解决哪些未解决问题：匹配、多视角规模化、统一几何预测、动态场景、长序列状态、测试时修正、可渲染输出？
3. 这些分支之间是互补关系、接口关系还是问题设置不同，而不是简单性能先后关系？
4. 哪些能力来自 3R 主模型，哪些来自外部先验，如 Depth Anything、DINO、CoTracker、SAM2、SpatialTracker、Depth Pro、Metric3D v2？
5. 从研究模型走向真实应用时，哪些证据必须被记录：输入条件、输出表示、质量信号、失败样本、许可证、显存/耗时、代码/权重状态？

## 5. 建议最终章节结构

将 `main.tex` 调整为以下结构，必要时可微调标题，但逻辑顺序不要乱。

### 1. 引言

- 传统 SfM/MVS 的基本流程和局限。
- DUSt3R 后 3R / feed-forward reconstruction 的范式变化。
- 本文综述范围：pointmap、visual geometry、streaming reconstruction、dynamic 3R、test-time adaptation、Gaussian output。
- 证据边界：论文机制、官方代码、本地复现、应用质量四类证据分开。

### 2. 从 SfM/MVS 到 pointmap 表示

- 传统流程：feature matching、pose estimation、triangulation、MVS、global optimization。
- DUSt3R 的 pointmap 和 confidence 为什么成为后续共同语言。
- pointmap 的优势：弱化相机先验、连接深度/匹配/位姿/点云。
- pointmap 的限制：尺度、全局一致性、动态干扰、长序列漂移。

### 3. 基础谱系：DUSt3R、MASt3R 与 SfM 接口

- DUSt3R：范式起点，不写成最终答案。
- MASt3R：3D-grounded matching，强调匹配而非简单替代 DUSt3R。
- MASt3R-SfM：把神经匹配重新接回传统 SfM，作为桥接机制。

### 4. 多视角规模化与统一视觉几何

- Fast3R：many-view one-forward-pass，重点是输入规模问题。
- MV-DUSt3R+：sparse-view、多视角 decoder、reference fusion。
- VGGT：camera、depth、pointmap、tracks 的统一视觉几何输出。
- MapAnything：metric feed-forward reconstruction 和可选条件输入。
- Pow3R：camera/scene priors 如何改变无约束重建问题。
- 重点讨论输入条件和输出几何量，不做无证据排行。

### 5. 视频、动态场景与 4D 重建

- 动态场景为何破坏静态 pointmap 假设。
- Align3R：深度先验与动态视频对齐，只作为桥接。
- MonST3R：motion-aware geometry。
- POMATO：pointmap matching + temporal motion。
- D^2USt3R：dynamic / 4D pointmap。
- Easi3R：training-free motion disentanglement from DUSt3R，不突出为主线中心。
- RayMap3R：inference-time RayMap 和动态抑制。
- 明确 4D pointmap、dynamic reconstruction、4DGS asset 不是同一件事。

### 6. 长序列重建中的状态、记忆与缓存机制

- CUT3R：persistent recurrent state。
- Spann3R：spatial memory。
- Point3R：explicit spatial pointer memory。
- STream3R / LongStream：causal 或 autoregressive streaming route。
- LONG3R / LoGeR / Mem3R：long sequence、local-global hybrid memory、tracking/mapping memory。
- OVGGT / PAS3R / FILT3R：fixed-budget cache、pose-adaptive update、latent-state filtering。
- 必须区分 recurrent state、external memory、hybrid memory、cache governance、filtering，不要统称“记忆增强”。

### 7. 测试时验证、修正与先验输入

- Test3R：triplet consistency / prompt tuning / test-time consistency。
- TTT3R：test-time training / state update。
- G-CUT3R：camera/depth prior guided reconstruction。
- MASt3R-SfM：classical consistency loop。
- Depth Anything、Depth Pro、Metric3D v2、DINO、CoTracker、SAM2、SpatialTracker 作为辅助先验，不喧宾夺主。
- 讨论先验冲突、计算成本、失败模式和质量证据。

### 8. 从几何预测到可查看输出

- point cloud、depth、confidence、camera、tracks、mesh、Gaussian 的不同角色。
- 3DGS / 4DGS 是渲染表示和资产层，不是 pose-free 3R 本身。
- Splatt3R、InstantSplat、NoPoSplat 如何把 3R 结果连接到 Gaussian 输出。
- 强调渲染 demo 不等于底层几何完全可信。

### 9. 应用证据、复现边界与失败样本记录

- 输入 regime、输出表示、质量信号、代码/权重状态、许可证、显存/耗时。
- 区分 paper-proven、official-code、local-smoke-test、application-validated、尚需确认。
- 说明为什么“流程跑通”不能写成“质量领先”。
- 只讨论一般性的复现证据记录方法，不出现 KYKT、Dream、Dream3R 或本地项目叙事。

### 10. 开放问题与结论

- 长序列漂移与状态污染。
- 动态/静态分离与非刚体运动。
- 先验冲突与测试时更新成本。
- metric scale、camera、depth、tracks 的一致性。
- Gaussian 输出的几何可信度。
- 许可证、复现成本和应用报告标准。
- 结论要收束到 3R 研究的结构性问题和发展方向，不要写口号。

## 6. 图表规划

图表数量宁可少而精，不要堆满页面。

### 图 1：3R 模型谱系图

- DUSt3R 为根。
- 分支包括：匹配/SfM、多视角统一几何、动态/4D、长序列记忆、测试时机制、Gaussian 输出。
- 只表达问题分支，不表达性能排序。
- 细线、白底、文字清晰，不要粗线、不用渐变、不用装饰图标。

### 图 2：从传统 SfM/MVS 到 pointmap 的范式变化

- 左侧传统流程：matching -> pose -> triangulation -> MVS/fusion -> BA。
- 右侧 3R 流程：image(s) -> pointmap/depth/confidence -> alignment/checking -> output representation。
- 用于帮助引言和第二节，而不是炫图。

### 图 3：长序列状态与记忆机制图

- recurrent state：CUT3R / STream3R。
- spatial/pointer memory：Spann3R / Point3R。
- hybrid memory：LONG3R / LoGeR / Mem3R。
- cache/update/filtering：OVGGT / PAS3R / FILT3R / LongStream。
- 强调机制差异。

### 图 4：应用证据路径图

- 输入图像/视频 -> 3R 几何预测 -> 一致性/置信度检查 -> 输出表示 -> 可视化/报告。
- 旁支记录：来源、失败样本、许可证、复现状态。
- 明确“可运行不等于质量验证”。

### 表 1：基础与多视角模型比较

列建议：模型、输入条件、输出表示、核心机制、证据边界。

### 表 2：动态 3R 机制对照

必须包含 Align3R、MonST3R、POMATO、D^2USt3R、Easi3R、RayMap3R。

列建议：动态问题入口、机制、输出/中间量、写作边界。

### 表 3：长序列与流式 3R 记忆原语

列建议：类别、代表工作、主要作用、潜在失败点。

### 表 4：测试时机制与先验输入

列建议：方法/先验、进入位置、修正信号、风险与证据边界。

### 表 5：应用证据矩阵

列建议：输出层、代表方法、质量信号、需要避免的过度表述。

### 表格要求

- 使用 booktabs，不使用竖线。
- 表格文字要能读，不要为了塞信息把字号压得过小。
- 英文长词可用 `\makecell` 或手动断行。
- 如果一张表太宽，拆成两张，不要硬塞。
- 表格标题要学术化，不要写“粗线表格”“能力大图”这类说明。

## 7. 文献覆盖要求

正文必须自然覆盖以下模型和先验，但不要机械罗列：

- DUSt3R
- MASt3R
- MASt3R-SfM
- Fast3R
- MV-DUSt3R+
- VGGT
- MapAnything
- Align3R
- Pow3R
- CUT3R
- Spann3R
- Point3R
- STream3R
- LONG3R
- LoGeR
- Mem3R
- OVGGT
- PAS3R
- FILT3R
- LongStream
- MonST3R
- POMATO
- D^2USt3R
- Easi3R
- RayMap3R
- Test3R
- TTT3R
- G-CUT3R
- Splatt3R
- InstantSplat
- NoPoSplat
- 3D Gaussian Splatting
- 4DGS / 4D Gaussian Splatting
- Depth Anything / Depth Anything V2
- DINOv2 / DINOv3
- CoTracker
- SAM2
- SpatialTracker
- Depth Pro
- Metric3D v2

覆盖方式：

- 主干模型在正文中解释。
- 辅助先验放在“先验输入”或表格中。
- 边缘模型可在机制表中出现，不必每个都写长段。
- 不要把模型名密集堆在一个段落里；每段应有明确论点。

## 8. 写作质量要求

逐段检查：

1. 每段开头应有明确主题句。
2. 每段只解决一个问题，不要同时塞入五个模型。
3. 模型比较要围绕输入假设、输出表示、机制差异、失败模式展开。
4. 少用“与此同时、此外、值得注意的是”这类机械连接词。
5. 不要写“该方向具有广阔前景”这种空话；改写为具体开放问题。
6. 不要把“可扩展、可验证、可部署”作为口号；必须说明扩展到什么、验证什么、部署受什么限制。
7. 删除“显著提升”“有效解决”等无实验来源形容。
8. 结论不要重复摘要，要提炼结构性认识。

## 9. 引用和事实检查

1. 正文关键断言必须有 `\citep{}`。
2. 所有 `references.bib` 中条目应能被 BibTeX 正确处理。
3. 对 2025/2026 年预印本保持保守语气。
4. 如果没有逐篇核对实验表，不要写“优于”“领先”“SOTA”。
5. 如果代码/权重/许可证没有从官方仓库确认，不要写“可直接落地”。
6. 可以写“论文声称”“官方仓库显示”“本地记录显示”，但不要混为同一种证据。
7. 对项目页和 GitHub 信息要标注为官方项目状态，不代表论文实验结论。

## 10. LaTeX 编译要求

使用以下手动编译流程，不依赖 `latexmk`：

```powershell
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
bibtex build\main
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
```

编译后检查：

1. `build/main.pdf` 存在。
2. `build/main.log` 不应有 undefined citations。
3. `build/main.log` 不应有 `Overfull \hbox`。
4. `Underfull \hbox` 可以接受少量表格断行导致的情况，但如果影响视觉要修。
5. MiKTeX 如果提示 unsupported Windows，但 PDF 正常生成，可记录为环境警告，不要误判为稿件失败。
6. 渲染抽查至少三页：第一页、主要图所在页、主要表格所在页。

## 11. 阶段推进建议

建议按以下阶段推进，阶段完成后更新 `NEW_CHAT_HANDOFF.md` 和 `notes/work_log.md`：

1. 诊断阶段：读取文件，确认当前稿件、参考文献、图表和编译状态。
2. 结构阶段：调整章节顺序、标题和段落主线。
3. 正文阶段：重写摘要、引言、核心章节和结论。
4. 图表阶段：重绘或精简 TikZ 图和 booktabs 表格。
5. 证据阶段：检查引用、保守化断言、标注尚需确认之处。
6. 编译阶段：完成 BibTeX 和 PDF 编译，修复日志问题。
7. 交接阶段：更新 handoff 和 work log，写明下一步。

## 12. 最终交付说明

最终回答必须简短说明：

1. 更新了哪些文件。
2. PDF 路径。
3. 编译是否通过。
4. 图表做了哪些调整。
5. `NEW_CHAT_HANDOFF.md` 和 `notes/work_log.md` 是否已更新。
6. 仍需人工确认的事实点，例如部分 2026 预印本的代码状态、许可证、实验表细节。

不要输出长篇自我评价，不要说“已经全面提升质量”这种空话。只报告事实。
