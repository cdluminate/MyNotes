// https://felix.abecassis.me/2011/09/cpp-getting-started-with-sse/
// xmm0 ... xmm7, each of them is a 128bit register.
// 128bit -> 2 fp64, 4 fp32, 2 i64, 4 i32, 8 i16, 16 u8
// __m128*: __m128 for float, __m128d for double, __m128i for int, short, char

#include <emmintrin.h>
#include <stdio.h>
#include <malloc.h>
#include <math.h>
#include <time.h>

#define VECLEN 33554432

void svsqrt(float* X, size_t N) {
	for (int i = 0; i < N; i++) {
		X[i] = sqrt(X[i]);
	}
}

void svsqrt_sse(float* X, size_t N) {
	// N must be 4 K where K in Integer.
	__m128* x = (__m128*)X;
	for (int i = 0; i < (int)(N/4); i++, x++, X+=4) {
		_mm_store_ps(X, _mm_sqrt_ps(*x));
	}
}

void svsqrt_sse_aggressive(float* X, size_t N) {
	// N must be 8 * 4 K where K in Integer.
	// use all XMM (SSE) registers xmm0 ... xmm7
	__m128* x0 = (__m128*)X; __m128* x1 = x0+1;
	__m128* x2 = x0+2; __m128* x3 = x0+3;
	__m128* x4 = x0+4; __m128* x5 = x0+5;
	__m128* x6 = x0+6; __m128* x7 = x0+7;
	for (int i = 0; i < (int)(N/32); i++, X+=32,
			x0++,x1++,x2++,x3++,x4++,x5++,x6++,x7++) {
		_mm_store_ps(X+0, _mm_sqrt_ps(*x0));
		_mm_store_ps(X+4, _mm_sqrt_ps(*x1));
		_mm_store_ps(X+8, _mm_sqrt_ps(*x2));
		_mm_store_ps(X+12, _mm_sqrt_ps(*x3));
		_mm_store_ps(X+16, _mm_sqrt_ps(*x4));
		_mm_store_ps(X+20, _mm_sqrt_ps(*x5));
		_mm_store_ps(X+24, _mm_sqrt_ps(*x6));
		_mm_store_ps(X+28, _mm_sqrt_ps(*x7));
	}
}

void i8xpy_sse(char* X, const char* Y, size_t N) {
	// N must be a multiple of 16
	__m128i* l = (__m128i*)X;
	__m128i* r = (__m128i*)Y;
	for (int i = 0; i < (int)(N/16); i++, l++, r++) {
		_mm_store_si128(l, _mm_add_epi8(*l, *r));
	}
}

int
main(void)
{
	clock_t c1;

	float a[] __attribute__ ((aligned (16))) = { 1., 4., 9., 16. };
	printf("%f %f %f %f\n", a[0], a[1], a[2], a[3]);

	__m128 t = _mm_sqrt_ps(*((__m128*)a));
	float* b = (float*)&t;

	printf("%f %f %f %f\n", b[0], b[1], b[2], b[3]);

	float* c;
	posix_memalign((void**)&c, 16, sizeof(float)*VECLEN);

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
	svsqrt_sse(c, VECLEN);
	printf("%ld\n", clock()-c1);

	for (int i = 0; i < VECLEN; i++) {
		c[i] = 3141592.65358;
	}
	c1 = clock();
	svsqrt_sse_aggressive(c, VECLEN);
	printf("%ld\n", clock()-c1);

	return 0;
}
