#!/usr/bin/env bash
set -euo pipefail

export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-1}"

ROOT="${ROOT:-/hdd3/kykt26/code/dream3r}"
OUT="${OUT:-runs/stage6_fusion/frozen_prior_decoder_sweep}"
KITTI_CACHE="${KITTI_CACHE:-runs/stage6_fusion/scf_kitti_cache.pt}"
ETH3D_CACHE="${ETH3D_CACHE:-runs/stage6_fusion/scf_eth3d_cache.pt}"
STATE_PRIOR_CKPT="${STATE_PRIOR_CKPT:-runs/stage6_fusion/state_prior_sweep/state_seed_7/latest.pt}"
PRIOR_KL_WEIGHT="${PRIOR_KL_WEIGHT:-0.1}"

cd "$ROOT"
mkdir -p "$OUT"

run_one() {
  local name="$1"
  shift
  echo "[$(date '+%F %T')] START $name" | tee -a "$OUT/sweep.log"
  conda run --no-capture-output -n dream3r \
    python -m dream3r.scripts.train_proposal_set_decoder \
      --cache "$KITTI_CACHE" "$ETH3D_CACHE" \
      --output-dir "$OUT/$name" \
      --seed 7 \
      --epochs 300 \
      --lr 1e-3 \
      --state-prior-checkpoint "$STATE_PRIOR_CKPT" \
      --freeze-state-prior \
      --prior-kl-weight "$PRIOR_KL_WEIGHT" \
      "$@" \
      2>&1 | tee "$OUT/$name.log"
  echo "[$(date '+%F %T')] OK $name" | tee -a "$OUT/sweep.log"
}

run_one "frozen_prior_state_seed_7"
run_one "frozen_prior_shuffle_state_seed_7" --shuffle-state

echo "[$(date '+%F %T')] === Frozen-prior decoder sweep complete ===" | tee -a "$OUT/sweep.log"
