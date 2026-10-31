function isPrime(n::Int)
	for i in 2:ceil(sqrt(n))
		if n%i==0 && n!=i return false end
	end
	return true
end
primes = [1,2,3]

ubound = 2000000
for i in 5:2:ubound
	if isPrime(i)
		push!(primes, i)
	end
end

println(sum(primes))
