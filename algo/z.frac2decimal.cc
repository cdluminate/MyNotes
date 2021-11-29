#include <stdio.h>

void
frac2decimal(int a, int b, int c) // a/b
{
	int res = 0, rem = 0;
	printf("%d.", a/b);
	res = a/b; rem = a%b;
	for (int i = 0; i < c; i++) {
		rem *= 10;
		res = rem/b; rem = rem%b;
		res = (i!=c-1) ? res :
			(10*rem/b)>=5 ? res+1 : res;
		printf("%1d", res);
	}
	printf("\n");
	return;
}

int
main(void)
{
	frac2decimal(1, 6, 4);
	frac2decimal(1, 6, 5);
	return 0;
}
