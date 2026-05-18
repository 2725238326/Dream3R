# STYLE_CONTRACT — Dream3R 开题报告双稿语言风格契约

| 字段 | 取值 |
|---|---|
| 文件类型 | planning artifact (双稿语言风格契约 + sync rule) |
| 创建日期 | 2026-05-16 |
| 状态 | v1.1 active (cycle 036 启动 → cycle 042 最终修订 → expansion cycle 开始; §2 vocab 62 行; §6 sync log 7+1 entries) |
| 授权根 | DEC-20260516-001 (cycle 036) + DEC-20260516-002 (cycle 037) + DEC-20260516-003 (cycle 038) + DEC-20260516-004 (cycle 039) + DEC-20260517-001 (cycle 040) + DEC-20260517-002 (cycle 041) + DEC-20260517-003 (cycle 042) |
| 触及范围 | 仅本文件; 同步规则约束 DRAFT_INTERNAL_V1.md ↔ DRAFT_EXTERNAL_V1.md |

## 1. 契约目的

Dream3R 开题报告按用户决策采用双稿:

- 内部稿 `DRAFT_INTERNAL_V1.md` — Dream-vocabulary 内部使用; 含 Dream / Dream3R / cycle / SPEC / DEC / CR / Track A / W1-W22 等内部 workflow 术语; 直接引用 Dream 项目工件路径与 ID; 对内部审计 + 后续 cycle 回溯友好
- 外部稿 `DRAFT_EXTERNAL_V1.md` — 学术中文; 完全剥离 Dream-vocabulary; 用 "候选架构 X" / "本研究架构" 替代 Dream3R; 用学术化通用词汇替代 SPEC/DEC/CR/W-task 等编号; 对外审阅友好 (导师 / 学院 / 论文评审)

本契约规定: (a) 双稿之间的 vocabulary 一一映射 (§2 替换表); (b) 双稿同步规则 (§3 internal-is-master + 周期性 external 快照); (c) 候选架构 X 命名引入规则 (§4); (d) candidate-not-final 关键句式表 (§5)。

## 2. Vocabulary 替换表 (seed; cycle 037+ 扩充)

下表是双稿对译规则。新增条目按 cycle 编号在 §6 sync log 中记录。

