#!/usr/bin/python3
# 2016 lumin, simple parallelization in python3

import time
import math

class Timer:
  def __init__(self):
    self.reset()
  def reset(self):
    self.start = 0.0
    self.end = 0.0
    self.interval = 0.0
  def set(self):
    self.start = time.time()
  def stop(self):
    self.end = time.time()
    self.interval = self.end - self.start
    print('costs time %f s' % self.interval)

number_tasks = 20000000

timer = Timer()
task = range(number_tasks)

print('I: using for-loop')
timer.set()
result1 = []
for i in task:
  result1.append(math.sin(i))
result1 = None
timer.stop()
#print(result1)

print('I: using map()')
timer.set()
result2 = list(map(math.sin, task))
result2 = None
timer.stop()
#print(result2)


print('I: using ThreadPool')
from multiprocessing.dummy import Pool as ThreadPool

timer.set()
pool = ThreadPool()
result3 = pool.map(math.sin, task)
result3 = None
pool.close()
pool.join()
timer.stop()

print('I: using Pool')
from multiprocessing import Pool

timer.set()
pool2 = Pool()
result4 = pool2.map(math.sin, task)
result4 = None
pool2.close()
pool2.join()
timer.stop()

print('I: create Pool with \'with\'')
timer.set()
with Pool() as pool6:
  result6 = pool6.map(math.sin, task)
timer.stop()

print('I: using one-line for')
timer.set()
result0 = [ math.sin(i) for i in range(number_tasks) ]
timer.stop()

print('I: two functions')
def myfun1(array):
  return [ math.sin(element) for element in array ]
def myfun2(array):
  sin = math.sin
  return [ math.sin(element) for element in array ]
def myfun3(array):
  return list(map(math.sin, array))
def myfun4(array):
  sin = math.sin
  return list(map(sin, array))
timer.set(); myfun1(task); timer.stop()
timer.set(); myfun2(task); timer.stop()
timer.set(); myfun3(task); timer.stop()
timer.set(); myfun4(task); timer.stop()

print('I: this technique is awesome!')
'''
def convert_image(imagepath):
  subprocess.call(['convert', '-resize', '64x64',
    imagepath, imagepath + '_'])

task = [ str(i)+'.jpg' for i in range(1, 2000+1)]
'''
