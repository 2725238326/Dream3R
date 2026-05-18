# SOTA Matrix V2: Survey-Driven Re-labeling of v0.2 Comparator Pool

| 字段 | 取值 |
|---|---|
| 文件类型 | planning artifact (非 spec, 非决策) |
| 创建日期 | 2026-05-15 |
| 状态 | v1, draft (planning-only; 不替换 SPEC-20260507-001 v0.2) |
| 上游 | `planning/SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL.md` (§4 P0-2) + `Dream/3R-mix/` 综述四轴判断 |
| 授权根 | DEC-20260515-001 (cycle 035 launch) |
| 触及范围 | 仅本文件; 不动 spec, 不动 code, 不动 NEXT_PHASE_ROADMAP |
| 引用 spec | SPEC-20260507-001 v0.2 (Tier 1-5 + Axis 9-11) — 不修改 |

## 1. Purpose

SPEC-20260507-001 v0.2 把 16 + 3 个 comparator entries 重组为 5 个 tier (in-pool 7 / out-of-pool 3 / out-of-scope 1 / foundation 1 / orthogonal 8), 并在 Axis 1-11 上标注每个 entry 的位置。

2026-05-15 综述识别了四个新的分类轴 (六类失败模式 / 长序列内存四类 / 测试时三类 / 输出资产三类), 加上 proposal §3 提出的输入扩展第五轴。本文件把 SPEC-007 v0.2 的所有 Tier 1-5 entries (加上综述里出现的 Point3R / Mem3R / G-CUT3R / Pow3R / MASt3R-SfM 几个 variant) 在这五个轴上重新标注一次, 暴露"v0.2 池子哪些子类落点厚 / 哪些子类第一类支持空缺", 为后续 v0.4 spec delta 起草 (B1 Critic 路径拆分 / B3 输入扩展 axis) 提供 markdown 评估素材。

**本文件不做的事** (per DEC-20260515-001 §Required Boundary):

- 不修改 SPEC-20260507-001 v0.2 的 Tier 划分或 Axis 1-11
- 不起草 v0.3 / v0.4 comparator spec delta
- 不动 W18 GaussianHead tensor 契约
- 不下结论说"某 comparator 优于另一个"——本文件只描述子类落点, 不做相对优劣判断
- 不修改任何 expert 在 Composer C5 池中的 admission 状态

## 2. Re-labeling 五轴定义

### 轴 A: 几何失败模式 (六类, per 综述 §10)

```text
A1: 弱纹理   (low-texture indoor / textureless wall)
A2: 镜面玻璃 (specular / glass / mirror; reflection-vs-real geometry ambiguity)
A3: 快速运动 (fast motion; large inter-frame displacement; motion blur)
A4: 长基线   (wide baseline; large parallax; matching gap)
A5: 尺度漂移 (scale drift; long-sequence cumulative error)
A6: 域外     (OOD; training distribution is indoor + urban; outdoor / aerial / underwater unseen)
```

### 轴 B: 长序列内存四类 (per 综述 §6)

```text
B1: 空间指针         (spatial pointer; explicit 3D-anchored memory; e.g., Point3R / AnchorBank)
B2: causal-AR        (causal-autoregressive state token; e.g., CUT3R / STream3R)
B3: hybrid memory    (compressed + selected + sliding; e.g., NSA-hybrid)
B4: 预算治理 / 滤波  (budget governance; dynamic pruning; e.g., LONG3R)
```

### 轴 C: 测试时机制三类 (per 综述 §7)

```text
C1: 一致性优化       (test-time consistency optimization; no parameter update; e.g., Test3R)
C2: TTT 参数更新     (test-time training; backprop at inference; e.g., TTT3R)
C3: 先验注入位置区分 (prior-as-input; pose/intrinsics/sparse-depth fed into network; e.g., G-CUT3R / Pow3R / MASt3R-SfM)
```

### 轴 D: 输出资产三类 (per 综述 §8)

```text
D1: 4D pointmap   (per-pixel 3D point sequence; main 3R output)
D2: dynamic mask  (per-pixel dynamic / static labeling)
D3: 4DGS asset    (renderable Gaussian parameters; downstream renderer required)
```

