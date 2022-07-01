main:
	echo HELP

mnist:
	# preprocess MNIST dataset
	python3 -m veccls.mnist burst -s train -d mnist-train
	python3 -m veccls.mnist burst -s test  -d mnist-test

