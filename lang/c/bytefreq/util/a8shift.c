/* a8freq :: a8shift.c
 * 	Shift alphabets by (+/-)N positions.
 * 	A very simple way of encryption.
 *
 * Author : C.D.Luminate
 * 	< CDLuminate AT gmail DOT com >
 * 
 * https://github.com/CDLuminate/a8freq
 * LICENCE : MIT
 */

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

/* Usage()
 * display help message */
void Usage (char *prog_name)
{
	fprintf (stderr,"\
Usage : %s [-o OFFSET] [FILE]\n\
Offset alphabets by OFFSET positions.(which is 0 if not specified)\n\
options :\n\
    -o OFFSET	set OFFSET value(int), negative avaliable.\n\
    -h 		show this help info\n",
   		 prog_name);
}

/* MAIN */
int
main (int argc, char **argv)
{
	/* buffer */
	register int buf;

	/* */
	int offset = 0;

	/* the default input file should be stdin,
	 *	if FILE is not specified.
	 */
	FILE *in_file = stdin;

	/* FIXME : how to append action to file itself ? */
	FILE *out_file = stdout;

	/* int opt is used by getopt() */
	int opt;
	while ((opt = getopt (argc, argv, "ho:f:")) != -1) {
		switch (opt) {
			case 'h':
				/*help*/
				Usage (argv[0]);
				exit (EXIT_SUCCESS);
				break;
			case 'o':
				/* config offset */
				offset = atoi (optarg);
				break;
			default: 
				/* out of exception */
				Usage (argv[0]);
				exit (EXIT_FAILURE);
				break;
		}
	}

	/* tell if FILE is specified */
        if (optind < argc) {
                if ((in_file = fopen (argv[optind], "r")) == NULL) {
                        perror ("fopen");
                        exit(EXIT_FAILURE);
                }
        }


	/* main part */
	while ((buf = fgetc (in_file)) != EOF && !feof(in_file)) {
		switch (buf) {
			case 'a' ... 'z':
				buf = buf + offset % 26;
				if (buf > 'z') buf -= 26;
				if (buf < 'a') buf += 26;
				break;
			case 'A' ... 'Z':
				buf = buf + offset % 26;
				if (buf > 'Z') buf -= 26;
				if (buf < 'A') buf += 26;
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
