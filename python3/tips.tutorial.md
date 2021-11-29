Pyhton 3 tutorial Note
---
> http://www.liaoxuefeng.com wiki : python tutorial
> python official introduction

list and tuple
```
a = [ ... ]
len(a)

b = ( .... ) # different from list, values in a tuple cannot be changed.
len(b)
```

dict
```
d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
if 'Thomas' in d:
```

set
```
>>> s = set([1, 1, 2, 2, 3, 3])
>>> s
{1, 2, 3}
```

stub function
```
def nop():
    pass
```

advanced feature
```
# slice
L[0:3]
L[:]

# iterate
from collections import Iterable
isinstance('abc', Iterable) # is string iterable

for i, value in enumerate(['A', 'B', 'C']):
  print(i, value)

for x, y in [(1, 1), (2, 4), (3, 9)]:
    print(x, y)

[x * x for x in range(1, 11)]
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

[m + n for m in 'ABC' for n in 'XYZ']
['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']

# generator
g = (x * x for x in range(10))
<generator object <genexpr> at 0x1022ef630>

''' another form of generator : using yield '''

# iterator
''' iterator can be handled by next(), it can be used to
    generate infinite number of data, while iterable objects
    cannot do the same '''
it = iter([1, 2, 3, 4, 5])
while True:
  try:
    x = next(it)
  except StopIteration:
    break
```

functional programming
```
# map/reduce
def f(x):
  return x * x
result = list(map(f, [ i in range(10) ]))
''' or list(map(lambda x: x*x, result)) '''

from functools import reduce
summary = reduce((lambda x,y: x+y), result)
# reduce: ((((x+y)+y)+y)+y)

# filter


def is_odd(n):
    return n % 2 == 1
list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))

# sorted
sorted()
```

python support for `lambda` expression is limited.

decorator
```
def ftrace(func):
  def wrapper(*args, **kw):
    print('%s():' % func.__name__)
    return func(*args, **kw)
  return wrapper
# equivalent to hello = ftrace(hello)
@ftrace
def hello():
  print('hello python')
```

module and package
```
create file __init__.py under package directory,
  which can be empty.

#!/usr/bin/python3
'''
document for this file
'''
import sys

__author__ = 'author'

def stub():
  pass

if __name__ == '__main__'
  stub()

```

object oriented programming (OOP)
```
class Student(object):
  def __init__(self, value=0):
    self.value = value
  def dump(self):
    print(self.value)
```

TODO

unittest, see [test.py](./test.py)  
