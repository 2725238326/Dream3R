#!/bin/bash
# Re-run C (multi-seed sweep) with --seed properly threaded into both train
# AND LOO eval. The original overnight run only varied the train seed; the
# LOO eval hardcoded torch.manual_seed(7), so all 15 results were
# byte-identical. After today's eval_router_loo.py + eval_router_joint_loo.py
# fix (now --seed CLI), this re-run produces real seed-variance numbers.

set -u

export CUDA_VISIBLE_DEVICES=1

ROOT=/hdd3/kykt26/code/dream3r
RUNS=$ROOT/runs
CKPT=/hdd3/kykt26/checkpoints
LOG_DIR=$RUNS/seed_sweep_v2_20260527
mkdir -p "$LOG_DIR"
PROGRESS="$LOG_DIR/progress.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$PROGRESS"
}

run_step() {
    local name="$1"
    shift
    local logfile="$LOG_DIR/$name.log"
    log "START $name"
    if (cd "$ROOT" && conda run -n dream3r "$@") > "$logfile" 2>&1; then
        log "OK    $name"
        return 0
    else
        log "FAIL  $name (see $logfile)"
        return 1
    fi
}

log "=== Seed sweep v2 (seed-fixed LOO) begin ==="

KITTI_REGIME=$RUNS/stage3_regime_labels/regime_labels.json
KITTI_ORACLE=$RUNS/stage5_s1_expand_oracle/oracle_expert_labels.json
ETH3D_REGIME=$RUNS/eth3d_cross_dataset_regime_labels/regime_labels.json
ETH3D_ORACLE_SPARSE=$RUNS/eth3d_cross_dataset_oracle/oracle_expert_labels.json

for SEED in 7 11 13 17 19; do
    log "--- seed=$SEED ---"

    # (a) KITTI-robust LOO with --seed
    run_step "C2_a_kitti_robust_s${SEED}_loo" \
        python -m dream3r.scripts.eval_router_loo \
            --regime-labels "$KITTI_REGIME" \
            --oracle-labels "$KITTI_ORACLE" \
            --output $RUNS/seed_sweep_v2/kitti_robust_s${SEED}_loo/results_loo.json \
            --work-dir $RUNS/seed_sweep_v2/kitti_robust_s${SEED}_loo/folds \
            --epochs 2000 --lr 0.05 --batch-size 58 \
            --feature-mode regime_stats_robust \
            --seed $SEED

    # (b) ETH3D-only sparse LOO with --seed
    run_step "C2_b_eth3d_only_s${SEED}_loo" \
        python -m dream3r.scripts.eval_router_loo \
            --regime-labels "$ETH3D_REGIME" \
            --oracle-labels "$ETH3D_ORACLE_SPARSE" \
            --output $RUNS/seed_sweep_v2/eth3d_only_s${SEED}_loo/results_loo.json \
            --work-dir $RUNS/seed_sweep_v2/eth3d_only_s${SEED}_loo/folds \
            --epochs 2000 --lr 0.05 --batch-size 49 \
            --feature-mode regime_stats \
            --seed $SEED

    # (c) Joint v2 per-domain norm LOO with --seed
    run_step "C2_c_joint_v2_s${SEED}_loo" \
        python -m dream3r.scripts.eval_router_joint_loo \
            --kitti-regime "$KITTI_REGIME" \
            --kitti-oracle "$KITTI_ORACLE" \
            --eth3d-regime "$ETH3D_REGIME" \
            --eth3d-oracle "$ETH3D_ORACLE_SPARSE" \
            --output $RUNS/seed_sweep_v2/joint_v2_s${SEED}_loo/results_loo.json \
            --work-dir $RUNS/seed_sweep_v2/joint_v2_s${SEED}_loo/folds \
            --epochs 2000 --lr 0.05 --batch-size 108 \
            --per-domain-norm \
            --seed $SEED
done

log "=== Seed sweep v2 complete ==="
