main:
	echo HELP

# preprocess MNIST dataset
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
