#include <cstdlib>
#include <iostream>
#include <cstdio>
#include <sys/time.h>
#include <cblas.h>
#include <cassert>
#include <cstring>
using namespace std;

void
sgemm(size_t M, size_t N, size_t K, float *A, size_t LDA, float *B, size_t LDB, float *C, size_t LDC);

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

// test helper
void
bench(void (*func)(size_t m, size_t n, size_t k, float *a, size_t lda, float *b, size_t ldb, float *c, size_t ldc), size_t sz)
{
	// allocate memory
	float *A = (float*)aligned_alloc(64, sz*sz*sizeof(float));
	float *B = (float*)aligned_alloc(64, sz*sz*sizeof(float));
	float *C = (float*)aligned_alloc(64, sz*sz*sizeof(float));
	float *D = (float*)aligned_alloc(64, sz*sz*sizeof(float));

	// prepare data
	pop_(sz, A, true);
	pop_(sz, B, true);
	pop_(sz, C, false);
	pop_(sz, D, false);

	// run naive impl
	tic();
	func(sz, sz, sz, A, sz, B, sz, C, sz);
	long el = toc();
	if (0 == el) el++;
	float gflops = (2.0 *  sz * sz * sz)/el * 1e-3;

	// run reference impl
	tic();
	cblas_sgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
			sz, sz, sz, 1., A, sz, B, sz, 0., D, sz);
	long refel = toc();
	float refgflops = (2.0 *  sz * sz * sz)/refel * 1e-3;

	// compare
	cblas_saxpy(sz*sz, -1., C, 1, D, 1);
	assert(cblas_snrm2(sz*sz, D, 1) < 1.);
	printf("(%5d) %9ld μs, %6.3f gflops, maxerr %6.3f | ref %8ld μs, %9.3f gflops\n",
			sz, el, gflops, D[cblas_isamax(sz*sz, D, 1)], refel, refgflops);
	fflush(stdout);

	// free
	free(A); free(B); free(C); free(D);
}

int
main(void)
{
	bench(sgemm, 512);
	return 0;
}
