'''
The publisher-subscriber model
    PUB       SUB


'''
import sys
import zmq
import random
import time


__ADDRESS__ = 'tcp://127.0.0.1:5556'


def mainServer(argv):

    socket = zmq.Context().socket(zmq.PUB)
    socket.bind(__ADDRESS__)

    while True:
        time.sleep(0.1)
        x = random.randint(0, 100)
        y = random.random()
        msg = f'{x} {y}'

        print('<-', msg)
        socket.send_string(msg)


def mainClient(argv):

    socket = zmq.Context().socket(zmq.SUB)
    socket.connect(__ADDRESS__)

    socket.setsockopt_string(zmq.SUBSCRIBE, '50')

    for i in range(5):
        msg = socket.recv_string()
        x, y = msg.split()
        print('->', x, y)


if __name__ == '__main__':
    eval(f'main{sys.argv[1]}')(sys.argv[2:])
