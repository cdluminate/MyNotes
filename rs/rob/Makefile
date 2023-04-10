clone:
	git clone https://github.com/MadryLab/robustness.git robustness.git --depth=1
	cd robustness.git; git rev-parse HEAD > ../robustness.stamp
	mv robustness.git/* . -v
	rm -rf robustness.git

cifar-r50-nat: clone
	bash cifar10-r50-nat.sh
