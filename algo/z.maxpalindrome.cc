#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int
isPalindrome(char* s, int begin, int end)
{
	if (begin > end) return -1;
	while (begin < end) {
		if (s[begin] != s[end]) return 0;
		begin++; end--;
	}
	return 1;
}

void
strLower(char* s, size_t sz)
{
	for (size_t i = 0; i < sz; i++)
		s[i] = tolower((unsigned char)(s[i]));
}

void
maxPalindrome(char *s, size_t sz)
{
	int maxlen = 0, maxi = 0, maxj = 0;
	for (int i = 0; i < sz; i++) {
		for (int j = i; j < sz; j++) {
			if (isPalindrome(s, i, j)) {
				int len = j-i+1;
				if (len > maxlen) {
					maxlen = len;
					maxi = i;
					maxj = j;
				}
			}
		}
	}
	printf("orig str: %s\n", s);
	printf("longest palindrome: ");
	for (int k = maxi; k <= maxj; k++) {
		putchar(s[k]);
	}
	putchar('\n');
}

void
findPalindrome(char *s, size_t sz, size_t curl, size_t curr, int* maxlen, int* maxi, int* maxj)
{
	while (curl > 0 && curr < sz) {
		if (s[curl] != s[curr]) break;
		printf("-> curl %ld [%c], curr %ld [%c], maxlen %d\n", curl, s[curl], curr, s[curr], *maxlen);
		if (curr-curl+1 > *maxlen) {
			*maxlen = curr-curl+1;
			*maxi = curl; *maxj = curr;
		}
		curl--; curr++;
	}
}

void
maxPalindrome2(char *s, size_t sz)
{
	int maxlen = 0, maxi = 0, maxj = 0;
	for (size_t i = 0; i < sz; i++) {
		// odd number as palindrome length
		findPalindrome(s, sz, i-1, i+1, &maxlen, &maxi, &maxj);
		// even number as palindrome length
		findPalindrome(s, sz, i-1, i, &maxlen, &maxi, &maxj);
	}
	printf("orig str: %s\n", s);
	printf("longest palindrome: ");
	for (int k = maxi; k <= maxj; k++) {
		putchar(s[k]);
	}
	putchar('\n');
}

int
main(void)
{
	//char* buffer = "Confuciuss say: Madam, I'm Adam.";
	// this will cause failure because the string will be put to the
	// .rodata section, generate assembly with gcc -S to inspect this.
	char buffer[] = "Confuciuss say: Madam, I'm Adam.";
	strLower(buffer, strlen(buffer));

	maxPalindrome(buffer, strlen(buffer));
	maxPalindrome2(buffer, strlen(buffer));

	return 0;
}
