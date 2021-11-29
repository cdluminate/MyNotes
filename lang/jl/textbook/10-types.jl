println("https://docs.julialang.org/en/latest/manual/types/")

(1+2)::Int64

function sinc(x)::Float64
    if x == 0
        return 1
    end
    return sin(pi*x)/(pi*x)
end

function myplus(x, y)
    x+y
end

function myplus(x::Int8, y::Int8)
    x+y
end

# composite types
struct Foo
    bar
    baz::Int
    qux::Float64
end

foo = Foo("Hello", 12, 3.)
typeof(foo)
foo.bar  # accessing field values

# mutable composite types
mutable struct Bar
    baz
    qux::Float64
end

bar = Bar("Hello", 0.);
bar.qux = 1.
bar.baz = 1//2

# parametric composite types
struct Point{T}
    x::T
    y::T
end

Point{Float64} <: Point

function norm2(p::Point{<:Real})  # p::Point{Real} is incorrect
    sqrt(p.x^2 + p.y^2)
end
norm2(Point{Float64}(3., 4.))

# custome pretty println
Base.show(io::IO, z::Point) = print(io, "Point(", z.x, ",", z.y, ")")
println(Point{Float64}(1.,2.))

# value types
struct Val{x}
end
Base.@pure Val(x) = Val{x}()
firstlast(::Val{true}) = "first"
firstlast(::Val{false}) = "last"
firstlast(Val(true))
firstlast(Val(false))