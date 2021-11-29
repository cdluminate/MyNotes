cdef extern from "math.h":
  float sinf(float x)

def sin_cy3(float x):
  return sinf(x)
