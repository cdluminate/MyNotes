/* md5bin.c
   <cdluminate@gmail.com> / MIT licence
 */

#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/md5.h>

int
main (int argc, char **argv)
{
	char md[16];
	if (argc != 2)
		exit (1);
	MD5 ((unsigned char *)argv[1], strlen(argv[1]), (unsigned char *)md);
	write (1, md, 16);
	return 0;
}
