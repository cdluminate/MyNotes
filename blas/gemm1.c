#include <cstddef>

/*
void
sgemm(size_t M, size_t N, size_t K, float *A, size_t LDA, float *B, size_t LDB, float *C, size_t LDC)
{
	// NOTE: column-major
	for (size_t i = 0; i < M; i++) {
		for (size_t j = 0; j < N; j++) {
			for (size_t k = 0; k < K; k++) {
				C[i*LDC+j] = C[i*LDC+j] + A[i*LDA+k] * B[k*LDB+j];
			}
		}
	}
}
*/

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
		for (size_t j = 0; j < N; j++) {
			addDot(K, A+i*LDA, 1, B+j, LDB, C+i*LDC+j);
		}
	}
}
