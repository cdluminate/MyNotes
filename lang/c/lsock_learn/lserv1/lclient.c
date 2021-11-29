/* lclient.c

   this is the client to lserver.c

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
#define BUFFER_SIZE 512

int Err (const char name[]) {
	perror (name);
	exit (EXIT_FAILURE);
}

int
main (int argc, char **argv)
{
//	int debug = 1;

	int sock_fd;
	char buffer[BUFFER_SIZE];

	struct sockaddr_in serv_addr;
	struct hostent * host;

	if (argc != 2) {
		exit (EXIT_FAILURE);
	}

	/* get host */
	host = gethostbyname (argv[1]);
	if (host == NULL) Err ("gethostbyname");
	
	/* Create Socket */
	sock_fd = socket (AF_INET, SOCK_STREAM,
			getprotobyname("tcp")->p_proto);
	if (sock_fd == -1) Err ("socket");

	/* fill sockaddr_in */
	memset (&serv_addr, 0, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr = *((struct in_addr *)host->h_addr);
	serv_addr.sin_port = htons(PORT);

	/* Connect */
	if (connect(sock_fd, (struct sockaddr *)&serv_addr, sizeof(struct sockaddr)) == -1) {
		Err ("connect");
	}

	/* Connect success */
	if (read(sock_fd, buffer, BUFFER_SIZE) == -1) {
		Err ("read");
	}
	buffer[511] = '\0';

	/* Print message from server */
	printf ("%s", buffer);

	close (sock_fd);

	return 0;
}


