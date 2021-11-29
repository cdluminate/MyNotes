#include <iostream>
#include <cmath>
using namespace std;

/* Assume that A = x * y = 24
 *                 1  24
 *                 2  12
 *                 .. .. 
 *                 12  2
 *                 24  1
 * to recude unnecessary computation,
 * we just test the range [0, int(sqrt(n))] inclusive.
 */

bool
isPrime(int n) {
	if (n <= 1) return false;
	for (int i = 2; i <= sqrt(n); i++) {
		if (n % i == 0) return false;
	}
	return true;
}

int
main(void)
{
	for (auto i : {0, 1, 2, 3, 4, 5, 7, 10, 17, 37, 64}) {
		cout << i << " : " << (isPrime(i) ? "true" : "false") << endl;
	}
	return 0;
}
