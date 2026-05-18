# Dream3R Demo Summary

Status: formal presentation summary; includes first real-data smoke evidence.

Date: 2026-05-10

## 30-second opening

这项工作的目标不是简单复现某一个三维重建模型，而是围绕长序列场景中的重建稳定性、空间状态保留和错误检查，搭建一个可以继续实验和扩展的原型系统。当前代码已经实现了连续窗口处理、空间记忆、几何自检、多模型接口和真实数据初步运行流程。

## Main claim

当前阶段可以说明的是：Dream3R 已经从方案设计推进到可运行代码，并且开始从合成输入验证过渡到真实数据流程验证。

- 模型可以完成前向和反向计算。
- 支持连续窗口输入和状态传递。
- 空间记忆模块可以写入、召回并记录状态。
- 几何自检模块可以输出冲突分数和修正建议。
- 状态更新路径可以在 `cross_attention` 和 `mamba_hybrid` 之间切换。
- 服务器上已跑通 KITTI rectified RGB/depth 的两窗口真实数据流程。
- smoke test 和完整单元测试已通过。

## Live Command

Run synthetic architecture demo on server:

```bash
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -m dream3r.demo_mamba_path
```

Run real-data smoke on server:

```bash
cd /hdd3/kykt26/code/dream3r
conda run -n dream3r python -m dream3r.evaluate_real_sequence \
  --data-root /hdd3/kykt26/data \
  --max-sequences 1 \
  --max-windows 2 \
  --recurrence mamba_hybrid \
  --output demo_artifacts/real_sequence/kitti_metrics.json
```

## Captured Demo Output

Latest captured output:

```json
{
  "device": "cuda",
  "variants": [
    {
      "recurrence_type": "cross_attention",
      "backend": "StateTokenRecurrence",
      "backend_error": "",
      "elapsed_ms_3_windows": 5357.51,
      "latent_state_tokens": [1, 32, 128],
      "state_delta_mean_abs": 0.586081,
      "stable_promotion_rate": 1.0,
      "nsa_branch_mean": {
        "compressed": 0.046747,
        "selected": 0.889811,
        "sliding": 0.063441
      },
      "conflict_score_mean": 74.862854,
      "recommended_action": [1]
    },
    {
      "recurrence_type": "mamba_hybrid",
      "backend": "mamba_ssm",
      "backend_error": "",
      "elapsed_ms_3_windows": 4370.37,
      "latent_state_tokens": [1, 32, 128],
      "state_delta_mean_abs": 0.311841,
      "stable_promotion_rate": 1.0,
      "nsa_branch_mean": {
        "compressed": 0.10086,
        "selected": 0.884492,
        "sliding": 0.014648
      },
      "conflict_score_mean": 13.274281,
      "recommended_action": [5]
    }
  ]
}
```

## How to explain the output

- `device: cuda`: 运行发生在服务器 GPU 环境中。
- `recurrence_type`: 同一套模型可以切换不同的时序状态更新方式。
- `backend: mamba_ssm`: Mamba 路径使用服务器已有的 `mamba_ssm` 包。
- `latent_state_tokens: [1, 32, 128]`: 连续处理时状态张量形状保持稳定。
- `state_delta_mean_abs`: 状态在窗口之间发生变化，说明时序更新路径被实际调用。
- `stable_promotion_rate`: 空间记忆写入路径被触发。
- `nsa_branch_mean`: 记忆检索的不同分支参与了融合。
- `recommended_action`: 几何自检模块输出了修正动作，不是空接口。

## Important caveats

- Mamba uses `mamba_ssm.Mamba(use_fast_path=False)`. The installed fast CUDA path has a `causal_conv1d` ABI mismatch, so we use the compatible path.
- The Mamba demo inputs are synthetic. This verifies integration behavior, not final reconstruction quality.
- The KITTI run is a real-data smoke path using deterministic RGB/depth patch features and approximate scaled KITTI intrinsics. It verifies that real data can pass through the current processing path; it is not a trained-quality benchmark.
- GaussianHead is a tensor contract for future 3DGS output. It is not a renderer yet.
- Full 3R quality claims need real data evaluation and ablations.

## 8-minute demo flow

1. **问题背景，60s**: 长序列三维重建中容易出现状态遗忘、漂移和错误累积。
2. **方案结构，90s**: 展示感知、空间记忆、几何自检、多模型接口和模块间信息传递。
3. **已完成工作，90s**: 说明代码原型、测试、合成演示和真实数据初步运行。
4. **演示，90s**: 运行 `dream3r.demo_mamba_path`，解释状态更新、记忆写入和自检输出。
5. **验证结果，60s**: 说明服务器 smoke test 和完整单元测试通过。
6. **真实数据流程，60s**: 展示 `REAL_DATA_SMOKE.md` 和 `demo_artifacts/real_sequence/kitti_metrics.json`。
7. **后续计划，60s**: 真实数据消融、自检校准、多模型调度评估和三维可视化接入。

## Verification Snapshot

Last verified on server:

- `scripts/sync_verify_server.ps1 -Mode verify`: local/server package files match.
- `scripts/sync_verify_server.ps1 -Mode test`: smoke pass.
- `scripts/sync_verify_server.ps1 -Mode test -FullTests`: smoke plus all `dream3r.tests.test_*` pass.
- `dream3r.demo_mamba_path`: pass.
- `dream3r.evaluate_real_sequence`: pass on two KITTI windows with `mamba_hybrid` / `mamba_ssm`.

## Real-Data Smoke Snapshot

Latest KITTI smoke:

- sequence: `2011_09_26_drive_0001_sync_02`
- windows: 2, four frames each
- backend: `mamba_ssm`
- pointmap L2: `20.4747`
- depth RMSE: `21.8658`
- memory occupancy: `60.0`
- stable promotion rate: `1.0`
- output: `/hdd3/kykt26/code/dream3r/demo_artifacts/real_sequence/kitti_metrics.json`

Interpretation: this is integration evidence only. Geometry quality is expected to be limited before real-data training, checkpoint integration, and calibration.

## Next Phase

Priority after the current demo:

1. Real-data ablation: `cross_attention` vs `mamba_hybrid`.
2. Real-data ablation: NSA on/off, active/stable on/off, Critic on/off.
3. Critic calibration on real geometric distributions.
4. Expert routing quality report.
5. Renderer-backed 3DGS only after dependency approval.
