/* libkernel.c */

#ifdef __cplusplus
extern "C" {
#endif

#include <stdio.h>

/* interface */
int hello(void);
double dasum(double *, size_t);
double pdasum(double *, size_t);
void dvdump(double *, size_t);

/* implementation */
int
hello (void)
{
  return 0;
}

double
dasum(double * a, size_t n)
{
  double sum = .0;
  for (size_t i = 0; i < n; i++)
    sum += a[i]>0 ? a[i] : -a[i];
  return sum;
}

double
pdasum(double * a, size_t n)
{
  double sum = .0;
  size_t i = 0;
  #pragma omp parallel for reduction (+:sum)
  for (i = 0; i < n; i++)
    sum += a[i]>0 ? a[i] : -a[i];
  return sum;
}

void
dvdump(double * a, size_t n)
{
  for (size_t i = 0; i < n; i++)
    printf("%.2f ", a[i]);
  printf("\n");
  return;
}

#ifdef __cplusplus
}
#endif
