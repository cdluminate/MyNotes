#!/usr/bin/python3
'''
Birthday attack against a fake hash function but the result is strange
'''
import time
import math
import random

class Timer(object):
  def __init__(self):
    self.start_ = 0.0
  def start(self):
    self.start_  = time.time()
  def end(self, task=''):
    print('%s costs time %f s'%(task, time.time()-self.start_))

def myhash(message):
  return (84589 * message + 45989)%217728

def main():
  timer = Timer()

  # select M, find M'
  timer.start() 
  m = random.randint(0, 217728)
  hm = myhash(m)
  print('message %d hash %d'%(m, hm))
 
  for i in range(217728 ** 2):
    if myhash(i) == hm and i != m:
      print('collision detected at %d with hash %d'%(i, myhash(i)))
      break
  timer.end('method 1')

  # select M and M'
  timer.start()
  while True:
    m1 = random.randint(0, 217728 ** 2)
    m2 = random.randint(0, 217728 ** 2)
    print('trying %d and %d'%(m1, m2))
    if myhash(m1) == myhash(m2) and m1 != m2:
      print('collision detected at %d and %d with hash %d'%(m1, m2, myhash(m1)))
      break
  timer.end()

main()
