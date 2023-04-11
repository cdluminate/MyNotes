
import torch as th
import time
m = 600

print('bench Double')
ta = time.time()
th.set_default_tensor_type('torch.DoubleTensor')
for i in range(m):
    a = th.rand(i+1, i+1)
    b = th.mm(a, a)
print('bench Double ..', time.time() -ta )

print('bench Float')
ta = time.time()
th.set_default_tensor_type('torch.FloatTensor')
for i in range(m):
    a = th.rand(i+1, i+1)
    b = th.mm(a, a)
print('bench Float ..', time.time() -ta )

'''
2520M, no env
bench Double .. 4.186146020889282
bench Float .. 2.6033060550689697

2520M OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 python3 cpu.mm.bench.py 
bench Double .. 2.879751205444336
bench Float .. 1.7010955810546875

6900K, no env
bench Double .. 5.657126426696777
bench Float .. 3.3477628231048584

6900K ➜  x OMP_NUM_THREADS=2 MKL_NUM_THREADS=2 python3 x.py
bench Double .. 5.15796160697937
bench Float .. 2.7169785499572754
6900k ➜  x OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 python3 x.py
bench Double .. 4.075693368911743
bench Float .. 1.7874641418457031
6900k ➜  x OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 python3 x.py
bench Double .. 2.804839849472046
bench Float .. 1.4415724277496338
6900k ➜  x OMP_NUM_THREADS=16 MKL_NUM_THREADS=16 python3 x.py
bench Double .. 5.056839942932129
bench Float .. 3.010272264480591
'''
