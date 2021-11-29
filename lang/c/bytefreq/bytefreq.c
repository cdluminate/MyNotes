/* bytefreq.c

   Count Byte/Char freqency, using Serial/Parallel Approaches.

   C.D.Luminate <cdluminate AT gmail DOT com> 
   MIT Licence, 2014
 */

// TODO : -S option does not accept 0x?? hex number (atoi)
/* FIXME : long int overflow issue . */

#define BYTEFREQ_VERSION "Version: 2.4 (2014/12/23)\n"

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>

#include <sys/stat.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <sys/sendfile.h>

#include <omp.h>

#include "src/wrapper.h"
#include "src/bsdbar.h"

#include "src/crunch.h"
#include "src/mark.h"
#include "src/struct.h"
#include "src/find.h"
#include "src/print.h"

/* ===BEGIN HELP MESSAGE============================ */
void Usage (char *pname)
{
	fprintf (stderr,
"Usage:\n"
"  %s [options] [FILE]\n"
"Description:\n"
"  Count Byte/Char frequency.\n"
"  Only shows Total read size if no char specified.\n"
"  If given no <FILE>, it would read from the stdin.\n"
"Options:\n"
"  -h     show this help message\n"
"  -V     show version info\n"
"  -v     verbose mode\n"
"  -D     debug mode (> -v)\n"
"  -f     use float instead of percent output\n"
"\n"
"  -p     use parallel approach\n"
"  -U     use UNIX socket apprach (sendfile)\n"
"\n"
"  -A     specify all bytes to count\n"
"  -l     specify lower to count\n"
"  -u     specify upper to count\n"
"  -s     specify symbol to count\n"
"  -c     specify control character to count\n"
"  -a     specify alphabets to count (= '-lu')\n"
"  -S <N> specify the byte N (decimal)\n"
"  ...\n"
"For more info see -v\n", pname);
}

void Version (void)
{
	fprintf (stderr,
BYTEFREQ_VERSION
"Author: C.D.Luminate / MIT Licence / 2014\n");
}
/* ===END HELP MESSAGE============================== */

long total_read; /* apart from struct bytefreq */

int fd; /* for open */
int loop; /* var for loop */

/* flags */
int use_percent_output = 1; /* set to 1 as default, 0 to cancel */
int use_stdin;
int use_verbose;

/* use getopt() */
void bf_parse_option (int argc, char **argv);
/* used to select a crunch_* function */
long (* Crunch)(int _fd, long _counter[256], int _verbose);

/* MAIN */
int
main (int argc, char **argv)
{
	/* Serial one as default, use -p to switch to parallel */
	Crunch = crunch_serial; /* see include/crunch.h */
	/* clear structure */
	bzero (&bf, sizeof(bf));
    /* parse options and set flags itself */
    bf_parse_option (argc, argv);

	/* open file, then pass the fd to Crunch() */
	if (!use_stdin) 
		fd = Open (argv[optind], O_RDONLY);
	/* hint if no char is marked */
	if (find_mark_set (bf.mark) == 0) {
		fprintf (stderr, "HINT: see -h to find out more options.\n");
	}

	/* optimize I/O */
	posix_fadvise (fd, 0, 0, POSIX_FADV_SEQUENTIAL);

	/* =======Start Crunch=========== */
	if (use_verbose) fputs ("\x1B[mCrunching data ...\n", stderr);
	total_read = Crunch (fd, bf.c, use_verbose);

	/* find minmax */
	find_byte_extreme (&(bf.ex), bf.c);
	find_spec_extreme (&(bf.ex), bf.mark, bf.c);
	find_total (&(bf.tot), bf.mark, bf.c);

	/* #### print table #### */
	fprintf (stdout, "\x1B[m"); /* restore color */
	print_the_table_header ();

	/* print info about specified chars */
	for (loop = 0; loop < 256; loop++) {
		print_entry (bf, loop, use_percent_output);	
	}

	print_summary (bf, total_read);
	return 0;
}

void
bf_parse_option (int argc, char **argv)
{
    /* parse option */
    int opt = 0; /* for getopt() */

	while ((opt = getopt(argc, argv, "hVpulAasnfvcS:UD")) != -1) {
		switch (opt) {
		case 'p': /* use parallel */
			Crunch = crunch_parallel;
			break;
		case 'h': /* help */
			Usage (argv[0]);
			exit (EXIT_SUCCESS);
			break;
		case 'V': /* version info */
			Version ();
			exit (EXIT_SUCCESS);
			break;
		case 'v': /* verbose mode */
			use_verbose = 1;
			break;
		case 'D': /* debug mode */
			use_verbose = 2;
			break;
		case 'c': /* control */
			mark_control (bf.mark);
			break;
		case 'u': /* upper */
			mark_upper (bf.mark);
			break;
		case 'l': /* lower */
			mark_lower (bf.mark);
			break;
		case 'A': /* all */
			mark_all (bf.mark);
			break;
		case 'a': /* alphabets, i.e. upper && lower */
			mark_lower (bf.mark);
			mark_upper (bf.mark);
			break;
		case 's': /* symbol */
			mark_symbol (bf.mark);
			break;
		case 'n': /* number */
			mark_number (bf.mark);
			break;
		case 'f': /* don't use percent output */
			use_percent_output = 0;
			break;
		case 'S': /* specify a byte (decimal) to count */
			if (atoi(optarg) > 255 || atoi(optarg) < 0) {
				fprintf (stderr, "%s: Specified an invalid byte.\n", argv[0]);
				exit (EXIT_FAILURE);
			}
			bf.mark[(unsigned int)atoi(optarg)] = 1;
			break;
		case 'U': /* use crunch_unixsock */
			Crunch = crunch_unixsock;
			break;
		default:
			Usage (argv[0]);
			exit (EXIT_FAILURE);
		}
	}
	/* see if user want to use stdin */
	if (optind >= argc) {
		use_stdin = 1;
		fd = fileno(stdin);
	}
    return;
}
