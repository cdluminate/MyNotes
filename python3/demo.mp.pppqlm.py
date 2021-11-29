#!/usr/bin/python3
'''
multiprocessing

https://docs.python.org/3/library/multiprocessing.html?highlight=multiprocessing#module-multiprocessing
http://stackoverflow.com/questions/25557686/python-sharing-a-lock-between-processes
'''
from multiprocessing import Pool, Process, Queue, Pipe, Lock, Manager
import os

def f1(x):
  return x*x

def simple1():
  with Pool(5) as p:
    print(p.map(f1, [1, 2, 3]))

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f2(name):
    info('function f')
    print('hello', name)

def simple2():
    info('main line')
    p = Process(target=f2, args=('bob',))
    p.start()
    p.join()

def foo(q):
    q.put('hello')

def exchange1():
    q = Queue()
    p = Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()

def f4(conn):
    conn.send([42, None, 'hello'])
    conn.close()

def exchange2():
    parent_conn, child_conn = Pipe()
    p = Process(target=f4, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()

def f(l, i):
    l.acquire()
    try:
        print('hello world', i)
    finally:
        l.release()

def sync1():
    lock = Lock()
    for num in range(10):
        Process(target=f, args=(lock, num)).start()

def kernel(t):
    lock = t[0]
    task = t[1]
    counter = t[2]
    import time
    print(task)
    time.sleep(1)
    lock.acquire()
    try:
        counter[0] = counter[0] + 1
    finally:
        print('done', counter[0])
        lock.release()

def share1():
  with Manager() as manager:
    lock = manager.Lock()
    counter = manager.list([0])
    args = [ (lock, task, counter) for task in range(100) ]
    #print(args)
    with Pool(10) as p:
      p.map(kernel, args)

def share2():
  import time
  with Manager() as manager:
    lock = manager.Lock()
    counter = manager.list([0])
    args = [ (lock, task, counter) for task in range(100) ]
    #with Pool(100) as p:
    with Pool(20) as p:
      async_result = p.map_async(kernel, args)
      while not async_result.ready(): # ~ p.join
        print('manager: {} complete'.format(counter[0]))
        time.sleep(0.5) # print overall progress every 0.5 secs
      print(async_result.successful())

if __name__ == '__main__':
  print()
  simple1()
  print()
  simple2()
  print()
  exchange1()
  print()
  exchange2()
  print()
  sync1()
  print()
  share1()
  print()
  share2()
