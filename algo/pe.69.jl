# [69](https://projecteuler.net/problem=69)

#Euler totient function looks like
#```math
#\varphi(n) = n \prod_{p|n} ( 1 - \frac{1}{p} )
#```
#
#To find the solution n* which maximizes our object function
#```math
#\text{max} \frac{n}{\varphi(n)} = \frac{1}{ \prod\limits_{p|n} (1-\frac{1}{p}) }, n \leq 1000000
#```
#
#is equivalent to
#```math
#\text{min} \prod_{p|n} (1-\frac{1}{p}), n \leq 1000000
#```
#
#Distinct prime factors $`p_i \in \{p|n\}`$ are always positive integers that are larger than 1,
#hence $`0 < 1-\frac{1}{p} < 1`$ always holds. To minimize the above object function, we need
#as many distince prime factors as possible from the number n*. Now we comprehend this problem
#as to figure out a integer n* where n* <= 1000000 and has the most distinct prime factors
#among the ingeters less or equal to itself.
#
#Let's think about this problem in the reverse direction. The most ideal integer for this problem
#should ship all possible primes, e.g. $`n^* =\prod([2,3,5,7,11,\ldots])`$. Moreover, there are infinite
#number of primes, and the constraint $`n\leq 1000000`$ is exactly telling us when we should stop
#the infinite production.
#
for i in 1:20
    @printf "%d\t%8d\t%s\n" i prod(primes(i)) "$(prod(primes(i))<1_000_000)"
end

#Output
#```
#1	       1	true
#2	       2	true
#3	       6	true
#4	       6	true
#5	      30	true
#6	      30	true
#7	     210	true
#8	     210	true
#9	     210	true
#10	     210	true
#11	    2310	true
#12	    2310	true
#13	   30030	true
#14	   30030	true
#15	   30030	true
#16	   30030	true
#17	  510510	true
#18	  510510	true    *
#19	 9699690	false
#20	 9699690	false
#```
