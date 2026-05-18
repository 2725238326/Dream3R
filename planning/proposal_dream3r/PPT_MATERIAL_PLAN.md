# 开题报告 PPT 材料规划

| 字段 | 取值 |
|---|---|
| 创建日期 | 2026-05-17 |
| 受众 | 导师（开题报告答辩） |
| 源文件 | DRAFT_EXTERNAL_V1.md（外部稿 v1, ~24000 字） |
| PPT 工具 | 用户已有 PPT 生成 skill + 模板 |

---

## 一、项目定调（PPT 叙事主线）

### 核心叙事弧（一句话）

> 3R 方向方法爆发但缺乏系统化对比框架 → 我们从两个层面回应：(A) 候选架构在统一框架内并置多机制评估；(B) 聚合管理平台让多模型对比成为标准化流程 → 贡献是对照实验数据 + 可复用平台，不是优越性声明。

### 三条红线（贯穿全 PPT）

1. **候选不等于最终**：X 是被评估的候选方案，不是最终答案
2. **不押注单一支线**：每个子模块可独立验证/退化
3. **提供对照数据，不宣称优越性**：claim 边界是"评估…是否在…维度上呈现优势"

### 两大支柱关系

```
支柱 A（算法创新）         支柱 B（工程平台）
候选架构 X                 聚合管理平台
6 模块 + 7 专家池           7 模型统一接入 + 6 验证通过
    ↑ 消融实验需求               ↑ 调度执行基础设施
    └────── 互相支撑 ──────┘
```

---

## 二、幻灯片结构（20 页）

### Slide 1：封面

- **标题**：面向前馈式三维重建的候选架构设计与统一聚合管理平台
- **副标题**：硕士学位论文开题报告
- **信息**：姓名 / 导师 / 学院 / 日期
- **图表需求**：无（纯文字 + 模板背景）

---

### Slide 2：研究背景 — 3R 方向爆发

- **核心内容**：
  - 3R 定义：单次前向传播直接回归三维点图
  - DUSt3R (2024) 以来的子方向分化：跨视图几何 / 多视角 / 动态 4D / 长序列 / 测试时优化 / 可渲染资产
  - 一句话：方法多样性已不亚于经典几何重建
- **图表需求**：
  - [图 F1] **3R 方向演化谱系图**
  - 来源选项：(a) 综述 TikZ fig:lineage 裁剪渲染；(b) AI 重绘为更简洁的时间线
  - 综述渲染页参考：`Dream/3R-mix/build/apa7ish_rendered_pages/main_p003.png` 或 `main_p004.png`
- **讲述要点**：2024-2026 两年，3R 方向从 DUSt3R 一棵树长成了一片森林

---

### Slide 3：问题提出 — 六类失败模式 + 三组未解问题

- **核心内容**（两列布局）：
  - 左列：六类失败模式（弱纹理 / 镜面 / 快速运动 / 长基线 / 尺度漂移 / 域外）
  - 右列：三组研究问题（Q1 验证机制 / Q2 长序列内存 / Q3 多专家组合）+ Q4 平台
- **图表需求**：
  - [图 F2] **六类失败模式示意图**
  - 来源：论文原图裁剪（各论文 Fig.1 中的失败案例拼贴）或 AI 生成概念图
  - 候选论文图源：MonST3R Fig.1（动态）、DUSt3R 对比图（长基线）、Test3R Fig（一致性失败）
- **讲述要点**：现有方法把这些当 limitations 一笔带过；我们把它们纳入架构设计

---

### Slide 4：研究现状 — 综述四轴总结

- **核心内容**：
  - 综述 44 篇引文的四轴框架：失败模式 / 长序列内存 / 测试时机制 / 输出资产
  - 同期完成的 18 页中文综述（sibling artifact）
  - 覆盖矩阵：21 子类 → 6 first-class / 11 partial / 4 absent
- **图表需求**：
  - [图 F3] **四轴覆盖矩阵热力图**
  - 来源：根据 §2.7 数据自绘（21 子类 × 覆盖状态的彩色矩阵图）
  - 颜色编码：绿色=first-class / 黄色=partial / 红色=absent
- **讲述要点**：综述不仅是文献回顾，更是架构设计的判断框架

---

### Slide 5：工具链空白 — 支柱 B 的动机

