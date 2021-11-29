/* find.h
 * this is a part of bytefreq

    Count Byte/Char freqency.
       
    C.D.Luminate <cdluminate AT gmail DOT com> 
    MIT Licence, 2014
 */

/* def */
int find_mark_set (int _mark[256]);
void find_spec_extreme (struct bytefreq_ex *_ex, int _mark[256], long _counter[256]);
void find_byte_extreme (struct bytefreq_ex *_ex, long _counter[256]);
void find_total (struct bytefreq_tot *_tot, int _mark[256], long _counter[256]);
int find_expection (long _counter[256]);
/* end def */

/* -------------------------------------------------------------------------- */
int
find_mark_set (int _mark[256])
{
	int ret = 0;
	/* if no mark is set, return 1 (true), or return 0(false) */
	int _lo;
	for (_lo = 0; _lo < 256; _lo++) {
		if (_mark[_lo] > 0) ret++;
	}
	return ret;
}

void
find_byte_extreme (struct bytefreq_ex *_ex, long _counter[256])
{
	int _lo;
	long _max = 0;
	long _min = 0;
	char _maxc = 0;
	char _minc = 0;

	for (_lo = 0; _lo < 256; _lo++) {
		if (_counter[_lo] > _max) {
			_max = _counter[_lo];
			_maxc = (char)_lo;
		}
	}
	_min = _max; /* important ! */
	for (_lo = 0; _lo < 256; _lo++) {
		if (_counter[_lo] < _min) {
			_min = _counter[_lo];
			_minc = (char)_lo;
		}
	}

	_ex -> byte_max = _max;
	_ex -> byte_min = _min;
	_ex -> byte_max_char = _maxc;
	_ex -> byte_min_char = _minc;
	return;
}

void
find_spec_extreme (struct bytefreq_ex *_ex, int _mark[256], long _counter[256])
{
	int _lo;
	long _max = 0;
	long _min;
	char _maxc = 0;
	char _minc = 0;

	for (_lo = 0; _lo < 256; _lo++) {
		if (_counter[_lo] > _max && _mark[_lo])
		{
			_max = _counter[_lo];
			_maxc = (char)_lo;
		}
	}
	_min = _max; /* important ! */
	for (_lo = 0; _lo < 256; _lo++) {
		if (_counter[_lo] < _min && _mark[_lo]) {
			_min = _counter[_lo];
			_minc = (char)_lo;
		}
	}

	_ex -> spec_max = _max;
	_ex -> spec_min = _min;
	_ex -> spec_max_char = _maxc;
	_ex -> spec_min_char = _minc;
	return;
}

void
find_total (struct bytefreq_tot *_tot, int _mark[256], long _counter[256])
{
	int _lo;
	for (_lo = 0; _lo < 256; _lo++) {
		_tot -> total_byte += _counter[_lo];
		if (_mark[_lo])
			_tot -> total_spec += _counter[_lo];
	}
	return;
}

int
find_expection (long _counter[256])
{
	/* calculate the mathematical expection char among the whole counter array */
	long _tot = 0;
	long _cxn = 0;
	int _t;
        for (_t = 0; _t < 256; _t++) {
               _tot += _counter[_t];
               _cxn += _counter[_t] * _t;
        }
        return (int)(_cxn/_tot);
}

