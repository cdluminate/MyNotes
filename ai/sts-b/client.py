import zmq
from zmq.utils import jsonapi

socket = zmq.Context().socket(zmq.REQ)
socket.connect('tcp://localhost:15555')

req = {'guid': 1,
        'sent1': 'Two zebra standing next to each other on a field.',
        'sent2': 'A man riding a motorcycle down the straight road.',
        }

while True:

    print('<-', req)
    socket.send(jsonapi.dumps(req))

    msg = socket.recv()
    print('->', jsonapi.loads(msg))
