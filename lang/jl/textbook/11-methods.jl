println("https://docs.julialang.org/en/latest/manual/methods/")

f(x::Float64, y::Float64) = 2x + y
f(2., 3.)

f(x::Number, y::Number) = 2x + y
f(2, 3.)

methods(f)
methods(+)

# parametric methods
same_type(x::T, y::T) where {T} = true
same_type(x, y) = false
same_type(1, 2)
same_type(1., 2)

myappend(v::Vector{T}, x::T) where {T <: Number} = [v..., x]
myappend([1,2,3], 4)


function matmul(A::AbstractMatrix, B::AbstractMatrix)
    op = (ai, bi) -> ai * bi + ai * bi
    R = promote_op(op, eltype(A), eltype(B))
    output = similar(B, R, (size(A, 1), size(B, 2)))
    if size(A, 2) > 0
        for j in 1:size(B, 2)
            for i in 1:size(B, 1)
                ab::R = a[i, 1] * b[1, j]
                for k in 2:size(A, 2)
                    ab += a[i, k] * b[k, j]
                end
                output[i, j] = ab
            end
        end
    end
    return output
end

# function-like objects
struct Poly{R}
    coef::Vector{R}
end

function (p::Poly)(x)
    v = p.coef[end]
    for i = (length(p.coef)-1):-1:1
        v = v*x + p.coef[i]
    end
    return v
end

p = Poly([1,10,100])
println(p(3))

function emptyfunction
end