| 内部稿 (DRAFT_INTERNAL) | 外部稿 (DRAFT_EXTERNAL) | 备注 / 决策来源 |
|---|---|---|
| Dream3R | 候选架构 X / 本研究架构 | 用户 2026-05-16 AskUserQuestion 决定 |
| Dream / Dream 项目 | (omit; 改写为 "本研究" / "该研究项目") | 内部 framework 名称不外露 |
| Track A / Track B | 主线工作 / 综述工作 | 仅在叙述上下文中使用; 否则 omit |
| SPEC-YYYYMMDD-NNN | "体系结构设计文档 v0.X" / "消融实验方案 v0.X" / "比较方法图谱 v0.X" 等中文化 | 不暴露 SPEC ID |
| DEC-YYYYMMDD-NNN | "项目关键决策 N" / "本研究的设计决策" | 不暴露 DEC ID; 必要时仅说 "项目决策" |
| CYCLE-YYYYMMDD-NNN | "研发周期 N" / "项目阶段 N" | 不暴露 cycle ID |
| CR-1 .. CR-6 | "信号校验规则族 (1-6)" / "跨模块信号契约的六条规则" | 集体名称替代; 不暴露 CR-N 编号 |
| W1 .. W22 / W19-W30 | "实现里程碑 1-22" / "近期工作里程碑 19-30" | 中文化 + 高层化 |
| F-001 / F-002 | "内部工作规则" / "算力部署约束 (远端服务器执行)" | 高层化 |
| agent / Dream agent / 子智能体 | (omit; 改写为 "本研究的执行流程" / "作者") | 内部 workflow 词汇 |
| skill / Claude skill | (omit; 改写为 "工具" / "脚本") | 同上 |
| workflow / research workflow | (omit; 改写为 "研究流程" / "研究方法") | 同上 |
| 本地项目 / 项目内部 | (omit; 改写为 "本研究") | 内部上下文术语 |
| KYKT / KYKT 服务器 | (omit; 改写为 "远端服务器" / "实验环境") | 内部服务器名称 |
| ablate_recurrence.py | "消融实验脚本" | 文件名中文化 |
| ABL-memory-N / ABL-v02-N | "记忆模块消融实验 N" / "架构 v0.2 消融实验 N" | 编号中文化 |
| evaluate_real_sequence.py | "真实数据评测脚本" | 文件名中文化 |
| AnchorBank / K=256 | "空间锚点存储 / 容量 256" | 中文化 |
| NSA three-branch | "三分支稀疏注意力 (压缩 / 选择 / 滑窗)" | 中文化 + 子结构展开 |
| StateToken / Mamba hybrid | "状态记忆向量" / "Mamba-Transformer 混合循环结构" | 中文化 |
| pointmap L2 = 20.47 | "点图 L2 误差 20.47 (作为集成证据, 非训练后质量)" | 数值保留, 上下文标注 |
| 4DGS asset | "四维高斯渲染资产 (4D Gaussian Splatting)" | 首次出现展开英文 |
| C1 Perceiver | 感知模块 / 视觉骨干 | 模块名中文化 (cycle 038 §4 添加) |
| C2 Memory | 记忆模块 | 同上 |
| C3 Permanence | 永久性模块 | 同上 |
| C4 Critic | 校验模块 | 同上 |
| C5 Composer | 编排模块 / 多专家组合层 | 同上 |
| C6 Bus | 总线模块 / 信号契约层 | 同上 |
| Pillar A / Pillar D | 主线 A / 主线 D | 主张层中文化 (cycle 038 §4 添加) |
| Delta N (v0.2 spec delta) | "(内部设计文档中的某项 delta)" / omit | spec ID 不暴露 |
| A5 reroute_model | 路由切换动作 / 切换模型动作 | 动作名中文化 |
| repair actions 0/1/2/3/4/5 | 修复动作 0/1/2/3/4/5 | 数字保留, 动作名中文化 |
| conflict_score / theta_conflict | 冲突评分 / 冲突阈值 | 信号 + 阈值中文化 |
| capability_match (spread) | 能力匹配度 (跨度) | 描述符中文化 |
| cost_adjusted_match | 成本调整后的匹配度 | 同上 |
| epsilon_tie | 平局窗口 | 同上 |
| fail_fast / fail_fast_threshold | 早期失败 (阈值) | 同上 |
| evidence label | 证据标签 | 信号属性中文化 |
| forward-reference null protocol | 前向引用空协议 | v2.1 子协议中文化 |
| permanence_link | 永久性 link | 信号路径名半中文化 |
| signal names (suppress_static_write / latent_drift_proxy / write_value_estimate 等) | 保留英文 (作为引号包裹的信号名) | signal ID 不强制中文化, 上下文以中文解释 |
| C4' (TTT 路径模块代号) | omit / "后续候选模块" | cycle 039 §3.1 添加; v0.4 spec delta B1 候选未实装时引用 |
| Innovation Point / IP1 / IP2 / IP3 | 保留英文 + 中文括注 (e.g., IP1: 校验作为架构组件) | cycle 039 §6.2 添加; 双稿一致, 无替换 |
| hard_fail / soft_fail | 硬失败 / 软失败 (双稿一致, 半中文化保留信号语义) | cycle 040 §5.3 添加; cycle 029 v1.1 ablation rule 命名 |
| oracle-bus | 理想信号总线 (作为上界估计基准, 非实际部署组件) | cycle 040 §5.3 添加; ABL-memory-0 oracle 路径命名 |
| monotone upgrade gate | 单调升级门 (评测一致性约束) | cycle 040 §5.4 添加; CRITIC_CALIBRATION_PLAN_V1 校准方法 B 命名 |
| fixture regime R1-R5 | 校准 fixture 制度 R1-R5 | cycle 040 §5.4 + §5.6 添加; CRITIC_CALIBRATION_PLAN_V1 五类合成失败注入命名 |
| 集成证据 (integration evidence) | 集成证据 (integration evidence; 区别于训练后质量) | cycle 040 §7.3 添加; RECENT_PROGRESS.md line 78 boundary statement 标签 |
| R-OOD-1 / R-EXT-PRIOR-1 / R-4DGS-LIC-1 / R-INPUT-EXT-1 | 域外检测缺口 / 外部先验冲突 / 可渲染输出许可链 / 输入扩展空缺 (内部 R-编号 omit) | cycle 041 §9 添加; WORK_RISK_REGISTER v1.1 +4 cross-spec 风险中文化 |
| R-PROP-VOCAB-1 / R-PROP-CLAIM-1 / R-PROP-SYNC-1 | (内部稿保留 R-编号; 外部稿 omit, 改写为 vocab 泄漏风险 / over-claim 风险 / 双稿语义漂移风险) | cycle 041 §9.5 添加; WORK_RISK_REGISTER v1.2 +3 proposal-cycle 风险中文化 |
| KYKT / KYKT 平台 | 本研究管理平台 / 聚合管理平台 | expansion cycle 添加; 支柱 B 项目名称 |
| vision_ui | 平台前端 / 桌面客户端 | expansion cycle 添加; 前端代码仓库名 |
| runner / ssh_runner | 模型执行器 / 远端推理调度器 | expansion cycle 添加; 执行层组件名 |
| model_registry | 模型注册层 | expansion cycle 添加; 注册抽象层 |
| smoke test (平台层) | 集成验证 / 端到端验证 | expansion cycle 添加; 平台层验证步骤命名 |
| job.json / status.json | 任务描述文件 / 状态文件 | expansion cycle 添加; 平台输出合同文件名 |
| scene_meta.json | 输出元数据合同 | expansion cycle 添加; 平台统一输出元数据文件名 |
| local_jobs/ | 本地任务缓存 | expansion cycle 添加; 本地缓存目录名 |
| Tauri / Tauri 2 | 保留 (通用桌面框架名, 不替换) | expansion cycle 添加; 通用技术名词保留 |
| FastAPI / React / TypeScript | 保留 (通用技术名词, 不替换) | expansion cycle 添加; 通用技术名词保留 |
| /hdd3/kykt26/... (服务器绝对路径) | omit (改为 "远端 GPU 服务器" / "远端实验环境") | expansion cycle 添加; 内部路径不外露 |
| 服务器 env 名 (monst3r, dust3r, mast3r, spann3r 等) | omit (改为 "对应模型运行环境") | expansion cycle 添加; conda env 名不外露 |