### 轴 E: 输入扩展三类 (proposal §3 bonus axis)

```text
E1: pose / intrinsics 注入 (camera pose / K matrix as first-class input)
E2: sparse depth 先验      (sparse / RGB-D depth hints as first-class input)
E3: video / 4D 直接输入    (video frame rate / temporal prior as first-class input)
```

## 3. Cell 标注规则

每个 cell 取以下五个值之一:

```text
✓     primary      该 comparator 的论文把该子类作为主要贡献; 第一类支持
⚠ partial          该 comparator 部分落点; 通常通过 variant 或推断
⚠ variant          该 comparator 有专门 variant 在该子类落点 (如 G-CUT3R = CUT3R + prior)
—     not first-class 该 comparator 在该子类没有第一类支持
n/a   inapplicable 该子类对该 comparator 不适用 (如 backbone-only entries)
```

每个 cell 末尾的 evidence label (统一在表后给出, 不在 cell 内重复):

- `paper-derived` = 论文显式宣称
- `inferred`      = 综述判断或我从架构推断
- `engineering`   = 我从 v0.2 架构知识判断
- `agent-decided` = 我在本次 re-labeling 中决定的分配

---

## 4. Re-labeled Matrix

### Table A: 失败模式覆盖 (轴 A)

| Comparator | Tier | A1 弱纹理 | A2 镜面玻璃 | A3 快速运动 | A4 长基线 | A5 尺度漂移 | A6 域外 |
|---|---|---|---|---|---|---|---|
| MASt3R | T1 in-pool | ⚠ partial | — | — | ✓ primary | — | ⚠ partial |
| Fast3R | T1 in-pool | — | — | ⚠ partial | ⚠ partial | — | — |
| Spann3R | T1 in-pool | — | — | ⚠ partial | — | ⚠ partial | — |
| CUT3R | T1 in-pool | — | — | ⚠ partial | — | ⚠ partial | ⚠ partial |
| MoGe-2 | T1 in-pool | ⚠ partial | — | — | — | — | ⚠ partial |
| DepthAnything-V2 | T1 in-pool | ⚠ partial | — | — | — | — | ✓ primary |
| Test3R | T1 in-pool | ⚠ partial | ⚠ partial | — | ⚠ partial | ⚠ partial | ⚠ partial |
| VGGT | T2 dropped | ✓ primary | — | — | ✓ primary | ⚠ partial | — |
| MapAnything | T2 dropped | n/a | n/a | n/a | n/a | n/a | n/a |
| Kimi-KDA | T2 dropped | n/a | n/a | n/a | n/a | n/a | n/a |
| ViT-L backbone | T3 oos | n/a | n/a | n/a | n/a | n/a | n/a |
| DUSt3R | T4 foundation | ⚠ partial | — | — | ⚠ partial | — | — |
| STream3R | T5 orthogonal | — | — | ⚠ partial | — | ⚠ partial | — |
| LONG3R / LongStream / LoGeR | T5 orthogonal | — | — | — | — | ✓ primary | — |
| TTT3R | T5 orthogonal | ⚠ partial | ⚠ partial | — | — | ⚠ partial | ✓ primary |
| MonST3R | T5 orthogonal | — | — | ✓ primary | — | — | — |
| POMATO / D²USt3R / Easi3R / RayMap3R | T5 orthogonal | — | — | ⚠ partial | — | — | — |
| Mamba-3R variants | T5 orthogonal | — | — | — | — | ⚠ partial | — |
| SLAM3R | T5 orthogonal | — | — | — | — | ✓ primary | — |
| Splatt3R / InstantSplat / NoPoSplat / 4DGS | T5 orthogonal | ⚠ partial | — | — | — | — | — |

### Table B: 长序列内存四类 (轴 B)

