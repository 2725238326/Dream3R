#!/bin/bash
# Phase C: 5-seed LOO with geometric reroute (sampson_distance, margin=0.10).
# Compares router-only (predicted_metric) vs router+reroute (reroute_metric)
# on the same fold predictions. The eval script computes both in one pass.

set -u
export CUDA_VISIBLE_DEVICES=1

ROOT=/hdd3/kykt26/code/dream3r
RUNS=$ROOT/runs
LOG_DIR=$RUNS/geometric_reroute_loo_sweep
mkdir -p "$LOG_DIR"
PROGRESS="$LOG_DIR/progress.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$PROGRESS"; }

run_step() {
    local name="$1"; shift
    local logfile="$LOG_DIR/$name.log"
    log "START $name"
    if (cd "$ROOT" && conda run -n dream3r "$@") > "$logfile" 2>&1; then
        log "OK    $name"
    else
        log "FAIL  $name (see $logfile)"
    fi
}

log "=== Phase C geometric reroute 5-seed sweep begin ==="

KITTI_REGIME=$RUNS/stage3_regime_labels/regime_labels.json
KITTI_ORACLE=$RUNS/stage5_s1_expand_oracle/oracle_expert_labels.json
ETH3D_REGIME=$RUNS/eth3d_cross_dataset_regime_labels/regime_labels.json
ETH3D_ORACLE=$RUNS/eth3d_dense_oracle/oracle_expert_labels.json
KITTI_CRITIC=$RUNS/critic_cache/kitti_critic.json
ETH3D_CRITIC=$RUNS/critic_cache/eth3d_critic.json

for SEED in 7 11 13 17 19; do
    run_step "joint_reroute_s${SEED}" \
        python -m dream3r.scripts.eval_router_joint_loo \
            --kitti-regime "$KITTI_REGIME" \
            --kitti-oracle "$KITTI_ORACLE" \
            --eth3d-regime "$ETH3D_REGIME" \
            --eth3d-oracle "$ETH3D_ORACLE" \
            --output $RUNS/geometric_reroute_loo_sweep/joint_v3_dense_sampson_m0.10_s${SEED}/results_loo.json \
            --work-dir $RUNS/geometric_reroute_loo_sweep/joint_v3_dense_sampson_m0.10_s${SEED}/folds \
            --epochs 2000 --lr 0.05 --batch-size 108 --per-domain-norm \
            --seed $SEED \
            --kitti-critic-cache "$KITTI_CRITIC" \
            --eth3d-critic-cache "$ETH3D_CRITIC" \
            --geometric-signal sampson_distance \
            --reroute-margin 0.10
done

log "=== Phase C sweep complete ==="
