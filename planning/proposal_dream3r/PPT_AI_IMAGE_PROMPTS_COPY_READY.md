# PPT AI 绘图提示词（可整块复制版）

文件名：`ppt_assets/ai/F04_two_pillars_3840x2160.png`

```text
Canvas and size: 16:9 landscape, 3840 x 2160 px, high-resolution PNG.

Create a clean formal academic conceptual diagram for a Chinese thesis proposal PowerPoint. The figure shows two research pillars side by side, with a natural, restrained Beihang-style blue academic visual tone.

Content to include:
Left pillar title: 支柱 A：候选架构 X
Left pillar sub-items: 六模块架构；七专家池；算法创新；消融实验需求
Right pillar title: 支柱 B：聚合管理平台
Right pillar sub-items: 统一执行合同；七模型接入；调度执行基础设施；结果归集
Between the two pillars, draw two clear bidirectional arrows:
A → B：消融实验需求
B → A：调度执行基础设施
Add a small bottom statement: 贡献边界：提供对照数据与可复用平台，不宣称单一方案优越。

Layout requirements:
Two balanced vertical pillar blocks, left and right, aligned to the same baseline.
Use enough whitespace around the pillars so the figure can fit under a PowerPoint title bar.
Keep no more than six visible content blocks. Do not crowd the page.
Use muted academic blue for the left pillar, muted teal or green for the right pillar, warm gray for supporting text, and a small orange accent only for the bidirectional arrows.
No decorative background. No logo. No fake interface.

Style requirements:
Formal academic technical diagram, white or very light background, flat 2D vector-like style, clean lines, consistent stroke weight, high contrast, readable labels, natural and serious thesis proposal tone.
Chinese labels should be concise and readable. If Chinese text rendering is unreliable, leave clean blank label areas so the final labels can be overlaid in PowerPoint.

Negative prompt:
photorealistic, 3D pillars, marble columns, dark background, neon color, gradient background, decorative blobs, bokeh, clipart, cartoon, hand-drawn sketch, watercolor, glossy UI, fake dashboard, fake app screenshot, logo, watermark, random text, pseudo text, misspelled text, text overlap, tiny unreadable labels, cluttered layout, excessive icons, dramatic shadows, perspective distortion, cropped content, blurry, low resolution
```

文件名：`ppt_assets/ai/F05_candidate_architecture_x_3840x2160.png`

```text
Canvas and size: 16:9 landscape, 3840 x 2160 px, high-resolution PNG.

Create the main technical architecture diagram for a feed-forward 3D reconstruction candidate architecture, suitable for a Chinese master's thesis proposal PowerPoint. The diagram must look formal, natural, restrained, and academic, not like a product dashboard or marketing graphic.

Content to include:
Left input area:
图像序列 / 单图 / 图像对

Center architecture modules arranged as a clear data-flow system:
1. 感知模块：DINOv3-S frozen backbone → 特征 token
2. 记忆模块：三分支稀疏注意力 + 锚点存储 K=256 + Mamba 混合
3. 永久性模块：Slot Attention + permanence link → 动静分离
4. 校验模块：Sampson / depth / 共视 → 冲突评分 → 修复动作
5. 编排模块：七专家池 + 能力描述符 → 路由
6. 总线模块：六条信号校验规则

Cross-module signals to show:
永久性模块 → 记忆模块：suppress_static_write
校验模块 → 编排模块：reroute_model
记忆模块 → 校验模块：latent_drift_proxy

Highlight:
校验模块 marked as 主线 A
编排模块 marked as 主线 D

Right output area:
4D pointmap (D1)
Dynamic mask (D2)
Dashed optional output: 4DGS 资产 (D3，后续候选)

Layout requirements:
Use a left-to-right architecture layout: inputs on the left, six modules in the middle, outputs on the right.
The bus module should span the bottom as a contract layer.
Use thick arrows for main data flow and thinner dashed arrows for cross-module signals.
Keep the whole figure readable at slide size. Avoid dense paragraph text.
Leave safe margins for insertion into a PowerPoint slide with an existing title bar and page number.

Color requirements:
感知模块 in muted blue.
记忆模块 in teal.
永久性模块 in soft green.
校验模块 in muted orange, slightly emphasized.
编排模块 in purple-blue or deep academic blue, slightly emphasized.
总线模块 in warm gray.
Use a white or very light background. No gradients.

Style requirements:
Formal academic architecture figure, clean vector-like 2D diagram, consistent line weight, high contrast, no decorative elements.
Chinese labels should be concise and readable. If Chinese text rendering is unreliable, leave clean blank label areas so the final labels can be overlaid in PowerPoint.

Negative prompt:
photorealistic, 3D render, dark background, neon color, gradient background, circuit-board background, glowing neural network, decorative blobs, bokeh, clipart, cartoon, hand-drawn sketch, watercolor, glossy UI, fake app screenshot, logo, watermark, random text, pseudo text, misspelled text, text overlap, tiny unreadable labels, tangled arrows, cluttered layout, excessive icons, dramatic shadows, perspective distortion, cropped boxes, blurry, low resolution
```

