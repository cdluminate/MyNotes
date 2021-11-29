#!/usr/bin/ptthon3

from functools import reduce

def fun(x):
  return x * x

a = [ i for i in range(10) ]
result = list(map(fun, a))
print(result)

print(reduce(lambda x,y: x+y, result))

def ftrace(func):
  def wrapper(*args, **kw):
    print('%s():' % func.__name__, end=' ')
    return func(*args, **kw)
  return wrapper

@ftrace
def hello():
  print('hello python')

hello()

def foo():
    print('asdf')
foo = ftrace(foo)
foo()

'''
http://mingxinglai.com/cn/2015/08/python-decorator/
'''
