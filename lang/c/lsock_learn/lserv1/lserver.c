/* lserver.c

   Learning Socket Programming.
   this is the server end, it listens on 127.0.0.1:2333,
   and send a banner to clients.

   C.D.Luminate <cdluminate@gmail.com>
   2014/09/28
   */

#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <netdb.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define PORT 2333
#define BACKLOG 3
#define BANNER "BANNER! From the Server\n"

int Err(const char name[]) {
	perror (name);
	exit (EXIT_FAILURE);
}

int
main (int argc, char **argv)
{
	int debug = 1;

	time_t t_sec;
	int sock_fd;
	int new_fd;
	socklen_t addrlen;

	struct sockaddr_in serv_addr;
	struct sockaddr_in clie_addr;
	
	/* Make Socket */
	sock_fd = socket(AF_INET, SOCK_STREAM,
		getprotobyname("tcp")->p_proto);
	if (sock_fd == -1) {
		Err ("socket");
	}
	if (debug) fprintf (stderr, "[%ld] Socket created.\n", time(&t_sec));

	/* Fill sockaddr_in */
	memset (&serv_addr, 0, sizeof(struct sockaddr_in));
	serv_addr.sin_family = AF_INET;
	//serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	inet_pton (AF_INET, "127.0.0.1", &serv_addr.sin_addr);
	//serv_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
	serv_addr.sin_port = htons(PORT);
	
	/* Bind */
	if (bind(sock_fd, (struct sockaddr *)&serv_addr,
		sizeof(struct sockaddr)) == -1)
	{
		Err ("bind");
	}
	if (debug) fprintf (stderr, "[%ld] Bind success.\n", time(&t_sec));

	/* Listen */
	if (listen(sock_fd, BACKLOG) == -1) {
		Err ("listen");
	}
	if (debug) fprintf (stderr, "[%ld] Listen.\n", time(&t_sec));

	/* Standalone */
	addrlen = sizeof(struct sockaddr);
	do { 
		/* wait for a client,
		   once connected, send the BANNER to client and close
		   */
		new_fd = accept (sock_fd, (struct sockaddr *)&clie_addr, &addrlen);
		if (new_fd == -1) {
			Err ("accept");
		}
		if (debug) fprintf (stderr, "[%ld] Accept\n", time(&t_sec));
		fprintf (stderr, "[%ld] Get Connection from %s : %d\n",
			time(&t_sec),
			inet_ntoa(clie_addr.sin_addr),
			clie_addr.sin_port);
		if (write(new_fd, BANNER, sizeof(BANNER)) == -1) {
			Err ("write");
		}
		if (debug) fprintf (stderr, "[%ld] Banner sent, close\n", time(&t_sec));
		/* close the connection */
		close (new_fd);
	} while(1);

	close (sock_fd);

	fprintf (stderr, "[%ld] Exit.\n", time(&t_sec));
	return 0;
}
