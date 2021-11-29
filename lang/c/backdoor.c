#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int
main (int argc, char ** argv, char ** envp)
{
  if (argc == 2) {
    printf ("we execve('/bin/bash', _argv, NULL). %s\n", argv[1]);
    setuid(geteuid());
    char * _argv[] = { "bash", NULL };
    execve ("/bin/bash", _argv, envp);
  } else {
    return 1;
  }
  return 0;
}
