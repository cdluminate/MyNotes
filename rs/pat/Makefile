export NCCL_P2P_DISABLE=1
export CUDA_VISIBLE_DEVICES=0,1

train_cifar:
	python3 train_cifar.py --max_epochs=50

train_imagenet:
	python3 train_imagenet.py \
		-a resnet50 \
		--dist-url 'tcp://127.0.0.1:12345' \
		--dist-backend 'nccl' \
		--multiprocessing-distributed \
		--world-size 1 \
		--rank 0 \
		~/zfs/ILSVRC
