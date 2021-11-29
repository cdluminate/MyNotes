# Julia 0.6
function singleNumber(vector)
	reduce(xor, vector)
end

a = [1,1,2,3,3]
println(singleNumber(a))
