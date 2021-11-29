// https://software.intel.com/sites/default/files/m/d/4/1/d/8/Intro_to_Intel_AVX.pdf
// https://software.intel.com/en-us/articles/introduction-to-intel-advanced-vector-extensions/
// hardware supporting AVX consists of 16 256-bit YMM registers ymm0..ymm15
//   and a 32-bit control/status register MXCSR
// data should be aligned before feeding to AVX instructions.
//   the alignment should be 16-byte for 128-bit access and 32-byte for 256-bit

#include <immintrin.h>
#include <stdio.h>
#include <malloc.h>
#include <math.h>
#include <time.h>

#define VECLEN 33554432

void svsqrt(float* X, size_t N) {
#pragma omp for
	for (int i = 0; i < N; i++) {
		X[i] = sqrt(X[i]);
	}
}

void svsqrt_avx(float* X, size_t N) {
	// N must be 8 K where K in Integer.
	__m256* x = (__m256*)X;
	for (int i = 0; i < (int)(N/8); i++, x++, X+=8) {
		_mm256_store_ps(X, _mm256_sqrt_ps(*x));
	}
}

void svsqrt_avx_aggressive(float* X, size_t N) {
	// N must be 16 * 8 K where K in Integer
	__m256* x0 = (__m256*)X; __m256* x1 = x0+1;
	__m256* x2 = x0+2; __m256* x3 = x0+3;
	__m256* x4 = x0+4; __m256* x5 = x0+5;
	__m256* x6 = x0+6; __m256* x7 = x0+7;
	__m256* x8 = x0+8; __m256* x9 = x0+9;
	__m256* x10 = x0+10; __m256* x11 = x0+11;
	__m256* x12 = x0+12; __m256* x13 = x0+13;
	__m256* x14 = x0+14; __m256* x15 = x0+15;
	for (int i = 0; i < (int)(N/128); i++, X+=128,
			x0++, x1++, x2++, x3++, x4++, x5++, x6++, x7++) {
		_mm256_store_ps(X+0, _mm256_sqrt_ps(*x0));
		_mm256_store_ps(X+8, _mm256_sqrt_ps(*x1));
		_mm256_store_ps(X+16, _mm256_sqrt_ps(*x2));
		_mm256_store_ps(X+24, _mm256_sqrt_ps(*x3));
		_mm256_store_ps(X+32, _mm256_sqrt_ps(*x4));
		_mm256_store_ps(X+40, _mm256_sqrt_ps(*x5));
		_mm256_store_ps(X+48, _mm256_sqrt_ps(*x6));
		_mm256_store_ps(X+56, _mm256_sqrt_ps(*x7));
		_mm256_store_ps(X+64, _mm256_sqrt_ps(*x8));
		_mm256_store_ps(X+72, _mm256_sqrt_ps(*x9));
		_mm256_store_ps(X+80, _mm256_sqrt_ps(*x10));
		_mm256_store_ps(X+88, _mm256_sqrt_ps(*x11));
		_mm256_store_ps(X+96, _mm256_sqrt_ps(*x12));
		_mm256_store_ps(X+104, _mm256_sqrt_ps(*x13));
		_mm256_store_ps(X+112, _mm256_sqrt_ps(*x14));
		_mm256_store_ps(X+120, _mm256_sqrt_ps(*x15));
	}
}

int
main(void)
{
	clock_t c1;

	float* c;
	posix_memalign((void**)&c, 32, sizeof(float)*VECLEN);

	for (int i = 0; i < VECLEN; i++) {
		c[i] = 3141592.65358;
	}
	c1 = clock();
	svsqrt(c, VECLEN);
	printf("%ld\n", clock()-c1);

	for (int i = 0; i < VECLEN; i++) {
		c[i] = 3141592.65358;
	}
	c1 = clock();
	svsqrt_avx(c, VECLEN);
	printf("%ld\n", clock()-c1);

	for (int i = 0; i < VECLEN; i++) {
		c[i] = 3141592.65358;
	}
	c1 = clock();
	svsqrt_avx_aggressive(c, VECLEN);
	printf("%ld\n", clock()-c1);

	return 0;
}

// -mavx2 avx.c -O3 -lm -ffast-math -march=native -mtune=native
// result: plain code, after compiler optimization, is the fastest branch.
