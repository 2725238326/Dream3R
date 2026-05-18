# Dream3R v0.2 Architecture Handoff Prompt

将下面 `---` 之间的整段内容粘贴到新对话的第一条消息：

---

我们在做一个叫 Dream3R 的 3D 重建研究项目，正在推进 v0.2 架构 deltas。我先给你交代上一轮已经完成的工作和被中断的位置，再让你继续。请你先读完不要急着干活。

## 项目背景（一句话）

Dream3R = 控制图架构（control-graph-as-architecture）。核心创新：3R 领域不缺 backbone，缺一个验证 + 异构路由的控制层。v0.1 在 cycle 016 已经写出（specs/SPEC-20260506-001-dream3r-architecture.md, 1821 行），v0.2 在 cycle 018 进行中。

## 上轮 2026-05-06 用户决策（已 lock 在 DEC-20260506-002）

用户在多轮对话中逐项锁定了 v0.2 deltas：

```text
1. 稀疏注意力：YES (NSA 风格 token 级稀疏)
2. 注意力残差 / Kimi Linear / KDA：DROP（"和咱这个没关系"）
3. VGGT / MapAnything：DROP（"太重了，我们的方案就是要快速些"）
4. backbone：DINOv3-Small（替换 DUSt3R 原 ViT-L；~14x 参数缩减）
5. 速度优先级：(a) inference 实时为主，(b)(c) 兼顾
   目标 30-50 ms/frame at 30 FPS
6. Memory 路径：A (anchor bank retrieval) + B (hierarchical) + NSA 实现
7. 主 claim：A (Verification-as-architecture) + D (Heterogeneous
   best-of-N Composer) — 这是我推荐用户接受的
8. v0.2 形式：NEW spec 文件，不修改 v0.1 in-place
9. Composer 池：7 个轻量 3R（MASt3R / Fast3R / Spann3R / CUT3R /
   MoGe-2 / DepthAnything-V2 / Test3R）
```

## 上轮已交付的工件（cycle 018 S1-S3 done）

```text
decisions/DEC-20260506-002-cycle-018-launch-v02-architecture.md
   — v0.2 全部 deltas + drop 列表 + 主 claim 收窄锁定
planning/COMPOSER_CAPABILITY_DESCRIPTORS.md
   — 7 个轻量 3R 的 capability descriptor（innovation point / input
     regime / output schema / cost / attention regime / adapter
     sketch / capability_match / failure modes / evidence label）
   — 路由策略草稿 + cross-axis summary table
planning/NSA_MEMORY_INTEGRATION_MEMO.md
   — NSA 三分支映射到 v0.2 Memory 层级 (A+B)
   — bounded anchor bank K=256 + 选择门由 Critic confidence +
     Permanence link 共驱
   — 风险标注：LM-to-3R transfer speculative
planning/DINOV3_C1_INTEGRATION_MEMO.md
   — DINOv3-S 替 ViT-L 的迁移路径
   — 头部从头训；frozen-backbone 默认；-B fallback 文档化
   — 风险标注：pointmap 质量可能下滑
TASK_SNAPSHOT.md（已更新 header + Current task + Subtask board +
   If interrupted 块；F-001 rule 6: FIRST in sync chain）
registry/decision_registry.md（已 append DEC-002 行）
cycles/CYCLE-20260506-003.md（cycle 018 部分日志，S1-S3 done）
```

## 上轮被中断的位置

cycle 018 S4 + S5 部分未完成：

```text
S4 PENDING: specs/SPEC-20260506-004-dream3r-architecture-v02.md
   — v0.2 delta-only spec（~400-600 行；不重写 v0.1 主体）
   — 用三份 planning 工件作为 input
   — 章节建议：
     1. Identity / Approval（per DEC-20260506-002）
     2. Scope of v0.2 deltas（streaming-first 优先级 + 不重写 v0.1）
     3. Frame budget table（每帧 30-50 ms 组件分配）
     4. C1 Perceiver substitution（ViT-L -> DINOv3-S；引用集成 memo）
     5. C2 Memory implementation（anchor bank + NSA；引用集成 memo）
     6. Sparse attention 作为架构优化（不是主 claim）
     7. C5 Composer 池（引用 capability descriptors）
     8. Main claim narrowing（A + D 双柱；E supporting；B/C 降级）
     9. v0.1 Open Questions Q1-Q6 解决/搁置/继承
     10. Risks（v0.2 特定风险：DINOv3 质量下滑 / NSA 转移失败 /
         frame budget inferred 未测量）
     11. Boundaries（继承 v0.1 13 项 + v0.2 新增）
     12. Open Questions for v0.3
     13. Discipline notes
     14. Version history（指向 v0.1 + 跨引用）

S5 PARTIAL: 剩余 sync 链
   - registry/research_unit_registry.md：RU-007 状态从 "speculative
     only; keep for survey" 改为 "rejected for v0.2 scope; LM-to-3R
     transfer not pursued"（in-place edit 一行）
   - WORKFLOW_STATUS.md / RESEARCH_STATE.md / INDEX.md 轻量 sync
     （添加 cycle 018 + DEC-002 + 4 个新工件的指针）
   - specs/SPEC-20260506-001 v0.1 末尾添加 "Version history" 段
     指向 v0.2（不改 v0.1 主体；只追加尾部指针）
```

