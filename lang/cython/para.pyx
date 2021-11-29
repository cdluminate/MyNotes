from cython.parallel import parallel, prange
from libc.stdio cimport printf
cimport openmp

# http://docs.cython.org/en/latest/src/userguide/parallelism.html

def main():

    cdef int num_threads
    openmp.omp_set_dynamic(1)
    with nogil, parallel():
        num_threads = openmp.omp_get_num_threads()
        printf('%d ', num_threads)
