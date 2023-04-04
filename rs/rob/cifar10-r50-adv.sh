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
           --attack-steps 20 \
           | tee ${LOGDIR}/train.log
fi
LOGDIR_E20=${LOGDIR}/attack-eval-20/
if ! test -d ${LOGDIR_E20}; then
    mkdir -p ${LOGDIR_E20}
    python -m robustness.main --dataset cifar --data ~/.torch/ \
        --out-dir ${LOGDIR_E20} \
        --arch resnet50 \
        --eval-only 1 \
        --adv-eval 1 \
        --constraint inf \
        --eps $(python3 -c "print(8./255.)") \
        --attack-lr $(python3 -c "print(2./255.)") \
        --attack-steps 20 \
        --resume $(find ${LOGDIR} -type f -name '*.pt.best' | head -n1) \
        | tee ${LOGDIR_E20}/eval.log
fi
