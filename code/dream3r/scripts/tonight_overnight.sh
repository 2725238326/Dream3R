#!/bin/bash
# Tonight overnight orchestrator (2026-05-26 evening)
#
# Run sequence:
#  A. Build ETH3D dense-GT oracle (rebuilds 50w oracle with rig_scan_eval/*.ply)
#  A.1. ETH3D zero-shot transfer eval with router_kitti_robust_v1 + new oracle
#  A.2. Train router_eth3d_v2_dense + closure + 50-fold LOO
#  A.3. Train router_joint_v3_dense (per-domain norm) + closure + 109-fold LOO
#  C. Multi-seed sweep: 5 seeds x 3 experiments = 15 runs total
#
# Single nohup invocation, every step gates on the previous. progress.log is
# the source of truth for the morning HANDOFF.

set -u

# Pin to an idle GPU so we don't fight other users on GPU 0/2.
# Verified idle at startup: GPU 1 and GPU 3 both 0% / 24GB free.
export CUDA_VISIBLE_DEVICES=1

ROOT=/hdd3/kykt26/code/dream3r
RUNS=$ROOT/runs
CKPT=/hdd3/kykt26/checkpoints
LOG_DIR=$RUNS/overnight_20260526
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

log "=== Overnight pipeline begin ==="

# ===========================================================================
# A. Dense oracle build + ETH3D-side retrain + joint v3 retrain
# ===========================================================================

ETH3D_REGIME=$RUNS/eth3d_cross_dataset_regime_labels/regime_labels.json
KITTI_REGIME=$RUNS/stage3_regime_labels/regime_labels.json
KITTI_ORACLE=$RUNS/stage5_s1_expand_oracle/oracle_expert_labels.json
DENSE_ORACLE=$RUNS/eth3d_dense_oracle/oracle_expert_labels.json

# A.0 Dense oracle build
run_step "A0_dense_oracle_build" \
    python -m dream3r.scripts.build_oracle_expert_labels_eth3d \
        --root /hdd3/kykt26/data \
        --regime-labels "$ETH3D_REGIME" \
        --output "$DENSE_ORACLE" \
        --experts fast3r mast3r spann3r \
        --align-scale --dense-gt \
    || { log "A0 failed; aborting A"; A_OK=0; }
A_OK=${A_OK:-1}

if [ "$A_OK" = "1" ]; then
    # A.1 KITTI-robust router zero-shot on dense ETH3D
    run_step "A1_kitti_robust_eth3d_dense_transfer" \
        python -m dream3r.scripts.eval_cross_domain_router \
            --regime-labels "$ETH3D_REGIME" \
            --oracle-labels "$DENSE_ORACLE" \
            --router-checkpoint $CKPT/router_kitti_robust_v1/latest.pt \
            --kitti-oracle-labels "$KITTI_ORACLE" \
            --output $RUNS/router_kitti_robust_v1_eth3d_dense/results.json \
            --feature-mode regime_stats_robust

    # A.2 ETH3D-only router with dense oracle (retrain because oracle changed)
    run_step "A2a_router_eth3d_v2_dense_train" \
        python -m dream3r.scripts.train_router_only \
            --preset router_only \
            --oracle-labels "$DENSE_ORACLE" \
            --regime-labels "$ETH3D_REGIME" \
            --output-dir $CKPT/router_eth3d_v2_dense \
            --epochs 2000 --lr 0.05 --batch-size 32 \
            --disable-critic-augmentation --feature-mode regime_stats

    run_step "A2b_router_eth3d_v2_dense_ablation" \
        python -m dream3r.scripts.eval_router_ablation \
            --regime-labels "$ETH3D_REGIME" \
            --oracle-labels "$DENSE_ORACLE" \
            --router-checkpoint $CKPT/router_eth3d_v2_dense/latest.pt \
            --output $RUNS/router_eth3d_v2_dense_ablation/results.json \
            --feature-mode regime_stats

    run_step "A2c_router_eth3d_v2_dense_loo" \
        python -m dream3r.scripts.eval_router_loo \
            --regime-labels "$ETH3D_REGIME" \
            --oracle-labels "$DENSE_ORACLE" \
            --output $RUNS/router_eth3d_v2_dense_loo/results_loo.json \
            --work-dir $RUNS/router_eth3d_v2_dense_loo/folds \
            --epochs 2000 --lr 0.05 --batch-size 49 \
            --feature-mode regime_stats

    # A.3 Joint v3 with per-domain norm + dense ETH3D oracle
    run_step "A3a_router_joint_v3_dense_train" \
        python -m dream3r.scripts.train_router_joint_domain \
            --kitti-regime "$KITTI_REGIME" \
            --kitti-oracle "$KITTI_ORACLE" \
            --eth3d-regime "$ETH3D_REGIME" \
            --eth3d-oracle "$DENSE_ORACLE" \
            --output-dir $CKPT/router_joint_v3_dense \
            --epochs 2000 --lr 0.05 --batch-size 32 --per-domain-norm

    run_step "A3b_router_joint_v3_dense_loo" \
        python -m dream3r.scripts.eval_router_joint_loo \
            --kitti-regime "$KITTI_REGIME" \
            --kitti-oracle "$KITTI_ORACLE" \
            --eth3d-regime "$ETH3D_REGIME" \
            --eth3d-oracle "$DENSE_ORACLE" \
            --output $RUNS/router_joint_v3_dense_loo/results_loo.json \
            --work-dir $RUNS/router_joint_v3_dense_loo/folds \
            --epochs 2000 --lr 0.05 --batch-size 108 --per-domain-norm
