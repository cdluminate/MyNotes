#include <stdio.h>
#include <unistd.h>
void foo(void)
{
	for (int i = 1; i < 10000; i++)
		for (int j = 1; j < 10000; j++)
			continue;
	return;
}
int main(void)
{
	foo();
	sleep(1);
	return 0;
}

/*

gcc -g a.c
valgrind --tool=callgrind ./a.out
callgrind_annotate callgrind.out.<pid> --tree=both
gprof2dot -f callgrind callgrind.out.<pid> | dot -Tsvg xxx.svg

http://valgrind.org/docs/manual/cl-manual.html#cl-manual.basics

 */
