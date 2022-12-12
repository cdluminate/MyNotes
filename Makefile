pytest:
	pytest -v puftm

train:
	python3 -m puftm.train -d mnist -m lenet