## 接下来怎么做

按这个顺序：

1. **必读**（不要跳过）：
   - `Dream/TASK_SNAPSHOT.md`（你将看到 cycle 018 状态 + 完整 If
     interrupted 块）
   - `Dream/decisions/DEC-20260506-002-cycle-018-launch-v02-architecture.md`
   - `Dream/planning/COMPOSER_CAPABILITY_DESCRIPTORS.md`
   - `Dream/planning/NSA_MEMORY_INTEGRATION_MEMO.md`
   - `Dream/planning/DINOV3_C1_INTEGRATION_MEMO.md`
   - `Dream/cycles/CYCLE-20260506-003.md`

2. **不要重读**（已在 TASK_SNAPSHOT TOC 里、F-001 anti-32MB 规则）：
   - `Dream/specs/SPEC-20260506-001-dream3r-architecture.md`（1821 行，
     95 KB）— 用 Grep -n 按需查具体段，**不要全文 Read**

3. **跨会话 memory**（必读）：
   - `C:\Users\27252\.claude\projects\e--kykt\memory\feedback_dream_mainline_architecture_first.md`
   - `C:\Users\27252\.claude\projects\e--kykt\memory\feedback_kykt_server_topology.md`

4. 读完之后，问我："要先写 SPEC-004 v0.2 spec（S4）还是先把
   S5 剩余 sync 一次性收尾？" 我会决定。

## 硬规则（不要踩）

```text
- 不训练 / 不下载 checkpoint / 不动代码 / 不动 KYKT 前后端
- 不重写 v0.1 spec 主体；v0.2 是 NEW 文件
- 每条 v0.2 delta 必须带 evidence label：
  paper-known / paper-derived / inferred / speculative
  NSA-to-3R = speculative；DINOv3-S 替换 = paper-derived；
  frame budget = inferred；Composer descriptors = paper-known
- F-001 anti-32MB：不要并发读多个大文件；优先 Grep -n + Edit；
  Write 仅用于新文件
- 不要把 B (state-ownership) / C (reservation tokens A7/A8) 删掉，
  它们降级为 discipline / future work，不是退场
- 不要把 RU-007 (KDA) 从 source map / unit bank 删掉；只更新
  status 为 "rejected for v0.2 scope; preserved as historical RU"
  （Honesty Override）
- Surgical Edits：只动需要动的文件 / 段落
- 每个新工件碰到大段 prose 时单文件不要超过 ~600 行
```

## 服务器和环境（仅参考；本轮不动）

```text
- IP: 172.17.140.97, 用户: kykt26
- conda env: dream3r (torch 2.5.1+cu121, mamba-ssm 2.2.4)
- GPU: 4 x TITAN RTX 24GB
- v0.2 全是 markdown，本轮不需要 ssh，但 NSA / DINOv3 任何
  实现尝试都需要单独 DEC 授权（不是这轮干）
```

读完上面所有必读文件后，告诉我你看到的状态，然后等我说"继续 S4"或"先收尾 S5"或别的方向。**先不要开始写代码或动任何 spec/ 下面的文件。**

---

## 给你（用户）的备注

- 如果你想保持上轮的精确路径，直接粘贴上面整段就行
- 如果你想换个方向（比如先放弃 v0.2 转去做别的），把上面整段后追加："**改方向**：xxx"
- 如果你想让新对话直接动手写 SPEC-004 而不是先确认，把上面"读完之后..."那段改成"**读完直接写 S4，按 DEC-002 的章节大纲，章节建议见上**"
