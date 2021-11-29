# single line comment
#= multi
   line
   comments 
   https://learnxinyminutes.com/docs/julia/
=#

# -- types and operators --

3
3.2
2+1im
2//3 # rational

div(5,2) # 2
2^2 # 4
6%5 # 1

true
false

s = "string"
println(s[1]) # s, julia indexes from 1
println("expression in string $(s[3:4])")

@printf "%s\n" "hello"
println("println()")
println(bits(Int64(12345)))

λ = 1 # unicode characters are recognized

# -- variables and collections --

a = Int64[] # empty array
b = [4, 5, 6]
c = [4; 5; 6]
println(b[1], b[end])

mata = [1 2; 3 4] # 2x2 array
push!(a, 1) # add element to last position
push!(a, 2)
append!(a, b) # append b elements to a
pop!(b)
push!(b, 6)
shift!(a) # all elements move left and pop the first element
unshift!(a, 7) # all elements go right and put the element to head

arr = [5,4,6]
sort(arr) # will not change arr
sort!(arr) # arr will be changed

some_var = 5
try
	var_not_defined
	a[0]
	a[end+1]
catch e
	println(e)
end

a = [1:5;] # ~ Array(1:5)
a[1:3] # slicing
a[2:end] # slicing

in(1, [1,2,3]) # true
1 in [1,2,3] # true
length(a)

tup = (1,2,3) # tuples are immutable
x,y,z = tup # unpack tuples
(1,) != (1) # one-element tuple

d = Dict("one"=> 1, "two"=> 2)
d["one"]
keys(d)
values(d)
in(("one"=> 1), d) # true
in(("two"=> 3), d) # false
haskey(d, "one")
# d["four"] # ERROR
get(d, "one", 4) # 1
get(d, "four", 4) # 4

Set()
seta = Set([1,1,2,2,3,3]) # Set supports push!(), in() and so on ...
println(seta)
# intersect() union() setdiff()

# -- control flow --
if 1 < 2
	println("msg")
elseif 3 < 4
	println("ridiculous")
else
	println("else")
end

for fruit in ["apple", "peach", "banana"]
	println("$fruit is a kind of fruit")
end
for mapping in Dict("one"=> 1, "two"=> 2)
# for (k,v) in Dict("one"=> 1, "two"=> 2) # also works
	println("$(mapping[1]) => $(mapping[2])")
end

j = 1
while j < 4
	j+=j
end

try
	error("example error")
catch e
	println("caught $e")
end

# -- functions --
function add(x, y)
	println("adding $x and $y")
	x+y
end
add(5, 6)
f_add(x, y) = x+y # compact assignment of functions
f_foo(x, y) = x+y, x-y # returns a tuple

function va_args(args...)
	return args
end
va_args(1, 2, 3)

add([5,6]...) # equiv to add(5,6), the ... is called a splat.

function f_positional(a, b, x=5, y=6) # positional arguments
	return "$a $b and $x $y"
end
function f_keyword(; k1=4, name2="hello") # keyword argument
	return Dict("k1"=> k1, "name2"=> name2)
end

function create_adder(x) # Julia has first class functions
	adder = function (y)
		return x+y
	end
	return adder
end

println( (x -> x>2)(3) ) # true; this is stabby lambda syntax

map(+, [1,2,3,4]) # built-in higher order functions
filter(x -> x>5, [3,4,5,6,7])

println([(x -> x+1)(i) for i in [1, 2, 3]]) # list comprehensions

# -- types --
typeof(5) # Int64
type MyType
	real::Float64
	imag::Float64
	tag::AbstractString
	stub # same as stub::Any
end
aaa = MyType(0.1, 0.2, "test", 0)
bbb = typeof(aaa)(0, 0, "bbb", 0)

abstract Cat # just a name and node in the type hierarchy
println(subtypes(AbstractString))
println(super(Int64))

type Lion <: Cat # <: is the subtype operator
	name_color
	roar::AbstractString
end
Lion(roar::AbstractString) = Lion("gree", roar) # overloading constructor
type Panther <: Cat
	eye_color
	Panther() = new(green) # will only have this constructor
end

# -- multiple dispatch --
function meow(animal::Lion)
	animal.roar
end
function meow(animal::Panther)
	"grrr"
end
issubtype(Lion, Cat)

# -- under the hood
sqare_area(l) = l*l
code_native(sqare_area, (Int32,))
code_native(sqare_area, (Float64,))

# -- quick guide done
