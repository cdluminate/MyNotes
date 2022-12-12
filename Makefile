num_GPUs=1

pytest:
	pytest -v puftm

train:
	python3 -m puftm.train -d mnist -m lenet

train-dist:
	torchrun --standalone --nnodes=1 --nproc_per_node=$(num_GPUs) \
		bin/train.py \
		--dataset=mnist --model=lenet
