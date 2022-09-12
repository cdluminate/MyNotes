/*
 * Emulates nvidia-persistenced.
 *
 * nvcc -O2 -m64 -Xcompiler -fpic -Xcompiler -fpie -gencode arch=compute_70,code=compute_70 fake-nvidia-persistenced.cc -o fnp
 *
 * Reference: https://github.com/NVIDIA/cuda-samples/
 * Samples/0_Introduction/simpleMultiGPU/simpleMultiGPU.cu
 */
#include <stdio.h>
#include <unistd.h>
#include <assert.h>
#include <cuda_runtime.h>

const int MAX_GPU = 16;

int main(int argc, char **argv)
{
	int num_gpu = 0; 
	float *d_data[MAX_GPU];

	printf(">_< Staring fake-nvidia-persistenced\n");
	cudaGetDeviceCount(&num_gpu);
	printf("    found %d CUDA devices.\n", num_gpu);

	for (int i = 0; i < num_gpu; i++) {
		cudaSetDevice(i);
		cudaDeviceSetLimit(cudaLimitStackSize, (size_t)1);
		cudaDeviceSetLimit(cudaLimitMallocHeapSize, (size_t)1);
		cudaMalloc((void **)&d_data[i], 1 * sizeof(float));
		printf("    allocated a stub array on device %d.\n", i);
	}
	printf(">_< Started fake presistence mode. Press ctrl^c to quit.\n");
	while (1) {
		sleep(1);
	}
	for (int i = 0; i < num_gpu; i++)
		cudaFree(d_data[i]);

	return 0;
}
