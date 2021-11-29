#include <cstddef>

void
addDot1x4(size_t K, float *A, size_t LDA, float *B, size_t LDB, float *C, size_t LDC)
{
	register float Ak = 0., C0 = 0., C1 = 0., C2 = 0., C3 = 0.;
	float *pB0, *pB1, *pB2, *pB3;
	pB0 = B+0; pB1 = B+1; pB2 = B+2; pB3 = B+3;
	for (int k = 0; k < K; k+=4){
		Ak = A[k];
		C0 += Ak * *pB0;
		C1 += Ak * *pB1;
		C2 += Ak * *pB2;
		C3 += Ak * *pB3;

		Ak = A[k+1];
		C0 += Ak * pB0[LDB];
		C1 += Ak * pB1[LDB];
		C2 += Ak * pB2[LDB];
		C3 += Ak * pB3[LDB];

		Ak = A[k+2];
		C0 += Ak * pB0[LDB*2];
		C1 += Ak * pB1[LDB*2];
		C2 += Ak * pB2[LDB*2];
		C3 += Ak * pB3[LDB*2];

		Ak = A[k+3];
		C0 += Ak * pB0[LDB*3];
		C1 += Ak * pB1[LDB*3];
		C2 += Ak * pB2[LDB*3];
		C3 += Ak * pB3[LDB*3];
		pB0 += 4*LDB; pB1 += 4*LDB; pB2 += 4*LDB; pB3 += 4*LDB;
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
