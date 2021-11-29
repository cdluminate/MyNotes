#!/usr/bin/python3
import os
os.putenv('LD_LIBRARY_PATH', '.')
import ctypes

librmath = ctypes.CDLL('./librmath.so')
print(librmath.square(5))

class Point(ctypes.Structure):
    _fields_ = [('x', ctypes.c_double), ('y', ctypes.c_double)]

    def __str__(self):
        return 'Point(%f,%f)' % (self.x, self.y)

librmath.move_point.argtypes = (Point, ctypes.c_double, ctypes.c_double)
librmath.move_point.restype = Point
librmath.move_point_inplace.argtypes = (ctypes.POINTER(Point), ctypes.c_double, ctypes.c_double)
librmath.move_point_inplace.restype = None

p = Point(5.0, 1.0)
print(p)
p2 = librmath.move_point(p, 1.0, -1.0)
print(p2)


class Slice(ctypes.Structure):
    _fields_ = [('ptr', ctypes.POINTER(ctypes.c_int32)),
            ('len', ctypes.c_uint64)]

librmath.wrapper.restype = Slice

v = librmath.wrapper()
print(v)
print([v.ptr[i] for i in range(v.len)])