**新增规则**: 任何上表未列出的内部术语在内部稿首次出现时, 在外部稿同步出现时必须在本表追加一行, 并在 §6 sync log 记录新增。

## 3. 双稿同步规则 (internal-is-master + 周期性 external 快照)

```text
规则 1: 内部稿是 master.
  - 任何研究内容变更先落 DRAFT_INTERNAL_V1.md
  - 内部稿可以独立编辑 (无需立即同步外部稿)

规则 2: 外部稿是 internal 的周期性快照.
  - cycle 末尾 (在 cycle log close 之前) 把内部稿当前 cycle 新增 / 修订的内容快照到外部稿
  - 快照时按 §2 vocab 替换表逐项替换
  - 快照后在本文件 §6 sync log 追加一行

规则 3: 外部稿 standalone 编辑限制.
  - 允许: 语序调整 / 标点修订 / 段落分割 / 字体强调标记 (这些是 prose smoothing)
  - 不允许: 增删段落 / 修改技术claim / 新增 / 删除 example / 引入新方法名
  - 任何语义变更必须先在内部稿落地, 然后整段重新快照到外部稿

规则 4: 每次 sync 后跑 vocab 防火墙 grep 验证.
  - 命令: Grep 在 DRAFT_EXTERNAL_V1.md 上跑 pattern `cycle|SPEC-|DEC-|CR-N|agent|skill|workflow|本地项目` (返回应为 0 hits)
  - 加跑: Grep 在 DRAFT_EXTERNAL_V1.md 主体上跑 pattern `Dream3R` (case-insensitive; 返回应为 0 hits except references 区域)
  - 失败则回滚该 sync 并修订

规则 5: cycle 末尾的 sync 操作本身不构成 cycle log 的 "subtask"; 它是 cycle close 的前提条件之一.
```

## 4. 候选架构 X 命名引入规则

外部稿 §1 首次提及代号时, 必须用如下句式引入:

```text
本研究提出并评估一个代号为 "候选架构 X" (Candidate Architecture X) 的前馈式
3R 架构. 为简洁计, 以下正文均以 "候选架构 X" 或 "本研究架构" 指代该架构.
```

之后正文使用规则:

- 一种主用词为主 (建议 "候选架构 X" 是主用; "本研究架构" 是次用, 用于句法变换避免重复)
- 不混用其他指代 (e.g., 不出现 "我们的架构" / "Dream3R" / "X 系统" 等)
- 在 §6 预期成果 + §3 候选研究问题 等位置, 强调 "候选" 字义 (与 candidate-not-final 配合, 见 §5)

