## https://zhuanlan.zhihu.com/p/47592565


# Abstract types
abstract type AbstractNode end
abstract type AbstractOp end


# Tensor: Nodes in the Graph
mutable struct Tensor{T, OT} <: AbstractNode
	value::T
	grad::T
	via::OT

	Tensor(val::T) where T = new{T, Any}(val, zero(val), nothing)
	Tensor(val::T, grad::T) where T = new{T, Any}(val, grad, nothing)
	Tensor(val::T, via::OT) where {T, OT} = new{T, OT}(val, zero(val), via)
end

x1, x2 = Tensor(rand()), Tensor(rand())
println(x1, x2)

# Operator: Edges in the Graph
struct Operator{FT <: Function, ArgsT <: Tuple} <: AbstractOp
	f::FT
	b::FT
	args::ArgsT
end

# Impl. Operators
struct Linear <: Operator
end


function (*)(a::AbstractNode, b::AbstractNode)
	Node()
end


# __main__
y = x1 * x2


## intermediate nodes
#struct Node{FT <: Operator, ArgsT <: Tuple, KwargsT <: NamedTuple} <: AbstractNode
#	f::FT
#	args::ArgsT
#	kwargs::KwargsT
#end
#
#Node(f::Function, args, kwargs) = Node(TraitMethod(f), args, kwargs)
#Node(op, args) = Node(op, args, NamedTuple())
#
#struct CachedNode{NT <: AbstractNode, outT} <: AbstractNode
#	node::NT
#	output::outT
#end
#
#function CachedNode(f, args; kwargs...)
#	node = Node(f, args, kwargs.data)
#	output = forward(node)
#	CachedNode(node, output)
#end
#
## forward pass
#forward(op::Operator, args...; kwargs) = op(args...; kwargs...)
#value(x) = x
#value(x::Variable) = x.value
#value(x::CachedNode) = x.output
#forward(x) = x
#forward(x::Variable) = value(x)
#
## real operators
#struct Linear <: Operator
#	w::Matrix{Float32}
#	b::Vector{Float32}
#end
#(op::Linear)(x::Vector) = op.w * x + op.b
#
#println(Variable(2.0))
