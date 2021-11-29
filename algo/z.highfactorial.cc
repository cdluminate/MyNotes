// high-precision factorial

#include <stdio.h>
#include <string.h>

int d[3000];

int
main(void)
{
	int n = 30;
	bzero(d, 3000*sizeof(__typeof__(d[0])));
	d[0] = 1;
	for (int i = 2; i <= n; i++) {
		int c = 0;
		for (int j = 0; j < 3000; j++) {
			int s = d[j] * i + c;
			d[j] = s % 10;
			c = s / 10;
		}
	}
	for (int j=3000-1; j >= 0; j--) if (d[j]) {
		for (int i = j; i >= 0; i--) printf("%d", d[i]);
		break;
	}
	printf("\n");
	return 0;
}
