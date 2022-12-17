
value = [len(x) for x in open('a large file')] # bad when file is large
print(value)

it_value = (len(x) for x in open('a large file')) # construct a generator
print(it_value)
print(next(it_value))
print(next(it_value))

# another powerful outcome of generator
roots = ((x, x**0.5) for x in it_value)
print(next(root))

