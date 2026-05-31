#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${ROOT_DIR:-/hdd3/kykt26/code/dream3r}"
cd "$ROOT_DIR"

export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-1}"

CACHE_ARGS=(
  runs/stage6_fusion/scf_kitti_cache.pt
  runs/stage6_fusion/scf_eth3d_cache.pt
)

SEEDS=("${@:-11 13 17}")

for seed in "${SEEDS[@]}"; do
  echo "=== ver2.1 metric refresh seed=${seed}: correct state ==="
  conda run -n dream3r python -m dream3r.scripts.train_scf_head \
    --cache "${CACHE_ARGS[@]}" \
    --output-dir "runs/stage6_fusion/ver21_metric_refresh/seed_${seed}_state" \
    --seed "$seed" --epochs 300

  echo "=== ver2.1 metric refresh seed=${seed}: no state ==="
  conda run -n dream3r python -m dream3r.scripts.train_scf_head \
    --cache "${CACHE_ARGS[@]}" \
    --output-dir "runs/stage6_fusion/ver21_metric_refresh/seed_${seed}_no_state" \
    --seed "$seed" --epochs 300 --no-state

  echo "=== ver2.1 metric refresh seed=${seed}: shuffled state ==="
  conda run -n dream3r python -m dream3r.scripts.train_scf_head \
    --cache "${CACHE_ARGS[@]}" \
    --output-dir "runs/stage6_fusion/ver21_metric_refresh/seed_${seed}_shuffle_state" \
    --seed "$seed" --epochs 300 --shuffle-state
done
