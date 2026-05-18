# Agent Handoff Prompt: 开题报告扩展 — 双支柱项目

> **本文件是给其他 agent 的任务提示词。**
> 由 Cascade (cycle 042 agent) 于 2026-05-17 编写。
> 用户已于 2026-05-17 确认四项关键设计决策（见下文）。
> 阅读本文件后按指令执行。

---

## 任务概述

你的任务是将 Dream3R 开题报告从 **单支柱 (新架构模型)** 扩展为 **双支柱 (新架构模型 + KYKT 聚合管理平台)**。

现有开题报告 (§1-§9, 外稿 ~15000 字) 仅覆盖 Dream3R 新架构。用户要求加入 KYKT 平台作为项目的第二大部分。

### 用户确认的四项关键设计决策

1. **Q4 定位**：KYKT 平台作为项目**主体问题之一** (Q4)，与 Q1-Q3 并列，不是仅仅工程贡献。
2. **§4 结构**：支柱 B 为**独立节 §4-B**，与 §4-A (六模块架构) 并列，不作为其子节。
3. **时间线粒度**：平台里程碑采用 **P-1 / P-2 / ...** 编号体系（区别于架构的 W1-W30），粒度为“阶段性交付物”。
4. **API 设计深度**：待后续讨论。当前扩展**仅写概念层**（动机 + 接口方向 + 下游场景举例），不展开具体 endpoint 设计。

## 项目两大支柱

### 支柱 A — Dream3R 新架构模型 (已有)

前馈式三维重建候选多模块架构，六模块设计：感知 / 记忆 / 永久性 / 校验 / 编排 / 总线。三个研究问题：几何校验 (Q1)、长序列内存 (Q2)、多专家组合 (Q3)。

### 支柱 B — KYKT 聚合管理平台 (需新增)

本地桌面端 3R / 视觉几何模型实验工作台。核心能力：

- **技术栈**：Tauri 2 桌面壳 + React + TypeScript 前端 + FastAPI 本地后端 + SSH/SCP 远端调度
- **模型管理**：统一模型注册层 (model_registry)，当前已接入 6 个 3R 模型 (DUSt3R / MASt3R / MonST3R / Spann3R / Fast3R / CUT3R)，其中 4 个已通过平台 smoke test
- **统一输出合同**：所有模型复用同一套 job.json / status.json / scene_meta.json / result_summary 结构
- **评估框架**：样例矩阵 (Sample Matrix) + AI 评估层 (OpenAI-compatible advisor) + 人工评分
- **已有桌面产品**：命令中心 / 工作台 / 任务分屏面板 / 样例矩阵 / 系统部署控制台 / AI 工作台
- **后续规划**：
  - API 导出层：将模型推理封装为可调用的 REST/gRPC 接口
  - 应用对接层：对接三维重建下游应用 (点云编辑 / AR / 数字孪生)
  - 便携打包：嵌入式 Python + React dist + exe 一键发布
  - 新模型扩展：Pi3X / ZipMap / LingBot-Map 等前沿模型

### 双支柱关系

```text
前馈式三维重建 = 算法创新 (Dream3R) + 工程平台 (KYKT)
  - Dream3R 的消融/评测需要 KYKT 平台调度执行
  - KYKT 平台的核心价值 = 为 Dream3R 等新架构提供标准化实验环境
  - 平台 API 导出 = 将研究成果转化为可对接应用的工程产出
```

## 必读文件

### 开题报告体系 (最重要)

| 文件 | 用途 |
|---|---|
| `Dream/planning/proposal_dream3r/PROPOSAL_EXPANSION_PLAN.md` | **本次扩展的总体规划 (先读这个)** |
| `Dream/planning/proposal_dream3r/OUTLINE_V1.md` | 9 章结构 + 章节映射表 |
| `Dream/planning/proposal_dream3r/STYLE_CONTRACT.md` | **双稿语言风格契约 (vocab 替换表 + sync rule + G3/G4 grep 规则)** |
| `Dream/planning/proposal_dream3r/DRAFT_INTERNAL_V1.md` | 内部稿 (Dream vocabulary, master copy) |
| `Dream/planning/proposal_dream3r/DRAFT_EXTERNAL_V1.md` | 外部稿 (学术中文, vocab-clean) |

### KYKT 平台素材 (写作参考)

| 文件 | 用途 |
|---|---|
| `README.md` (项目根) | 三条线总览 |
| `KYKT.md` | 工程主线详细状态 |
| `Coding/4.06/vision_ui/README.md` | 平台架构与功能 |
| `Coding/4.06/vision_ui/THREER_MODEL_ROADMAP.md` | 3R 模型接入路线 (8 层分类) |
| `Coding/4.06/vision_ui/ACTIVE_MODEL_INTEGRATION_PLAN.md` | 活跃模型集成计划 |
| `Coding/4.06/vision_ui/MODEL_DEPLOYMENT_STATUS.md` | 部署状态 |
| `Coding/4.06/vision_ui/DESIGN.md` | UI 设计体系 |
| `PROJECT_PROGRESS_2026-05-03.md` | 最新进度快照 |

