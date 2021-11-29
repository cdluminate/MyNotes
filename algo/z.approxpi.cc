#include <stdio.h>
#include <math.h>

// Don't do this with reduce&conquer, stack overflow!
//double
//pi_rq(int n, int sign)
//{
//	double item = 1. / n;
//	if (item < 1e-6) {
//		return sign*item;
//	} else {
//		return sign*item + pi_rq(n+2, -sign);
//	}
//}

double
pi_approx(void)
{
	double sum = 0.;
	// sum i=1 n ( (-1)^i-1 * 1/(2i-1) )
	for (int i = 1; ; i++) {
		double item = 1./i;
		double sign = i%2==1 ? 1. : -1.;
		sum += sign*item;
		if (item < 1e-6) break;
	}
	return sum;
}

int
main(void)
{
	printf("%lf\n", 4.*pi_approx());
	return 0;
}
