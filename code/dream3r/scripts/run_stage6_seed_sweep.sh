#!/bin/bash
# Stage 6 fusion head 5-seed training sweep.
# Builds caches once (if absent), trains head per seed on KITTI+ETH3D joint
# split (80/20 per-domain), and harvests per-seed JSON results.

set -u
export CUDA_VISIBLE_DEVICES=1

ROOT=/hdd3/kykt26/code/dream3r
RUNS=$ROOT/runs
CACHE_DIR=$RUNS/stage6_fusion
SWEEP_DIR=$CACHE_DIR/sweep
mkdir -p "$CACHE_DIR" "$SWEEP_DIR"
PROGRESS="$SWEEP_DIR/progress.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$PROGRESS"; }

run_step() {
    local name="$1"; shift
    local logfile="$SWEEP_DIR/$name.log"
    log "START $name"
    if (cd "$ROOT" && conda run -n dream3r "$@") > "$logfile" 2>&1; then
        log "OK    $name"
    else
        log "FAIL  $name (see $logfile)"
    fi
}

log "=== Stage 6 sweep begin ==="

KITTI_REGIME=$RUNS/stage3_regime_labels/regime_labels.json
ETH3D_REGIME=$RUNS/eth3d_cross_dataset_regime_labels/regime_labels.json
KITTI_CACHE=$CACHE_DIR/kitti_cache.pt
ETH3D_CACHE=$CACHE_DIR/eth3d_cache.pt

# Cache build (idempotent)
if [ ! -f "$KITTI_CACHE" ]; then
    run_step "cache_kitti" \
        python -m dream3r.scripts.train_fusion_head build-cache \
            --dataset kitti_long \
            --regime-labels "$KITTI_REGIME" \
            --output "$KITTI_CACHE"
else
    log "SKIP  cache_kitti (exists)"
fi

if [ ! -f "$ETH3D_CACHE" ]; then
    run_step "cache_eth3d" \
        python -m dream3r.scripts.train_fusion_head build-cache \
            --dataset eth3d_long \
            --regime-labels "$ETH3D_REGIME" \
            --output "$ETH3D_CACHE"
else
    log "SKIP  cache_eth3d (exists)"
fi

# 5-seed training sweep
for SEED in 7 11 13 17 19; do
    run_step "train_s${SEED}" \
        python -m dream3r.scripts.train_fusion_head train \
            --cache "$KITTI_CACHE" "$ETH3D_CACHE" \
            --output-dir "$SWEEP_DIR/seed_${SEED}" \
            --seed $SEED \
            --epochs 300 \
            --lr 1e-3
done

log "=== Stage 6 sweep complete ==="
