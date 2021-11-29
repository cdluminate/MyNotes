/* print.h
 * this is a part of bytefreq

    Count Byte/Char freqency.
       
    C.D.Luminate <cdluminate AT gmail DOT com> 
    MIT Licence, 2014
 */

void
print_the_table_header ()
{
	fprintf (stdout,
"===========================================================\n"
"Character      Count           of_ALL          of_Specified\n"
"===========    ============    ============    ============\n");
	return;
}

void
print_entry (struct bytefreq bf, int loop, int use_percent_output)
{
	/* if not marked, skip */
	if (!(bf.mark[loop]))
		return;

	/* set color, according to max/min */
	if (bf.c[loop] == bf.ex.spec_max)
		fprintf (stdout, "\x1B[31m");
	if (bf.c[loop] == bf.ex.spec_min)
		fprintf (stdout, "\x1B[32m");

	/* print entry, and consider flag "dont_use_percent_output" */
	if (!use_percent_output)
		fprintf (stdout, "(0x%1$x, '%2$c')    %3$12ld    %5$12.8lf    %4$12.8lf\n", loop, loop,
			 bf.c[loop], (double)bf.c[loop]/bf.tot.total_spec,
			 (double)bf.c[loop]/bf.tot.total_byte);
	else
		fprintf (stdout, "(0x%1$x, '%2$c')    %3$12ld   %5$11.3lf %%   %4$11.3lf %%\n", loop, loop,
			 bf.c[loop], (double)100.0*bf.c[loop]/bf.tot.total_spec,
			 (double)100.0*bf.c[loop]/bf.tot.total_byte);

	/* restore color to default */
	fprintf (stdout, "\x1B[m");
	return;
}

void
print_summary (struct bytefreq bf, long total_read)
{
	fprintf (stdout, "Maximous of specified : (0x%X  '%c') : \x1B[33m%ld\x1B[m\n",
		 bf.ex.spec_max_char, bf.ex.spec_max_char, bf.ex.spec_max);
	fprintf (stdout, "Minimous of specified : (0x%X, '%c') : \x1B[33m%ld\x1B[m\n",
		 bf.ex.spec_min_char, bf.ex.spec_min_char, bf.ex.spec_min);
	fprintf (stdout, "The Math Expectation  : (0x%X, '%c', dec \x1B[33m%d\x1B[m)\n",
		 (char)find_expection(bf.c), (char)find_expection(bf.c), find_expection(bf.c));
	fprintf (stdout, "Total bytes specified : \x1B[33m%ld, %.3lf%%\x1B[m\n",
	 	 bf.tot.total_spec,
		 (double)100.0*bf.tot.total_spec/bf.tot.total_byte);
	fprintf (stdout, "Total bytes read()    : \x1B[33m%ld\x1B[m\n",
	         total_read);
	return;
}
