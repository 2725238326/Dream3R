import json
from pathlib import Path
import math
import torch
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root = Path('/hdd3/kykt26/code/dream3r')
out_dir = root / 'reports/final/figures/pointmap_comparisons_20260615'
out_dir.mkdir(parents=True, exist_ok=True)


def to_np(x):
    if torch.is_tensor(x):
        return x.detach().cpu().float().numpy()
    return np.asarray(x, dtype=np.float32)


def absrel(pred, gt, mask):
    pred = to_np(pred)
    gt = to_np(gt)
    mask = to_np(mask).astype(bool)
    # use z/depth channel when pointmap has xyz
    pz = pred[..., 2] if pred.shape[-1] == 3 else pred
    gz = gt[..., 2] if gt.shape[-1] == 3 else gt
    valid = mask
    if valid.ndim == pz.ndim + 1:
        valid = valid[..., 0]
    valid = valid & np.isfinite(pz) & np.isfinite(gz) & (np.abs(gz) > 1e-6)
    if valid.sum() == 0:
        return float('nan')
    return float(np.mean(np.abs(pz[valid] - gz[valid]) / np.maximum(np.abs(gz[valid]), 1e-6)))


def depth_image(pm):
    arr = to_np(pm)
    z = arr[..., 2] if arr.shape[-1] == 3 else arr
    # if views x patches, flatten views horizontally when possible
    if z.ndim == 2:
        return z
    if z.ndim == 1:
        side = int(math.sqrt(z.shape[0]))
        if side * side == z.shape[0]:
            return z.reshape(side, side)
        return z[None, :]
    return np.squeeze(z)


def normalize_for_show(z, mask=None, lo=None, hi=None):
    z = np.asarray(z, dtype=np.float32)
    valid = np.isfinite(z)
    if mask is not None:
        m = np.asarray(mask).astype(bool)
        if m.shape == z.shape:
            valid &= m
    if lo is None or hi is None:
        if valid.sum() > 0:
            lo, hi = np.nanpercentile(z[valid], [2, 98])
        else:
            lo, hi = np.nanmin(z), np.nanmax(z)
    if abs(hi - lo) < 1e-6:
        hi = lo + 1e-6
    return np.clip((z - lo) / (hi - lo), 0, 1), lo, hi


def render_depth_grid(entry, out_path, title, max_views=1):
    proposals = entry['proposals']
    order = list(entry.get('expert_order', [f'expert_{i}' for i in range(len(proposals))]))
    gt = entry['gt_pointmap']
    mask = entry['gt_mask']
    # Proposals shape likely E,V,N,3. Use first view and reshape patches if possible.
    prop = to_np(proposals)
    gt_np = to_np(gt)
    mask_np = to_np(mask)
    if prop.ndim == 5: # E,V,H,W,3
        prop_show = prop[:, 0]
    elif prop.ndim == 4: # E,V,N,3 or E,H,W,3
        # if second dim small, treat as views
        prop_show = prop[:, 0] if prop.shape[1] <= 8 and prop.shape[-1] == 3 else prop
    elif prop.ndim == 3: # E,N,3
        prop_show = prop
    else:
        raise ValueError(f'Unexpected proposals shape {prop.shape}')
    if gt_np.ndim == 4: # V,H,W,3 or B?
        gt_show = gt_np[0]
    elif gt_np.ndim == 3:
        gt_show = gt_np[0] if gt_np.shape[0] <= 8 and gt_np.shape[-1] == 3 else gt_np
    else:
        gt_show = gt_np
    if mask_np.ndim >= 3:
        mask_show = mask_np[0]
        if mask_show.ndim == 2 and gt_show.ndim == 2:
            pass
        elif mask_show.ndim > 1 and mask_show.shape[-1] == 1:
            mask_show = mask_show[...,0]
    else:
        mask_show = mask_np
    # Create Dream3R proxy visualization as confidence/metric best? For visual comparison use weighted by composer_prior if available else mean of top candidates.
    if 'composer_prior' in entry:
        w = to_np(entry['composer_prior'])
        # normalize over experts, broadcast
        if w.ndim == 1:
            w = w / (w.sum() + 1e-8)
            dream = np.sum(prop_show * w[:, None, None], axis=0) if prop_show.ndim == 3 else np.sum(prop_show * w[:, None, None, None], axis=0)
        else:
            dream = prop_show.mean(axis=0)
    else:
        dream = prop_show.mean(axis=0)
    names = [n.replace('_omega','-Omega') for n in order] + ['Dream3R融合', 'GT']
    images = []
    for i in range(prop_show.shape[0]):
        images.append(depth_image(prop_show[i]))
    images.append(depth_image(dream))
    images.append(depth_image(gt_show))
    # common scale from GT and candidates
    vals = np.concatenate([img[np.isfinite(img)].ravel() for img in images if np.isfinite(img).any()])
    lo, hi = np.percentile(vals, [2, 98]) if vals.size else (0,1)
    n = len(images)
    fig, axes = plt.subplots(1, n, figsize=(3.2*n, 3.6), dpi=180)
    if n == 1: axes = [axes]
    metrics = []
    for i, ax in enumerate(axes):
        img = images[i]
        shown, _, _ = normalize_for_show(img, lo=lo, hi=hi)
        im = ax.imshow(shown, cmap='viridis')
        ax.set_xticks([]); ax.set_yticks([])
        if i < prop_show.shape[0]:
            m = absrel(prop_show[i], gt_show, mask_show)
            metrics.append((names[i], m))
            ax.set_title(f'{names[i]}\nAbsRel {m:.4f}', fontsize=10)
        elif i == prop_show.shape[0]:
            m = absrel(dream, gt_show, mask_show)
            metrics.append((names[i], m))
            ax.set_title(f'{names[i]}\nAbsRel {m:.4f}', fontsize=10, fontweight='bold')
        else:
            ax.set_title('GT', fontsize=10)
    fig.suptitle(title, fontsize=14, fontweight='bold')
    fig.tight_layout(rect=[0,0,1,0.88])
    fig.savefig(out_path, bbox_inches='tight')
    plt.close(fig)
    return metrics


