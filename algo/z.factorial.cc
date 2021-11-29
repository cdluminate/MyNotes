/**
 * @file factorial.cc
 * @brief calculate factorial recursively.
 */
#include <iostream>
#include <unordered_map>
using namespace std;

long
factorial (long n)
{
	cout << "factorial(" << n << ")" << endl;
	return (n==0) ? 1 : n*factorial(n-1);
}

long
factorial_cached (long n)
{
	cout << "factorial_cached(" << n << ")" << endl;
	static std::unordered_map<long, long> cache;
	if (cache.find(n) == cache.end()) {
		long res = (n==0) ? 1 : n*factorial_cached(n-1);
		cache[n] = res;
		return res;
	} else {
		return cache.find(n)->second;
	}
}

int
main (void)
{
	cout << "factorial without cache" << endl;
	cout << factorial(13) << endl;
	cout << factorial(13) << endl;
	cout << factorial_cached(13) << endl;
	cout << factorial_cached(13) << endl;
	return 0;
}
