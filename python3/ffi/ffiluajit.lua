-- luajit FFI

local ffi = require 'ffi';

ffi.cdef [[
  int kernel (char * s);
]]
local kernel = ffi.load('kernel')
assert(kernel)

local msg = ffi.new('char [10]', 'ffiluajit')
print(kernel.kernel(msg))

