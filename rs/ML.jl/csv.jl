module csv
	using Random
	export load, iris

	function read(path::AbstractString; skipfirst=false)
		lines = readlines(path)[(skipfirst ? 2 : 1):end]
		lines = [split(x, '\t') for x in lines]
		lines = [replace(x, " " => "") for x in lines]
		[Array{Any}(x) for x in lines]
	end

	function iris(path::AbstractString = "iris.csv")
		dataset = read(path; skipfirst=true)
		labels = Set(x[end] for x in dataset)
		labelmap = Dict(v => k for (k,v) in enumerate(labels))
		for (i, entry) in enumerate(dataset)
			dataset[i][end] = labelmap[entry[end]]
		end
		dataset = [[(typeof(x) <: AbstractString) ? parse(Float32, x) : x for x in entry] for entry in dataset]
		dataset = transpose(hcat(dataset...))
		dataset = dataset[shuffle(1:150), :]
		trainset = dataset[1:120, :]
		valset   = dataset[121:135, :]
		testset  = dataset[136:150, :]
		return (trainset, valset, testset), labelmap
	end
end
