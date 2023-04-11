push!(LOAD_PATH, ".")
using Test
using counter

@testset "Counter test" begin
	ctr = Counter()
	ctr.inc!(1)
	ctr.inc!(2)
	ctr.update!([1,1,1,1,1])
	ctr.update!([1,2,23,3,1])
	@test first(ctr.topk(3)[1]) == 1
end
