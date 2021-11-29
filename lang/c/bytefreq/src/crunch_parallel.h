long
crunch_parallel (int _fd, long _counter[256], int _verbose)
{
	/* the value to return */
	long _total_read = 0;

	/* stat */
	struct stat st;
	bzero (&st, sizeof(st));
	fstat (_fd, &st);

	/* flush counter */
	bzero (_counter, 256*sizeof(long));

	/* allocate buffer and flush it */
	char *_buf = (char *)Malloc (BF_BFSZ_PARA);
	bzero (_buf, BF_BFSZ_PARA);

	/* start crunching */
	if (_verbose) BSDbar_init ();
	int _loop;
	long _readn;
	while ((_readn = Read(_fd, _buf, BF_BFSZ_PARA)) > 0) {
		if (_verbose) BSDbar_refresh (100*_total_read/st.st_size);
		_total_read += _readn;
		#pragma omp parallel for
		for (_loop = 0; _loop < _readn; _loop++) {
			_counter[(unsigned char)*(_buf+_loop)]++;
		}
	}
	if (_verbose) BSDbar_clear();

	/* free buffer and return */
	free (_buf);
	return _total_read;
}
