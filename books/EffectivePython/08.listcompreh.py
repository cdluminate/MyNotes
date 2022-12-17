
matrix = [[1,2,3], [4,5,6], [7,8,9]]

flat = [x for row in matrix for x in row]
print(flat)

squared = [[x**2 for x in row] for row in matrix]
print(squared)

# when the data structure is more complex, straight for loops
# are clearer than list comprehensions
