# STAGE 1 — Minimum Viable Real (MVR)

**Goal:** Get **one real expert + real backbone + real KITTI image pair** to produce a real pointmap with a measurable depth metric. Eliminate "the entire pipeline runs on random tensors" problem.

**Success criteria:**
- 在 1 个 KITTI sequence 的 1 个 image pair 上，端到端跑通：
  ```
  KITTI image → DINOv3-B → Perceiver → (Memory passthrough) → MASt3R adapter (real) → pointmap
  ```
- 计算 depth abs-rel < 0.5 vs KITTI velodyne ground truth
- 全部本地+服务器测试 195+ 通过

**Estimated time:** 1-2 weeks

---

## Tasks

### T1.1 — DINOv3 backbone integration

**Sub-goal:** Make `Perceiver` capable of consuming real images via DINOv3.

**Spec:**
- 下载 `facebook/dinov3-vitb16-pretrain-lvd1689m` 到 `E:\Dream3R\downloads\dinov3-vitb16\`
- scp 到 server: `/hdd3/kykt26/checkpoints/dinov3-vitb16/`
- 修改 `code/dream3r/perceiver.py`（如不存在则在 `model.py` Perceiver 类中）：
  - 加 `backbone_type='dinov3_vitb16'` 分支
  - 用 `torch.hub.load` 或 `transformers.AutoModel.from_pretrained` 加载
  - 默认 `backbone_freeze=True`
  - 输入 `[B, N, 3, H, W]` → 输出 `[B, N, P, D=768]` patch features
- 配置文件 `config.py`：`use_backbone=True, backbone_type='dinov3_vitb16'` 作为新 preset `small_real`

**Verify:**
- 单元测试：`tests/test_dinov3_backbone.py`
  - 加载 backbone，输入 `[1, 4, 3, 224, 224]`，输出 shape `[1, 4, 196, 768]`
  - 参数 frozen 验证：`all(p.requires_grad == False for p in backbone.parameters())`
- Server smoke：`conda run -n dream3r python -c "from dream3r.model import Dream3R; m = Dream3R(CONFIGS['small_real']); print(m.perceiver.backbone)"`

**Forbidden:**
- 不要改 v0.5 已有的 Perceiver 默认行为（保留 `use_backbone=False` 作为默认 fallback）
- 不要把 backbone 权重 commit 到 git（用 `.gitignore` 排除 `downloads/` 和 server checkpoints）

---

### T1.2 — KITTI real-image dataloader

**Sub-goal:** 让训练/评估能直接吃 KITTI 图像，而不是合成 tensor。

**Spec:**
- KITTI rectified 数据已在 `/hdd3/kykt26/data/kitti/rectified/`（无需下载）
- 新建 `code/dream3r/data/kitti_pair.py`：
  - `KITTIPairDataset`: 取 sequence 内连续两帧（间隔 1-3）作为 image pair
  - 加载图像、读取 calib、读取 velodyne 投影 depth
  - 输出: `{"images": [2, 3, H, W], "intrinsics": [2, 3, 3], "depth_gt": [2, H, W], "valid_mask": [2, H, W]}`
- 复用现有 evaluation 数据加载逻辑（看 `evaluate_real_sequence.py`）

**Verify:**
- 单元测试 `tests/test_kitti_pair.py`：
  - 加载 1 个 sequence，迭代 5 个 batch 不报错
  - shape 检查全部对
- Server smoke：`conda run -n dream3r python -c "from dream3r.data.kitti_pair import KITTIPairDataset; ds = KITTIPairDataset('/hdd3/kykt26/data/kitti/rectified'); print(len(ds), ds[0]['images'].shape)"`

**Forbidden:**
- 不要改 `synthetic.py` 的接口（保留合成数据测试路径）

---

### T1.3 — MASt3R real adapter

**Sub-goal:** 把 `MASt3RAdapter` 从 fallback stub 改成真实推理。

**Spec:**
- 下载 MASt3R checkpoint：`naver/MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric` 从 HF
  - 路径：`E:\Dream3R\downloads\mast3r-vitl/`
  - scp 到 `/hdd3/kykt26/checkpoints/mast3r-vitl/`
- `pip install` MASt3R 依赖（在 server conda env：`mast3r` 包或者 `git clone https://github.com/naver/mast3r` 到 `/hdd3/kykt26/code/external/mast3r`，加到 `PYTHONPATH`）
- 改 `composer_experts/mast3r_adapter.py`：
  - 实现 `load_checkpoint(path)`: 真正 load 模型权重
  - 实现 `forward(images, context)`: 调用 MASt3R 真实推理，输出 pointmap + confidence
  - 转换输出为 `ExpertOutput` 格式（17 个 evidence token）
