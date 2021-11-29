FLAGS=-I/usr/include/python3.5m -lpython3.5m
main:

	cython3 fib_cy3.pyx #> generates fib_cy3.c
	$(CC) -shared -fPIC fib_cy3.c -o fib_cy3.so $(FLAGS)

	cython3 sin_py3cy3.pyx
	$(CC) -shared -fPIC sin_py3cy3.c -o sin_py3cy3.so $(FLAGS)

	cython3 sin_cy3.pyx
	$(CC) -shared -fPIC sin_cy3.c -o sin_cy3.so $(FLAGS)

	python3 demo.py
	$(MAKE) clean
clean:
	-$(RM) *.c *.so
