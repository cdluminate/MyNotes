/**
 * @file benchmark.c
 * @brief benchmark the amount of time saved by parallel program
 * @note compile with '--std=c99'
 * @author Lumin <cdluminate@gmail.com>
 */

#define USE_CUDA
#undef USE_CUDA

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <omp.h>
#include <sys/time.h> // high precision timer, gettimeofday()
#include <assert.h>

#ifdef USE_CUDA
  #include "cudabench.h" // cuda benchmarks
#endif

double * new_vector (size_t len);
void fill_vector (double * v, size_t len, double val);
void dump_vector (double * v, size_t size);
void del_vector (double * v);

/**
 * @brief flag, set 1 to dump all debug information
 */
int debug = 0;

/**
 * @brief vector length used in L-1 benchmarks
 */
#define VLEN 1024*1024*16

/**
 * @brief matrix size used in L-2 benchmarks
 */
#define MVLEN 1024*4

/**
 * @brief matrix size used in L-3 benchmarks
 */
#define MMLEN 256

/**
 * @brief IMLEN image size, KLEN kernel size, FLEN(IM,K) feature map size
 */
#define IMLEN 512
#define KLEN 17
#define FLEN(im,k) ((im-k+1))

/**
 * @brief helper function for tester
 */
void
check_vector_eq (const double * src, const double * dest, size_t n)
{
  for (size_t i = 0; i < n; i++) {
    if (fabs(src[i] - dest[i]) > 1e-5) {
      fprintf (stderr, "E: check_vector_eq failure at element %ld\n", i);
      return;
    }
  }
}

/**
 * @breif dcopy, L-1 BLAS, serial
 */
void
dcopy_serial (const double * src, double * dest, size_t n)
{
  for (long i = 0; i < n; i++)
    dest[i] = src[i];
  return;
}

/**
 * @brief dcopy, L-1 BLAS, parallel
 */
void
dcopy_parallel (const double * src, double * dest, size_t n)
{
#pragma omp parallel for shared(src, dest)
  for (long i = 0; i < n; i++)
    dest[i] = src[i];
  return;
}

/**
 * @brief tester for dcopy
 */
void
test_dcopy (void (* dcopy)(const double * src, double * dest, size_t n))
{
  printf("[ .. ] test dcopy@%p\n", dcopy);
  // short vector
  double * A = new_vector(128);
  double * C = new_vector(128);
  fill_vector(A, 128, 1.);
  fill_vector(C, 128, 0.);
  dcopy (A, C, 128);
  check_vector_eq (A, C, 128);
  del_vector(A);
  del_vector(C);
  // long vector
  double * B = new_vector(65536);
  double * D = new_vector(65536);
  fill_vector(B, 65536, 2.);
  fill_vector(D, 65536, 0.);
  dcopy (B, D, 65536);
  check_vector_eq (B, D, 65536);
  del_vector (B);
  del_vector (D);
  printf("[ OK ] test dcopy@%p\n", dcopy);
}

/**
 * @brief dasum, L-1 BLAS, serial
 */
double
dasum_serial (const double * a, size_t n)
{
  double ret = 0.;
  for (long i = 0; i < n; i++) {
    ret += (a[i]>0.)?(a[i]):(-a[i]);
    //if (0 == i % 1000000) printf (" iter %ld, n = %lf\n", i, ret); // debug
  }
  return ret;
}

/**
 * @brief dasum, L-1 BLAS, parallel
 */
double
dasum_parallel (const double * a, size_t n)
{
  double ret = 0.;
#pragma omp parallel for reduction (+:ret)
  for (long i = 0; i < n; i++)
    ret += (a[i]>0.)?(a[i]):(-a[i]);
  return ret;
}

/**
 * @brief tester for dasum
 */
