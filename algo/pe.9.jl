# a < b < c, a+b+c=1000
for a = 1:333 # 3a < a+b+c < 1000, a < 1000/3
	for c = 334:1000 # 3c > a+b+c = 1000, c > 1000/3
		b = 1000 -a -c
		if b <= 0 continue end
		if a^2 + b^2 == c^2
			println(a, '\t', b, '\t', c)
		end
	end
end
