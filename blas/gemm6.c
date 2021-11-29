#include <cstddef>

void
addDot1x4(size_t K, float *A, size_t LDA, float *B, size_t LDB, float *C, size_t LDC)
{
	register float Ak = 0., C0 = 0., C1 = 0., C2 = 0., C3 = 0.;
	for (int k = 0; k < K; k++){
		Ak = A[k];
		C0 += Ak * B[k*LDB+0];
		C1 += Ak * B[k*LDB+1];
		C2 += Ak * B[k*LDB+2];
		C3 += Ak * B[k*LDB+3];
	}
	C[0] += C0; C[1] += C1; C[2] += C2; C[3] += C3;
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