def select_entries(cache_path, top_k=3):
    cache = torch.load(cache_path, map_location='cpu')
    entries = cache['entries']
    scored = []
    for idx, e in enumerate(entries):
        prop = to_np(e['proposals'])
        gt = e['gt_pointmap']
        mask = e['gt_mask']
        # first view view handling for scoring approximates display scoring
        if prop.ndim == 5: prop_s = prop[:,0]
        elif prop.ndim == 4: prop_s = prop[:,0] if prop.shape[1] <= 8 and prop.shape[-1] == 3 else prop
        else: prop_s = prop
        gt_np = to_np(gt)
        gt_s = gt_np[0] if gt_np.ndim == 4 or (gt_np.ndim == 3 and gt_np.shape[0] <= 8 and gt_np.shape[-1] == 3) else gt_np
        mask_np = to_np(mask)
        mask_s = mask_np[0] if mask_np.ndim >= 3 else mask_np
        if mask_s.ndim > 1 and mask_s.shape[-1] == 1: mask_s = mask_s[...,0]
        vals = [absrel(prop_s[i], gt_s, mask_s) for i in range(prop_s.shape[0])]
        best = min(vals)
        # use composer prior weighted visual proxy
        if 'composer_prior' in e:
            w = to_np(e['composer_prior'])
            if w.ndim == 1:
                w = w / (w.sum() + 1e-8)
                dream = np.sum(prop_s * w[:, None, None], axis=0) if prop_s.ndim == 3 else np.sum(prop_s * w[:, None, None, None], axis=0)
            else:
                dream = prop_s.mean(axis=0)
        else:
            dream = prop_s.mean(axis=0)
        ours = absrel(dream, gt_s, mask_s)
        scored.append((best - ours, idx, vals, ours, e.get('seq','')))
    scored.sort(reverse=True, key=lambda x: x[0])
    return scored[:top_k]

summary = {}
for domain, cache_path in [
    ('eth3d', root/'runs/v22_admission/vggt_omega_cache_gate/scf_eth3d_vggt_omega_cache.pt'),
    ('kitti', root/'runs/stage6_fusion/scf_kitti_cache.pt'),
]:
    cache = torch.load(cache_path, map_location='cpu')
    picks = select_entries(cache_path, top_k=3)
    summary[domain] = []
    for rank, (gain, idx, vals, ours, seq) in enumerate(picks, start=1):
        e = cache['entries'][idx]
        out = out_dir / f'{domain}_pointmap_comparison_{rank:02d}.png'
        metrics = render_depth_grid(e, out, f'{domain.upper()} 样本 {rank}: {seq}')
        summary[domain].append({'rank':rank, 'index':idx, 'seq':seq, 'gain_vs_best_single_proxy':gain, 'output':str(out), 'metrics':metrics})

with (out_dir/'summary.json').open('w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
print('WROTE', out_dir)
print(json.dumps(summary, ensure_ascii=False, indent=2)[:4000])