- **核心内容**：
  - Nerfstudio → NeRF 范式，不适配 3R
  - 商业产品 → 闭源不可控
  - 各模型 demo → 孤岛运行，跨模型对比全靠手动
  - **空白**：缺乏面向前馈式 3R 的统一聚合对比平台
- **图表需求**：
  - [表 T1] **与现有平台的对比表**（直接复用 §4-B.3 的 7 维度对比表）
- **讲述要点**：7 个模型 × 7 个不同的环境/格式/输出 = 不可控的实验成本

---

### Slide 6：研究目标 — 四个设计目标 + 两大支柱

- **核心内容**：
  - 四个设计目标（§1.4）：失败模式响应 / 内存统一 / 多专家评估 / 验证路径区分
  - 两大支柱明确提出：A=候选架构 / B=聚合管理平台
  - 候选不等于最终的研究纪律
- **图表需求**：
  - [图 F4] **两大支柱关系示意图**（简洁的双柱 + 箭头互联图）
  - 来源：AI 生成或手绘
- **讲述要点**：我们不是做一个"更好的模型"，而是做一套"可对照评估的研究框架"

---

### Slide 7：候选架构 X — 整体设计（核心页）

- **核心内容**：
  - 六模块总览：感知 → 记忆 → 永久性 → 校验 → 编排 → 总线
  - 两条主线：A=验证作为架构组件 / D=异构 best-of-N 编排
  - 帧预算约束：30-50 ms/frame
  - 输入：图像序列/单图/图像对 → 输出：4D pointmap + dynamic mask
- **图表需求**：
  - [图 F5] **候选架构 X 整体架构图**（六模块 + 信号流 + 输入输出）
  - 来源：**AI 生成**（学术风格技术架构图）— 这是 PPT 中最重要的图
  - 详细提示词见 §四
- **讲述要点**：六个模块各司其职，通过总线信号契约协同

---

### Slide 8：校验模块 — 主线 A 详解

- **核心内容**：
  - 三类几何信号：Sampson 几何 / 深度一致性 / 共视冲突
  - 修复动作 0/1/2（不修复 / 局部重跑 / 全窗口重跑）+ 路由切换
  - 与 Test3R 的关系：hybrid = 验证+修复，但不含 TTT 参数更新
  - 六类失败模式 → 5 sub-signal 的逐类标定（plan-ready）
- **图表需求**：
  - [图 F6] **校验模块流程图**
  - 来源：AI 生成（信号→聚合→阈值→修复动作 的流程图）
- **讲述要点**：把验证从"测试后附加"提升为"架构内置组件"

---

### Slide 9：编排模块 — 主线 D 详解

- **核心内容**：
  - 7 专家池表格（MASt3R / Fast3R / Spann3R / CUT3R / MoGe-2 / DepthAnything-V2 / Test3R）
  - 能力描述符 + 路由策略
  - 与校验模块的协作（信号校验规则第 1/4 条）
- **图表需求**：
  - [表 T2] **7 专家池能力矩阵**（直接复用 §4.6 表格，简化为 PPT 版）
  - [图 F7] **路由决策流程**（匹配度跨度>0 → 成本调整解析；=0 → 早期失败）
- **讲述要点**：不是"我们的模型 vs 别人的模型"，而是"让多个专家各展其长"

---

### Slide 10：记忆模块 — 四类机制统一

- **核心内容**：
  - 三分支稀疏注意力：压缩↔递推状态 / 选择↔空间指针 / 滑窗↔混合记忆
  - 空间锚点存储 K=256 + 状态记忆向量 + Mamba-Transformer 混合循环
  - 缓存治理部分覆盖（诚实承认缺口）
- **图表需求**：
  - [图 F8] **记忆模块三分支架构图**
  - 来源：AI 生成（三个并行分支 + 融合 + 锚点存储的示意图）
- **讲述要点**：现有系统每个只占一档，我们在单一模块内同时实装三档

---

### Slide 11：聚合管理平台架构 — 支柱 B（核心页）

- **核心内容**：
  - 四层分离架构：桌面前端(Tauri+React) / 本地后端(FastAPI) / 远端调度(SSH/SCP) / 模型执行器
  - 六个核心视图：命令中心 / 任务工作台 / 样本矩阵 / 系统控制台 / AI 助手 / 模型路线图
  - 代码规模：~15000 行手写代码
- **图表需求**：
  - [图 F9] **平台四层架构图**（从前端到远端的分层 + 数据流）
  - 来源：AI 生成或手绘
