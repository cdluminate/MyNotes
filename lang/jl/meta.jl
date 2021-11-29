struct MyNumber
	x::Float64
end

for op in (:sin, :cos, :tan, :log, :exp)
	@eval Base.$op(a::MyNumber) = MyNumber($op(a.x))
end

x = MyNumber(π)
println(sin(x), cos(x), tan(x))
