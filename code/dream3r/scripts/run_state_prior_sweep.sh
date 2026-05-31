#!/bin/bash
# Dream3R state-only expert-prior diagnostic sweep.

set -u
export CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-1}

ROOT=${ROOT:-/hdd3/kykt26/code/dream3r}
RUNS=$ROOT/runs
CACHE_DIR=$RUNS/stage6_fusion
SWEEP_DIR=${SWEEP_DIR:-$CACHE_DIR/state_prior_sweep}
mkdir -p "$SWEEP_DIR"
PROGRESS="$SWEEP_DIR/progress.log"

EPOCHS=${EPOCHS:-300}
LR=${LR:-1e-3}
KITTI_CACHE=$CACHE_DIR/scf_kitti_cache.pt
ETH3D_CACHE=$CACHE_DIR/scf_eth3d_cache.pt

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$PROGRESS"; }

run_step() {
    local name="$1"; shift
    local out_dir="$SWEEP_DIR/$name"
    local logfile="$SWEEP_DIR/$name.log"
    if [ -f "$out_dir/results.json" ]; then
        log "SKIP  $name (results exist)"
        return 0
    fi
    log "START $name"
    if (cd "$ROOT" && conda run --no-capture-output -n dream3r "$@") > "$logfile" 2>&1; then
        log "OK    $name"
    else
        log "FAIL  $name (see $logfile)"
    fi
}

log "=== StatePrior sweep begin (epochs=$EPOCHS, lr=$LR, cuda=$CUDA_VISIBLE_DEVICES) ==="

for SEED in 7; do
    run_step "state_seed_${SEED}" \
        python -m dream3r.scripts.train_state_prior_head \
            --cache "$KITTI_CACHE" "$ETH3D_CACHE" \
            --output-dir "$SWEEP_DIR/state_seed_${SEED}" \
            --seed "$SEED" \
            --epochs "$EPOCHS" \
            --lr "$LR"

    run_step "no_state_seed_${SEED}" \
        python -m dream3r.scripts.train_state_prior_head \
            --cache "$KITTI_CACHE" "$ETH3D_CACHE" \
            --output-dir "$SWEEP_DIR/no_state_seed_${SEED}" \
            --seed "$SEED" \
            --epochs "$EPOCHS" \
            --lr "$LR" \
            --no-state

    run_step "shuffle_state_seed_${SEED}" \
        python -m dream3r.scripts.train_state_prior_head \
            --cache "$KITTI_CACHE" "$ETH3D_CACHE" \
            --output-dir "$SWEEP_DIR/shuffle_state_seed_${SEED}" \
            --seed "$SEED" \
            --epochs "$EPOCHS" \
            --lr "$LR" \
            --shuffle-state
done

log "=== StatePrior sweep complete ==="
