#!/bin/bash
set -e
set -x
export NCCL_P2P_DISABLE=1
export CUDA_VISIBLE_DEVICES=0,1
LOGDIR=${0%.sh}
if ! test -d ${LOGDIR}; then
    mkdir -p ${LOGDIR}
    python -m robustness.main --dataset cifar --data ~/.torch/ \
           --out-dir ${LOGDIR} \
           --arch resnet50 \
           --adv-train 1 \
           --constraint inf \
           --eps $(python3 -c "print(8./255.)") \
           --attack-lr $(python3 -c "print(2./255.)") \
           --attack-steps 7 \
           --use-self-neu 0.1 \
           | tee ${LOGDIR}/train.log
fi
LOGDIR_E7=${LOGDIR}/attack-eval-7/
if ! test -d ${LOGDIR_E7}; then
    mkdir -p ${LOGDIR_E7}
    python -m robustness.main --dataset cifar --data ~/.torch/ \
        --out-dir ${LOGDIR_E7} \
        --arch resnet50 \
        --eval-only 1 \
        --adv-eval 1 \
        --constraint inf \
        --eps $(python3 -c "print(8./255.)") \
        --attack-lr $(python3 -c "print(2./255.)") \
        --attack-steps 7 \
        --use-self-neu 0.1 \
        --resume $(find ${LOGDIR} -type f -name '*.pt.best' | head -n1) \
        | tee ${LOGDIR_E7}/eval.log
fi
# 20 steps: 81.9 51.6
#  7 steps: 86.61 52.89 (OK)
# Reference: 87 53

# neu 0.1 (bug): 86.4 52.8
