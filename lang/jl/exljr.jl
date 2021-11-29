#!/usr/bin/julia
# julia examples from LJR

f(x) = x^2 * cos(x)*tan(x)*besselj(x, 1.5)

@time println(f(2.5))
@time println(f(2.5))

A = rand(3, 3)
A * A
A .* A

A = rand(100, 10)
b = rand(100)
@time A\b
@time A\b

x = 10
println(2x)

x = y = z = 10
println( :(x=y=z=10) )
println( typeof( :(x=y=z=10) ))

println( :(x^2x) )
println( :(x^2*x) )
println( :(2x) )

println( macroexpand( :(@evalpoly x 2 3) ) )

println( @evalpoly x 1 2 3 )
println( 1 + 2x + 3x^2 )

function f(n)
   sum(0:3:n) + sum(0:5:n) - sum(0:15:n)
end

@time println( f(Int128(2)^64))
@time println( f(Int128(2)^64))

function nextfib(n)
   a, b = zero(n), one(n)
   while b < n
      a, b = b, a+b
   end
   return b
end

@time println( nextfib( Int128(2)^120 ))
@time println( nextfib( Int128(2)^120 ))

@code_llvm nextfib( Int128(2)^120 )

nheads = @parallel (+) for i=1:200000000
   Int(rand(Bool))
end
println(nheads)

x = 0
@simd for i=1:20000000
   x += Int(rand(Bool))
end
println(x)

a = SharedArray(Float64, 10)
@parallel for i=1:10
   a[i] = i
end
println(a)

#using Threads
#
#println(Threads.nthreads())
#Threads.@threads for i = 1:10
#   a[i] = Threads.threadid()
#end
#println(a)

#using ArrayFire
#a = rand(AFArray{Float32}, 100, 100)
#@time a^log(a)
#@time a^log(a)

x1 = rand(1000000);
x2 = rand(1000000);
@time dot(x1, x2);
