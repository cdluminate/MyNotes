#!/usr/bin/julia
# memscan.jl PID HEAD TAIL

pid = parse(Int64, ARGS[1])
head = parse(Int64, ARGS[2])
tail = parse(Int64, ARGS[3])
needle = Int64(233)

# open memory mapping
# cat /proc/pic/maps for mem info
mem = open("/proc/$(pid)/mem", "r")

for offset in head:0x8:tail-0x8
	seek(mem, offset)
	num = read(mem, Int64)
	if num == needle
		println(hex(offset), " ", num)
	else
		println(hex(offset), " ", num)
	end
end
