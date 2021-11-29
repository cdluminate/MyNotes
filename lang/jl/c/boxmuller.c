/* Generating Gaussian-distributed random numbers */
/*
  @reference https://en.wikipedia.org/wiki/Box%E2%80%93Muller_transform#Implementation
  @reference http://www.zhihu.com/question/29971598#answer-17169006
  @reference http://mathworld.wolfram.com/Box-MullerTransformation.html
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

/* interface */

double * boxmuller(double *, size_t);

/* impl */
double *
boxmuller (double * a, size_t n)
{
  /* Box-Muller Gassian distributed random number generator
     $$ z_1 = \sqrt{-2 \ln x_1 } \cos( 2\pi x_2 ) $$
     $$ z_2 = \sqrt{-2 \ln x_1 } \sin( 2\pi x_2 ) $$
   */
  #define PI 3.1415926535897932384
  #define drand(void) (1.0-((double)rand()/(double)RAND_MAX)) // (0, 1]

  srand(clock());
  for (size_t i = 0; i < n; i+=2) {
    double u1 = drand();
    double u2 = drand();
    double r  = sqrt(-2.0 * log(u1));
    double theta = 2.0 * PI * u2;
    a[i] = r * cos(theta); // z0
    if (i+1<n) a[i+1] = r * sin(theta); // z1
  }
  return a;
}