文件名：`ppt_assets/ai/F06_critic_module_flow_3840x2160.png`

```text
Canvas and size: 16:9 landscape, 3840 x 2160 px, high-resolution PNG.

Create a formal academic technical flow diagram for the geometric verification module in a feed-forward 3D reconstruction system. The figure should be clean, natural, and suitable for a Chinese thesis proposal PowerPoint.

Content to include:
Three input signal branches:
Sampson 几何
深度一致性
共视冲突

The three branches converge into:
冲突评分聚合

Then pass through:
阈值门控

Branch into repair actions:
动作 0：不修复
动作 1：局部重跑
动作 2：全窗口重跑
动作 3+：预留路径（dashed）

Add a special dashed arrow from the repair or threshold stage to an external module:
编排模块：reroute_model

Add a small boundary note:
无参数更新；用于评估验证机制的边际贡献

Layout requirements:
Three signal inputs should appear on the left or top.
Conflict aggregation and threshold gate should be visually central.
Repair actions should branch clearly on the right or bottom.
The external composer/routing module should sit outside the main flow, connected by one clean dashed arrow.
Avoid cluttered arrows and avoid paragraph text.
Leave safe margins for a PowerPoint title bar and page number.

Color requirements:
Use muted blue and gray for input signals.
Use muted orange for the verification and threshold path.
Use warm gray for reserved dashed paths.
Use white or very light background.

Style requirements:
Formal academic flow chart, flat 2D vector-like style, clean lines, consistent stroke weight, readable labels.
Chinese labels should be concise and readable. If Chinese text rendering is unreliable, leave clean blank label areas so the final labels can be overlaid in PowerPoint.

Negative prompt:
photorealistic, 3D pipeline, dark background, neon color, gradient background, decorative blobs, bokeh, clipart, cartoon, hand-drawn sketch, watercolor, glossy UI, fake dashboard, fake app screenshot, logo, watermark, random text, pseudo text, misspelled text, text overlap, tiny unreadable labels, cluttered arrows, excessive icons, dramatic shadows, perspective distortion, cropped content, blurry, low resolution
```

文件名：`ppt_assets/ai/F07_routing_decision_flow_3840x2160.png`

```text
Canvas and size: 16:9 landscape, 3840 x 2160 px, high-resolution PNG.

Create a simple formal academic flow diagram for the expert routing decision process in a multi-expert 3R reconstruction system. The figure should be natural, restrained, and readable in a Chinese thesis proposal PowerPoint.

Content to include:
Start node:
输入 regime 与失败模式信号

Next node:
读取七专家能力描述符

Decision node:
能力匹配度跨度 > 0 ?

If yes branch:
成本调整后的匹配度解析
选择候选专家
输出：路由结果

If no branch:
早期失败触发
输出：保守退化 / 待人工复核

Side note connected to the decision node:
平局窗口内由校验模块决断

Layout requirements:
Use a clean left-to-right or top-down decision flow.
Use exactly one main diamond decision node.
Two branches should be clearly separated.
Use minimal text and avoid dense explanations.
Leave enough margins for use under an existing PPT title bar.

Color requirements:
Muted academic blue for normal flow.
Muted orange for the decision node and warning branch.
Warm gray for fallback or side note.
White or very light background.

Style requirements:
Formal academic technical diagram, flat 2D vector-like flowchart, consistent line weight, high contrast, readable labels, no decorative visuals.
Chinese labels should be concise and readable. If Chinese text rendering is unreliable, leave clean blank label areas so the final labels can be overlaid in PowerPoint.

Negative prompt:
photorealistic, 3D render, dark background, neon color, gradient background, decorative blobs, bokeh, clipart, cartoon, hand-drawn sketch, watercolor, glossy UI, fake dashboard, fake app screenshot, logo, watermark, random text, pseudo text, misspelled text, text overlap, tiny unreadable labels, confusing arrows, flowchart clutter, excessive icons, dramatic shadows, perspective distortion, cropped content, blurry, low resolution
```