| Comparator | Tier | B1 空间指针 | B2 causal-AR | B3 hybrid | B4 预算治理 |
|---|---|---|---|---|---|
| MASt3R | T1 in-pool | — | — | — | — |
| Fast3R | T1 in-pool | — | — | — | — |
| Spann3R | T1 in-pool | ✓ primary | — | — | — |
| CUT3R | T1 in-pool | — | ✓ primary | — | — |
| MoGe-2 | T1 in-pool | n/a | n/a | n/a | n/a |
| DepthAnything-V2 | T1 in-pool | n/a | n/a | n/a | n/a |
| Test3R | T1 in-pool | — | — | — | — |
| VGGT | T2 dropped | — | — | — | — |
| MapAnything | T2 dropped | n/a | n/a | n/a | n/a |
| Kimi-KDA | T2 dropped | — | — | ⚠ partial | — |
| DUSt3R | T4 foundation | — | — | — | — |
| STream3R | T5 orthogonal | — | ✓ primary | — | — |
| LONG3R | T5 orthogonal | — | — | — | ✓ primary |
| LongStream / LoGeR | T5 orthogonal | — | — | ⚠ partial | ⚠ partial |
| TTT3R | T5 orthogonal | — | — | — | — |
| MonST3R | T5 orthogonal | — | — | — | — |
| POMATO 等 | T5 orthogonal | — | — | — | — |
| Mamba-3R variants | T5 orthogonal | — | ✓ primary | — | — |
| SLAM3R | T5 orthogonal | ⚠ partial | — | ⚠ partial | — |
| Splatt3R / 4DGS variants | T5 orthogonal | — | — | — | — |
| Point3R (综述 §6 引用; 不在 SPEC-007 v0.2 entry list) | (附录) | ✓ primary | — | — | — |
| Mem3R (综述 §6 引用; 不在 SPEC-007 v0.2 entry list) | (附录) | — | — | ⚠ partial | ⚠ partial |

### Table C: 测试时机制三类 (轴 C)

| Comparator | Tier | C1 一致性优化 | C2 TTT 参数更新 | C3 先验注入位置 |
|---|---|---|---|---|
| MASt3R | T1 in-pool | — | — | — |
| MASt3R-SfM (variant; 综述 §7 引用) | (附录) | — | — | ✓ primary |
| Fast3R | T1 in-pool | — | — | — |
| Spann3R | T1 in-pool | — | — | — |
| CUT3R | T1 in-pool | — | — | — |
| G-CUT3R (variant; 综述 §7 引用) | (附录) | — | — | ✓ primary |
| MoGe-2 | T1 in-pool | — | — | — |
| DepthAnything-V2 | T1 in-pool | — | — | — |
| Test3R | T1 in-pool | ✓ primary | — | — |
| Pow3R (综述 §7 引用; 不在 SPEC-007 v0.2 entry list) | (附录) | — | — | ✓ primary |
| TTT3R | T5 orthogonal | — | ✓ primary | — |
| 其余 T5 entries | T5 orthogonal | — | — | — |

### Table D: 输出资产三类 (轴 D)

| Comparator | Tier | D1 4D pointmap | D2 dynamic mask | D3 4DGS asset |
|---|---|---|---|---|
| MASt3R | T1 in-pool | ✓ primary | — | — |
| Fast3R | T1 in-pool | ✓ primary | — | — |
| Spann3R | T1 in-pool | ✓ primary | — | — |
| CUT3R | T1 in-pool | ✓ primary | — | — |
| MoGe-2 | T1 in-pool | ⚠ partial (depth-derived) | — | — |
| DepthAnything-V2 | T1 in-pool | ⚠ partial (depth-derived) | — | — |
| Test3R | T1 in-pool | ✓ primary | — | — |
| VGGT | T2 dropped | ✓ primary | — | — |
| DUSt3R | T4 foundation | ✓ primary | — | — |
| STream3R | T5 orthogonal | ✓ primary | — | — |
| LONG3R 等 | T5 orthogonal | ✓ primary | — | — |
| TTT3R | T5 orthogonal | ✓ primary (refined) | — | — |
| MonST3R | T5 orthogonal | ✓ primary | ✓ primary | — |
| POMATO / D²USt3R / Easi3R / RayMap3R | T5 orthogonal | ✓ primary | ⚠ partial | — |
| Mamba-3R variants | T5 orthogonal | ✓ primary | — | — |
| SLAM3R | T5 orthogonal | ✓ primary | — | — |
| Splatt3R / InstantSplat / NoPoSplat / 4DGS variants | T5 orthogonal | — | — | ✓ primary |

