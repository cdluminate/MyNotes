Introducing Python
===
> Oreilly, Bill Lubanovic  

# chapter2: py ingredients: numbers, strings, and variables

int division and float division
```
In [2]: 9/5
Out[2]: 1.8

In [3]: 9//5
Out[3]: 1
```

# chapter2: py filling: lists, tuples, dictionaries, and sets

list copying
```
a = [ 1, 2, 3 ]
b = a # surprise
c = a.copy()
d = list(a)
e = a[:]
```

```
a = [ ... ]
b = ...
c = ...
if len(set(map(len, [a, b, c]))) != 1:
  raise Expception
```

# chapter 4: py crust: code structures

Iterate multiple sequences with `zip()`.

function as closure
```
def a(string):
  def b():
    return "... %s" % string
  return b
```

generators
```
def my_range(first=0, last=10, step=1):
  number = first
  while number < last:
    yield number
    number += step

my_range # function
ranger = my_range(1, 5) # ranger is a generator
for x in ranger: # traversal
```

# chapter 5: py boxes: modules, packages, and programs

python standard library
```
handle missing keys with setdefault() and defaultdict()

count items with Counter()
  from collections import Counter
  breakfast = [ 'spam', 'eggs' , 'spam', 'spam' ]
  breakfast_counter = Counter(breakfast) -> Counter({ 'spam': 3, 'egg': 1 })

order by key with OrderedDict()
  from collections import OrderedDict

stack + queue = deque
  from collections import deque

  e.g.
  def palindrome(word):
    from collections import deque
    dq = deque(word):
    while len(dq) > 1:
      if dq.popleft() != dq.pop():
        return False
    return True

print nicely with pprint()
  from pprint import pprint
```

# chapter 6: objects and classes

get help fron the parent class with super
```
class Person():
  def __init__(self, name):
    self.name = name

class EmailPerson(Person):
  def __init__(self, name, email):
    super().__init__(name) # super() -> Person
    self.email = email
```

method types
```
class A():
  count = 0
  def __init__(self):
    A.count += 1
  def exclaim(self):
    print("I'm an A!")
  @classmethod
  def kids(cls):
    print(cls.count, ' A objects found')
  @staticmethod
  def commercial():
    print("hello")

A.commercial() # ok
a = A()
b = A()
A.kids() # 2
```

special methods
```
comparison
__eq__(self, other) self == other
__ne__
__lt__
__gt__
__le__
__ge__

math
__add__(self, other) self + other
__sub__
__mul__
__floordiv__ //
__truediv__ /
__mod__ %
__pow__ **

miscellaneous
__str__(self) str(self)
__repr__(self) repr(self)
__len__(self) len(self)
```

named tuples
```
from collections import namedtuple
Duck = namedtuple('Duck', 'bill tail')
duck = Duck('wide orange', 'long')
duck # Duck(bill='wide orange', tail='long')
duck.bill
duck.tail
```

# chapter7: mangle data like a pro

formating
```
print('{0:#^80s}'.format(' this is a comment line '))
```

regular expressions.

pack and unpack
```
import struct
struct.pack('>L', 154) # > for little-endian, L for 4-byte long int

width, height = struct.unpack('>LL', data[16:24])
```

# chapter8: data has to go somewhere

### text/binary file input/output.

```
with open('file', 'w+') as f:
  f.write(msg)
```

### structured text files

```
import csv
v = [ [ 'a', 'b' ], [ 'c', 'd' ] ]
with open('junk', 'wt') as fout:
  csvout = csv.writer(fout)
  csvout.writerows(v)

import csv
with open('junk', 'rt') as fin:
  cin = csv.reader(fin)
  v = [ row for row in cin ]
```

xml. html.

json.
```
import json
json.dumps()
json.loads()
```

YAML.
```
import yaml
```

configuration files
```
import configparser
```

serializing binary blobs with pickle
```
import pickle
import datetime
now1 = datetime.datetime.utcnow()
pickled = pickle.dumps(now1)
now2 = pickle.loads(pickled)
now1
now2
```

### structured binary files

spreadsheets

HDF5

### relational databases

SQL, DB-API, SQLite, and so on.

### NoSQL data stores

dbm family, quick example
```
import dbm
db = dbm.open('definitions', 'c') # 'r' read, 'w' write, 'c' both

db['key'] = value # use it like a dictionary
len(db) # db size 1
db['key'] # lookup

db.close()
```

memcached, Redis (data structure server).

### full-text databases

e.g. Xapian

# chapter9: the web, untangled

web clients  
* test with telnet  
* python's standard web libraries: http, urllib  
* beyond the standard library: requests  

web servers  
* `python3 -m http.server`  
* WCGI  
* frameworks (e.g. `bottle`, `flask`)  
* (non-python) apache, nginx  

# chapter10: systems

```
import os   # system
import glob # list matching files
```

programs and processes
```
import subprocess
import multiprocessing
```

# chapter11: concurrency and networks

ZeroMQ is like a Lego set.

# chapter12: be a pythonista

pip, ipython

name and document

`if __name__=='__main__':`

test your code with `pylint, pyflakes, and pep8`.

test with unittest.

test with doctest.

test with nose. (simpler than unittest)

debug with pdb.

logging error messages.

optimize your code  
1. measure timing `from time import time`.  
2. algorithms and data structures.  
3. cython, numpy, and c extensions.  
4. pypy.  

```
from timeit import timeit

def make_list_1():
  result = []
  for value in range(1000):
    result.append()
  return result

def make_list_2():
  result = [ value for value in range(1000) ]
  return result

print('make_list_1 takes', timeit(make_list_1, number=1000), 'seconds')
print('make_list_2 takes', timeit(make_list_2, number=1000), 'seconds')
```

source control, git

clone this book: `git clone https://github.com/madscheme/introducing-python`.

# appendix A, python art

2-D graphics  
* imghdr (detects file type)  
* colorsys (converts color, e.g. RGB, YIQ, HSV, HLS)  
* PIL and Pillow  
* imagemagick  
* graphical user interface (GUI), e.g. tkinter  

3-D graphics and animation  
* panda3d  
* blender  
* maya  

Plots, graphs, visualization  
* matplotlib  
* ...  

# appendix B: py at work

pp. 353, pass

# appendix C: py Sci

pandas for messy data.

---

Marked as done. Dec 12 2016. Nice book.
