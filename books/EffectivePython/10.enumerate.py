
my_list = [ ... ]

# bad
for i in range(len(my_list)):
    item = my_list[i]

# better
for i, item in enumerate(my_list):
    print(i, item)

# let enumerate count from 1
for i, item in enumerate(my_list, 1):
    print(i, item)