文件名：`ppt_assets/ai/F08_memory_three_branch_3840x2160.png`

```text
Canvas and size: 16:9 landscape, 3840 x 2160 px, high-resolution PNG.

Create a formal academic technical architecture diagram for a three-branch sparse attention memory module in a long-sequence feed-forward 3D reconstruction system. The diagram should be clean, natural, restrained, and suitable for a Chinese thesis proposal PowerPoint.

Content to include:
Input on the left:
当前窗口特征 token

Three parallel branches in the center:
Branch 1 title: 压缩分支
Branch 1 details: compressed latent；递推状态；状态记忆向量

Branch 2 title: 选择分支
Branch 2 details: 空间锚点检索；AnchorBank K=256；top-k retrieval

Branch 3 title: 滑窗分支
Branch 3 details: 局部 frame-value tokens；direct attention

The three branches merge into:
注意力融合

Add a loop component:
Mamba-Transformer 混合循环

Add memory taxonomy tags:
B1 递推状态
B2 空间指针
B3 混合记忆
B4 缓存治理（partial，dashed gray）

Output on the right:
长序列几何上下文
latent_drift_proxy

Layout requirements:
Use a left-to-right layout: input on left, three parallel branches in center, fusion and output on right.
The three branches should be visually separated and aligned.
Use dashed gray styling for B4 partial coverage.
Avoid equations and avoid paragraph text.
Leave safe margins for a PowerPoint title bar and page number.

Color requirements:
Compression branch in muted blue.
Selection branch in soft green.
Sliding window branch in purple-blue or teal.
Fusion node in deep academic blue.
Partial B4 in dashed warm gray.
White or very light background.

Style requirements:
Formal academic architecture diagram, clean vector-like 2D style, consistent line weight, high contrast, readable labels, natural thesis proposal tone.
Chinese labels should be concise and readable. If Chinese text rendering is unreliable, leave clean blank label areas so the final labels can be overlaid in PowerPoint.

Negative prompt:
photorealistic, glowing neural network art, 3D render, dark background, neon color, gradient mesh, decorative blobs, bokeh, clipart, cartoon, hand-drawn sketch, watercolor, glossy UI, fake dashboard, fake app screenshot, logo, watermark, random text, pseudo text, misspelled text, text overlap, tiny unreadable labels, tangled arrows, cluttered branches, excessive icons, dramatic shadows, perspective distortion, cropped content, blurry, low resolution
```

文件名：`ppt_assets/ai/F09_platform_four_layer_architecture_3840x2160.png`

```text
Canvas and size: 16:9 landscape, 3840 x 2160 px, high-resolution PNG.

Create a clean formal academic layered architecture diagram for a desktop-first 3R model aggregation management platform. This must be an architecture diagram only, not a fake UI screenshot. The style should be natural, restrained, and suitable for a Chinese thesis proposal PowerPoint.

Content to include:
Four horizontal layers from top to bottom:

Layer 1 title: 桌面前端
Layer 1 details: Tauri 2；React；TypeScript
Layer 1 views: 命令中心；任务工作台；样本矩阵；系统控制台；AI 助手；模型路线图

Layer 2 title: 本地后端
Layer 2 details: FastAPI；Python
Layer 2 components: 模型注册；任务队列；合同验证

Layer 3 title: 远端调度
Layer 3 details: SSH / SCP
Layer 3 components: 文件上传；进程管理；日志轮询；结果回传

Layer 4 title: 模型执行器
Layer 4 details: 独立 Python scripts
Model boxes: DUSt3R；MASt3R；MonST3R；Spann3R；Fast3R；CUT3R；Align3R

Add vertical arrows between layers to show data flow.
Add a side label:
统一执行合同贯穿四层

Layout requirements:
Four clean horizontal bands with aligned boundaries.
Each layer should contain only a few concise internal blocks.
Model executor row may contain seven small aligned model boxes.
Do not create a browser window, application screen, dashboard, or UI mockup.
Leave safe margins for insertion into a PowerPoint slide.

Color requirements:
Layer 1 in muted academic blue.
Layer 2 in teal.
Layer 3 in muted orange.
Layer 4 in soft green.
Use warm gray for connectors and side label.
White or very light background.

Style requirements:
Formal academic system architecture diagram, flat 2D vector-like style, consistent line weight, high contrast, readable labels.
Chinese labels should be concise and readable. If Chinese text rendering is unreliable, leave clean blank label areas so the final labels can be overlaid in PowerPoint.

Negative prompt:
fake UI screenshot, fake app screenshot, glossy UI, dashboard mockup, browser window, phone mockup, photorealistic, 3D server rack, dark background, neon color, gradient background, decorative blobs, bokeh, clipart, cartoon, excessive icons, logo, watermark, random text, pseudo text, misspelled text, text overlap, tiny unreadable labels, cluttered layout, dramatic shadows, perspective distortion, cropped content, blurry, low resolution
```

