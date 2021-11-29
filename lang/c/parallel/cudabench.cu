
#include <cuda_runtime.h>
#include <stdio.h>
#include <stdlib.h>
#include "cudabench.h"

#define assertCudaSuccess(ans) { _assertCudaSuccess((ans), __FILE__, __LINE__); }
inline void _assertCudaSuccess(cudaError_t code, char *file, int line)
{
  if (code != cudaSuccess) {
    fprintf(stderr,"CUDA Error: %s %s %d\n", cudaGetErrorString(code), file, line);
    exit(code);
  }
}

// dcopy
__global__ void
_dcopy_cuda (const double * S, double * D, size_t length)
{
  int id = blockDim.x * blockIdx.x + threadIdx.x;
  if (id < length) D[id] = S[id];
}
void
dcopy_cuda (const double * A, double * B, size_t length)
{
  size_t size = sizeof(double) * length;
  // malloc
  double * d_A = NULL, * d_B = NULL;
  cudaMalloc ((void**)&d_A, size);
  cudaMalloc ((void**)&d_B, size);
  // transter H -> D
  cudaMemcpy (d_A, A, size, cudaMemcpyHostToDevice);
  // apply kernel
  int threadsperblock = 256;
  int blockspergrid = (length + threadsperblock - 1)/threadsperblock;
  _dcopy_cuda <<<blockspergrid, threadsperblock>>> (d_A, d_B, length);
  // transter D -> H
  cudaMemcpy (B, d_B, size, cudaMemcpyDeviceToHost);
  // free
  cudaFree (d_A);
  cudaFree (d_B);
}

// dscal
__global__ void
_dscal_cuda (double * x, const double a, size_t n)
{
  int id = blockDim.x * blockIdx.x + threadIdx.x;
  if (id < n) x[id] = x[id] * a;
}
void
dscal_cuda (double * x, const double a, size_t n)
{
  size_t size = sizeof(double) * n;
  // malloc
  double * d_A = NULL;
  cudaMalloc ((void**)&d_A, size);
  // transter H -> D
  cudaMemcpy (d_A, x, size, cudaMemcpyHostToDevice);
  // apply kernel
  int threadsperblock = 256;
  int blockspergrid = (n + threadsperblock - 1)/threadsperblock;
  _dscal_cuda <<<blockspergrid, threadsperblock>>> (d_A, a, n);
  // transter D -> H
  cudaMemcpy (x, d_A, size, cudaMemcpyDeviceToHost);
  // free
  cudaFree (d_A);
}

// dasum
__global__ void
_dasum_cuda (double * a, size_t n, double * o)
{
  int id = blockDim.x * blockIdx.x + threadIdx.x;
  //extern __shared__ double sd[];
  //if (id < n) sd[threadIdx.x] = a[id];
  //__syncthreads();

  for (size_t b=(blockDim.x / 2); b > 0; b >>= 1) {
    if (threadIdx.x < b && id < n) {
      a[id] += a[id+b];
      //sd[threadIdx.x] += sd[threadIdx.x + b];
    }
    __syncthreads();
  }
  if (threadIdx.x == 0) {
    o[blockIdx.x] = a[id];
    //o[blockIdx.x] = sd[0];
  }
}
double
dasum_cuda (const double * a, size_t n)
{
  double sum = 0.;
  size_t size = sizeof(double) * n;
  int threadsperblock = 256;
  int blockspergrid = (n + threadsperblock - 1)/threadsperblock;
  if (blockspergrid == 0) blockspergrid = 1; // fixes bug when vector is short.
  printf ("<<<%ld, %ld>>>\n", blockspergrid, threadsperblock);
  // malloc
  double * d_A = NULL, * d_S = NULL;
  cudaMalloc ((void **)&d_A, size);
  cudaMalloc ((void **)&d_S, blockspergrid*sizeof(double));
  // transter H -> D
  cudaMemcpy (d_A, a, size, cudaMemcpyHostToDevice);
  cudaMemset (d_S, 0, blockspergrid*sizeof(double));
  // apply kernel
  _dasum_cuda <<<blockspergrid, threadsperblock>>> (d_A, n, d_S);
  // transfer D -> H
  double * h_S = NULL;
  h_S = (double *) malloc (blockspergrid*sizeof(double));
  memset ((void *)h_S, 0, blockspergrid*sizeof(double));
  cudaMemcpy (h_S, d_S, blockspergrid*sizeof(double), cudaMemcpyDeviceToHost);
  for (size_t i = 0; i < blockspergrid; i++) {
    printf ("%lf (%ld, %ld)\n", h_S[i], i, blockspergrid);
  }
  for (size_t i = 0; i < blockspergrid; i++) sum += h_S[i];
  free (h_S);
  cudaFree (d_A);
  cudaFree (d_S);
  return sum;
}
