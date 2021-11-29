# https://docs.julialang.org/en/stable/manual/integers-and-floating-point-numbers/
println(1 |> UInt8)
println(1 |> Int128)
println(1. |> Float16)
println(typeof(1))
println(Sys.WORD_SIZE)
println(typemin(UInt8), " ", typemax(UInt8))

println(bitstring(0.0))
println(eps(Float64))
println(eps(BigFloat))
println(nextfloat(0.0))

println(factorial(BigInt(40)))
println(parse(BigInt, "123123123123"))

x = 3
println(2x^2 -3x + 1)
println(2(x-1)^2)
println((x-1)x)

zero(Float64)
one(BigFloat)