void
test_dasum (double (* dasum)(const double * a, size_t n))
{
  printf("[ .. ] test dasum@%p\n", dasum);
  // long vector
  double * A = new_vector(1280);
  fill_vector(A, 1280, 1.); //dump_vector (A, 128);
  double ret = dasum (A, 1280); //printf ("%lf\n", ret);
  assert(fabs(ret - 1280.) < 1e-5);
  del_vector (A);
  // short vector // FIXME: BUG: wrong result dasum_cuda when size 128
  double * B = new_vector(128);
  fill_vector(B, 128, 1.0);
  ret = dasum(B, 128);
  assert(fabs(ret - 128.) < 1e-5);
  del_vector (B);
  // another long vector
  double * C = new_vector(1200);
  fill_vector(C, 1200, 1.); //dump_vector (A, 128);
  ret = dasum (C, 1200); //printf ("%lf\n", ret);
  assert(fabs(ret - 1200.) < 1e-5);
  del_vector (C);
  printf("[ OK ] test dasum@%p\n", dasum);
}

/**
 * @brief dscal, L-1 BLAS, serial
 */
void
dscal_serial (double * x, const double a, size_t n)
{
  for (size_t i = 0; i < n; i++)
    x[i] *= a;
}

/**
 * @brief dscal, L-1 BLAS, parallel
 */
void
dscal_parallel (double * x, const double a, size_t n)
{
#pragma omp parallel for shared(x)
  for (size_t i = 0; i < n; i++)
    x[i] *= a;
}

/**
 * @brief ddot, L-1 BLAS, serial
 */
double
ddot_serial (const double * a, const double * b, size_t n)
{
  double ret = 0.;
  for (long i = 0; i < n; i++)
    ret += a[i] * b[i];
  return ret;
}

/**
 * @brief ddot, L-1 BLAS, parallel
 */
double
ddot_parallel (const double * a, const double * b, size_t n)
{
  double ret = 0.;
#pragma omp parallel for reduction (+:ret)
  for (long i = 0; i < n; i++)
    ret += a[i] * b[i];
  return ret;
}

/**
 * @brief daxpby, L-1 BLAS Extension, serial
 */
void
daxpby_serial (const double * x, const double a,
  double * y, const double b, size_t n)
{
  // a x + b y -> y
  for (long i = 0; i < n; i++)
    y[i] += a * x[i] + b * y[i];
}

/**
 * @brief daxpby, L-1 BLAS Extension, parallel
 */
void
daxpby_parallel (const double * x, const double a,
  double * y, const double b, size_t n)
{
  // a x + b y -> y
#pragma omp parallel for shared(x, y)
  for (long i = 0; i < n; i++)
    y[i] += a * x[i] + b * y[i];
}

/**
 * @brief dgemv, L-2 BLAS, serial
 * @f[ a x * b y -> dest @f]
 */
void
dgemv_serial (const double * x, const double a,
  const double * y, const double b, 
  size_t n, double * dest)
{
  // note, x is matrix !
  for (size_t i = 0; i < n; i++) { // for each row of x
    dest[i] = y[i];
    for (size_t j = 0; j < n; j++) { // for each column of y
      dest[i] += a * *(x+(i*n)+j) * b * y[j];
    }
  }
}

/**
 * @brief dgemv, L-2 BLAS, parallel
 * @f[ a x * b y -> dest @f]
 */
void
dgemv_parallel (const double * x, const double a,
  const double * y, const double b,
  size_t n, double * dest)
{
  size_t j = 0;
#pragma omp parallel for shared(x, y, dest) private(j)
  for (size_t i = 0; i < n; i++) { // for each row of x
    dest[i] = y[i];
    for (j = 0; j < n; j++) { // for each column of y
      dest[i] += a * *(x+(i*n)+j) * b * y[j];
    }
  }
}

/**
 * @brief dgemv, L-2 BLAS, parallel version 2
 * @f[ a x * b y -> dest @f]
 */
void
dgemv_parallelv2 (const double * x, const double a,
  const double * y, const double b,
  size_t n, double * dest)
{
  size_t j = 0;
  size_t i = 0;
  dcopy_parallel(y, dest, n);
#pragma omp parallel for collapse(2) shared(x, y, dest) private(i,j)
  for (i = 0; i < n; i++) { // for each row of x
  for (j = 0; j < n; j++) { // for each column of y
      dest[i] += a * *(x+(i*n)+j) * b * y[j];
  }}
}

