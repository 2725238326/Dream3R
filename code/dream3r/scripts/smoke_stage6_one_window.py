"""One-window smoke: discover d_memory + verify V04PipelineWithFusion runs."""

import torch

from dream3r.data.kitti_long import KITTILongSequenceDataset
from dream3r.model import build_dream3r
from dream3r.orchestrator import build_v04_pipeline
from dream3r.scripts.v04_pipeline_with_fusion import build_v04_pipeline_with_fusion


def main():
    ds = KITTILongSequenceDataset(
        sequence_length=4,
        overlap=2,
        windows_per_sample=1,
        max_sequences=1,
        min_sequence_frames=4,
        max_frames_per_sequence=20,
    )
    print(f"dataset len: {len(ds)}", flush=True)
    sample = ds[0]
    print(f"sequence: {sample['sequence_name']}", flush=True)
    print(f"images shape: {tuple(sample['images'].shape)}", flush=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = build_dream3r("small_real")
    model.eval()

    # Probe a vanilla V04Pipeline to discover d_memory at runtime
    pipeline_probe = build_v04_pipeline(model, max_repair_attempts=1).to(device)
    images = sample["images"][0].unsqueeze(0).to(device)
    with torch.no_grad():
        out = pipeline_probe(images=images, timestep=0)
    print(f"expert.pointmap shape: {tuple(out.expert.pointmap.shape)}", flush=True)
    mc = out.memory.fused_context
    print(
        f"memory.fused_context shape: {tuple(mc.shape) if mc is not None else None}",
        flush=True,
    )
    print(f"critic.conflict_score shape: {tuple(out.critic.conflict_score.shape)}", flush=True)
    d_mem = int(mc.shape[-1]) if mc is not None else 256
    print(f"discovered d_memory: {d_mem}", flush=True)

    pipeline_fuse = build_v04_pipeline_with_fusion(model, d_memory=d_mem).to(device)
    pipeline_fuse.eval()
    with torch.no_grad():
        out_fuse = pipeline_fuse(images=images, timestep=0)
    print(f"V04PipelineWithFusion pointmap shape: {tuple(out_fuse.pointmap.shape)}", flush=True)
    print(
        f"V04PipelineWithFusion expert.pointmap shape: "
        f"{tuple(out_fuse.expert.pointmap.shape)}",
        flush=True,
    )
    diff = (out_fuse.pointmap - out_fuse.expert.pointmap).abs().max().item()
    print(f"max |pipeline.pointmap - expert.pointmap| at init: {diff}", flush=True)
    assert diff < 1e-5, f"head should start identity, got {diff}"
    print("SMOKE PASS", flush=True)


if __name__ == "__main__":
    main()
