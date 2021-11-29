#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void
swap(char* s, size_t idxa, size_t idxb)
{
	char tmp = s[idxa];
	s[idxa] = s[idxb];
	s[idxb] = tmp;
	return;
}

void
bsort(char* s, size_t sz, int descending)
{
	for (size_t i = 0; i < sz; i++) {
		for (size_t j = i+1; j < sz; j++) {
			if (descending) {
				if (s[i] < s[j]) swap(s, i, j);
			} else {
				if (s[i] > s[j]) swap(s, i, j);
			}
		}
	}
	return;
}

int
p6174_next(int x)
{
	char s[10];
	snprintf(s, 10, "%d", x);
	char lens = strlen(s);
	bsort(s, lens, 1);
	int high = atoi(s);
	bsort(s, lens, 0);
	int low = atoi(s);
	int res = high - low;
	return res;
}


int
main(void)
{
	//char buf[] = "192385";
	//puts(buf);
	//bsort(buf, strlen(buf), 0);
	//puts(buf);
	//bsort(buf, strlen(buf), 1);
	//puts(buf);

	int x = 1234;
	int xnext = p6174_next(x);
	printf("%d->%d", x, xnext);
	do {
		x = xnext;
		xnext = p6174_next(x);
		printf("->%d", xnext);
	} while (x != xnext);
	puts("");
	return 0;
}
