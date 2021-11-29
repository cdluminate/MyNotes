#include <cstddef>

void
addDot(size_t K, float *A, size_t LDA, float *B, size_t LDB, float *c)
{
	for (int k = 0; k < K; k++){
		*c += A[k*LDA] * B[k*LDB];
	}
}

void
addDot1x4(size_t K, float *A, size_t LDA, float *B, size_t LDB, float *C, size_t LDC)
{
	addDot(K, A, 1, B+0, LDB, C+0);
	addDot(K, A, 1, B+1, LDB, C+1);
	addDot(K, A, 1, B+2, LDB, C+2);
	addDot(K, A, 1, B+3, LDB, C+3);
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
