function twoSum(nums, target)
	-- nums: Table[number]
	-- target: number
	m = {}
	for k, v in pairs(nums) do
		if nil == m[target - v] then
			m[v] = k
		else
			return {k, m[target - v]}
		end
	end
	return {-1, -1}
end

v = {2,7,11,15}
print(twoSum(v, 13))
