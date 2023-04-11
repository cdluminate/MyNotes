.PHONY: build
build:
	python3 setup.py build_ext --inplace

clean:
	python3 setup.py clean
	-$(RM) *.so *.c

test:
	PYTHONPATH=. pytest-3 --tb=long -s -v tests
	-$(RM) -rf __pycache__ .cache