### Table E: 输入扩展三类 (proposal §3 bonus axis)

| Comparator | Tier | E1 pose / intrinsics | E2 sparse depth | E3 video / 4D 时序 |
|---|---|---|---|---|
| MASt3R | T1 in-pool | — | — | — |
| MASt3R-SfM (variant) | (附录) | ✓ primary | — | — |
| Fast3R | T1 in-pool | — | — | ⚠ partial (multi-view) |
| Spann3R | T1 in-pool | — | — | ⚠ partial (streaming) |
| CUT3R | T1 in-pool | — | — | ⚠ partial (streaming) |
| G-CUT3R (variant) | (附录) | ✓ primary | ⚠ partial | — |
| MoGe-2 | T1 in-pool | — | — | — |
| DepthAnything-V2 | T1 in-pool | — | — | — |
| Test3R | T1 in-pool | — | — | — |
| Pow3R | (附录) | ✓ primary | ✓ primary | — |
| VGGT | T2 dropped | — | — | — |
| DUSt3R | T4 foundation | — | — | — |
| STream3R | T5 orthogonal | — | — | ⚠ partial |
| LONG3R 等 | T5 orthogonal | — | — | ✓ primary (long video) |
| TTT3R | T5 orthogonal | — | — | — |
| MonST3R | T5 orthogonal | — | — | ⚠ partial (dynamic video) |
| POMATO 等 | T5 orthogonal | — | — | ⚠ partial |
| Mamba-3R variants | T5 orthogonal | — | — | ⚠ partial |
| SLAM3R | T5 orthogonal | — | — | ⚠ partial |
| Splatt3R / NoPoSplat 等 | T5 orthogonal | (Splatt3R 需要 pose; NoPoSplat 不需要 pose) | — | — |

## 5. Per-row evidence labels

| Comparator | 主 evidence label | 备注 |
|---|---|---|
| MASt3R / Fast3R / Spann3R / CUT3R / MoGe-2 / DAv2 / Test3R | paper-derived | T1 论文都明确宣称对应子类 |
| MASt3R-SfM / G-CUT3R / Pow3R | paper-derived (variant) | variant 论文宣称, 但不是 base entry 在 SPEC-007 v0.2 中的一级 entry |
| VGGT / MapAnything / Kimi-KDA | paper-derived (drop reason) | 落点判断基于已发表论文; tier 判断 user-decided per DEC-20260506-002 |
| DUSt3R | paper-derived (lineage) | foundation; 子类标注按论文 |
| STream3R / LONG3R / TTT3R / MonST3R / Mamba-3R / SLAM3R | paper-derived | 子类落点按论文宣称 |
| POMATO / D²USt3R / Easi3R / RayMap3R | inferred | 子类落点综述判断, 部分通过推断 |
| Splatt3R / InstantSplat / NoPoSplat / 4DGS | paper-derived (asset) | D3 4DGS asset 子类按论文 |
| Point3R / Mem3R | paper-derived | 综述 §6 直接引用 |
| 所有 ⚠ partial 的 cell | engineering / inferred | 我从 v0.2 架构知识或综述判断推断子类部分落点 |

## 6. Aggregated observations

### 6.1 长序列内存维度 (Table B)

T1 in-pool 7 个里只有 2 个在长序列内存 4 个子类落点: Spann3R (B1 空间指针 ✓) + CUT3R (B2 causal-AR ✓)。MoGe-2 / DAv2 是单帧深度 specialist, 长序列内存维度不适用; MASt3R / Fast3R / Test3R 没有长序列内存机制。

T5 orthogonal 撑起余下 3 个子类: STream3R (B2) + LONG3R (B4) + Mamba-3R (B2) + SLAM3R (B1+B3 partial)。综述 §6 引用的 Point3R (B1 ✓) + Mem3R (B3+B4 partial) 不在 SPEC-007 v0.2 entry list, 是 SPEC-007 v0.2 entry list 的潜在补充候选 (但补充本身需要独立 spec delta + DEC, 不在本文件范围)。