- **讲述要点**：合同驱动的关注点分离 — 新模型接入只需一个执行器脚本

---

### Slide 12：统一执行合同 — 核心学术抽象

- **核心内容**：
  - 三文件合同：job.json / status.json / scene_meta.json
  - 执行流时序：提交 → 验证 → 上传 → 远端执行 → 回传 → 解析 → 展示
  - 学术意义：解决 §2.8 的 demo 孤岛问题
- **图表需求**：
  - [图 F10] **执行流时序图**（从桌面端到远端再回来的完整链路）
  - 来源：AI 生成或 Mermaid sequence diagram
- **讲述要点**：统一执行合同是 demo 孤岛问题的形式化解法

---

### Slide 13：跨模型实测数据 — 已有工程证据

- **核心内容**：
  - 6 模型跨模型对比矩阵（实测数据表）
  - 三个模式发现：流式最快(24-26s) / 静态中等(91-95s) / 动态最慢(223s)
  - 产物类型差异 → 印证统一合同必要性
- **图表需求**：
  - [表 T3] **跨模型对比矩阵**（直接复用 §7.7 表格）
  - [图 F11] **推理耗时柱状图**（6 模型的耗时可视化）
  - 来源：根据 cross_model_report.json 数据绘制
- **讲述要点**：这不是 benchmark 结果，是集成验证的工程证据

---

### Slide 14：实验设计 — 三层证据 + 消融组

- **核心内容**：
  - 三层证据阶梯：L1 论文层 / L2 代理用例层 / L3 原型实现层
  - 架构层消融 10 项（3 tier）+ 记忆消融 12 项 + 校验标定 30 项阈值
  - 长序列评测：4 变体 × 4 度量 × windows {10,20,50,100}
  - GPU 预算 ~1377 hours
  - 平台层评测标准（§5.8）
- **图表需求**：
  - [图 F12] **实验设计总览图**（三组消融 + 标定 + 长序列 + 平台评测 的层级关系图）
  - 来源：AI 生成或手绘层级图
- **讲述要点**：所有实验都是 plan-ready，执行需要算力授权

---

### Slide 15：四个创新点

- **核心内容**：
  - IP1: 校验作为架构组件（对应 Q1 + 主线 A）
  - IP2: 异构多专家组合（对应 Q3 + 主线 D）
  - IP3: 长序列内存四类统一（对应 Q2 + 记忆模块）
  - IP4: 统一聚合管理平台（对应 Q4 + 支柱 B）
  - 句式约束：全部用"提供...候选...+ 对照实验证据"
- **图表需求**：
  - [图 F13] **Q ↔ IP 映射图**（四个研究问题到四个创新点的对应关系）
  - 来源：简单的四对箭头图，手绘或 AI 生成
- **讲述要点**：四个创新点不是"我们更好"，而是"我们提供对照证据"

---

### Slide 16：已完成工作 — 支柱 A 进展

- **核心内容**：
  - 架构设计文档 7 份 + 跨模块信号契约 v2.1
  - 实现里程碑 1-18 完成
  - KITTI 真实数据集成验证：L2=20.47 / RMSE=21.87（集成证据，非训练后质量）
  - 第 0 项记忆消融 22/22 fixture pass
  - 同期中文综述 18 页 44 引文
- **图表需求**：
  - [图 F14] **KITTI 集成验证输出可视化**
  - 来源选项：(a) KITTI 场景图片 + 重建点云截图；(b) 文字+数字表格即可
- **讲述要点**：L2=20.47 是"跑通了"的证据，不是"训练好了"的证据

---

### Slide 17：已完成工作 — 支柱 B 进展

- **核心内容**：
  - 平台代码 ~15000 行
  - 7 模型接入 / 6 端到端验证通过 / Align3R 待权重
  - 远端 SSH 调度完整实装（孤立任务恢复、安全取消）
  - 三层评估框架（自动指标已实装，人工+AI 为候选）
- **图表需求**：
  - [图 F15] **平台 UI 截图**（如有截图；或用模型接入状态表替代）
  - [表 T4] **模型接入状态表**（直接复用 §7.7 的 7 行表格）
  - 来源：平台实际运行截图（需用户提供或截图）
- **讲述要点**：不是 demo，是完整的工程产品 — 15000 行代码在线运行

---

### Slide 18：研究计划 — 时间线

