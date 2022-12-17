
def sort_priority(values, group):
    ''' python support clusores:
    functions that refer to variables from the scope in which
    they were defined.
    '''
    def helper(x):
        if x in group:
            return (0, x)
        return (1, x)
    values.sort(key=helper)

numbers = [8,3,1,2,5,4,7,6]
group = {2,3,5,7}
sort_priority(numbers, group)
print(numbers)

def sort_priority2(numbers, group):
    found = False
    def helper(x):
        if x in group:
            found = True # seems simple
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

found = sort_priority2(numbers, group)
print('Found:', found) # the result is wrong
print(numbers)

# python's traversal order when looking for a variable
# 1. current function's scope
# 2. any enclosing scopes
# 3. global scope, i.e. the scope of the module
# 4. the built-in scope
# but assinging works differently

def sort_priority3(numbers, group):
    found = False
    def helper(x):
        nonlocal found                  # note this line
        if x in group:
            found = True # seems simple
            return (0, x)
        return (1, x)
    numbers.sort(key=helper)
    return found

found = sort_priority3(numbers, group)
print('Found:', found) # the result is wrong
print(numbers)

# sometimes the code gets complicated with nonlocal statement,
# in this case consider to define a class and store the states
# in the self.* namespace, and override __call__ method to
# make the class callable as a function.
