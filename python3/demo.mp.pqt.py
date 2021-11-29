'''
http://www.cnblogs.com/284628487a/p/5590857.html
'''
import os
import sys

def spline(msg):
    return msg if len(msg)>72 else spline('-'+msg+'-')
p = lambda x: print(spline(x))


p('fork')
pid = os.fork() # UNIX only
if pid == 0:
    print('fork child')
    raise SystemExit
else:
    print('fork parent')

p('fork .. ok')


p('Process')
from multiprocessing import Process
def backjob(args):
    print('backjob: args=', args)
worker = Process(target=backjob, args=('test',))
worker.start()
worker.join()
p('Process .. ok')

# Pool for mass amount of subprocesses

p('Queue IPC')
from multiprocessing import Queue
import time
def populate(_q):
    for _ in range(10):
        print('{}: populate data and write to queue'.format(os.getpid()))
        _q.put(1)
        time.sleep(1)
qbuf = Queue()
worker = Process(target=populate, args=(qbuf,))
worker.start()
ta = time.time()
for _ in range(9):
    print('{}: consume data in the queue, {}'.format(os.getpid(), qbuf.get()))
    time.sleep(1)
print('time elapsed', time.time() -ta )
worker.join()
worker.terminate()
p('Queue IPC')

p('Serial')
ta = time.time()
for _ in range(9):
    print('{}: populate data and write to queue'.format(os.getpid()))
    time.sleep(1)
    print('{}: consume data in the queue'.format(os.getpid()))
    time.sleep(1)
print('time elapsed', time.time() -ta )
p('Serial - ok')