/**
 * @brief dgemm, L-3 BLAS, serial version
 * @f[ A_{m x n} * B_{n x k} -> C_{m x k} @f]
 */
void
dgemm_serial (const double * A, const double * B,
  size_t m, size_t n, size_t k, double * C)
{
  size_t mm = 0, nn = 0, kk = 0;
  for (mm = 0; mm < m; mm++) {
    for (kk = 0; kk < k; kk++) {
      *(C+mm*k+kk) = 0;
      for (nn = 0; nn < n; nn++) {
        *(C+mm*k+kk) += *(A+mm*n+nn) * *(B+nn*k+kk);
      }
    }
  }
}

/**
 * @brief dgemm, L-3 BLAS, parallel version
 * @f[ A_{m x n} * B_{n x k} -> C_{m x k} @f]
 */
void
dgemm_parallel (const double * A, const double * B,
  size_t m, size_t n, size_t k, double * C)
{
  size_t mm = 0, nn = 0, kk = 0;
#pragma omp parallel for collapse(2) shared(A, B) private(nn)
// Note, dynamic scheduler seems to reduce performance here
  for (mm = 0; mm < m; mm++) {
  for (kk = 0; kk < k; kk++) {
    *(C+mm*k+kk) = 0;
    for (nn = 0; nn < n; nn++) {
      *(C+mm*k+kk) += *(A+mm*n+nn) * *(B+nn*k+kk);
    }
  }}
}

/**
 * @brief dgemm, L-3 BLAS, parallel version 2
 * @f[ A_{m x n} * B_{n x k} -> C_{m x k} @f]
 */
void
dgemm_parallelv2 (const double * A, const double * B,
  size_t m, size_t n, size_t k, double * C)
{
  size_t mm = 0, nn = 0, kk = 0;
#pragma omp parallel for shared(A, B) private(kk,nn)
  for (mm = 0; mm < m; mm++) {
    for (kk = 0; kk < k; kk++) {
      *(C+mm*k+kk) = 0;
      for (nn = 0; nn < n; nn++) {
        *(C+mm*k+kk) += *(A+mm*n+nn) * *(B+nn*k+kk);
      }
    }
  }
}

/**
 * @brief 2-D convolution in serial 
 * (Computer Vision Convolution, not Signal Convolution)
 * @param[in] smap source map
 * @param[in] dmap destination map
 * @param[in] m smap size
 * @param[in] k kernel size
 * @note no padding
 */
void
conv2_serial (const double * smap, const double * kernel,
  size_t ssize, size_t ksize,
  double * dmap)
{
  for (unsigned int i = 0; i < FLEN(ssize,ksize); i++) { // for each row of output map
  for (unsigned int j = 0; j < FLEN(ssize,ksize); j++) { // for each column of output map
    // element wise mult, smap part with kernel
    double sum = 0.;
    for (unsigned int m = 0; m < ksize; m++) {
    for (unsigned int n = 0; n < ksize; n++) {
      sum += kernel[m*ksize +n] * smap[(i+m)*ssize + j+n];
    }}
    // finish (i,j) of output feature map
    dmap[i*FLEN(ssize,ksize)+j] = sum;
  }}
  return;
}

/**
 * @brief 2-D convolution in parallel
 * (Computer Vision Convolution, not Signal Convolution)
 */
void
conv2_parallel (const double * smap, const double * kernel,
  size_t ssize, size_t ksize,
  double * dmap)
{
  double sum = 0.;
#pragma omp parallel for collapse(2) shared(smap,kernel,dmap) private(sum)
  for (unsigned int i = 0; i < FLEN(ssize,ksize); i++) { // for each row of output map
  for (unsigned int j = 0; j < FLEN(ssize,ksize); j++) { // for each column of output map
    // element wise mult, smap part with kernel
    sum = 0.;
    for (unsigned int m = 0; m < ksize; m++) {
    for (unsigned int n = 0; n < ksize; n++) {
      sum += kernel[m*ksize +n] * smap[(i+m)*ssize + j+n];
    }}
    // finish (i,j) of output feature map
    dmap[i*FLEN(ssize,ksize)+j] = sum;
  }}
  return;
}

