# https://docs.julialang.org/en/stable/manual/getting-started/
println(PROGRAM_FILE)

for x in ARGS
   println(x)
end

println("julia -p --procs N|auto")
