module knn
	using LinearAlgebra
	using Statistics

	push!(LOAD_PATH, ".")
	import csv
	using counter	

	export KNN, knnTrain, knnClassify

	# Define the k-Nearest-Neighbor Model
	mutable struct KNN
		k::Integer            # The default number of neighbors
		metric::Function      # The default metric used to find neighbors
		X::Array              # Training data in shape (M, ...)
		y::Array              # Training label in shape (M,)
	end

	function knnTrain(X::Array, y::Array; k::Integer = 1,
					   metric::Function = (x,y)->(norm(x-y))) :: KNN
		if size(X, 1) != size(y, 1)
			throw(DimensionMismatch)
		end
		if size(X, 1) < k
			throw(BoundsError)
		end
		model = KNN(k, metric, X, y)
		return model
	end

	function knnClassify(knn::KNN, needle::Vector)::Integer
		scores = zeros(size(knn.X, 1))
		for i in 1:size(knn.X, 1)
			scores[i] = knn.metric(needle, knn.X[i,:])
		end
		argsort = sortperm(scores, rev=false)
		# Collect top-k results
		ctr = Counter()
		ctr.update!(knn.y[argsort[1:knn.k]])
		return first(first(ctr.topk(1)))
	end

	function knnClassify(knn::KNN, needles::Matrix)::Vector{Integer}
		results = zeros(Integer, size(needles, 1))
		for i in 1:size(needles, 1)
			results[i] = knnClassify(knn, needles[i, :])
		end
		return results
	end

	function knnRegression(knn::KNN, needle::Vector)::Real
		scores = zeros(size(knn.X, 1))
		for i in 1:size(knn.X, 1)
			scores[i] = knn.metric(needle, knn.X[i,:])
		end
		argsort = sortperm(scores, rev=false)
		return mean(knn.y[argsort[1:knn.k]])
	end

	function knnRegression(knn::KNN, needles::Matrix)::Vector{Real}
		results = zeros(Real, size(needles, 1))
		for i in 1:size(needles, 1)
			results = knnRegression(knn, needles[i, :])
		end
		return results
	end
end
