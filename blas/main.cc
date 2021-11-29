/*
 * Reference: Xianyi's slide
 * https://www.leiphone.com/news/201704/Puevv3ZWxn0heoEv.html
 * ref: https://github.com/flame/how-to-optimize-gemm/wiki
 * LDA: linear displacement of A
 * INCX: increment of X
 */

#include <cstdlib>
#include <iostream>
#include <cstdio>
#include <sys/time.h>
#include <cblas.h>
#include <cassert>
#include <cstring>
using namespace std;

// timer
static struct timeval _tv;
inline void tic(void) {
	// save current time
	gettimeofday(&_tv, nullptr);
}
inline long toc(void) {
	// get current time
	struct timeval now;
	gettimeofday(&now, nullptr);
	// report time elapsed
	return now.tv_sec*1e6 + now.tv_usec - _tv.tv_sec*1e6 - _tv.tv_usec;
}

// populate data for matrices
void
pop_(size_t m, float *a, bool rand) {
	for (int i = 0; i < m; i++) {
		for (int j = 0; j < m; j++) {
			a[i*m+j] = rand ? drand48() : 0.;
		}
	}
}

// copier
void ikcopy(size_t N, float *x, size_t ldx, float *y, size_t ldy) {
	// x -copy-> y
	if (ldx == 1 && ldy == 1) {
		memcpy(y, x, N*sizeof(float));
	} else {
		for (size_t i = 0; i < N; i++) {
			y[i*ldy] = x[i*ldx];
		}
	}
}

// dumper
void
dump(size_t n, float *a, size_t inc) {
	for (int i = 0; i < n; i+=inc)
		cout << " " << a[i];
	cout << endl;
}

// test helper
void
bench(void (*func)(size_t m, float *a, float *b, float *c)) {
	for (int M = 64; M <= 4096; M*=2) {
		float *A = (float*)aligned_alloc(64, M*M*sizeof(float));
		float *B = (float*)aligned_alloc(64, M*M*sizeof(float));
		float *C = (float*)aligned_alloc(64, M*M*sizeof(float));
		float *D = (float*)aligned_alloc(64, M*M*sizeof(float));
		// prepare data
		pop_(M, A, true);
		pop_(M, B, true);
		pop_(M, C, false);
		pop_(M, D, false);
		// run naive impl
		tic();
		func(M, A, B, C);
		long el = toc();
		if (0 == el) el++;
		float gflops = (2.0 *  M * M * M)/el * 1e-3;
		// run reference impl
		tic();
		cblas_sgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
				M, M, M, 1., A, M, B, M, 0., D, M);
		long refel = toc();
		float refgflops = (2.0 *  M * M * M)/refel * 1e-3;
		// compare
		cblas_saxpy(M*M, -1., C, 1, D, 1);
		//assert(cblas_snrm2(M*M, D, 1) < 1.);
		printf("(%5d) %9ld μs, %6.3f gflops, maxerr %6.3f | ref %8ld μs, %9.3f gflops\n",
				M, el, gflops, D[cblas_isamax(M*M, D, 1)], refel, refgflops);
		fflush(stdout);
		// free
		free(A); free(B); free(C); free(D);
	}
}

// naive impl 1
void
gemm_1(size_t m, float *a, float *b, float *c) {
	for (int i = 0; i < m; i++) {
		for (int j = 0; j < m; j++) {
			for (int k = 0; k < m; k++) {
				c[i*m+j] = c[i*m+j] + a[i*m+k] * b[k*m+j];
			}
		}
	}
}

// impl 2: exchange nesting level and unroll
void
gemm_2(size_t m, float *a, float *b, float *c) {
	for (int j = 0; j < m; j+=4) { // unrolled by 4
		for (int i = 0; i < m; i++) {
			for (int k = 0; k < m; k++) { // AddDot 1x4
				c[i*m+j+0] = c[i*m+j+0] + a[i*m+k] * b[k*m+j+0];
				c[i*m+j+1] = c[i*m+j+1] + a[i*m+k] * b[k*m+j+1];
				c[i*m+j+2] = c[i*m+j+2] + a[i*m+k] * b[k*m+j+2];
				c[i*m+j+3] = c[i*m+j+3] + a[i*m+k] * b[k*m+j+3];
			}
		}
	}
}