Dream3R v0.3 在长序列内存维度的对应关系 (per SPEC-20260508-001 v0.3 C2 + SPEC-20260507-001 Axis 9):

```text
B1 空间指针         <-> C2 AnchorBank K=256 + 3D-aware retrieval (✓ primary)
B2 causal-AR        <-> C2 StateToken + W17 Mamba hybrid          (✓ primary)
B3 hybrid memory    <-> C2 NSA three-branch (compressed/selected/sliding) (✓ primary)
B4 预算治理 / 滤波  <-> C2 frame budget interface layer            (⚠ partial)
```

观察: Dream3R 在 4 个子类上 3 ✓ + 1 ⚠, 是综述四轴中覆盖最厚的一维。B4 的 ⚠ 是因为 LONG3R-style 动态剪枝的对比尚未在 ablate_recurrence 中进行 (这是 LONG_SEQ_REAL_TABLE_PLAN 的执行素材)。

### 6.2 测试时机制维度 (Table C)

只有 4 个 entry 落点在 C1-C3 上: Test3R (C1 ✓) + TTT3R (C2 ✓) + MASt3R-SfM (C3 ✓) + G-CUT3R (C3 ✓) + Pow3R (C3 ✓)。

```text
C1 一致性优化       <-> C4 Critic repair actions 0/1/2 (W7/W9/W15) (⚠ partial)
                       Dream3R 当前 Critic 是 "验证 + 修复" hybrid; 独立的一致性优化循环
                       (Test3R 风格无参数更新) 未拆出
C2 TTT 参数更新     <-> W25 在 NEXT_PHASE_ROADMAP 但 gated         (✗ 空缺)
                       适应循环 / 反向传播路径 / 参数适应位置均未实装
C3 先验注入位置区分 <-> C5 Composer fallback                       (⚠ partial)
                       G-CUT3R / Pow3R / MASt3R-SfM 风格的 prior-as-input 路径未单独对应
```

观察: C1 partial 是 proposal §4 P1-1 (B1 v0.4 spec delta) 的核心动机; C2 完全空缺是 W25 升级到 P1 的依据; C3 partial 是 proposal §4 P1-3 (B3 v0.4 spec delta) 的核心动机。三个测试时子类都需要 v0.4 spec delta 解决, 不能在 markdown 范围内推进。

### 6.3 输出资产维度 (Table D)

D1 4D pointmap 普遍覆盖 (T1 in-pool 7 个里 5 个 ✓, T5 orthogonal 8 个里 7 个 ✓); D2 dynamic mask 由 MonST3R + POMATO 系列承担; D3 4DGS asset 由 Splatt3R / InstantSplat / NoPoSplat / 4DGS variants (T5 orthogonal) 唯一承担, 是综述 §8 强调"输出资产三类不是同一种输出"的关键证据。

```text
D1 4D pointmap    <-> C2-C5 端到端主输出                  (✓ primary)
D2 dynamic mask   <-> C3 Permanence 输出 + W14            (✓ primary)
D3 4DGS asset     <-> W18 GaussianHead tensor 契约        (⚠ partial; renderer gated W27)
```

观察: Dream3R 在 D1 + D2 上 ✓; D3 的 tensor 已存在但 consumer 接口契约未在 spec 明示, 这是 proposal §4 P1-2 (B2 v0.4 spec delta) 的核心动机。

### 6.4 失败模式维度 (Table A)

T1 in-pool 在 6 子类上覆盖最稀疏: 大部分 cell 是 ⚠ partial 或 — (not first-class); 只有 MASt3R (A4 ✓) + DAv2 (A6 ✓) 是 ✓ primary。T5 orthogonal 撑起其他子类: VGGT (A1 + A4 ✓ 但已 dropped) / MonST3R (A3 ✓) / LONG3R + SLAM3R (A5 ✓) / TTT3R (A6 ✓ via test-time adaptation)。

