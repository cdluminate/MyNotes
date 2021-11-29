/* wrapper.h
 * data cruncher for Bytefreq, this is a part of bytefreq

   Count Byte/Char freqency, using Serial/Parallel Approaches.

   C.D.Luminate <cdluminate AT gmail DOT com> 
   MIT Licence, 2014
*/

#ifndef Bytefreq_WRAPPER_H
#define Bytefreq_WRAPPER_H

#include <stdio.h>
#include <stdlib.h>

#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

/* NOTE : all functions in this file is wrapper function */

//        int socket(int domain, int type, int protocol);
int
Socket (int domain, int type, int protocol)
{
	int _ret;
	if ((_ret = socket(domain, type, protocol)) == -1){
		perror ("socket");
		exit (EXIT_FAILURE);
	}
	return _ret;
}

int 
Socketpair (int domain, int type, int protocol, int sv[2])
{
	int _ret;
	if ((_ret = socketpair (domain, type, protocol, sv)) == -1) {
		perror ("socketpair");
		exit (EXIT_FAILURE);
	}
	return _ret;
}

pid_t
Fork (void)
{
	pid_t _ret;
	if ((_ret = fork()) == -1) {
		perror ("fork");
		exit (EXIT_FAILURE);
	}
	return _ret;
}

int
Open (const char *pathname, int flags)
{
    int fd;
    if ((fd = open(pathname, flags)) < 0) {
        perror ("open");
        exit (EXIT_FAILURE);
    }
    return fd;
}

int
Close (int fd)
{
    int ret;
    if ((ret = close (fd)) == -1) {
        perror ("close");
        exit (EXIT_FAILURE);
    }
    return ret;
}

ssize_t
Read (int fd, void *buf, size_t count)
{
    ssize_t ssize;
    if ((ssize = read (fd, buf, count)) == -1) {
        perror ("read");
        exit (EXIT_FAILURE);
    }
    return ssize;
}

ssize_t
Write (int fd, const void *buf, size_t count)
{
    ssize_t ssize;
    if ((ssize = write (fd, buf, count)) == -1) {
        perror ("write");
        exit (EXIT_FAILURE);
    }
    return ssize;
}

void *
Malloc (size_t size) /* wrapper for malloc(3) */
{
	void *_ptr;
	if ((_ptr = malloc (size)) == NULL) {
		perror ("malloc");
		exit (EXIT_FAILURE);
	}
	return _ptr;
}

ssize_t
Sendfile(int out_fd, int in_fd, off_t *offset, size_t count)
{
	ssize_t _ = sendfile (out_fd, in_fd, offset, count);
	if (_ == -1) {
		perror ("sendfile");
		exit (EXIT_FAILURE);
	}
	return _;
}

#endif /* Bytefreq_WRAPPER_H */
