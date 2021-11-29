function add2(x, y)
    x + y
end

add2(x, y) = x + y
println(add2(1, 2))

∑(x, y) = x + y

function g(x, y)::Int128
    x + y
end
println(typeof(g(1,2)), g(1,2))

# operators are functions
1 + 2 + 3
+(1,2,3)
f = +
f(1,2,3)

# operators with special names
hcat
vcat
hvcat
adjoint
getindex
setindex!
getproperty
setproperty!

# anonymous function
x -> x^2 +2x -1

function (x)
    x^2 + 2x - 1
end

map(x -> x^2, 0:9)

() -> 3  # zero argument function
(x, y, z) -> x^2 + y^2 + z^2

# tuple
(1, 1+1, 0., "hello")
t = (a=1, b=2)  # named tuple
t.a

function foo(x, y)
    return x+y, x*y
end
foo(2,3)

# argument destructing
myminmax(x, y) = (y < x) ? (y, x) : (x, y)
myrange((min, max)) = max - min
myrange(myminmax(2, 10))

# VA-args
bar(a, b, x...) = (a, b, x)
bar(1,2)
bar(1,2,3,4)
bar(1,2,(3,4,5,6,7)...)  # splat
bar([1,2,3,4,5,6]...)

# optional arguments
function Date(y::Int64, m::Int64 = 1, d::Int64 = 1)
    error === nothing || throw(:Xerror)
end
Date(2000)

# keyword arguments
function keywords(x, y; attr1="string", attr2=1)
    ###
end
keywords(1, 2, attr1="asdf")

map(x -> begin
    if x < 0 && iseven(x)
        return 0
    elseif x == 0
        return 1
    else
        return x
    end
end, [1,2,3])

# do x passes "x" as the first argument to the callable
map([1,2,3]) do x
    return x^2
end

open("junk", "w") do io
    write(io, "file write test")
end

# dot syntax
a = [0:10...]
sin.(a)
broadcast(sin, a)  # equivalent
broadcast((x, y) -> x+y, pi, [1,2,3])
broadcast((x, y) -> x*y, [1,2,3], [3,4,5])
b = Float32.([0:10...])
broadcast!(sin, b, b)

X = similar(b)  # pre-allocate output memory
@. X = sin(cos(b))