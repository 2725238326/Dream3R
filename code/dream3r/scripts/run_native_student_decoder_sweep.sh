#!/usr/bin/env bash
set -euo pipefail

export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-1}"

ROOT="${ROOT:-/hdd3/kykt26/code/dream3r}"
OUT="${OUT:-runs/stage6_fusion/native_student_decoder_sweep}"
KITTI_CACHE="${KITTI_CACHE:-runs/stage6_fusion/scf_kitti_cache.pt}"
ETH3D_CACHE="${ETH3D_CACHE:-runs/stage6_fusion/scf_eth3d_cache.pt}"
STATE_PRIOR_CKPT="${STATE_PRIOR_CKPT:-runs/stage6_fusion/state_prior_sweep/state_seed_7/latest.pt}"
EPOCHS="${EPOCHS:-50}"
LR="${LR:-5e-4}"
PROPOSAL_DROPOUT="${PROPOSAL_DROPOUT:-0.35}"
DISTILL_WEIGHT="${DISTILL_WEIGHT:-0.5}"
RESIDUAL_SCALE="${RESIDUAL_SCALE:-0.05}"
DROPOUT_CONSISTENCY_WEIGHT="${DROPOUT_CONSISTENCY_WEIGHT:-0.0}"
TEMPORAL_LOSS_WEIGHT="${TEMPORAL_LOSS_WEIGHT:-0.0}"
SCALE_DRIFT_LOSS_WEIGHT="${SCALE_DRIFT_LOSS_WEIGHT:-0.0}"

cd "$ROOT"
mkdir -p "$OUT"

run_one() {
  local name="$1"
  shift
  echo "[$(date '+%F %T')] START $name" | tee -a "$OUT/sweep.log"
  conda run --no-capture-output -n dream3r \
    python -m dream3r.scripts.train_native_student_decoder \
      --cache "$KITTI_CACHE" "$ETH3D_CACHE" \
      --output-dir "$OUT/$name" \
      --state-prior-checkpoint "$STATE_PRIOR_CKPT" \
      --seed 7 \
      --epochs "$EPOCHS" \
      --lr "$LR" \
      --proposal-dropout "$PROPOSAL_DROPOUT" \
      --distill-weight "$DISTILL_WEIGHT" \
      --residual-scale "$RESIDUAL_SCALE" \
      --dropout-consistency-weight "$DROPOUT_CONSISTENCY_WEIGHT" \
      --temporal-loss-weight "$TEMPORAL_LOSS_WEIGHT" \
      --scale-drift-loss-weight "$SCALE_DRIFT_LOSS_WEIGHT" \
      "$@" \
      2>&1 | tee "$OUT/$name.log"
  echo "[$(date '+%F %T')] OK $name" | tee -a "$OUT/sweep.log"
}

run_one "native_student_state_seed_7"
run_one "native_student_no_state_seed_7" --no-state
run_one "native_student_shuffle_state_seed_7" --shuffle-state

echo "[$(date '+%F %T')] === Native student decoder sweep complete ===" | tee -a "$OUT/sweep.log"
