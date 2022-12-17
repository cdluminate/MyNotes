module counter
	import Base.print

	export Counter

	mutable struct Counter
		accumulator::Dict{Any,Integer}
		update!::Function
		inc!::Function
		topk::Function
	end

	function Counter()
		ctr = Counter(Dict(), update!, inc!, topk)
		ctr.update! = x -> update!(ctr, x)
		ctr.inc! = x -> inc!(ctr, x)
		ctr.topk = x -> topk(ctr, x)
		return ctr
	end

	function inc!(counter::Counter, key::Any)
		if key in keys(counter.accumulator)
			counter.accumulator[key] += 1
		else
			counter.accumulator[key] = 1
		end
	end

	function update!(counter::Counter, iter::Base.Generator)
		for x in iter
			inc!(counter, x)
		end
	end

	function update!(counter::Counter, arr::Array)
		for x in arr
			inc!(counter, x)
		end
	end

	function topk(counter::Counter, k::Integer)::Array
		sort!(collect(counter.accumulator), by=last, rev=true)[1:k]
	end
end
