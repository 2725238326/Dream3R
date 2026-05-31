#!/usr/bin/env bash
set -euo pipefail

export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-1}"

ROOT="${ROOT:-/hdd3/kykt26/code/dream3r}"
OUT="${OUT:-runs/stage6_fusion/prior_conditioned_decoder_sweep}"
KITTI_CACHE="${KITTI_CACHE:-runs/stage6_fusion/scf_kitti_cache.pt}"
ETH3D_CACHE="${ETH3D_CACHE:-runs/stage6_fusion/scf_eth3d_cache.pt}"

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
      "$@" \
      2>&1 | tee "$OUT/$name.log"
  echo "[$(date '+%F %T')] OK $name" | tee -a "$OUT/sweep.log"
}

run_one "prior_state_seed_7"
run_one "prior_no_state_seed_7" --no-state
run_one "prior_shuffle_state_seed_7" --shuffle-state

echo "[$(date '+%F %T')] === Prior-conditioned decoder sweep complete ===" | tee -a "$OUT/sweep.log"
