export NCCL_P2P_DISABLE=1
export CUDA_VISIBLE_DEVICES=0,1

poc:
	python3 patpoc.py -m resnet18
	python3 patpoc.py -m resnet50
	python3 patpoc.py -m resnet152

train_cifar:
	python3 train_cifar.py --max_epochs=50

# Quadro RTX 8000 * 2 (48GB)
#  *   Acc@1 75.540 Acc@5 92.688
#  Official reference score: ResNet50_Weights.IMAGENET1K_V1 76.13 92.862 25.6M 4.09
train_imagenet:
	python3 train_imagenet.py \
		-a resnet50 \
		--dist-url 'tcp://127.0.0.1:12345' \
		--dist-backend 'nccl' \
		--multiprocessing-distributed \
		--world-size 1 \
		--rank 0 \
		./ILSVRC

