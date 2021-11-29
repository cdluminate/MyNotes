#include <unistd.h>
#define class struct
class mystruct {
	void (* func)(void);
} test ;

void
hello (void)
{
	write (1, "hello\n", 7);
	return;
}

int
main (void)
{
	test.func = hello;
	test.func();
	return 0;
}
