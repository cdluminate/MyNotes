import torch as th
import time
m = 600

print('bench CUDA Double')
ta = time.time()
th.set_default_tensor_type('torch.cuda.DoubleTensor')
for i in range(m):
    with th.cuda.device(0):
        a = th.rand(i+1, i+1).cuda()
        b = th.mm(a, a)
print('bench Double ..', time.time() -ta )

print('bench CUDA Float')
ta = time.time()
th.set_default_tensor_type('torch.cuda.FloatTensor')
for i in range(m):
    with th.cuda.device(0):
        a = th.rand(i+1, i+1).cuda()
        b = th.mm(a, a)
print('bench Float ..', time.time() -ta )

'''
TitanX Pascal ➜  x python3 gpu.mm.bench.py 
bench CUDA Double
bench Double .. 1.8817291259765625
bench CUDA Float
bench Float .. 0.2785158157348633
'''
