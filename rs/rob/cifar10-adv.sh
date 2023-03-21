export NCCL_P2P_DISABLE=1
export CUDA_VISIBLE_DEVICES=0
python -m robustness.main --dataset cifar --data ~/.torch/ \
       --adv-train 1 --arch resnet18 --out-dir cifar10-adv \
       --eps 0.03137254901960784 --constraint inf --attack-lr 2.0
