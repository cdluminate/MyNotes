# FIXME:: grooming


# --[ (a*b+c*d) -> muladd ]
# LJR

ex = :(a1*b1 + a2*b2 + a3*b3 + a4*b4)
# :(a1 * b1 + a2 * b2 + a3 * b3 + a4 * b4)

co = [Symbol.(ex.args[i].args[2:3]) for i in 2:length(ex.args)]
#4-element Array{Array{Symbol,1},1}:
# Symbol[:a1, :b1]
# Symbol[:a2, :b2]
# Symbol[:a3, :b3]
# Symbol[:a4, :b4]

res = Expr(:call, :*, co[end]...)
# :(a4 * b4)

for i in (length(co)-1):-1:1
    res = :(muladd( $(co[i]...), $res ))
end

res
#:(muladd(a1, b1, muladd(a2, b2, muladd(a3, b3, a4 * b4))))

function _muladd_transform(ex)
    if length(ex.args) == 2
        return ex.args[2]
    else
    a, b = ex.args[2].args[2:end]
    rest = _muladd_transform(Expr(ex.head, :+, ex.args[3:end]...))
    return :($(Base.muladd)($a, $b, $rest))
    end
end

function _muladd_rewrite(ex)
    co = [Symbol.(ex.args[i].args[2:3]) for i in 2:length(ex.args)]
    res = Expr(:call, :*, co[end]...)
    for i in (length(co)-1):-1:1
        res = :(muladd( $(co[i]...), $res ))
    end
    res
end

# Symbolic diff
# LJR

struct SymbolFun{T} end
SymbolFun(S::Symbol) = SymbolFun{S}()

D(ex::Symbol, x::Symbol) = ex == x ? 1 :0
D(ex::Number, x::Symbol) = 0

function D(ex::Expr, x)
    @assert ex.head == :call
    D(SymbolFun(ex.args[1]), ex.args[2:end], x)
end

D(fun::SymbolFun{T}, args, x) where T = error("string(T) function is not supported!")

# Power Rule
function D(::SymbolFun{:^}, args, x)
    a, b = args[1], args[2]
    da, db = D(a, x), D(b, x)
    if da == 0 && db == 0    # if a^b is constant: a^b -> 0
        return 0
    elseif db == 0           # if b is constant: a^b -> b*da*a^(b-1)
        return :( $b* $da * ($a ^ ($b - 1)) )
    else                     # a(x)^b(x) -> http://www.wolframalpha.com/input/?source=frontpage-immediate-access&i=d%2Fdx+a(x)%5Eb(x)
                             # I don't know, just ask Wolfram Alpha!
        :( $a ^ ($b - 1) * ($da * $b + $a * log($a) * $db) )
    end
end

# Product Rule
# d/dx (f * g) = (d/dx f) * g + f * (d/dx g)
# d/dx (f * g * h) = (d/dx f) * g * h + f * (d/dx g) * h + ...
function D(::SymbolFun{:*}, args, x)
    N = length(args)
    outer_args = Vector{Any}(N)
    for i in 1:N
        inner_args = Vector{Any}(N)
        for j in 1:N
            i == j ? inner_args[j] = D(args[j], x) : inner_args[j] = args[j]
        end
        outer_args[i] = Expr(:call, :*, inner_args...)
    end
    Expr(:call, :+, outer_args...)
end

# The Quotient Rule
# d/dx (f / g) = ((d/dx f) * g - f * (d/dx g)) / g^2
function D(::SymbolFun{:/}, args, x)
    f, g = args[1], args[2]
    df, dg = D(f, x), D(g, x)
    if df == 0 && dg == 0
        return 0
    elseif df == 0
        return :( -$dg * $f / $g^2 )
    elseif dg == 0
        return :( $df / $g )
    else
        return :( ($df * $g - $f * $dg) / $g^2 )
    end
end

function D(::SymbolFun{:+}, args, x)
    terms = Any[:+]
    for y in args
        dx = D(y, x)
        if dx != 0
            push!(terms, dx)
        end
    end
    if (length(terms) == 1)
        return 0
    elseif (length(terms) == 2)
        return terms[2]
    else
        return Expr(:call, terms...)
    end
end

function D(::SymbolFun{:-}, args, x)
    terms = Any[:-]
    term1 = D(args[1], x)
    push!(terms, term1)
    for y in args[2:end]
        dx = D(y, x)
        if dx != 0
            push!(terms, dx)
        end
    end
    if term1 != 0 && length(terms) == 2 && length(args) >= 2
        return term1
    elseif (term1 == 0 && length(terms) == 2)
        return 0
    else
        return Expr(:call, terms...)
    end
end

D(fun::SymbolFun{T}, args, x) where T = error("$(string(T)) function is not supported!")

[1:57] 
 ```julia> ex = :(11x^3 + 12 + 13x^5 + 14x^9)
:(11 * x ^ 3 + 12 + 13 * x ^ 5 + 14 * x ^ 9)

julia> Meta.show_sexpr(ex)
(:call, :+, (:call, :*, 11, (:call, :^, :x, 3)), 12, (:call, :*, 13, (:call, :^,
:x, 5)), (:call, :*, 14, (:call, :^, :x, 9)))```
