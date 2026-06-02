#!/usr/bin/env bash
set -euo pipefail

export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-1}"

ROOT="${ROOT:-/hdd3/kykt26/code/dream3r}"
OUT="${OUT:-runs/stage6_fusion/image_state_student_sweep}"
KITTI_CACHE="${KITTI_CACHE:-runs/stage6_fusion/image_state_student_kitti_cache.pt}"
ETH3D_CACHE="${ETH3D_CACHE:-runs/stage6_fusion/image_state_student_eth3d_cache.pt}"
STATE_PRIOR_CKPT="${STATE_PRIOR_CKPT:-runs/stage6_fusion/state_prior_sweep/state_seed_7/latest.pt}"
EPOCHS="${EPOCHS:-50}"
LR="${LR:-5e-4}"
PROPOSAL_DROPOUT="${PROPOSAL_DROPOUT:-0.5}"

cd "$ROOT"
mkdir -p "$OUT"

run_one() {
  local name="$1"
  shift
  echo "[$(date '+%F %T')] START $name" | tee -a "$OUT/sweep.log"
  conda run --no-capture-output -n dream3r \
    python -m dream3r.scripts.train_image_state_student \
      --cache "$KITTI_CACHE" "$ETH3D_CACHE" \
      --output-dir "$OUT/$name" \
      --state-prior-checkpoint "$STATE_PRIOR_CKPT" \
      --seed 7 \
      --epochs "$EPOCHS" \
      --lr "$LR" \
      --proposal-dropout "$PROPOSAL_DROPOUT" \
      "$@" \
      2>&1 | tee "$OUT/$name.log"
  echo "[$(date '+%F %T')] OK $name" | tee -a "$OUT/sweep.log"
}

run_one "image_state_student_state_seed_7"
run_one "image_state_student_no_state_seed_7" --no-state
run_one "image_state_student_shuffle_state_seed_7" --shuffle-state

echo "[$(date '+%F %T')] === Image-state student sweep complete ===" | tee -a "$OUT/sweep.log"
