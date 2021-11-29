# PA = LU factorization, Julia 0.6
# L, U, P <- mylup( A )
# L, U, p <- lu( A )

# I don't know how to print a pretty matrix like that in REPL.
function pp(A, name)
	println("--- $(name) ---")
	for i in 1:size(A, 1)
		for j in 1:size(A,2)
			print(A[i,j], "  ")
		end
		println("")
	end
	println("---  ---  ---")
end
# TODO: use writedlm(STDOUT, matrix)

function mylup(A, debug=true)
	# FIXME: NO ARGUMENT CHECK
	P = eye(size(A, 1))
	L = eye(size(A,1))
	U = copy(A)
	if debug
		pp(P, "P orig")
		pp(L, "L orig")
		pp(U, "U orig")
	end

	# select the best pivot for the first row
	cursor = indmax(abs.(U[1:end,1]))
	P[[1,cursor],:] = P[[cursor,1],:]
	U[[1,cursor],:] = U[[cursor,1],:]
	if U[1,1] == 0
		error("Pivot is 0 at step 1, the matrix is singular")
	end
	if debug
		println("> round $(1), indmax $(cursor), exchange $(1),$(cursor)")
		pp(P, "P exchange")
		pp(U, "U exhange")
	end

	# process row 2:end
	for i in 2:size(A,1)

		# select pivot for row i, i > 1
		cursor = indmax(abs.(U[i:end,i])) +i-1
		P[[i,cursor],:] = P[[cursor,i],:]
		U[[i,cursor],:] = U[[cursor,i],:]
		if U[i,i] == 0
			error("Pivot is 0 at step $(i), the matrix is singular")
		end
		if debug
			println("> round $(i), indmax $(cursor), exchange $(i),$(cursor)")
			pp(P, "P exchange")
			pp(U, "U exhange")
		end

		for j in 1:i-1
			multiplier = U[i,j]/U[j,j]
			U[i,:] -= multiplier .* U[j,:]
			L[i,j] = multiplier
			if debug
				println("> multiplier $(multiplier), row$(i) - $(multiplier) * row$(j)")
				pp(U, "U mult")
				pp(L, "L mult")
			end
		end
	end
	if debug
		pp(P*A-L*U, "P*A-L*U")
		println(maximum(P*A-L*U), " XXX")
	end
	return L, U, P
end

function compare(a, debug=false)
	L, U, P = mylup(a, debug)
	println("size $(size(a)), norm (LU-PA) = $(norm(L*U - P*a)), max element diff $(maximum(L*U-P*a))")
end

a = [ 1.0 1 1; 1 1 3; 2 5 8] # FIXME: weirdly fails if this is Array{Int64,2} with bloody InexactError
compare(a, false)

b = [ 1 -1 0 0 ; -1 2 -1 0 ; 0 -1 2 -1; 0 0 -1 2 ]
compare(b, false)

x = 20
c = rand(x,x)
compare(c, false)

for s in 1:99
	A = rand(s, s)
	compare(A)
end
