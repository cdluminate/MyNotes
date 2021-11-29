#!/usr/bin/python3.7
# some Python 3.7 features
# file:///usr/share/doc/python3.7/html/whatsnew/3.7.html

# -- PEP 557, Data Classes

from dataclasses import dataclass
@dataclass
class Point:
    x: float
    y: float
    z: float = 0.0

p = Point(1.5, 2.5)
print(p)
