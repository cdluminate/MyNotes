from libc.stdlib cimport atoi
from libc.math   cimport sin

cdef double f(double x):
    return sin(x*x)

def parse_charptr_to_pyInt(char* s):
    assert(s is not NULL)
    return atoi(s)

def basic():
    pass

def calling_c():
    print(parse_charptr_to_pyInt('1234'))
    print(f(3.14))

def using_c_lib():
    pass # TODO

def main():
    functions = [basic, calling_c, using_c_lib]
    for fun in functions:
        print(f'> Function {fun.__name__}(...)')
        fun()