内部稿首次提及时直接用 "Dream3R", 不需引入代号。

**references.bib 例外**: 如果引文标题中本身包含 "Dream3R" 字符串 (例如假设未来 Dream3R 正式发表), 该字符串作为 paper-derived bibliography 字段不受本规则约束。但目前 (2026-05-16) Dream3R 尚未正式发表, references.bib 中也不应出现 Dream3R 字符串。

## 5. Candidate-not-final 关键句式对比表

per DEC-20260501-011 (thesis reframe; Dream3R 为 candidate-not-final) + DEC-20260504-002 (no-all-in; 不收敛到单一 finalist), 开题报告语言必须避免 "Dream3R / 候选架构 X 是最终方案" 的暗示。下表给出禁用 / 允许句式对照:

| 禁用句式 (over-claim) | 允许句式 (candidate-not-final) |
|---|---|
| "证明 X 优于 SOTA" | "评估 X 在 ... 维度上是否相对 SOTA 呈现优势" |
| "X 是最佳架构" | "X 是被评估的候选架构之一" |
| "X 解决了 OOD 问题" | "X 设计了 OOD 检测路径的候选方案; 实证效果待验证" |
| "X 是最终设计" | "X 是当前迭代的候选; 后续版本可能修订或替换" |
| "本研究将证明 ..." | "本研究将考察 X 在 ... 维度上的表现" |
| "X 显著优于 baseline" | "X 与 baseline 在 ... 指标上的对比结果将作为评估依据" |
| "X 不存在 OOD 问题" | "X 对 OOD 场景的鲁棒性是后续验证目标之一" |
| "唯一可行的方案" | "本研究探索的候选方案之一" |
| "完全解决了长序列内存问题" | "针对长序列内存机制提出了候选架构层方案" |

外部稿与内部稿同时受本句式表约束 (内部稿即使用 Dream3R 命名, 也应避免 over-claim, 因为 candidate-not-final 是研究决策而非语言决策)。

## 6. Sync log (append-only)

按时序追加。每行记录: `cycle NNN · §X · sync direction · vocab substitutions · vocab-grep verification`。

