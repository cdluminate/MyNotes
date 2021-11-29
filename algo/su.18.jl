# [18](https://projecteuler.net/problem=18) / [67](https://projecteuler.net/problem=67)

#In a triangle like this:
#
#      a
#     b c
#    d e f
#    
#the best way to find the anwser is not to get the maximum from the summaries of
#all possible branches from top to bottom.
#
#There is such a recursive pattern
#
#a + max( b+max(b,c), c+max(e,f)
#
# tri.txt
#75
#95 64
#17 47 82
#18 35 87 10
#20 04 82 47 65
#19 01 23 75 03 34
#88 02 77 73 07 63 67
#99 65 04 28 06 16 70 92
#41 41 26 56 83 40 80 70 33
#41 48 72 33 47 32 37 16 94 29
#53 71 44 65 25 43 91 52 97 51 14
#70 11 33 28 77 73 17 78 39 68 17 57
#91 71 52 38 17 14 91 43 58 50 27 29 48
#63 66 04 68 89 53 67 30 73 16 69 87 40 31
#04 62 98 27 23 09 70 98 73 93 38 53 60 04 23

import Base.zero
zero(::SubString{String}) = 0 # Julia 0.5

ZeroString(::SubString{String}) = 0
ZeroString(x::Int64) = x

A = readdlm("tri.txt")
A = ZeroString.(A)

function myreduction(m)
	if size(m)[1] == 1
		return m[1,1]
	else
		mprime = m[1:(end-1), :]
		for k in 1:(size(m, 1)-1)
			mprime[size(mprime, 1), k] += max(
									 m[size(m, 1),k], m[size(m, 1),k+1])
		end
		return myreduction(mprime)
	end
end

println(myreduction(A))
