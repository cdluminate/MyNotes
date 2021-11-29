#include <stdio.h>

//t = 100:333;
//t2 = 2*t;
//t3 = 3*t;
//needle = int8(mod(t,1000)/100) + int8(mod(t,100)/10) +
// int8(mod(t,10)) + int8(mod(t2,1000)/100) + int8(mod(t2,100)/10) +
// int8(mod(t2,10)) + int8(mod(t3,1000)/100) + int8(mod(t3,100)/10) + int8(mod(t3,10));
//needle == 45

int
sumofdigits(int x) // x \in [100, 333]
{
	int s = 0;
	//printf("-> %d", x);
	x %= 1000;
	s += x/100; x%=100;
	s += x/10;  x%=10;
	s += x;
	//printf(" , %d\n", s);
	return s;
}
int (*s)(int) = sumofdigits;

int
main(void)
{
	for (int i = 100; i <= 333; i++) {
		if (45 == sumofdigits(i) + sumofdigits(2*i) + sumofdigits(3*i)) {
			//printf("%d %d %d\n", i, 2*i, 3*i);
			printf("=> i = %d, 2i = %d, 3i = %d, xsum = %d\n", i, 2*i, 3*i, s(i) + s(2*i) + s(3*i));
		}
	}
	return 0;
}