```text
2026-05-16 · cycle 036 close · §1 initial draft created in both internal and external · 13 vocab substitutions seeded in §2 · DRAFT_EXTERNAL_V1.md §1 grep verified clean (0 hits on cycle|SPEC-|DEC-|CR-N|agent|skill|workflow|本地项目 + 0 hits on Dream3R case-insensitive)
2026-05-16 · cycle 037 close · §2 国内外研究现状 drafted in DRAFT_INTERNAL_V1.md (~4200 字, Dream-vocabulary master) then snapshotted to DRAFT_EXTERNAL_V1.md (~3700 字, vocab-clean using 代号 候选架构 X / 本研究架构) · 7 sub-sections (2.1 基础谱系 / 2.2 多视角规模化 / 2.3 视频动态 4D / 2.4 长序列内存四类 B1-B4 / 2.5 测试时三类 C1-C3 / 2.6 输出资产三类 D1-D3 / 2.7 综述四轴覆盖矩阵 + 落点) · vocab substitutions used (delta over §1 seed; no new rows added to §2 substitution table this cycle, all substitutions covered by existing 22-row seed): Dream3R → 候选架构 X / 本研究架构; SPEC-20260506-004 v0.2 / SPEC-20260508-001 v0.3 / SPEC-20260507-001 v0.2 → omit (replaced with paraphrase via "多专家组合层" / "记忆模块" / "比较图谱" 等中文化命名); CYCLE-20260515-001 / cycle 035 → omit (replaced with "本研究后续阶段计划" / "同期内部规划文档"); CR-1..CR-6 → "信号校验规则族 (1-6)"; DEC-20260504-002 → "本研究的不押注单一支线设计"; W17/W18 → omit (replaced with "已经实装到张量契约级别"); AnchorBank K=256 → "空间锚点存储 (容量 256)"; NSA three-branch → "三分支稀疏注意力 (压缩 / 选择 / 滑窗)"; StateToken → "状态记忆向量"; Mamba hybrid → "Mamba-Transformer 混合循环结构"; 4DGS asset → "4DGS 资产 / 四维高斯渲染资产 (4D Gaussian Splatting)"; SOTA_MATRIX_V2 / WORK_RISK_REGISTER / CRITIC_CALIBRATION_PLAN_V1 / LONG_SEQ_REAL_TABLE_PLAN → "若干本研究的内部规划文档" / "本研究的明确实证缺口" / "本研究的实证缺口" 等高层化命名 · G3a vocab firewall grep on full DRAFT_EXTERNAL_V1.md (pattern cycle|SPEC-|DEC-|CR-N|agent|skill|workflow|本地项目): 0 hits · G3b Dream3R case-insensitive grep on full DRAFT_EXTERNAL_V1.md: 0 hits · G4 over-claim grep on both drafts §2 (pattern 证明.{0,10}优于|最佳.{0,5}架构|最终.{0,5}架构|X 解决了|Dream3R 解决了): 0 hits on both
2026-05-16 · cycle 038 close · §4 研究方案 (外部稿) / §4 Dream3R v0.3 架构 (内部稿) drafted in DRAFT_INTERNAL_V1.md (~4000 字 Dream-vocabulary master, C1-C6 编号 + Delta 1/2/3/5/6 引用 + CR-1..CR-6 引用) then snapshotted to DRAFT_EXTERNAL_V1.md (~3000 字 vocab-clean 六模块中文化命名) · 8 sub-sections (4.1 整体设计 + 帧预算 / 4.2 感知模块 C1 Perceiver DINOv3-S / 4.3 记忆模块 C2 三分支 + 锚点存储 + 状态记忆向量 + Mamba 混合 / 4.4 永久性模块 C3 Slot Attention + permanence_link / 4.5 校验模块 C4 Sampson + depth + 共视 + 修复动作 0-5 / 4.6 编排模块 C5 7 专家池 / 4.7 总线模块 C6 六条信号校验规则 / 4.8 与现有 3R 系统的结构差异) · §2 vocab substitution table appended 19 new rows (C1-C6 → 感知 / 记忆 / 永久性 / 校验 / 编排 / 总线 模块; Pillar A/D → 主线 A/D; Delta N → omit; A5 reroute_model → 路由切换动作; repair actions 0-5 → 修复动作 0-5; conflict_score / theta_conflict → 冲突评分 / 冲突阈值; capability_match spread → 能力匹配度跨度; cost_adjusted_match → 成本调整后的匹配度; epsilon_tie → 平局窗口; fail_fast → 早期失败; evidence label → 证据标签; forward-reference null protocol → 前向引用空协议; permanence_link → 永久性 link; signal names suppress_static_write / latent_drift_proxy / write_value_estimate → 保留英文上下文中文解释) · 22-row seed 表升级到 41 行总计 · 1 corrective edit needed: cycle 037 在 grep 之后追加的 DRAFT_EXTERNAL_V1 元数据 row "最后更新 | 2026-05-16 (cycle 037 §2 起草; +~3700 字)" 在 cycle 037 prose-only G3a 范围外, 但 cycle 038 全文件 G3a 范围内触发 1 hit; rephrased 为 "最后更新 | 2026-05-16 (§2 + §4 起草, 累计正文 +~7000 字)" 去除 cycle 字串 · G3a full-file grep 复跑 0 hits · G3b 0 hits · G4 0 hits on both drafts (full file)
2026-05-17 · cycle 039 close · §3 候选研究问题 + §6 预期成果与创新点 drafted together in DRAFT_INTERNAL_V1.md (§3 ~1800 字 + §6 ~1300 字 = ~3100 字 Dream-vocabulary master, Q1/Q2/Q3 + 三个 IP + 4-finalist 独立性 + candidate-not-final 声明) then snapshotted to DRAFT_EXTERNAL_V1.md (§3 ~1500 字 + §6 ~1000 字 = ~2500 字 vocab-clean 三个研究问题 + 三个 IP) · §3 5 sub-sections (3.1 Q1 验证机制 + 3.2 Q2 长序列内存 + 3.3 Q3 多专家组合 + 3.4 4-finalist 模块独立性 + 3.5 候选 vs 最终 研究地位) · §6 3 sub-sections (6.1 预期交付物 + 6.2 三个 IP 声明 + 6.3 与现有工作的实证差异) · §2 vocab substitution table appended 2 new rows (C4' TTT 路径模块代号 → omit / "后续候选模块"; Innovation Point / IP1/IP2/IP3 → 保留英文 + 中文括注, 双稿一致无替换) · 41-row 表升级到 43 行总计 · G3a full-file grep 0 hits · G3b 0 hits · G4 7 corrective edits needed (cycle 036 precedent): negation-context occurrences of forbidden patterns ("最终架构方案" / "X 解决了" / "Dream3R 解决了" / "证明 ... 优于") explicitly used in candidate-not-final 句式 examples ("不说 X 解决了..., 说 X 提供了...候选证据") triggered grep hits in §3.2 + §3.3 + §3.5 + §6.1 + §6.2 IP1 + §6.2 IP3 + §6.2 closing paragraph; rephrased to "最终方案" / "X 已完全解决" / "Dream3R 已完全解决" / "宣称 ... 优于" to remove literal forbidden substrings while preserving 句式 contrast semantics; G3a + G3b + G4 re-greps all 0 hits on both drafts (full file) · 累计正文 § 1 + § 2 + § 3 + § 4 + § 6 ~11300 内 + ~9500 外 字 ≈ 54% of OUTLINE_V1 §2 表 总字数估算 (~21100 内 / ~16000 外) · candidate-not-final 句式 大规模应用本 cycle 完成, §3.5 + §6.2 + §6.3 是 STYLE_CONTRACT §5 句式对比表的最高密度应用
2026-05-17 · cycle 042 close · 最终修订 + PDF 编译 + 提交 packaging (DEC-20260517-003 authorized) · no new body text drafted (content frozen after cycle 041 通稿审查) · bottom metadata cleanup: DRAFT_INTERNAL_V1.md stale metadata block (cycle 036 scaffold) replaced with §1-§9 completion state; DRAFT_EXTERNAL_V1.md same; orphaned sync table in DRAFT_INTERNAL_V1.md removed (STYLE_CONTRACT §6 is authoritative sync log) · §8.1 短期 timeline past-tense fix: cycle 040/041 marked 已完成, cycle 042 marked 本 cycle · references.bib copied from Track B survey 44 entries · PDF compiled via pandoc 3.9 + xelatex (MiKTeX) + SimSun: proposal_external_v1_2026-05-17.pdf 263 KB, exit code 0, 6 missing-glyph warnings (↔ U+2194 cosmetic only) · deliverables/ created: SUBMISSION_PACKAGE_ADVISOR_PROPOSAL_2026-05-17.md (~500 字 Chinese cover note, 6 sections) + SUBMISSION_RECORD_PROPOSAL_2026-05-17.md (yaml metadata + checklist) · G3a vocab firewall on cover note: 0 hits (clean) · G3b Dream3R firewall on cover note: 0 hits (clean) · no §2 vocab table changes (50 rows unchanged) · §1-§9 全部章节 + PDF + 提交 packaging complete; proposal track closed
2026-05-17 · cycle 041 close · §9 风险分析与应对 drafted in DRAFT_INTERNAL_V1.md (~1500 字 Dream-vocabulary master, 6 sub-sections: 9.1 架构层风险 5 per-spec + 9.2 跨模块风险 R-OOD-1/R-EXT-PRIOR-1/R-4DGS-LIC-1/R-INPUT-EXT-1 + 9.3 实证执行風险 集成证据 vs 质量 boundary + ABL plan-only + 数据集 license + 9.4 工程时序風险 W19-W30 + v0.4 delta + 3DGS license + 9.5 开题报告 process 風险 R-PROP-VOCAB-1/R-PROP-CLAIM-1/R-PROP-SYNC-1 + 9.6 風险应对策略 P0/P1/P2 表) then snapshotted to DRAFT_EXTERNAL_V1.md (~1000 字 vocab-clean 5 sub-sections: 9.1-9.4 架构层/跨模块/实证执行/工程时序 + 9.5 风险应对策略; §9.5 开题报告 process 风险 omitted from external per vocab-clean rule) · §2 vocab substitution table appended 2 new rows (R-OOD-1/R-EXT-PRIOR-1/R-4DGS-LIC-1/R-INPUT-EXT-1 → 域外检测缺口/外部先验冲突/可渲染输出许可链/输入扩展空缺; R-PROP-VOCAB-1/R-PROP-CLAIM-1/R-PROP-SYNC-1 → vocab 泄漏风险/over-claim 风险/双稿语义漂移风险) · 48-row 表升级到 50 行总计 · G3a full-file grep 0 hits (first-pass clean) · G3b 0 hits (first-pass clean) · G4 1 corrective edit needed on DRAFT_INTERNAL_V1.md §9.5: negation-context literal "证明 X 优于 / X 是最终设计" in R-PROP-CLAIM-1 description rephrased to "over-claim 表述 (宣称优越性 / 宣称为最终设计 等)" per cycle 039 precedent; G4 re-grep 0 hits on both drafts · G4 DRAFT_EXTERNAL_V1.md first-pass 0 hits · 通稿审查 completed: §7.3 集成证据 caveat present + §5 plan-only caveats present + §8 candidate timeline framing present + §3.5/§6.2/§6.3 candidate-not-final 措辞 advisor-readable + §7.6 编号密度 acceptable + no §1-§8 surgical edits needed · 累计正文 §1-§9 ~19300 内 + ~15000 外 字 ≈ 92% of OUTLINE_V1 §2 表 总字数估算 (~21100 内 / ~16000 外) · §1-§9 全部章节 dual-draft 完整, ready for cycle 042 最终修订 + PDF 编译
2026-05-17 · expansion sync · 支柱 B 完整同步 DRAFT_INTERNAL_V1.md → DRAFT_EXTERNAL_V1.md · 9 insertion points: §1.7 (支柱 B 动机) / §2.8 (3R 工具链综述) / §3.6 Q4 (统一聚合平台研究问题) / §4 intro update (双支柱) + §4-B (平台架构 5 sub-sections) / §5.8 (平台层评测标准) / §6 intro update (4 IPs) + IP4 声明 + §6.3 平台工程差异 / §7 intro update (7 subsections) + §7.7 (平台进展) / §8.4 (平台里程碑 P-1..P-7) / §9 intro update (5 layers) + §9.5 (平台层风险) + §9.6 renumber + 平台行 · vocab substitutions: KYKT → 聚合管理平台; vision_ui → 平台前端; runner → 模型执行器; model_registry → 模型注册层; job.json → 任务描述文件; status.json → 状态文件; scene_meta.json → 输出元数据合同; /hdd3/kykt26 → 远端 GPU 服务器; conda env names → omit · additional vocab fixes (pre-existing leaks): kykt26 → 远端 GPU 服务器 (§7.2); C2 记忆模块 → 记忆模块 (§5.3 / §7.2 / §7.6); conda env on server → 远端服务器运行环境 (§7.6) · G3a/G3b/G4 全部 0 hits · 外部稿元数据更新: 状态 含支柱 B 扩展; 字数 ~21000 字 (A ~15000 + B ~6000) · §2 vocab table unchanged (50 rows)
2026-05-17 · cycle 040 close · §5 实验设计与评测协议 + §7 研究进展与已完成工作 + §8 研究计划与时间安排 drafted together in DRAFT_INTERNAL_V1.md (§5 ~2800 字 + §7 ~2200 字 + §8 ~1500 字 = ~6500 字 Dream-vocabulary master; ABL-v02-1..10 + ABL-memory-0..11 + CRITIC_CALIBRATION_PLAN_V1 + LONG_SEQ_REAL_TABLE_PLAN + W1-W18 + KITTI smoke + 综述 + cycle 历史 + M1-M8 时间表) then snapshotted to DRAFT_EXTERNAL_V1.md (§5 ~2000 字 + §7 ~1500 字 + §8 ~1000 字 = ~4500 字 vocab-clean 评测协议 + 研究进展 + 时间安排) · §5 7 sub-sections (5.1 三层证据阶梯 / 5.2 架构层消融 / 5.3 记忆机制消融 / 5.4 Critic 标定 / 5.5 长序列真实评测 / 5.6 评测数据集 / 5.7 主要评测指标) · §7 6 sub-sections (7.1 架构设计文档系列 / 7.2 实现里程碑 W1-W18 / 7.3 KITTI 集成证据 / 7.4 综述发布 / 7.5 综述反哺 / 7.6 cycle 历史) · §8 3 sub-sections (8.1 短期 M1-M2 / 8.2 中期 M3-M5 / 8.3 长期 M6-M8) · §2 vocab substitution table appended 5 new rows (hard_fail / soft_fail → 硬失败 / 软失败 双稿一致; oracle-bus → 理想信号总线 (上界估计基准); monotone upgrade gate → 单调升级门; fixture regime R1-R5 → 校准 fixture 制度 R1-R5; 集成证据 (integration evidence) → 集成证据 双稿一致 区别于训练后质量) · 43-row 表升级到 48 行总计 · G3a + G3b 5 corrective edits needed (cycle 036 + cycle 039 precedent): 4 G3a hits + 1 G3b hit on first pass — §5.3 closing paragraph "cycle 040 仅 plan-level 引用" 改写为 "本阶段仅 plan-level 引用"; §7.5 deliverables list "dream3r 实现仓库" (lowercase repo name) 改写为 "本研究架构实现仓库"; §7.5 "proposal-cycle 相关 vocab firewall / claim 过度 / 双稿语义漂移 三 行" 改写为 "开题报告阶段相关 vocab 防火墙 / claim 过度 / 双稿语义漂移 三行"; §8.1 short-term bullet "(cycle 外人工动作)" 改写为 "(本阶段外人工动作)"; §8.2 medium-term bullet "cycle 040 后第一个 unblocked task" 改写为 "本阶段后第一个 unblocked task" · G4 0 hits on first pass (§5 + §7 + §8 不再含 cycle 039 那种 candidate-not-final 句式 contrast 高密度段落, 因此 negation-context literal 没有 trigger) · G3a + G3b + G4 re-greps all 0 hits on both drafts (full file) · 累计正文 § 1 + § 2 + § 3 + § 4 + § 5 + § 6 + § 7 + § 8 ~17800 内 + ~14000 外 字 ≈ 85% of OUTLINE_V1 §2 表 总字数估算 (~21100 内 / ~16000 外) · 实证-anchored 章节首次 stress test on vocab 替换表 + sync rule + candidate-not-final 句式 三重约束, 5 corrective edits 全部围绕 "cycle" 字串泄漏 (§7.5 内部 sync chain 描述 + §5.3 计划性表述 + §8 时间表 + §7.5 仓库 lowercase 命名 leak) 而非 over-claim 句式; cycle 041 通稿审查 + §9 风险章节为唯一剩余 chapter
```

