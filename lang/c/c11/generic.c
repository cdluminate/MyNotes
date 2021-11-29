#include <stdio.h>

void foo_d(double a){ printf("d"); }
void foo_f(float a){ printf("f"); }
void foo_c(char a){ printf("c"); }
void foo_i(int a){ printf("i"); }
#define foo(X) _Generic((X), default: foo_i, \
	double: foo_d, float: foo_f, char: foo_c)(X)

int main(void){
	foo((double)0.); foo((float)0.); foo((char)0);
	return 0;
}
