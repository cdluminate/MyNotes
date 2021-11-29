/* struct.h
 * this is a part of bytefreq

    Count Byte/Char freqency.
       
    C.D.Luminate <cdluminate AT gmail DOT com> 
    MIT Licence, 2014
 */

/* === sub structures === */
struct bytefreq_tot {
	/* store total values */
	long total_spec;
	long total_byte;
} ;

struct bytefreq_ex {
	/* store the extreme values */
	long spec_max;
	long spec_min;
	long byte_max;
	long byte_min;
	char spec_max_char;
	char spec_min_char;
	char byte_max_char;
	char byte_min_char;
} ;


/* === master structure ===*/
struct bytefreq {
	/* raw counter */
	long c[256];
	/* mark */
	int mark[256];
	/* deal with raw data */
	long control;
	long symbol;
	long number;
	long upper;
	long lower;
	/* cooked data */
	long visible;
	long invisible;
	long alpha;
	struct bytefreq_tot tot;
	struct bytefreq_ex ex;
} bf; /* bf, the master structure */