- **核心内容**：
  - 短期 M1-M2：开题完稿 + 提交
  - 中期 M3-M5：里程碑 19-26 + 后续设计候选 B1/B2/B3
  - 长期 M6-M8：4DGS 渲染器 + 真实训练 + 论文
  - 平台里程碑 P-1 到 P-7 并行
  - 候选时间表，非承诺性进度
- **图表需求**：
  - [图 F16] **甘特图 / 时间线图**
  - 来源：根据 §8 数据绘制（M1-M8 + P-1 到 P-7 的双轨时间线）
  - 工具建议：Mermaid Gantt 或表格形式
- **讲述要点**：每个里程碑独立决策，受算力和实证反馈双重约束

---

### Slide 19：风险分析

- **核心内容**：
  - 五层风险：架构层 / 跨模块 / 实证执行 / 工程时序 / 平台层
  - 核心风险精选 3-4 条：校验标定缺口 / 消融全部待执行 / 域外检测 absent / 环境漂移
  - 整体判断：无一风险被完全消除，但均有方案级缓解
  - 与候选研究定位一致：风险是研究对象的一部分
- **图表需求**：
  - [表 T5] **风险优先级表**（直接复用 §9.6 的精简版 P0/P1/P2 表格）
- **讲述要点**：所有风险显式声明，不隐瞒缺口

---

### Slide 20：总结与致谢

- **核心内容**：
  - 一句话总结：两大支柱（候选架构 + 聚合平台）为 3R 方向提供可对照评估的研究框架
  - 已完成：架构设计 + 里程碑 1-18 + KITTI 集成验证 + 平台 15000 行代码 + 7 模型接入 + 综述 18 页
  - 待推进：消融执行 + 真实训练 + 论文
  - 致谢导师
- **图表需求**：无（纯文字总结）

---

## 三、图表需求汇总 + 来源分类

### A. 可直接复用的已有资源

| 编号 | 内容 | 来源路径 |
|---|---|---|
| F1 备选 | 3R 谱系图 | `Dream/3R-mix/build/apa7ish_rendered_pages/main_p003.png` 或 `main_p004.png`（综述 TikZ 渲染） |
| T1 | 与现有平台对比表 | DRAFT_EXTERNAL_V1.md §4-B.3 L418-426 |
| T2 | 7 专家池表格 | DRAFT_EXTERNAL_V1.md §4.6 L341-350 |
| T3 | 跨模型对比矩阵 | DRAFT_EXTERNAL_V1.md §7.7 L752-759 |
| T4 | 模型接入状态表 | DRAFT_EXTERNAL_V1.md §7.7 L738-746 |
| T5 | 风险优先级表 | DRAFT_EXTERNAL_V1.md §9.6 L886-893 |

### B. 需要从论文裁剪的图片

| 编号 | 内容 | 论文来源建议 |
|---|---|---|
| F2 素材 | 六类失败模式示意 | DUSt3R Fig.1 / MonST3R Fig.1 / Test3R Fig / 综述 §10 失败模式图 |
| F14 素材 | KITTI 场景参考 | KITTI 数据集官方示例图 / 综述中 KITTI 相关图 |

### C. 需要用户提供的截图

| 编号 | 内容 | 说明 |
|---|---|---|
| F15 | 平台 UI 截图 | 用户运行平台后截取：命令中心 / 任务工作台 / 样本矩阵 中选 1-2 张代表性截图 |

### D. 需要绘制/AI 生成的图（详细提示词见 §四）

| 编号 | 内容 | 复杂度 |
|---|---|---|
| F4 | 两大支柱关系图 | 简单 |
| F5 | 候选架构 X 整体架构图 | **高**（最重要） |
| F6 | 校验模块流程图 | 中等 |
| F7 | 路由决策流程 | 简单 |
| F8 | 记忆模块三分支架构图 | 中等 |
| F9 | 平台四层架构图 | 中等 |
| F10 | 执行流时序图 | 中等 |
| F11 | 推理耗时柱状图 | 简单（数据可视化） |
| F12 | 实验设计总览图 | 中等 |
| F13 | Q↔IP 映射图 | 简单 |
| F16 | 甘特图/时间线 | 中等 |

### E. 需要绘制的数据可视化

| 编号 | 内容 | 数据源 |
|---|---|---|
| F3 | 四轴覆盖矩阵热力图 | §2.7: 21 子类, 6/11/4 分布 |
| F11 | 推理耗时柱状图 | cross_model_report.json: Spann3R 24.8s / CUT3R 26.2s / Fast3R 28.5s / DUSt3R 91.2s / MASt3R 95.0s / MonST3R 223.3s |

