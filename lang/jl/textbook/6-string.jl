AbstractString
println("all string types are subtypes of the abstract type AbstractString")
println(typeof('x'))
str = """asdfkasdf"quote" """
str = "hello, world\n"
for i in 1:length(str)
	println(str[i])
end
println(str[end-1])
println(str[2:4])

println("hello" * "world")  # string concatenation is noncommutative
println("interpolation $str")

println(occursin("a", "asdf"))
println(occursin("x", "sdf"))  # 'a' in 'sdf'
println(length(str))
println(repeat(str, 10))
println(join([str, str]))

println("Julia's regex is perl-compatible (PCRE)")
occursin(r"^\s*(?:#|$)", "not a comment")  # false
match(r"^\s*(?:#|$)", "# a comment")  # RegexMatch("#")
m = match(r"#", "#")
if m === nothing
	println("nothing")
else
	println(m)
end

println(replace("Programming Python", "Python" => "Julia"))
println("perlre(1)")
