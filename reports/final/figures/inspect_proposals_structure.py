import torch
from pathlib import Path
p=Path('/hdd3/kykt26/code/dream3r/runs/v22_admission/vggt_omega_cache_gate/scf_eth3d_vggt_omega_cache.pt')
obj=torch.load(p,map_location='cpu')
e=obj['entries'][0]
print('entry keys', e.keys())
print('expert_order', e.get('expert_order'))
print('proposals type', type(e['proposals']))
if isinstance(e['proposals'], dict):
    print('proposal keys', e['proposals'].keys())
    for k,v in e['proposals'].items():
        print(' proposal', k, type(v))
        if torch.is_tensor(v): print('  shape', tuple(v.shape), v.dtype)
        elif isinstance(v, dict):
            print('  keys', v.keys())
            for kk,vv in v.items():
                if torch.is_tensor(vv): print('   ', kk, tuple(vv.shape), vv.dtype)
                else: print('   ', kk, type(vv), str(vv)[:80])
        else: print('  val', str(v)[:120])
for k in ['gt_pointmap','gt_mask','memory_context','conflict_score','composer_prior']:
    v=e.get(k)
    print(k, type(v), tuple(v.shape) if torch.is_tensor(v) else str(v)[:200])
