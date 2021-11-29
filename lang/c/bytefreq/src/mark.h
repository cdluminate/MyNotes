/* mark.h
 * data cruncher for Bytefreq, this is a part of bytefreq

   Count Byte/Char freqency, using Serial/Parallel Approaches.

   C.D.Luminate <cdluminate AT gmail DOT com> 
   MIT Licence, 2014
 */

/* indicates _type used only in this file */
#define CONTROL 1
#define SYMBOL  2
#define NUMBER  4
#define UPPER   8
#define LOWER   16
#define ALPHA   32
#define ALL     128

/* interfaces  */
int mark_control (int _mark[256]);
int mark_symbol (int _mark[256]);
int mark_number (int _mark[256]);
int mark_upper (int _mark[256]);
int mark_lower (int _mark[256]);
int mark_all (int _mark[256]);


/* core function, internally use */
int
_count_marker (int _type, int _mark[256])
{
/* the definition only used in following part of this file */
#define eqtype(j) (_type == (j)) /* equal to _type? */
/* end def */
	int _lo; /* loop */
	if (_type == ALL) {
		/* then set all marks as 1 and return */
		for (_lo = 0; _lo < 256; _lo++) {
			_mark[_lo] = 1;
		}
		return 256;
	}
	/* not all */
	for (_lo = 0; _lo < 256; _lo++) {
		switch (_lo) {
		/* the switch{} block used gcc extension */
		case 0 ... 31:
			if (eqtype(CONTROL)) _mark[_lo] = 1;
			break;
		case 32 ... 47:
			if (eqtype(SYMBOL)) _mark[_lo] = 1;
			break;
		case 48 ... 57:
			if (eqtype(NUMBER)) _mark[_lo] = 1;
			break;
		case 58 ... 64:
			if (eqtype(SYMBOL)) _mark[_lo] = 1;
			break;
		case 65 ... 90:
			if (eqtype(UPPER) || eqtype(ALPHA)) _mark[_lo] = 1;
			break;
		case 91 ... 96:
			if (eqtype(SYMBOL)) _mark[_lo] = 1;
			break;
		case 97 ... 122:
			if (eqtype(LOWER) || eqtype(ALPHA)) _mark[_lo] = 1;
			break;
		case 123 ... 126:
			if (eqtype(SYMBOL)) _mark[_lo] = 1;
			break;
		case 127:
			if (eqtype(CONTROL)) _mark[_lo] = 1;
			break;
		default:
			;
		}
	}
	return 0;
}

/* implement */
int mark_control (int _mark[256]) {
	return _count_marker (CONTROL, _mark);
}
int mark_symbol (int _mark[256]) {
	return _count_marker (SYMBOL, _mark);
}
int mark_number (int _mark[256]) {
	return _count_marker (NUMBER, _mark);
}
int mark_upper (int _mark[256]) {
	return _count_marker (UPPER, _mark);
}
int mark_lower (int _mark[256]) {
	return _count_marker (LOWER, _mark);
}
int mark_all (int _mark[256]) {
	return _count_marker (ALL, _mark);
}
