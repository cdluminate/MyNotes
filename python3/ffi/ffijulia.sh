#!/bin/sh
set -e

export LD_LIBRARY_PATH=.

julia -e '
ret = ccall( (:kernel, "libkernel.so"), Int32, (Ptr{Cchar},), "hello julia ffi")'
