export NCCL_P2P_DISABLE=1
export CUDA_VISIBLE_DEVICES=0
if ! test -d cifar10-ref; then
	python -m robustness.main --dataset cifar --data ~/.torch/ \
	       --adv-train 0 --arch resnet18 --out-dir cifar10-ref \
	       | tee cifar10-ref/training-log.sh
fi
if ! test -d cifar10-ref/attack-eval/; then
	python -m robustness.main --dataset cifar --eval-only 1 \
		--out-dir cifar10-ref/attack-eval/ \
		--arch resnet18 --adv-eval 1 --constraint inf \
		--eps 0.03137254901960784 --attack-lr 2 \
		--attack-steps 100 \
		--resume cifar10-ref/583440ab-f6bf-41f2-ad2d-4891b7d5106e/checkpoint.pt.best
fi
