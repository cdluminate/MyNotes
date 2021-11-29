# compound expression
z = begin
    x = 1
    y = 2
    x + y
end

(x = 1;
 y = 2;
 x + y)

 # conditional evaluation
 function test(x, y)
    if x < y
        println("<")
        z = false
    elseif x > y
        println(">")
        z = false
    else
        println("=")
        z = true
    end
    z == true || println("no")  # if-blocks are leaky
end
test(1, 3)

begin
    x, y = 1, 2
    println(x < y ? "less" :
            x > y ? "greater" : "equal")
end

# short-circuit evaluation
false || (println("true"); true)
false && println("this won't be displayed")

function fact(n::Int)
    n >= 0 || error("n must be non-negative")
    n == 0 && return 1
    n * fact(n-1)
end
fact(5)

# repeated evaluation
i = 1
while i <= 5
    println(i)
    global i += 1
end

for i = 1:5
    if i == 1
        continue
    end
    println(i)
end

for i in 1:5
    println(i)
    if i > 2
        break
    end
end

for i ∈ ["foo", "bar"]
    println(i)
end

for i in 1:2, j in 3:4
    println((i,j))
end

# exceptions
try
    sqrt(-1)
catch e
    println("caught exception", e)
end

struct MyException <: Exception end
f(x) = x >= 0 ? x : throw(MyException())
f(-1)
f(1)

f(x) = try sqrt(x) catch sqrt(complex(x, 0)) end  # but exception is much slower than comparison
f(-1)

sqrt_second(x) = try
    sqrt(x[2])
catch y
    if isa(y, DomainError)
        sqrt(complex(x[2], 0))
    elseif isa(y, BoundsError)
        sqrt(x)
    end
end
sqrt_second([1 3])
sqrt_second(3)

fff = 1
try
    #
finally
    println(fff)
end

# tasks (aka coroutines)
function producer(c::Channel)
    put!(c, "start")
    for n in 1:4
        put!(c, 2n)
    end
    put!(c, "stop")
end
chnl = Channel(producer)
take!(chnl)

for x in Channel(producer)
    println(x)
end