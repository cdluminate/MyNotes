#!/bin/bash
set -e
set -x
export NCCL_P2P_DISABLE=1
export CUDA_VISIBLE_DEVICES=4,5,6,7
LOGDIR=${0%.sh}
if ! test -d ${LOGDIR}; then
	mkdir -p ${LOGDIR}
	python -m robustness.main --dataset cifar --data ~/.torch/ \
	       --adv-train 0 \
	       --arch resnet50 \
	       --out-dir ${LOGDIR} \
	       | tee ${LOGDIR}/train.log
fi
LOGDIR_E20=${LOGDIR}/attack-eval-20/
if ! test -d ${LOGDIR_E20}; then
	mkdir -p ${LOGDIR_E20}
	python -m robustness.main --dataset cifar --data ~/.torch/ \
		--eval-only 1 \
		--arch resnet50 \
		--adv-eval 1 \
		--constraint inf \
		--out-dir ${LOGDIR_E20} \
		--eps 0.03137254901960784 --attack-lr 2 \
		--attack-steps 20 \
		--resume $(find ${LOGDIR} -type f -name '*.pt.best' | head -n1) \
		| tee ${LOGDIR_E20}/eval.log
fi
