#include <stdio.h>

long
factorial(long n)
{
	return (n == 0 || n == 1) ? 1 : n * factorial(n-1);
}

long
combinations(long m, long n) // m <= n
{
	return factorial(n)/(factorial(m)*factorial(n-m));
}

int
main(void)
{
	printf("%ld\n", combinations(1, 20));
	return 0;
}
