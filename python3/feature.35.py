#!/usr/bin/python3.5
# file:///usr/share/doc/python3.7/html/whatsnew/3.5.html

# -- PEP 465, A dedicated infix operator for matrix multiplication
import numpy
x = numpy.ones(3)
y = numpy.eye(3)
print(y @ x)
print(x @ y)

# -- PEP 484, Type Hints
def greeting(name: str) -> str:
    return 'Hello ' + name
