/*
   lsock.h

   deal with some functions  */

#include <netinet/in.h>
#include <netinet/tcp.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

#include <signal.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/time.h>
#include <sys/select.h>
#include <fcntl.h>

//int socket(int domain, int type, int protocol);
int
Socket (int domain, int type, int protocol)
{
	int _lsock;
	_lsock = socket (domain, type, protocol);
	if (_lsock == -1) {
		perror ("socket");
		exit (EXIT_FAILURE);
	}
	return _lsock;
}

//int bind(int sockfd, const struct sockaddr *addr,
//         socklen_t addrlen);
int
Bind (int sockfd, const struct sockaddr *addr,
	  socklen_t addrlen)
{
	int _lbind;
	_lbind = bind (sockfd, addr, addrlen);
	if (_lbind == -1) {
		perror ("bind");
		exit (EXIT_FAILURE);
	}
	return _lbind;
}

//int listen(int sockfd, int backlog);
int
Listen (int sockfd, int backlog)
{
	int _llist;
	_llist = listen (sockfd, backlog);
	if (_llist == -1) {
		perror ("listen");
		exit (EXIT_FAILURE);
	}
	return _llist;
}

//int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
int
Accept (int sockfd, struct sockaddr *addr, socklen_t *addrlen)
{
	int _lacce;
	_lacce = accept (sockfd, addr, addrlen);
	if (_lacce == -1) {
		perror ("accept");
		exit (EXIT_FAILURE);
	}
	return _lacce;
}

//pid_t fork(void);
pid_t
Fork (void)
{
	pid_t _lfork;
	_lfork = fork();
	if (_lfork == -1) {
		perror ("fork");
		exit (EXIT_FAILURE);
	}
	return _lfork;
}

//int close(int fd);
int
Close (int fd)
{
	int _lclose;
	_lclose = close (fd);
	if (_lclose == -1) {
		perror ("close");
		exit (EXIT_FAILURE);
	}
	return _lclose;
}

//int connect(int sockfd, const struct sockaddr *addr,
//                   socklen_t addrlen);
int
Connect (int sockfd, const struct sockaddr *addr,
	 socklen_t addrlen)
{
	int _lconn;
	_lconn = connect (sockfd, addr, addrlen);
	if (_lconn == -1) {
		perror ("connect");
		exit (EXIT_FAILURE);
	}
	return _lconn;
}
