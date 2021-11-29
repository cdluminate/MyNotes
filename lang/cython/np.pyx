'''
Must compile this file as np.so, or cpython would complain
dynamic module does not define module export function
'''
import numpy as np
cimport numpy as np

DType = np.int
ctypedef np.int_t DType_t

def asum(np.ndarray x):
    '''
    returns the sum of the absolute values of the given array
    '''
    assert x.dtype == DType
    cdef int N = x.size

    cdef DType_t s = 0
    for i in range(N):
        s += x[i] if x[i] > 0 else -x[i]
    return s
