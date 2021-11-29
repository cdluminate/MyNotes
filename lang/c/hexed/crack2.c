#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PASS "word"

void guard (void);

int
main (void)
{
	guard();
	printf ("this is the main function\n");

	return 0;
}

void
guard (void)
{
	char buffer[256];
	bzero (buffer, 256);
	int n;

	fgets (buffer, 255, stdin);
	n = strncmp (PASS, buffer, 4);
	if (n == 0) {
		printf ("Success, Welcome!\n");
	} else {
		printf ("REJECT\n");
		exit (-1);
	}
}