## 执行步骤

### Step 1: 更新 STYLE_CONTRACT §2 vocab 替换表

在 §2 表底追加 KYKT 平台相关替换行 (~10-15 行)：

| 内部稿用语 | 外部稿替换 |
|---|---|
| KYKT | 本研究管理平台 / 聚合管理平台 |
| vision_ui | 平台前端 / 桌面客户端 |
| runner / ssh_runner | 模型执行器 / 远端推理调度器 |
| model_registry | 模型注册层 |
| smoke test | 集成验证 / 端到端验证 |
| job.json / status.json | 任务描述文件 / 状态文件 |
| scene_meta.json | 输出元数据合同 |
| local_jobs/ | 本地任务缓存 |
| Tauri | 保留 (通用桌面框架名) |
| FastAPI / React | 保留 (通用技术名词) |
| /hdd3/kykt26/... | omit (改为 "远端 GPU 服务器") |
| 服务器 env 名 (monst3r, dust3r, mast3r) | omit (改为 "对应模型运行环境") |

### Step 2: 更新 OUTLINE_V1.md

在各章节的 outline 中增加支柱 B 子节。参照 `PROPOSAL_EXPANSION_PLAN.md` §2.1 的映射表。

### Step 3: 扩展 DRAFT_INTERNAL_V1.md (逐章)

按以下指引在各章添加支柱 B 内容。**使用 Dream vocabulary (内部稿风格)**：

#### §1 研究背景 (+300-500 字)
- 在现有 3R 方向背景之后，增加一段：模型多样化带来的工程管理挑战
- 引出 KYKT 平台的必要性：统一管理 → 降低实验成本 → 加速研究闭环
- 保持学术性，不要写成产品介绍

#### §2 国内外研究现状 (+800-1200 字)
- 增加子节 §2.8（或合适编号）：现有 3R 工具链与平台综述
  - Nerfstudio (学术平台, 主要面向 NeRF)
  - Polycam / Luma AI / RealityCapture (商业产品, 不开源)
  - 各模型官方 demo (孤立, 不可对比)
  - 指出 gap：缺乏面向前馈式 3R 的统一聚合对比管理平台

#### §3 研究问题 (+500-800 字)

**重要：Q4 是项目主体问题之一，与 Q1-Q3 并列，不是辅助性质。**

- 增加 Q4：如何设计面向多模型 3R 研究的统一聚合管理与评估平台
  - 子问题：统一输出合同、跨模型对比评估、研究-应用对接
  - 与 Q1-Q3 的关系：Q4 为 Q1-Q3 的实证验证提供工程基础设施，同时自身也是独立的研究贡献
  - Q4 应具有与 Q1-Q3 同等的学术分量：有明确的研究问题、方法设计、实验验证、创新点

#### §4 研究方案 (+2000-3000 字, 核心新增)

**重要：支柱 B 为独立节 §4-B，与 §4-A (六模块架构) 并列。** 不是 §4.9 子节。建议结构：

- §4-A: Dream3R 新架构模型 (已有内容，不修改)
- §4-B: KYKT 聚合管理平台架构
  - §4-B.1 总体架构 (Tauri + React + FastAPI + SSH runner)
  - §4-B.2 模型注册与统一执行合同 (model_registry → runner → output contract)
  - §4-B.3 统一评估框架 (样例矩阵 + AI 评估层 + 人工评分)
  - §4-B.4 应用对接层设计 (仅概念层：动机 + 接口方向 + 下游场景举例，不展开 endpoint 设计)
  - §4-B.5 与 Dream3R 架构的协同 (Dream3R 消融实验 → KYKT 平台调度)

#### §5 实验设计 (+500-800 字)
- 在现有三层证据阶梯之后，增加平台层评测：
  - 新模型接入耗时 (目标: 1 天内完成 registry + runner + smoke)
  - 统一合同覆盖率 (6/6 模型已复用同一 output contract)
  - 跨模型对比矩阵完整度
  - API 对接能力验证

#### §6 预期成果与创新点 (+300-500 字)
- 增加 IP4：面向前馈式 3R 的统一聚合管理平台
  - 工程创新：统一模型合同 + 桌面级体验 + 研究-应用闭环
  - 与 IP1-IP3 的关系