// impl 3: using register
void
gemm_3(size_t m, float *a, float *b, float *c) {
	for (int j = 0; j < m; j+=4) { // unrolled by 4
		for (int i = 0; i < m; i++) {
			register float c00, c01, c02, c03;
			register float a0k;
			c00 = 0.; c01 = 0.; c02 = 0.; c03 = 0.;
			for (int k = 0; k < m; k++) { // AddDot 1x4
				a0k = a[i*m+k];
				c00 = c00 + a0k * b[k*m+j+0];
				c01 = c01 + a0k * b[k*m+j+1];
				c02 = c02 + a0k * b[k*m+j+2];
				c03 = c03 + a0k * b[k*m+j+3];
			}
			c[i*m+j+0] = c00;
			c[i*m+j+1] = c01;
			c[i*m+j+2] = c02;
			c[i*m+j+3] = c03;
		}
	}
}

// impl 4: eliminate offset calculation
void
gemm_4(size_t m, float *a, float *b, float *c) {
	for (int j = 0; j < m; j+=4) { // unrolled by 4
		for (int i = 0; i < m; i++) {
			auto bp0 = &b[0*m+j+0];
			auto bp1 = &b[0*m+j+1];
			auto bp2 = &b[0*m+j+2];
			auto bp3 = &b[0*m+j+3];
			register float c00, c01, c02, c03;
			register float a0k;
			c00 = 0.; c01 = 0.; c02 = 0.; c03 = 0.;
			for (int k = 0; k < m; k++) { // AddDot 1x4
				a0k = a[i*m+k];
				c00 = c00 + a0k * *bp0;
				c01 = c01 + a0k * *bp1;
				c02 = c02 + a0k * *bp2;
				c03 = c03 + a0k * *bp3;

				bp0+=m; bp1+=m; bp2+=m; bp3+=m;
			}
			c[i*m+j+0] = c00;
			c[i*m+j+1] = c01;
			c[i*m+j+2] = c02;
			c[i*m+j+3] = c03;
		}
	}
}

// impl 5: unroll another for loop
void
gemm_5(size_t m, float *a, float *b, float *c) {
	for (int j = 0; j < m; j+=4) { // unrolled by 4
		for (int i = 0; i < m; i+=4) { // unrolled by 4
			auto bp0 = &b[0*m+j+0];
			auto bp1 = &b[0*m+j+1];
			auto bp2 = &b[0*m+j+2];
			auto bp3 = &b[0*m+j+3];
			register float c00, c01, c02, c03;
			register float c10, c11, c12, c13;
			register float c20, c21, c22, c23;
			register float c30, c31, c32, c33;
			register float a0k, a1k, a2k, a3k;
			c00 = 0.; c01 = 0.; c02 = 0.; c03 = 0.;
			c10 = 0.; c11 = 0.; c12 = 0.; c13 = 0.;
			c20 = 0.; c21 = 0.; c22 = 0.; c23 = 0.;
			c30 = 0.; c31 = 0.; c32 = 0.; c33 = 0.;
			for (int k = 0; k < m; k++) { // AddDot 4x4
				a0k = a[(i+0)*m+k];
				a1k = a[(i+1)*m+k];
				a2k = a[(i+2)*m+k];
				a3k = a[(i+3)*m+k];

				c00 = c00 + a0k * *bp0;
				c01 = c01 + a0k * *bp1;
				c02 = c02 + a0k * *bp2;
				c03 = c03 + a0k * *bp3;

				c10 = c10 + a1k * *bp0;
				c11 = c11 + a1k * *bp1;
				c12 = c12 + a1k * *bp2;
				c13 = c13 + a1k * *bp3;

				c20 = c20 + a2k * *bp0;
				c21 = c21 + a2k * *bp1;
				c22 = c22 + a2k * *bp2;
				c23 = c23 + a2k * *bp3;

				c30 = c30 + a3k * *bp0;
				c31 = c31 + a3k * *bp1;
				c32 = c32 + a3k * *bp2;
				c33 = c33 + a3k * *bp3;

				bp0+=m; bp1+=m; bp2+=m; bp3+=m;
			}
			c[(i+0)*m+j+0] = c00;
			c[(i+0)*m+j+1] = c01;
			c[(i+0)*m+j+2] = c02;
			c[(i+0)*m+j+3] = c03;

			c[(i+1)*m+j+0] = c10;
			c[(i+1)*m+j+1] = c11;
			c[(i+1)*m+j+2] = c12;
			c[(i+1)*m+j+3] = c13;

			c[(i+2)*m+j+0] = c20;
			c[(i+2)*m+j+1] = c21;
			c[(i+2)*m+j+2] = c22;
			c[(i+2)*m+j+3] = c23;

			c[(i+3)*m+j+0] = c30;
			c[(i+3)*m+j+1] = c31;
			c[(i+3)*m+j+2] = c32;
			c[(i+3)*m+j+3] = c33;
		}
	}
}


