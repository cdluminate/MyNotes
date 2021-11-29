'''
https://docs.python.org/3/reference/datamodel.html#object.__getitem__
'''
class XXX(object):
    def __init__(self):
        self.data = {int(i): str(i) for i in range(3)}
    def __len__(self):
        return len(self.data)
    def __getitem__(self, index):
        if index >= len(self): raise IndexError
        return self.data[index], index

x = XXX()
for v, i in x:
    print(v, i)
