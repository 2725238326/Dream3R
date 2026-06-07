# Dream3R RC Limitations

Date: 2026-06-05

- The release candidate is not SOTA; it is the best bounded, controlled
  Dream3R candidate currently available.
- VGGT-Omega is not the release model path because state-causality controls did
  not pass.
- KITTI remains the limiting domain for VGGT-Omega; VGGT's standalone KITTI
  mean is poor in the 50-window admission gate.
- ETH3D benefits strongly from VGGT-Omega oracle admission, but this has not
  been converted into a robust state-causal model yet.
- Qwen semantics remain diagnostic only and are not used in the RC model.
- Native student decoding remains metric-flat relative to the bounded baseline.
- Frozen core files should remain untouched for this RC.
