/* lserv2.c

   lumin's server 2, which implements sort of server/client model.

   This is a test code, the author is reading
   <<UNIX Network Programming : Socket API>>

   C.D.Luminate <cdluminate@gmail.com>
   2014/10/{03,04} */
/* TODO : some times it behaves strangely,
   e.g. if I type PASS pass first, then USER user,
   	the auth process will not go, but some former version
	of me will do. */
/* ISSUE : the signal() function is not POSIX standard,
   	   should use POSIX sigaction() instead. */

/* lsock.h */
#include "lsock.h"

/* settings */
//#define LSOCK_USE_IPv4
#define LSOCK_USE_IPv6

#define BANNER "Sort_of_Server2 :: Please input your instructions.\n"
#define BYE_MSG "From Server : BYE\n\0\0"
#define HTML "<html>It works!</html>\n"

#define SECRET "++ This is the secret information for authed user\n"
#define SEC_FAIL "++ not permitted, REJECT\n"

/* ---------- vars -------------*/
/* debug flag */
int debug = 1;

/* general socket related vars */
int listenfd;
int connfd;
#ifdef LSOCK_USE_IPv4
struct sockaddr_in clie_addr;
struct sockaddr_in serv_addr;
#else
struct sockaddr_in6 clie_addr;
struct sockaddr_in6 serv_addr;
#endif
socklen_t cli_len;
pid_t c_pid;
int port = 2333; /* local listen port, 2333 default */

/* remote and server information */
char raddr[128];		//remote addr 
unsigned short rport = 0;	//remote port
char saddr[128];		//server addr
unsigned short sport = 0;	//server port

/* instruction buffer */
char inst[1024];
/* feed back buffer */
char feed[1024];
/* store parsed instruction */
char argv0[1024];
char argv1[1024];
/* readn : store return value of read() */
int readn = 0;
int opt;

/* more functions */
/* authentication */
	/* auth_state , >0 means login, <=0 not login */
int auth_st = -1; 
char auth_user[8];
char auth_pass[8];
char true_user[8]; /* max user and pass length is 4 */
char true_pass[8];

/* -------------functions ----------*/
/* service things */
int do_serv (FILE *fp, int connfd);
/* parse instruction from client */
int inst_parse (const char *src, char *argv0, char *argv1);
/* signal SIGINT */
void do_sigint (int sig);
void do_sigchld (int sig) {
	pid_t _pid;
	int _stat;
	_pid = wait(&_stat);
	printf ("[31m*[m child %d terminated\n", _pid);
	return;
}
/* flush socket related info */
int flush_sock_re (void)
{
	bzero (raddr, sizeof(raddr));
	bzero (saddr, sizeof(saddr));
	bzero (&serv_addr, sizeof(serv_addr));
	bzero (&clie_addr, sizeof(clie_addr));
	return 0;
}
/* flush buffer */
int flush_buf (void)
{
	bzero (inst, sizeof(inst));
	bzero (feed, sizeof(feed));
	bzero (argv0, sizeof(argv0));
	bzero (argv1, sizeof(argv1));
	return 0;
}
/* flush authentication info */
int flush_auth (void)
{
	bzero (auth_pass, sizeof(auth_pass));
	bzero (auth_user, sizeof(auth_user));
	return 0;
}
/* auth core */
int authenticate (int *state, const char *user, const char *pass);
/* judge if to auth and do auth matter */
int auto_auth (void);
/* read configuration, user and pass */
int readconf (const char *_file, char *_buffer)
{
	int _fd;
	if ((_fd = open (_file, O_RDONLY)) == -1) {
		perror ("open");
		exit (EXIT_FAILURE);
	}
	read (_fd, _buffer, 4);
	Close (_fd);
	return 0;
}

