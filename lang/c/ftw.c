#define _XOPEN_SOURCE 500
#define _GNU_SOURCE
#include <ftw.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

/* see manpage of ftw and nftw : File Tree Walk */

char* target;
int (*display_info) (const char *fpath, const struct stat *sb,
                     int typeflag, struct FTW *ftwbuf);

static int
_nftw_display_info_match(const char *fpath, const struct stat *sb,
             int tflag, struct FTW *ftwbuf)
{
	if (strcasestr(fpath, target) != (char*) NULL)
        printf("%7jd  %-40s\n", (intmax_t) sb->st_size, fpath);
    return 0;           /* To tell nftw() to continue */
}

static int
_nftw_display_info_nomatch(const char *fpath, const struct stat *sb,
             int tflag, struct FTW *ftwbuf)
{
	printf("%7jd  %-40s\n", (intmax_t) sb->st_size, fpath);
    return 0;           /* To tell nftw() to continue */
}
int
main(int argc, char *argv[])
{
    int flags = 0;

	if (argc > 1) {
        display_info = _nftw_display_info_match;
		target = argv[1];
	} else {
		display_info = _nftw_display_info_nomatch;
	}
	
    if (argc > 2 && strchr(argv[2], 'm') != NULL)
        flags |= FTW_MOUNT;
    if (argc > 2 && strchr(argv[2], 'p') != NULL)
        flags |= FTW_PHYS;

    if (nftw(".", display_info, 20, flags) == -1) {
        perror("nftw");
        exit(EXIT_FAILURE);
    }
    exit(EXIT_SUCCESS);
}
