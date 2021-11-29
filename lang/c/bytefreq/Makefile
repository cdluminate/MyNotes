DESTDIR =
BIN = $(DESTDIR)/usr/bin

CC = /usr/bin/gcc
CFLAGS = -Wall -O1 -fopenmp

bytefreq: bytefreq.c
	$(CC) $(CFLAGS) -o bytefreq bytefreq.c
install: bytefreq
	install -m0755 bytefreq $(BIN)
uninstall:
	rm /usr/bin/bytefreq 
deb-pkg:
	dpkg-buildpackage -us -uc
	dh clean
	make clean
	
.PHONY : clean
clean:
	-rm bytefreq
#	if [ -e bytefreq ]; then\
#		rm bytefreq; \
#	fi