A6 域外 (OOD) 子类只有 DAv2 + TTT3R 两个 ✓ entry。Dream3R v0.3 当前没有 OOD 检测路径 (per SPEC-006 + COMPOSER_CAPABILITY_DESCRIPTORS), 综述指出训练分布偏室内 + 城市, OOD 几何置信度衰减未设计。这是 proposal §4 P0-4 风险登记新增项 + P2-2 OOD 暂缓研究项的依据。

### 6.5 输入扩展维度 (Table E, bonus axis)

E1 pose / intrinsics 的第一类支持只在 variant 一层: MASt3R-SfM / G-CUT3R / Pow3R / Splatt3R; 没有任何 SPEC-007 v0.2 一级 entry 提供。E2 sparse depth 第一类支持只有 Pow3R + G-CUT3R variant; E3 video / 4D 时序的第一类支持主要在 LONG3R 长视频 + MonST3R 动态视频上。

观察: Dream3R v0.3 把图像 + 序列作为唯一输入, 在三个输入扩展子类上都是 ✗ 空缺。这是 proposal §4 P1-3 (B3 v0.4 spec delta) 的核心动机 — Dream3R 想覆盖 G-CUT3R / Pow3R / MASt3R-SfM 这一类工作必须在架构层加 input_priors 张量通道。

## 7. 4 个空缺识别 (per proposal §4 P0-4)

下面 4 项是从五轴 re-labeling 中清晰浮出的 v0.2 comparator pool 第一类支持空缺。每项指向 `planning/WORK_RISK_REGISTER.md` 即将新增的对应风险行 (本 cycle 035 P0-4 任务):

1. **OOD 检测路径空缺 (轴 A6)**: T1 in-pool 只有 DAv2 在 A6 ✓, 但 DAv2 是单帧深度 foundation, 不是 3R 几何 OOD detector。Dream3R 当前 C4 Critic 不区分"训练分布内的 conflict vs 训练分布外的 OOD"。 -> WORK_RISK_REGISTER 新增 R-OOD-1。
2. **外部先验冲突未建模 (轴 C3 + 综述 §7)**: G-CUT3R / Pow3R 把外部先验作为 input, Dream3R 当前 CR-1..CR-6 不处理 prior-vs-geometry 冲突。 -> WORK_RISK_REGISTER 新增 R-EXT-PRIOR-1。
3. **4DGS asset license 链断点 (轴 D3 + 综述 §8)**: Splatt3R / InstantSplat / NoPoSplat 都涉及 Gaussian splatting 渲染 stack; W18 GaussianHead tensor 契约未明示 license 标注。 -> WORK_RISK_REGISTER 新增 R-4DGS-LIC-1。
4. **输入扩展 axis 空缺 (轴 E1+E2+E3)**: Dream3R v0.3 不接受 pose / sparse depth / video timestamp 第一类输入; 与 G-CUT3R / Pow3R / MASt3R-SfM / Splatt3R 这类对照点缺乏可比性。 -> WORK_RISK_REGISTER 新增 R-INPUT-EXT-1。

## 8. 与 v0.2 SPEC 的关系

### 8.1 不修改 SPEC-007 v0.2

本文件不修改 SPEC-20260507-001 v0.2 的:
- 5 个 tier 划分 (in-pool 7 / out-of-pool 3 / out-of-scope 1 / foundation 1 / orthogonal 8)
- Axis 1-11 定义
- 任何 entry 的 paper-known evidence label
- threat ranking (HIGH / MEDIUM / LOW)
- ABL anchoring (ABL-v02-1..9)

### 8.2 不预设 v0.3 / v0.4 spec delta

本文件揭示的 4 个空缺 (§7) 不直接转化为 spec change。任何 spec change 需 per DEC-20260503-001 research-code-discipline + 独立 DEC:

- 把 Point3R 加入 in-pool? -> 需 v0.3 comparator delta + DEC
- 把 G-CUT3R / Pow3R 列为 prior-injection 子类 explicit comparator? -> 同上
- 把 4DGS asset 写入 D3 contract 在 SPEC-006 §C-output? -> proposal §5 B2 v0.4 spec delta + DEC
- 把 input_priors 通道写入 C5 Composer? -> proposal §5 B3 v0.4 spec delta + DEC

