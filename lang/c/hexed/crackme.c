#include <stdio.h>
#include <string.h>

#define PASS "word"

int
main (void)
{
	char buffer[256];
	bzero (buffer, 256);

	int n;

	fgets (buffer, 255, stdin);
	n = strncmp (PASS, buffer, 4);
	if (n == 0) {
		printf ("Success", n);
	} else {
		printf ("REJECT", n);
	}

	return 0;
}
