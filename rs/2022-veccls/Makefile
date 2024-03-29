# common variables
G ?= 8  # number of GPUs

usage:
	echo The whole pipeline for reproducing this work is split into
	echo a series of steps. Just read this Makefile and see what each
	echo step does.

mnist-all:
	# full pipeline for reproducing the work
	for i in $$(seq 1 7); do $(MAKE) mnist-$${i}; done
fashion-all:
	for i in $$(seq 1 7); do $(MAKE) mnist-$${i}; done

# preprocess MNIST dataset: mnist-{1,2,3,4,5}
mnist-1:
	# step 1: burst binary MNIST blob into png files
	python3 -m veccls.mnist burst -s train -d mnist-train
	python3 -m veccls.mnist burst -s test  -d mnist-test
fashion-1:
	python3 -m veccls.fashion burst -s train -d fashion-train
	python3 -m veccls.fashion burst -s test  -d fashion-test
cifar10-1:
	python3 -m veccls.cifar10 burst -s train -d cifar10-train
	python3 -m veccls.cifar10 burst -s test  -d cifar10-test

mnist-2:
	# step 2: trace png files into svgs
	bash scripts/prepro-mnist.sh mnist-train/
	bash scripts/prepro-mnist.sh mnist-test/
fashion-2:
	bash scripts/prepro-fashion.sh fashion-train/
	bash scripts/prepro-fashion.sh fashion-test/
cifar10-2:
	bash scripts/prepro-cifar10.sh cifar10-train/
	bash scripts/prepro-cifar10.sh cifar10-test/
	
mnist-3:
	# step 3: parse svgs into sequence data
	python3 -m veccls.batchsvg2json -s mnist-train
	python3 -m veccls.batchsvg2json -s mnist-test
fashion-3:
	python3 -m veccls.batchsvg2json -s fashion-train
	python3 -m veccls.batchsvg2json -s fashion-test
cifar10-3:
	python3 -m veccls.batchsvg2json -s cifar10-train
	python3 -m veccls.batchsvg2json -s cifar10-test

mnist-4:
	# step 4: collect json files and aggregate into one
	python3 -m veccls.mnist collect -d mnist-train
	python3 -m veccls.mnist collect -d mnist-test
fashion-4:
	python3 -m veccls.fashion collect -d fashion-train
	python3 -m veccls.fashion collect -d fashion-test
cifar10-4:
	python3 -m veccls.cifar10 collect -d cifar10-train
	python3 -m veccls.cifar10 collect -d cifar10-test

mnist-5:
	# step 5: now we can remove the temporary files
	-$(RM) -rf mnist-train
	-$(RM) -rf mnist-test
	echo -- We use mnist-train.json and mnist-test.json --
	python3 -m veccls.jsonstat -j mnist-train.json
	python3 -m veccls.jsonstat -j mnist-test.json
fashion-5:
	-$(RM) -rf fashion-train
	-$(RM) -rf fashion-test
	echo -- We use fashin-train.json and fashion-test.json --
	python3 -m veccls.jsonstat -j fashion-train.json
	python3 -m veccls.jsonstat -j fashion-test.json
cifar10-5:
	-$(RM) -rf cifar10-train
	-$(RM) -rf cifar10-test
	echo -- We use cifar10-train.json and cifar10-test.json --
	python3 -m veccls.jsonstat -j cifar10-train.json
	python3 -m veccls.jsonstat -j cifar10-test.json

# dataloader and model training: mnist-{6...
mnist-6:
	# step 6: test dataset class
	python3 -m veccls.mnist_dataset
fashion-6:
	python3 -m veccls.fashion_dataset
cifar10-6:
	python3 -m veccls.cifar10_dataset

mnist-7:
	# step 7: training
	python3 -m veccls.train --dataset=mnist --model_type=gru
	python3 -m veccls.train --dataset=mnist --model_type=hgru
	python3 -m veccls.train --dataset=mnist --model_type=pst
	python3 -m veccls.train --dataset=mnist --model_type=hpst
	python3 -m torch.distributed.launch \
		--nproc_per_node=$(G) --use_env --master_port=23456 \
		scripts/train.py --dataset=mnist
fashion-7:
	python3 -m veccls.train --dataset=fashion --model_type=gru
	python3 -m veccls.train --dataset=fashion --model_type=hgru
	python3 -m veccls.train --dataset=fashion --model_type=pst
	python3 -m veccls.train --dataset=fashion --model_type=hpst
	python3 -m torch.distributed.launch \
		--nproc_per_node=$(G) --use_env --master_port=24567 \
		scripts/train.py --dataset=fashion
cifar10-7:
	python3 -m veccls.train --dataset=cifar10 --model_type=hgru
	python3 -m veccls.train --dataset=cifar10 --model_type=hpst
	python3 -m torch.distributed.launch \
		--nproc_per_node=$(G) --use_env --master_port=25678 \
		scripts/train.py --dataset=cifar10

# [formal training command and parameters]
mnist-dist:
	torchrun \
		--standalone --nnodes=1 --nproc_per_node=$(G) \
		scripts/train.py --dataset=mnist \
		--epochs 16 --lr_drop=12
fashion-dist:
	torchrun \
		--standalone --nnodes=1 --nproc_per_node=$(G) \
		scripts/train.py --dataset=fashion \
		--epochs 16 --lr_drop=12
cifar10-dist:
	torchrun \
		--standalone --nnodes=1 --nproc_per_node=$(G) \
		scripts/train.py --dataset=cifar10 \
		--epochs 50 --lr_drop=25
