#!/usr/bin/python3.5
''' functional programming with python 
http://www.oreilly.com/programming/free/files/functional-programming-python.pdf
https://docs.python.org/3.5/howto/functional.html

-- functional style --
language features e.g. iterator, generator
library modules e.g. itertools, functools

each function operates on its input and produces some output.
functions that have no side effects at all are called pure functional.
avoiding side effects means not using data structures that get updated
as a program runs, and every function's output must only depend on its
input.

python programs written in functional style provide a functional-appearing
interface but will use non-functional features internally.

functional programming can be considered the opposite side of
object-oriented programming. objects are little capsules containing some
iternal state along with a collection of method calls that let you modify
this state.

functional design may seem like an odd constraint to work under. Why
you should avoid objects and side effects? these are theoretical advantages
to the functional style

    * formal provability
    * modularity
    * composability
    * ease of debugging and testing

'''

''' iterators '''
l = [ 1, 2, 3 ]
it = iter(l) # iterator object
it.__next__() # iteration ends with StopIteration exception
next(it) # equivalent to it.__next__()
for i in iter(l): print(i)
L = list(iter(l))
T = tuple(iter(l))
# there is no backward step or reset function for iterator.

# any python sequence type will automatically support creation of iterator.
m = { 'Jan': 1, 'Feb': 2, 'Mar': 3 }  
for key in m: print(key, m[key]) # the order is random
# appropriate iterator for dict: dict.values() dict.items()
L = [('Italy', 'Rome'), ('France', 'Paris'), ('US', 'Washington DC')]
dict(iter(L)) # dict constructor supports an iterator that returns (key,value pairs)

# list comprehensions and generator expressions are borrowed from Haskell
line_list = ['  line 1\n', 'line 2  \n']
stripped_iterator = (line.strip() for line in line_list) # returns iterator
stripped_list = [line.strip() for line in line_list] # returns list
stripped_list2 = [line.strip() for line in line_list if line != ""]
'''
generator expressions:
    (expression for expr1 in seq1 if condition1
            for expr2 in seq2 if condition2
            for ... in ... if ...)
e.g. obj_total = sum(obj.count for obj in list_all_objects())
'''
# the following is an example of list comprehension
a = [i*10+j for i in range(1,4) for j in range(1,6) if j%2 == 1]

''' generators '''
def generate_ints(N): # returns an iterator function
    for i in range(N):
        yield i # a function containing "yield" is a generator function
# more examples at testsuite: Lib/test/test_generators.py

''' built-in functions '''
list(map(str.upper, ['sentence', 'fragment']))
[s.upper() for s in ['sentence', 'fragment']]
list(filter(lambda x: ((x%2)==0), range(10)))
for i, line in enumerate(open(__file__, 'r')): print(i, line.strip())
# sorted() any() all() zip()

''' itertools '''
import itertools
# itertools.count(n) returns an infinite stream of integers
# itertools.cycle(content) returns an iterator that repeats the elements infinitely.
# itertools.repeat(content, n) repeats content for n times, or endlessly if n was omitted.
# ...
# itertools.combinations(iterable, r) gives all possible r-tuple of the elements in iterable
# itertools.permutations(iterable, r)
# itertools.groupby(iterable, key_func=None) collects all the consecutive elements from the underlying itertable that have the same key value

''' functools '''
import functools
# functools.partial(function, arg1, arg2, ...)
# functools.reduce(function, iterable, [initial_value]) # where the function takes two values

''' lambda expression '''
# https://docs.python.org/3.5/howto/functional.html#small-functions-and-the-lambda-expression

''' (extra) functional style algorithm '''
def fpsum(vec):
    if len(vec)==1:
        return vec[0]
    else:
        return vec[0]+fpsum(vec[1:])

print(fpsum(list(range(101))))
