#!/usr/bin/env python3

'''
https://www.zhihu.com/question/48755767#answer-47628816
https://www.zhihu.com/question/23760468#answer-5661732
https://stackoverflow.com/questions/101268/hidden-features-of-python#101276
https://www.zhihu.com/question/57470958#answer-56901848
https://zhuanlan.zhihu.com/p/28008875
'''

                                                            # problem example 1
a = 4.2
b = 2.1
print((a+b)==6.3) # False

                                                                       # tips 1
L = [ i*i for i in range(5) ]
for idx,value in enumerate(L, 1): # index starts from 1
    print(idx, ':', value)

                                                                       # tips 2

# for item in L[::-1]:
for item in reversed(L):
    print(item)

                                                                       # tips 3
# for row in rows:
#   if row[1]==0 and row[9] != 'YES':
#     return True
# return False
# -> return any(row[1]==0 and row[9] != 'YES' for row in rows)

                                                                       # tips 4
# raise SystemExit('It failed')

                                                                       # tips 5
# if not os.path.exists('myfile'):
#   with open('myfile', 'wt') as f:
#     f.write('content\n')
# else:
#   print('file already exists')
# -> with open('myfile', 'xt') as f:
#      f.write('content\n')

                                                                       # tips 6
# port = kwargs.get('port')
# if port is None:
#   port = 3306
# -> port = kwargs.get('port', 3306)

# -> last = L.pop()
                                                                       # tips 7
#d = {}
#for key,value in pairs:
#    if key not in d:
#        d[key] = []
#    d[key].append(value)
# ->
#d = defaultdict(list)
#for key,value in pairs:
#    d[key].append(value)

#d = defaultdict(int)
#for line in file:
#    for word in line.strip().split():
#        d[word] += 1
# See also: collections.Counter
#word_count = Counter()
#for line in file:
#  word_count.update(line.strip().split())

#result = sorted(zip(d.values(), d.keys(), reverse=True))[:3]
#for val,key in result: print(key, val)
# ->
# for key,val in word_count.most_common(3): print(key,val)

                                                                       # tips 8
#namedtuple

                                                                       # tips 9
#from threading import Thread
#import time
#import random
#from queue import Queue
#
#queue = Queue(10)
#
#class ProducerThread(Thread):
#    def run(self):
#        nums = range(5)
#        global queue
#        while True:
#            num = random.choice(nums)
#            queue.put(num)
#            print('produced', num)
#            time.sleep(random.random())
#
#class ConsumerThread(Thread):
#    def run(self):
#        global queue
#        while True:
#            num = queue.get()
#            queue.task_done()
#            print('consumed', num)
#            time.sleep(random.random())
#
#ProducerThread().start()
#ConsumerThread().start()

# from multiprocessing import Pool
# from multiprocessing.dummy import Pool

                                                                      # tips 10
# decorator: TODO

                                                                      # tips 11
# simple factory
class Shape(object): pass
class Circle(Shape): pass
class Square(Shape): pass

for name in ('Circle', 'Square'):
    cls = globals()[name]
    obj = cls()

                                                                     # tips 2/1
class ObjectDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
    def __setattr__(self, name, value):
        self[name] = value

                                                                     # tips 3/1
# context manager
class OpenContext(object):
    def __init__(self, filename, mode):
        self.fp = open(filename, mode)
    def __enter__(self):
        return self.fp
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fp.close()
# with OpenContext('/tmp/a', 'a') as f:
#   f.write('hello')

                                                                     # tips 4/1
# save memory with __slots__
class Foo(object):
    __slots__ = ['id', 'caption', 'url']
    '''
    use __slots__ when the attributes of the class is fixed.
    Then python will not use a dict to store the attributes, but with a list.
    '''
    def __init__(self, id, caption, url):
        self.id = id
        self.caption = caption
        self.url = url

                                                                     # misc
a = 1
b = 4
c = [b,a][a>b]

