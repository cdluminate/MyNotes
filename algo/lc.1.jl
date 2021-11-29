using Test

function twoSum(nums::Array{Int64,1}, target::Int64)
	d = Dict()
	for (i, x) in enumerate(nums)
		if get(d, target-x, -1) > 0
			return (get(d, target-x, nothing), i)
		end
		d[x] = i
	end
	(0, 0)
end

@test twoSum([3,2,4], 6) == (2,3)
@test twoSum([3,2,4], 9) == (0,0)