/**
 * @brief tell user the time difference in second.
 * @param tvs the starting time stamp.
 * @param tve the ending timp stamp.
 * @see sys/time.h, gettimeofday(2)
 */
void
timediff (struct timeval tvs, struct timeval tve, char * msg)
{
  long diff_sec  = tve.tv_sec - tvs.tv_sec;
  long diff_usec = tve.tv_usec - tvs.tv_usec;
  double dtime = diff_sec + diff_usec/1e+6;
  fprintf (stdout, "I: [%s] time cost is %1.6f seconds.\n",
    (msg==NULL)?"":msg, dtime);
}
/**
 * @brief find the time difference in second
 */
double
gettimediff (struct timeval tvs, struct timeval tve)
{
  return ((tve.tv_sec - tvs.tv_sec) + (tve.tv_usec - tvs.tv_usec)/1e+6);
}

/**
 * @brief print a spliting line on screen
 */
void
hrulefill (void)
{
  for (int i = 0; i < 80; i++)
    fprintf (stdout, "-");
  fprintf (stdout, "\n");
  return;
}

/**
 * @brief dump a vector to screen
 */
void
dump_vector (double * v, size_t size)
{
  for (size_t i = 0; i < size; i++)
    fprintf (stdout, " %.3lf", v[i]);
  fprintf (stdout, "\n");
  return;
}

/**
 * @brief dump a matrix to screen
 */
void
dump_matrix (double * m, size_t row, size_t col)
{
  for (size_t i = 0; i < row; i++) {
    for (size_t j = 0; j < col; j++)
      fprintf (stdout, " %.3lf", m[i*col+j]);
    fprintf (stdout, "\n");
  }
  return;
}

/**
 * @brief allocate a vector in double
 * @note values of vector not initialized on allocation.
 */
double *
new_vector (size_t len)
{
  double * ret = (double *)malloc(len*sizeof(double));
  assert(ret != NULL);
  return ret;
}

/**
 * @brief delete a vector in double
 */
void
del_vector (double * v)
{
  free(v);
}

/**
 * @brief fill a double vector with a value
 */
void
fill_vector (double * v, size_t len, double val)
{
  for (size_t i = 0; i < len; i++)
    v[i] = val;
  return;
}

/**
 * @brief allocate a double matrix
 */
double *
new_matrix (size_t row, size_t col)
{
  double * ret = (double *)malloc(row*col*sizeof(double));
  assert(ret != NULL);
  return ret;
}

/**
 * @brief delete a matrix in double
 */
void
del_matrix (double * m)
{
  free(m);
}

/**
 * @brief fill a double matrix with a value
 */
void
fill_matrix (double * m, size_t row, size_t col, double val)
{
  for (size_t i = 0; i < row; i++)
    for (size_t j = 0; j < col; j++)
      m[i*col+j] = val;
  return;
}

// benchmark for dcopy
void benchmark_dcopy (void (* dcopy)(const double * src, double * dest, size_t n))
{
  struct timeval tvs;
  struct timeval tve;
  long   sizes[8]  ={ 1, 16, 256, 4096, 65536, 1048576, 16777216, 33554432 };
  double results[8]={ 0.,0.,  0.,   0.,    0.,      0.,       0.,       0. };
  // print table header
  for (int i = 0; i < 8; i++) printf ("|%8ld", sizes[i]);
  printf ("|\n");
  for (int i = 0; i < 8; i++) {
    // prepare memory for data
    double * A = new_vector(sizes[i]);
    double * C = new_vector(sizes[i]);
    fill_vector (A, sizes[i], 1.);
    fill_vector (C, sizes[i], 0.);
    // calculate
    gettimeofday (&tvs, NULL);
    dcopy (A, C, sizes[i]);
    gettimeofday (&tve, NULL);
    check_vector_eq (A, C, sizes[i]);
    // store result
    results[i] = gettimediff (tvs, tve);
    del_vector (A);
    del_vector (C);
  }
  // print results
  for (int i = 0; i < 8; i++) printf ("|%8.6lf", results[i]);
  printf ("|\n");
}

