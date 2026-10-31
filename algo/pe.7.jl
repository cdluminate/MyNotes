function isPrime(n::Int)
	for i in 2:ceil(sqrt(n))
		if n%i==0 && n!=i return false end
	end
	return true
end

function nextPrime!(l)
	x = l[end]+2
	while !isPrime(x)
		x += 2
	end
	push!(l, x)
end

l = [2,3,5,7,11,13]
while length(l) < 10001
	nextPrime!(l)
end
println(length(l))
println(l[end])
