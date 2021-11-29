#include <stdio.h>
#include <string.h>
#include <ctype.h>

// average word length

int
main(void)
{
	char* s = (char*)"qwke asdl weas   asdk weas asdf ";

	// method 1
	int cl = 0, cr = 0;
	int wl = 0, wc = 0;
	while (cl < strlen(s)) {
		// scan a word each time
		while (!isalpha(s[cl]) && cl<strlen(s)) cl++; // cl then points to the first alpha
		if (cl >= strlen(s)) break;
		cr = cl; while (isalpha(s[cr]) && cr<strlen(s)) cr++; // cr at last alpha + 1
		wl += cr - cl; wc++;
		cl = cr;
	}
	printf("%d %d\n", wl, wc);

	// method 2
	int wl2 = 0, wc2 = 0;
	for (int i = 0; i < strlen(s); i++) {
		if (isalpha(s[i])) wl2++;
		//if (i < strlen(s)-1)
		//	if (!isalpha(s[i]) && isalpha(s[i+1])) wc2++;
		if (i > 0)
			if (isalpha(s[i]) && !isalpha(s[i+1])) wc2++;
	}
	printf("%d %d\n", wl2, wc2);

	return 0;
}