本文件只是为 spec delta 起草提供 markdown 评估素材。

### 8.3 与 SOTA 矩阵 v1 (假设存在) 的差异

SPEC-007 v0.2 是按 Composer 池 admission 视角组织 (5 tier 按 in-pool / out-of-pool / orthogonal 等); 本文件 v2 按综述四轴 + 输入扩展轴重新切片同一组 entry, 视角是 capability-coverage 而非 admission-decision。两个视角并存, 不互相替换。

## 9. Limitations & next direction

### 9.1 本文件不能回答

- 哪个 comparator "更好" — 本文件只描述子类落点, 不做相对优劣 (per §1 boundary)
- 子类落点是否就够 - "✓ primary" 只表示论文宣称, 不表示实测胜过其他 entry
- Dream3R 在每个子类上的"质量等级" — 本文件不对 Dream3R 做实测评估; Dream3R 的 4D pointmap 当前只跑过 KITTI 2 窗 (L2=20.47, integration evidence per cycle 034)
- 任何 ablation 跑结果 — F-002 + DEC-20260515-001 §Not authorized 都禁止本 cycle 启动 ablation

### 9.2 下一步 (per proposal §6 + DEC-20260515-001 §Next Direction If Passed)

A. 启动 CRITIC_CALIBRATION_PLAN_V1 执行 -> 独立 DEC, 对应 §7 R-OOD-1 部分缓解
B. 启动 LONG_SEQ_REAL_TABLE_PLAN 执行 -> 独立 DEC, 对应 §6.1 B4 ⚠ -> ✓ 升级
C. 启动 v0.4 spec delta 起草 (B1 / B2 / B3) -> 独立 DEC 三个, 对应 §6.2 + §6.3 + §6.5 三个 ⚠ partial 升级
D. 暂停 + 修订本文件 (如 re-labeling 有错)
E. 回到 architecture-first mainline 非 survey 工作 (W22 visualization pack, W23 expert adapter)

DEC-20260506-001 architecture-first mainline + DEC-20260504-002 no-all-in + DEC-20260501-011 thesis reframe + DEC-20260503-001 research-code-discipline 全部仍在 force, 本文件不动。

## 10. Metadata

| 字段 | 取值 |
|---|---|
| 文件路径 | `Dream/planning/SOTA_MATRIX_V2.md` |
| 创建日期 | 2026-05-15 |
| 状态 | v1, draft (planning artifact, 不替换 SPEC-007 v0.2) |
| 作者 | Dream agent |
| 上游 | SURVEY_DRIVEN_OPTIMIZATION_PROPOSAL §4 P0-2 + 综述四轴判断 |
| 授权根 | DEC-20260515-001 (cycle 035 launch) |
| 引用 spec (不修改) | SPEC-20260506-003 v0.1 / SPEC-20260506-004 v0.2 / SPEC-20260506-005 v0.2 / SPEC-20260507-001 v0.2 / SPEC-20260508-001 v0.3 / SPEC-20260508-002 |
| 引用 paradigm (不修改) | CROSS_SPEC_SIGNAL_CONTRACT v2.1 (CR-1..CR-6) / RESEARCH_CODE_DISCIPLINE / COMPOSER_CAPABILITY_DESCRIPTORS |
| 引用代码状态 (不修改) | RECENT_PROGRESS (W1-W18 + KITTI smoke) / NEXT_PHASE_ROADMAP (W19-W27) |
| 下游候选 | WORK_RISK_REGISTER 4 项 (本 cycle 035 P0-4) / CRITIC_CALIBRATION_PLAN_V1 / LONG_SEQ_REAL_TABLE_PLAN |
| 不下游 | 任何 spec change / ablation 跑 / checkpoint 下载 / 训练 (F-002 不变) |

---

**End of SOTA Matrix V2.** 本文件是 cycle 035 P0-2 deliverable; 后续若需推进 spec delta 或 ablation, 必须独立 DEC + per-step gate。
