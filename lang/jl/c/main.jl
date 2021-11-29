#!/usr/bin/julia
# http://julia.readthedocs.io/en/latest/manual/calling-c-and-fortran-code/

println(now())

# --[ ccall ]--
# you need to compile your library with -shared and -fPIC options.

# check libkernel.so first
if stat("./libkernel.so").inode == 0 then
   println(" => ./libkernel.so not found")
else
   println(" => ./libkernel.so found")
end

# handle the LD_LIBRARY_PATH environment
function getenv(name::AbstractString) # getenv(3)
   val = ccall( (:getenv, "libc.so.6"), Cstring, (Cstring,), name )
   if val == C_NULL then
      error("getenv: undefined variable: ", name)
   end
   bytestring(val) # use unsafe_string for julia 5.0
end
function setenv(name::AbstractString, value::AbstractString, overwrite::Int64) # setenv(3)
   val = ccall( (:setenv, "libc.so.6"), Int32, (Cstring, Cstring, Cint),
                name, value, overwrite)
   if val == -1 then
      error("setenv: failed")
   end
   val
end

println(" => SHELL ", getenv("SHELL"))
setenv("LD_LIBRARY_PATH", "./", 1)
println(" => LD_LIBRARY_PATH ", getenv("LD_LIBRARY_PATH"))

a = ccall( (:hello, "libkernel.so"), Int32, () )
println(a)

b = [ 1.0, 2.0, 3.0, 4.0, 5.0, -5.0 ]
println(sizeof(b), " ", length(b))
ccall( (:dvdump, "libkernel.so"), Void, (Ptr{Cdouble}, Csize_t), b, length(b))
a = ccall( (:dasum, "libkernel.so"), Float64, (Ptr{Cdouble}, Csize_t), b, length(b))
println(a)
a = ccall( (:pdasum, "libkernel.so"), Float64, (Ptr{Cdouble}, Csize_t), b, length(b))

b = zeros(1, 5)
ccall( (:boxmuller, "libboxmuller.so"), Ptr{Float64}, (Ptr{Cdouble}, Csize_t), b, length(b))
println(b)
println(length(b))
#for i = 1:length(b)
#   println(b[i])
#end
