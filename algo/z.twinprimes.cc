#include <stdio.h>

#define dbg 1

// do not pass a large number to it
int
isPrime(int n)
{
	// assume that n > 0
	//for (int i = 2; i < n-1; i++) {
	if (n == 1) return 0;
	for (int i = 2; 2*i <= n; i++) {
		if (n % i == 0) return 0;
	}
	//if (dbg) printf("%d is prime\n", n);
	return 1;
}

int
isTwinPrimes(int n)
{
	// if n & n+2 are twin primes
	return (isPrime(n) && isPrime(n+2));
}

int
getMaxTwinPrimes(int m)
{
	// m \in [5,10000]
	for (int i = m-2; i > 4; i--) {
		//if (dbg) printf("testing %d %d\n", i, i+2);
		if (isTwinPrimes(i)) {
			printf("%d %d\n", i, i+2);
			return 0;
		}
	}
	return 0;
}

int
main(void)
{
	getMaxTwinPrimes(20);
	getMaxTwinPrimes(1000);
	return 0;
}
