#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define PASS "word"

void guard (void);
int GameLoop (void);

int
main (void)
{
	guard();
	GameLoop ();

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

int
GameLoop (void)
{
	printf ("welcome\n");
	char buffer[1024];
	while (read(0, buffer, 1024) > 0) {
		write (1, buffer, strlen(buffer));
		memset (buffer, 0x00, 1024);
	}
	return 0;
}
