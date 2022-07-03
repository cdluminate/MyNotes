main:
	echo HELP

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
	
mnist-3:
	# step 3: parse svgs into sequence data
	python3 -m veccls.batchsvg2json -s mnist-train
	python3 -m veccls.batchsvg2json -s mnist-test
fashion-3:
	python3 -m veccls.batchsvg2json -s fashion-train
	python3 -m veccls.batchsvg2json -s fashion-test

mnist-4:
	# step 4: collect json files and aggregate into one
	python3 -m veccls.mnist collect -d mnist-train
	python3 -m veccls.mnist collect -d mnist-test
fashion-4:
	python3 -m veccls.fashion collect -d fashion-train
	python3 -m veccls.fashion collect -d fashion-test

mnist-5:
	# step 5: now we can remove the temporary files
	-$(RM) -rf mnist-train
	-$(RM) -rf mnist-test
	echo -- We use mnist-train.json and mnist-test.json --
fashion-5:
	-$(RM) -rf fashion-train
	-$(RM) -rf fashion-test
	echo -- We use fashin-train.json and fashion-test.json --

# dataloader and model training: mnist-{6...
mnist-6:
	# step 6: test dataset class
	python3 -m veccls.mnist_dataset
fashion-6:
	python3 -m veccls.fashion_dataset

mnist-7:
	# step 7: training
	python3 -m veccls.train_mnist --model_type=gru
	python3 -m veccls.train_mnist --model_type=hgru
	python3 -m veccls.train_mnist --model_type=pst
	python3 -m veccls.train_mnist --model_type=hpst
fashion-7:
	python3 -m veccls.train_fashion --model_type=gru
	python3 -m veccls.train_fashion --model_type=hgru
	python3 -m veccls.train_fashion --model_type=pst
	python3 -m veccls.train_fashion --model_type=hpst
