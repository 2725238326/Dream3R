# Dream3R Mainwork — Architecture Implementation Roadmap

**Version:** 1.0  
**Date:** 2026-05-23  
**Author:** Cascade (handoff to next agent)  
**Status:** Active

---

## 0. 假设与目标（请用户确认）

**默认目标：工作 demo（option 2）** — 在 KITTI 上跑通端到端，输出真实 pointmap，并对一个核心创新点（NSA memory 或 Composer routing）做有效性对比。**不追求 SOTA，追求每个数字真实**。

如目标变化：
- 选 option 1（顶会）：所有 stage 完成后还需加 ScanNet/ETH3D + 完整消融 + baseline 复现
- 选 option 3（PoC）：只做 Stage 1 + Stage 2 即可
- 选 option 4（提案级）：只做 Stage 1，定性结果即可

---

## 1. 当前现实诊断

**v0.5 架构是空壳。** 数据流：
```
随机 tensor → Linear projection → Memory/Critic/Composer (无意义) 
            → 8 个 Expert (全部 fallback) → 假 pointmap → 形状测试通过
```

**v0.5 已闭合的工程价值（不要丢弃）：**
- 模块接口定义清晰（contracts.py）
- Bus 跨模块通信机制 work
- 测试基础设施完备（195 tests pass）
- Critic、Memory、Permanence、ComposerRouter 的"骨架"代码逻辑正确（只是没有真数据）

**核心缺失：**
1. ❌ 没有真实 backbone（DINOv3）
2. ❌ 没有任何真实 expert（MASt3R 等都是 stub）
3. ❌ 没有真实数据 dataloader（只有合成数据）
4. ❌ 没有真实 evaluation metric

---

## 2. 实施路线图（5 个 Stage）

每个 Stage 一个独立 markdown，详见 `mainwork/STAGE-*.md`。

```
Stage 1 (MVR)        ──→ Stage 2 (Memory)    ──→ Stage 3 (Composer)
单 expert 端到端跑通     训练 Memory 证明价值     多 expert + 路由学习
1-2 周                  1 周                    1 周
                          │
                          ↓
                       Stage 4 (Critic+Repair)  ──→ Stage 5 (Stretch)
                       Critic 触发 repair       更多 expert / Permanence
                       1 周                     可选
```

**关键依赖：**
- Stage 1 是所有后续的前提
- Stage 2-4 顺序可调，但都依赖 Stage 1
- Stage 5 可选

---

## 3. Stage 索引

| Stage | 目标 | 时长 | 文档 |
|---|---|---|---|
| **0** | 当前空壳状态（已完成的脚手架） | done | — |
| **1** | DINOv3 + MASt3R + KITTI 真实端到端 smoke | 1-2 周 | `mainwork/STAGE-1-MVR.md` |
| **2** | 训练 Memory 模块证明长序列价值 | 1 周 | `mainwork/STAGE-2-MEMORY.md` |
| **3** | 加 Fast3R + 训练 Composer Router | 1 周 | `mainwork/STAGE-3-COMPOSER.md` |
| **4** | Critic + Repair 真实信号 | 1 周 | `mainwork/STAGE-4-CRITIC.md` |
| **5** | 可选拓展（CUT3R / Permanence / GS） | 可选 | `mainwork/STAGE-5-STRETCH.md` |

---

## 4. 全局规则

### 4.1 编码规范（强制）

**遵循 Karpathy 4 原则**（见根目录 `CLAUDE.md`）：

1. **Think Before Coding** — 不假设，不藏疑问，浮现 tradeoff
2. **Simplicity First** — 最小代码解决问题，不投机
3. **Surgical Changes** — 只动该动的，每行 diff 都能追到 user 请求
4. **Goal-Driven Execution** — 定义成功标准，循环直到通过

### 4.2 执行规则（强制）

- **本地 Windows = 编辑 + 同步 only**，不跑模型
- **服务器 = 训练 + 推理 + KITTI eval**，via `ssh BUAA-Server`
- **大文件下载流程**：先下到 `E:\Dream3R\downloads\` → 再 `scp` 到 server。**不直接在 server 上 wget/curl 大文件**（避免污染、便于本地审计）
- **代码同步流程**：本地编辑 → `scp` 到 `/hdd3/kykt26/code/dream3r/dream3r/<file>`
- **测试流程**：
  - 本地（schema/shape only）：`cd E:\Dream3R\code\dream3r && python -m pytest tests/ -q`
  - 服务器（完整）：`ssh BUAA-Server "cd /hdd3/kykt26/code/dream3r && conda run -n dream3r python -m pytest dream3r/tests/ -q"`
- **每个 Stage 闭合必须**：
  1. 通过该 Stage 的 success criteria
  2. 写一个 `cycles/CYCLE-YYYYMMDD-NNN.md`
  3. 写一个 `decisions/DEC-YYYYMMDD-NNN-stage-N-closure.md`
  4. 更新 `mainwork.md` 的 Stage 状态
- **不动核心**：除非修 bug，否则不要改 `anchor_bank.py / nsa_attention.py / model.py 主 forward`

### 4.3 数据与 checkpoint 管理

| 类型 | 本地路径 | 服务器路径 |
|---|---|---|
| 代码 | `E:\Dream3R\code\dream3r\` | `/hdd3/kykt26/code/dream3r/dream3r/` |
| 下载暂存 | `E:\Dream3R\downloads\` | （不存在，scp 后删除本地） |
| Checkpoints | （不存放） | `/hdd3/kykt26/checkpoints/` |
| 数据 | （不存放） | `/hdd3/kykt26/data/` |
| Runs/logs | （不存放） | `/hdd3/kykt26/code/dream3r/runs/` |

### 4.4 提问规则

遇到以下情况**必须停下来问用户**，不要自己决定：
- 需要下载 >500MB 的权重或数据
- 需要修改 v0.3 / v0.5 已闭合的核心模块
- 在两个合理设计方案之间犹豫
- 训练超过 4 小时不收敛
- 测试出现新的失败但与当前任务无关

---

## 5. 状态追踪

| Stage | 状态 | 开始 | 完成 | DEC |
|---|---|---|---|---|
| 0 | ✅ done | — | 2026-05-23 | DEC-20260523-001 (A6) |
| 1 | ✅ done | 2026-05-23 | 2026-05-23 | DEC-20260523-004 |
| 2 | ✅ done | 2026-05-23 | 2026-05-23 | DEC-20260523-005 |
| 3 | ✅ done | 2026-05-23 | 2026-05-23 | DEC-20260523-006 |
| 4 | 🔲 pending | — | — | — |
| 5 | 🔲 optional | — | — | — |

---

## 6. 与现有文档的关系

- **不取代** `specs/SPEC-20260522-001-dream3r-v05-axes.md`（A1-A8 axis spec），而是**复用其轴定义**
- **不取代** `cycles/` 和 `decisions/` 目录，而是**统一调度它们**
- 取代 `HANDOFF_PROMPT_NEXT.md`（已过时）

---

## 7. 第一个动作

**下一个 agent 看完本文件后**：
1. 阅读 `CLAUDE.md`
2. 阅读 `mainwork/STAGE-1-MVR.md`
3. 按 STAGE-1 的 todo 逐项执行
4. 卡住就问，不要瞎猜
