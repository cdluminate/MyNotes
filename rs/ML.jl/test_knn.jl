using LinearAlgebra

push!(LOAD_PATH, ".")
import csv
using knn

# sanity test

model = knnTrain(rand(10, 2), [1:10...]; k=1)
println(model.X, model.y)
println(knnClassify(model, [0.5,0.5]))
for i in 2:10
	model.k = i
	println(knnClassify(model, [0.5,0.5]))
end

## iris test

(trainset, valset, testset), labelmap = csv.iris()

model = knnTrain(trainset[:,2:end-1], trainset[:,end]; k=3)
pred = knnClassify(model, valset[:, 2:end-1])
accuracy = sum(pred .== valset[:,end]) / length(pred)
println("validation accuracy ", accuracy)
