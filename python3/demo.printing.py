#!/usr/bin/python3

import os
import sys

print('{:5d} {:7d}'.format(1, 2)) # both right aligh

print('{:<5d} {:>7d}'.format(1, 2)) # left, right

print('{:>5d} {:<7d}'.format(1, 2)) # right, left

'''

https://docs.python.org/3/library/string.html?highlight=string#module-string

"Harold's a clever {0!s}"        # Calls str() on the argument first
"Bring out the holy {name!r}"    # Calls repr() on the argument first
"More {!a}"                      # Calls ascii() on the argument first
'''