cycle 037+ 起草 §2 后追加。cycle 039 close 2026-05-17 追加 §3 + §6 entry。cycle 040 close 2026-05-17 追加 §5 + §7 + §8 entry。cycle 041 close 2026-05-17 追加 §9 entry。cycle 042 close 2026-05-17 追加 最终修订 + PDF 编译 entry。expansion cycle 2026-05-17 追加 §2 KYKT vocab +12 行 + OUTLINE + DRAFT 双支柱扩展 entry。expansion sync 2026-05-17 追加 支柱 B 完整同步 entry (§1.7 / §2.8 / §3.6 Q4 / §4-B / §5.8 / §6 IP4 + §6.3 平台工程差异 / §7.7 / §8.4 / §9.5 + §9.6 表)。

## 7. 不在本契约范围内的事项

本契约 **不** 规定:

- 开题报告的章节结构 (那是 OUTLINE_V1.md 的范围)
- 开题报告的技术内容 (那是 DRAFT_INTERNAL_V1.md / DRAFT_EXTERNAL_V1.md 各章节的范围)
- 开题报告的字数 / 篇幅总量 (那是 OUTLINE_V1.md 的估算范围)
- 引文管理与 references.bib 结构 (留给 cycle 037+ §2 国内外研究现状起草时定型)
- 图表生成 (留给 cycle 037+; 可能复用 Track B 综述 TikZ 图源, 但需在内部稿明确引用关系)

## 8. 元数据与上游链接

| 字段 | 取值 |
|---|---|
| 文件路径 | `Dream/planning/proposal_dream3r/STYLE_CONTRACT.md` |
| 创建日期 | 2026-05-16 |
| 状态 | v1 active |
| 作者 | Dream agent (cycle 036) |
| 上游决策 | DEC-20260516-001 (cycle 036 launch) + DEC-20260501-011 (candidate-not-final) + DEC-20260504-002 (no-all-in) + 用户 2026-05-16 AskUserQuestion 答案 |
| 相邻工件 | OUTLINE_V1.md (章节结构) / DRAFT_INTERNAL_V1.md (内部稿) / DRAFT_EXTERNAL_V1.md (外部稿) |
| 下游 | cycle 037+ §2-§9 起草将持续扩充 §2 替换表 + §6 sync log |

---

**End of style contract v1.** 本契约是 cycle 036 P0-B 子任务 deliverable; cycle 037+ 起草 §2 时按 §3 sync 规则同步并扩充本契约。
