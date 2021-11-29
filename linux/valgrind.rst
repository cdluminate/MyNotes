Valgrind tips
=============

Reference: http://valgrind.org/docs/manual/quick-start.html

::

  #include <stdlib.h>

  void f(void)
  {
     int* x = malloc(10 * sizeof(int));
     x[10] = 0;        // problem 1: heap block overrun
  }                    // problem 2: memory leak -- x not freed

  int main(void)
  {
     f();
     return 0;
  }

then run command::

  valgrind --leak-check=yes myprog
