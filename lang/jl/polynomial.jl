# using Julia 0.6.2
iter = 100
println("$(iter) iterations for each n")
for n in (10,50,100,150,200,300,400,500,10000,20000,50000,100000)
	# construct the polynomial
	A = randn!(Array{Float64}(n+1)) # coefficients of the polynomial
	T = Array{Float64}(0)
	# run several times and find the mean time
	for i in 1:iter
		X = fill!(Array{Float64}(n+1), 1)
		x = Float64(rand()) # parameter of the polynomial
		tic()
		for j in 2:n+1
			X[j] = x * X[j-1]
		end
		P_x = dot(A, X)
		push!(T, toq())
	end
	Tmean = mean(T)
	println("n = $(n) \t\tTmean = $(Tmean)")
end

#using Julia 0.6.2
iter = 100
println("$(iter) iterations for each n")
for n in (10,50,100,150,200,300,400,500,10000,20000,50000,100000)
	# construct the polynomial
	A = randn!(Array{Float64}(n+1))
	T = Array{Float64}(0)
	# run several times and find the mean time
	for i in 1:iter
		x = Float64(rand())
		P_x = 0.
		tic()
		for j in 1:n+1
			P_x += A[j] * x^(j-1)
		end
		push!(T, toq())
	end
	Tmean = mean(T)
	println("n = $(n) \t\tTmean = $(Tmean)")
end

#using Julia 0.6.2
iter = 100
println("$(iter) iterations for each n")
for n in (10,50,100,150,200,300,400,500,10000,20000,50000,100000)
	# construct the polynomial
	A = randn!(Array{Float64}(n+1))
	T = Array{Float64}(0)
	# run several times and find the mean time
	for i in 1:iter
		x = Float64(rand())
		P_x = 0.
		xj = 1.
		tic()
		for j in 1:n+1
			P_x += xj * A[j]
			xj *= x
		end
		push!(T, toq())
	end
	Tmean = mean(T)
	println("n = $(n) \t\tTmean = $(Tmean)")
end

#using Julia 0.6.2
iter = 100
println("$(iter) iterations for each n")
for n in (10,50,100,150,200,300,400,500,10000,20000,50000,100000)
	# construct the polynomial
	A = randn!(Array{Float64}(n+1))
	T = Array{Float64}(0)
	# run several times and find the mean time
	for i in 1:iter
		x = Float64(rand())
		P_x = A[end]
		tic()
		for j in n:-1:1
			P_x = x * P_x + A[j]
		end
		push!(T, toq())
	end
	Tmean = mean(T)
	println("n = $(n) \t\tTmean = $(Tmean)")
end
