CC=gcc
main:
	$(CC) -g -Wall -fopenmp -shared -fPIC kernel.c -o libkernel.so
	$(CC) -g -Wall -shared -fPIC boxmuller.c -o libboxmuller.so
	export LD_LIBRARY_PATH=.; ./main.jl
clean:
	-rm libkernel.so libboxmuller.so