/* =========== main ================= */	
int
main (int argc, char **argv)
{
	/* parse option */
	while ((opt = getopt(argc, argv, "p:")) != -1) {
		switch (opt) {
		case 'p':
			port = atoi(optarg);
			if (port > 65535 || port < 0) {
				printf ("Invalid Port Number\n");
				exit (EXIT_FAILURE);
			}
			break;
		default:
			printf ("Unkown Option\n");
			exit (EXIT_FAILURE);
		}
	}

	/* flush socket related info */
	flush_sock_re ();
	flush_buf ();
	flush_auth ();

	/* read config */
	/* user and pass fixed length 4 */
	readconf ("config/user.conf", true_user);
	readconf ("config/pass.conf", true_pass);
	if (debug) fprintf (stderr, "\x1b[31m""*[m user='[34m%s[m' pass='[34m%s[m'\n""\x1b[m", true_user, true_pass);

	/* create socket */
#ifdef LSOCK_USE_IPv4
	listenfd = Socket (AF_INET, SOCK_STREAM, 0);
#else
	listenfd = Socket (AF_INET6, SOCK_STREAM, 0);
#endif
	if (debug) printf ("[31m*[m initialized socket\n");

	/* fill in sockaddr */
#ifdef LSOCK_USE_IPv4
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	serv_addr.sin_port = htons(port);
#else
	serv_addr.sin6_family = AF_INET6;
	//serv_addr.sin6_addr.s6_addr = htonl(INADDR_ANY);
	inet_pton (AF_INET6, "::0", &serv_addr.sin6_addr);
	serv_addr.sin6_port = htons(port);

#endif

	/* fill server ipv4 addr and port info */
#ifdef LSOCK_USE_IPv4
	inet_ntop (AF_INET, &serv_addr.sin_addr, saddr, sizeof(serv_addr));
	sport = ntohs (serv_addr.sin_port);
#else
	inet_ntop (AF_INET6, &serv_addr.sin6_addr, saddr, sizeof(serv_addr));
	sport = ntohs (serv_addr.sin6_port);
#endif

	/* use socket option SO_REUSEADDR | SO_REUSEPORT */
	int _flag = 1;
	int _optlen = sizeof(int);
	if (setsockopt (listenfd, SOL_SOCKET, SO_REUSEADDR, &_flag, _optlen) == -1) {
		perror ("setsockopt");
		exit (EXIT_FAILURE);
	}

	/* bind */
	Bind (listenfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr));
	if (debug) printf ("[31m*[m bind sucess\n");
	
	/* listen */
	Listen (listenfd, 5);
#ifdef LSOCK_USE_IPv4
	if (debug) printf ("[31m*[m listenning on %s:%d ...\n",
			   saddr , ntohs(serv_addr.sin_port));	
#else
	if (debug) printf ("[31m*[m listenning on [%s]:%d ...\n",
			   saddr , ntohs(serv_addr.sin6_port));	
#endif


	/* prepare signal actions */
	(void) signal(SIGINT, do_sigint);
	(void) signal(SIGCHLD, do_sigchld);

	/* standalone loop */
	while (1) {
		cli_len = sizeof(clie_addr);
		/* if no client connects the server, 
		   the function will block server */
		connfd = Accept(listenfd,
				(struct sockaddr *)&clie_addr, &cli_len);
		/* get client addr and port info */
#ifdef LSOCK_USE_IPv4
		rport = ntohs (clie_addr.sin_port);
		inet_ntop (AF_INET, &clie_addr.sin_addr.s_addr, raddr,
			sizeof(clie_addr));
#else
		rport = ntohs (clie_addr.sin6_port);
		inet_ntop (AF_INET, &clie_addr.sin6_addr.s6_addr, raddr,
			sizeof(clie_addr));
#endif
		if (debug) printf ("[31m*[m accept client from %s:%d\n",
				   raddr, rport);

		/* fork the server client,
		   the parent process closes connfd and listen to other
		   clients, the child process do service matter and exit*/
		if ( (c_pid = Fork()) == 0) {
			/* c_pid in parent process will not be 0,
			   so it will not step in here.
			   c_pid in child process will be 0 or -1(error),
			   so code here tells child what to do */
			/* listen mode off */
			Close (listenfd);
			/* write welcome message back */
			write (connfd, BANNER, sizeof(BANNER));
			/* start do_serv loop, until instruction
			   'quit' is recieved */
			do_serv (stdin, connfd); 
			/* had recieved the 'quit' instruction, do_serv
			   loop was broke. then write the BYE_BYE message */
			write (connfd, BYE_MSG, sizeof(BYE_MSG));
			/* close connfd and exit */
			Close (connfd);
			exit (EXIT_SUCCESS);
		}
		/* parent process will not step into the if () code block,
		   so parent should just close connfd, and let the child
		   do_serv */
		Close (connfd);
	}

	Close (listenfd);
	return 0;
}

