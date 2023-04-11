import torch as th
import time
from collections import defaultdict

def bench(m, repeat, q):
    print('Benchmarking for size {} matrix GEMM'.format(m).center(72, '_'))

    ta = time.time()
    th.set_default_tensor_type('torch.DoubleTensor')
    for _ in range(repeat):
        a = th.rand(m, m)
        c = th.rand(m, m)
        b = th.mm(a, c)
    te = time.time()-ta
    print('CPU Double:', te, 'size', m, 'repeat', repeat)
    q['CPU D'].append(te)
    
    ta = time.time()
    th.set_default_tensor_type('torch.cuda.DoubleTensor')
    for _ in range(repeat):
        with th.cuda.device(0):
            a = th.rand(m, m).cuda()
            c = th.rand(m, m).cuda()
            b = th.mm(a, c)
    te = time.time()-ta
    print('CUDA Double:', te, 'size', m, 'repeat', repeat)
    q['CUDA D'].append(te)
    
    ta = time.time()
    th.set_default_tensor_type('torch.FloatTensor')
    for _ in range(repeat):
        a = th.rand(m, m)
        c = th.rand(m, m)
        b = th.mm(a, c)
    te = time.time()-ta
    print('CPU Float:', te, 'size', m, 'repeat', repeat)
    q['CPU F'].append(te)
    
    ta = time.time()
    th.set_default_tensor_type('torch.cuda.FloatTensor')
    for _ in range(repeat):
        with th.cuda.device(0):
            a = th.rand(m, m).cuda()
            c = th.rand(m, m).cuda()
            b = th.mm(a, c)
    te = time.time()-ta
    print('CUDA Float:', te, 'size', m, 'repeat', repeat)
    q['CUDA F'].append(te)

repeat = 1000
#for m in (10, 100, 128, 300, 512):
#    bench(m, repeat)
#print('Benchmarking done'.format(m).center(72, '_'))

bench(128, 1, defaultdict(list))

## though you can parse the text with awk ...
def dumpq(q):
    print('CPU D\t CPU F\t CUDA D\t CUDA F')
    for i in range(len(q['CPU D'])):
        print(q['CPU D'][i],
              q['CPU F'][i],
              q['CUDA D'][i],
              q['CUDA F'][i])

print('finding the intersection')
qsmall = defaultdict(list)
for m in range(1, 384):
    bench(m, repeat, qsmall)
#print(qsmall)

qlarge = defaultdict(list)
for m in (128, 256, 384, 480, 512, 640, 720, 768, 960, 1024, 1280, 1366,
          1600, 1920, 2048, 2560, 4096, 8192):
    bench(m, 500, qlarge)

dumpq(qsmall)
dumpq(qlarge)