import random
a = [random.randint(0,9) for _ in range(10)]
a.sort(key=lambda x:x)
a = [(random.randint(0,9), random.random()) for _ in range(20)]
a.sort(key=lambda x: (x[0], x[1]))

class Test:
    def __init__(self):
        for i in range(10):
            exec("self.p{} = lambda: print({})".format(i, i))
        for i in range(10): exec("self.p{}".format(i))
x = Test()
x.p0()
x.p9()

list_1 = [[1, 2], [3, 4, 5], [6, 7], [8], [9]]
list_2 = []
for x in list_1: list_2 += x
list_2 = [elem for group in list_1 for elem in group]
sum(list_1, [])

from functools import reduce
reduce(lambda x,y: x+y, list_1)

for i in [1,1,2]:
    if i == 0: break
else:
    print('i \\neq 0 \\forall i')
for i in [1,1,0]:
    if i == 0: break
else:
    print('i \\neq 0 \\forall i')

4<6<8
4<6<1

import copy
list_x = copy.copy(list_1)

def genlist(x=[], e=None):
    x.append(e)
    return x
l1 = genlist(e=1)
print(l1)
l2 = genlist(e=2) # not expected
print(l1, l2)

# optimizing loops: get avoid of many point operations
l = []
append = l.append
for i in range(10): append(i)


a = [1,2,3]
b = [4,5,6]
z = list(zip(a, b)) # [(1, 4), (2, 5), (3, 6)]
z = list(zip(*z)) # [(1, 2, 3), (4, 5, 6)]

from itertools import islice
  # grouping adjacent list items
list(zip(*([iter(range(6))]*1))) #[(0,), (1,), (2,), (3,), (4,), (5,)]
list(zip(*([iter(range(6))]*2))) #[(0, 1), (2, 3), (4, 5)]
list(zip(*([iter(range(6))]*3))) #[(0, 1, 2), (3, 4, 5)]

list(zip(*(islice(list(range(6)), i, None, 3) for i in range(3))))
#[(0, 1, 2), (3, 4, 5)]
list(zip(*(islice(list(range(6)), i, None, 2) for i in range(2))))
#[(0, 1), (2, 3), (4, 5)]
list(zip(*(islice(list(range(6)), i, None, 1) for i in range(1))))
#[(0,), (1,), (2,), (3,), (4,), (5,)]


  # sliding windows (n-grams)
list(zip(*(islice(range(6), i, None) for i in range(1))))
#[(0,), (1,), (2,), (3,), (4,), (5,)]
list(zip(*(islice(range(6), i, None) for i in range(2))))
#[(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]
list(zip(*(islice(range(6), i, None) for i in range(3))))
#[(0, 1, 2), (1, 2, 3), (2, 3, 4), (3, 4, 5)]
list(zip(*(islice(range(6), i, None) for i in range(4))))
#[(0, 1, 2, 3), (1, 2, 3, 4), (2, 3, 4, 5)]

  # invert a dict
d = {i: i**2 for i in range(10)}
#{0: 0, 1: 1, 2: 4, 3: 9, 4: 16, 5: 25, 6: 36, 7: 49, 8: 64, 9: 81}
di = dict(zip(d.values(), d.keys()))
#{0: 0, 1: 1, 4: 2, 9: 3, 16: 4, 25: 5, 36: 6, 49: 7, 64: 8, 81: 9}

  # flatten a list
flat = lambda f: [e for l in f for e in flat(l)] if type(f) is list else [f]
flat([1,[2], [3, [4]]]) #[1, 2, 3, 4]
flat([1,[2], [3, [4, [5,6,7]]], [[8,9]]]) #[1, 2, 3, 4, 5, 6, 7, 8, 9]

  # LEGB rule: local, enclosing, global, built-in

a = (i for i in range(10000)) # fast creation, slow traversal
b = [i for i in range(10000)] # slow creation, fast traversal


# https://gist.github.com/JeffPaine/6213790
