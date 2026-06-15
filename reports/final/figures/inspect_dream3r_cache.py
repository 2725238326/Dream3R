import torch
from pathlib import Path
paths = [
 'runs/v22_admission/vggt_omega_cache_gate/scf_eth3d_vggt_omega_cache.pt',
 'runs/v22_admission/vggt_omega_cache_gate/scf_kitti_vggt_omega_cache.pt',
 'runs/stage6_fusion/scf_eth3d_cache.pt',
 'runs/stage6_fusion/scf_kitti_cache.pt',
 'runs/stage6_fusion/kitti_cache_real.pt',
 'runs/stage6_fusion/eth3d_cache_real.pt',
]
for p in paths:
    pp=Path(p)
    print('\n###', p, 'exists=', pp.exists(), flush=True)
    if not pp.exists():
        continue
    obj=torch.load(pp, map_location='cpu')
    print('type', type(obj), flush=True)
    if isinstance(obj, dict):
        print('keys', list(obj.keys())[:80], flush=True)
        for k,v in obj.items():
            if torch.is_tensor(v):
                print(' ', k, tuple(v.shape), v.dtype, flush=True)
            elif isinstance(v, (list, tuple)):
                print(' ', k, type(v).__name__, 'len', len(v), 'first_type', type(v[0]) if v else None, flush=True)
                if v and isinstance(v[0], dict): print('   first keys', list(v[0].keys())[:50], flush=True)
            else:
                print(' ', k, type(v).__name__, str(v)[:160], flush=True)
    elif isinstance(obj, list):
        print('len', len(obj), 'first', type(obj[0]) if obj else None, flush=True)
        if obj and isinstance(obj[0], dict):
            print('first keys', list(obj[0].keys())[:80], flush=True)
            for k,v in obj[0].items():
                if torch.is_tensor(v): print(' ', k, tuple(v.shape), v.dtype, flush=True)
                else: print(' ', k, type(v).__name__, str(v)[:120], flush=True)
