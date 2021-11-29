# https://docs.python.org/3/library/ctypes.html
# http://starship.python.net/crew/theller/ctypes/tutorial.html
import ctypes

libc = ctypes.cdll.LoadLibrary("libc.so.6")
libc = ctypes.CDLL("libc.so.6")

print(libc.getpid())

kernel = ctypes.CDLL("./kernel.so")
print(kernel.kernel(ctypes.c_char_p("hello python3 ffi to C library".encode())))

import cffi
ffi = cffi.FFI()
ffi.cdef("""
    int printf(const char *, ...);
""")
libc = ffi.dlopen(None)   # standard library
libc.printf("hello, %s!\n", ffi.new("char[]", ["world".encode()] )) #FIXME

