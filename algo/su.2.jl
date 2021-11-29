# Get the summary of some numbers in fibonacci sequence.
v = [1,1]
s = 0
while (v[end] < 4000000)
    if v[end]%2==0 s+=v[end] end
    push!(v, v[end]+v[end-1])
end
println(s)
# 4613732
