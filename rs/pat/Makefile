# default models:
#  CNN: ResNet50 (torchvision.models.resnet50)
#  Transformer: Swin_T (torchvision.models.swin_t)
export NCCL_P2P_DISABLE=1
export CUDA_VISIBLE_DEVICES=0,1

probmass:
	python3 pat_resnet.py -B
	python3 pat_resnet.py -S
	python3 pat_resnet.py -R

train_cifar:
	python3 train_cifar.py --max_epochs=50

# Quadro RTX 8000 * 2 (48GB)
#  *   Acc@1 75.540 Acc@5 92.688
#  Official reference score: ResNet50_Weights.IMAGENET1K_V1 76.13 92.862 25.6M 4.09
train_imagenet_r50:
	python3 train_imagenet.py \
		-a resnet50 \
		--dist-url 'tcp://127.0.0.1:12345' \
		--dist-backend 'nccl' \
		--multiprocessing-distributed \
		--world-size 1 \
		--rank 0 \
		./ILSVRC

# Acc@1 74.718 Acc@5 92.134
train_imagenet_r50_8gpu:
	CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
		python3 \
		train_imagenet.py \
		-a resnet50 \
		--dist-url 'tcp://127.0.0.1:12345' \
		--dist-backend 'nccl' \
		--multiprocessing-distributed \
		--world-size 1 \
		--rank 0 \
		--batch-size 1024 \
		./ILSVRC

# Quadro RTX 8000 * 2 (48GB)
# *   Acc@1 70.372 Acc@5 89.390
# should use this one: https://github.com/pytorch/vision/blob/main/references/classification/train.py
# Official reference score: Swin_T_Weights.IMAGENET1K_V1 81.474 95.776 28.3M 4.49
train_imagenet_swint:
	python3 train_imagenet.py \
		-a swin_t \
		--dist-url 'tcp://127.0.0.1:12345' \
		--dist-backend 'nccl' \
		--multiprocessing-distributed \
		--world-size 1 \
		--rank 0 \
		./ILSVRC

# *   Acc@1 70.802 Acc@5 89.502
train_imagenet_swint_8gpu:
	CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
		python3 \
		train_imagenet.py \
		-a swin_t \
		--dist-url 'tcp://127.0.0.1:12345' \
		--dist-backend 'nccl' \
		--multiprocessing-distributed \
		--world-size 1 \
		--rank 0 \
		--batch-size 1024 \
		./ILSVRC

# Quadro RTX 8000 * 2 (48GB)
#  *   Acc@1 69.906 Acc@5 89.334
# Official reference score: ResNet18_Weights.IMAGENET1K_V1 69.758 89.078 11.7M 1.81
train_imagenet_r18:
	python3 train_imagenet.py \
		-a resnet18 \
		--dist-url 'tcp://127.0.0.1:12345' \
		--dist-backend 'nccl' \
		--multiprocessing-distributed \
		--world-size 1 \
		--rank 0 \
		./ILSVRC

# Quadro RTX 8000 * 2 (48GB)
# Acc@1 75.396 Acc@5 92.692 r50-x-bn1-flat/
# Acc@1 75.406 Acc@5 92.702 r50-x-bn1-exp/
# Acc@1 75.648 Acc@5 92.744 r50-x-bn1-rflat/
train_pat_row1:
	python3 train_imagenet.py \
		-a resnet50 \
		--dist-url 'tcp://127.0.0.1:12345' \
		--dist-backend 'nccl' \
		--multiprocessing-distributed \
		--world-size 1 \
		--rank 0 \
		--patij=row1 \
		./ILSVRC

eval:
	 python3 eval_imagenet.py --resume baseline-r50/checkpoint.pth.tar