// impl 6: X86_64 SIMD (SSE, SSE2)
// ref: https://stackoverflow.com/questions/13257166/print-a-m128i-variable
#include <xmmintrin.h>
void pu8_m128(__m128i x) {
	alignas(16) uint8_t v[16];
	_mm_store_si128((__m128i*)v, x);
	printf("__m128 as u8: %x %x %x %x | %x %x %x %x | %x %x %x %x | %x %x %x %x\n",
	   v[0], v[1],  v[2],  v[3],  v[4],  v[5],  v[6],  v[7],
	   v[8], v[9], v[10], v[11], v[12], v[13], v[14], v[15]);
}

void
gemm_6(size_t m, float *a, float *b, float *c) {
	for (int j = 0; j < m; j+=4) { // unrolled by 4
		for (int i = 0; i < m; i+=4) { // unrolled by 4
			__m128 c0x = _mm_setzero_ps();
			__m128 c1x = _mm_setzero_ps();
			__m128 c2x = _mm_setzero_ps();
			__m128 c3x = _mm_setzero_ps();
			for (int k = 0; k < m; k++) { // AddDot 4x4
				__m128 a0x = _mm_load_ps1(a + (i+0)*m + k);
				__m128 a1x = _mm_load_ps1(a + (i+1)*m + k);
				__m128 a2x = _mm_load_ps1(a + (i+2)*m + k);
				__m128 a3x = _mm_load_ps1(a + (i+3)*m + k);

				__m128 bx = _mm_load_ps(b+k*m+j);

				c0x = _mm_add_ps(c0x, _mm_mul_ps(a0x, bx));
				c1x = _mm_add_ps(c1x, _mm_mul_ps(a1x, bx));
				c2x = _mm_add_ps(c2x, _mm_mul_ps(a2x, bx));
				c3x = _mm_add_ps(c3x, _mm_mul_ps(a3x, bx));
			}
			_mm_store_ps(c+(i+0)*m+j, c0x);
			_mm_store_ps(c+(i+1)*m+j, c1x);
			_mm_store_ps(c+(i+2)*m+j, c2x);
			_mm_store_ps(c+(i+3)*m+j, c3x);
		}
	}
}