文件名：`ppt_assets/ai/F10_execution_contract_sequence_3840x2160.png`

```text
Canvas and size: 16:9 landscape, 3840 x 2160 px, high-resolution PNG.

Create a clean formal academic sequence-style flow diagram showing the lifecycle of a unified 3R model execution contract. The figure should be natural, restrained, and suitable for a Chinese thesis proposal PowerPoint.

Content to include:
Actors from left to right:
桌面前端
本地后端
任务队列
远端服务器
模型执行器
结果展示

Steps to show:
1. 提交任务：job.json
2. 参数合同验证
3. 进入任务队列
4. SSH/SCP 上传输入
5. 远端 conda 环境执行
6. 实时写入 status.json
7. 本地轮询状态
8. SCP 回传输出目录
9. 解析 scene_meta.json
10. 前端刷新结果视图

Highlight three JSON contract files:
job.json：输入合同
status.json：状态合同
scene_meta.json：输出合同

Layout requirements:
Use a left-to-right sequence diagram or clean flow chart.
Actors should be aligned along the top or center.
Show steps with short arrows, not dense paragraphs.
The three JSON file boxes should be visually highlighted but not oversized.
Leave safe margins for an existing PowerPoint title bar and page number.

Color requirements:
Muted blue for local components.
Muted orange for remote dispatch and execution.
Soft green for returned results.
Warm gray for arrows and auxiliary labels.
White or very light background.

Style requirements:
Formal academic workflow diagram, flat 2D vector-like style, consistent line weight, high contrast, readable labels.
Chinese labels should be concise and readable. If Chinese text rendering is unreliable, leave clean blank label areas so the final labels can be overlaid in PowerPoint.

Negative prompt:
fake UI screenshot, terminal screenshot, code screenshot, photorealistic server, 3D icons, dark background, neon color, gradient background, decorative blobs, bokeh, clipart, cartoon, logo, watermark, random text, pseudo text, misspelled text, text overlap, tiny unreadable labels, overlapping arrows, cluttered layout, dramatic shadows, perspective distortion, cropped content, blurry, low resolution
```

文件名：`ppt_assets/ai/F12_experiment_design_overview_3840x2160.png`

```text
Canvas and size: 16:9 landscape, 3840 x 2160 px, high-resolution PNG.

Create a formal academic hierarchical overview diagram of the experimental design for a 3R thesis proposal. The figure should look natural, restrained, and suitable for a Chinese academic PowerPoint template.

Content to include:
Top title node:
实验设计总览

Five branches:
1. 架构层消融
Details: 10 项；3 tier

2. 记忆消融
Details: 12 项

3. 校验标定
Details: 30 阈值；6 类失败模式

4. 长序列评测
Details: 4 变体；4 度量；windows 10/20/50/100

5. 平台层评测
Details: 合同覆盖率；对比矩阵；报告导出；API 候选

Bottom bar:
GPU 预算约 1377 hours
状态：方案 ready，执行受算力授权门控

Layout requirements:
Use a top-down hierarchy or clean branching structure with five clearly separated groups.
Keep each branch short and readable.
Do not use dense paragraphs.
The bottom bar should be quiet and not dominate the slide.
Leave safe margins for a PowerPoint title bar and page number.

Color requirements:
Use muted blue, teal, orange, purple-blue, and soft green for the five branches.
Use warm gray for the bottom bar.
Use a small orange marker for the execution gate.
White or very light background.

Style requirements:
Formal academic experiment design diagram, flat 2D vector-like style, consistent line weight, high contrast, readable labels, serious thesis proposal tone.
Chinese labels should be concise and readable. If Chinese text rendering is unreliable, leave clean blank label areas so the final labels can be overlaid in PowerPoint.

Negative prompt:
photorealistic, 3D chart, dark background, neon color, gradient background, busy mind map, decorative blobs, bokeh, clipart, cartoon, hand-drawn sketch, watercolor, fake dashboard, logo, watermark, random text, pseudo text, misspelled text, text overlap, tiny unreadable labels, cluttered branches, excessive icons, dramatic shadows, perspective distortion, cropped content, blurry, low resolution
```

