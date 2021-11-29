import time
import functools
import numpy as np
import torch as th

N = 8192
matrices = [(np.random.rand(2,2), np.random.rand(2,2)) for _ in range(N)]

# Method A
time_start = time.time()
resultsA = tuple(map(lambda x:
        (th.from_numpy(x[0]).cuda() @ th.from_numpy(x[1]).cuda()), matrices))
time_end = time.time()
print(methodA := time_end - time_start)

# Method B
time_start = time.time()
resultsB = tuple(map(lambda x: (x[0] @ x[1]), matrices))
time_end = time.time()
print(methodB := time_end - time_start)

# Summary
print(functools.reduce(np.add, map(np.abs, (x[0].detach().cpu().numpy() 
        - x[1] for x in zip(resultsA, resultsB)))).sum())
print(methodA/methodB)
