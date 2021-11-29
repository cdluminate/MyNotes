#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void
snake(int n)
{
	//int** m = (int**)malloc(sizeof(int)*n*n);
	//bzero((void*)m, sizeof(int)*n*n);
	int m[100][100];
	bzero((void*)m, sizeof(m));
	int cx = 0, cy = n-1; // current location
	int count = 0;

	m[cx][cy] = ++count;
	while (count < n*n) {
		while (cx < n-1 && !m[cx+1][cy]) m[++cx][cy] = ++count;
		while (cy > 0   && !m[cx][cy-1]) m[cx][--cy] = ++count;
		while (cx > 0   && !m[cx-1][cy]) m[--cx][cy] = ++count;
		while (cy < n-1 && !m[cx][cy+1]) m[cx][++cy] = ++count;
	}

	for (int i = 0; i < n; i++) {
		for (int j = 0; j < n; j++) {
			printf("%d ", m[i][j]);
		}
		printf("\n");
	}
	return;
}

int
main(void)
{
	snake(4);
	return 0;
}