文件名：`ppt_assets/ai/F13_question_innovation_mapping_3840x2160.png`

```text
Canvas and size: 16:9 landscape, 3840 x 2160 px, high-resolution PNG.

Create a clean formal academic mapping diagram connecting four research questions to four innovation points. The figure should be natural, restrained, and suitable for a Chinese master's thesis proposal PowerPoint.

Content to include:
Left column title:
研究问题

Left column items:
Q1 验证机制
Q2 长序列内存
Q3 多专家组合
Q4 统一平台

Right column title:
创新点

Right column items:
IP1 校验作为架构组件
IP2 异构多专家组合
IP3 长序列内存统一
IP4 统一聚合管理平台

Arrows:
Q1 → IP1
Q2 → IP3
Q3 → IP2
Q4 → IP4

Add a small bottom note:
创新点表述限定为“候选方案 + 对照实验证据”

Layout requirements:
Two balanced columns with four rows.
Use direct arrows. Q2 and Q3 mappings may cross only if the crossing is visually clean and not confusing.
Avoid paragraph text and avoid dense labels.
Leave safe margins for an existing PowerPoint title bar and page number.

Color requirements:
Muted academic blue for the question column.
Soft teal or green for the innovation column.
Muted orange for arrows.
Warm gray for the bottom note.
White or very light background.

Style requirements:
Formal academic mapping diagram, flat 2D vector-like style, consistent line weight, high contrast, readable labels.
Chinese labels should be concise and readable. If Chinese text rendering is unreliable, leave clean blank label areas so the final labels can be overlaid in PowerPoint.

Negative prompt:
photorealistic, 3D render, dark background, neon color, gradient background, complex network graph, decorative blobs, bokeh, clipart, cartoon, hand-drawn sketch, watercolor, fake dashboard, logo, watermark, random text, pseudo text, misspelled text, text overlap, tiny unreadable labels, tangled arrows, excessive icons, dramatic shadows, perspective distortion, cropped content, blurry, low resolution
```

文件名：`ppt_assets/ai/F16_research_timeline_gantt_3840x2160.png`

```text
Canvas and size: 16:9 landscape, 3840 x 2160 px, high-resolution PNG.

Create a clean formal academic timeline / Gantt-style diagram for a Chinese thesis proposal. The figure should show a candidate research schedule from M1 to M8 and a parallel platform milestone track. It must look natural, restrained, and compatible with a blue academic PowerPoint template.

Content to include:
Horizontal time axis:
M1 M2 M3 M4 M5 M6 M7 M8

Main research track:
M1-M2：开题完稿 + 提交
M3-M5：里程碑 19-26；真实数据路径；多专家加载；校验标定
M6-M8：4DGS 渲染器；真实训练；论文撰写

Platform track:
P-1：Align3R 验证，7/7 覆盖
P-2：跨模型对比视图
P-3：评估报告导出
P-4：候选架构 X 接入
P-5：REST API 候选
P-6：人工评分层
P-7：AI 辅助评估层候选

Add a small note:
候选时间表，受算力授权、实证反馈与导师意见影响

Layout requirements:
Use two horizontal tracks: 主研究线 and 平台线.
Use clean Gantt bars, not a crowded project management screenshot.
Keep labels short and readable.
Use subtle grouping for short-term M1-M2, mid-term M3-M5, long-term M6-M8.
Leave safe margins for a PowerPoint title bar and page number.

Color requirements:
Muted academic blue for the main research track.
Teal or green for the platform track.
Warm gray for the time axis and grid.
Small orange accents for gated or candidate milestones.
White or very light background.

Style requirements:
Formal academic schedule diagram, flat 2D vector-like style, consistent line weight, high contrast, readable labels.
Chinese labels should be concise and readable. If Chinese text rendering is unreliable, leave clean blank label areas so the final labels can be overlaid in PowerPoint.

Negative prompt:
photorealistic, office software screenshot, project management app screenshot, fake UI, dark background, neon color, gradient background, decorative blobs, bokeh, clipart, cartoon, hand-drawn sketch, watercolor, logo, watermark, random text, pseudo text, misspelled text, text overlap, tiny unreadable labels, cluttered bars, excessive gridlines, dramatic shadows, perspective distortion, cropped content, blurry, low resolution
```

