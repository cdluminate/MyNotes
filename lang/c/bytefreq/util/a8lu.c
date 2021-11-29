/* a8freq :: a8lu.c
 *      l(ower)u(pper)
 * 	convert alphabets between upper and lower case.
 *
 * Author : C.D.Luminate 
 * 	< cdluminate AT gmail DOT com >
 *	started at 02 / 06 /2014
 *
 * https://github.com/CDLuminate/a8freq
 * LICENCE : MIT
 */

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

void Usage (char *prog_name)
{
	fprintf (stderr, "\
Usage : %s [-hr] [FILE]\n\
Convert alphabets between upper and lower case\n\
If FILE not specified, stdin will be used.\n\
       -h    print this help message.\n\
       -r    reverse converting, upper to lower.\n",
       		 prog_name);
}


int
main (int argc, char *argv[])
{
	FILE *in_file = stdin;
	FILE *out_file = stdout;

	/* defalut is lower to upper, revflag is reverse_flag */
	int revflag = 0;

	/* used by getopt() */
	int opt;

	/* buffer */
	register int buf = 0;

	while ((opt = getopt (argc, argv, "hr")) != -1) {
		switch (opt) {
			case 'h':
				/* help */
				Usage (argv[0]);
				exit (EXIT_SUCCESS);
				break;
			case 'r':
				/* reverse, namely upper to lower */
				revflag = 1;
				break;
			default:
				/* out of exception */
				Usage (argv[0]);
				exit (EXIT_FAILURE);
				break;
		}
	}

	/* tell if a FILE is specified */
	if (optind < argc) {
		if ((in_file = fopen (argv[optind], "r")) == NULL) {
			perror ("fopen");
			exit (EXIT_FAILURE);
		}
	}

	/* change case, the core part */
	while ( (buf = fgetc (in_file)) != EOF && !feof(in_file)) {
		/* change case according to revflag */
		switch (buf) {
			case 'a' ... 'z':
				if (!revflag) buf -= 32;
				break;
			case 'A' ... 'Z':
				if (revflag) buf += 32;
				break;
			default:
				break;
		}
		
		fputc (buf, out_file);
	}

	fclose (in_file);
	fclose (out_file);
	return 0;
}
