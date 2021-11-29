# Julia 0.6.2
import Base.*
using LinearAlgebra

× = *
ᵀ = transpose
(x)ᵀ = transpose(x)
⋅ = dot
∑(x) = reduce(+, x)
√(x) = sqrt(x)

# ascii and unicode euclidean distance implementation
euc_dist₁(x, y) = sqrt(sum((x-y).^2))
euc_dist₂(x, y) = √(∑((x-y)⋅(x-y)))

a, b = rand(5), rand(5)
println(euc_dist₁(a, b) - euc_dist₂(a, b))

# ascii and unicode cosine similarity implementation
⁻¹ = inv
(x)⁻¹ = 1/x
ϕ = norm
cos_dist₁(x, y) = dot(x, y) / (norm(x) * norm(y))
cos_dist₂(x, y) = (x ⋅ y) × ((ϕ(x) × ϕ(y))⁻¹)

println(cos_dist₁(a, b) - cos_dist₂(a, b))
