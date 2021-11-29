'''
actually Queue() can be used without lock.
here the locks are used for demonstration
'''
import os
import sys
import time
from multiprocessing import Queue, Process, Lock, Manager, Pool

QLtasks = {'q': Queue(), 'l': Lock()}
QLresults = {'q': Queue(), 'l': Lock()}

# generate tasks
for i in range(100):
    QLtasks['q'].put(i)

# define worker function
def crunch(qlIn, qlOut) -> None:
    if qlIn['q'].empty(): return
    task = qlIn['q'].get()
    #print(os.getpid(), task)
    time.sleep(0.5)
    qlOut['q'].put([task, time.ctime()])
    #print(os.getpid(), 'task done')

workers = [Process(target=crunch, args=(QLtasks, QLresults)) for _ in range(7)]
for worker in workers: worker.start()
while True:
    for i, worker in enumerate(workers):
        if not worker.is_alive():
            worker.join()
            worker.terminate()
            workers[i] = Process(target=crunch, args=(QLtasks, QLresults))
            workers[i].start()
        else:
            pass

    if QLtasks['q'].empty(): break

    time.sleep(1e-3)
    print(QLresults['q'].qsize())

# examine the results
results = []
while not QLresults['q'].empty(): results.append(QLresults['q'].get())
print(results)