#### §7 研究进展 (+800-1200 字)
- 增加子节：KYKT 平台开发进展
  - 6 模型已接入 model_registry (DUSt3R / MASt3R / MonST3R / Spann3R / Fast3R / CUT3R)
  - 4 模型已通过平台 smoke (MASt3R / MonST3R / Spann3R / Fast3R)
  - 桌面客户端：Tauri 2 + React + TypeScript, 已发布 exe / MSI / NSIS 安装包
  - AI 评估层：OpenAI-compatible advisor 已集成
  - 样例矩阵与对比评估框架已搭建
  - 远端部署管理 (SSH 调度 + PID 级取消 + 孤儿任务自愈)

#### §8 时间安排 (+300-500 字)

**重要：平台里程碑采用 P-1 / P-2 / ... 编号（区别于架构的 W1-W30），粒度为“阶段性交付物”。**

- 在 M1-M8 时间表中嵌入平台里程碑：
  - M1-M2：P-1 全部 6 模型 smoke + P-2 横向对比矩阵
  - M3-M5：P-3 API 导出层原型 + P-4 应用对接原型 + P-5 新模型扩展
  - M6-M8：P-6 便携打包发布 + P-7 平台综合评估
- 每个 P-N 里程碑应有明确的交付物定义，但不需要像 W1-W30 那样细到单个代码任务

#### §9 风险分析 (+300-500 字)
- 增加平台层风险：
  - 多模型 Python 环境 / CUDA 版本冲突
  - 远端服务器可用性 (GPU 资源竞争)
  - Tauri 生态在 Windows 上的兼容性
  - API 安全性与权限控制

### Step 4: 同步到 DRAFT_EXTERNAL_V1.md

按 STYLE_CONTRACT §3 规则做 vocab-clean snapshot。确保新增内容通过 §2 替换表清洗。

### Step 5: 运行 vocab 防火墙 grep

对 DRAFT_EXTERNAL_V1.md 全文件运行：
- **G3a**: `rg -i "cycle|SPEC-|DEC-|CR-[0-9]|agent|skill|workflow|本地项目" DRAFT_EXTERNAL_V1.md` → 期望 0 hits
- **G3b**: `rg -i "Dream3R" DRAFT_EXTERNAL_V1.md` → 期望 0 hits
- **G3a on KYKT additions**: 额外确认 `rg -i "KYKT|vision_ui|runner|smoke.test|local_jobs|model_registry" DRAFT_EXTERNAL_V1.md` → 期望 0 hits
- **G4**: `rg -i "最终架构方案|X 解决了|Dream3R 解决了|证明.*优于" DRAFT_EXTERNAL_V1.md` → 期望 0 hits

### Step 6: 重新编译 PDF

```powershell
pandoc DRAFT_EXTERNAL_V1.md -o deliverables/proposal_external_v1_2026-05-17.pdf --pdf-engine=xelatex -V CJKmainfont="SimSun" -V mainfont="SimSun" -V geometry:margin=2.5cm -V fontsize=12pt -V documentclass=article --from=markdown+pipe_tables+strikeout
```

### Step 7: 更新同步链

- STYLE_CONTRACT §6 sync log: 新增 expansion cycle entry
- Cycle log: 创建新 cycle log
- TASK_SNAPSHOT → WORKFLOW_STATUS → INDEX

## 硬约束

1. **内部稿是 master**：先写内部稿，再 snapshot 到外部稿
2. **candidate-not-final 措辞**：支柱 B 同样是候选方案，不是已验证产品。使用“候选平台设计” / “初步实现” / “当前版本” 等表述
   - 但注意：Q4 是项目主体问题，不要贬低其学术地位。“候选”指的是方案还未经过完整验证，而非它不重要
3. **证据标签**：
   - 已通过 smoke test 的模型 = engineering-demonstrated
   - 平台功能 = code-observed
   - API 导出层 = plan-level (尚未实现)
   - 应用对接 = plan-level
4. **不修改支柱 A 现有内容**：只在各章末尾或合适位置追加支柱 B 内容，不重写已有段落。但 §4 需要结构性调整：现有内容归入 §4-A，新增内容为 §4-B
5. **不实际写代码 / 不启动服务器 / 不下载模型**
6. **vocab-clean 必须 0 hits**：所有新增内容必须通过 G3a + G3b + 新增 KYKT vocab grep

## 预估产出

- 外稿新增 ~6000-9000 字 (总计 ~21000-24000 字)
- 内稿新增 ~8000-12000 字 (总计 ~27000-31000 字)
- STYLE_CONTRACT §2 新增 ~10-15 行 vocab 替换
- 新 PDF 编译

---

*本提示词由 Cascade 编写。如有疑问，参照 `PROPOSAL_EXPANSION_PLAN.md` 和 `STYLE_CONTRACT.md`。*
