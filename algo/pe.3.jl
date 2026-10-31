# N = 13195 # 29
 N = 600851475143 # 6857
ubound = Int(ceil(sqrt(N)))
if ubound%2 == 0
	ubound -= 1
end
lpf = 1

function isPrime(n::Int)
	for i in 2:ceil(sqrt(n))
		if n%i==0
			return false
		end
	end
	return true
end

while ubound > 1
	if N%ubound==0 && isPrime(ubound)
		lpf = ubound
		break
	end
	ubound -= 2
end
println(N, '\t', lpf)
