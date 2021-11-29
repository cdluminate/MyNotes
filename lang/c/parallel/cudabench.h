/*

 plugin for the benchmarking program: benchmark.c

 */
#ifndef CUDABENCH_H_
#define CUDABENCH_H_

#include <cuda_runtime.h>

// kernel functions

__global__ void _dcopy_cuda (const double * S, double * D, size_t n); // double vector copy
__global__ void _dscal_cuda (double * x, const double a, size_t n);
__global__ void _dasum_cuda (const double * a, size_t n, double * s);

// wrapper functions

void dcopy_cuda (const double * A, double * B, size_t n);
void dscal_cuda (double * x, const double a, size_t n);
double dasum_cuda (const double * a, size_t n);

#endif // CUDABENCH_H_
