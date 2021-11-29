#include <stdio.h>
#include <stdlib.h>

int
kernel (char * s)
{
  printf ("%s\n", s); // will not display in ctypes call
  return 42;
}
