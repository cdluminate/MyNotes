# N = 10 # 2520
N = 20 # 232792560
function isPrime(n::Int)
	for i in 2:ceil(sqrt(n))
		if n%i==0 && i!=n return false end
	end
	return true
end
primes = [x for x in 1:N if isPrime(x)]
print(primes)

function factorize(n::Int)
	f = Int[]
	while n > 1
		for i in 2:n
			if n%i==0
				n /= i
				push!(f, i)
				break
			end
		end
	end
	f
end
#println(factorize(2520))

p = Dict((i, 0) for i in primes)
for i in 1:N
	s = factorize(i)
	c = Dict((i,0) for i in primes)
	for j in s
		c[j] += 1
	end
	for (k,v) in c
		p[k] = max(p[k], v)
	end
end
println(p)
prod_p = 1
for (k, v) in p
	prod_p *= k^v
end
println(N, '\t', prod_p)
