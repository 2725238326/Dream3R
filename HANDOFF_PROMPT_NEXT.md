# Dream3R 下一步任务交接 — 2026-05-23 13:38

## 当前状态

**已完成（本会话）：**
- ✅ A4 闭合：`vggt_adapter.py` + `capability_card v2.2`（`feed_forward_manyview` regime）+ 8 experts 注册
- ✅ A5 闭合：action 4 (`test3r_offpath_verify`) 已接好，7 测试通过
- ✅ A6 闭合：cycle log + DEC + SOTA matrix 更新
- ✅ A8 闭合：`memory_action.py`（6 子动作 enum + StateUpdatePolicy + TTTStateUpdater scaffold）+ `planning/TTT_PLAN.md`
- ✅ Bus 跨 batch 形状泄漏 bug 修复：`bus.hard_reset()` + `model.forward` 在 `timestep==0` 时调用
- ✅ `n_regimes` 全局从 5 改成 6（config / model.py CONFIGS / synthetic.py / train.py / 所有测试）
- ✅ 本地测试 195 通过，服务器测试 194 通过
- ✅ 已同步：`bus.py model.py modules.py config.py train.py memory_action.py composer_experts/* tests/*`

**正在运行：**
- 🟢 **GPU 0** 训练（PID 3005990）：`train_v05_bus_fix.log`，bs=16, epochs=20, preset=small
  - 启动时间：13:23
  - 预计完成：~23:00（10h）

**未启动 / 已停 / 待办：**
- ⚠️ GPU 1 bank_capacity ablation 似乎已结束（GPU 1: 9 MiB），需检查 `runs/kitti_bank_ablation.json` 是否完整
- ⚠️ 之前的 epoch 5 崩溃训练 `train_v05_bs16.log` 需删除或归档

---

## 待完成任务（按优先级）

### P0. 监控当前训练（GPU 0）

```bash
ssh BUAA-Server "tail -20 /hdd3/kykt26/code/dream3r/runs/train_v05_bus_fix.log"
```

判断：每 epoch ~12min 是正常的；若 loss 不收敛或形状错误再 ping 我。

### P1. A6 bank_capacity ablation 收尾

```bash
ssh BUAA-Server "ls -lh /hdd3/kykt26/code/dream3r/runs/kitti_bank_ablation.json"
# 如果完整（>1KB），用 scripts/analyze_kitti_json.py 出报告
ssh BUAA-Server "cd /hdd3/kykt26/code/dream3r && conda run -n dream3r python dream3r/scripts/analyze_kitti_json.py runs/kitti_bank_ablation.json"
```

把结果写进 `cycles/CYCLE-20260523-001.md` 的"补充证据"段。

### P2. 写 A4 / A8 的 DEC 文档

参考 `decisions/DEC-20260523-001-a6-nsa-sliding-closure.md` 的结构，写：

- `decisions/DEC-20260523-002-a4-vggt-capability-v22.md`
  - 引用 `SPEC-20260522-001 §A4`
  - closes_iff 1-5 全部勾选
  - 列出修改文件：`vggt_adapter.py method_profiles.py base_adapter.py composer_experts/__init__.py config.py model.py modules.py + 8 个测试文件`
  - 195 local / 194 server 测试通过

- `decisions/DEC-20260523-003-a8-memory-a1-action.md`
  - 引用 `SPEC-20260522-001 §A8`
  - closes_iff 1, 2, 4 已满足；3, 5 推迟到 W25 训练
  - 列出修改文件：`memory_action.py + tests/test_memory_action_policy.py + planning/TTT_PLAN.md`
  - 14 个新测试通过

### P3. 更新 `SOTA_FEATURE_MATRIX.md`

在 `code/dream3r/SOTA_FEATURE_MATRIX.md` 加：
- VGGT 行（feed-forward manyview category）
- A8 行：memory action policy = stub→scaffold

参考第 168 行附近 A6 的更新方式。

### P4. 写 cycle log

`cycles/CYCLE-20260523-002.md` 总结今天的全部产出（A4 + A5 验证 + A8 + bus fix）。

### P5（可选，本地可做）. A3 起步

`PermanenceOutput` 新增 `dynamic_mask_final` 字段（与 `dynamic_mask_proxy` 并存），CR-2 优先消费 `final`，回退 `proxy`。
- 文件：`contracts.py orchestrator.py modules.py`
- 不需 server，纯本地 + 测试

---

## 关键约束

- **本地 Windows 不跑模型**，只编辑 + 同步 + 测试 schema-only 的东西
- **所有训练 / KITTI eval 在 server 跑**：`ssh BUAA-Server`，conda env `dream3r`
- **同步用 scp**（不用 sync_verify_server.ps1，慢）：
  ```powershell
  scp E:\Dream3R\code\dream3r\<file> BUAA-Server:/hdd3/kykt26/code/dream3r/dream3r/
  ```
- **测试命令**：
  - 本地：`cd E:\Dream3R\code\dream3r && python -m pytest tests/ -q`
  - 服务器：`ssh BUAA-Server "cd /hdd3/kykt26/code/dream3r && conda run -n dream3r python -m pytest dream3r/tests/ -q"`
- **不要改 v0.3 核心**：`anchor_bank.py / nsa_attention.py / model.py forward 主路径`（除非 bug fix）
- **闭合一个 axis 必须写 DEC**，不能直接合并

---

## 关键文件位置

| 项 | 路径 |
|---|---|
| v0.5 axes spec | `specs/SPEC-20260522-001-dream3r-v05-axes.md` |
| 测试运行入口 | `code/dream3r/tests/` |
| 训练入口 | `code/dream3r/train.py` |
| KITTI eval | `code/dream3r/evaluate_real_sequence.py` |
| 服务器 runs | `/hdd3/kykt26/code/dream3r/runs/` |
| KITTI 数据 | `/hdd3/kykt26/data/kitti/rectified` |
| 本会话产出 cycle log | `cycles/CYCLE-20260523-001.md`（A6） |
| W25 训练计划 | `planning/TTT_PLAN.md` |

---

## 已知 bug / 注意事项

1. **AMP dtype mismatch** 在 `ComposerRouter.forward` 已修（`modules.py:1293-1296`），不要回退
2. **Bus 跨 batch 泄漏** 已修（`bus.py hard_reset` + `model.py timestep==0 分支`），不要回退
3. **n_regimes=6** 现在是默认，老 checkpoint（n_regimes=5）不能直接 resume
4. **VGGT 是 stub**：返回 fallback output；真正的 VGGT checkpoint 加载需要用户授权下载
5. 训练日志路径变化：用 `train_v05_bus_fix.log`，不要看 `train_v05_bs16.log`（已崩溃）

---

## 一句话总结

**v0.5 八个 axis 中 A4/A5/A6/A8 已闭合，A1/A2/A3/A7 阻塞或推迟。下一步是写文档（DEC + cycle log + SOTA 更新）+ 监控当前训练。**
