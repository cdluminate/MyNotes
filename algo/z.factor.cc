#include <stdio.h>
#include <stdbool.h> // C99

long
factorial(long n)
{
	return (n==0)? 1 : n*factorial(n-1);
}

bool
isPrime(long n)
{
	for (long i = 2; i < n; i++)
		if (n%i == 0) return false;
	return true;
}

long
smallestPrimeFactor(long n)
{
	for (long i = 2; i < n; i++)
		if (isPrime(i) && n%i == 0) return i;
	return n; // This is prime number
}

void
factor(long n)
{
	if (!isPrime(n)) {
		long spf = smallestPrimeFactor(n);
		printf("%ld ", spf);
		factor(n / spf);
	} else {
		printf("%ld\n", n);
	}
	return;
}

int
main(void)
{
	factor(666);
	factor(factorial(5));
	factor(factorial(13));
	return 0;
}

// FIXME: overflow
