function isPalin(n::Int)
	s = string(n)
	curl, curr = 1, length(s)
	while curl < curr
		if s[curl] != s[curr]
			return false
		end
		curl, curr = curl+1, curr-1
	end
	return true
end
#println(isPalin(9009))
#println(isPalin(9909))

function findLargestPalinProd(ubound::Int, lbound::Int)
	for n in ubound*ubound:-1:lbound*lbound
		if isPalin(n)
			# break into product of two 3-digit numbers
			for i in ubound:-1:lbound
				if n%ubound==0
					return (ubound, n/ubound)
				end
			end
		end
	end
end
#res = findLargestPalinProd(99,10) # 9009 = 99*91
res = findLargestPalinProd(999,100) # 90909 = 999*91
println(res, '\t', prod(res))
