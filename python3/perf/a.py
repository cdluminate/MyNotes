import time
import functools
import numpy as np
import torch as th

margin = 0.2
N = 128
reps = th.rand(N, 512).cuda()

# Method A
time_start = time.time()
scoresA = th.zeros(N, N).to(reps.device)
__norm = functools.partial(th.nn.functional.normalize, p=2, dim=-1)
for i in range(N):
    for j in range(N):
        ri, rj = __norm(reps[i]), __norm(reps[j])
        scoresA[i,j] = 1 - ri.dot(rj)
time_end = time.time()
print(methodA := time_end - time_start)

# Method B
time_start = time.time()
reps_n = th.nn.functional.normalize(reps, p=2, dim=1)
scoresB = 1 - reps_n.mm(reps_n.t())
time_end = time.time()
print(methodB := time_end - time_start)

# Summary
print((scoresA - scoresB).norm())
print(methodA/methodB)
