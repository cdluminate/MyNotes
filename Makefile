main:
	echo HELP

mnist-all:
	# full pipeline for reproducing the work
	$(MAKE) mnist-1
	$(MAKE) mnist-2
	$(MAKE) mnist-3
	$(MAKE) mnist-4
	$(MAKE) mnist-5

# preprocess MNIST dataset: mnist-{1,2,3,4,5}
mnist-1:
	# step 1: burst binary MNIST blob into png files
	python3 -m veccls.mnist burst -s train -d mnist-train
	python3 -m veccls.mnist burst -s test  -d mnist-test

mnist-2:
	# step 2: trace png files into svgs
	bash scripts/prepro-mnist.sh mnist-train/
	bash scripts/prepro-mnist.sh mnist-test/
	
mnist-3:
	# step 3: parse svgs into sequence data
	python3 -m veccls.batchsvg2json -s mnist-train
	python3 -m veccls.batchsvg2json -s mnist-test

mnist-4:
	# step 4: collect json files and aggregate into one
	python3 -m veccls.mnist collect -d mnist-train
	python3 -m veccls.mnist collect -d mnist-test

mnist-5:
	# step 5: now we can remove the temporary files
	-$(RM) -rf mnist-train
	-$(RM) -rf mnist-test
	echo -- We use mnist-train.json and mnist-test.json --

# dataloader and model training: mnist-{6...
mnist-6:
	# step 6: test dataset class
	python3 -m veccls.mnist_dataset