- 保留 fallback 路径：`is_loaded=False` 时返回旧的 fallback

**Verify:**
- 单元测试 `tests/test_mast3r_real.py`（**只在 server 跑，标 `@pytest.mark.gpu`**）：
  - load checkpoint 成功
  - `forward` 输入 `[1, 2, 3, 224, 224]` 真实图像，pointmap 输出非全零
  - confidence map shape 正确
- Server smoke：在 1 个 KITTI image pair 上跑，可视化 pointmap 是否合理

**Forbidden:**
- 不要修改 MASt3R 官方代码（用 import 调用，不要 fork 进来）
- 不要把 1.5GB 权重提交 git

---

### T1.4 — End-to-end smoke on 1 KITTI pair

**Sub-goal:** 把 T1.1 + T1.2 + T1.3 串起来跑通 1 个 image pair。

**Spec:**
- 新建 `code/dream3r/scripts/smoke_real_e2e.py`：
  ```
  1. 加载 1 个 KITTI image pair
  2. 创建 Dream3R(CONFIGS['small_real'])，加载 DINOv3 + MASt3R checkpoints
  3. 跑一次 forward
  4. 取 pointmap, 计算 depth = pointmap[..., 2]
  5. 用 KITTI velodyne ground truth 计算 abs-rel error
  6. 打印 metric + 保存可视化（depth map PNG）
  ```
- Memory / Critic / Composer / Permanence 都用现有 stub 行为，本 stage 不训练它们

**Verify (Stage 1 整体闭合标准):**
- `conda run -n dream3r python -m dream3r.scripts.smoke_real_e2e --kitti_seq 00 --pair 0,1 --output /hdd3/kykt26/code/dream3r/runs/stage1_smoke/`
- 期望：`depth_abs_rel` 打印出来，且 < 0.5（MASt3R 单独在 KITTI 上的预期数字应该在 0.1-0.3）
- 可视化 depth PNG 肉眼合理（有结构，不是噪声）
- 195+ tests 通过（本地 + server）

**Closure artifacts:**
- `cycles/CYCLE-YYYYMMDD-stage1.md` 总结
- `decisions/DEC-YYYYMMDD-NNN-stage1-mvr-closure.md`
- `mainwork.md` 状态表更新 Stage 1 → ✅

---

## Risk Register

| 风险 | 缓解 |
|---|---|
| DINOv3 不在 timm，需要手写加载 | 用 HuggingFace transformers 库，`AutoModel.from_pretrained` |
| MASt3R 依赖与 dream3r conda env 冲突 | 用 `git clone` + `PYTHONPATH` 方式，不 pip install |
| KITTI velodyne depth 投影代码缺失 | 复用现有 `evaluate_real_sequence.py` 的逻辑 |
| 显存不够（DINOv3-B + MASt3R 同时） | 用 ViT-B（不要 ViT-L），batch=1 推理 |
| 1.5GB MASt3R 下载慢 | 在本地用 `hf_hub_download` 后台下载，期间继续 T1.1/T1.2 |

---

## 不做什么（本 stage 明确不做）

- ❌ 训练任何模块
- ❌ 多个 expert 并存
- ❌ Memory 学习长序列
- ❌ Composer router 真实路由
- ❌ Critic 真实判别
- ❌ Permanence 在动态场景
- ❌ GaussianHead

这些都在 Stage 2-5。
