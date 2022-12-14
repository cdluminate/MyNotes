num_GPUs=1

default:
	$(MAKE) train
	$(MAKE) eval
	$(MAKE) extract
	$(MAKE) analyze
	$(MAKE) finetune

pytest:
	pytest -v puftm

train:
	python3 -m puftm.train -d mnist -m lenet
	cp -av exps/mnist_lenet exps/mnist_lenet.orig

train-dist:
	torchrun --standalone --nnodes=1 --nproc_per_node=$(num_GPUs) \
		bin/train.py \
		--dataset=mnist --model=lenet

eval:
	python3 -m puftm.eval -d mnist -m lenet

eval-dist:
	torchrun --standalone --nnodes=1 --nproc_per_node=$(num_GPUs) \
		bin/eval.py \
		--dataset=mnist --model=lenet

extract:
	python3 bin/extract.py -d mnist -m lenet

analyze:
	-$(RM) -rf exps/mnist_lenet
	cp -av exps/mnist_lenet.orig exps/mnist_lenet
	python3 bin/analyze.py
	python3 -m puftm.eval -d mnist -m lenet -r exps/mnist_lenet/model_latest.pt
	python3 -m puftm.eval -d mnist -m lenet -r exps/mnist_lenet/model_modified.pt

finetune:
	sed -i -e 's/report_every: int = 50/report_every: int = 1/' puftm/config.py
	python3 -m puftm.train -d mnist -m lenet \
		--lr 1e-4 --epochs 1 \
		-r exps/mnist_lenet/model_modified.pt
