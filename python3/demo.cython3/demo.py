#!/usr/bin/python3
'''
Reference:
Kurt W. Smith-Cython - A guide for Python programmers-O'Reilly (2015)
'''
import time
import math

class Timer(object):
  def __init__(self):
    self.stamp_start = 0.0
    self.stamp_stop = 0.0
  def start(self):
    self.stamp_start = time.time()
  def stop(self, task=''):
    self.stamp_stop = time.time()
    print('task %s costs time %f s.'%(task, self.stamp_stop - self.stamp_start))

def fib_py3(n):
  a, b = 0, 1
  for i in range(n):
    a, b = a+b, a
  return a

def sin_py3(vec):
  sin = math.sin
  return list(map(sin, vec))

def main():
  timer = Timer()
  n = 100000
  vec = list(range(2000000))
  vec = map(float, vec)

  timer.start()
  fib_py3(n)
  timer.stop('fib_py3')

  from fib_cy3 import fib_cy3
  timer.start()
  fib_cy3(n)
  timer.stop('fib_cy3')

  timer.start()
  sin_py3(vec)
  timer.stop('sin_py3')

  from sin_py3cy3 import sin_py3cy3
  timer.start()
  sin_py3cy3(vec)
  timer.stop('sin_py3cy3')

  from sin_cy3 import sin_cy3
  timer.start()
  list(map(sin_cy3, vec))
  timer.stop('sin_cy3')

if __name__ == "__main__":
  main()