/* service matter */
int
do_serv (FILE *fp, int connfd)
{
	/* both for select */
	int maxfdp1;
	fd_set rset, wset;

	FD_ZERO (&rset);
	FD_ZERO (&wset);

/* do_serv() infinite loop */
	while (1) {
		/* prepare set for select */
		FD_SET (connfd, &rset);
		FD_SET (connfd, &wset);
		maxfdp1 = connfd + 1;

/* STAGE 1 : select and read the connfd */
		/* if read instruction from client success ,
		   print instruction and write feed back */

		/* block at Select until connfd is readable */
		if (select (maxfdp1, &rset, NULL, NULL, NULL) == -1) {
			perror ("select");
			exit (EXIT_FAILURE);
		}

		readn = read(connfd, inst, 1023);
		if ( readn >= 0) {
			/* print conn info */
			fprintf (stdout, "- %s:%d -> %s: INST %s",
				 raddr, rport, "Server" , inst);
			/* print the feed back in buffer,
			   then write to connfd, default on */
			//snprintf (feed, 1023, "RECV %s", inst);
			snprintf (feed, 1023, "--- RECV INST ---\n");
			if (select (maxfdp1, NULL, &wset, NULL, NULL) == 0) {
				perror ("select");
				exit (EXIT_FAILURE);
			}
			write (connfd, feed, strlen(feed));
		} else {/* (readn < 0) */ 
			perror ("read");
			exit (EXIT_FAILURE);
		}
		/* if went here, server should have recieved something */

/* STAGE 2 : parse instruction and respond */
		inst_parse (inst, argv0, argv1);
		
		/* block until connfd is write-able */
		if (select (maxfdp1, NULL, &wset, NULL, NULL) == 0) {
			perror ("select");
			exit (EXIT_FAILURE);
		}

		/* compare parsed instruction with some commands */
		if (!strncmp(argv0, "GET", 3)) {
			write (connfd, HTML, sizeof(HTML));
		} else if (strncmp(argv0, "quit", 4)==0 ||
			   strncmp(argv0, "QUIT", 4)==0) {
			write (connfd, BYE_MSG, sizeof(BYE_MSG));
			Close (connfd);
			exit (EXIT_SUCCESS);
		} else if (!strncmp(argv0, "USER", 4)) {
			if (strlen(argv1)>0) strncpy (auth_user, argv1, 4);
			auto_auth ();
		} else if (!strncmp(argv0, "PASS", 4)) {
			if (strlen(argv1)>0) strncpy (auth_pass, argv1, 4);
			auto_auth ();
		} else if (!strncmp(argv0, "SEC", 3)) {
			if (auth_st > 0) {
				write (connfd, SECRET, sizeof(SECRET));
			} else if (auth_st <= 0) {
				write (connfd, SEC_FAIL, sizeof(SEC_FAIL));
				printf ("+ [31mWARN[m: %s attempted to read SEC but failed\n",
					raddr);
			}
		} else if (!strncmp(argv0, "LOGOUT", 6)) {
			auth_st = -1;
			flush_auth ();
#define LOGOUT "--- Logging out ---\n"
			write (connfd, LOGOUT, sizeof(LOGOUT));
		} else {
			/* instruction not supported */
#define INST_NA "--- Instruction Not Supported ---\n"
			write (connfd, INST_NA, sizeof(INST_NA));
			continue;
		}
/* End of Stage 2*/

		/* flush general buffers */
		flush_buf ();
	}
	return 0;
}

/* parse the instruction into argv0 and argv1 */
int
inst_parse (const char *src, char *argv0, char *argv1)
{
	sscanf (src, "%s %s", argv0, argv1);
	if (debug>1) printf ("+ argv0 [%s], argv1 [%s]\n", argv0, argv1);
	return 0;
}

/* when catched SIGINT */
void
do_sigint (int sig)
{
	printf ("\n[31m*[m Signal <[31mSIGINT[m>\n");
	exit (EXIT_SUCCESS);
}

/* verify and auth */
int
authenticate (int *state, const char *user, const char *pass)
{
	/* return value :
		1 || >1  auth success
	       -1 || <0  auth fail
	        0        jump over */

	/* step 1, correct state if need */
	if (*state < -1) {
		*state = -1;
		return 0;
	}
	else if (*state > 0) {
		/* authed succ */
		return 0;
	}

	/* step 2, auth */
	if (strncmp (user, true_user, sizeof(true_user)) == 0 &&
	    strncmp (pass, true_pass, sizeof(true_pass)) == 0) {
		*state = 1;
		return 1;
	} else {
		*state = -1;
		return -1;
	}
}

/* do_auth */
int
auto_auth (void)
{
	int _temp = 0;
	if (strlen(auth_user)>0 && strlen(auth_pass)>0) {
		_temp = authenticate(&auth_st, auth_user, auth_pass);
		if (_temp <= 0) {
#define AUTH_FAIL "--- Auth Failure ---\n"
			write (connfd, AUTH_FAIL, sizeof(AUTH_FAIL));
			flush_auth();
		} else {
			/* _temp > 0 */
#define AUTH_SUCC "--- Auth Success ---\n"
			write (connfd, AUTH_SUCC, sizeof(AUTH_SUCC));
			flush_auth();
		}
	}
	return 0;
}
