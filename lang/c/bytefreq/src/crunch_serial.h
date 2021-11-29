long
crunch_serial (int _fd, long _counter[256], int _verbose)
{
	/* stat */
	struct stat st;
	bzero (&st, sizeof(st));
	fstat (_fd, &st);

	/* the value to return */
	long _total_read = 0;

	/* flush counter */
	bzero (_counter, 256*sizeof(long));

	/* allocate buffer and flush it */
	char *_buf;
	_buf = (char *)Malloc (BF_BFSZ_SERI);
	if (_buf == NULL) exit (1);
	bzero (_buf, BF_BFSZ_SERI);

	/* start crunching */
	int _loop;
	long _readn;
	if (_verbose) BSDbar_init ();
	while ((_readn = Read(_fd, _buf, BF_BFSZ_SERI)) > 0) {
		if (_verbose) {
			BSDbar_refresh ((int)(1.0+100.0*((float)_total_read/st.st_size)));
		}
		_total_read += _readn;
		/* #pragma omp parallel for */
		for (_loop = 0; _loop < _readn; _loop++) {
			_counter[(unsigned char)*(_buf+_loop)]++;
		}
	}
	if (_verbose) BSDbar_clear ();

	/* free buffer and return */
	free (_buf);
	return _total_read;
}
