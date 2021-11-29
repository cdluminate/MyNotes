#!/usr/bin/python3.6
# some Python 3.6 features
# file:///usr/share/doc/python3.7/html/whatsnew/3.6.html

# -- PEP 498, Formatted string literals
import decimal

name = 'Fred'
print(f'His name is {name}')
width, precision, value = 10, 4, decimal.Decimal('12.34567')
print(f'result: {value:{width}.{precision}}')

# -- PEP 526, Syntax for variable annotations
from typing import *

primes: List[int] = []
captain: str

class Starship:
    stats: Dict[str, int] = {}