// benchmark for dasum
void benchmark_dasum (double (* dasum)(const double * src, size_t n))
{
  struct timeval tvs;
  struct timeval tve;
  long   sizes[8]  ={ 1, 16, 256, 4096, 65536, 1048576, 16777216, 33554432 };
  double results[8]={ 0.,0.,  0.,   0.,    0.,      0.,       0.,       0. };
  // print table header
  for (int i = 0; i < 8; i++) printf ("|%8ld", sizes[i]);
  printf ("|\n");
  for (int i = 0; i < 8; i++) {
    // prepare memory for data
    double * A = new_vector(sizes[i]);
    fill_vector (A, sizes[i], 1.);
    // calculate
    gettimeofday (&tvs, NULL);
    (void) dasum (A, sizes[i]); // discard the summary
    gettimeofday (&tve, NULL);
    // store result
    results[i] = gettimediff (tvs, tve);
    del_vector (A);
  }
  // print results
  for (int i = 0; i < 8; i++) printf ("|%8.6lf", results[i]);
  printf ("|\n");
}

// benchmark for ddot
void benchmark_ddot (double (* ddot)(const double * a, const double * b, size_t n))
{
  struct timeval tvs;
  struct timeval tve;
  long   sizes[8]  ={ 1, 16, 256, 4096, 65536, 1048576, 16777216, 33554432 };
  double results[8]={ 0.,0.,  0.,   0.,    0.,      0.,       0.,       0. };
  // print table header
  for (int i = 0; i < 8; i++) printf ("|%8ld", sizes[i]);
  printf ("|\n");
  for (int i = 0; i < 8; i++) {
    // prepare memory for data
    double * A = new_vector(sizes[i]);
    double * B = new_vector(sizes[i]);
    fill_vector (A, sizes[i], 1.);
    fill_vector (B, sizes[i], 1.);
    // calculate
    gettimeofday (&tvs, NULL);
    (void) ddot (A, B, sizes[i]); // discard the summary
    gettimeofday (&tve, NULL);
    // store result
    results[i] = gettimediff (tvs, tve);
    del_vector (A);
    del_vector (B);
  }
  // print results
  for (int i = 0; i < 8; i++) printf ("|%8.6lf", results[i]);
  printf ("|\n");
}

// benchmark for dscal
void benchmark_dscal (void (* dscal)(double * x, const double a, size_t n))
{
  struct timeval tvs;
  struct timeval tve;
  long   sizes[8]  ={ 1, 16, 256, 4096, 65536, 1048576, 16777216, 33554432 };
  double results[8]={ 0.,0.,  0.,   0.,    0.,      0.,       0.,       0. };
  // print table header
  for (int i = 0; i < 8; i++) printf ("|%8ld", sizes[i]);
  printf ("|\n");
  for (int i = 0; i < 8; i++) {
    // prepare memory for data
    double * A = new_vector(sizes[i]);
    fill_vector (A, sizes[i], 1.);
    // calculate
    gettimeofday (&tvs, NULL);
    dscal (A, 0.5, sizes[i]); // discard the summary
    gettimeofday (&tve, NULL);
    // store result
    results[i] = gettimediff (tvs, tve);
    del_vector (A);
  }
  // print results
  for (int i = 0; i < 8; i++) printf ("|%8.6lf", results[i]);
  printf ("|\n");
}

/**
 * @brief Lumin's benchmark
 */