// impl7: x86_64 SIMD (AVX, FMA)
#include <immintrin.h>
void
gemm_7(size_t m, float *a, float *b, float *c) {
	for (int j = 0; j < m; j+=8) { // unrolled by 8
		for (int i = 0; i < m; i+=8) { // unrolled by 8
			__m256 c0x = _mm256_setzero_ps();
			__m256 c1x = _mm256_setzero_ps();
			__m256 c2x = _mm256_setzero_ps();
			__m256 c3x = _mm256_setzero_ps();
			__m256 c4x = _mm256_setzero_ps();
			__m256 c5x = _mm256_setzero_ps();
			__m256 c6x = _mm256_setzero_ps();
			__m256 c7x = _mm256_setzero_ps();
			for (int k = 0; k < m; k++) { // AddDot 8x8
				__m256 a0x = _mm256_broadcast_ss(a+(i+0)*m+k);
				__m256 a1x = _mm256_broadcast_ss(a+(i+1)*m+k);
				__m256 a2x = _mm256_broadcast_ss(a+(i+2)*m+k);
				__m256 a3x = _mm256_broadcast_ss(a+(i+3)*m+k);
				__m256 a4x = _mm256_broadcast_ss(a+(i+4)*m+k);
				__m256 a5x = _mm256_broadcast_ss(a+(i+5)*m+k);
				__m256 a6x = _mm256_broadcast_ss(a+(i+6)*m+k);
				__m256 a7x = _mm256_broadcast_ss(a+(i+7)*m+k);

				__m256 bx = _mm256_load_ps(b+k*m+j);

				c0x = _mm256_fmadd_ps(a0x, bx, c0x);
				c1x = _mm256_fmadd_ps(a1x, bx, c1x);
				c2x = _mm256_fmadd_ps(a2x, bx, c2x);
				c3x = _mm256_fmadd_ps(a3x, bx, c3x);
				c4x = _mm256_fmadd_ps(a4x, bx, c4x);
				c5x = _mm256_fmadd_ps(a5x, bx, c5x);
				c6x = _mm256_fmadd_ps(a6x, bx, c6x);
				c7x = _mm256_fmadd_ps(a7x, bx, c7x);
			}
			_mm256_store_ps(c+(i+0)*m+j, c0x);
			_mm256_store_ps(c+(i+1)*m+j, c1x);
			_mm256_store_ps(c+(i+2)*m+j, c2x);
			_mm256_store_ps(c+(i+3)*m+j, c3x);
			_mm256_store_ps(c+(i+4)*m+j, c4x);
			_mm256_store_ps(c+(i+5)*m+j, c5x);
			_mm256_store_ps(c+(i+6)*m+j, c6x);
			_mm256_store_ps(c+(i+7)*m+j, c7x);
		}
	}
}

