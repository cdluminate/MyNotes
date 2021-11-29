#include <cstddef>

void
addDot(size_t K, float *A, size_t LDA, float *B, size_t LDB, float *c)
{
	for (int k = 0; k < K; k++){
		*c += A[k*LDA] * B[k*LDB];
	}
}

void
sgemm(size_t M, size_t N, size_t K, float *A, size_t LDA, float *B, size_t LDB, float *C, size_t LDC)
{
	for (size_t i = 0; i < M; i++) {
		for (size_t j = 0; j < N; j+=4) {
			addDot(K, A+i*LDA, 1, B+j+0, LDB, C+i*LDC+j+0);
			addDot(K, A+i*LDA, 1, B+j+1, LDB, C+i*LDC+j+1);
			addDot(K, A+i*LDA, 1, B+j+2, LDB, C+i*LDC+j+2);
			addDot(K, A+i*LDA, 1, B+j+3, LDB, C+i*LDC+j+3);
		}
	}
}
