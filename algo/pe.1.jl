# [1](https://projecteuler.net/problem=1)

# \sum_i ia + \sum_j jb  \text{ ,where } i \neq nb , j \neq ma

@time s = sum([ i for i in filter(x -> (x%3==0) || (x%5==0), 1:999) ])
println(s)
# slow
# 233168

# equivalent to \sum_i ia + \sum_j jb - \sum_k kab
# where kab is the repeated numbers among ia and jb.

@time s = sum([ 3:3:999; 5:5:999; -(15:15:999) ])
println(s)
# fast
# 233168