// impl 8: Blocking. Useful for big matrices.
void
ikgemm8(size_t M, size_t N, size_t K, const float alpha, float *a, size_t lda,
	   	float *b, size_t ldb, const float beta, float *c, size_t ldc) {
	__m256 valpha = _mm256_broadcast_ss(&alpha);
	__m256 vbeta  = _mm256_broadcast_ss(&beta);
	for (int j = 0; j < N; j+=8) { // unrolled by 8
		for (int i = 0; i < M; i+=8) { // unrolled by 8
			__m256 c0x, c1x, c2x, c3x, c4x, c5x, c6x, c7x;
			if (beta == 0.) {
				c0x = _mm256_setzero_ps();
				c1x = _mm256_setzero_ps();
				c2x = _mm256_setzero_ps();
				c3x = _mm256_setzero_ps();
				c4x = _mm256_setzero_ps();
				c5x = _mm256_setzero_ps();
				c6x = _mm256_setzero_ps();
				c7x = _mm256_setzero_ps();
			} else if (beta == 1.) {
				c0x = _mm256_load_ps(c+(i+0)*ldc+j);
				c1x = _mm256_load_ps(c+(i+1)*ldc+j);
				c2x = _mm256_load_ps(c+(i+2)*ldc+j);
				c3x = _mm256_load_ps(c+(i+3)*ldc+j);
				c4x = _mm256_load_ps(c+(i+4)*ldc+j);
				c5x = _mm256_load_ps(c+(i+5)*ldc+j);
				c6x = _mm256_load_ps(c+(i+6)*ldc+j);
				c7x = _mm256_load_ps(c+(i+7)*ldc+j);
			} else {
				c0x = _mm256_mul_ps(_mm256_load_ps(c+(i+0)*ldc+j), vbeta);
				c1x = _mm256_mul_ps(_mm256_load_ps(c+(i+1)*ldc+j), vbeta);
				c2x = _mm256_mul_ps(_mm256_load_ps(c+(i+2)*ldc+j), vbeta);
				c3x = _mm256_mul_ps(_mm256_load_ps(c+(i+3)*ldc+j), vbeta);
				c4x = _mm256_mul_ps(_mm256_load_ps(c+(i+4)*ldc+j), vbeta);
				c5x = _mm256_mul_ps(_mm256_load_ps(c+(i+5)*ldc+j), vbeta);
				c6x = _mm256_mul_ps(_mm256_load_ps(c+(i+6)*ldc+j), vbeta);
				c7x = _mm256_mul_ps(_mm256_load_ps(c+(i+7)*ldc+j), vbeta);
			}
			for (int k = 0; k < K; k++) { // AddDot 8x8
				__m256 a0x = _mm256_broadcast_ss(a+(i+0)*lda+k);
				__m256 a1x = _mm256_broadcast_ss(a+(i+1)*lda+k);
				__m256 a2x = _mm256_broadcast_ss(a+(i+2)*lda+k);
				__m256 a3x = _mm256_broadcast_ss(a+(i+3)*lda+k);
				__m256 a4x = _mm256_broadcast_ss(a+(i+4)*lda+k);
				__m256 a5x = _mm256_broadcast_ss(a+(i+5)*lda+k);
				__m256 a6x = _mm256_broadcast_ss(a+(i+6)*lda+k);
				__m256 a7x = _mm256_broadcast_ss(a+(i+7)*lda+k);

				__m256 bx = _mm256_load_ps(b+k*ldb+j);
				if (alpha != 1.0) bx = _mm256_mul_ps(bx, valpha);

				c0x = _mm256_fmadd_ps(a0x, bx, c0x);
				c1x = _mm256_fmadd_ps(a1x, bx, c1x);
				c2x = _mm256_fmadd_ps(a2x, bx, c2x);
				c3x = _mm256_fmadd_ps(a3x, bx, c3x);
				c4x = _mm256_fmadd_ps(a4x, bx, c4x);
				c5x = _mm256_fmadd_ps(a5x, bx, c5x);
				c6x = _mm256_fmadd_ps(a6x, bx, c6x);
				c7x = _mm256_fmadd_ps(a7x, bx, c7x);
			}
			_mm256_store_ps(c+(i+0)*ldc+j, c0x);
			_mm256_store_ps(c+(i+1)*ldc+j, c1x);
			_mm256_store_ps(c+(i+2)*ldc+j, c2x);
			_mm256_store_ps(c+(i+3)*ldc+j, c3x);
			_mm256_store_ps(c+(i+4)*ldc+j, c4x);
			_mm256_store_ps(c+(i+5)*ldc+j, c5x);
			_mm256_store_ps(c+(i+6)*ldc+j, c6x);
			_mm256_store_ps(c+(i+7)*ldc+j, c7x);
		}
	}
}
void
gemm_8(size_t m, float *a, float *b, float *c) {
	// mc * m blocks of C by a call to the InnerKernel
	size_t kc = 64; // tuned according to L2 cache
	size_t mc = 64; // tuned according to L2 cache
	for (int p = 0; p < m; p += kc) { // M, N, Block(K)
		for (int q = 0; q < m; q += mc) { // Block(M), N, Block(K)
			// ikgemm8(subM, N, subK, alpha, subA, lda, subB, ldb, beta, subC, ldc);
			ikgemm8(mc, m, kc, 1., &a[q*m+p], m, &b[p*m+0], m, 1., &c[q*m+0], m);
		}
	}
}