int
main (int argc, char ** argv, char ** envp)
{
  fprintf (stdout, "Lumin's serial/parallel/cuda benchmark\nI: initializing ... ");
  fflush(stdout);

  struct timeval tvs; // tv_s, for starting point
  struct timeval tve; // tv_e, for ending point

  // init times
  struct timeval tvi; // tv_init
  struct timeval tvt; // tv_terminate

  gettimeofday(&tvi, NULL);
  fprintf(stdout, "[OK]\n");

  hrulefill();
  { // start unit tests

    test_dcopy(dcopy_serial);
    test_dcopy(dcopy_parallel);
#ifdef USE_CUDA
    test_dcopy(dcopy_cuda);
#endif // USE_CUDA

    test_dasum(dasum_serial);
    test_dasum(dasum_parallel);
#ifdef USE_CUDA
    test_dasum(dasum_cuda);
#endif

  } // end unit tests
  hrulefill();
  { // copy test

    printf ("I: [dcopy_serial] test series\n");
    benchmark_dcopy (dcopy_serial);
    printf ("I: [dcopy_parallel] test series\n");
    benchmark_dcopy (dcopy_parallel);
#ifdef USE_CUDA
    printf ("I: [dcopy_cuda] test series\n");
    benchmark_dcopy (dcopy_cuda);
#endif // USE_CUDA

  }
  hrulefill();
  { // asum test

    printf ("I: [dasum_serial] test series\n");
    benchmark_dasum (dasum_serial);
    printf ("I: [dasum_parallel] test series\n");
    benchmark_dasum (dasum_parallel);
#ifdef USE_CUDA
    printf ("I: [dasum_cuda] test series\n");
    benchmark_dasum (dasum_cuda);
#endif // USE_CUDA

  }
  hrulefill();
  { // dot test
    // FIXME: add unit tests for ddot

    // run benchmarks
    printf ("I: [ddot_serial] test series\n");
    benchmark_ddot (ddot_serial);
    printf ("I: [ddot_parallel] test series\n");
    benchmark_ddot (ddot_parallel);

  }
  hrulefill();
  { // scal test
    // FIXME: add unit tests

    // run benchmarks
    printf ("I: [dscal_serial] test series\n");
    benchmark_dscal (dscal_serial);
    printf ("I: [dscal_parallel] test series\n");
    benchmark_dscal (dscal_parallel);
#ifdef USE_CUDA
    printf ("I: [dscal_cuda] test series\n");
    benchmark_dscal (dscal_cuda);
#endif // USE_CUDA

  }
  hrulefill();
  { // axpby test

    // data
    double * A = new_vector(VLEN);
    double * C = new_vector(VLEN);
    fill_vector(A, VLEN, 1.);
    fill_vector(C, VLEN, 1.);

    // serial
    gettimeofday(&tvs, NULL);
    daxpby_serial (A, 0.5, C, 0.5, VLEN);
    gettimeofday(&tve, NULL);
    timediff (tvs, tve, "daxpby in serial");

    if (debug) dump_vector(A, VLEN);
    if (debug) dump_vector(C, VLEN);

    // parallel
    gettimeofday(&tvs, NULL);
    daxpby_parallel (A, 0.5, C, 0.5, VLEN);
    gettimeofday(&tve, NULL);
    timediff (tvs, tve, "daxpby in parallel");

    if (debug) dump_vector(A, VLEN);
    if (debug) dump_vector(C, VLEN);

    // post-test
    del_vector(A);
    del_vector(C);
  }
  hrulefill();
  { // gemv test

    // data
    double * M = new_matrix(MVLEN, MVLEN);
    double * A = new_vector(MVLEN);
    double * Y = new_vector(MVLEN);
    fill_matrix(M, MVLEN, MVLEN, 1.);
    fill_vector(A, MVLEN, 1.);
    fill_vector(Y, MVLEN, 1.);
  
    if (debug) dump_matrix(M, MVLEN, MVLEN);
    if (debug) dump_vector(A, MVLEN);

    // serial
    gettimeofday(&tvs, NULL);
    dgemv_serial (M, 1., A, 1., MVLEN, Y);
    gettimeofday(&tve, NULL);
    timediff (tvs, tve, "dgemv in serial");

    if (debug) dump_vector(Y, MVLEN);

    // parallel
    gettimeofday(&tvs, NULL);
    dgemv_parallel (M, 1., A, 1., MVLEN, Y);
    gettimeofday(&tve, NULL);
    timediff (tvs, tve, "dgemv in parallel");

    if (debug) dump_vector(Y, MVLEN);

    // parallelv2
    gettimeofday(&tvs, NULL);
    dgemv_parallelv2 (M, 1., A, 1., MVLEN, Y);
    gettimeofday(&tve, NULL);
    timediff (tvs, tve, "dgemv in parallelv2");

    if (debug) dump_vector(Y, MVLEN);

    // post-test
    del_matrix(M);
    del_vector(A);
    del_vector(Y);

  }
  hrulefill();
  { // gemm

    // data
    double * X = new_matrix(MMLEN, MMLEN);
    double * Y = new_matrix(MMLEN, MMLEN);
    double * Z = new_matrix(MMLEN, MMLEN);
    fill_matrix(X, MMLEN, MMLEN, 1.);
    fill_matrix(Y, MMLEN, MMLEN, 1.);
    fill_matrix(Z, MMLEN, MMLEN, 0.);
  
    if (debug) dump_matrix(X, MMLEN, MMLEN);
    if (debug) dump_matrix(Y, MMLEN, MMLEN);

    // serial
    gettimeofday(&tvs, NULL);
    dgemm_serial (X, Y, MMLEN, MMLEN, MMLEN, Z);
    gettimeofday(&tve, NULL);
    timediff (tvs, tve, "dgemm in serial");

    if (debug) dump_matrix(Z, MMLEN, MMLEN);

    // parallel
    gettimeofday(&tvs, NULL);
    dgemm_parallel (X, Y, MMLEN, MMLEN, MMLEN, Z);
    gettimeofday(&tve, NULL);
    timediff (tvs, tve, "dgemm in parallel");

    if (debug) dump_matrix(Z, MMLEN, MMLEN);

    // parallel v2
    gettimeofday(&tvs, NULL);
    dgemm_parallelv2 (X, Y, MMLEN, MMLEN, MMLEN, Z);
    gettimeofday(&tve, NULL);
    timediff (tvs, tve, "dgemm in parallelv2");

    if (debug) dump_matrix(Z, MMLEN, MMLEN);

    // post-test
    del_matrix(X);
    del_matrix(Y);
    del_matrix(Z);

  }
  hrulefill();
  { // convolution

    // data
    double * image = new_matrix(IMLEN, IMLEN);
    double * kernel = new_matrix(KLEN, KLEN);
    double * fmap = new_matrix(FLEN(IMLEN,KLEN), FLEN(IMLEN,KLEN));
    fill_matrix(image, IMLEN, IMLEN, 1.);
    fill_matrix(kernel, KLEN, KLEN, 1.);
    fill_matrix(fmap, FLEN(IMLEN,KLEN), FLEN(IMLEN,KLEN), 0.);

    if (debug) dump_matrix(image, IMLEN, IMLEN);
    if (debug) dump_matrix(kernel, KLEN, KLEN);

    // serial
    gettimeofday(&tvs, NULL);
    conv2_serial (image, kernel, IMLEN, KLEN, fmap);
    gettimeofday(&tve, NULL);
    timediff (tvs, tve, "conv2 in serial");

    if (debug) dump_matrix(fmap, FLEN(IMLEN,KLEN), FLEN(IMLEN,KLEN));

    // parallel
    gettimeofday(&tvs, NULL);
    conv2_parallel (image, kernel, IMLEN, KLEN, fmap);
    gettimeofday(&tve, NULL);
    timediff (tvs, tve, "conv2 in parallel");

    if (debug) dump_matrix(fmap, FLEN(IMLEN,KLEN), FLEN(IMLEN,KLEN));

    // post-test
    del_matrix(image);
    del_matrix(kernel);
    del_matrix(fmap);

  }
  hrulefill();

  // how long all the benchmarks take
  gettimeofday(&tvt, NULL);
  timediff(tvi, tvt, "All benchmark");

  return 0;
}
