CC=gcc
CFLAGS=-fopenmp -g -Wall -std=c11
main:
	@parallel 'printf " CC %s\n" {} ; $(CC) $(CFLAGS) {} -o {.}.elf' ::: *.c
clean:
	-$(RM) *.elf
cuda:
	nvcc -c -g cudabench.cu -o cudabench.o
	$(CXX) -fopenmp -g -std=gnu++11 benchmark.c cudabench.o -o benchmark.elf -lcuda -lcudart