// impl 9: Packing A: Better caching efficiency
void
ikgemm9(size_t M, size_t N, size_t K, const float alpha, float *a, size_t lda,
	   	float *b, size_t ldb, const float beta, float *c, size_t ldc) {
	__m256 valpha = _mm256_broadcast_ss(&alpha);
	__m256 vbeta  = _mm256_broadcast_ss(&beta);
	float packedA[M*K];
	for (int i = 0; i < M; i++) ikcopy(K, a+i*lda, 1, packedA+i*K, 1);
	for (int j = 0; j < N; j+=8) { // unrolled by 8
		for (int i = 0; i < M; i+=8) { // unrolled by 8
			__m256 c0x, c1x, c2x, c3x, c4x, c5x, c6x, c7x;
			if (beta == 0.) {
				c0x = _mm256_setzero_ps();
				c1x = _mm256_setzero_ps();
				c2x = _mm256_setzero_ps();
				c3x = _mm256_setzero_ps();
				c4x = _mm256_setzero_ps();
				c5x = _mm256_setzero_ps();
				c6x = _mm256_setzero_ps();
				c7x = _mm256_setzero_ps();
			} else if (beta == 1.) {
				c0x = _mm256_load_ps(c+(i+0)*ldc+j);
				c1x = _mm256_load_ps(c+(i+1)*ldc+j);
				c2x = _mm256_load_ps(c+(i+2)*ldc+j);
				c3x = _mm256_load_ps(c+(i+3)*ldc+j);
				c4x = _mm256_load_ps(c+(i+4)*ldc+j);
				c5x = _mm256_load_ps(c+(i+5)*ldc+j);
				c6x = _mm256_load_ps(c+(i+6)*ldc+j);
				c7x = _mm256_load_ps(c+(i+7)*ldc+j);
			} else {
				c0x = _mm256_mul_ps(_mm256_load_ps(c+(i+0)*ldc+j), vbeta);
				c1x = _mm256_mul_ps(_mm256_load_ps(c+(i+1)*ldc+j), vbeta);
				c2x = _mm256_mul_ps(_mm256_load_ps(c+(i+2)*ldc+j), vbeta);
				c3x = _mm256_mul_ps(_mm256_load_ps(c+(i+3)*ldc+j), vbeta);
				c4x = _mm256_mul_ps(_mm256_load_ps(c+(i+4)*ldc+j), vbeta);
				c5x = _mm256_mul_ps(_mm256_load_ps(c+(i+5)*ldc+j), vbeta);
				c6x = _mm256_mul_ps(_mm256_load_ps(c+(i+6)*ldc+j), vbeta);
				c7x = _mm256_mul_ps(_mm256_load_ps(c+(i+7)*ldc+j), vbeta);
			}
			for (int k = 0; k < K; k++) { // AddDot 8x8
				__m256 a0x = _mm256_broadcast_ss(packedA+(i+0)*K+k);
				__m256 a1x = _mm256_broadcast_ss(packedA+(i+1)*K+k);
				__m256 a2x = _mm256_broadcast_ss(packedA+(i+2)*K+k);
				__m256 a3x = _mm256_broadcast_ss(packedA+(i+3)*K+k);
				__m256 a4x = _mm256_broadcast_ss(packedA+(i+4)*K+k);
				__m256 a5x = _mm256_broadcast_ss(packedA+(i+5)*K+k);
				__m256 a6x = _mm256_broadcast_ss(packedA+(i+6)*K+k);
				__m256 a7x = _mm256_broadcast_ss(packedA+(i+7)*K+k);

				__m256 bx = _mm256_load_ps(b+k*ldb+j);
				if (alpha != 1.0) bx = _mm256_mul_ps(bx, valpha);

				c0x = _mm256_fmadd_ps(a0x, bx, c0x);
				c1x = _mm256_fmadd_ps(a1x, bx, c1x);
				c2x = _mm256_fmadd_ps(a2x, bx, c2x);
				c3x = _mm256_fmadd_ps(a3x, bx, c3x);
				c4x = _mm256_fmadd_ps(a4x, bx, c4x);
				c5x = _mm256_fmadd_ps(a5x, bx, c5x);
				c6x = _mm256_fmadd_ps(a6x, bx, c6x);
				c7x = _mm256_fmadd_ps(a7x, bx, c7x);
			}
			_mm256_store_ps(c+(i+0)*ldc+j, c0x);
			_mm256_store_ps(c+(i+1)*ldc+j, c1x);
			_mm256_store_ps(c+(i+2)*ldc+j, c2x);
			_mm256_store_ps(c+(i+3)*ldc+j, c3x);
			_mm256_store_ps(c+(i+4)*ldc+j, c4x);
			_mm256_store_ps(c+(i+5)*ldc+j, c5x);
			_mm256_store_ps(c+(i+6)*ldc+j, c6x);
			_mm256_store_ps(c+(i+7)*ldc+j, c7x);
		}
	}
}
void
gemm_9(size_t m, float *a, float *b, float *c) {
	// mc * m blocks of C by a call to the InnerKernel
	size_t kc = 64; // tuned according to L2 cache
	size_t mc = 64; // tuned according to L2 cache
	for (int p = 0; p < m; p += kc) { // M, N, Block(K)
		for (int q = 0; q < m; q += mc) { // Block(M), N, Block(K)
			// ikgemm8(subM, N, subK, alpha, subA, lda, subB, ldb, beta, subC, ldc);
			ikgemm9(mc, m, kc, 1., &a[q*m+p], m, &b[p*m+0], m, 1., &c[q*m+0], m);
		}
	}
}

