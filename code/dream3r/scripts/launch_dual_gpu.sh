#!/bin/bash
# Launch dual-GPU workload on Dream3R server.
#   GPU 0: synthetic training (Dream3R v0.5 axes, small preset, 20 epochs)
#   GPU 1: KITTI long-sequence evaluation (mamba_hybrid, 10 windows)
#
# Both tasks write logs with tqdm progress bars.
# After launch, tail both logs simultaneously.

set -e

ROOT=/hdd3/kykt26/code/dream3r
RUNS=$ROOT/runs
mkdir -p $RUNS

# Kill any previously running Dream3R workloads (paranoid cleanup)
pkill -f "dream3r.train" 2>/dev/null || true
pkill -f "dream3r.evaluate_real_sequence" 2>/dev/null || true
sleep 2

TS=$(date +%Y%m%d_%H%M%S)
TRAIN_LOG=$RUNS/train_v05_${TS}.log
EVAL_LOG=$RUNS/eval_kitti_${TS}.log

echo "Activating dream3r env..."
source activate dream3r

cd $ROOT

echo "Launching GPU 0: training (log: $TRAIN_LOG)"
PYTHONUNBUFFERED=1 CUDA_VISIBLE_DEVICES=0 \
  nohup python -m dream3r.train \
    --preset small --epochs 20 --batch_size 4 --gpus 0 \
    > $TRAIN_LOG 2>&1 &
TRAIN_PID=$!
echo "  train PID: $TRAIN_PID"

echo "Launching GPU 1: KITTI eval (log: $EVAL_LOG)"
PYTHONUNBUFFERED=1 CUDA_VISIBLE_DEVICES=1 \
  nohup python -m dream3r.evaluate_real_sequence \
    --data-root /hdd3/kykt26/data \
    --max-sequences 1 --max-windows 10 \
    --recurrence mamba_hybrid \
    --output $RUNS/kitti_10win_${TS}.json \
    > $EVAL_LOG 2>&1 &
EVAL_PID=$!
echo "  eval  PID: $EVAL_PID"

echo ""
echo "=== Logs ==="
echo "  Train: $TRAIN_LOG"
echo "  Eval:  $EVAL_LOG"
echo ""
echo "Tail train:  ssh BUAA-Server 'tail -f $TRAIN_LOG'"
echo "Tail eval:   ssh BUAA-Server 'tail -f $EVAL_LOG'"
echo "Tail both:   ssh BUAA-Server 'tail -f $TRAIN_LOG $EVAL_LOG'"
echo ""
echo "GPU status: ssh BUAA-Server 'nvidia-smi'"
