# v12 PPT 内容补充请求提示词

## 01_架构主线审阅与补全

请作为“开题报告内容审阅 agent”，只基于本地资料，不要联网，不要扩写成论文正文。请阅读以下文件：

- `E:\kykt\Dream\WORKFLOW_STATUS.md`
- `E:\kykt\Dream\RESEARCH_STATE.md`
- `E:\kykt\Dream\code\dream3r\RESEARCH_BASE_AND_INNOVATIONS.md`
- `E:\kykt\Dream\planning\MEMORY_V03_DESIGN_STUDY.md`
- `E:\kykt\Dream\planning\MEMORY_V03_P0_PROTOTYPE_PLAN.md`
- `E:\kykt\Dream\specs\SPEC-20260508-001-dream3r-c2-memory-v03-addendum.md`
- `E:\kykt\Dream\paradigm\CROSS_SPEC_SIGNAL_CONTRACT.md`

输出一个 markdown，保存为：

`E:\kykt\Dream\planning\proposal_dream3r\deliverables\ppt_work\agent_feedback_architecture_v12.md`

输出内容严格按以下结构：

1. `架构主线一句话`
   - 用 1 句话说明 Dream3R 候选架构到底解决什么问题。
   - 要像开题报告，不要营销腔。

2. `必须讲清楚的 5 个模块`
   - Perceiver
   - SpatialMemory / C2 Memory v0.3
   - Permanence
   - Critic
   - Composer / Router
   每个模块输出 3 行：`功能定位`、`输入输出`、`后续验证方式`。

3. `当前 PPT 是否漏讲`
   - 对 v12 现有页结构逐项判断：是否缺“研究问题”、是否缺“架构思路”、是否缺“实现边界”、是否缺“验证路径”。
   - 每条只写 1-2 句，不要长篇。

4. `可直接放进 PPT 的短句`
   - 给 12 条短句，每条不超过 24 个中文字符。
   - 必须是正式展示文本，不要出现“可以看到”“这里说明”“讲解时”等口语提示。

5. `不能写成已完成结果的表述`
   - 列出 6 条需要避免的夸大说法。
   - 每条给一个安全改写。

约束：

- 所有 claim 必须能从上述文件中找到依据。
- 明确区分“已实现/已验证/待验证/计划”。
- 不要引入新概念、新名字或新模型。
- 不要生成 PPT 文件。

## 02_软件平台主体内容补全

请作为“软件平台内容审阅 agent”，只基于本地资料和当前项目状态，不要编造真实 UI。请阅读：

- `E:\kykt\Dream\WORKFLOW_STATUS.md`
- `E:\kykt\Dream\RESEARCH_STATE.md`
- `E:\kykt\Dream\paradigm\RESEARCH_WORKFLOW.md`
- `E:\kykt\Dream\handoff\FRONTEND_DESIGN_HANDOFF_PROMPT.md`
- `E:\kykt\Dream\planning\proposal_dream3r\PPT_MATERIAL_PLAN.md`
- `E:\kykt\Dream\planning\proposal_dream3r\DRAFT_EXTERNAL_V1.md`

如果能在 `E:\kykt\Dream` 下找到平台相关代码、执行器、注册表、模型管理、远端执行或日志记录文件，请列出具体路径；如果找不到，也要明确说“未找到直接代码证据”。

输出一个 markdown，保存为：

`E:\kykt\Dream\planning\proposal_dream3r\deliverables\ppt_work\agent_feedback_platform_v12.md`

输出内容严格按以下结构：

1. `平台定位`
   - 用 2 句话说明平台为什么是第二主体，不是附属 UI。

2. `平台闭环`
   - 按 `任务提交 -> 合同生成 -> 远端执行 -> 状态回传 -> 结果归档 -> 对比评测` 写出每步一句话。

3. `软件架构`
   - 输出四层：桌面交互层、本地服务层、远端调度层、模型执行层。
   - 每层给：职责、可能涉及的技术/文件、后续验证方式。

4. `平台与候选架构的配合关系`
   - 给 5 条明确关系，比如平台如何记录 Memory/Critic/Composer 的输出字段，如何支持消融。

5. `PPT 可用短句`
   - 给 10 条短句，每条不超过 24 个中文字符。

6. `待用户补充`
   - 列出必须由用户补充的资料，例如真实 UI 截图、界面优化状态、模型运行记录、平台演示视频等。

约束：

- 不要把平台写成已经完整上线。
- 不要编造界面截图和功能完成度。
- 不要出现“AI 助手”“agent 自动化”等非正式展示词，除非原文件明确支持。

## 03_3R 相关工作页内容校准

请作为“相关工作校准 agent”，阅读：

- `E:\kykt\Dream\3R-mix\README.md`
- `E:\kykt\Dream\3R-mix\notes\chapter_structure.md`
- `E:\kykt\Dream\3R-mix\notes\model_inventory.md`
- `E:\kykt\Dream\planning\SOTA_MATRIX_V2.md`
- `E:\kykt\Dream\planning\proposal_dream3r\DRAFT_EXTERNAL_V1.md`

输出一个 markdown，保存为：

`E:\kykt\Dream\planning\proposal_dream3r\deliverables\ppt_work\agent_feedback_related_work_v12.md`

输出内容：

1. `模型分组`
   - 将 DUSt3R、MASt3R、Fast3R、VGGT、MonST3R、CUT3R、Spann3R、Test3R 分成 3-4 类。
   - 每类给一句“特点”和一句“对本课题的启示”。

2. `开题报告讲法`
   - 给一段 120-160 字的正式口径，说明“现有模型特点 -> 缺口 -> 本课题为何采取融合、记忆、稀疏注意力和校验机制”。

3. `PPT 可用短句`
   - 给 12 条，每条不超过 22 个中文字符。

4. `风险表达`
   - 给 5 条避免夸大现有模型或本课题创新性的安全表述。

约束：

- 不要写成文献综述长段落。
- 不要把模型特点写错或混淆。
- 不要声称本课题已经超过这些模型。

## 04_可视化素材建议

请作为“开题 PPT 可视化建议 agent”，基于当前 v12 PPT 的结构，判断哪些页适合补图，哪些页不适合补图。输入材料为：

- `E:\kykt\Dream\planning\proposal_dream3r\deliverables\ppt_work\contact_sheet_reference_mode_v12.png`
- `E:\kykt\Dream\planning\proposal_dream3r\deliverables\ppt_work\proposal_dream3r_opening_report_reference_mode_v12.pptx`
- `E:\kykt\Dream\planning\proposal_dream3r\PPT_AI_IMAGE_PROMPTS_COPY_READY.md`

输出一个 markdown，保存为：

`E:\kykt\Dream\planning\proposal_dream3r\deliverables\ppt_work\agent_feedback_visuals_v12.md`

输出内容：

1. `建议保留纯 PPT 结构的页`
   - 给页码和原因。

2. `建议补真实截图或论文图的页`
   - 给页码、所需图、来源要求。

3. `建议用 draw.io/Visio 重画的页`
   - 给页码、图名、节点、连线、禁止事项。

4. `不建议用 AI 生成图的页`
   - 给原因，尤其指出哪些图会显得不学术。

5. `若必须 AI 生成图`
   - 给 3 个最适合生成的图名、尺寸、文件名和一句用途说明。

约束：

- 不要改 PPT。
- 不要生成图片。
- 不要建议纯装饰图。
- 优先建议可编辑流程图、架构图和真实截图。
