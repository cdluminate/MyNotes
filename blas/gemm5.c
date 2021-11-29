#include <cstddef>

void
addDot1x4(size_t K, float *A, size_t LDA, float *B, size_t LDB, float *C, size_t LDC)
{
	for (int k = 0; k < K; k++){
		C[0] += A[k] * B[k*LDB+0];
		C[1] += A[k] * B[k*LDB+1];
		C[2] += A[k] * B[k*LDB+2];
		C[3] += A[k] * B[k*LDB+3];
	}
}

void
sgemm(size_t M, size_t N, size_t K, float *A, size_t LDA, float *B, size_t LDB, float *C, size_t LDC)
{
	for (size_t i = 0; i < M; i++) {
		for (size_t j = 0; j < N; j+=4) {
			addDot1x4(K, A+i*LDA, LDA, B+j, LDB, C+i*LDC+j, LDC);
		}
	}
}
