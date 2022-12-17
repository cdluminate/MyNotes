
names = ["Cecillia", "Lise", "Marie"]
letters = [len(x) for x in names]

# bad
for i, name in enumerate(names):
    count = letters[i]
    pass

# better
for name, count in zip(names, letters):
    pass
