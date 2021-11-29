#!/usr/bin/python3
# http://numba.pydata.org/numba-doc/0.37.0/user/overview.html

import numba as nb
import numpy as np
import time

# jit decorator tells Numba to compile this function.
# The argument types will be inferred by Numba when function is called.
@nb.jit
def sum2d():
    arr = np.arange(65536).reshape(256,256)
    M, N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i,j]
    return result

def sum2d_plain():
    arr = np.arange(65536).reshape(256,256)
    M, N = arr.shape
    result = 0.0
    for i in range(M):
        for j in range(N):
            result += arr[i,j]
    return result

@nb.vectorize([nb.float64(nb.float64, nb.float64),
               nb.float32(nb.float32, nb.float32)])
def _vctadd(x, y):
    return x+y

def vctadd():
    x, y = np.arange(65536), np.arange(65536)
    return _vctadd(x, y)

def _vctadd_plain(x, y):
    return x + y

def vctadd_plain():
    x, y = np.arange(65536), np.arange(65536)
    return _vctadd_plain(x, y)

# @nb.jitclass

# @nb.cfunc

@nb.njit(parallel=True)
def prange_test():
    a = np.random.rand(65536)
    s = 0
    for i in nb.prange(a.shape[0]):
        s += a[i]
    return s

def prange_test_plain():
    a = np.random.rand(65536)
    s = 0
    for i in nb.prange(a.shape[0]):
        s += a[i]
    return s

# @nb.stencil

def compare(funname):
    eval(funname + '_plain')()
    eval(funname)()

    ts_plain = time.time()
    eval(funname + '_plain')()
    te_plain = time.time()

    ts_numba = time.time()
    eval(funname)()
    te_numba = time.time()

    print('> {}; plain: {}; +numba: {}'.format(funname, te_plain - ts_plain, te_numba - ts_numba))

compare('sum2d')
compare('vctadd')
compare('prange_test')