fi

log "=== A finished, beginning C ==="

# ===========================================================================
# C. Multi-seed sweep on (a) robust KITTI, (b) ETH3D-only (sparse), (c) joint v2
#
# 5 seeds: 7 (already done), 11, 13, 17, 19
# We re-run all 5 for uniformity so the result JSONs share format.
# ===========================================================================

ETH3D_ORACLE_SPARSE=$RUNS/eth3d_cross_dataset_oracle/oracle_expert_labels.json

for SEED in 7 11 13 17 19; do
    log "--- seed=$SEED ---"

    # (a) KITTI-robust, seed
    run_step "C_a_kitti_robust_s${SEED}_train" \
        python -m dream3r.scripts.train_router_only \
            --preset router_only \
            --oracle-labels "$KITTI_ORACLE" \
            --regime-labels "$KITTI_REGIME" \
            --output-dir $CKPT/seed_sweep/kitti_robust_s${SEED} \
            --epochs 2000 --lr 0.05 --batch-size 32 \
            --disable-critic-augmentation --feature-mode regime_stats_robust \
            --seed $SEED

    run_step "C_a_kitti_robust_s${SEED}_loo" \
        python -m dream3r.scripts.eval_router_loo \
            --regime-labels "$KITTI_REGIME" \
            --oracle-labels "$KITTI_ORACLE" \
            --output $RUNS/seed_sweep/kitti_robust_s${SEED}_loo/results_loo.json \
            --work-dir $RUNS/seed_sweep/kitti_robust_s${SEED}_loo/folds \
            --epochs 2000 --lr 0.05 --batch-size 58 --feature-mode regime_stats_robust

    # (b) ETH3D-only sparse, seed
    run_step "C_b_eth3d_only_s${SEED}_train" \
        python -m dream3r.scripts.train_router_only \
            --preset router_only \
            --oracle-labels "$ETH3D_ORACLE_SPARSE" \
            --regime-labels "$ETH3D_REGIME" \
            --output-dir $CKPT/seed_sweep/eth3d_only_s${SEED} \
            --epochs 2000 --lr 0.05 --batch-size 32 \
            --disable-critic-augmentation --feature-mode regime_stats \
            --seed $SEED

    run_step "C_b_eth3d_only_s${SEED}_loo" \
        python -m dream3r.scripts.eval_router_loo \
            --regime-labels "$ETH3D_REGIME" \
            --oracle-labels "$ETH3D_ORACLE_SPARSE" \
            --output $RUNS/seed_sweep/eth3d_only_s${SEED}_loo/results_loo.json \
            --work-dir $RUNS/seed_sweep/eth3d_only_s${SEED}_loo/folds \
            --epochs 2000 --lr 0.05 --batch-size 49 --feature-mode regime_stats

    # (c) Joint v2 per-domain norm, seed
    run_step "C_c_joint_v2_s${SEED}_train" \
        python -m dream3r.scripts.train_router_joint_domain \
            --kitti-regime "$KITTI_REGIME" \
            --kitti-oracle "$KITTI_ORACLE" \
            --eth3d-regime "$ETH3D_REGIME" \
            --eth3d-oracle "$ETH3D_ORACLE_SPARSE" \
            --output-dir $CKPT/seed_sweep/joint_v2_s${SEED} \
            --epochs 2000 --lr 0.05 --batch-size 32 --per-domain-norm \
            --seed $SEED

    run_step "C_c_joint_v2_s${SEED}_loo" \
        python -m dream3r.scripts.eval_router_joint_loo \
            --kitti-regime "$KITTI_REGIME" \
            --kitti-oracle "$KITTI_ORACLE" \
            --eth3d-regime "$ETH3D_REGIME" \
            --eth3d-oracle "$ETH3D_ORACLE_SPARSE" \
            --output $RUNS/seed_sweep/joint_v2_s${SEED}_loo/results_loo.json \
            --work-dir $RUNS/seed_sweep/joint_v2_s${SEED}_loo/folds \
            --epochs 2000 --lr 0.05 --batch-size 108 --per-domain-norm
done

log "=== Overnight pipeline complete ==="
