#include <iostream>

int
main (void)
{
	std::cout << sizeof(double);
    __asm__("int $0x3"); # SIGTRAP
    std::cout << sizeof(float);
	return 0;
}