---

## 四、AI 生图提示词

### 通用风格约束（所有架构图共享）

**正面风格**:
- Academic technical diagram, clean vector style
- White or very light background, high contrast
- Rounded rectangles for modules, directional arrows for data flow
- Color palette: muted blues (#4A90D9), teals (#50B5AA), warm grays (#8C8C8C), accent orange (#E8934A) for key highlights
- Consistent line weight, professional typography
- Chinese labels with English annotations in parentheses
- Flat design, no 3D effects, no gradients, no shadows
- Clear visual hierarchy with size and color coding
- 16:9 aspect ratio for slides

**负面提示词**:
- No photorealistic rendering, no 3D perspective
- No decorative elements, no icons, no clipart
- No dark backgrounds, no neon colors, no gradients
- No hand-drawn sketch style, no watercolor
- No text overlap, no cluttered layout
- No brand logos, no watermarks
- No blurry or low-resolution output

---

### F5: 候选架构 X 整体架构图（最重要）

**描述**:
Technical architecture diagram showing a feed-forward 3D reconstruction system with 6 modules arranged in a data flow layout.

**结构说明**:
```
输入层（左）:
  - 图像序列 / 单图 / 图像对

六模块（中，从上到下或从左到右）:
  [感知模块] DINOv3-S frozen backbone → 特征 token
      ↓
  [记忆模块] 三分支稀疏注意力 + 锚点存储 K=256 + Mamba 混合
      ↓         ↕ suppress_static_write
  [永久性模块] Slot Attention + permanence link → 动静分离
      ↓
  [校验模块] Sampson / depth / 共视 → 冲突评分 → 修复动作
      ↕ reroute_model                    主线 A 标注
  [编排模块] 7 专家池 + 能力描述符 → 路由    主线 D 标注
      ↓
  [总线模块] 6 条信号校验规则（跨模块信号契约）

输出层（右）:
  - 4D pointmap (D1)
  - Dynamic mask (D2)
  - [虚线] 4DGS 资产 (D3, 后续候选)
```

**提示词**:
```
Academic technical architecture diagram, feed-forward 3D reconstruction system.
Six interconnected modules in a clean flow layout: Perceiver (blue),
Memory (teal), Permanence (green), Critic (orange, highlighted as "Main Line A"),
Composer (purple, highlighted as "Main Line D"), Bus (gray, spanning bottom).
Input on left (image sequence), output on right (4D pointmap + dynamic mask).
Directional arrows showing data flow and cross-module signals.
Chinese labels: 感知模块, 记忆模块, 永久性模块, 校验模块, 编排模块, 总线模块.
Clean white background, flat vector style, 16:9 aspect ratio,
professional academic diagram suitable for thesis defense presentation.
```

**负面**: `photorealistic, 3D render, dark background, decorative, cluttered, hand-drawn, watercolor, neon, gradient, shadows, clipart`

---

### F6: 校验模块流程图

**提示词**:
```
Technical flow diagram for a geometric verification module.
Three input signal branches (Sampson geometry, depth consistency, co-visibility conflict)
converge into a conflict score aggregation node, then pass through a threshold gate.
Below the gate, four repair action paths branch out: Action 0 (no repair),
Action 1 (local re-run), Action 2 (full window re-run), Action 3+ (reserved, dashed).
A special "reroute" arrow connects to an external "Composer" module box.
Chinese labels. Clean academic style, white background, flat vector, 16:9.
```

**负面**: 同通用

---

### F8: 记忆模块三分支架构图

**提示词**:
```
Technical architecture diagram of a three-branch sparse attention memory module.
Three parallel branches: Compression branch (compressed latent, recursive state),
Selection branch (spatial anchor retrieval, top-k from AnchorBank K=256),
Sliding window branch (local frame-value tokens, direct attention).
All three branches merge via attention fusion.
Additional components: State Memory Vector (recurrence), Mamba-Transformer hybrid loop.
Color-coded mapping to memory taxonomy: B1 recursive (blue),
B2 spatial pointer (green), B3 hybrid (purple), B4 budget governance (gray, dashed, partial).
Chinese labels. Clean academic style, white background, flat vector, 16:9.
```

**负面**: 同通用

---

### F9: 平台四层架构图

**提示词**:
```
Technical layered architecture diagram for a desktop-first 3D reconstruction
management platform, four horizontal layers stacked vertically:
Layer 1 (top, blue): Desktop Frontend - Tauri 2 + React + TypeScript,
  six view icons (command center, job workbench, sample matrix,
  system console, AI advisor, model roadmap).
Layer 2 (teal): Local Backend - FastAPI + Python,
  sub-components: model registry, task queue, contract validation.
Layer 3 (orange): Remote Dispatch - SSH/SCP,
  sub-components: file upload, process management, log streaming, result retrieval.
Layer 4 (bottom, green): Model Executors - 7 independent Python scripts,
  7 small boxes labeled: DUSt3R, MASt3R, MonST3R, Spann3R, Fast3R, CUT3R, Align3R.
Vertical arrows between layers showing data flow.
Chinese labels. Clean academic style, white background, flat vector, 16:9.
```

**负面**: 同通用

---

### F10: 统一执行合同流程图

**提示词**:
```
Sequence diagram or flow chart showing the execution lifecycle of a unified
3R model execution contract. Steps from left to right:
1. Desktop Frontend submits task (job.json)
2. Local Backend validates parameter contract
3. Task enters queue
4. SSH pushes input files to remote server
5. Remote model executor starts in conda environment
6. Executor writes status.json in real-time
7. Local backend polls status
8. Inference completes, SCP retrieves output directory
9. Local backend parses scene_meta.json
10. Frontend refreshes result view
Three JSON file icons highlighted: job.json (input), status.json (state), scene_meta.json (output).
Chinese labels. Clean academic style, white background, flat vector, 16:9.
```

**负面**: 同通用

---

### F4: 两大支柱关系图

**提示词**:
```
Simple conceptual diagram showing two research pillars side by side.
Left pillar (blue): "支柱 A: 候选架构 X" with sub-items:
  6 modules, 7 expert pool, algorithm innovation.
Right pillar (green): "支柱 B: 聚合管理平台" with sub-items:
  7 models, unified contract, engineering infrastructure.
Bidirectional arrows between pillars labeled:
  "A→B: 消融实验需求" and "B→A: 调度执行基础设施".
Clean, minimal, academic style, white background, 16:9.
```

**负面**: 同通用

---

### F12: 实验设计总览图

**提示词**:
```
Hierarchical overview diagram of experimental design for a 3D reconstruction thesis.
Top level: "实验设计总览" branching into 5 groups:
1. Architecture ablation (10 items, 3 tiers) - blue
2. Memory ablation (12 items) - teal
3. Critic calibration (30 thresholds × 6 failure modes) - orange
4. Long-sequence evaluation (4 variants × 4 metrics × 4 window sizes) - purple
5. Platform evaluation (4 metrics) - green
Bottom bar: "GPU budget ~1377 hours | All plan-ready, execution gated"
Chinese labels. Tree/hierarchy layout, clean academic style, white background, 16:9.
```

**负面**: 同通用

---

### F13: Q↔IP 映射图

**提示词**:
```
Simple mapping diagram with 4 items on each side connected by arrows.
Left side "研究问题": Q1 验证机制, Q2 长序列内存, Q3 多专家组合, Q4 统一平台.
Right side "创新点": IP1 校验作为架构组件, IP2 异构多专家组合,
IP3 长序列内存统一, IP4 统一聚合管理平台.
Arrows: Q1→IP1, Q2→IP3, Q3→IP2, Q4→IP4.
Note that Q2↔IP3 and Q3↔IP2 cross over (not 1:1 sequential).
Clean minimal style, white background, 16:9.
```

**负面**: 同通用

---

## 五、数据可视化规格

### F3: 四轴覆盖矩阵

数据源（§2.7）:

| 轴 | 子类 | 覆盖状态 |
|---|---|---|
| A 失败模式 | 弱纹理 | first-class |
| A 失败模式 | 长基线 | first-class |
| A 失败模式 | 镜面 | partial |
| A 失败模式 | 快速运动 | partial |
| A 失败模式 | 尺度漂移 | partial |
| A 失败模式 | 域外(OOD) | absent |
| B 长序列内存 | B1 递推状态 | first-class |
| B 长序列内存 | B2 空间指针 | first-class |
| B 长序列内存 | B3 混合记忆 | first-class |
| B 长序列内存 | B4 缓存治理 | partial |
| C 测试时 | C1 一致性优化 | partial |
| C 测试时 | C2 TTT 参数更新 | absent |
| C 测试时 | C3 先验注入 | partial |
| D 输出资产 | D1 4D pointmap | first-class |
| D 输出资产 | D2 dynamic mask | partial |
| D 输出资产 | D3 4DGS 渲染 | absent |
| 扩展 | 输入扩展轴 | absent |

颜色: first-class=#4CAF50 / partial=#FFC107 / absent=#F44336

### F11: 推理耗时柱状图

| 模型 | 耗时(秒) | 范式 |
|---|---|---|
| Spann3R | 24.8 | 流式序列 |
| CUT3R | 26.2 | 流式序列 |
| Fast3R | 28.5 | 多视图批处理 |
| DUSt3R | 91.2 | 静态重建 |
| MASt3R | 95.0 | 静态重建 |
| MonST3R | 223.3 | 视频/动态 |

按范式分色: 流式=#50B5AA / 批处理=#4A90D9 / 静态=#8C8C8C / 动态=#E8934A

### F16: 甘特图数据

```
M1-M2 (短期):
  - 开题完稿 + 提交
  - P-1: Align3R 验证 → 7/7 覆盖

M3-M5 (中期):
  - 里程碑 19: DTU+KITTI loader
  - 里程碑 20-23: 多专家加载+可视化+消融
  - 里程碑 24: 校验标定执行
  - P-2: 跨模型对比视图
  - P-3: 评估报告导出
  - P-4: 候选架构X接入 (第8模型)

M6-M8 (长期):
  - 里程碑 25-26: TTT + 输入扩展
  - 里程碑 27: 4DGS 渲染器
  - 真实数据训练
  - 论文撰写
  - P-5~P-7: API + 人工评分 + AI 辅助
```

---

## 六、附属资料清单

PPT 制作时需要准备的完整资料包:

| 序号 | 资料 | 路径 | 用途 |
|---|---|---|---|
| 1 | 开题报告全文 | `DRAFT_EXTERNAL_V1.md` | 文字素材主源 |
| 2 | 综述 PDF | `deliverables/3r_survey_stage_final_2026-05-15_natural.pdf` | 引用 + 谱系图裁剪 |
| 3 | 综述渲染页 | `Dream/3R-mix/build/apa7ish_rendered_pages/` | 图表裁剪 |
| 4 | 跨模型对比数据 | `Coding/4.06/vision_ui/scripts/cross_model_report.json` | 数据可视化 |
| 5 | 平台代码 | `Coding/4.06/vision_ui/` | 截图 + 代码规模统计 |
| 6 | 模型输出样例 | `Coding/4.06/vision_ui/local_jobs/` | 动态掩码 / 匹配图 等产物截图 |
| 7 | 风格契约 | `STYLE_CONTRACT.md` | vocab 参考 |
| 8 | references.bib | `references.bib` | 引文数据 |

---

## 七、讲述时长分配建议（按 15 分钟估算）

| 部分 | Slides | 时长 | 备注 |
|---|---|---|---|
| 开场+背景 | 1-3 | 2 分钟 | 快速建立问题意识 |
| 研究现状 | 4-5 | 2 分钟 | 综述定调 + 工具链空白 |
| 研究方案 | 6-12 | 5 分钟 | **核心**：架构 + 平台，详细讲 |
| 实测数据+实验设计 | 13-14 | 2 分钟 | 已有证据 + 计划 |
| 创新点+进展 | 15-17 | 2.5 分钟 | 成果展示 |
| 计划+风险+总结 | 18-20 | 1.5 分钟 | 收尾 |

若 20 分钟答辩，则研究方案部分可扩展到 7 分钟，实验设计扩展到 3 分钟。

---

## 八、注意事项

1. **全程避免内部术语**: 不出现 Dream3R / KYKT / cycle / SPEC / DEC / agent 等词
2. **系统命名**: 一律使用"候选架构 X"或"本研究架构"
3. **平台命名**: 使用"聚合管理平台"或"本研究平台"
4. **claim 边界**: 每张涉及创新的 slide 都用"候选/评估/对照实验"句式
5. **数字一致**: 7 模型接入 / 6 验证通过 / 44 引文 / 18 页综述 / ~15000 行代码 / ~24000 字开题
6. **证据标签**: KITTI 数据必须标"集成证据，非训练后质量"