// impl 10: Packing B: similar to A, better caching efficiency
void
ikgemm10(size_t M, size_t N, size_t K, const float alpha, float *a, size_t lda,
	   	float *b, size_t ldb, const float beta, float *c, size_t ldc) {
	__m256 valpha = _mm256_broadcast_ss(&alpha);
	__m256 vbeta  = _mm256_broadcast_ss(&beta);
	float packedA[M*K];
	float packedB[K*N];
	for (int i = 0; i < M; i++) ikcopy(K, a+i*lda, 1, packedA+i*K, 1);
	for (int i = 0; i < K; i++) ikcopy(N, b+i*ldb, 1, packedB+i*N, 1);
	for (int j = 0; j < N; j+=8) { // unrolled by 8
		for (int i = 0; i < M; i+=8) { // unrolled by 8
			__m256 c0x, c1x, c2x, c3x, c4x, c5x, c6x, c7x;
			if (beta == 0.) {
				c0x = _mm256_setzero_ps();
				c1x = _mm256_setzero_ps();
				c2x = _mm256_setzero_ps();
				c3x = _mm256_setzero_ps();
				c4x = _mm256_setzero_ps();
				c5x = _mm256_setzero_ps();
				c6x = _mm256_setzero_ps();
				c7x = _mm256_setzero_ps();
			} else if (beta == 1.) {
				c0x = _mm256_load_ps(c+(i+0)*ldc+j);
				c1x = _mm256_load_ps(c+(i+1)*ldc+j);
				c2x = _mm256_load_ps(c+(i+2)*ldc+j);
				c3x = _mm256_load_ps(c+(i+3)*ldc+j);
				c4x = _mm256_load_ps(c+(i+4)*ldc+j);
				c5x = _mm256_load_ps(c+(i+5)*ldc+j);
				c6x = _mm256_load_ps(c+(i+6)*ldc+j);
				c7x = _mm256_load_ps(c+(i+7)*ldc+j);
			} else {
				c0x = _mm256_mul_ps(_mm256_load_ps(c+(i+0)*ldc+j), vbeta);
				c1x = _mm256_mul_ps(_mm256_load_ps(c+(i+1)*ldc+j), vbeta);
				c2x = _mm256_mul_ps(_mm256_load_ps(c+(i+2)*ldc+j), vbeta);
				c3x = _mm256_mul_ps(_mm256_load_ps(c+(i+3)*ldc+j), vbeta);
				c4x = _mm256_mul_ps(_mm256_load_ps(c+(i+4)*ldc+j), vbeta);
				c5x = _mm256_mul_ps(_mm256_load_ps(c+(i+5)*ldc+j), vbeta);
				c6x = _mm256_mul_ps(_mm256_load_ps(c+(i+6)*ldc+j), vbeta);
				c7x = _mm256_mul_ps(_mm256_load_ps(c+(i+7)*ldc+j), vbeta);
			}
			for (int k = 0; k < K; k++) { // AddDot 8x8
				__m256 a0x = _mm256_broadcast_ss(packedA+(i+0)*K+k);
				__m256 a1x = _mm256_broadcast_ss(packedA+(i+1)*K+k);
				__m256 a2x = _mm256_broadcast_ss(packedA+(i+2)*K+k);
				__m256 a3x = _mm256_broadcast_ss(packedA+(i+3)*K+k);
				__m256 a4x = _mm256_broadcast_ss(packedA+(i+4)*K+k);
				__m256 a5x = _mm256_broadcast_ss(packedA+(i+5)*K+k);
				__m256 a6x = _mm256_broadcast_ss(packedA+(i+6)*K+k);
				__m256 a7x = _mm256_broadcast_ss(packedA+(i+7)*K+k);

				__m256 bx = _mm256_load_ps(packedB+k*N+j);
				if (alpha != 1.0) bx = _mm256_mul_ps(bx, valpha);

				c0x = _mm256_fmadd_ps(a0x, bx, c0x);
				c1x = _mm256_fmadd_ps(a1x, bx, c1x);
				c2x = _mm256_fmadd_ps(a2x, bx, c2x);
				c3x = _mm256_fmadd_ps(a3x, bx, c3x);
				c4x = _mm256_fmadd_ps(a4x, bx, c4x);
				c5x = _mm256_fmadd_ps(a5x, bx, c5x);
				c6x = _mm256_fmadd_ps(a6x, bx, c6x);
				c7x = _mm256_fmadd_ps(a7x, bx, c7x);
			}
			_mm256_store_ps(c+(i+0)*ldc+j, c0x);
			_mm256_store_ps(c+(i+1)*ldc+j, c1x);
			_mm256_store_ps(c+(i+2)*ldc+j, c2x);
			_mm256_store_ps(c+(i+3)*ldc+j, c3x);
			_mm256_store_ps(c+(i+4)*ldc+j, c4x);
			_mm256_store_ps(c+(i+5)*ldc+j, c5x);
			_mm256_store_ps(c+(i+6)*ldc+j, c6x);
			_mm256_store_ps(c+(i+7)*ldc+j, c7x);
		}
	}
}
void
gemm_10(size_t m, float *a, float *b, float *c) {
	// mc * m blocks of C by a call to the InnerKernel
	size_t kc = 64; // tuned according to L2 cache
	size_t mc = 64; // tuned according to L2 cache
	for (int p = 0; p < m; p += kc) { // M, N, Block(K)
		for (int q = 0; q < m; q += mc) { // Block(M), N, Block(K)
			// ikgemm8(subM, N, subK, alpha, subA, lda, subB, ldb, beta, subC, ldc);
			ikgemm10(mc, m, kc, 1., &a[q*m+p], m, &b[p*m+0], m, 1., &c[q*m+0], m);
		}
	}
}


// impl 11: Threading

int
main(void)
{
	cout << "GEMM_1 Benchmark: naive implementation" << endl;
	bench(gemm_1);

	cout << "GEMM_2 Benchmark: nesting and unroll" << endl;
	bench(gemm_2);

	cout << "GEMM_3 Benchmark: register" << endl;
	bench(gemm_3);

	cout << "GEMM_4 Benchmark: eliminate offset calculation" << endl;
	bench(gemm_4);

	cout << "GEMM_5 Benchmark: unroll more loop" << endl;
	bench(gemm_5);

	cout << "GEMM_6 Benchmark: SIMD SSE" << endl;
	bench(gemm_6);

	cout << "GEMM_7 Benchmark: SIMD AVX" << endl;
	bench(gemm_7);

	cout << "GEMM_8 Benchmark: Blocking" << endl;
	bench(gemm_8);

	cout << "GEMM_9 Benchmark: Packing A" << endl;
	bench(gemm_9);

	cout << "GEMM_10 Benchmark: Packing B" << endl;
	bench(gemm_10);

	return 0;
}
