# Dream3R v1.1 Final Model Non-Claims

Date: 2026-06-10

Dream3R `v1.1.0` does not claim:

- SOTA on KITTI, ETH3D, or any public leaderboard.
- Proposal-free foundation 3R.
- Image-only inference without proposal teachers.
- That VGGT-Omega is a universal Dream3R replacement.
- That Qwen/VLM outputs provide geometry.
- That a native Dream3R decoder can replace proposal teachers yet.
- That Foundation3R is promotable as the delivered model.
- That all dynamic/long-sequence cases are solved.
- That the current real-cache demo is a full benchmark rerun.
- That the current cache/control evidence is enough for a paper-scale final
  evaluation without a separate final-eval pass.

It does claim:

- a runnable and verifiable state-conditioned proposal-fusion 3R package;
- a domain-conditional official policy for KITTI and ETH3D;
- state/no-state/shuffle controls for the official v1.1.0 metrics;
- a stable `v1.0-rc1` fallback and regression gate;
- real proposal-cache runtime evidence.
