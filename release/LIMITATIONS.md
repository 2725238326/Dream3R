# Dream3R v1.1 Final Model Limitations

Date: 2026-06-10

- Dream3R `v1.1.0` is not a SOTA or leaderboard claim; it is the current
  controlled final-stage proposal-fusion model package.
- The model is not proposal-free. It still consumes proposal teachers and
  cached candidate geometry during inference.
- The real-cache v1.1 demo proves cache consumption and branch expert order; it
  is not a full benchmark rerun.
- KITTI remains conservative: the official KITTI branch stays on the
  `v1.0-rc1` bounded StatePrior + residual path.
- ETH3D benefits from the VGGT-Omega-expanded SCF branch, but VGGT-Omega is not
  a universal replacement for Dream3R.
- Qwen semantics remain diagnostic only and are not used as geometry evidence.
- Foundation3R/proposal-free decoding remains research-only after the current
  state-modulation and scratch/student gates failed promotion.
- Native student decoding remains metric-flat relative to the bounded baseline.
- Long-sequence streaming deployment and paper-scale final evaluation remain
  future work unless a later final-eval pass supplies stronger evidence.
- Stable substrate files should remain closed for v1.1 unless a directly
  verified release-line bug requires a small fix.
