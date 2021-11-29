#!/usr/bin/python3
import pickle
from pprint import pprint

data = {'list': [1, 2.0, 3, 4+6j],
        'tuple': ('string', ),
        'set': {1,2,3},
        'constant': None,
        'bool': True,
        'dict': {'a':1, 'b':2} }

print(repr(pickle.dumps(data, protocol=0))) # dump string using ascii protocol
pickle.dump(data, open('data.pkl', 'wb+')) # using default protocol

data_restore = pickle.load(open('data.pkl', 'rb'))
pprint(data_restore)
